"""Tests for admin bot command handlers — aiogram and deps mocked."""
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_session, SAMPLE_STRUCTURED


def _make_message(text: str) -> MagicMock:
    msg = MagicMock()
    msg.text = text
    msg.answer = AsyncMock()
    return msg


class TestCmdStatus:
    async def test_shows_pending_count_and_last_session(self):
        from src.bot.admin_bot import cmd_status
        message = _make_message("/status")
        session = make_session(
            structured_json=SAMPLE_STRUCTURED,
            started_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
        )

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.count_pending = AsyncMock(return_value=3)
        session_repo.get_last = AsyncMock(return_value=session)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_status(message)

        response = message.answer.call_args.args[0]
        assert "3" in response  # pending count
        assert "2026-05-27" in response

    async def test_shows_no_session_when_none_found(self):
        from src.bot.admin_bot import cmd_status
        message = _make_message("/status")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.count_pending = AsyncMock(return_value=0)
        session_repo.get_last = AsyncMock(return_value=None)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_status(message)

        message.answer.assert_called_once()


class TestCmdBackfill:
    async def test_queues_backfill_job_with_since_id(self):
        from src.bot.admin_bot import cmd_backfill
        message = _make_message("/backfill 12345")

        with patch("src.bot.admin_bot.create_pool") as mock_pool:
            pool_instance = AsyncMock()
            mock_pool.return_value = pool_instance
            pool_instance.enqueue_job = AsyncMock()
            pool_instance.aclose = AsyncMock()
            await cmd_backfill(message)

        pool_instance.enqueue_job.assert_called_once_with("run_backfill", 12345, None)

    async def test_backfill_defaults_to_zero_when_no_id_given(self):
        from src.bot.admin_bot import cmd_backfill
        message = _make_message("/backfill")

        with patch("src.bot.admin_bot.create_pool") as mock_pool:
            pool_instance = AsyncMock()
            mock_pool.return_value = pool_instance
            pool_instance.enqueue_job = AsyncMock()
            pool_instance.aclose = AsyncMock()
            await cmd_backfill(message)

        pool_instance.enqueue_job.assert_called_once_with("run_backfill", 0, None)

    async def test_backfill_returns_error_for_invalid_id(self):
        from src.bot.admin_bot import cmd_backfill
        message = _make_message("/backfill notanumber")

        await cmd_backfill(message)

        response = message.answer.call_args.args[0]
        assert "❌" in response

    async def test_backfill_accepts_date_string(self):
        from src.bot.admin_bot import cmd_backfill
        message = _make_message("/backfill 2024-01-15")

        with patch("src.bot.admin_bot.create_pool") as mock_pool:
            pool_instance = AsyncMock()
            mock_pool.return_value = pool_instance
            pool_instance.enqueue_job = AsyncMock()
            pool_instance.aclose = AsyncMock()
            await cmd_backfill(message)

        pool_instance.enqueue_job.assert_called_once_with("run_backfill", 0, "2024-01-15")

    async def test_backfill_rejects_invalid_date(self):
        from src.bot.admin_bot import cmd_backfill
        message = _make_message("/backfill 2024-99-99")

        await cmd_backfill(message)

        response = message.answer.call_args.args[0]
        assert "❌" in response


class TestRunBackfillTask:
    async def test_run_backfill_calls_core_and_notifies(self):
        from src.tasks import run_backfill

        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        with patch("src.backfill.backfill_core", new_callable=AsyncMock, return_value=42) as mock_core:
            await run_backfill(ctx, since_id=0, since_date_str=None, limit=0)

        mock_core.assert_called_once()
        assert redis.publish.call_count == 2  # start + complete notifications
        _, done_msg = redis.publish.call_args.args
        data = json.loads(done_msg)
        assert "42" in data["text"]

    async def test_run_backfill_with_date_parses_correctly(self):
        from datetime import timezone
        from src.tasks import run_backfill

        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        with patch("src.backfill.backfill_core", new_callable=AsyncMock, return_value=100) as mock_core:
            await run_backfill(ctx, since_id=0, since_date_str="2024-06-01", limit=0)

        call_kwargs = mock_core.call_args
        since_date = call_kwargs.kwargs.get("since_date") or call_kwargs.args[2]
        assert since_date.year == 2024
        assert since_date.month == 6
        assert since_date.tzinfo == timezone.utc

    async def test_run_backfill_notifies_on_failure(self):
        from src.tasks import run_backfill

        redis = AsyncMock()
        redis.publish = AsyncMock()
        ctx = {"redis": redis}

        with patch("src.backfill.backfill_core", new_callable=AsyncMock, side_effect=Exception("TG error")):
            with pytest.raises(Exception, match="TG error"):
                await run_backfill(ctx)

        # Should have published start + failure notifications
        assert redis.publish.call_count == 2
        _, fail_msg = redis.publish.call_args.args
        data = json.loads(fail_msg)
        assert data.get("error") is True
        assert "TG error" in data["text"]


class TestCmdRetry:
    async def test_requeues_session_for_processing(self):
        from src.bot.admin_bot import cmd_retry
        message = _make_message("/retry 5")
        session = make_session(session_id=5)

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.update_status = AsyncMock()

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                with patch("src.bot.admin_bot.create_pool") as mock_pool:
                    pool_instance = AsyncMock()
                    mock_pool.return_value = pool_instance
                    pool_instance.enqueue_job = AsyncMock()
                    pool_instance.aclose = AsyncMock()
                    await cmd_retry(message)

        pool_instance.enqueue_job.assert_called_once_with("process_session", 5)
        response = message.answer.call_args.args[0]
        assert "✅" in response

    async def test_returns_error_when_session_not_found(self):
        from src.bot.admin_bot import cmd_retry
        message = _make_message("/retry 999")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=None)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_retry(message)

        response = message.answer.call_args.args[0]
        assert "❌" in response
        assert "999" in response

    async def test_returns_error_for_invalid_session_id(self):
        from src.bot.admin_bot import cmd_retry
        message = _make_message("/retry abc")

        await cmd_retry(message)

        response = message.answer.call_args.args[0]
        assert "❌" in response

    async def test_requires_session_id_argument(self):
        from src.bot.admin_bot import cmd_retry
        message = _make_message("/retry")

        await cmd_retry(message)

        response = message.answer.call_args.args[0]
        assert "❌" in response
        assert "Usage" in response


