"""Pre-built Cypher queries for all LeaseGuard dashboard and RAG views."""
from __future__ import annotations
from leaseguard.graph.neo4j_client import Neo4jClient


class GraphQueries:
    """Repository of business-critical Cypher queries."""

    def __init__(self, client: Neo4jClient | None = None) -> None:
        self._db = client or Neo4jClient()

    # ── Lease queries ──────────────────────────────────────────────────────

    def all_leases(self, limit: int = 500) -> list[dict]:
        """Return every lease with its property and tenant details."""
        return self._db.run(
            """
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease)-[:SIGNED_BY]->(t:Tenant)
            RETURN
                l.lease_id        AS lease_id,
                p.address         AS property,
                p.city            AS city,
                p.state           AS state,
                t.tenant_name     AS tenant,
                t.industry        AS industry,
                toString(l.start_date)  AS start_date,
                toString(l.end_date)    AS end_date,
                l.base_rent_psf   AS rent_psf,
                l.rentable_sqft   AS sqft,
                l.annual_rent     AS annual_rent,
                l.lease_type      AS lease_type,
                l.escalation_pct  AS escalation_pct,
                l.source_file     AS source_file
            ORDER BY l.end_date ASC
            LIMIT $limit
            """,
            limit=limit,
        )

    def expiring_leases(self, days: int = 90) -> list[dict]:
        """Leases whose end_date falls within the next *days* calendar days."""
        return self._db.run(
            f"""
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease)-[:SIGNED_BY]->(t:Tenant)
            WHERE l.end_date >= date()
              AND l.end_date <= date() + duration('P{days}D')
            RETURN
                l.lease_id       AS lease_id,
                p.address        AS property,
                p.city           AS city,
                t.tenant_name    AS tenant,
                toString(l.end_date)   AS expiration_date,
                l.rentable_sqft  AS sqft,
                l.base_rent_psf  AS rent_psf,
                l.annual_rent    AS annual_rent,
                l.lease_type     AS lease_type,
                l.source_file    AS source_file
            ORDER BY l.end_date ASC
            """,
        )

    def lease_by_id(self, lease_id: str) -> dict | None:
        """Full lease detail for a single lease_id."""
        rows = self._db.run(
            """
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease {lease_id: $lid})-[:SIGNED_BY]->(t:Tenant)
            OPTIONAL MATCH (l)-[:HAS_CLAUSE]->(c:Clause)
            OPTIONAL MATCH (l)-[:HAS_OPTION]->(ro:RenewalOption)
            OPTIONAL MATCH (l)-[:HAS_TERM_RIGHT]->(tr:TerminationRight)
            RETURN
                l.lease_id       AS lease_id,
                p.address        AS property,
                p.city           AS city,
                t.tenant_name    AS tenant,
                t.industry       AS industry,
                toString(l.start_date) AS start_date,
                toString(l.end_date)   AS end_date,
                l.base_rent_psf  AS rent_psf,
                l.rentable_sqft  AS sqft,
                l.lease_type     AS lease_type,
                l.escalation_pct AS escalation_pct,
                collect(DISTINCT c.text)        AS clauses,
                collect(DISTINCT ro.term_years) AS renewal_terms,
                collect(DISTINCT {
                    ey: tr.effective_after_year,
                    nm: tr.notice_months
                })                              AS term_rights
            LIMIT 1
            """,
            lid=lease_id,
        )
        return rows[0] if rows else None

    # ── Risk queries ───────────────────────────────────────────────────────

    def high_risk_clauses(self) -> list[dict]:
        """All clauses flagged risk_level=HIGH with their parent lease/property."""
        return self._db.run(
            """
            MATCH (l:Lease)-[:HAS_CLAUSE]->(c:Clause {risk_level: 'HIGH'})
            MATCH (p:Property)-[:HAS_LEASE]->(l)
            MATCH (l)-[:SIGNED_BY]->(t:Tenant)
            RETURN
                l.lease_id    AS lease_id,
                p.address     AS property,
                t.tenant_name AS tenant,
                c.text        AS clause_text,
                c.risk_level  AS risk_level
            ORDER BY l.lease_id
            """
        )

    def tenant_concentration(self) -> list[dict]:
        """Aggregate sqft per tenant and compute portfolio share (%)."""
        rows = self._db.run(
            """
            MATCH (t:Tenant)<-[:SIGNED_BY]-(l:Lease)
            WITH t.tenant_name AS tenant,
                 count(l)         AS lease_count,
                 sum(l.rentable_sqft) AS total_sqft
            WITH collect({tenant:tenant, lease_count:lease_count, total_sqft:total_sqft}) AS all_tenants,
                 sum(total_sqft) AS portfolio_sqft
            UNWIND all_tenants AS row
            RETURN
                row.tenant       AS tenant,
                row.lease_count  AS lease_count,
                row.total_sqft   AS total_sqft,
                portfolio_sqft   AS portfolio_total_sqft,
                CASE WHEN portfolio_sqft > 0
                     THEN round(toFloat(row.total_sqft) / portfolio_sqft * 1000) / 10.0
                     ELSE 0.0
                END              AS concentration_pct
            ORDER BY total_sqft DESC
            """
        )
        return rows

    def termination_rights_window(self, months_ahead: int = 12) -> list[dict]:
        """Termination rights that could be exercised in the next N months."""
        return self._db.run(
            f"""
            MATCH (l:Lease)-[:HAS_TERM_RIGHT]->(tr:TerminationRight)
            MATCH (p:Property)-[:HAS_LEASE]->(l)
            MATCH (l)-[:SIGNED_BY]->(t:Tenant)
            WHERE l.start_date + duration({{years: tr.effective_after_year}})
                  <= date() + duration('P{months_ahead}M')
            RETURN
                l.lease_id               AS lease_id,
                p.address                AS property,
                t.tenant_name            AS tenant,
                tr.effective_after_year  AS effective_after_year,
                tr.notice_months         AS notice_months,
                toString(l.end_date)     AS lease_expiry
            ORDER BY tr.effective_after_year
            """
        )

    # ── Portfolio analytics ────────────────────────────────────────────────

    def portfolio_summary(self) -> dict:
        """High-level portfolio statistics for the sidebar."""
        row = {}
        for q, key in [
            ("MATCH (l:Lease) RETURN count(l) AS n", "lease_count"),
            ("MATCH (l:Lease) RETURN sum(l.rentable_sqft) AS n", "total_sqft"),
            ("MATCH (l:Lease) RETURN avg(l.base_rent_psf) AS n", "avg_rent_psf"),
            ("MATCH (t:Tenant) RETURN count(t) AS n", "tenant_count"),
            ("MATCH (p:Property) RETURN count(p) AS n", "property_count"),
            ("MATCH (c:Clause {risk_level:'HIGH'}) RETURN count(c) AS n", "high_risk_clauses"),
        ]:
            rows = self._db.run(q)
            row[key] = rows[0].get("n", 0) if rows else 0
        if row.get("avg_rent_psf"):
            row["avg_rent_psf"] = round(float(row["avg_rent_psf"]), 2)
        return row

    def city_breakdown(self) -> list[dict]:
        """Lease count and total sqft by city — for map/heat-map views."""
        return self._db.run(
            """
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease)
            RETURN
                p.city           AS city,
                p.state          AS state,
                count(l)         AS lease_count,
                sum(l.rentable_sqft) AS total_sqft,
                avg(l.base_rent_psf) AS avg_rent_psf
            ORDER BY total_sqft DESC
            """
        )

    def graph_for_visualisation(self, limit: int = 60) -> dict:
        """Return nodes + edges suitable for a pyvis / D3 force graph."""
        leases = self._db.run(
            """
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease)-[:SIGNED_BY]->(t:Tenant)
            RETURN p.address AS prop, l.lease_id AS lid, t.tenant_name AS tenant
            LIMIT $limit
            """,
            limit=limit,
        )
        nodes: list[dict] = []
        edges: list[dict] = []
        seen: set[str] = set()

        def add_node(nid, label, ntype):
            if nid not in seen:
                nodes.append({"id": nid, "label": label[:25], "type": ntype})
                seen.add(nid)

        for row in leases:
            add_node(row["prop"],   row["prop"],   "Property")
            add_node(row["tenant"], row["tenant"], "Tenant")
            add_node(row["lid"],    row["lid"],    "Lease")
            edges.append({"from": row["prop"],   "to": row["lid"],    "label": "HAS_LEASE"})
            edges.append({"from": row["lid"],    "to": row["tenant"], "label": "SIGNED_BY"})

        # Add clauses
        clauses = self._db.run(
            "MATCH (l:Lease)-[:HAS_CLAUSE]->(c:Clause) "
            "RETURN l.lease_id AS lid, id(c) AS cid, c.text AS txt LIMIT 30"
        )
        for row in clauses:
            cnode = f"clause_{row['cid']}"
            add_node(cnode, row["txt"][:20] + "…", "Clause")
            edges.append({"from": row["lid"], "to": cnode, "label": "HAS_CLAUSE"})

        # Renewal options
        options = self._db.run(
            """
            MATCH (l:Lease)-[:HAS_OPTION]->(r:RenewalOption)
            RETURN l.lease_id AS lid, id(r) AS rid, r.term_years AS term
            LIMIT 40
            """
        )
        for row in options:
            onode = f"option_{row['rid']}"
            term = row.get("term") or "?"
            add_node(onode, f"{term}yr option", "RenewalOption")
            edges.append({"from": row["lid"], "to": onode, "label": "HAS_OPTION"})

        # Termination rights
        terms = self._db.run(
            """
            MATCH (l:Lease)-[:HAS_TERM_RIGHT]->(t:TerminationRight)
            RETURN l.lease_id AS lid, id(t) AS tid
            LIMIT 40
            """
        )
        for row in terms:
            tnode = f"term_{row['tid']}"
            add_node(tnode, "Termination Right", "TerminationRight")
            edges.append({"from": row["lid"], "to": tnode, "label": "HAS_TERM_RIGHT"})

        return {"nodes": nodes, "edges": edges}

    def relationships_table(self, limit: int = 500) -> list[dict]:
        """
        Full lease-centric export of knowledge-graph features.

        One row per Property → HAS_LEASE → Lease → SIGNED_BY → Tenant path,
        with Property / Tenant / Lease attributes plus Option, TerminationRight,
        and Clause details attached to that lease.
        """
        rows = self._db.run(
            """
            MATCH (p:Property)-[:HAS_LEASE]->(l:Lease)-[:SIGNED_BY]->(t:Tenant)
            OPTIONAL MATCH (l)-[:HAS_CLAUSE]->(c:Clause)
            OPTIONAL MATCH (l)-[:HAS_OPTION]->(ro:RenewalOption)
            OPTIONAL MATCH (l)-[:HAS_TERM_RIGHT]->(tr:TerminationRight)
            WITH p, l, t,
                 collect(DISTINCT CASE WHEN c IS NULL THEN null ELSE {
                   text: coalesce(c.text, ''),
                   risk_level: coalesce(c.risk_level, ''),
                   clause_type: coalesce(c.clause_type, '')
                 } END) AS clause_nodes,
                 collect(DISTINCT CASE WHEN ro IS NULL THEN null ELSE {
                   term_years: ro.term_years,
                   notice_months: ro.notice_months,
                   rent_basis: coalesce(ro.rent_basis, '')
                 } END) AS option_nodes,
                 collect(DISTINCT CASE WHEN tr IS NULL THEN null ELSE {
                   effective_after_year: tr.effective_after_year,
                   notice_months: tr.notice_months,
                   penalty_months: tr.penalty_months
                 } END) AS term_nodes
            WITH p, l, t,
                 [x IN clause_nodes WHERE x IS NOT NULL] AS clauses,
                 [x IN option_nodes WHERE x IS NOT NULL] AS options,
                 [x IN term_nodes WHERE x IS NOT NULL] AS term_rights
            OPTIONAL MATCH (p)-[:HAS_LEASE]->(plx:Lease)
            WITH p, l, t, clauses, options, term_rights,
                 count(DISTINCT plx) AS property_lease_count
            OPTIONAL MATCH (p)-[:HAS_LEASE]->(:Lease)-[:SIGNED_BY]->(ptx:Tenant)
            WITH p, l, t, clauses, options, term_rights, property_lease_count,
                 count(DISTINCT ptx) AS property_tenant_count
            OPTIONAL MATCH (t)<-[:SIGNED_BY]-(tlx:Lease)
            WITH p, l, t, clauses, options, term_rights, property_lease_count,
                 property_tenant_count, count(DISTINCT tlx) AS tenant_lease_count
            RETURN
                l.lease_id AS lease_id,
                toString(l.start_date) AS start_date,
                toString(l.end_date) AS end_date,
                l.base_rent_psf AS rent_psf,
                l.rentable_sqft AS sqft,
                l.annual_rent AS annual_rent,
                l.lease_type AS lease_type,
                l.escalation_pct AS escalation_pct,
                coalesce(l.source_file, '') AS source_file,
                p.address AS property,
                coalesce(p.city, '') AS city,
                coalesce(p.state, '') AS state,
                p.sqft AS property_sqft,
                t.tenant_name AS tenant,
                coalesce(t.industry, '') AS industry,
                tenant_lease_count,
                property_lease_count,
                property_tenant_count,
                clauses,
                options,
                term_rights
            ORDER BY l.lease_id
            LIMIT $limit
            """,
            limit=limit,
        )

        out: list[dict] = []
        for i, r in enumerate(rows):
            prop_leases = int(r.get("property_lease_count") or 0)
            tenant_leases = int(r.get("tenant_lease_count") or 0)
            prop_tenants = int(r.get("property_tenant_count") or 0)

            property_note = ""
            if prop_tenants >= 2:
                property_note = f"{prop_tenants} tenants"
            elif prop_leases >= 2:
                property_note = "same building"
            tenant_note = f"{tenant_leases} leases total" if tenant_leases >= 2 else ""

            options = [o for o in (r.get("options") or []) if o]
            term_rights = [t for t in (r.get("term_rights") or []) if t]
            clauses_raw = [c for c in (r.get("clauses") or []) if c]

            option_labels = []
            option_details = []
            for o in options:
                years = o.get("term_years")
                notice = o.get("notice_months")
                basis = o.get("rent_basis") or ""
                label = f"{years or '?'}yr Option"
                option_labels.append(label)
                option_details.append(
                    f"{label} (notice={notice or '?'}mo, basis={basis or 'n/a'})"
                )

            term_labels = ["Termination Right"] * len(term_rights)
            term_details = []
            for tr in term_rights:
                term_details.append(
                    "Termination Right "
                    f"(after_year={tr.get('effective_after_year') or '?'}, "
                    f"notice={tr.get('notice_months') or '?'}mo, "
                    f"penalty={tr.get('penalty_months') or '?'}mo)"
                )

            special = []
            clause_details = []
            seen: set[str] = set()
            for c in clauses_raw:
                text = (c.get("text") or "").strip()
                ctype = (c.get("clause_type") or "").strip()
                risk = (c.get("risk_level") or "").strip()
                low = f"{ctype} {text}".lower()
                if "exclusiv" in low:
                    label = "Exclusivity"
                elif "co-tenancy" in low or "cotenancy" in low:
                    label = "Co-Tenancy"
                elif "rofr" in low or "first refusal" in low:
                    label = "ROFR"
                elif "terminat" in low:
                    label = "Termination Right"
                elif ctype:
                    label = ctype
                else:
                    label = text.split(".")[0][:40] if text else "Clause"
                if label and label not in seen:
                    seen.add(label)
                    special.append(label)
                if text or ctype:
                    clause_details.append(
                        f"{label}"
                        + (f" [{risk}]" if risk else "")
                        + (f": {text}" if text else "")
                    )

            for lbl in option_labels + term_labels:
                if lbl not in seen:
                    seen.add(lbl)
                    special.append(lbl)

            edges = ["HAS_LEASE", "SIGNED_BY"]
            if options:
                edges.append("HAS_OPTION")
            if term_rights:
                edges.append("HAS_TERM_RIGHT")
            if clauses_raw:
                edges.append("HAS_CLAUSE")

            out.append(
                {
                    "id": i + 1,
                    "lease_id": r.get("lease_id") or "",
                    "start_date": r.get("start_date") or "",
                    "end_date": r.get("end_date") or "",
                    "rent_psf": r.get("rent_psf") if r.get("rent_psf") is not None else "",
                    "sqft": r.get("sqft") if r.get("sqft") is not None else "",
                    "annual_rent": r.get("annual_rent") if r.get("annual_rent") is not None else "",
                    "lease_type": r.get("lease_type") or "",
                    "escalation_pct": r.get("escalation_pct") if r.get("escalation_pct") is not None else "",
                    "source_file": r.get("source_file") or "",
                    "property": r.get("property") or "",
                    "city": r.get("city") or "",
                    "state": r.get("state") or "",
                    "property_sqft": r.get("property_sqft") if r.get("property_sqft") is not None else "",
                    "property_note": property_note,
                    "tenant": r.get("tenant") or "",
                    "industry": r.get("industry") or "",
                    "tenant_note": tenant_note,
                    "relationship": "Property -> HAS_LEASE -> Lease -> SIGNED_BY -> Tenant",
                    "graph_edges": edges,
                    "special_clauses": special,
                    "clause_details": clause_details,
                    "renewal_options": option_details,
                    "termination_rights": term_details,
                }
            )
        return out
