"""Tests for Claude Vision OCR."""
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _make_anthropic_response(text: str) -> MagicMock:
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    return resp


class TestExtractTextFromImage:
    async def test_returns_extracted_text(self):
        from src.processors.ocr import extract_text_from_image
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_anthropic_response("Extracted text")
        )

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with patch.object(Path, "read_bytes", return_value=b"image bytes"):
                result = await extract_text_from_image(Path("image.png"))

        assert result == "Extracted text"

    async def test_returns_none_for_unsupported_format(self):
        from src.processors.ocr import extract_text_from_image
        result = await extract_text_from_image(Path("document.bmp"))
        assert result is None

    async def test_returns_none_when_extracted_text_is_empty(self):
        from src.processors.ocr import extract_text_from_image
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_anthropic_response("   ")
        )

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with patch.object(Path, "read_bytes", return_value=b"image"):
                result = await extract_text_from_image(Path("image.jpg"))

        assert result is None

    async def test_uses_correct_media_type_for_jpg(self):
        from src.processors.ocr import extract_text_from_image
        mock_client = AsyncMock()
        captured = {}

        async def capture_create(**kwargs):
            msg_content = kwargs["messages"][0]["content"]
            captured["media_type"] = msg_content[0]["source"]["media_type"]
            return _make_anthropic_response("text")

        mock_client.messages.create = capture_create

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with patch.object(Path, "read_bytes", return_value=b"image"):
                await extract_text_from_image(Path("photo.jpg"))

        assert captured["media_type"] == "image/jpeg"

    async def test_uses_correct_media_type_for_png(self):
        from src.processors.ocr import extract_text_from_image
        mock_client = AsyncMock()
        captured = {}

        async def capture_create(**kwargs):
            msg_content = kwargs["messages"][0]["content"]
            captured["media_type"] = msg_content[0]["source"]["media_type"]
            return _make_anthropic_response("text")

        mock_client.messages.create = capture_create

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with patch.object(Path, "read_bytes", return_value=b"image"):
                await extract_text_from_image(Path("screenshot.png"))

        assert captured["media_type"] == "image/png"

    async def test_re_raises_exception_after_retries(self):
        from src.processors.ocr import extract_text_from_image
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API error"))

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with patch.object(Path, "read_bytes", return_value=b"image"):
                # tenacity may wrap the exception in RetryError
                with pytest.raises(Exception):
                    await extract_text_from_image(Path("image.jpg"))

    async def test_supported_formats(self):
        from src.processors.ocr import SUPPORTED_IMAGE_EXTS
        assert ".jpg" in SUPPORTED_IMAGE_EXTS
        assert ".jpeg" in SUPPORTED_IMAGE_EXTS
        assert ".png" in SUPPORTED_IMAGE_EXTS
        assert ".gif" in SUPPORTED_IMAGE_EXTS
        assert ".webp" in SUPPORTED_IMAGE_EXTS


class TestExtractTextFromBytes:
    async def test_returns_extracted_text(self):
        from src.processors.ocr import extract_text_from_bytes
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_anthropic_response("Text from bytes")
        )

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            result = await extract_text_from_bytes(b"image bytes", "image/png")

        assert result == "Text from bytes"

    async def test_raises_on_exception_after_retries(self):
        from src.processors.ocr import extract_text_from_bytes
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("fail"))

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            with pytest.raises(Exception):
                await extract_text_from_bytes(b"image bytes")

    async def test_returns_none_for_empty_result(self):
        from src.processors.ocr import extract_text_from_bytes
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_anthropic_response("")
        )

        with patch("src.processors.ocr._get_client", return_value=mock_client):
            result = await extract_text_from_bytes(b"image bytes")

        assert result is None
