"""PDF/DOCX → text via PyMuPDF."""
from pathlib import Path

import structlog

log = structlog.get_logger()


def extract_text_from_pdf(path: Path) -> str | None:
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(str(path))
        pages = [page.get_text() for page in doc]
        doc.close()
        return "\n\n".join(pages).strip() or None
    except Exception:
        log.exception("pdf_extract_error", path=str(path))
        return None


def extract_text_from_docx(path: Path) -> str | None:
    try:
        import zipfile
        import xml.etree.ElementTree as ET

        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with zipfile.ZipFile(str(path)) as zf:
            xml_content = zf.read("word/document.xml")

        tree = ET.fromstring(xml_content)
        paragraphs = []
        for para in tree.iter(f"{ns}p"):
            texts = [node.text for node in para.iter(f"{ns}t") if node.text]
            paragraphs.append("".join(texts))
        return "\n".join(paragraphs).strip() or None
    except Exception:
        log.exception("docx_extract_error", path=str(path))
        return None


def extract_text_from_document(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif suffix in (".docx", ".doc"):
        return extract_text_from_docx(path)
    return None
