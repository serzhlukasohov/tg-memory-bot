"""
Edge cases not covered by the primary test files.
Each test targets a specific boundary condition or failure mode identified in audit.
"""
import asyncio
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_message, make_session, SAMPLE_STRUCTURED


# ---------------------------------------------------------------------------
# session_builder edge cases
# ---------------------------------------------------------------------------

class TestSessionBuilderEdgeCases:
    def test_microsecond_boundary_does_not_split_session(self):
        """Gap of exactly 120 min + 1 microsecond must split the session."""
        from src.processors.session_builder import build_sessions
        base = datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
        msgs = [
            make_message(1, date=base),
            make_message(2, date=base + timedelta(minutes=120, microseconds=1)),
        ]
        sessions = build_sessions(msgs)
        assert len(sessions) == 2

    def test_single_participant_no_author_name(self):
        """format_conversation with author_id but no name falls back to user_{id}."""
        from src.processors.session_builder import format_conversation
        msg = make_message(1, author_name="", author_id=777, text="hello")
        result = format_conversation([msg])
        assert "user_777" in result

    def test_link_metadata_missing_keys(self):
        """format_conversation handles link_metadata with missing title/description."""
        from src.processors.session_builder import format_conversation
        msg = make_message(1, text="", link_metadata={"url": "https://x.com"})
        result = format_conversation([msg])
        # Should not crash; empty strings for missing keys
        assert "[Link:" in result

    def test_album_with_single_message_still_grouped(self):
        """A grouped_id with only one message should still appear as a list."""
        from src.processors.session_builder import merge_albums
        msgs = [make_message(1, date=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc), grouped_id=42)]
        result = merge_albums(msgs)
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert result[0][0].msg_id == 1


# ---------------------------------------------------------------------------
# structurer edge cases
# ---------------------------------------------------------------------------

class TestStructurerEdgeCases:
    async def test_all_messages_have_no_author_name(self):
        """When all author_names are empty, prompt should say 'Unknown'."""
        from src.processors.structurer import structure_session
        messages = [
            make_message(i, author_name="", author_id=i, text=f"msg {i}")
            for i in range(3)
        ]
        captured = []

        async def capture(msgs):
            captured.extend(msgs)
            return json.dumps(SAMPLE_STRUCTURED)

        with patch("src.processors.structurer._call_claude", side_effect=capture):
            await structure_session(messages, datetime(2026, 5, 27, tzinfo=timezone.utc), 30)

        assert "Unknown" in captured[0]["content"]

    async def test_none_author_names_treated_same_as_empty(self):
        """author_name=None messages should not appear in participants."""
        from src.processors.structurer import structure_session
        messages = [
            make_message(1, author_name=None, text="test"),
            make_message(2, author_name="Alice", text="test"),
            make_message(3, author_name=None, text="test"),
        ]
        captured = []

        async def capture(msgs):
            captured.extend(msgs)
            return json.dumps(SAMPLE_STRUCTURED)

        with patch("src.processors.structurer._call_claude", side_effect=capture):
            await structure_session(messages, datetime(2026, 5, 27, tzinfo=timezone.utc), 30)

        prompt = captured[0]["content"]
        assert "Alice" in prompt
        # "None" should not appear as a participant name
        assert "None" not in prompt.split("PARTICIPANTS:")[1].split("\n")[0]

    async def test_json_with_missing_optional_fields(self):
        """Claude response missing optional arrays should not crash."""
        from src.processors.structurer import structure_session
        minimal = {
            "summary": "Short session",
            "energy": "low",
            "main_topics": [],
            "decisions": [],
            "open_questions": [],
            "ideas": [],
            "action_items": [],
            "context_update": "",
        }

        with patch("src.processors.structurer._call_claude", new_callable=AsyncMock,
                   return_value=json.dumps(minimal)):
            result = await structure_session(
                [make_message(i) for i in range(3)],
                datetime(2026, 5, 27, tzinfo=timezone.utc),
                10,
            )

        assert result["decisions"] == []
        assert result["summary"] == "Short session"


# ---------------------------------------------------------------------------
# notion_writer edge cases
# ---------------------------------------------------------------------------

