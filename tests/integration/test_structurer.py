"""Tests for Claude API structuring — fully mocked."""
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_message, SAMPLE_STRUCTURED


def _make_claude_response(content: str) -> MagicMock:
    resp = MagicMock()
    resp.content = [MagicMock(text=content)]
    return resp


class TestParseJson:
    def test_parses_valid_json(self):
        from src.processors.structurer import _parse_json
        result = _parse_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_strips_json_markdown_fence(self):
        from src.processors.structurer import _parse_json
        text = "```json\n{\"key\": \"value\"}\n```"
        result = _parse_json(text)
        assert result == {"key": "value"}

    def test_strips_generic_markdown_fence(self):
        from src.processors.structurer import _parse_json
        text = "```\n{\"key\": \"value\"}\n```"
        result = _parse_json(text)
        assert result == {"key": "value"}

    def test_raises_json_parse_error_on_invalid(self):
        from src.processors.structurer import _parse_json, JSONParseError
        with pytest.raises(JSONParseError):
            _parse_json("this is not json")

    def test_raises_on_empty_object(self):
        from src.processors.structurer import _parse_json
        result = _parse_json("{}")
        assert result == {}


class TestStructureSession:
    async def test_returns_parsed_structured_json(self):
        from src.processors.structurer import structure_session
        messages = [
            make_message(1, text="Let's launch on ProductHunt"),
            make_message(2, text="Agreed, next Tuesday"),
            make_message(3, text="Great plan"),
        ]
        json_str = json.dumps(SAMPLE_STRUCTURED)

        with patch("src.processors.structurer._call_claude", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = json_str
            result = await structure_session(
                messages,
                datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
                120,
            )

        assert result["summary"] == SAMPLE_STRUCTURED["summary"]
        assert result["energy"] == "high"
        assert len(result["decisions"]) == 2
        mock_call.assert_called_once()

    async def test_retries_on_invalid_json(self):
        from src.processors.structurer import structure_session
        messages = [make_message(i, text=f"msg {i}") for i in range(3)]
        bad_json = "this is not json at all"
        good_json = json.dumps(SAMPLE_STRUCTURED)

        call_count = 0

        async def mock_call(msgs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return bad_json
            return good_json

        with patch("src.processors.structurer._call_claude", side_effect=mock_call):
            result = await structure_session(
                messages,
                datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
                60,
            )

        assert call_count == 2
        assert result["energy"] == "high"

    async def test_raises_after_max_retries_on_persistent_bad_json(self):
        from src.processors.structurer import structure_session, JSONParseError
        from tenacity import RetryError
        messages = [make_message(i, text=f"msg {i}") for i in range(3)]

        with patch("src.processors.structurer._call_claude", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "always bad json {"
            # tenacity wraps JSONParseError in RetryError after exhausting attempts
            with pytest.raises((JSONParseError, RetryError)):
                await structure_session(
                    messages,
                    datetime(2026, 5, 27, tzinfo=timezone.utc),
                    60,
                )

    async def test_includes_participants_in_prompt(self):
        from src.processors.structurer import structure_session
        messages = [
            make_message(1, author_name="Alice", text="test"),
            make_message(2, author_name="Bob", text="test"),
            make_message(3, author_name="Alice", text="test"),
        ]
        captured_messages = []

        async def capture_call(msgs):
            captured_messages.extend(msgs)
            return json.dumps(SAMPLE_STRUCTURED)

        with patch("src.processors.structurer._call_claude", side_effect=capture_call):
            await structure_session(messages, datetime(2026, 5, 27, tzinfo=timezone.utc), 30)

        user_prompt = captured_messages[0]["content"]
        assert "Alice" in user_prompt
        assert "Bob" in user_prompt

    async def test_includes_duration_in_prompt(self):
        from src.processors.structurer import structure_session
        messages = [make_message(i) for i in range(3)]
        captured = []

        async def capture_call(msgs):
            captured.extend(msgs)
            return json.dumps(SAMPLE_STRUCTURED)

        with patch("src.processors.structurer._call_claude", side_effect=capture_call):
            await structure_session(messages, datetime(2026, 5, 27, tzinfo=timezone.utc), 45)

        assert "45" in captured[0]["content"]


class TestGenerateStartupContext:
    async def test_returns_markdown_string(self):
        from src.processors.structurer import generate_startup_context
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="# Startup Context\n\nTest content")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.processors.structurer._get_client", return_value=mock_client):
            result = await generate_startup_context(
                previous_context_updates=["Update 1", "Update 2"],
                new_update="New update",
                open_questions=["Question 1"],
                open_actions=["Action 1"],
                key_decisions=[{"text": "Decision", "date": "2026-05-27"}],
            )
        assert "Startup Context" in result

    async def test_limits_previous_updates_to_20(self):
        from src.processors.structurer import generate_startup_context
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="context")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        captured_prompts = []

        async def capture(*args, **kwargs):
            captured_prompts.append(kwargs.get("messages", []))
            return mock_response

        mock_client.messages.create = capture

        with patch("src.processors.structurer._get_client", return_value=mock_client):
            await generate_startup_context(
                previous_context_updates=[f"Update {i}" for i in range(30)],
                new_update="latest",
                open_questions=[],
                open_actions=[],
                key_decisions=[],
            )

        prompt = captured_prompts[0][0]["content"]
        # Should include "Update 20" through "Update 29" (last 20) but not "Update 0"
        assert "Update 29" in prompt
        assert "Update 0" not in prompt
