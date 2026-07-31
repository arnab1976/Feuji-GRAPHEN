"""PDF text and table extraction — pdfplumber + PyMuPDF fallback."""
from __future__ import annotations
import io
from pathlib import Path
from typing import Any

from loguru import logger

from leaseguard.config import CHUNK_SIZE, CHUNK_OVERLAP


class PDFExtractor:
    """Extract raw text and tables from commercial lease PDF files."""

    # ── Public API ─────────────────────────────────────────────────────────

    def extract(self, pdf_path: str | Path) -> dict[str, Any]:
        """Extract from a file path on disk."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        with open(path, "rb") as fh:
            data = fh.read()
        return self._process(data, path.name)

    def extract_from_bytes(self, data: bytes, filename: str) -> dict[str, Any]:
        """Extract from raw bytes (e.g. Streamlit UploadedFile)."""
        return self._process(data, filename)

    def chunk_text(
        self,
        text: str,
        chunk_size: int = CHUNK_SIZE,
        overlap: int = CHUNK_OVERLAP,
    ) -> list[str]:
        """
        Split *text* into overlapping chunks for downstream LLM processing.

        Each chunk is at most *chunk_size* characters; consecutive chunks share
        *overlap* characters so entities near a boundary are not lost.
        """
        if not text.strip():
            return []
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            if end == len(text):
                break
            start += chunk_size - overlap
        return chunks

    # ── Internal helpers ───────────────────────────────────────────────────

    def _process(self, data: bytes, filename: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "filename":  filename,
            "pages":     [],
            "full_text": "",
            "tables":    [],
            "page_count": 0,
        }
        try:
            result = self._extract_pdfplumber(data, filename)
        except Exception as exc:
            logger.warning(f"pdfplumber failed for {filename} ({exc}); trying PyMuPDF")
            try:
                result = self._extract_pymupdf(data, filename)
            except Exception as exc2:
                logger.error(f"Both PDF parsers failed for {filename}: {exc2}")
        result["char_count"] = len(result.get("full_text", ""))
        return result

    def _extract_pdfplumber(self, data: bytes, filename: str) -> dict[str, Any]:
        import pdfplumber  # type: ignore

        pages: list[dict] = []
        full_text = ""
        tables: list[list] = []

        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for i, page in enumerate(pdf.pages):
                text   = page.extract_text() or ""
                tbls   = page.extract_tables() or []
                pages.append({"page": i + 1, "text": text, "tables": tbls})
                full_text += text + "\n"
                tables.extend(tbls)

        return {
            "filename":   filename,
            "pages":      pages,
            "full_text":  full_text,
            "tables":     tables,
            "page_count": len(pages),
        }

    def _extract_pymupdf(self, data: bytes, filename: str) -> dict[str, Any]:
        import fitz  # type: ignore  (PyMuPDF)

        pages: list[dict] = []
        full_text = ""

        doc = fitz.open(stream=data, filetype="pdf")
        for i, page in enumerate(doc):
            text = page.get_text("text") or ""
            pages.append({"page": i + 1, "text": text, "tables": []})
            full_text += text + "\n"
        doc.close()

        return {
            "filename":   filename,
            "pages":      pages,
            "full_text":  full_text,
            "tables":     [],
            "page_count": len(pages),
        }
