"""Tests for Notion API writer — fully mocked."""
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch, call

import pytest

from tests.conftest import make_message, make_session, SAMPLE_STRUCTURED


def _make_notion_client():
    client = MagicMock()
    client.pages = MagicMock()
    client.pages.create = AsyncMock(return_value={"id": "page-id-123"})
    client.blocks = MagicMock()
    client.blocks.children = MagicMock()
    client.blocks.children.append = AsyncMock(return_value={})
    return client


async def _fake_api_call(coro):
    """Replacement for _api_call that just awaits the coroutine directly."""
    return await coro


class TestAppendBlocksPaginated:
    async def test_single_batch_when_under_100(self):
        from src.writers.notion_writer import _append_blocks_paginated
        client = _make_notion_client()
        blocks = [{"type": "paragraph"} for _ in range(50)]

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await _append_blocks_paginated("page-id", blocks)

        assert client.blocks.children.append.call_count == 1

    async def test_multiple_batches_for_over_100_blocks(self):
        from src.writers.notion_writer import _append_blocks_paginated
        client = _make_notion_client()
        blocks = [{"type": "paragraph"} for _ in range(250)]

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await _append_blocks_paginated("page-id", blocks)

        # 250 blocks → 3 batches (100+100+50)
        assert client.blocks.children.append.call_count == 3


class TestCreateSessionPage:
    async def test_creates_page_with_correct_database(self):
        from src.writers.notion_writer import create_session_page
        client = _make_notion_client()
        session = make_session()
        messages = [make_message(1, text="Hello"), make_message(2, text="World")]

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                page_id = await create_session_page(session, SAMPLE_STRUCTURED, messages)

        assert page_id == "page-id-123"
        create_call = client.pages.create.call_args
        assert create_call.kwargs["parent"]["database_id"] == "sessions-db-id"

    async def test_sets_energy_property(self):
        from src.writers.notion_writer import create_session_page
        client = _make_notion_client()
        session = make_session()
        messages = [make_message(1)]

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_session_page(session, SAMPLE_STRUCTURED, messages)

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Energy"]["select"]["name"] == "high"

    async def test_sets_decisions_count(self):
        from src.writers.notion_writer import create_session_page
        client = _make_notion_client()
        session = make_session()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_session_page(session, SAMPLE_STRUCTURED, [make_message(1)])

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Decisions Count"]["number"] == 2

    async def test_includes_github_link_when_provided(self):
        from src.writers.notion_writer import create_session_page
        client = _make_notion_client()
        session = make_session()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_session_page(
                    session, SAMPLE_STRUCTURED, [make_message(1)],
                    github_link="https://github.com/repo/sessions/test.md",
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert "GitHub Link" in props
        assert props["GitHub Link"]["url"] == "https://github.com/repo/sessions/test.md"

    async def test_no_github_link_when_not_provided(self):
        from src.writers.notion_writer import create_session_page
        client = _make_notion_client()
        session = make_session()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_session_page(session, SAMPLE_STRUCTURED, [make_message(1)])

        props = client.pages.create.call_args.kwargs["properties"]
        assert "GitHub Link" not in props


class TestCreateKnowledgeItem:
    async def test_creates_page_in_items_database(self):
        from src.writers.notion_writer import create_knowledge_item
        client = _make_notion_client()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                pid = await create_knowledge_item(
                    "decision", "Use Supabase", None, ["tech"],
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        assert pid == "page-id-123"
        create_call = client.pages.create.call_args
        assert create_call.kwargs["parent"]["database_id"] == "items-db-id"

    async def test_sets_correct_item_type(self):
        from src.writers.notion_writer import create_knowledge_item
        client = _make_notion_client()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_knowledge_item(
                    "open_question", "What is the pricing?", "Alice", [],
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Type"]["select"]["name"] == "open_question"

    async def test_sets_owner_when_provided(self):
        from src.writers.notion_writer import create_knowledge_item
        client = _make_notion_client()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_knowledge_item(
                    "action_item", "Fix billing", "Bob", [],
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Owner"]["rich_text"][0]["text"]["content"] == "Bob"

    async def test_no_owner_property_when_owner_is_none(self):
        from src.writers.notion_writer import create_knowledge_item
        client = _make_notion_client()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_knowledge_item(
                    "decision", "Use Redis", None, [],
                    "session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert "Owner" not in props

    async def test_links_to_session_via_relation(self):
        from src.writers.notion_writer import create_knowledge_item
        client = _make_notion_client()

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                await create_knowledge_item(
                    "idea", "Build referral", None, [],
                    "my-session-page-id", datetime(2026, 5, 27, tzinfo=timezone.utc),
                )

        props = client.pages.create.call_args.kwargs["properties"]
        assert props["Session"]["relation"][0]["id"] == "my-session-page-id"


class TestWriteSessionToNotion:
    async def test_creates_session_and_all_items(self):
        from src.writers.notion_writer import write_session_to_notion
        session = make_session()
        messages = [make_message(1), make_message(2)]

        page_counter = [0]

        async def mock_page_create(**kwargs):
            page_counter[0] += 1
            return {"id": f"page-{page_counter[0]}"}

        client = _make_notion_client()
        client.pages.create = mock_page_create

        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                session_pid, item_pids = await write_session_to_notion(
                    session, SAMPLE_STRUCTURED, messages
                )

        assert session_pid == "page-1"
        # decisions(2) + questions(1) + ideas(1) + actions(1)
        assert len(item_pids) == 5

    async def test_returns_session_page_id_and_item_ids(self):
        from src.writers.notion_writer import write_session_to_notion
        session = make_session()

        client = _make_notion_client()
        with patch("src.writers.notion_writer._get_client", return_value=client):
            with patch("src.writers.notion_writer._api_call", side_effect=_fake_api_call):
                session_pid, item_pids = await write_session_to_notion(
                    session, SAMPLE_STRUCTURED, [make_message(1)]
                )

        assert isinstance(session_pid, str)
        assert isinstance(item_pids, list)
