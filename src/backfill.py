"""Telegram group history backfill.

Can be run as a CLI script or invoked as an ARQ task via run_backfill in tasks.py.

Usage:
    python -m src.backfill --since-id 0 --limit 0
    python -m src.backfill --since-id 12345 --limit 500
    python -m src.backfill --since-date 2024-01-15
"""
import argparse
import asyncio
import json
import signal
from datetime import datetime, timezone

import redis.asyncio as aioredis
import structlog
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

from src.config import settings

log = structlog.get_logger()
STREAM_KEY = "tg:incoming"
CHECKPOINT_KEY = "backfill:last_msg_id"
BATCH_SIZE = 100
BATCH_SLEEP = 2


async def _resolve_since_id(client: TelegramClient, since_date: datetime) -> int:
    """Return the message ID of the last message before since_date (use as min_id)."""
    msgs = await client.get_messages(
        settings.tg_group_id,
        limit=1,
        offset_date=since_date,
    )
    return msgs[0].id if msgs else 0


async def backfill_core(
    redis: aioredis.Redis,
    since_id: int = 0,
    since_date: datetime | None = None,
    limit: int = 0,
    shutdown_event: asyncio.Event | None = None,
) -> int:
    """
    Load messages from Telegram into the Redis stream.

    Returns the number of messages pushed to the stream.
    Resumes from checkpoint when since_id=0 and since_date=None.
    """
    client = TelegramClient(
        StringSession(settings.tg_session_string),
        settings.tg_api_id,
        settings.tg_api_hash,
    )
    await client.start()

    try:
        # Resolve date → message ID
        if since_date is not None:
            since_id = await _resolve_since_id(client, since_date)
            log.info("resolved_date_to_id", since_date=since_date.isoformat(), since_id=since_id)
        elif since_id == 0:
            checkpoint = await redis.get(CHECKPOINT_KEY)
            if checkpoint:
                since_id = int(checkpoint)
                log.info("resuming_from_checkpoint", since_id=since_id)

        log.info("backfill_started", since_id=since_id, limit=limit or "unlimited")

        processed = 0
        batch: list[dict] = []

        async def flush_batch() -> None:
            nonlocal processed
            pipe = redis.pipeline()
            for payload in batch:
                pipe.xadd(STREAM_KEY, {"data": json.dumps(payload)})
            await pipe.execute()
            processed += len(batch)
            last_id = batch[-1]["msg_id"]
            await redis.set(CHECKPOINT_KEY, str(last_id))
            log.info("batch_flushed", count=len(batch), total=processed, last_msg_id=last_id)
            batch.clear()

        async for message in client.iter_messages(
            settings.tg_group_id,
            reverse=True,
            min_id=since_id,
            limit=limit or None,
        ):
            if shutdown_event is not None and shutdown_event.is_set():
                break

            try:
                media_type = type(message.media).__name__ if message.media else None
                author_name = ""
                if message.sender:
                    sender = message.sender
                    parts = filter(None, [
                        getattr(sender, "first_name", None),
                        getattr(sender, "last_name", None),
                    ])
                    author_name = " ".join(parts) or getattr(sender, "username", "") or ""

                payload = {
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
                batch.append(payload)

            except FloodWaitError as e:
                log.warning("flood_wait", seconds=e.seconds)
                if batch:
                    await flush_batch()
                await asyncio.sleep(e.seconds + 5)
            except Exception:
                log.exception("backfill_msg_error", msg_id=getattr(message, "id", None))

            if len(batch) >= BATCH_SIZE:
                await flush_batch()
                await asyncio.sleep(BATCH_SLEEP)

        if batch:
            await flush_batch()

    finally:
        await client.disconnect()

    log.info("backfill_complete", total_processed=processed)
    return processed


async def main(since_id: int, limit: int, since_date: datetime | None = None) -> None:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)

    shutdown_event = asyncio.Event()

    def _handle_signal(*_):
        log.info("shutdown_signal_received")
        shutdown_event.set()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, _handle_signal)
    loop.add_signal_handler(signal.SIGTERM, _handle_signal)

    try:
        await backfill_core(
            redis,
            since_id=since_id,
            since_date=since_date,
            limit=limit,
            shutdown_event=shutdown_event,
        )
    finally:
        await redis.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill Telegram group history")
    parser.add_argument("--since-id", type=int, default=0, help="Min message ID to start from (0 = from checkpoint or beginning)")
    parser.add_argument("--since-date", type=str, default=None, help="Load messages on and after this date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=0, help="Max messages to process (0 = all)")
    args = parser.parse_args()

    since_date = None
    if args.since_date:
        since_date = datetime.strptime(args.since_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    asyncio.run(main(args.since_id, args.limit, since_date=since_date))
