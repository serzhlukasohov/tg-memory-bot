"""Telethon user-client: listens to group messages, writes to Redis Stream."""
import asyncio
import json
from datetime import timezone

import redis.asyncio as aioredis
import structlog
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

from src.config import settings
from src.processors.media import download_to_bytes
from src.processors.ocr import extract_text_from_bytes
from src.processors.transcribe import transcribe_bytes

log = structlog.get_logger()
STREAM_KEY = "tg:incoming"

# Telethon media class name → processing category
_VOICE_TYPES = {"MessageMediaDocument"}  # voice/audio are Documents in Telethon
_PHOTO_TYPES = {"MessageMediaPhoto"}


def _msg_to_payload(message) -> dict:
    media_type = type(message.media).__name__ if message.media else None
    author_name = ""
    if message.sender:
        sender = message.sender
        parts = filter(None, [getattr(sender, "first_name", None), getattr(sender, "last_name", None)])
        author_name = " ".join(parts) or getattr(sender, "username", "") or ""

    return {
        "msg_id": message.id,
        "chat_id": message.chat_id,
        "date": message.date.astimezone(timezone.utc).isoformat(),
        "text": message.text or "",
        "author_id": message.sender_id,
        "author_name": author_name,
        "has_media": message.media is not None,
        "media_type": media_type,
        "grouped_id": message.grouped_id,
        "reply_to_msg_id": message.reply_to_msg_id,
    }


def _is_voice(message) -> bool:
    """Return True if message contains a voice note or audio file."""
    if not message.media:
        return False
    media_type = type(message.media).__name__
    if media_type not in _VOICE_TYPES:
        return False
    doc = getattr(message.media, "document", None)
    if not doc:
        return False
    mime = getattr(doc, "mime_type", "") or ""
    return mime.startswith("audio/") or mime == "video/ogg"  # Telegram voice notes


def _is_photo(message) -> bool:
    return type(message.media).__name__ in _PHOTO_TYPES


async def _enrich_media(client: TelegramClient, redis: aioredis.Redis, message, base_payload: dict) -> None:
    """Download and transcribe/OCR media, then push an update into the stream."""
    try:
        transcription: str | None = None
        ocr_text: str | None = None

        if _is_voice(message):
            audio_bytes = await download_to_bytes(client, message)
            if audio_bytes:
                doc = message.media.document
                mime = getattr(doc, "mime_type", "audio/ogg")
                ext = "mp3" if "mpeg" in mime else "ogg"
                transcription = await transcribe_bytes(audio_bytes, filename=f"voice.{ext}")

        elif _is_photo(message):
            image_bytes = await download_to_bytes(client, message)
            if image_bytes:
                ocr_text = await extract_text_from_bytes(image_bytes, media_type="image/jpeg")

        if transcription or ocr_text:
            update = {**base_payload, "_edited": True}
            if transcription:
                update["transcription"] = transcription
            if ocr_text:
                update["ocr_text"] = ocr_text
            await redis.xadd(STREAM_KEY, {"data": json.dumps(update)})
            log.info("media_enrichment_done", msg_id=base_payload["msg_id"],
                     has_transcription=bool(transcription), has_ocr=bool(ocr_text))

    except Exception:
        log.exception("media_enrichment_error", msg_id=base_payload.get("msg_id"))


async def main() -> None:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    client = TelegramClient(
        StringSession(settings.tg_session_string),
        settings.tg_api_id,
        settings.tg_api_hash,
    )

    @client.on(events.NewMessage(chats=settings.tg_group_id))
    async def on_new_message(event):
        try:
            payload = _msg_to_payload(event.message)
            await redis.xadd(STREAM_KEY, {"data": json.dumps(payload)})
            log.info("message_queued", msg_id=payload["msg_id"])

            # Schedule media enrichment in background — does not block new messages
            if event.message.media:
                asyncio.create_task(
                    _enrich_media(client, redis, event.message, payload)
                )
        except FloodWaitError as e:
            log.warning("flood_wait", seconds=e.seconds)
            await asyncio.sleep(e.seconds + 5)
        except Exception:
            log.exception("listener_error")

    @client.on(events.MessageEdited(chats=settings.tg_group_id))
    async def on_edit(event):
        try:
            payload = _msg_to_payload(event.message)
            payload["_edited"] = True
            await redis.xadd(STREAM_KEY, {"data": json.dumps(payload)})
            log.info("message_edit_queued", msg_id=payload["msg_id"])
        except Exception:
            log.exception("listener_edit_error")

    await client.start()
    log.info("listener_started", group_id=settings.tg_group_id)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
