"""Images → text via Claude vision."""
import base64
from pathlib import Path

import structlog
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings

log = structlog.get_logger()
_client: AsyncAnthropic | None = None

SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
async def extract_text_from_image(image_path: Path) -> str | None:
    """Extract text from image using Claude vision."""
    suffix = image_path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_EXTS:
        return None

    media_type = MEDIA_TYPE_MAP.get(suffix, "image/jpeg")
    client = _get_client()

    try:
        image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")
        response = await client.messages.create(
            model=settings.claude_model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from this image. Return only the text, no commentary.",
                        },
                    ],
                }
            ],
        )
        text = response.content[0].text.strip()
        return text if text else None
    except Exception:
        log.exception("ocr_error", path=str(image_path))
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
async def extract_text_from_bytes(image_bytes: bytes, media_type: str = "image/jpeg") -> str | None:
    """Extract text from image bytes."""
    client = _get_client()
    try:
        image_data = base64.standard_b64encode(image_bytes).decode("utf-8")
        response = await client.messages.create(
            model=settings.claude_model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from this image. Return only the text, no commentary.",
                        },
                    ],
                }
            ],
        )
        return response.content[0].text.strip() or None
    except Exception:
        log.exception("ocr_bytes_error")
        raise
