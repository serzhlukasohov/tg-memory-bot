"""aiogram 3.x admin bot for operator commands."""
import asyncio
import json

import redis.asyncio as aioredis
import structlog
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from arq import create_pool
from arq.connections import RedisSettings

from src.config import settings
from src.db.models import SessionStatus
from src.db.repository import (
    KnowledgeItemRepository,
    MessageRepository,
    SessionRepository,
    async_session_factory,
)

log = structlog.get_logger()
bot = Bot(token=settings.tg_bot_token)
dp = Dispatcher()


@dp.message(Command("status"))
async def cmd_status(message: Message) -> None:
    async with async_session_factory() as db:
        session_repo = SessionRepository(db)
        pending = await session_repo.count_pending()
        last = await session_repo.get_last()

    lines = [f"📊 **Bot Status**", f"", f"⏳ Pending sessions: {pending}"]
    if last:
        lines += [
            f"",
            f"**Last session:**",
            f"• ID: {last.id}",
            f"• Date: {last.started_at.strftime('%Y-%m-%d %H:%M')}",
            f"• Status: {last.status}",
        ]
        if last.structured_json:
            s = last.structured_json
            lines.append(f"• Summary: {s.get('summary', '')[:200]}")

    await message.answer("\n".join(lines), parse_mode="Markdown")


@dp.message(Command("backfill"))
async def cmd_backfill(message: Message) -> None:
    """
    /backfill              — resume from checkpoint (or from the very beginning)
    /backfill 2024-01-15   — load all messages on and after that date
    /backfill 12345        — load messages with ID > 12345
    """
    arg = (message.text.split(maxsplit=1)[1].strip() if len(message.text.split(maxsplit=1)) > 1 else "").strip()

    since_id = 0
    since_date_str = None

    if arg:
        # Try date first (YYYY-MM-DD)
        if len(arg) == 10 and arg[4] == "-" and arg[7] == "-":
            try:
                from datetime import datetime
                datetime.strptime(arg, "%Y-%m-%d")  # validate
                since_date_str = arg
            except ValueError:
                await message.answer("❌ Invalid date. Use YYYY-MM-DD format, e.g. /backfill 2024-01-15")
                return
        else:
            try:
                since_id = int(arg)
            except ValueError:
                await message.answer("❌ Usage:\n/backfill\n/backfill 2024-01-15\n/backfill 12345")
                return

    if since_date_str:
        desc = f"messages from {since_date_str} onwards"
    elif since_id:
        desc = f"messages after ID {since_id}"
    else:
        desc = "all messages (resuming from checkpoint if available)"

    await message.answer(f"🔄 Queuing backfill: {desc}…")
    pool = await create_pool(RedisSettings.from_dsn(settings.redis_url))
    try:
        await pool.enqueue_job("run_backfill", since_id, since_date_str)
    finally:
        await pool.aclose()
    await message.answer("✅ Backfill queued. You'll get a notification when it finishes.")


