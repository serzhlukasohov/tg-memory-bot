"""Tests for ARQ worker pipeline — all external services mocked."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_message, make_session, SAMPLE_STRUCTURED


def _make_ctx(redis=None):
    return {"redis": redis or AsyncMock()}


class TestConsumeStream:
    # consume_stream is an infinite loop that catches CancelledError internally.
    # We test it by running it as a task and cancelling it after assertions.

    async def test_processes_messages_from_stream(self):
        import asyncio
        from src.tasks import consume_stream

        redis = AsyncMock()
        redis.xgroup_create = AsyncMock(side_effect=Exception("group exists"))

        payload = {
            "msg_id": 1,
            "chat_id": -100123,
            "date": "2026-05-27T10:00:00+00:00",
            "text": "test",
            "author_id": 1,
            "author_name": "Alice",
            "has_media": False,
            "media_type": None,
            "grouped_id": None,
            "reply_to_msg_id": None,
        }

        call_count = [0]
        processed = asyncio.Event()

        async def mock_xreadgroup(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [("tg:incoming", [(b"1-0", {"data": json.dumps(payload)})])]
            processed.set()
            await asyncio.sleep(10)  # block until task is cancelled
            return []

        redis.xreadgroup = mock_xreadgroup
        redis.xack = AsyncMock()

        mock_repo = AsyncMock()
        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=mock_repo):
                task = asyncio.create_task(consume_stream(_make_ctx(redis)))
                await asyncio.wait_for(processed.wait(), timeout=2.0)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        mock_repo.upsert.assert_called_once()

    async def test_acknowledges_processed_messages(self):
        import asyncio
        from src.tasks import consume_stream

        redis = AsyncMock()
        redis.xgroup_create = AsyncMock()

        payload = {
            "msg_id": 42, "chat_id": -100, "date": "2026-05-27T10:00:00+00:00",
            "text": "msg", "author_id": 1, "author_name": "A",
            "has_media": False, "media_type": None,
            "grouped_id": None, "reply_to_msg_id": None,
        }

        call_count = [0]
        acked = asyncio.Event()

        async def mock_xreadgroup(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [("tg:incoming", [("msg-id-1", {"data": json.dumps(payload)})])]
            acked.set()
            await asyncio.sleep(10)
            return []

        redis.xreadgroup = mock_xreadgroup
        redis.xack = AsyncMock()

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=AsyncMock()):
                task = asyncio.create_task(consume_stream(_make_ctx(redis)))
                await asyncio.wait_for(acked.wait(), timeout=2.0)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        redis.xack.assert_called_once_with("tg:incoming", "workers", "msg-id-1")


class TestBuildAndQueueSessions:
    async def test_archives_short_sessions(self):
        from src.tasks import build_and_queue_sessions

        now = datetime.now(timezone.utc)
        # 2 messages = less than MIN_SESSION_MESSAGES (3)
        msgs = [
            make_message(1, date=now - timedelta(hours=5)),
            make_message(2, date=now - timedelta(hours=4, minutes=50)),
        ]

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        msg_repo = AsyncMock()
        msg_repo.get_unassigned_since = AsyncMock(return_value=msgs)
        session_repo = AsyncMock()
        session_repo.create = AsyncMock(return_value=make_session())

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=msg_repo):
                with patch("src.tasks.SessionRepository", return_value=session_repo):
                    with patch("src.tasks.create_pool") as mock_pool:
                        mock_pool.return_value.__aenter__ = AsyncMock(return_value=AsyncMock())
                        mock_pool.return_value.__aexit__ = AsyncMock(return_value=False)
                        mock_pool.return_value.aclose = AsyncMock()
                        await build_and_queue_sessions(_make_ctx())

        # Session created with archived status
        create_call = session_repo.create.call_args
        assert create_call.args[0]["status"] == "archived"

    async def test_skips_when_no_eligible_messages(self):
        from src.tasks import build_and_queue_sessions

        msg_repo = AsyncMock()
        msg_repo.get_unassigned_since = AsyncMock(return_value=[])

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=msg_repo):
                with patch("src.tasks.SessionRepository"):
                    await build_and_queue_sessions(_make_ctx())

        # Should return early without creating sessions
        msg_repo.get_unassigned_since.assert_called_once()

    async def test_skips_when_already_locked(self):
        """If another cron run holds the lock, skip silently."""
        from src.tasks import build_and_queue_sessions

        redis = AsyncMock()
        redis.set = AsyncMock(return_value=None)  # lock not acquired
        redis.delete = AsyncMock()
        ctx = {"redis": redis}

        with patch("src.tasks.async_session_factory") as mock_factory:
            await build_and_queue_sessions(ctx)

        mock_factory.assert_not_called()
        redis.delete.assert_not_called()


class TestProcessSession:
    async def test_marks_session_as_processing_then_processed(self):
        from src.tasks import process_session

        session = make_session(session_id=1, retry_count=0, tg_msg_ids=[1, 2, 3])
        messages = [make_message(i) for i in range(3)]

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)
        mock_db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))))

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.update_status = AsyncMock()
        session_repo.increment_retry = AsyncMock(return_value=1)

        msg_repo = AsyncMock()
        msg_repo.get_by_ids = AsyncMock(return_value=messages)

        item_repo = AsyncMock()
        item_repo.get_open_questions = AsyncMock(return_value=[])
        item_repo.get_open_actions = AsyncMock(return_value=[])
        item_repo.create_many = AsyncMock()

        log_repo = AsyncMock()
        log_repo.log = AsyncMock()

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository", return_value=msg_repo):
                    with patch("src.tasks.KnowledgeItemRepository", return_value=item_repo):
                        with patch("src.tasks.ProcessingLogRepository", return_value=log_repo):
                            with patch("src.tasks.structure_session", new_callable=AsyncMock,
                                       return_value=SAMPLE_STRUCTURED):
                                with patch("src.tasks.generate_startup_context", new_callable=AsyncMock,
                                           return_value="# Context"):
                                    with patch("src.tasks.write_session_to_github", new_callable=AsyncMock,
                                               return_value="sessions/2026-05-27-10-01.md"):
                                        with patch("src.tasks.write_session_to_notion", new_callable=AsyncMock,
                                                   return_value=("notion-page-id", ["item-1"])):
                                            with patch("src.tasks.get_session_github_url",
                                                       return_value="https://github.com/test"):
                                                with patch("src.tasks.create_pool") as mock_pool:
                                                    mock_pool.return_value.aclose = AsyncMock()
                                                    await process_session(_make_ctx(), 1)

        # First call must be "processing", last call must be "processed"
        status_calls = session_repo.update_status.call_args_list
        assert status_calls[0].args[1] == "processing"
        assert status_calls[-1].args[1] == "processed"

    async def test_skips_when_session_not_found(self):
        from src.tasks import process_session

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=None)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository"):
                    with patch("src.tasks.KnowledgeItemRepository"):
                        with patch("src.tasks.ProcessingLogRepository"):
                            await process_session(_make_ctx(), 999)

        session_repo.update_status.assert_not_called()

    async def test_marks_failed_when_max_retries_exceeded(self):
        from src.tasks import process_session

        session = make_session(session_id=1, retry_count=3)  # already at max

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.update_status = AsyncMock()

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository"):
                    with patch("src.tasks.KnowledgeItemRepository"):
                        with patch("src.tasks.ProcessingLogRepository"):
                            with patch("src.tasks._notify_failure", new_callable=AsyncMock):
                                await process_session(_make_ctx(), 1)

        # Must set status to "failed" (not just contain the word)
        status_values = [c.args[1] for c in session_repo.update_status.call_args_list]
        assert "failed" in status_values

    async def test_increments_retry_on_error(self):
        from src.tasks import process_session

        session = make_session(session_id=1, retry_count=0)
        messages = [make_message(i) for i in range(3)]

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)
        mock_db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))))

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.increment_retry = AsyncMock(return_value=1)
        session_repo.update_status = AsyncMock()

        msg_repo = AsyncMock()
        msg_repo.get_by_ids = AsyncMock(return_value=messages)

        item_repo = AsyncMock()
        item_repo.get_open_questions = AsyncMock(return_value=[])
        item_repo.get_open_actions = AsyncMock(return_value=[])

        log_repo = AsyncMock()
        log_repo.log = AsyncMock()

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository", return_value=msg_repo):
                    with patch("src.tasks.KnowledgeItemRepository", return_value=item_repo):
                        with patch("src.tasks.ProcessingLogRepository", return_value=log_repo):
                            with patch("src.tasks.structure_session", side_effect=Exception("Claude down")):
                                with patch("src.tasks.create_pool") as mock_pool:
                                    pool_instance = AsyncMock()
                                    mock_pool.return_value = pool_instance
                                    pool_instance.enqueue_job = AsyncMock()
                                    pool_instance.aclose = AsyncMock()
                                    await process_session(_make_ctx(), 1)

        session_repo.increment_retry.assert_called_once_with(1)

    async def test_skips_when_already_locked(self):
        """If Redis lock is already held, process_session returns without doing anything."""
        from src.tasks import process_session

        redis = AsyncMock()
        redis.set = AsyncMock(return_value=None)  # lock NOT acquired
        redis.delete = AsyncMock()
        ctx = {"redis": redis}

        with patch("src.tasks.async_session_factory"):
            with patch("src.tasks.SessionRepository") as mock_repo_cls:
                await process_session(ctx, 99)

        mock_repo_cls.assert_not_called()
        redis.delete.assert_not_called()

    async def test_lock_released_even_on_error(self):
        """Lock is always released even when processing raises."""
        from src.tasks import process_session

        redis = AsyncMock()
        redis.set = AsyncMock(return_value=True)
        redis.delete = AsyncMock()
        ctx = {"redis": redis}

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(side_effect=Exception("DB exploded"))

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository"):
                    with patch("src.tasks.KnowledgeItemRepository"):
                        with patch("src.tasks.ProcessingLogRepository"):
                            # Exception propagates but lock must still be released
                            try:
                                await process_session(ctx, 1)
                            except Exception:
                                pass

        redis.delete.assert_called_once()

    async def test_skips_when_already_processed(self):
        """Idempotency: if session.status == processed, does nothing."""
        from src.tasks import process_session

        session = make_session(session_id=1, retry_count=0, status="processed")

        redis = AsyncMock()
        redis.set = AsyncMock(return_value=True)
        redis.delete = AsyncMock()
        ctx = {"redis": redis}

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.update_status = AsyncMock()

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository"):
                    with patch("src.tasks.KnowledgeItemRepository"):
                        with patch("src.tasks.ProcessingLogRepository"):
                            await process_session(ctx, 1)

        session_repo.update_status.assert_not_called()


class TestNotifyHelpers:
    async def test_notify_success_publishes_to_redis(self):
        from src.tasks import _notify_success
        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        await _notify_success(ctx, 1, SAMPLE_STRUCTURED, "https://github.com/test")

        redis.publish.assert_called_once()
        channel, message_str = redis.publish.call_args.args
        assert channel == "bot:notifications"
        message = json.loads(message_str)
        assert "text" in message
        assert "1" in message["text"]

    async def test_notify_failure_publishes_to_redis(self):
        from src.tasks import _notify_failure
        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        await _notify_failure(ctx, 42, "Something broke")

        redis.publish.assert_called_once()
        message = json.loads(redis.publish.call_args.args[1])
        assert "42" in message["text"]
        assert "Something broke" in message["text"]

    async def test_notify_failure_truncates_long_errors(self):
        from src.tasks import _notify_failure
        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        long_error = "x" * 1000
        await _notify_failure(ctx, 1, long_error)

        message = json.loads(redis.publish.call_args.args[1])
        assert len(message["text"]) < 800  # truncated to 500 + surrounding text
