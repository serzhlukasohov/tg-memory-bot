"""Notion API writer with rate limiting."""
from datetime import datetime

import structlog
from aiolimiter import AsyncLimiter
from notion_client import AsyncClient
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from src.config import settings
from src.db.models import Message, Session

log = structlog.get_logger()

# Notion limits: 3 req/s, we use 2 to be safe
_limiter = AsyncLimiter(2, 1)

ENERGY_COLORS = {"high": "green", "medium": "yellow", "low": "red"}
ITEM_TYPE_COLORS = {
    "decision": "green",
    "open_question": "blue",
    "idea": "purple",
    "action_item": "orange",
}
NOTION_API_VERSION = "2025-09-03"

_notion: AsyncClient | None = None


def _get_client() -> AsyncClient:
    global _notion
    if _notion is None:
        _notion = AsyncClient(
            auth=settings.notion_token,
            notion_version=NOTION_API_VERSION,
        )
    return _notion


def _chunks(text: str, size: int = 1900) -> list[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def _rich_text(text: str) -> list[dict]:
    return [{"type": "text", "text": {"content": chunk}} for chunk in _chunks(text)]


def _paragraph(text: str) -> dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": _rich_text(text)}}


def _heading2(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _bullet(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": _rich_text(text[:2000])},
    }


def _todo(text: str, checked: bool = False) -> dict:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {"rich_text": _rich_text(text[:2000]), "checked": checked},
    }


def _callout(text: str, emoji: str = "ℹ️") -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": _rich_text(text[:2000]),
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


@retry(stop=stop_after_attempt(5), wait=wait_exponential_jitter(initial=2, max=60))
async def _api_call(coro):
    async with _limiter:
        return await coro


async def _append_blocks_paginated(page_id: str, blocks: list[dict]) -> None:
    """Append blocks in batches of 100 (Notion limit)."""
    notion = _get_client()
    for i in range(0, len(blocks), 100):
        batch = blocks[i : i + 100]
        await _api_call(
            notion.blocks.children.append(block_id=page_id, children=batch)
        )


def _build_session_blocks(structured: dict, messages: list[Message]) -> list[dict]:
    blocks: list[dict] = []

    # Callout with metadata
    energy = structured.get("energy", "medium")
    participants = sorted({msg.author_name for msg in messages if msg.author_name})
    meta_text = (
        f"Participants: {', '.join(participants)} | Energy: {energy.upper()} | "
        f"Topics: {', '.join(structured.get('main_topics', []))}"
    )
    blocks.append(_callout(meta_text, "📊"))

    # Summary
    blocks.append(_heading2("📋 Summary"))
    blocks.append(_paragraph(structured.get("summary", "")))

    # Decisions
    decisions = structured.get("decisions", [])
    if decisions:
        blocks.append(_heading2("✅ Decisions"))
        for d in decisions:
            tags = " _" + ", ".join(d.get("tags", [])) + "_" if d.get("tags") else ""
            blocks.append(_bullet(f"{d.get('text', '')}{tags}"))

    # Open Questions
    questions = structured.get("open_questions", [])
    if questions:
        blocks.append(_heading2("❓ Open Questions"))
        for q in questions:
            owner = f" — @{q['owner']}" if q.get("owner") else ""
            blocks.append(_bullet(f"{q.get('text', '')}{owner}"))

    # Ideas
    ideas = structured.get("ideas", [])
    if ideas:
        blocks.append(_heading2("💡 Ideas"))
        for idea in ideas:
            potential = f"[{idea.get('potential', 'medium')}] " if idea.get("potential") else ""
            blocks.append(_bullet(f"{potential}{idea.get('text', '')}"))

    # Action Items
    actions = structured.get("action_items", [])
    if actions:
        blocks.append(_heading2("📌 Action Items"))
        for a in actions:
            owner = f"@{a['owner']}: " if a.get("owner") else ""
            due = f" (due: {a['due']})" if a.get("due") else ""
            blocks.append(_todo(f"{owner}{a.get('text', '')}{due}"))

    # Context Update
    context_update = structured.get("context_update", "")
    if context_update:
        blocks.append(_heading2("🔄 Context Update"))
        blocks.append(_paragraph(context_update))

    # Original conversation
    blocks.append(_heading2("💬 Original Conversation"))
    conversation_parts: list[str] = []
    for msg in messages:
        name = msg.author_name or f"user_{msg.author_id}"
        time_str = msg.date.strftime("%H:%M")
        text = msg.text or (f"[Voice: {msg.transcription}]" if msg.transcription else "[media]")
        conversation_parts.append(f"[{time_str}] {name}: {text}")

    full_convo = "\n".join(conversation_parts)
    for chunk in _chunks(full_convo, 1900):
        blocks.append(_paragraph(chunk))

    return blocks


async def create_session_page(
    session: Session,
    structured: dict,
    messages: list[Message],
    github_link: str | None = None,
) -> str:
    """Create a session page in Notion Sessions DB. Returns notion_page_id."""
    notion = _get_client()
    participants = sorted({msg.author_name for msg in messages if msg.author_name})
    session_title = f"Session {session.started_at.strftime('%Y-%m-%d %H:%M')} — {structured.get('summary', '')[:60]}…"

    duration_minutes = int((session.ended_at - session.started_at).total_seconds() / 60)

    properties: dict = {
        "Title": {"title": [{"text": {"content": session_title[:255]}}]},
        "Date": {"date": {"start": session.started_at.isoformat()}},
        "Duration": {"number": duration_minutes},
        "Participants": {
            "multi_select": [{"name": p} for p in participants]
        },
        "Main Topics": {
            "multi_select": [{"name": t} for t in structured.get("main_topics", [])[:10]]
        },
        "Energy": {
            "select": {
                "name": structured.get("energy", "medium"),
                "color": ENERGY_COLORS.get(structured.get("energy", "medium"), "default"),
            }
        },
        "Decisions Count": {"number": len(structured.get("decisions", []))},
        "Open Questions Count": {"number": len(structured.get("open_questions", []))},
        "Action Items Count": {"number": len(structured.get("action_items", []))},
        "Summary": {"rich_text": _rich_text(structured.get("summary", "")[:2000])},
        "Status": {"status": {"name": "processed"}},
    }
    if github_link:
        properties["GitHub Link"] = {"url": github_link}

    # Create page without children first (faster)
    response = await _api_call(
        notion.pages.create(
            parent={"database_id": settings.notion_sessions_db_id},
            properties=properties,
        )
    )
    page_id: str = response["id"]

    # Append content blocks
    blocks = _build_session_blocks(structured, messages)
    await _append_blocks_paginated(page_id, blocks)

    log.info("notion_session_created", page_id=page_id)
    return page_id


async def create_knowledge_item(
    item_type: str,
    text: str,
    owner: str | None,
    tags: list[str],
    session_page_id: str,
    session_date: datetime,
    extra: dict | None = None,
) -> str:
    """Create a knowledge item page in Notion Items DB. Returns notion_page_id."""
    notion = _get_client()

    properties: dict = {
        "Title": {"title": [{"text": {"content": text[:255]}}]},
        "Type": {
            "select": {
                "name": item_type,
                "color": ITEM_TYPE_COLORS.get(item_type, "default"),
            }
        },
        "Status": {"select": {"name": "open"}},
        "Tags": {"multi_select": [{"name": t} for t in tags[:10]]},
        "Session": {"relation": [{"id": session_page_id}]},
        "Date": {"date": {"start": session_date.isoformat()}},
    }
    if owner:
        properties["Owner"] = {"rich_text": [{"text": {"content": owner[:256]}}]}

    if extra and extra.get("potential"):
        properties["Priority"] = {"select": {"name": extra["potential"]}}

    response = await _api_call(
        notion.pages.create(
            parent={"database_id": settings.notion_items_db_id},
            properties=properties,
        )
    )
    page_id: str = response["id"]
    log.info("notion_item_created", page_id=page_id, item_type=item_type)
    return page_id


async def write_session_to_notion(
    session: Session,
    structured: dict,
    messages: list[Message],
    github_link: str | None = None,
) -> tuple[str, list[str]]:
    """
    Write full session to Notion. Returns (session_page_id, [item_page_ids]).
    Idempotent — checks session.notion_page_id before creating.
    """
    session_page_id = await create_session_page(session, structured, messages, github_link)

    item_ids: list[str] = []

    for decision in structured.get("decisions", []):
        pid = await create_knowledge_item(
            "decision",
            decision.get("text", ""),
            None,
            decision.get("tags", []),
            session_page_id,
            session.started_at,
        )
        item_ids.append(pid)

    for question in structured.get("open_questions", []):
        pid = await create_knowledge_item(
            "open_question",
            question.get("text", ""),
            question.get("owner"),
            question.get("tags", []),
            session_page_id,
            session.started_at,
        )
        item_ids.append(pid)

    for idea in structured.get("ideas", []):
        pid = await create_knowledge_item(
            "idea",
            idea.get("text", ""),
            None,
            idea.get("tags", []),
            session_page_id,
            session.started_at,
            extra={"potential": idea.get("potential")},
        )
        item_ids.append(pid)

    for action in structured.get("action_items", []):
        pid = await create_knowledge_item(
            "action_item",
            action.get("text", ""),
            action.get("owner"),
            action.get("tags", []),
            session_page_id,
            session.started_at,
        )
        item_ids.append(pid)

    return session_page_id, item_ids
