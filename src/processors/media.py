"""Download media files from Telegram via Telethon."""
import asyncio
import io
from pathlib import Path

import structlog
from telethon import TelegramClient
from telethon.errors import FloodWaitError

log = structlog.get_logger()
DOWNLOAD_DIR = Path("/tmp/tg_media")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def download_media(client: TelegramClient, message) -> Path | None:
    """Download message media to a temp file. Returns local path or None."""
    if not message.media:
        return None
    try:
        path = await client.download_media(message, file=str(DOWNLOAD_DIR))
        if path:
            return Path(path)
    except FloodWaitError as e:
        log.warning("flood_wait_download", seconds=e.seconds)
        await asyncio.sleep(e.seconds + 5)
        path = await client.download_media(message, file=str(DOWNLOAD_DIR))
        if path:
            return Path(path)
    except Exception:
        log.exception("media_download_error", msg_id=getattr(message, "id", None))
    return None


async def download_to_bytes(client: TelegramClient, message) -> bytes | None:
    """Download media directly to memory bytes."""
    if not message.media:
        return None
    try:
        buf = io.BytesIO()
        await client.download_media(message, file=buf)
        return buf.getvalue()
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds + 5)
        buf = io.BytesIO()
        await client.download_media(message, file=buf)
        return buf.getvalue()
    except Exception:
        log.exception("media_bytes_error", msg_id=getattr(message, "id", None))
        return None