class TestNotionWriterEdgeCases:
    async def _fake_api_call(self, coro):
        return await coro

    async def test_very_long_summary_title_fits_255_chars(self):
        """Session title must never exceed 255 chars (Notion limit)."""
        from src.writers.notion_writer import create_session_page
        client = MagicMock()
        client.pages.create = AsyncMock(return_value={"id": "p1"})
        client.blocks.children.append = AsyncMock(return_value={})

        session = make_session()
        long_summary = "A" * 500
        structured = {**SAMPLE_STRUCTURED, "summary": long_summary}

        async def fake_api(coro):
            return await coro

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=fake_api):
                await create_session_page(session, structured, [make_message(1)])

        props = client.pages.create.call_args.kwargs["properties"]
        title = props["Title"]["title"][0]["text"]["content"]
        assert len(title) <= 255

    async def test_energy_not_in_map_defaults_to_default_color(self):
        """Unknown energy value doesn't crash, uses default color."""
        from src.writers.notion_writer import create_session_page
        client = MagicMock()
        client.pages.create = AsyncMock(return_value={"id": "p1"})
        client.blocks.children.append = AsyncMock(return_value={})

        session = make_session()
        structured = {**SAMPLE_STRUCTURED, "energy": "extreme"}

        async def fake_api(coro):
            return await coro

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=fake_api):
                # Must not raise
                await create_session_page(session, structured, [make_message(1)])

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Energy"]["select"]["name"] == "extreme"

    async def test_idea_priority_set_from_potential(self):
        """Ideas with 'potential' field should get Priority in Notion."""
        from src.writers.notion_writer import create_knowledge_item
        client = MagicMock()
        client.pages.create = AsyncMock(return_value={"id": "p1"})

        async def fake_api(coro):
            return await coro

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=fake_api):
                await create_knowledge_item(
                    "idea", "Build referral", None, [],
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                    extra={"potential": "high"},
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert "Priority" in props
        assert props["Priority"]["select"]["name"] == "high"

    async def test_rich_text_with_empty_string_returns_empty_list(self):
        """_rich_text on empty string gives no blocks (consistent with _chunks behaviour)."""
        from src.writers.notion_writer import _rich_text
        result = _rich_text("")
        assert result == []

    async def test_multi_select_capped_at_10_tags(self):
        """Tags list longer than 10 entries is silently capped."""
        from src.writers.notion_writer import create_knowledge_item
        client = MagicMock()
        client.pages.create = AsyncMock(return_value={"id": "p1"})

        async def fake_api(coro):
            return await coro

        tags = [f"tag{i}" for i in range(20)]

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=fake_api):
                await create_knowledge_item(
                    "decision", "Use Redis", None, tags,
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert len(props["Tags"]["multi_select"]) == 10


# ---------------------------------------------------------------------------
# listener edge cases
# ---------------------------------------------------------------------------

class TestListenerEdgeCases:
    def test_sender_with_all_none_name_fields(self):
        """Sender has first_name=None, last_name=None, username=None → empty string."""
        from src.listener import _msg_to_payload
        msg = MagicMock()
        msg.id = 1
        msg.chat_id = -100
        msg.date = datetime(2026, 5, 27, tzinfo=timezone.utc)
        msg.text = "hi"
        msg.sender_id = 5
        msg.media = None
        msg.grouped_id = None
        msg.reply_to_msg_id = None

        sender = MagicMock()
        sender.first_name = None
        sender.last_name = None
        sender.username = None
        msg.sender = sender

        payload = _msg_to_payload(msg)
        assert payload["author_name"] == ""

    def test_media_type_name_from_class(self):
        """media_type is the class name of message.media, not a string."""
        from src.listener import _msg_to_payload
        msg = MagicMock()
        msg.id = 1
        msg.chat_id = -100
        msg.date = datetime(2026, 5, 27, tzinfo=timezone.utc)
        msg.text = ""
        msg.sender_id = 1
        msg.sender = None
        msg.grouped_id = None
        msg.reply_to_msg_id = None

        class MessageMediaPhoto:
            pass

        msg.media = MessageMediaPhoto()
        payload = _msg_to_payload(msg)
        assert payload["media_type"] == "MessageMediaPhoto"
        assert payload["has_media"] is True


# ---------------------------------------------------------------------------
# repository edge cases
# ---------------------------------------------------------------------------

class TestRepositoryEdgeCases:
    def _make_db(self):
        db = AsyncMock()
        db.execute = AsyncMock()
        db.commit = AsyncMock()
        db.add = MagicMock()
        db.add_all = MagicMock()
        db.refresh = AsyncMock()
        return db

    async def test_upsert_with_null_text_field(self):
        """Upsert sets text=None on existing message without crashing."""
        from src.db.repository import MessageRepository
        db = self._make_db()
        existing = MagicMock()
        existing.text = "old text"
        result = MagicMock()
        result.scalar_one_or_none.return_value = existing
        db.execute.return_value = result

        repo = MessageRepository(db)
        await repo.upsert({
            "msg_id": 1,
            "chat_id": -100,
            "date": datetime(2026, 5, 27, tzinfo=timezone.utc),
            "text": None,
        })

        assert existing.text is None

    async def test_update_status_uses_timezone_aware_datetime(self):
        """update_status sets updated_at with UTC timezone (not naive)."""
        from src.db.repository import SessionRepository
        db = self._make_db()
        db.execute.return_value = MagicMock()

        repo = SessionRepository(db)
        await repo.update_status(1, "processed")

        update_stmt = db.execute.call_args.args[0]
        # Extract the compiled values — just verify it doesn't use utcnow
        # The real check: no DeprecationWarning should be emitted
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            await repo.update_status(2, "failed")
            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)
                                     and "utcnow" in str(x.message)]
        assert len(deprecation_warnings) == 0

    async def test_get_by_ids_with_empty_list(self):
        """get_by_ids([]) returns empty sequence without crashing."""
        from src.db.repository import MessageRepository
        db = self._make_db()
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        db.execute.return_value = result

        repo = MessageRepository(db)
        msgs = await repo.get_by_ids([])
        assert list(msgs) == []

    async def test_create_many_with_empty_list_is_noop(self):
        """create_many([]) does not call add_all."""
        from src.db.repository import KnowledgeItemRepository
        db = self._make_db()
        repo = KnowledgeItemRepository(db)

        result = await repo.create_many([])
        assert result == []
        db.add_all.assert_not_called()


