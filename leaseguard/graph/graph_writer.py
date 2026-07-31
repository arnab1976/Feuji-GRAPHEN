"""Write extracted lease data to Neo4j — MERGE semantics prevent duplicates."""
from __future__ import annotations
import uuid
from typing import Any

from loguru import logger

from leaseguard.graph.neo4j_client import Neo4jClient
from leaseguard.ingestion.entity_resolver import EntityResolver


class GraphWriter:
    """
    Translate a structured lease dict into Neo4j nodes and relationships.

    Node types created:
        Property, Tenant, Lease, Clause, RenewalOption, TerminationRight

    Relationship types created:
        (Property)-[:HAS_LEASE]->(Lease)
        (Lease)-[:SIGNED_BY]->(Tenant)
        (Lease)-[:HAS_CLAUSE]->(Clause)
        (Lease)-[:HAS_OPTION]->(RenewalOption)
        (Lease)-[:HAS_TERM_RIGHT]->(TerminationRight)
    """

    def __init__(
        self,
        neo4j:    Neo4jClient   | None = None,
        resolver: EntityResolver | None = None,
    ) -> None:
        self._db       = neo4j    or Neo4jClient()
        self._resolver = resolver or EntityResolver()

    # ── Main entry point ───────────────────────────────────────────────────

    def write_lease(self, data: dict[str, Any], source_file: str = "") -> str:
        """
        Write a fully extracted lease dict to the graph.

        Returns the generated lease_id (e.g. 'LG-A3F9B2').
        """
        lease_id = self._new_id()
        address  = self._resolver.canonical_address(data.get("property_address"))
        tenant   = self._resolver.canonical_tenant(data.get("tenant_name"))
        start    = self._safe_date(data.get("lease_start_date"), "2000-01-01")
        end      = self._safe_date(data.get("lease_end_date"),   "2099-12-31")
        rent     = self._safe_float(data.get("base_rent_psf"))
        sqft     = self._safe_int(data.get("rentable_sqft"))
        ltype    = data.get("lease_type") or "Unknown"
        industry = data.get("tenant_industry") or ""
        city     = data.get("city")  or ""
        state    = data.get("state") or ""
        escal    = self._safe_float(data.get("escalation_pct"))
        ann_rent = self._safe_float(data.get("annual_rent"))

        # ── Core nodes + relationships ──────────────────────────────────────
        self._db.run_write(
            """
            MERGE (p:Property {address: $address})
              ON CREATE SET p.city = $city, p.state = $state, p.sqft = $sqft,
                            p.created_at = datetime()
              ON MATCH  SET p.last_seen  = datetime()
            MERGE (t:Tenant {tenant_name: $tenant})
              ON CREATE SET t.industry = $industry, t.created_at = datetime()
            CREATE (l:Lease {
                lease_id:      $lid,
                start_date:    date($start),
                end_date:      date($end),
                base_rent_psf: $rent,
                rentable_sqft: $sqft,
                annual_rent:   $ann_rent,
                lease_type:    $ltype,
                escalation_pct: $escal,
                source_file:   $src,
                ingested_at:   datetime()
            })
            MERGE (p)-[:HAS_LEASE]->(l)
            MERGE (l)-[:SIGNED_BY]->(t)
            """,
            address=address, city=city, state=state, sqft=sqft,
            tenant=tenant, industry=industry,
            lid=lease_id, start=start, end=end, rent=rent,
            ann_rent=ann_rent, ltype=ltype, escal=escal, src=source_file,
        )

        # ── Renewal options ─────────────────────────────────────────────────
        for opt in (data.get("renewal_options") or []):
            self._db.run_write(
                """
                MATCH (l:Lease {lease_id: $lid})
                CREATE (r:RenewalOption {
                    term_years:    $ty,
                    notice_months: $nm,
                    rent_basis:    $rb
                })
                CREATE (l)-[:HAS_OPTION]->(r)
                """,
                lid=lease_id,
                ty=self._safe_int(opt.get("term_years")),
                nm=self._safe_int(opt.get("notice_months")),
                rb=opt.get("rent_basis", "FMR"),
            )

        # ── Termination rights ──────────────────────────────────────────────
        for tr in (data.get("termination_rights") or []):
            self._db.run_write(
                """
                MATCH (l:Lease {lease_id: $lid})
                CREATE (t:TerminationRight {
                    effective_after_year: $ey,
                    notice_months:        $nm,
                    penalty_months:       $pm
                })
                CREATE (l)-[:HAS_TERM_RIGHT]->(t)
                """,
                lid=lease_id,
                ey=self._safe_int(tr.get("effective_after_year")),
                nm=self._safe_int(tr.get("notice_months")),
                pm=self._safe_int(tr.get("penalty_months")),
            )

        # ── Risk clauses ────────────────────────────────────────────────────
        for clause_text in (data.get("risk_clauses") or []):
            if not clause_text:
                continue
            self._db.run_write(
                """
                MATCH (l:Lease {lease_id: $lid})
                CREATE (c:Clause {text: $text, risk_level: 'HIGH', flagged_at: datetime()})
                CREATE (l)-[:HAS_CLAUSE]->(c)
                """,
                lid=lease_id, text=str(clause_text)[:1000],
            )

        logger.info(
            f"Graph write  lease_id={lease_id}  tenant={tenant}  addr={address[:40]}"
        )
        return lease_id

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _new_id() -> str:
        return "LG-" + uuid.uuid4().hex[:6].upper()

    @staticmethod
    def _safe_float(v: Any) -> float:
        try:
            return float(str(v).replace(",", "").replace("$", ""))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _safe_int(v: Any) -> int:
        try:
            return int(float(str(v).replace(",", "")))
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _safe_date(v: Any, default: str) -> str:
        if not v:
            return default
        s = str(v).strip()
        # Accept YYYY-MM-DD only
        if len(s) == 10 and s[4] == "-" and s[7] == "-":
            return s
        return default
