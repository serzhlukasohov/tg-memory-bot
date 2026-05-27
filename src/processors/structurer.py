"""Claude API: conversation → structured JSON knowledge."""
import json
from datetime import datetime

import structlog
from anthropic import AsyncAnthropic
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.config import settings
from src.db.models import Message
from src.processors.session_builder import format_conversation

log = structlog.get_logger()
_client: AsyncAnthropic | None = None

SYSTEM_PROMPT = """You are a startup knowledge librarian. Your job is to analyze a conversation \
between two founders and extract structured knowledge.

Output STRICT JSON, no prose, no markdown fences."""

USER_PROMPT_TEMPLATE = """SESSION DATE: {date}
PARTICIPANTS: {participants}
DURATION: ~{duration} minutes

CONVERSATION:
{formatted_messages}

Extract and return this exact JSON structure:
{{
  "summary": "<2-3 sentences what this session was about>",
  "energy": "high|medium|low",
  "main_topics": ["topic1", "topic2"],
  "decisions": [
    {{
      "text": "<what was decided>",
      "context": "<why, brief>",
      "tags": ["tag1"]
    }}
  ],
  "open_questions": [
    {{
      "text": "<the question>",
      "owner": "<name or null>",
      "tags": ["tag1"]
    }}
  ],
  "ideas": [
    {{
      "text": "<the idea>",
      "potential": "high|medium|low",
      "tags": ["tag1"]
    }}
  ],
  "action_items": [
    {{
      "text": "<what to do>",
      "owner": "<name or null>",
      "due": "<date string or null>",
      "tags": ["tag1"]
    }}
  ],
  "context_update": "<1 paragraph — what changed in the startup context after this session>"
}}"""

FIX_JSON_PROMPT = "Fix this JSON, output ONLY valid JSON: {broken_output}"


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


class JSONParseError(Exception):
    pass


class StructureValidationError(Exception):
    pass


_REQUIRED_KEYS = {"summary", "energy", "main_topics", "decisions", "open_questions", "ideas", "action_items", "context_update"}
_LIST_KEYS = {"main_topics", "decisions", "open_questions", "ideas", "action_items"}
_VALID_ENERGY = {"high", "medium", "low"}


def _validate_and_normalize(data: dict) -> dict:
    """Validate required keys and types; fill safe defaults for missing optional structure."""
    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        raise StructureValidationError(f"Claude response missing required keys: {missing}")

    # Normalize types — Claude occasionally returns a string instead of a list
    for key in _LIST_KEYS:
        if not isinstance(data[key], list):
            log.warning("structure_key_wrong_type", key=key, got=type(data[key]).__name__)
            data[key] = []

    if data["energy"] not in _VALID_ENERGY:
        log.warning("structure_invalid_energy", energy=data["energy"])
        data["energy"] = "medium"

    return data


async def _call_claude(messages: list[dict]) -> str:
    client = _get_client()
    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text.strip()


def _parse_json(text: str) -> dict:
    # Strip markdown fences if Claude added them despite instructions
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise JSONParseError(f"JSON parse failed: {e}") from e


@retry(
    retry=retry_if_exception_type(JSONParseError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def structure_session(
    messages: list[Message],
    session_date: datetime,
    duration_minutes: int,
) -> dict:
    """Call Claude to extract structured knowledge from a session."""
    participants = sorted({msg.author_name for msg in messages if msg.author_name})
    conversation_text = format_conversation(messages)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        date=session_date.strftime("%Y-%m-%d %H:%M UTC"),
        participants=", ".join(participants) if participants else "Unknown",
        duration=duration_minutes,
        formatted_messages=conversation_text,
    )

    conversation: list[dict] = [{"role": "user", "content": user_prompt}]
    raw = await _call_claude(conversation)

    try:
        parsed = _parse_json(raw)
    except JSONParseError:
        log.warning("json_parse_retry", raw_snippet=raw[:200])
        fix_messages = conversation + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": FIX_JSON_PROMPT.format(broken_output=raw)},
        ]
        fixed_raw = await _call_claude(fix_messages)
        parsed = _parse_json(fixed_raw)

    return _validate_and_normalize(parsed)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
async def generate_startup_context(
    previous_context_updates: list[str],
    new_update: str,
    open_questions: list[str],
    open_actions: list[str],
    key_decisions: list[dict],
) -> str:
    """Generate the STARTUP_CONTEXT.md content via Claude."""
    client = _get_client()

    updates_text = "\n\n".join(
        f"Update {i + 1}:\n{u}" for i, u in enumerate(previous_context_updates[-20:])
    )
    decisions_text = "\n".join(
        f"- [{d.get('date', '')}] {d.get('text', '')}" for d in key_decisions[-10:]
    )
    questions_text = "\n".join(f"- {q}" for q in open_questions)
    actions_text = "\n".join(f"- {a}" for a in open_actions)

    prompt = f"""You are synthesizing a startup context snapshot. Based on the session updates below, write a STARTUP_CONTEXT.md document.

PREVIOUS CONTEXT UPDATES:
{updates_text}

LATEST UPDATE:
{new_update}

KEY DECISIONS (chronological):
{decisions_text}

OPEN QUESTIONS:
{questions_text}

OPEN ACTION ITEMS:
{actions_text}

Write the document in this exact format:

# Startup Context
_Last updated: {{datetime}}_

## What we're building
{{актуальное описание продукта из всех решений}}

## Current Status
{{текущий статус и приоритеты}}

## Key Decisions Made
{{топ-10 самых важных решений с датами}}

## Open Questions
{{все открытые вопросы}}

## Next Actions
{{все открытые action items}}

Use the actual current datetime. Be concise and factual."""

    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()
