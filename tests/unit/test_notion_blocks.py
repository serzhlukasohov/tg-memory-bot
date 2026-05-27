"""Tests for Notion block builder helper functions."""
import pytest


class TestChunks:
    def test_short_text_single_chunk(self):
        from src.writers.notion_writer import _chunks
        result = _chunks("hello", 1900)
        assert result == ["hello"]

    def test_long_text_split_into_chunks(self):
        from src.writers.notion_writer import _chunks
        text = "x" * 4000
        result = _chunks(text, 1900)
        assert len(result) == 3  # 1900 + 1900 + 200
        assert len(result[0]) == 1900
        assert len(result[1]) == 1900
        assert len(result[2]) == 200

    def test_exactly_chunk_size(self):
        from src.writers.notion_writer import _chunks
        text = "x" * 1900
        result = _chunks(text, 1900)
        assert len(result) == 1

    def test_empty_string(self):
        from src.writers.notion_writer import _chunks
        # Empty string produces no slices via range(0, 0, size)
        assert _chunks("", 1900) == []

    def test_custom_chunk_size(self):
        from src.writers.notion_writer import _chunks
        result = _chunks("hello world", 5)
        assert result == ["hello", " worl", "d"]


class TestRichText:
    def test_short_text_single_block(self):
        from src.writers.notion_writer import _rich_text
        result = _rich_text("hello")
        assert len(result) == 1
        assert result[0]["type"] == "text"
        assert result[0]["text"]["content"] == "hello"

    def test_long_text_multiple_blocks(self):
        from src.writers.notion_writer import _rich_text
        text = "x" * 4000
        result = _rich_text(text)
        assert len(result) == 3
        assert all(r["type"] == "text" for r in result)


class TestBlockBuilders:
    def test_paragraph_structure(self):
        from src.writers.notion_writer import _paragraph
        block = _paragraph("test text")
        assert block["object"] == "block"
        assert block["type"] == "paragraph"
        assert "rich_text" in block["paragraph"]

    def test_heading2_structure(self):
        from src.writers.notion_writer import _heading2
        block = _heading2("My Heading")
        assert block["type"] == "heading_2"
        assert block["heading_2"]["rich_text"][0]["text"]["content"] == "My Heading"

    def test_bullet_structure(self):
        from src.writers.notion_writer import _bullet
        block = _bullet("bullet point")
        assert block["type"] == "bulleted_list_item"
        assert "rich_text" in block["bulleted_list_item"]

    def test_bullet_truncates_at_2000(self):
        from src.writers.notion_writer import _bullet
        long_text = "x" * 3000
        block = _bullet(long_text)
        # Rich text is built from the truncated version
        combined = "".join(r["text"]["content"] for r in block["bulleted_list_item"]["rich_text"])
        assert len(combined) <= 2000

    def test_todo_unchecked_by_default(self):
        from src.writers.notion_writer import _todo
        block = _todo("do something")
        assert block["type"] == "to_do"
        assert block["to_do"]["checked"] is False

    def test_todo_checked(self):
        from src.writers.notion_writer import _todo
        block = _todo("done", checked=True)
        assert block["to_do"]["checked"] is True

    def test_callout_structure(self):
        from src.writers.notion_writer import _callout
        block = _callout("info text", "ℹ️")
        assert block["type"] == "callout"
        assert block["callout"]["icon"]["emoji"] == "ℹ️"

    def test_callout_default_emoji(self):
        from src.writers.notion_writer import _callout
        block = _callout("info text")
        assert block["callout"]["icon"]["emoji"] == "ℹ️"


class TestBuildSessionBlocks:
    def test_returns_list_of_blocks(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message, SAMPLE_STRUCTURED
        msgs = [make_message(1, text="test")]
        blocks = _build_session_blocks(SAMPLE_STRUCTURED, msgs)
        assert isinstance(blocks, list)
        assert len(blocks) > 0

    def test_contains_summary_heading(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message, SAMPLE_STRUCTURED
        msgs = [make_message(1)]
        blocks = _build_session_blocks(SAMPLE_STRUCTURED, msgs)
        headings = [b for b in blocks if b["type"] == "heading_2"]
        heading_texts = [h["heading_2"]["rich_text"][0]["text"]["content"] for h in headings]
        assert "📋 Summary" in heading_texts

    def test_contains_decisions_heading(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message, SAMPLE_STRUCTURED
        blocks = _build_session_blocks(SAMPLE_STRUCTURED, [make_message(1)])
        headings = [b["heading_2"]["rich_text"][0]["text"]["content"]
                    for b in blocks if b["type"] == "heading_2"]
        assert "✅ Decisions" in headings

    def test_no_decisions_heading_when_empty(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message
        structured = {"summary": "short", "energy": "low",
                      "main_topics": [], "decisions": [], "open_questions": [],
                      "ideas": [], "action_items": [], "context_update": ""}
        blocks = _build_session_blocks(structured, [make_message(1)])
        headings = [b["heading_2"]["rich_text"][0]["text"]["content"]
                    for b in blocks if b["type"] == "heading_2"]
        assert "✅ Decisions" not in headings

    def test_action_items_use_todo_blocks(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message, SAMPLE_STRUCTURED
        blocks = _build_session_blocks(SAMPLE_STRUCTURED, [make_message(1)])
        todos = [b for b in blocks if b["type"] == "to_do"]
        assert len(todos) == len(SAMPLE_STRUCTURED["action_items"])

    def test_original_conversation_included(self):
        from src.writers.notion_writer import _build_session_blocks
        from tests.conftest import make_message, SAMPLE_STRUCTURED
        blocks = _build_session_blocks(SAMPLE_STRUCTURED, [make_message(1, text="test msg")])
        headings = [b["heading_2"]["rich_text"][0]["text"]["content"]
                    for b in blocks if b["type"] == "heading_2"]
        assert "💬 Original Conversation" in headings
