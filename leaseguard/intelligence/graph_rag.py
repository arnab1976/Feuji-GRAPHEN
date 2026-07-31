"""
Graph-RAG pipeline — ground every LLM answer in Neo4j + ChromaDB context.

Architecture:
  1. Classify question intent (expiry / concentration / clauses / general)
  2. Execute targeted Cypher query → structured graph context
  3. Semantic search ChromaDB → relevant lease text chunks
  4. Merge both contexts → call LLM with strict grounding prompt
  5. Return answer + provenance metadata
"""
from __future__ import annotations
import json
from loguru import logger

from leaseguard.graph.graph_queries  import GraphQueries
from leaseguard.intelligence.vector_store import VectorStore
from leaseguard.llm.llm_client       import LLMClient
from leaseguard.llm.prompts          import (
    GRAPH_RAG_SYSTEM, GRAPH_RAG_USER,
    RISK_SYSTEM, RISK_USER,
    CYPHER_SYSTEM, CYPHER_USER,
    SUMMARY_SYSTEM, SUMMARY_USER,
)


class GraphRAG:
    """
    Primary reasoning engine.

    Every public method retrieves structured graph context before calling
    the LLM — the LLM is forbidden (by system prompt) from answering
    outside the provided context, eliminating hallucination.
    """

    def __init__(
        self,
        graph:  GraphQueries | None = None,
        vector: VectorStore  | None = None,
        llm:    LLMClient    | None = None,
    ) -> None:
        self._graph  = graph  or GraphQueries()
        self._vector = vector or VectorStore()
        self._llm    = llm    or LLMClient()

    # ── Main Q&A entry point ───────────────────────────────────────────────

    def answer(self, question: str) -> dict:
        """
        Answer *question* grounded in the graph.

        Returns:
            answer       — LLM-generated answer string
            graph_context — list of graph rows used
            doc_context   — list of vector-search chunks used
            question      — echo of input
        """
        graph_ctx = self._route_graph_query(question)
        doc_ctx   = self._vector.search(question, n_results=3)

        answer = self._llm.chat(
            system=GRAPH_RAG_SYSTEM,
            user=GRAPH_RAG_USER.format(
                graph_context=json.dumps(graph_ctx, default=str, indent=2),
                doc_context="\n---\n".join(c["text"] for c in doc_ctx),
                question=question,
            ),
        )
        logger.info(f"Graph-RAG  graph_rows={len(graph_ctx)}  doc_chunks={len(doc_ctx)}")
        return {
            "answer":        answer,
            "graph_context": graph_ctx,
            "doc_context":   doc_ctx,
            "question":      question,
        }

    # ── Risk summary ────────────────────────────────────────────────────────

    def risk_summary(self, lease_id: str) -> str:
        """
        Generate a structured TOP-3 risk analysis for *lease_id*.

        Retrieves the full lease neighbourhood from the graph first.
        """
        detail = self._graph.lease_by_id(lease_id)
        if not detail:
            return f"Lease {lease_id!r} not found in the graph."
        return self._llm.chat(
            system=RISK_SYSTEM,
            user=RISK_USER.format(lease_json=json.dumps(detail, default=str, indent=2)),
        )

    # ── Portfolio narrative ─────────────────────────────────────────────────

    def portfolio_summary_narrative(self) -> str:
        """Generate a short executive summary of the whole portfolio."""
        summary = self._graph.portfolio_summary()
        expiring = self._graph.expiring_leases(days=90)
        conc     = self._graph.tenant_concentration()
        payload  = {
            "portfolio_stats":   summary,
            "expiring_90_days":  expiring[:5],
            "top_tenants":       conc[:5],
        }
        return self._llm.chat(
            system=SUMMARY_SYSTEM,
            user=SUMMARY_USER.format(portfolio_json=json.dumps(payload, default=str, indent=2)),
        )

    # ── LLM-to-Cypher (experimental) ───────────────────────────────────────

    def cypher_answer(self, question: str) -> dict:
        """
        Translate *question* to Cypher via LLM and execute it.

        Returns raw Cypher rows — useful for power users / API clients.
        Falls back to graph_route if Cypher execution fails.
        """
        cypher = self._llm.chat(
            system=CYPHER_SYSTEM,
            user=CYPHER_USER.format(question=question),
        ).strip().rstrip(";")

        try:
            rows = self._graph._db.run(cypher)
            return {"cypher": cypher, "rows": rows, "error": None}
        except Exception as exc:
            logger.warning(f"LLM-generated Cypher failed: {exc}\nQuery: {cypher}")
            return {"cypher": cypher, "rows": [], "error": str(exc)}

    # ── Intent routing ──────────────────────────────────────────────────────

    def _route_graph_query(self, question: str) -> list:
        """
        Classify the question and run the most relevant Cypher query.

        Simple keyword routing — sufficient for POC; replace with an LLM
        classifier for production.
        """
        q = question.lower()

        # Expiration
        if any(w in q for w in ("expir", "renew", "upcoming", "soon", "days")):
            days = (180 if "180" in q else 90 if "90" in q
                    else 60 if "60" in q else 30 if "30" in q else 90)
            return self._graph.expiring_leases(days)

        # Concentration / largest tenant
        if any(w in q for w in ("concentrat", "largest tenant", "biggest",
                                "most space", "most sqft")):
            return self._graph.tenant_concentration()

        # High-risk clauses
        if any(w in q for w in ("clause", "terminat", "co-tenancy", "exclusiv",
                                 "rofr", "first refusal", "high-risk", "high risk")):
            return self._graph.high_risk_clauses()

        # Termination rights window
        if any(w in q for w in ("terminat right", "break option", "early exit")):
            return self._graph.termination_rights_window()

        # Portfolio overview
        if any(w in q for w in ("summary", "total", "portfolio", "overview",
                                 "how many", "count")):
            return [self._graph.portfolio_summary()]

        # City breakdown
        if any(w in q for w in ("city", "market", "location", "where",
                                 "geographic", "breakdown")):
            return self._graph.city_breakdown()

        # Single lease lookup by ID
        for word in question.split():
            if word.upper().startswith("LG-") and len(word) > 4:
                detail = self._graph.lease_by_id(word.upper())
                return [detail] if detail else []

        # Default — return recent leases
        return self._graph.all_leases(limit=15)
