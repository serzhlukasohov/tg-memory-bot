"""Voice messages → text via OpenAI STT."""
from pathlib import Path

import structlog
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings

log = structlog.get_logger()
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
async def transcribe_audio(audio_path: Path) -> str | None:
    """Transcribe audio file using OpenAI Whisper."""
    client = _get_client()
    try:
        with open(audio_path, "rb") as f:
            response = await client.audio.transcriptions.create(
                model=settings.stt_model,
                file=f,
                response_format="text",
            )
        return str(response).strip()
    except Exception:
        log.exception("transcribe_error", path=str(audio_path))
        raise


async def transcribe_bytes(audio_bytes: bytes, filename: str = "voice.ogg") -> str | None:
    """Transcribe audio from bytes."""
    client = _get_client()
    try:
        import io
        buf = io.BytesIO(audio_bytes)
        buf.name = filename
        response = await client.audio.transcriptions.create(
            model=settings.stt_model,
            file=buf,
            response_format="text",
        )
        return str(response).strip()
    except Exception:
        log.exception("transcribe_bytes_error")
        return None
