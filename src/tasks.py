"""ARQ async workers: consume Redis stream, process sessions."""
import asyncio
import json
from datetime import datetime, timedelta, timezone

import redis.asyncio as aioredis
import structlog
from arq import create_pool, cron
from arq.connections import RedisSettings
from sqlalchemy import func, select, update

from src.config import settings
from src.db.models import Message as MessageModel
from src.db.models import Session as SessionModel
from src.db.models import SessionStatus
from src.db.repository import (
    KnowledgeItemRepository,
    MessageRepository,
    ProcessingLogRepository,
    SessionRepository,
    async_session_factory,
)
from src.processors.session_builder import build_sessions
from src.processors.structurer import generate_startup_context, structure_session
from src.writers.github_writer import get_session_github_url, write_session_to_github
from src.writers.notion_writer import write_session_to_notion

log = structlog.get_logger()

STREAM_KEY = "tg:incoming"
DEAD_LETTER_KEY = "tg:incoming:dead"
CONSUMER_GROUP = "workers"
CONSUMER_NAME = "worker-1"
MAX_RETRIES = 3
MIN_SESSION_MESSAGES = 3
# Reclaim pending messages older than this many milliseconds (stuck due to crash)
XAUTOCLAIM_MIN_IDLE_MS = 5 * 60 * 1000  # 5 minutes


async def consume_stream(ctx: dict) -> None:
    """Continuously read from Redis stream and upsert messages to DB."""
    redis: aioredis.Redis = ctx["redis"]

    # Ensure consumer group exists
    try:
        await redis.xgroup_create(STREAM_KEY, CONSUMER_GROUP, id="0", mkstream=True)
    except Exception:
        pass  # group already exists

    # Reclaim any messages that were pending for too long (worker crashed mid-batch)
    try:
        claimed = await redis.xautoclaim(
            STREAM_KEY, CONSUMER_GROUP, CONSUMER_NAME,
            min_idle_time=XAUTOCLAIM_MIN_IDLE_MS, start_id="0-0",
        )
        reclaimed = claimed[1] if claimed else []
        if reclaimed:
            log.info("xautoclaim_reclaimed", count=len(reclaimed))
    except Exception:
        log.warning("xautoclaim_unavailable")  # Redis < 6.2 fallback

    while True:
        try:
            results = await redis.xreadgroup(
                CONSUMER_GROUP,
                CONSUMER_NAME,
                {STREAM_KEY: ">"},
                count=50,
                block=2000,
            )
            if not results:
                continue

            async with async_session_factory() as db:
                msg_repo = MessageRepository(db)
                for stream_name, messages in results:
                    for msg_id, fields in messages:
                        try:
                            payload = json.loads(fields["data"])
                            payload.pop("_edited", False)
                            payload["date"] = datetime.fromisoformat(payload["date"])
                            await msg_repo.upsert(payload)
                            await redis.xack(STREAM_KEY, CONSUMER_GROUP, msg_id)
                        except Exception:
                            log.exception("stream_msg_error", msg_id=msg_id)
                            # Ack and move to dead-letter so it never blocks the queue
                            await redis.xack(STREAM_KEY, CONSUMER_GROUP, msg_id)
                            await redis.xadd(
                                DEAD_LETTER_KEY,
                                {"original_id": str(msg_id), "data": fields.get("data", ""), "error": "parse_failed"},
                            )
        except asyncio.CancelledError:
            break
        except Exception:
            log.exception("consume_stream_error")
            await asyncio.sleep(5)


async def build_and_queue_sessions(ctx: dict) -> None:
    """Check for messages ready to be grouped into sessions and enqueue processing."""
    redis: aioredis.Redis = ctx["redis"]

    # Prevent overlapping cron runs from creating duplicate sessions
    acquired = await redis.set("lock:build_and_queue_sessions", "1", nx=True, ex=360)
    if acquired is None:
        log.info("build_sessions_already_running")
        return

    try:
        await _build_and_queue_sessions_inner(ctx)
    finally:
        await redis.delete("lock:build_and_queue_sessions")