@dp.message(Command("retry"))
async def cmd_retry(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Usage: /retry <session_id>")
        return
    try:
        session_id = int(args[1].strip())
    except ValueError:
        await message.answer("❌ Session ID must be a number")
        return

    async with async_session_factory() as db:
        session_repo = SessionRepository(db)
        session = await session_repo.get(session_id)
        if not session:
            await message.answer(f"❌ Session {session_id} not found")
            return
        await session_repo.update_status(session_id, SessionStatus.queued, extra={"retry_count": 0})

    pool = await create_pool(RedisSettings.from_dsn(settings.redis_url))
    await pool.enqueue_job("process_session", session_id)
    await pool.aclose()
    await message.answer(f"✅ Session {session_id} re-queued for processing")


@dp.message(Command("last"))
async def cmd_last(message: Message) -> None:
    async with async_session_factory() as db:
        session_repo = SessionRepository(db)
        session = await session_repo.get_last()

    if not session or not session.structured_json:
        await message.answer("No processed sessions found yet.")
        return

    s = session.structured_json
    lines = [
        f"📋 **Last Session** — {session.started_at.strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"**Summary:** {s.get('summary', '')}",
        f"",
        f"**Energy:** {s.get('energy', 'unknown')}",
        f"**Topics:** {', '.join(s.get('main_topics', []))}",
        f"",
        f"📌 Decisions: {len(s.get('decisions', []))}",
        f"❓ Questions: {len(s.get('open_questions', []))}",
        f"💡 Ideas: {len(s.get('ideas', []))}",
        f"✅ Actions: {len(s.get('action_items', []))}",
    ]
    if session.github_file_path:
        url = f"https://github.com/{settings.github_repo}/blob/{settings.github_branch}/{session.github_file_path}"
        lines.append(f"\n🔗 [GitHub]({url})")

    await message.answer("\n".join(lines), parse_mode="Markdown")


@dp.message(Command("actions"))
async def cmd_actions(message: Message) -> None:
    """Show open action items."""
    async with async_session_factory() as db:
        item_repo = KnowledgeItemRepository(db)
        items = await item_repo.get_open_actions()

    if not items:
        await message.answer("✅ No open action items.")
        return

    lines = ["📌 **Open Action Items**", ""]
    for i, item in enumerate(items, 1):
        owner = f" @{item.owner}" if item.owner else ""
        due = f" _(due: {item.extra.get('due')})_" if item.extra and item.extra.get("due") else ""
        lines.append(f"{i}. `#{item.id}`{owner}: {item.text}{due}")

    await message.answer("\n".join(lines), parse_mode="Markdown")


@dp.message(Command("questions"))
async def cmd_questions(message: Message) -> None:
    """Show open questions."""
    async with async_session_factory() as db:
        item_repo = KnowledgeItemRepository(db)
        items = await item_repo.get_open_questions()

    if not items:
        await message.answer("✅ No open questions.")
        return

    lines = ["❓ **Open Questions**", ""]
    for i, item in enumerate(items, 1):
        owner = f" — @{item.owner}" if item.owner else ""
        lines.append(f"{i}. `#{item.id}`{owner}: {item.text}")

    await message.answer("\n".join(lines), parse_mode="Markdown")


@dp.message(Command("done"))
async def cmd_done(message: Message) -> None:
    """
    Mark a knowledge item as closed.
    Usage: /done <item_id>
    """
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Usage: /done <item_id>")
        return
    try:
        item_id = int(parts[1].strip())
    except ValueError:
        await message.answer("❌ Item ID must be a number")
        return

    async with async_session_factory() as db:
        item_repo = KnowledgeItemRepository(db)
        result = await item_repo.close(item_id)

    if result == "not_found":
        await message.answer(f"❌ Item #{item_id} not found")
        return
    if result == "already_closed":
        await message.answer(f"ℹ️ Item #{item_id} is already closed")
        return

    await message.answer(f"✅ Item #{item_id} marked as done")


async def listen_notifications(redis: aioredis.Redis) -> None:
    """Subscribe to Redis pub/sub for worker notifications. Reconnects on failure."""
    while True:
        try:
            pubsub = redis.pubsub()
            await pubsub.subscribe("bot:notifications")
            log.info("notification_listener_started")

            async for msg in pubsub.listen():
                if msg["type"] != "message":
                    continue
                try:
                    data = json.loads(msg["data"])
                    text = data.get("text", "")
                    if text:
                        await bot.send_message(
                            chat_id=settings.tg_group_id,
                            text=text,
                            parse_mode="Markdown",
                        )
                except Exception:
                    log.exception("notification_send_error")
        except Exception:
            log.exception("notification_listener_error")
            await asyncio.sleep(5)


async def main() -> None:
    redis = aioredis.from_url(settings.redis_url, decode_responses=True)

    # Run bot polling and notification listener concurrently
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=True),
        listen_notifications(redis),
    )


if __name__ == "__main__":
    asyncio.run(main())
