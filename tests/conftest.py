"""Shared fixtures and test configuration."""
import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Patch settings before any src import so pydantic-settings doesn't read .env
os.environ.setdefault("TG_API_ID", "12345")
os.environ.setdefault("TG_API_HASH", "testhash")
os.environ.setdefault("TG_SESSION_STRING", "testsession")
os.environ.setdefault("TG_GROUP_ID", "-1001234567890")
os.environ.setdefault("TG_BOT_TOKEN", "123:testtoken")
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test")
os.environ.setdefault("OPENAI_API_KEY", "sk-test")
os.environ.setdefault("NOTION_TOKEN", "secret_test")
os.environ.setdefault("NOTION_SESSIONS_DB_ID", "sessions-db-id")
os.environ.setdefault("NOTION_ITEMS_DB_ID", "items-db-id")
os.environ.setdefault("GITHUB_TOKEN", "ghp_test")
os.environ.setdefault("GITHUB_REPO", "user/startup-memory")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/testdb")


def make_message(
    msg_id: int = 1,
    chat_id: int = -1001234567890,
    date: datetime | None = None,
    text: str = "test message",
    author_id: int = 100,
    author_name: str = "Alice",
    has_media: bool = False,
    media_type: str | None = None,
    grouped_id: int | None = None,
    reply_to_msg_id: int | None = None,
    transcription: str | None = None,
    ocr_text: str | None = None,
    link_metadata: dict | None = None,
    session_id: int | None = None,
) -> MagicMock:
    msg = MagicMock()
    msg.msg_id = msg_id
    msg.chat_id = chat_id
    msg.date = date or datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
    msg.text = text
    msg.author_id = author_id
    msg.author_name = author_name
    msg.has_media = has_media
    msg.media_type = media_type
    msg.grouped_id = grouped_id
    msg.reply_to_msg_id = reply_to_msg_id
    msg.transcription = transcription
    msg.ocr_text = ocr_text
    msg.link_metadata = link_metadata
    msg.session_id = session_id
    return msg


def make_session(
    session_id: int = 1,
    chat_id: int = -1001234567890,
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
    status: str = "queued",
    tg_msg_ids: list[int] | None = None,
    structured_json: dict | None = None,
    notion_page_id: str | None = None,
    github_file_path: str | None = None,
    retry_count: int = 0,
    last_error: str | None = None,
) -> MagicMock:
    s = MagicMock()
    s.id = session_id
    s.chat_id = chat_id
    s.started_at = started_at or datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
    s.ended_at = ended_at or datetime(2026, 5, 27, 12, 0, 0, tzinfo=timezone.utc)
    s.status = status
    s.tg_msg_ids = tg_msg_ids or [1, 2, 3]
    s.structured_json = structured_json
    s.notion_page_id = notion_page_id
    s.github_file_path = github_file_path
    s.retry_count = retry_count
    s.last_error = last_error
    return s


SAMPLE_STRUCTURED = {
    "summary": "We decided to launch on ProductHunt next week and set the pricing.",
    "energy": "high",
    "main_topics": ["launch", "pricing"],
    "decisions": [
        {"text": "Launch on ProductHunt", "context": "Best channel for B2B SaaS", "tags": ["launch"]},
        {"text": "Charge $49/seat/month", "context": "Competitive pricing", "tags": ["pricing"]},
    ],
    "open_questions": [
        {"text": "Do we need SOC2?", "owner": "Alice", "tags": ["compliance"]},
    ],
    "ideas": [
        {"text": "Build a referral program", "potential": "high", "tags": ["growth"]},
    ],
    "action_items": [
        {"text": "Set up Stripe billing", "owner": "Bob", "due": "2026-05-30", "tags": ["billing"]},
    ],
    "context_update": "Team committed to ProductHunt launch. Pricing locked.",
}