async def _build_and_queue_sessions_inner(ctx: dict) -> None:
    async with async_session_factory() as db:
        msg_repo = MessageRepository(db)
        session_repo = SessionRepository(db)

        cutoff = datetime.now(timezone.utc) - timedelta(minutes=settings.session_gap_minutes + 10)
        messages = await msg_repo.get_unassigned_since(
            datetime.now(timezone.utc) - timedelta(days=7),
            settings.tg_group_id,
        )
        # Only consider messages older than gap (session must have ended)
        eligible = [m for m in messages if m.date < cutoff]
        if not eligible:
            return

        raw_sessions = build_sessions(eligible)
        pool = await create_pool(RedisSettings.from_dsn(settings.redis_url))

        try:
            for raw_session in raw_sessions:
                if len(raw_session.messages) < MIN_SESSION_MESSAGES:
                    # Archive without AI processing
                    session = await session_repo.create({
                        "chat_id": settings.tg_group_id,
                        "tg_msg_ids": [m.msg_id for m in raw_session.messages],
                        "started_at": raw_session.started_at,
                        "ended_at": raw_session.ended_at,
                        "status": SessionStatus.archived,
                    })
                    log.info("session_archived_too_short", session_id=session.id, count=len(raw_session.messages))
                    continue

                session = await session_repo.create({
                    "chat_id": settings.tg_group_id,
                    "tg_msg_ids": [m.msg_id for m in raw_session.messages],
                    "started_at": raw_session.started_at,
                    "ended_at": raw_session.ended_at,
                    "status": SessionStatus.queued,
                })
                # Link messages to session
                for msg in raw_session.messages:
                    await db.execute(
                        update(MessageModel)
                        .where(MessageModel.msg_id == msg.msg_id)
                        .values(session_id=session.id)
                    )
                await db.commit()

                await pool.enqueue_job(
                    "process_session", session.id,
                    _job_id=f"process_session_{session.id}",
                )
                log.info("session_queued", session_id=session.id)
        finally:
            await pool.aclose()


async def process_session(ctx: dict, session_id: int) -> None:
    """Main processing pipeline for a single session."""
    redis: aioredis.Redis = ctx["redis"]

    # Distributed lock: prevent concurrent processing of the same session.
    # TTL must exceed job_timeout (3600s) so the lock outlives any legitimate run.
    lock_key = f"session:lock:{session_id}"
    lock_ttl = 3900
    acquired = await redis.set(lock_key, "1", nx=True, ex=lock_ttl)
    if acquired is None:
        log.warning("session_already_locked", session_id=session_id)
        return

    try:
        await _process_session_inner(ctx, session_id)
    finally:
        await redis.delete(lock_key)


