"""
Create Neo4j constraints and indexes for the LeaseGuard graph schema.

Run once before first use:
    python -m leaseguard.graph.setup_schema
"""
from __future__ import annotations
from loguru import logger
from leaseguard.graph.neo4j_client import Neo4jClient

# Constraint DDL — idempotent (IF NOT EXISTS)
CONSTRAINTS = [
    "CREATE CONSTRAINT property_addr IF NOT EXISTS "
    "FOR (p:Property) REQUIRE p.address IS UNIQUE",

    "CREATE CONSTRAINT lease_id IF NOT EXISTS "
    "FOR (l:Lease) REQUIRE l.lease_id IS UNIQUE",

    "CREATE CONSTRAINT tenant_name IF NOT EXISTS "
    "FOR (t:Tenant) REQUIRE t.tenant_name IS UNIQUE",
]

# Index DDL
INDEXES = [
    "CREATE INDEX lease_end_idx   IF NOT EXISTS FOR (l:Lease) ON (l.end_date)",
    "CREATE INDEX lease_rent_idx  IF NOT EXISTS FOR (l:Lease) ON (l.base_rent_psf)",
    "CREATE INDEX lease_sqft_idx  IF NOT EXISTS FOR (l:Lease) ON (l.rentable_sqft)",
    "CREATE INDEX tenant_ind_idx  IF NOT EXISTS FOR (t:Tenant) ON (t.industry)",
    "CREATE INDEX prop_city_idx   IF NOT EXISTS FOR (p:Property) ON (p.city)",
    "CREATE INDEX clause_risk_idx IF NOT EXISTS FOR (c:Clause) ON (c.risk_level)",
]


def setup(client: Neo4jClient | None = None) -> None:
    """Apply all constraints and indexes to the connected Neo4j instance."""
    db = client or Neo4jClient()
    if not db.ping():
        raise RuntimeError(
            "Cannot connect to Neo4j.\n"
            "  • Is Neo4j running?  neo4j start\n"
            f"  • Check NEO4J_URI={db._uri}"
        )

    print("\n📐  Creating schema …\n")
    for ddl in CONSTRAINTS + INDEXES:
        db.run(ddl)
        short = ddl[:70] + ("…" if len(ddl) > 70 else "")
        print(f"  ✅  {short}")

    counts = db.node_counts()
    print(f"\n📊  Current graph:  {counts or 'empty'}\n")
    print("🎉  Schema ready!\n")


if __name__ == "__main__":
    setup()
