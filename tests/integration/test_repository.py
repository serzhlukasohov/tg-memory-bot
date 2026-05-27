"""Tests for async repository CRUD — DB session fully mocked."""
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_message, make_session


def _make_db_session():
    db = AsyncMock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.add = MagicMock()
    db.add_all = MagicMock()
    db.refresh = AsyncMock()
    return db


class TestMessageRepository:
    async def test_upsert_creates_new_message_when_not_found(self):
        from src.db.repository import MessageRepository
        db = _make_db_session()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None  # not found
        db.execute.return_value = result

        repo = MessageRepository(db)
        data = {
            "msg_id": 999,
            "chat_id": -100123,
            "date": datetime(2026, 5, 27, tzinfo=timezone.utc),
            "text": "Hello",
            "author_id": 1,
            "author_name": "Alice",
            "has_media": False,
        }
        await repo.upsert(data)

        db.add.assert_called_once()
        db.commit.assert_called_once()

    async def test_upsert_updates_existing_message(self):
        from src.db.repository import MessageRepository
        db = _make_db_session()
        existing = MagicMock()
        existing.msg_id = 999
        result = MagicMock()
        result.scalar_one_or_none.return_value = existing
        db.execute.return_value = result

        repo = MessageRepository(db)
        data = {"msg_id": 999, "text": "updated"}
        await repo.upsert(data)

        db.add.assert_not_called()
        assert existing.text == "updated"

    async def test_get_by_ids_returns_messages(self):
        from src.db.repository import MessageRepository
        db = _make_db_session()
        msg1 = make_message(1)
        msg2 = make_message(2)
        result = MagicMock()
        result.scalars.return_value.all.return_value = [msg1, msg2]
        db.execute.return_value = result

        repo = MessageRepository(db)
        messages = await repo.get_by_ids([1, 2])
        assert len(messages) == 2

    async def test_get_by_ids_empty_list(self):
        from src.db.repository import MessageRepository
        db = _make_db_session()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        db.execute.return_value = result

        repo = MessageRepository(db)
        messages = await repo.get_by_ids([])
        assert messages == []


class TestSessionRepository:
    async def test_create_saves_and_returns_session(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        repo = SessionRepository(db)

        data = {
            "chat_id": -100123,
            "tg_msg_ids": [1, 2, 3],
            "started_at": datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
            "ended_at": datetime(2026, 5, 27, 12, 0, tzinfo=timezone.utc),
            "status": "queued",
        }
        await repo.create(data)

        db.add.assert_called_once()
        db.commit.assert_called_once()

    async def test_get_returns_session_by_id(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        session = make_session(session_id=42)
        result = MagicMock()
        result.scalar_one_or_none.return_value = session
        db.execute.return_value = result

        repo = SessionRepository(db)
        found = await repo.get(42)
        assert found.id == 42

    async def test_get_returns_none_when_not_found(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        db.execute.return_value = result

        repo = SessionRepository(db)
        found = await repo.get(999)
        assert found is None

    async def test_get_last_returns_most_recent_session(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        session = make_session()
        result = MagicMock()
        result.scalar_one_or_none.return_value = session
        db.execute.return_value = result

        repo = SessionRepository(db)
        last = await repo.get_last()
        assert last is not None

    async def test_update_status_commits(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        result = MagicMock()
        db.execute.return_value = result

        repo = SessionRepository(db)
        await repo.update_status(1, "processed")

        db.execute.assert_called_once()
        db.commit.assert_called_once()

    async def test_update_status_with_error_message(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        db.execute.return_value = MagicMock()

        repo = SessionRepository(db)
        # Should not raise
        await repo.update_status(1, "failed", error="Something went wrong")
        db.commit.assert_called_once()

    async def test_increment_retry_increments_count(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        session = MagicMock()
        session.retry_count = 2
        result = MagicMock()
        result.scalar_one_or_none.return_value = session
        db.execute.return_value = result

        repo = SessionRepository(db)
        new_count = await repo.increment_retry(1)

        assert new_count == 3
        assert session.retry_count == 3
        db.commit.assert_called_once()

    async def test_list_failed_returns_failed_sessions(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        sessions = [make_session(status="failed"), make_session(status="failed")]
        result = MagicMock()
        result.scalars.return_value.all.return_value = sessions
        db.execute.return_value = result

        repo = SessionRepository(db)
        failed = await repo.list_failed()
        assert len(failed) == 2

    async def test_count_pending_returns_count(self):
        from src.db.repository import SessionRepository
        db = _make_db_session()
        sessions = [make_session(status="queued"), make_session(status="processing")]
        result = MagicMock()
        result.scalars.return_value.all.return_value = sessions
        db.execute.return_value = result

        repo = SessionRepository(db)
        count = await repo.count_pending()
        assert count == 2


class TestKnowledgeItemRepository:
    async def test_create_many_saves_all_items(self):
        from src.db.repository import KnowledgeItemRepository
        db = _make_db_session()
        repo = KnowledgeItemRepository(db)

        items = [
            {"session_id": 1, "item_type": "decision", "text": "Decision 1", "tags": []},
            {"session_id": 1, "item_type": "idea", "text": "Idea 1", "tags": ["growth"]},
        ]
        await repo.create_many(items)

        db.add_all.assert_called_once()
        assert len(db.add_all.call_args.args[0]) == 2
        db.commit.assert_called_once()

    async def test_create_many_empty_list(self):
        from src.db.repository import KnowledgeItemRepository
        db = _make_db_session()
        repo = KnowledgeItemRepository(db)

        result = await repo.create_many([])
        assert result == []

    async def test_set_notion_id_commits(self):
        from src.db.repository import KnowledgeItemRepository
        db = _make_db_session()
        db.execute.return_value = MagicMock()
        repo = KnowledgeItemRepository(db)

        await repo.set_notion_id(1, "page-id-abc")

        db.execute.assert_called_once()
        db.commit.assert_called_once()

    async def test_get_open_questions(self):
        from src.db.repository import KnowledgeItemRepository
        db = _make_db_session()
        items = [MagicMock(item_type="open_question", status="open")]
        result = MagicMock()
        result.scalars.return_value.all.return_value = items
        db.execute.return_value = result

        repo = KnowledgeItemRepository(db)
        questions = await repo.get_open_questions()
        assert len(questions) == 1


class TestProcessingLogRepository:
    async def test_log_creates_entry(self):
        from src.db.repository import ProcessingLogRepository
        db = _make_db_session()
        repo = ProcessingLogRepository(db)

        await repo.log(1, "structuring", "started")

        db.add.assert_called_once()
        db.commit.assert_called_once()

    async def test_log_with_error(self):
        from src.db.repository import ProcessingLogRepository
        db = _make_db_session()
        repo = ProcessingLogRepository(db)

        await repo.log(1, "notion", "failed", error="Rate limit hit", details={"code": 429})

        log_entry = db.add.call_args.args[0]
        assert log_entry.error == "Rate limit hit"
        assert log_entry.details == {"code": 429}

    async def test_log_with_no_session_id(self):
        from src.db.repository import ProcessingLogRepository
        db = _make_db_session()
        repo = ProcessingLogRepository(db)

        await repo.log(None, "global", "info")

        log_entry = db.add.call_args.args[0]
        assert log_entry.session_id is None
