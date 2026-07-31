"""Integration tests — require a running Neo4j instance.

Set SKIP_NEO4J_TESTS=false to enable these tests:
    SKIP_NEO4J_TESTS=false pytest tests/test_graph.py -v
"""
from __future__ import annotations
import pytest

from leaseguard.graph.neo4j_client  import Neo4jClient
from leaseguard.graph.graph_writer  import GraphWriter
from leaseguard.graph.graph_queries import GraphQueries


@pytest.fixture(scope="module")
def db(neo4j_skip):
    client = Neo4jClient()
    if not client.ping():
        pytest.skip("Neo4j not reachable")
    yield client
    client.close()


@pytest.fixture(scope="module")
def writer(db):
    return GraphWriter(neo4j=db)


@pytest.fixture(scope="module")
def queries(db):
    return GraphQueries(client=db)


class TestNeo4jClient:
    def test_ping(self, db):
        assert db.ping() is True

    def test_run_returns_list(self, db):
        result = db.run("RETURN 1 AS n, 'hello' AS s")
        assert isinstance(result, list)
        assert result[0]["n"] == 1
        assert result[0]["s"] == "hello"

    def test_node_counts_returns_dict(self, db):
        counts = db.node_counts()
        assert isinstance(counts, dict)


class TestGraphWriter:
    LEASE_DATA = {
        "tenant_name":       "Pytest Test Corp",
        "property_address":  "999 Test Avenue, Austin, TX 78702",
        "city":              "Austin",
        "state":             "TX",
        "lease_start_date":  "2024-01-01",
        "lease_end_date":    "2029-12-31",
        "base_rent_psf":     42.5,
        "rentable_sqft":     5000,
        "annual_rent":       212500.0,
        "lease_type":        "NNN",
        "escalation_pct":    3.0,
        "tenant_industry":   "Technology",
        "risk_clauses":      ["Termination right after Year 3"],
        "renewal_options":   [{"term_years": 5, "notice_months": 12, "rent_basis": "FMR"}],
        "termination_rights": [{"effective_after_year": 3, "notice_months": 12}],
    }

    @pytest.fixture(autouse=True)
    def cleanup(self, db):
        # Run test then clean up all test data
        yield
        db.run(
            "MATCH (t:Tenant {tenant_name:'Pytest Test Corp'}) "
            "OPTIONAL MATCH (t)<-[:SIGNED_BY]-(l:Lease) "
            "OPTIONAL MATCH (l)-[:HAS_CLAUSE]->(c:Clause) "
            "OPTIONAL MATCH (l)-[:HAS_OPTION]->(ro:RenewalOption) "
            "OPTIONAL MATCH (l)-[:HAS_TERM_RIGHT]->(tr:TerminationRight) "
            "OPTIONAL MATCH (p:Property)-[:HAS_LEASE]->(l) "
            "DETACH DELETE t, l, c, ro, tr, p"
        )

    def test_write_returns_lease_id(self, writer):
        lid = writer.write_lease(self.LEASE_DATA, source_file="test_lease.pdf")
        assert lid.startswith("LG-"), f"Expected LG-… got {lid!r}"
        assert len(lid) > 5

    def test_lease_node_exists_after_write(self, writer, db):
        lid = writer.write_lease(self.LEASE_DATA)
        rows = db.run("MATCH (l:Lease {lease_id:$lid}) RETURN l.lease_id AS id", lid=lid)
        assert rows and rows[0]["id"] == lid

    def test_property_node_created(self, writer, db):
        writer.write_lease(self.LEASE_DATA)
        rows = db.run(
            "MATCH (p:Property {address:$addr}) RETURN p.city AS city",
            addr="999 TEST AVENUE AUSTIN TX 78702",
        )
        # canonical_address normalises to upper case
        assert rows and rows[0]["city"] == "Austin"

    def test_has_lease_relationship(self, writer, db):
        lid = writer.write_lease(self.LEASE_DATA)
        rows = db.run(
            "MATCH (p:Property)-[:HAS_LEASE]->(l:Lease {lease_id:$lid}) RETURN l.lease_id",
            lid=lid,
        )
        assert rows

    def test_signed_by_relationship(self, writer, db):
        lid = writer.write_lease(self.LEASE_DATA)
        rows = db.run(
            "MATCH (l:Lease {lease_id:$lid})-[:SIGNED_BY]->(t:Tenant) RETURN t.tenant_name",
            lid=lid,
        )
        assert rows and "Pytest Test Corp" in rows[0]["t.tenant_name"]

    def test_clause_node_created(self, writer, db):
        lid = writer.write_lease(self.LEASE_DATA)
        rows = db.run(
            "MATCH (l:Lease {lease_id:$lid})-[:HAS_CLAUSE]->(c:Clause) RETURN c.risk_level",
            lid=lid,
        )
        assert rows and rows[0]["c.risk_level"] == "HIGH"

    def test_renewal_option_node(self, writer, db):
        lid = writer.write_lease(self.LEASE_DATA)
        rows = db.run(
            "MATCH (l:Lease {lease_id:$lid})-[:HAS_OPTION]->(r:RenewalOption) RETURN r.term_years",
            lid=lid,
        )
        assert rows and rows[0]["r.term_years"] == 5

    def test_merge_prevents_duplicate_tenant(self, writer, db):
        writer.write_lease(self.LEASE_DATA)
        writer.write_lease(self.LEASE_DATA)   # second write
        rows = db.run(
            "MATCH (t:Tenant {tenant_name:'Pytest Test Corp'}) RETURN count(t) AS n"
        )
        assert rows[0]["n"] == 1, "Tenant should not be duplicated"


class TestGraphQueries:
    def test_portfolio_summary_returns_dict(self, queries):
        summary = queries.portfolio_summary()
        assert isinstance(summary, dict)
        assert "lease_count" in summary

    def test_all_leases_returns_list(self, queries):
        result = queries.all_leases(limit=10)
        assert isinstance(result, list)

    def test_expiring_leases_returns_list(self, queries):
        result = queries.expiring_leases(days=365)
        assert isinstance(result, list)

    def test_high_risk_clauses_returns_list(self, queries):
        result = queries.high_risk_clauses()
        assert isinstance(result, list)

    def test_tenant_concentration_returns_list(self, queries):
        result = queries.tenant_concentration()
        assert isinstance(result, list)

    def test_city_breakdown_returns_list(self, queries):
        result = queries.city_breakdown()
        assert isinstance(result, list)

    def test_graph_for_visualisation(self, queries):
        result = queries.graph_for_visualisation(limit=10)
        assert "nodes" in result
        assert "edges" in result
        assert isinstance(result["nodes"], list)
        assert isinstance(result["edges"], list)
