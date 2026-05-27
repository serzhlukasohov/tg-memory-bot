"""Groups raw messages into Session objects."""
from datetime import timedelta
from typing import NamedTuple

from src.config import settings
from src.db.models import Message


class RawSession(NamedTuple):
    messages: list[Message]
    started_at: object
    ended_at: object


def build_sessions(messages: list[Message]) -> list[RawSession]:
    """Split a sorted list of messages into sessions by time gap."""
    if not messages:
        return []

    gap = timedelta(minutes=settings.session_gap_minutes)
    sessions: list[RawSession] = []
    bucket: list[Message] = [messages[0]]

    for msg in messages[1:]:
        if msg.date - bucket[-1].date > gap:
            sessions.append(RawSession(bucket, bucket[0].date, bucket[-1].date))
            bucket = [msg]
        else:
            bucket.append(msg)

    sessions.append(RawSession(bucket, bucket[0].date, bucket[-1].date))
    return sessions


def merge_albums(messages: list[Message]) -> list[Message | list[Message]]:
    """Group messages with the same grouped_id together."""
    albums: dict[int, list[Message]] = {}
    result: list[Message | list[Message]] = []

    for msg in messages:
        if msg.grouped_id:
            albums.setdefault(msg.grouped_id, []).append(msg)
        else:
            result.append(msg)

    # Insert albums in chronological order by first message date
    album_list = sorted(albums.values(), key=lambda g: g[0].date)
    all_items: list[tuple[object, object]] = [(msg.date, msg) for msg in result]
    for group in album_list:
        all_items.append((group[0].date, group))

    all_items.sort(key=lambda x: x[0])
    return [item for _, item in all_items]


def build_reply_tree(messages: list[Message]) -> dict[int, list[Message]]:
    """Build {parent_msg_id: [reply_messages]} mapping."""
    tree: dict[int, list[Message]] = {}
    for msg in messages:
        if msg.reply_to_msg_id:
            tree.setdefault(msg.reply_to_msg_id, []).append(msg)
    return tree


def format_conversation(messages: list[Message]) -> str:
    """Format messages as readable conversation text for Claude."""
    lines: list[str] = []
    for msg in messages:
        name = msg.author_name or f"user_{msg.author_id}"
        time_str = msg.date.strftime("%H:%M")
        parts: list[str] = []

        if msg.text:
            parts.append(msg.text)
        if msg.transcription:
            parts.append(f"[Voice: {msg.transcription}]")
        if msg.ocr_text:
            parts.append(f"[Image text: {msg.ocr_text}]")
        if msg.link_metadata:
            meta = msg.link_metadata
            parts.append(f"[Link: {meta.get('title', '')} — {meta.get('description', '')}]")

        content = " | ".join(parts) if parts else "[media]"
        lines.append(f"[{time_str}] {name}: {content}")

    return "\n".join(lines)
