"""Tests for URL extraction and link metadata fetching."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestExtractUrls:
    def test_extracts_http_url(self):
        from src.processors.links import extract_urls
        text = "Check out http://example.com for details"
        assert "http://example.com" in extract_urls(text)

    def test_extracts_https_url(self):
        from src.processors.links import extract_urls
        urls = extract_urls("Visit https://example.com/path?q=1")
        assert len(urls) == 1
        assert "https://example.com/path?q=1" in urls

    def test_extracts_multiple_urls(self):
        from src.processors.links import extract_urls
        text = "See https://a.com and https://b.com"
        urls = extract_urls(text)
        assert len(urls) == 2

    def test_returns_empty_list_for_no_urls(self):
        from src.processors.links import extract_urls
        assert extract_urls("no links here") == []

    def test_returns_empty_list_for_empty_string(self):
        from src.processors.links import extract_urls
        assert extract_urls("") == []

    def test_returns_empty_list_for_none_input(self):
        from src.processors.links import extract_urls
        assert extract_urls(None) == []


class TestExtractMeta:
    def test_extracts_og_title(self):
        from src.processors.links import _extract_meta
        html = '<meta property="og:title" content="Test Title">'
        assert _extract_meta(html, "og:title") == "Test Title"

    def test_extracts_meta_name(self):
        from src.processors.links import _extract_meta
        html = '<meta name="description" content="A page description">'
        assert _extract_meta(html, "description") == "A page description"

    def test_returns_none_when_not_found(self):
        from src.processors.links import _extract_meta
        assert _extract_meta("<html></html>", "og:title") is None

    def test_case_insensitive(self):
        from src.processors.links import _extract_meta
        html = '<META PROPERTY="og:title" CONTENT="Title">'
        assert _extract_meta(html, "og:title") == "Title"


class TestExtractTag:
    def test_extracts_title_tag(self):
        from src.processors.links import _extract_tag
        html = "<title>Page Title</title>"
        assert _extract_tag(html, "title") == "Page Title"

    def test_returns_none_when_not_found(self):
        from src.processors.links import _extract_tag
        assert _extract_tag("<html></html>", "title") is None


class TestFetchLinkMetadata:
    # web_preview is imported inside the function body, so patch at its source module
    async def test_uses_webpreview_first(self):
        from src.processors.links import fetch_link_metadata
        with patch("webpreview.web_preview", return_value=("Title", "Desc", "img.jpg")):
            result = await fetch_link_metadata("https://example.com")
        assert result["title"] == "Title"
        assert result["description"] == "Desc"

    async def test_falls_back_to_httpx_when_webpreview_fails(self):
        from src.processors.links import fetch_link_metadata
        html = '<meta property="og:title" content="Fallback Title">'

        mock_response = MagicMock()
        mock_response.text = html

        with patch("webpreview.web_preview", side_effect=Exception("fail")):
            with patch("httpx.AsyncClient") as mock_client_cls:
                mock_client = AsyncMock()
                mock_client.__aenter__ = AsyncMock(return_value=mock_client)
                mock_client.__aexit__ = AsyncMock(return_value=False)
                mock_client.get = AsyncMock(return_value=mock_response)
                mock_client_cls.return_value = mock_client

                result = await fetch_link_metadata("https://example.com")
        assert result["title"] == "Fallback Title"

    async def test_returns_empty_metadata_on_total_failure(self):
        from src.processors.links import fetch_link_metadata
        with patch("webpreview.web_preview", side_effect=Exception("fail")):
            with patch("httpx.AsyncClient", side_effect=Exception("network fail")):
                result = await fetch_link_metadata("https://example.com")
        assert result is not None
        assert result["url"] == "https://example.com"

    async def test_url_preserved_in_result(self):
        from src.processors.links import fetch_link_metadata
        url = "https://example.com"
        with patch("webpreview.web_preview", return_value=("T", "D", "")):
            result = await fetch_link_metadata(url)
        assert result["url"] == url


class TestEnrichMessageLinks:
    async def test_limits_to_five_urls(self):
        from src.processors.links import enrich_message_links
        urls = " ".join(f"https://example{i}.com" for i in range(10))

        with patch("src.processors.links.fetch_link_metadata", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = {"url": "x", "title": "X", "description": ""}
            result = await enrich_message_links(urls)
        assert len(result) <= 5
        assert mock_fetch.call_count <= 5

    async def test_returns_empty_list_for_no_urls(self):
        from src.processors.links import enrich_message_links
        result = await enrich_message_links("no links here")
        assert result == []

    async def test_returns_metadata_list(self):
        from src.processors.links import enrich_message_links
        with patch("src.processors.links.fetch_link_metadata", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = {"url": "https://example.com", "title": "Test", "description": ""}
            result = await enrich_message_links("https://example.com")
        assert len(result) == 1
        assert result[0]["title"] == "Test"