async def _process_session_inner(ctx: dict, session_id: int) -> None:
    async with async_session_factory() as db:
        session_repo = SessionRepository(db)
        msg_repo = MessageRepository(db)
        item_repo = KnowledgeItemRepository(db)
        log_repo = ProcessingLogRepository(db)

        session = await session_repo.get(session_id)
        if not session:
            log.error("session_not_found", session_id=session_id)
            return

        # Idempotency: skip if already successfully processed
        if session.status == SessionStatus.processed:
            log.info("session_already_processed", session_id=session_id)
            return

        if session.retry_count >= MAX_RETRIES:
            await session_repo.update_status(session_id, SessionStatus.failed)
            await _notify_failure(ctx, session_id, "Max retries exceeded")
            return

        await session_repo.update_status(session_id, SessionStatus.processing)

        try:
            messages = await msg_repo.get_by_ids(session.tg_msg_ids)
            if not messages:
                raise ValueError("No messages found for session")

            # Structure with Claude
            await log_repo.log(session_id, "structuring", "started")
            duration_minutes = int((session.ended_at - session.started_at).total_seconds() / 60)
            structured = await structure_session(list(messages), session.started_at, duration_minutes)
            await log_repo.log(session_id, "structuring", "completed")

            # Determine session number for this day
            session_number = await _get_session_number(db, session)

            # Get all previous context updates for STARTUP_CONTEXT regeneration
            prev_sessions = await db.execute(
                select(SessionModel)
                .where(
                    SessionModel.structured_json.is_not(None),
                    SessionModel.id != session_id,
                )
                .order_by(SessionModel.started_at)
            )
            prev_structured = [
                s.structured_json for s in prev_sessions.scalars().all()
                if s.structured_json
            ]
            context_updates = [s.get("context_update", "") for s in prev_structured if s.get("context_update")]

            open_questions_items = await item_repo.get_open_questions()
            open_actions_items = await item_repo.get_open_actions()

            all_decisions = []
            for s in prev_structured:
                for d in s.get("decisions", []):
                    all_decisions.append(d)
            for d in structured.get("decisions", []):
                all_decisions.append(d)

            # Generate STARTUP_CONTEXT
            startup_context = await generate_startup_context(
                previous_context_updates=context_updates,
                new_update=structured.get("context_update", ""),
                open_questions=[q.text for q in open_questions_items],
                open_actions=[a.text for a in open_actions_items],
                key_decisions=all_decisions,
            )

            # Write to GitHub (idempotent: skip if already written on a previous attempt)
            await log_repo.log(session_id, "github", "started")
            if session.github_file_path:
                github_path = session.github_file_path
                log.info("github_already_written", session_id=session_id, github_path=github_path)
            else:
                github_path = await write_session_to_github(
                    session=session,
                    structured=structured,
                    session_number=session_number,
                    startup_context=startup_context,
                    all_open_questions=list(open_questions_items),
                    all_open_actions=list(open_actions_items),
                    key_decisions=all_decisions,
                )
                # Persist immediately so retries don't re-create the file
                await session_repo.update_status(
                    session_id, SessionStatus.processing, extra={"github_file_path": github_path}
                )
            github_url = get_session_github_url(github_path)
            await log_repo.log(session_id, "github", "completed")

            # Write to Notion (idempotent: skip if already written on a previous attempt)
            await log_repo.log(session_id, "notion", "started")
            if session.notion_page_id:
                notion_page_id = session.notion_page_id
                log.info("notion_already_written", session_id=session_id, notion_page_id=notion_page_id)
            else:
                notion_page_id, item_notion_ids = await write_session_to_notion(
                    session=session,
                    structured=structured,
                    messages=list(messages),
                    github_link=github_url,
                )
                # Persist immediately so retries don't create duplicate pages
                await session_repo.update_status(
                    session_id, SessionStatus.processing, extra={"notion_page_id": notion_page_id}
                )
            await log_repo.log(session_id, "notion", "completed")

            # Save knowledge items to DB
            items_to_create = []
            for d in structured.get("decisions", []):
                items_to_create.append({
                    "session_id": session_id,
                    "item_type": "decision",
                    "text": d.get("text", ""),
                    "tags": d.get("tags", []),
                    "date": session.started_at,
                    "extra": {"context": d.get("context", "")},
                })
            for q in structured.get("open_questions", []):
                items_to_create.append({
                    "session_id": session_id,
                    "item_type": "open_question",
                    "text": q.get("text", ""),
                    "owner": q.get("owner"),
                    "tags": q.get("tags", []),
                    "date": session.started_at,
                })
            for idea in structured.get("ideas", []):
                items_to_create.append({
                    "session_id": session_id,
                    "item_type": "idea",
                    "text": idea.get("text", ""),
                    "tags": idea.get("tags", []),
                    "date": session.started_at,
                    "extra": {"potential": idea.get("potential")},
                })
            for a in structured.get("action_items", []):
                items_to_create.append({
                    "session_id": session_id,
                    "item_type": "action_item",
                    "text": a.get("text", ""),
                    "owner": a.get("owner"),
                    "tags": a.get("tags", []),
                    "date": session.started_at,
                    "extra": {"due": a.get("due")},
                })
            await item_repo.create_many(items_to_create)

            # Update session as processed
            await session_repo.update_status(
                session_id,
                SessionStatus.processed,
                extra={
                    "notion_page_id": notion_page_id,
                    "github_file_path": github_path,
                    "structured_json": structured,
                },
            )

            await _notify_success(ctx, session_id, structured, github_url)
            log.info("session_processed", session_id=session_id)

        except Exception as e:
            retry_count = await session_repo.increment_retry(session_id)
            await log_repo.log(session_id, "processing", "failed", error=str(e))
            log.exception("session_processing_error", session_id=session_id, retry=retry_count)

            if retry_count >= MAX_RETRIES:
                await session_repo.update_status(session_id, SessionStatus.failed, error=str(e))
                await _notify_failure(ctx, session_id, str(e))
                return

            await session_repo.update_status(session_id, SessionStatus.queued, error=str(e))

            # Re-enqueue with delay
            pool = await create_pool(RedisSettings.from_dsn(settings.redis_url))
            try:
                await pool.enqueue_job(
                    "process_session", session_id,
                    _defer_by=timedelta(minutes=5),
                    _job_id=f"process_session_{session_id}_retry",
                )
            finally:
                await pool.aclose()


