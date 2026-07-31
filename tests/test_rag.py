"""Unit tests for VectorStore and GraphRAG routing logic."""
from __future__ import annotations
import os
import shutil
import pytest

from leaseguard.intelligence.embedder     import embed, embed_one


# ── Embedder ──────────────────────────────────────────────────────────────────

class TestEmbedder:
    def test_embed_returns_array(self):
        arr = embed(["Hello world", "Lease agreement"])
        assert arr.shape == (2, 384)
        assert arr.dtype.kind == "f"   # float

    def test_embed_one_returns_1d(self):
        v = embed_one("commercial lease")
        assert v.shape == (384,)

    def test_embed_empty_returns_empty(self):
        arr = embed([])
        assert arr.shape[0] == 0

    def test_embedding_differs_per_text(self):
        a = embed_one("property lease agreement")
        b = embed_one("completely different text about cooking")
        # Cosine similarity should be less than 0.95
        import numpy as np
        cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        assert cos < 0.95, f"Expected dissimilar texts, got cosine={cos:.3f}"


# ── VectorStore ───────────────────────────────────────────────────────────────

class TestVectorStore:
    TMP_PATH = "/tmp/leaseguard_test_chroma"

    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        if os.path.exists(self.TMP_PATH):
            shutil.rmtree(self.TMP_PATH, ignore_errors=True)

    def _store(self):
        from leaseguard.intelligence.vector_store import VectorStore
        return VectorStore(db_path=self.TMP_PATH, collection="test_col")

    def test_count_empty(self):
        store = self._store()
        assert store.count() == 0

    def test_add_and_count(self):
        store = self._store()
        store.add_chunks(["Tenant: Acme Corp", "Lease expires December 2028"], "LG-TEST1")
        assert store.count() == 2

    def test_search_returns_results(self):
        store = self._store()
        store.add_chunks(
            ["The lease expires on December 31, 2028",
             "Base rent is $35.00 per square foot",
             "Renewal option: 5 years"],
            "LG-TEST2",
        )
        results = store.search("when does the lease expire", n_results=2)
        assert len(results) >= 1
        assert "text" in results[0]
        assert "score" in results[0]
        assert results[0]["score"] > 0

    def test_search_most_relevant_first(self):
        store = self._store()
        store.add_chunks(
            ["Tenant: Vantage Analytics",
             "The lease expires December 31 2028",
             "Monthly rent is $29,000"],
            "LG-TEST3",
        )
        results = store.search("expiration date of lease", n_results=3)
        top = results[0]["text"].lower()
        assert "expir" in top or "2028" in top

    def test_re_ingest_no_duplicates(self):
        store = self._store()
        store.add_chunks(["Chunk one", "Chunk two"], "LG-DUP")
        store.add_chunks(["Chunk one", "Chunk two"], "LG-DUP")  # re-ingest
        assert store.count() == 2  # should not double


# ── GraphRAG intent routing ───────────────────────────────────────────────────

class TestGraphRAGRouting:
    """
    Test the _route_graph_query classification without hitting Neo4j.
    Uses a mock GraphQueries object.
    """

    class MockQueries:
        def __init__(self):
            self.called = None
        def expiring_leases(self, days):    self.called = ("expiring", days);    return []
        def tenant_concentration(self):     self.called = ("concentration",);    return []
        def high_risk_clauses(self):        self.called = ("clauses",);          return []
        def termination_rights_window(self, m=12): self.called = ("termination",); return []
        def portfolio_summary(self):        self.called = ("summary",);          return {}
        def city_breakdown(self):           self.called = ("city",);             return []
        def all_leases(self, limit=15):     self.called = ("all",);              return []
        def lease_by_id(self, lid):         self.called = ("single", lid);       return None

    def _rag(self):
        from leaseguard.intelligence.graph_rag import GraphRAG
        from unittest.mock import MagicMock
        mq = self.MockQueries()
        vs = MagicMock()
        vs.search.return_value = []
        llm = MagicMock()
        llm.chat.return_value = "Mocked answer"
        return GraphRAG(graph=mq, vector=vs, llm=llm), mq

    def test_routes_expiry_question(self):
        rag, mq = self._rag()
        rag._route_graph_query("Which leases expire in the next 90 days?")
        assert mq.called[0] == "expiring"
        assert mq.called[1] == 90

    def test_routes_concentration_question(self):
        rag, mq = self._rag()
        rag._route_graph_query("Which tenant has the highest concentration risk?")
        assert mq.called[0] == "concentration"

    def test_routes_clause_question(self):
        rag, mq = self._rag()
        rag._route_graph_query("Are there any high-risk co-tenancy clauses?")
        assert mq.called[0] == "clauses"

    def test_routes_summary_question(self):
        rag, mq = self._rag()
        rag._route_graph_query("Give me a portfolio summary")
        assert mq.called[0] == "summary"

    def test_routes_single_lease_by_id(self):
        rag, mq = self._rag()
        rag._route_graph_query("Tell me about lease LG-A3F9B2")
        assert mq.called[0] == "single"
        assert "LG-A3F9B2" in mq.called[1]

    def test_routes_default_to_all(self):
        rag, mq = self._rag()
        rag._route_graph_query("What is the meaning of life?")
        assert mq.called[0] == "all"
