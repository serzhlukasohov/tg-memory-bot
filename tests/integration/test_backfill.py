"""Tests for backfill script — Telethon and Redis mocked."""
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _make_tg_message(msg_id: int = 1, text: str = "test"):
    msg = MagicMock()
    msg.id = msg_id
    msg.chat_id = -1001234567890
    msg.date = datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
    msg.text = text
    msg.sender_id = 100
    msg.media = None
    msg.grouped_id = None
    msg.reply_to_msg_id = None
    sender = MagicMock()
    sender.first_name = "Alice"
    sender.last_name = None
    msg.sender = sender
    return msg


def _make_redis(checkpoint=None):
    # redis.pipeline() is called synchronously in backfill.py (not awaited)
    # so pipeline must be returned by a sync MagicMock, not an AsyncMock
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=checkpoint)
    redis.set = AsyncMock()
    redis.aclose = AsyncMock()
    pipeline = MagicMock()
    pipeline.xadd = MagicMock()
    pipeline.execute = AsyncMock(return_value=[])
    redis.pipeline = MagicMock(return_value=pipeline)
    return redis


def _make_client(messages):
    async def fake_iter_messages(*args, **kwargs):
        for msg in messages:
            yield msg

    mock_client = AsyncMock()
    mock_client.start = AsyncMock()
    mock_client.disconnect = AsyncMock()
    mock_client.iter_messages = fake_iter_messages
    return mock_client


class TestBackfillMain:
    async def test_processes_messages_and_writes_to_redis(self):
        from src.backfill import main
        messages = [_make_tg_message(i, f"msg {i}") for i in range(1, 4)]
        redis = _make_redis()
        client = _make_client(messages)

        with patch("src.backfill.StringSession"):
            with patch("src.backfill.TelegramClient", return_value=client):
                with patch("src.backfill.aioredis.from_url", return_value=redis):
                    with patch("asyncio.sleep", new_callable=AsyncMock):
                        await main(since_id=0, limit=3)

        # Checkpoint should be set after processing
        redis.set.assert_called()
        set_call = redis.set.call_args
        assert set_call.args[0] == "backfill:last_msg_id"

    async def test_resumes_from_checkpoint_when_since_id_is_zero(self):
        from src.backfill import main
        redis = _make_redis(checkpoint="500")
        captured_kwargs = {}

        async def fake_iter(*args, **kwargs):
            captured_kwargs.update(kwargs)
            return
            yield

        client = AsyncMock()
        client.start = AsyncMock()
        client.disconnect = AsyncMock()
        client.iter_messages = fake_iter

        with patch("src.backfill.StringSession"):
            with patch("src.backfill.TelegramClient", return_value=client):
                with patch("src.backfill.aioredis.from_url", return_value=redis):
                    await main(since_id=0, limit=0)

        assert captured_kwargs.get("min_id") == 500

    async def test_does_not_resume_when_explicit_since_id_given(self):
        from src.backfill import main
        # Even with checkpoint=999, explicit since_id=12345 should win
        redis = _make_redis(checkpoint="999")
        captured_kwargs = {}

        async def fake_iter(*args, **kwargs):
            captured_kwargs.update(kwargs)
            return
            yield

        client = AsyncMock()
        client.start = AsyncMock()
        client.disconnect = AsyncMock()
        client.iter_messages = fake_iter

        with patch("src.backfill.StringSession"):
            with patch("src.backfill.TelegramClient", return_value=client):
                with patch("src.backfill.aioredis.from_url", return_value=redis):
                    await main(since_id=12345, limit=0)

        assert captured_kwargs.get("min_id") == 12345

    async def test_flushes_batch_every_100_messages(self):
        from src.backfill import main
        messages = [_make_tg_message(i) for i in range(1, 102)]  # 101 messages
        redis = _make_redis()
        flush_count = [0]

        async def fake_execute():
            flush_count[0] += 1
            return []

        redis.pipeline.return_value.execute = fake_execute
        client = _make_client(messages)

        with patch("src.backfill.StringSession"):
            with patch("src.backfill.TelegramClient", return_value=client):
                with patch("src.backfill.aioredis.from_url", return_value=redis):
                    with patch("asyncio.sleep", new_callable=AsyncMock):
                        await main(since_id=0, limit=101)

        # 100 messages → batch 1, 1 remaining → batch 2
        assert flush_count[0] == 2

    async def test_payload_format_is_valid_json(self):
        from src.backfill import main
        messages = [_make_tg_message(1, "Hello world")]
        redis = _make_redis()
        captured_payloads = []

        def capture_xadd(stream, data):
            captured_payloads.append(json.loads(data["data"]))

        redis.pipeline.return_value.xadd = capture_xadd
        client = _make_client(messages)

        with patch("src.backfill.StringSession"):
            with patch("src.backfill.TelegramClient", return_value=client):
                with patch("src.backfill.aioredis.from_url", return_value=redis):
                    await main(since_id=0, limit=1)

        assert len(captured_payloads) == 1
        payload = captured_payloads[0]
        assert payload["msg_id"] == 1
        assert payload["text"] == "Hello world"
        assert "date" in payload
        assert "author_name" in payload
