from datetime import datetime, timezone
from typing import Sequence

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.db.models import KnowledgeItem, Message, ProcessingLog, Session, SessionStatus

log = structlog.get_logger()

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, data: dict) -> Message:
        result = await self.db.execute(
            select(Message).where(Message.msg_id == data["msg_id"])
        )
        msg = result.scalar_one_or_none()
        if msg is None:
            msg = Message(**data)
            self.db.add(msg)
        else:
            for k, v in data.items():
                setattr(msg, k, v)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_unassigned_since(self, since: datetime, chat_id: int) -> Sequence[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id, Message.session_id.is_(None), Message.date >= since)
            .order_by(Message.date)
        )
        return result.scalars().all()

    async def get_by_ids(self, msg_ids: list[int]) -> Sequence[Message]:
        result = await self.db.execute(
            select(Message).where(Message.msg_id.in_(msg_ids)).order_by(Message.date)
        )
        return result.scalars().all()


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Session:
        session = Session(**data)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get(self, session_id: int) -> Session | None:
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()

    async def get_last(self) -> Session | None:
        result = await self.db.execute(
            select(Session).order_by(Session.started_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        session_id: int,
        status: str,
        error: str | None = None,
        extra: dict | None = None,
    ) -> None:
        values: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if error is not None:
            values["last_error"] = error
        if extra:
            values.update(extra)
        await self.db.execute(
            update(Session).where(Session.id == session_id).values(**values)
        )
        await self.db.commit()

    async def increment_retry(self, session_id: int) -> int:
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        session = result.scalar_one_or_none()
        if session is None:
            log.error("session_missing_on_retry", session_id=session_id)
            return 999  # treat as exhausted to avoid re-enqueue loop
        session.retry_count += 1
        await self.db.commit()
        return session.retry_count

    async def list_failed(self) -> Sequence[Session]:
        result = await self.db.execute(
            select(Session).where(Session.status == SessionStatus.failed)
        )
        return result.scalars().all()

    async def count_pending(self) -> int:
        result = await self.db.execute(
            select(Session).where(Session.status.in_([SessionStatus.queued, SessionStatus.processing]))
        )
        return len(result.scalars().all())


class KnowledgeItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, items: list[dict]) -> list[KnowledgeItem]:
        if not items:
            return []
        objs = [KnowledgeItem(**item) for item in items]
        self.db.add_all(objs)
        await self.db.commit()
        return objs

    async def set_notion_id(self, item_id: int, notion_page_id: str) -> None:
        await self.db.execute(
            update(KnowledgeItem)
            .where(KnowledgeItem.id == item_id)
            .values(notion_page_id=notion_page_id)
        )
        await self.db.commit()

    async def get_open_questions(self) -> Sequence[KnowledgeItem]:
        result = await self.db.execute(
            select(KnowledgeItem).where(
                KnowledgeItem.item_type == "open_question",
                KnowledgeItem.status == "open",
            )
        )
        return result.scalars().all()

    async def get_open_actions(self) -> Sequence[KnowledgeItem]:
        result = await self.db.execute(
            select(KnowledgeItem).where(
                KnowledgeItem.item_type == "action_item",
                KnowledgeItem.status.in_(["open", "in_progress"]),
            )
        )
        return result.scalars().all()

    async def close(self, item_id: int) -> str:
        """Mark item as closed. Returns 'ok', 'not_found', or 'already_closed'."""
        result = await self.db.execute(select(KnowledgeItem).where(KnowledgeItem.id == item_id))
        item = result.scalar_one_or_none()
        if item is None:
            return "not_found"
        if item.status == "closed":
            return "already_closed"
        item.status = "closed"
        await self.db.commit()
        return "ok"


class ProcessingLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(self, session_id: int | None, stage: str, status: str, error: str | None = None, details: dict | None = None) -> None:
        entry = ProcessingLog(
            session_id=session_id,
            stage=stage,
            status=status,
            error=error,
            details=details,
        )
        self.db.add(entry)
        await self.db.commit()
