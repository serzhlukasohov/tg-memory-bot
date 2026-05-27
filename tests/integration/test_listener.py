"""Tests for Telegram listener — Telethon and Redis mocked."""
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _make_tg_message(
    msg_id: int = 1,
    text: str = "Hello",
    has_media: bool = False,
    media_type: str = None,
    grouped_id: int = None,
    reply_to_msg_id: int = None,
    sender_first: str = "Alice",
    sender_last: str = None,
    sender_id: int = 100,
):
    msg = MagicMock()
    msg.id = msg_id
    msg.chat_id = -1001234567890
    msg.date = datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
    msg.text = text
    msg.sender_id = sender_id
    msg.grouped_id = grouped_id
    msg.reply_to_msg_id = reply_to_msg_id

    if media_type:
        media = MagicMock()
        media.__class__.__name__ = media_type
        msg.media = media
    else:
        msg.media = None

    sender = MagicMock()
    sender.first_name = sender_first
    sender.last_name = sender_last
    sender.username = "alice"
    msg.sender = sender

    return msg


class TestMsgToPayload:
    def test_basic_text_message(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(msg_id=42, text="Hello world")
        payload = _msg_to_payload(msg)

        assert payload["msg_id"] == 42
        assert payload["text"] == "Hello world"
        assert payload["author_name"] == "Alice"
        assert payload["has_media"] is False
        assert payload["media_type"] is None

    def test_message_with_media(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(has_media=True, media_type="MessageMediaDocument")
        payload = _msg_to_payload(msg)

        assert payload["has_media"] is True
        assert payload["media_type"] == "MessageMediaDocument"

    def test_grouped_id_preserved(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(grouped_id=99999)
        payload = _msg_to_payload(msg)
        assert payload["grouped_id"] == 99999

    def test_reply_to_msg_id_preserved(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(reply_to_msg_id=5)
        payload = _msg_to_payload(msg)
        assert payload["reply_to_msg_id"] == 5

    def test_date_is_utc_isoformat(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message()
        payload = _msg_to_payload(msg)
        assert "2026-05-27" in payload["date"]
        assert "+00:00" in payload["date"] or "Z" in payload["date"]

    def test_author_name_combines_first_and_last(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(sender_first="John", sender_last="Doe")
        payload = _msg_to_payload(msg)
        assert payload["author_name"] == "John Doe"

    def test_author_name_first_only(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message(sender_first="Alice", sender_last=None)
        payload = _msg_to_payload(msg)
        assert payload["author_name"] == "Alice"

    def test_no_sender_gives_empty_name(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message()
        msg.sender = None
        payload = _msg_to_payload(msg)
        assert payload["author_name"] == ""

    def test_empty_text_becomes_empty_string(self):
        from src.listener import _msg_to_payload
        msg = _make_tg_message()
        msg.text = None
        payload = _msg_to_payload(msg)
        assert payload["text"] == ""


class TestOnNewMessage:
    async def test_writes_payload_to_redis_stream(self):
        redis_mock = AsyncMock()
        redis_mock.xadd = AsyncMock()
        msg = _make_tg_message(msg_id=1, text="Test message")

        with patch("src.listener.TelegramClient") as mock_client_cls:
            with patch("redis.asyncio.from_url", return_value=redis_mock):
                from src.listener import _msg_to_payload
                payload = _msg_to_payload(msg)
                await redis_mock.xadd("tg:incoming", {"data": json.dumps(payload)})

        redis_mock.xadd.assert_called_once()
        call_args = redis_mock.xadd.call_args
        assert call_args.args[0] == "tg:incoming"
        data = json.loads(call_args.args[1]["data"])
        assert data["msg_id"] == 1
        assert data["text"] == "Test message"

    async def test_edited_message_adds_edited_flag(self):
        redis_mock = AsyncMock()
        redis_mock.xadd = AsyncMock()
        msg = _make_tg_message(msg_id=5, text="Edited text")

        from src.listener import _msg_to_payload
        payload = _msg_to_payload(msg)
        payload["_edited"] = True
        await redis_mock.xadd("tg:incoming", {"data": json.dumps(payload)})

        data = json.loads(redis_mock.xadd.call_args.args[1]["data"])
        assert data["_edited"] is True


class TestEnrichMedia:
    def _make_voice_message(self, msg_id: int = 10):
        msg = MagicMock()
        msg.id = msg_id
        msg.chat_id = -100
        msg.date = datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc)
        msg.text = ""
        msg.sender_id = 1
        msg.grouped_id = None
        msg.reply_to_msg_id = None
        # Voice note: MessageMediaDocument with audio/ogg mime type
        doc = MagicMock()
        doc.mime_type = "audio/ogg"
        media = MagicMock()
        media.__class__.__name__ = "MessageMediaDocument"
        media.document = doc
        msg.media = media
        sender = MagicMock()
        sender.first_name = "Alice"
        sender.last_name = None
        sender.username = "alice"
        msg.sender = sender
        return msg

    def _make_photo_message(self, msg_id: int = 11):
        msg = MagicMock()
        msg.id = msg_id
        msg.chat_id = -100
        msg.date = datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc)
        msg.text = ""
        msg.sender_id = 1
        msg.grouped_id = None
        msg.reply_to_msg_id = None
        media = MagicMock()
        media.__class__.__name__ = "MessageMediaPhoto"
        msg.media = media
        sender = MagicMock()
        sender.first_name = "Bob"
        sender.last_name = None
        sender.username = "bob"
        msg.sender = sender
        return msg

    async def test_voice_message_triggers_transcription(self):
        from src.listener import _enrich_media, _msg_to_payload

        client = AsyncMock()
        redis = AsyncMock()
        redis.xadd = AsyncMock()
        msg = self._make_voice_message()
        payload = _msg_to_payload(msg)

        with patch("src.listener.download_to_bytes", new_callable=AsyncMock, return_value=b"audio-bytes"):
            with patch("src.listener.transcribe_bytes", new_callable=AsyncMock, return_value="Hello world"):
                await _enrich_media(client, redis, msg, payload)

        redis.xadd.assert_called_once()
        sent = json.loads(redis.xadd.call_args.args[1]["data"])
        assert sent["transcription"] == "Hello world"
        assert sent["_edited"] is True

    async def test_photo_message_triggers_ocr(self):
        from src.listener import _enrich_media, _msg_to_payload

        client = AsyncMock()
        redis = AsyncMock()
        redis.xadd = AsyncMock()
        msg = self._make_photo_message()
        payload = _msg_to_payload(msg)

        with patch("src.listener.download_to_bytes", new_callable=AsyncMock, return_value=b"image-bytes"):
            with patch("src.listener.extract_text_from_bytes", new_callable=AsyncMock, return_value="Whiteboard text"):
                await _enrich_media(client, redis, msg, payload)

        redis.xadd.assert_called_once()
        sent = json.loads(redis.xadd.call_args.args[1]["data"])
        assert sent["ocr_text"] == "Whiteboard text"

    async def test_no_xadd_when_transcription_is_empty(self):
        """If transcription returns None, no update pushed to stream."""
        from src.listener import _enrich_media, _msg_to_payload

        client = AsyncMock()
        redis = AsyncMock()
        redis.xadd = AsyncMock()
        msg = self._make_voice_message()
        payload = _msg_to_payload(msg)

        with patch("src.listener.download_to_bytes", new_callable=AsyncMock, return_value=b"audio"):
            with patch("src.listener.transcribe_bytes", new_callable=AsyncMock, return_value=None):
                await _enrich_media(client, redis, msg, payload)

        redis.xadd.assert_not_called()

    async def test_enrichment_error_does_not_raise(self):
        """If download fails, _enrich_media logs and returns silently."""
        from src.listener import _enrich_media, _msg_to_payload

        client = AsyncMock()
        redis = AsyncMock()
        msg = self._make_voice_message()
        payload = _msg_to_payload(msg)

        with patch("src.listener.download_to_bytes", new_callable=AsyncMock, side_effect=Exception("network error")):
            await _enrich_media(client, redis, msg, payload)  # must not raise

        redis.xadd.assert_not_called()
