"""
LeaseAgent — high-level orchestrator for the full ingest → ask → risk pipeline.

This is the single entry-point used by both the FastAPI endpoints and the
Streamlit UI.  It coordinates all five architectural layers.
"""
from __future__ import annotations
import tempfile
import os
from pathlib import Path
from loguru import logger

from leaseguard.ingestion.pdf_extractor  import PDFExtractor
from leaseguard.llm.extractor_llm        import LLMExtractor
from leaseguard.graph.graph_writer        import GraphWriter
from leaseguard.graph.graph_queries       import GraphQueries
from leaseguard.intelligence.vector_store import VectorStore
from leaseguard.intelligence.graph_rag    import GraphRAG


class LeaseAgent:
    """Coordinates all layers for lease ingestion and Q&A."""

    def __init__(self) -> None:
        self._pdf      = PDFExtractor()
        self._llm_ext  = LLMExtractor()
        self._writer   = GraphWriter()
        self._queries  = GraphQueries()
        self._vector   = VectorStore()
        self._rag      = GraphRAG(
            graph=self._queries,
            vector=self._vector,
        )
        logger.info("LeaseAgent initialised")

    # ── Ingestion ──────────────────────────────────────────────────────────

    def ingest_path(self, pdf_path: str | Path) -> dict:
        """
        Full pipeline: PDF file → Neo4j graph node.

        1. Extract text  (pdfplumber)
        2. Extract entities (LLM → JSON)
        3. Resolve entities (fuzzy match)
        4. Write to Neo4j  (MERGE)
        5. Embed chunks    (ChromaDB)

        Returns a summary dict with lease_id and extracted metadata.
        """
        path = Path(pdf_path)
        logger.info(f"Ingesting {path.name}")

        raw      = self._pdf.extract(str(path))
        data     = self._llm_ext.extract(raw["full_text"])
        lease_id = self._writer.write_lease(data, source_file=raw["filename"])

        chunks   = self._pdf.chunk_text(raw["full_text"])
        n_chunks = self._vector.add_chunks(chunks, lease_id, raw["filename"])

        logger.info(
            f"Ingested {path.name}  lease_id={lease_id}  chunks={n_chunks}"
        )
        return {
            "lease_id":  lease_id,
            "filename":  raw["filename"],
            "pages":     raw["page_count"],
            "chunks":    n_chunks,
            "data":      data,
        }

    def ingest_bytes(self, data: bytes, filename: str) -> dict:
        """Ingest from raw PDF bytes (Streamlit UploadedFile)."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            return self.ingest_path(tmp_path)
        finally:
            os.unlink(tmp_path)

    # ── Q&A ───────────────────────────────────────────────────────────────

    def ask(self, question: str) -> dict:
        """
        Natural-language question → graph-grounded answer.

        Returns:
            answer, graph_context, doc_context, question
        """
        return self._rag.answer(question)

    def cypher(self, question: str) -> dict:
        """LLM-generated Cypher → raw result rows (power-user API)."""
        return self._rag.cypher_answer(question)

    # ── Risk analysis ──────────────────────────────────────────────────────

    def risk(self, lease_id: str) -> str:
        """Structured TOP-3 risk analysis for a specific lease."""
        return self._rag.risk_summary(lease_id)

    def portfolio_narrative(self) -> str:
        """Short executive narrative of the full portfolio."""
        return self._rag.portfolio_summary_narrative()
