"""URL → metadata via webpreview + httpx fallback."""
import re

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

log = structlog.get_logger()
URL_RE = re.compile(r"https?://[^\s]+")


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text or "")


@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=10))
async def fetch_link_metadata(url: str) -> dict | None:
    """Fetch title and description for a URL."""
    try:
        from webpreview import web_preview

        title, description, image = web_preview(url, timeout=10)
        return {
            "url": url,
            "title": title or "",
            "description": description or "",
            "image": image or "",
        }
    except Exception:
        pass

    # Fallback: parse og/meta tags manually
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            html = response.text

        title = _extract_meta(html, "og:title") or _extract_tag(html, "title") or ""
        description = _extract_meta(html, "og:description") or _extract_meta(html, "description") or ""
        return {"url": url, "title": title, "description": description, "image": ""}
    except Exception:
        log.warning("link_metadata_failed", url=url)
        return {"url": url, "title": "", "description": "", "image": ""}


def _extract_meta(html: str, name: str) -> str | None:
    patterns = [
        f'<meta property="{name}" content="([^"]*)"',
        f'<meta name="{name}" content="([^"]*)"',
        f"<meta property='{name}' content='([^']*)'",
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _extract_tag(html: str, tag: str) -> str | None:
    m = re.search(f"<{tag}[^>]*>([^<]+)</{tag}>", html, re.IGNORECASE)
    return m.group(1).strip() if m else None


async def enrich_message_links(text: str) -> list[dict]:
    urls = extract_urls(text)
    results = []
    for url in urls[:5]:  # limit to 5 links per message
        meta = await fetch_link_metadata(url)
        if meta:
            results.append(meta)
    return results