class TestCmdLast:
    async def test_shows_session_summary(self):
        from src.bot.admin_bot import cmd_last
        message = _make_message("/last")
        session = make_session(
            structured_json=SAMPLE_STRUCTURED,
            started_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
            github_file_path="sessions/2026-05-27-10-01.md",
        )

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get_last = AsyncMock(return_value=session)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_last(message)

        response = message.answer.call_args.args[0]
        assert "2026-05-27" in response
        assert "high" in response
        assert "github.com" in response

    async def test_returns_not_found_when_no_sessions(self):
        from src.bot.admin_bot import cmd_last
        message = _make_message("/last")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get_last = AsyncMock(return_value=None)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_last(message)

        response = message.answer.call_args.args[0]
        assert "No processed sessions" in response

    async def test_shows_counts_for_all_item_types(self):
        from src.bot.admin_bot import cmd_last
        message = _make_message("/last")
        session = make_session(structured_json=SAMPLE_STRUCTURED)

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        session_repo = AsyncMock()
        session_repo.get_last = AsyncMock(return_value=session)

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.SessionRepository", return_value=session_repo):
                await cmd_last(message)

        response = message.answer.call_args.args[0]
        assert "2" in response   # 2 decisions
        assert "1" in response   # 1 question / 1 idea / 1 action


class TestListenNotifications:
    async def test_forwards_notifications_to_group(self):
        import asyncio
        import json
        from src.bot.admin_bot import listen_notifications

        async def mock_pubsub_listen():
            yield {"type": "subscribe", "data": None}
            yield {"type": "message", "data": json.dumps({"text": "✅ Session processed"})}
            # Pause so listen_notifications processes both messages before we cancel
            await asyncio.sleep(10)

        # redis.pubsub() must return synchronously (not a coroutine)
        pubsub = MagicMock()
        pubsub.subscribe = AsyncMock()
        pubsub.listen = mock_pubsub_listen

        redis = MagicMock()
        redis.pubsub = MagicMock(return_value=pubsub)

        with patch("src.bot.admin_bot.bot") as mock_bot:
            mock_bot.send_message = AsyncMock()
            task = asyncio.create_task(listen_notifications(redis))
            # Give it enough time to process the two messages
            await asyncio.sleep(0.1)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        mock_bot.send_message.assert_called_once()
        call_kwargs = mock_bot.send_message.call_args.kwargs
        assert "✅ Session processed" in call_kwargs.get("text", "")


class TestCmdActions:
    async def test_shows_open_actions(self):
        from src.bot.admin_bot import cmd_actions
        message = _make_message("/actions")

        item = MagicMock()
        item.id = 7
        item.text = "Set up Stripe"
        item.owner = "Bob"
        item.extra = {"due": "2026-06-01"}

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.get_open_actions = AsyncMock(return_value=[item])

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_actions(message)

        reply = message.answer.call_args.args[0]
        assert "#7" in reply
        assert "Set up Stripe" in reply
        assert "@Bob" in reply

    async def test_shows_no_actions_when_empty(self):
        from src.bot.admin_bot import cmd_actions
        message = _make_message("/actions")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.get_open_actions = AsyncMock(return_value=[])

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_actions(message)

        reply = message.answer.call_args.args[0]
        assert "No open" in reply


class TestCmdQuestions:
    async def test_shows_open_questions(self):
        from src.bot.admin_bot import cmd_questions
        message = _make_message("/questions")

        item = MagicMock()
        item.id = 3
        item.text = "Do we need SOC2?"
        item.owner = "Alice"

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.get_open_questions = AsyncMock(return_value=[item])

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_questions(message)

        reply = message.answer.call_args.args[0]
        assert "#3" in reply
        assert "SOC2" in reply


class TestCmdDone:
    async def test_marks_item_as_done(self):
        from src.bot.admin_bot import cmd_done
        message = _make_message("/done 7")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.close = AsyncMock(return_value="ok")

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_done(message)

        item_repo.close.assert_called_once_with(7)
        reply = message.answer.call_args.args[0]
        assert "✅" in reply
        assert "7" in reply

    async def test_returns_error_when_not_found(self):
        from src.bot.admin_bot import cmd_done
        message = _make_message("/done 999")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.close = AsyncMock(return_value="not_found")

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_done(message)

        reply = message.answer.call_args.args[0]
        assert "❌" in reply

    async def test_returns_info_when_already_closed(self):
        from src.bot.admin_bot import cmd_done
        message = _make_message("/done 5")

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        item_repo = AsyncMock()
        item_repo.close = AsyncMock(return_value="already_closed")

        with patch("src.bot.admin_bot.async_session_factory", return_value=mock_db):
            with patch("src.bot.admin_bot.KnowledgeItemRepository", return_value=item_repo):
                await cmd_done(message)

        reply = message.answer.call_args.args[0]
        assert "already" in reply.lower() or "ℹ️" in reply

    async def test_returns_error_for_missing_id(self):
        from src.bot.admin_bot import cmd_done
        message = _make_message("/done")
        await cmd_done(message)
        reply = message.answer.call_args.args[0]
        assert "❌" in reply
