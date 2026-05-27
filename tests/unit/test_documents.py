"""Tests for document text extraction."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestExtractTextFromPdf:
    def test_extracts_text_from_pages(self):
        from src.processors.documents import extract_text_from_pdf
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Page one content"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Page two content"
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page1, mock_page2]))

        with patch("fitz.open", return_value=mock_doc):
            result = extract_text_from_pdf(Path("test.pdf"))
        assert "Page one content" in result
        assert "Page two content" in result

    def test_returns_none_on_empty_document(self):
        from src.processors.documents import extract_text_from_pdf
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([]))

        with patch("fitz.open", return_value=mock_doc):
            result = extract_text_from_pdf(Path("empty.pdf"))
        assert result is None

    def test_returns_none_on_exception(self):
        from src.processors.documents import extract_text_from_pdf
        with patch("fitz.open", side_effect=Exception("corrupt pdf")):
            result = extract_text_from_pdf(Path("bad.pdf"))
        assert result is None

    def test_joins_pages_with_double_newline(self):
        from src.processors.documents import extract_text_from_pdf
        mock_pages = [MagicMock(get_text=MagicMock(return_value=f"Page {i}")) for i in range(3)]
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter(mock_pages))

        with patch("fitz.open", return_value=mock_doc):
            result = extract_text_from_pdf(Path("test.pdf"))
        assert "\n\n" in result


class TestExtractTextFromDocx:
    def _make_docx_xml(self, paragraphs: list[str]) -> bytes:
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        para_xml = ""
        for p in paragraphs:
            para_xml += f'<w:p xmlns:w="{ns}"><w:r xmlns:w="{ns}"><w:t xmlns:w="{ns}">{p}</w:t></w:r></w:p>'
        return f'<w:document xmlns:w="{ns}"><w:body>{para_xml}</w:body></w:document>'.encode()

    def test_extracts_paragraph_text(self):
        from src.processors.documents import extract_text_from_docx
        import zipfile
        import io

        xml_content = self._make_docx_xml(["Hello", "World"])
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("word/document.xml", xml_content)
        buf.seek(0)

        with patch("builtins.open", return_value=buf):
            with patch("zipfile.ZipFile") as mock_zip:
                mock_zip.return_value.__enter__ = MagicMock(return_value=mock_zip.return_value)
                mock_zip.return_value.__exit__ = MagicMock(return_value=False)
                mock_zip.return_value.read.return_value = xml_content
                result = extract_text_from_docx(Path("test.docx"))
        assert "Hello" in result
        assert "World" in result

    def test_returns_none_on_exception(self):
        from src.processors.documents import extract_text_from_docx
        with patch("zipfile.ZipFile", side_effect=Exception("bad zip")):
            result = extract_text_from_docx(Path("bad.docx"))
        assert result is None


class TestExtractTextFromDocument:
    def test_routes_pdf_to_pdf_extractor(self):
        from src.processors.documents import extract_text_from_document
        with patch("src.processors.documents.extract_text_from_pdf", return_value="pdf text") as mock:
            result = extract_text_from_document(Path("doc.pdf"))
        mock.assert_called_once()
        assert result == "pdf text"

    def test_routes_docx_to_docx_extractor(self):
        from src.processors.documents import extract_text_from_document
        with patch("src.processors.documents.extract_text_from_docx", return_value="docx text") as mock:
            result = extract_text_from_document(Path("doc.docx"))
        mock.assert_called_once()
        assert result == "docx text"

    def test_returns_none_for_unsupported_extension(self):
        from src.processors.documents import extract_text_from_document
        result = extract_text_from_document(Path("image.jpg"))
        assert result is None

    def test_case_insensitive_extension(self):
        from src.processors.documents import extract_text_from_document
        with patch("src.processors.documents.extract_text_from_pdf", return_value="text"):
            result = extract_text_from_document(Path("DOC.PDF"))
        assert result == "text"