async def _get_session_number(db, session) -> int:
    day_start = session.started_at.replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.count()).where(
            SessionModel.started_at >= day_start,
            SessionModel.started_at < day_start + timedelta(days=1),
            SessionModel.id <= session.id,
        )
    )
    return result.scalar_one()


async def _notify_success(ctx: dict, session_id: int, structured: dict, github_url: str) -> None:
    """Send success notification via admin bot."""
    try:
        summary = structured.get("summary", "")[:300]
        decisions_count = len(structured.get("decisions", []))
        actions_count = len(structured.get("action_items", []))
        text = (
            f"✅ Session #{session_id} processed\n\n"
            f"{summary}\n\n"
            f"📊 {decisions_count} decisions, {actions_count} actions\n"
            f"🔗 {github_url}"
        )
        redis: aioredis.Redis = ctx["redis"]
        await redis.publish("bot:notifications", json.dumps({"text": text}))
    except Exception:
        log.warning("notify_success_failed", session_id=session_id)


async def _notify_failure(ctx: dict, session_id: int, error: str) -> None:
    """Send failure notification via admin bot."""
    try:
        redis: aioredis.Redis = ctx["redis"]
        text = f"❌ Session #{session_id} FAILED after {MAX_RETRIES} retries\n\nError: {error[:500]}"
        await redis.publish("bot:notifications", json.dumps({"text": text, "error": True}))
    except Exception:
        log.warning("notify_failure_failed", session_id=session_id)


async def run_backfill(ctx: dict, since_id: int = 0, since_date_str: str | None = None, limit: int = 0) -> None:
    """ARQ task: load Telegram history into the stream. Notifies on start and completion."""
    from datetime import datetime, timezone

    from src.backfill import backfill_core

    redis: aioredis.Redis = ctx["redis"]

    since_date = None
    if since_date_str:
        since_date = datetime.strptime(since_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    start_desc = f"from date {since_date_str}" if since_date_str else f"from message ID {since_id}" if since_id else "from beginning (or checkpoint)"
    await redis.publish("bot:notifications", json.dumps({"text": f"🔄 Backfill started: {start_desc}"}))
    log.info("backfill_task_started", since_id=since_id, since_date_str=since_date_str)

    try:
        total = await backfill_core(redis, since_id=since_id, since_date=since_date, limit=limit)
        await redis.publish("bot:notifications", json.dumps({
            "text": f"✅ Backfill complete: {total} messages loaded into stream. Worker will process sessions automatically."
        }))
    except Exception as e:
        log.exception("backfill_task_error")
        await redis.publish("bot:notifications", json.dumps({
            "text": f"❌ Backfill failed: {str(e)[:300]}", "error": True
        }))
        raise


async def startup(ctx: dict) -> None:
    ctx["redis"] = aioredis.from_url(settings.redis_url, decode_responses=True)
    # consume_stream is an infinite loop — run as background task for the worker's lifetime
    ctx["stream_task"] = asyncio.create_task(consume_stream(ctx))
    log.info("worker_started")


async def shutdown(ctx: dict) -> None:
    task: asyncio.Task | None = ctx.get("stream_task")
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    await ctx["redis"].aclose()
    log.info("worker_stopped")


class WorkerSettings:
    functions = [process_session, build_and_queue_sessions, run_backfill]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    cron_jobs = [
        cron(build_and_queue_sessions, minute={0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}),
    ]
    max_jobs = 10
    job_timeout = 3600  # backfill can run up to 1 hour; resumable via checkpoint