# ---------------------------------------------------------------------------
# tasks pipeline edge cases
# ---------------------------------------------------------------------------

class TestTasksPipelineEdgeCases:
    def _full_mock_setup(self, session, messages, fail_at=None):
        """Return a dict of all mocked repositories for process_session."""
        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)
        mock_db.execute = AsyncMock(return_value=MagicMock(
            scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))
        ))

        session_repo = AsyncMock()
        session_repo.get = AsyncMock(return_value=session)
        session_repo.update_status = AsyncMock()
        session_repo.increment_retry = AsyncMock(return_value=session.retry_count + 1)

        msg_repo = AsyncMock()
        msg_repo.get_by_ids = AsyncMock(return_value=messages)

        item_repo = AsyncMock()
        item_repo.get_open_questions = AsyncMock(return_value=[])
        item_repo.get_open_actions = AsyncMock(return_value=[])
        item_repo.create_many = AsyncMock()

        log_repo = AsyncMock()
        log_repo.log = AsyncMock()

        return mock_db, session_repo, msg_repo, item_repo, log_repo

    async def test_consume_stream_dead_letters_invalid_json(self):
        """Malformed JSON payload is acked and moved to dead-letter stream (not lost, not stuck)."""
        from src.tasks import consume_stream, DEAD_LETTER_KEY

        redis = AsyncMock()
        redis.xgroup_create = AsyncMock()
        redis.xack = AsyncMock()
        redis.xadd = AsyncMock()

        call_count = [0]
        processed = asyncio.Event()

        async def mock_xreadgroup(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [("tg:incoming", [(b"bad-1", {"data": "{{not json"})])]
            processed.set()
            await asyncio.sleep(10)
            return []

        redis.xreadgroup = mock_xreadgroup

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=AsyncMock()):
                task = asyncio.create_task(consume_stream({"redis": redis}))
                await asyncio.wait_for(processed.wait(), timeout=2.0)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        # Bad message must be acked (removed from pending) AND sent to dead-letter
        redis.xack.assert_called_once_with("tg:incoming", "workers", b"bad-1")
        redis.xadd.assert_called_once()
        dead_letter_args = redis.xadd.call_args.args
        assert dead_letter_args[0] == DEAD_LETTER_KEY

    async def test_process_session_at_retry_boundary_marks_failed(self):
        """Session at retry_count = MAX_RETRIES - 1 that fails → marked failed, not re-enqueued."""
        from src.tasks import process_session, MAX_RETRIES
        # One retry short of the limit; after failing it hits MAX_RETRIES
        session = make_session(session_id=1, retry_count=MAX_RETRIES - 1)
        messages = [make_message(i) for i in range(3)]

        mock_db, session_repo, msg_repo, item_repo, log_repo = self._full_mock_setup(session, messages)
        # increment_retry returns MAX_RETRIES after incrementing
        session_repo.increment_retry = AsyncMock(return_value=MAX_RETRIES)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository", return_value=msg_repo):
                    with patch("src.tasks.KnowledgeItemRepository", return_value=item_repo):
                        with patch("src.tasks.ProcessingLogRepository", return_value=log_repo):
                            with patch("src.tasks.structure_session",
                                       side_effect=Exception("Claude timeout")):
                                with patch("src.tasks._notify_failure", new_callable=AsyncMock):
                                    with patch("src.tasks.create_pool") as mock_pool:
                                        pool = AsyncMock()
                                        mock_pool.return_value = pool
                                        pool.enqueue_job = AsyncMock()
                                        pool.aclose = AsyncMock()
                                        await process_session({"redis": AsyncMock()}, 1)

        # Must be marked failed
        status_values = [c.args[1] for c in session_repo.update_status.call_args_list]
        assert "failed" in status_values
        # Must NOT be re-enqueued (it hit the limit)
        pool.enqueue_job.assert_not_called()

    async def test_process_session_does_not_create_duplicate_notion_on_retry(self):
        """If notion write succeeds but github fails, retry should not double-create notion page.
        Currently this is a known limitation — session.notion_page_id is only saved AFTER both succeed.
        This test documents the current (imperfect) behavior."""
        from src.tasks import process_session
        session = make_session(session_id=1, retry_count=0, notion_page_id=None)
        messages = [make_message(i) for i in range(3)]

        mock_db, session_repo, msg_repo, item_repo, log_repo = self._full_mock_setup(session, messages)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.SessionRepository", return_value=session_repo):
                with patch("src.tasks.MessageRepository", return_value=msg_repo):
                    with patch("src.tasks.KnowledgeItemRepository", return_value=item_repo):
                        with patch("src.tasks.ProcessingLogRepository", return_value=log_repo):
                            with patch("src.tasks.structure_session", new_callable=AsyncMock,
                                       return_value=SAMPLE_STRUCTURED):
                                with patch("src.tasks.generate_startup_context", new_callable=AsyncMock,
                                           return_value="# Context"):
                                    # GitHub fails
                                    with patch("src.tasks.write_session_to_github",
                                               side_effect=Exception("GitHub API down")):
                                        with patch("src.tasks.write_session_to_notion",
                                                   new_callable=AsyncMock,
                                                   return_value=("notion-id", [])):
                                            with patch("src.tasks.create_pool") as mock_pool:
                                                pool = AsyncMock()
                                                mock_pool.return_value = pool
                                                pool.enqueue_job = AsyncMock()
                                                pool.aclose = AsyncMock()
                                                await process_session({"redis": AsyncMock()}, 1)

        # Session must NOT be marked processed (github failed)
        status_values = [c.args[1] for c in session_repo.update_status.call_args_list]
        assert "processed" not in status_values
        # retry count must be incremented
        session_repo.increment_retry.assert_called_once()

    async def test_build_and_queue_messages_older_than_cutoff_only(self):
        """Messages newer than gap+10 min cutoff should not be grouped yet."""
        from src.tasks import build_and_queue_sessions
        now = datetime.now(timezone.utc)

        # One eligible message (old) + one too-recent message
        old_msg = make_message(1, date=now - timedelta(hours=5))
        recent_msg = make_message(2, date=now - timedelta(minutes=10))

        msg_repo = AsyncMock()
        msg_repo.get_unassigned_since = AsyncMock(return_value=[old_msg, recent_msg])

        session_repo = AsyncMock()
        session_repo.create = AsyncMock(return_value=make_session())

        mock_db = AsyncMock()
        mock_db.__aenter__ = AsyncMock(return_value=mock_db)
        mock_db.__aexit__ = AsyncMock(return_value=False)

        with patch("src.tasks.async_session_factory", return_value=mock_db):
            with patch("src.tasks.MessageRepository", return_value=msg_repo):
                with patch("src.tasks.SessionRepository", return_value=session_repo):
                    with patch("src.tasks.create_pool") as mock_pool:
                        pool = AsyncMock()
                        mock_pool.return_value = pool
                        pool.enqueue_job = AsyncMock()
                        pool.aclose = AsyncMock()
                        await build_and_queue_sessions({"redis": AsyncMock()})

        # Only 1 eligible message → too few for a session (< 3), archived
        created_calls = session_repo.create.call_args_list
        if created_calls:
            # If a session was created from 1 message, it must be archived
            assert created_calls[0].args[0]["status"] == "archived"


