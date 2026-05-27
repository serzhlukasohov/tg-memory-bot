"""Tests for OpenAI STT transcription."""
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest


class TestTranscribeAudio:
    async def test_returns_transcription_text(self):
        from src.processors.transcribe import transcribe_audio
        mock_client = MagicMock()
        mock_client.audio = MagicMock()
        mock_client.audio.transcriptions = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(return_value="Hello world")

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            with patch("builtins.open", mock_open(read_data=b"audio bytes")):
                result = await transcribe_audio(Path("voice.ogg"))

        assert result == "Hello world"

    async def test_strips_whitespace(self):
        from src.processors.transcribe import transcribe_audio
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(return_value="  spaced output  ")

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            with patch("builtins.open", mock_open(read_data=b"audio")):
                result = await transcribe_audio(Path("voice.ogg"))

        assert result == "spaced output"

    async def test_uses_configured_model(self):
        from src.processors.transcribe import transcribe_audio
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(return_value="text")
        captured = {}

        async def capture_create(**kwargs):
            captured.update(kwargs)
            return "text"

        mock_client.audio.transcriptions.create = capture_create

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            with patch("builtins.open", mock_open(read_data=b"audio")):
                await transcribe_audio(Path("voice.ogg"))

        assert captured.get("model") == "gpt-4o-mini-transcribe"

    async def test_re_raises_exception_after_retries(self):
        from src.processors.transcribe import transcribe_audio
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(side_effect=Exception("API error"))

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            with patch("builtins.open", mock_open(read_data=b"audio")):
                # tenacity may wrap in RetryError after exhausting attempts
                with pytest.raises(Exception):
                    await transcribe_audio(Path("voice.ogg"))


class TestTranscribeBytes:
    async def test_returns_transcription(self):
        from src.processors.transcribe import transcribe_bytes
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(return_value="transcribed")

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            result = await transcribe_bytes(b"audio bytes")

        assert result == "transcribed"

    async def test_returns_none_on_exception(self):
        from src.processors.transcribe import transcribe_bytes
        mock_client = MagicMock()
        mock_client.audio.transcriptions.create = AsyncMock(side_effect=Exception("fail"))

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            result = await transcribe_bytes(b"audio bytes")

        assert result is None

    async def test_uses_provided_filename(self):
        from src.processors.transcribe import transcribe_bytes
        mock_client = MagicMock()
        captured = {}

        async def capture_create(**kwargs):
            buf = kwargs.get("file")
            captured["name"] = getattr(buf, "name", None)
            return "text"

        mock_client.audio.transcriptions.create = capture_create

        with patch("src.processors.transcribe._get_client", return_value=mock_client):
            await transcribe_bytes(b"audio", filename="recording.mp3")

        assert captured["name"] == "recording.mp3"