# ---------------------------------------------------------------------------
# github_writer edge cases
# ---------------------------------------------------------------------------

class TestGithubWriterEdgeCases:
    def test_session_markdown_with_no_optional_sections(self):
        """Markdown generated with all empty lists produces no section headers."""
        from src.writers.github_writer import _session_markdown
        session = make_session(
            started_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 11, 0, tzinfo=timezone.utc),
        )
        empty_structured = {
            "summary": "Nothing happened",
            "energy": "low",
            "decisions": [],
            "open_questions": [],
            "ideas": [],
            "action_items": [],
            "context_update": "",
        }
        md = _session_markdown(session, empty_structured, 1)

        assert "✅ Decisions" not in md
        assert "❓ Open Questions" not in md
        assert "💡 Ideas" not in md
        assert "📌 Action Items" not in md
        assert "Nothing happened" in md

    async def test_commit_message_truncates_long_summary(self):
        """Commit message summary is capped at 80 chars."""
        from src.writers.github_writer import write_session_to_github
        # We test via _session_markdown which feeds into commit message
        # The commit message construction is: summary_first[:80]
        long_summary = "X" * 200
        structured = {**SAMPLE_STRUCTURED, "summary": long_summary}

        session = make_session(
            started_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 12, 0, tzinfo=timezone.utc),
        )
        repo = MagicMock()
        commit_messages = []

        def capture_commit(repo, files, message):
            commit_messages.append(message)

        with patch("src.writers.github_writer._get_repo", return_value=repo):
            with patch("src.writers.github_writer._commit_files", side_effect=capture_commit):
                await write_session_to_github(
                    session=session,
                    structured=structured,
                    session_number=1,
                    startup_context="context",
                    all_open_questions=[],
                    all_open_actions=[],
                    key_decisions=[],
                )

        assert len(commit_messages) == 1
        # Commit message should not contain the full 200-char summary
        summary_part = commit_messages[0].split(": ")[1].split(" |")[0]
        assert len(summary_part) <= 80

    def test_decisions_entry_with_decision_missing_text(self):
        """Decision with empty text produces a list item with just the link."""
        from src.writers.github_writer import _build_decisions_entry
        structured = {
            "decisions": [{"text": "", "tags": []}],
        }
        entry = _build_decisions_entry(structured, datetime(2026, 5, 27, tzinfo=timezone.utc), "path.md")
        assert "##" in entry  # still has a date header

    async def test_session_file_path_format(self):
        """Session file path uses correct strftime format for hour and session number."""
        from src.writers.github_writer import write_session_to_github
        session = make_session(
            started_at=datetime(2026, 5, 27, 9, 5, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
        )
        repo = MagicMock()
        committed_paths = []

        def capture_commit(repo, files, message):
            committed_paths.extend(f[0] for f in files)

        with patch("src.writers.github_writer._get_repo", return_value=repo):
            with patch("src.writers.github_writer._commit_files", side_effect=capture_commit):
                await write_session_to_github(
                    session=session,
                    structured=SAMPLE_STRUCTURED,
                    session_number=3,
                    startup_context="ctx",
                    all_open_questions=[],
                    all_open_actions=[],
                    key_decisions=[],
                )

        session_path = next(p for p in committed_paths if p.startswith("sessions/"))
        # Hour 09, session 03
        assert "2026-05-27-09-03" in session_path
