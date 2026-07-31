"""
RiskAgent — specialised agent for portfolio-level risk analysis.

Runs independently of the main LeaseAgent; useful for scheduled batch
risk reports or webhook-triggered alerts.
"""
from __future__ import annotations
import json
from datetime import date, timedelta
from loguru import logger

from leaseguard.graph.graph_queries import GraphQueries
from leaseguard.llm.llm_client      import LLMClient
from leaseguard.llm.prompts         import RISK_SYSTEM, RISK_USER


class RiskAgent:
    """Compute and narrate lease portfolio risk signals."""

    def __init__(
        self,
        graph: GraphQueries | None = None,
        llm:   LLMClient    | None = None,
    ) -> None:
        self._graph = graph or GraphQueries()
        self._llm   = llm   or LLMClient()

    # ── Risk signals ───────────────────────────────────────────────────────

    def expiration_risk(self, days: int = 90) -> dict:
        """Leases expiring in next *days* days, flagged by urgency tier."""
        leases = self._graph.expiring_leases(days)
        today  = date.today()
        tiered: dict[str, list] = {"critical": [], "warning": [], "watch": []}
        for row in leases:
            end = date.fromisoformat(row["expiration_date"])
            d   = (end - today).days
            if d <= 30:
                tiered["critical"].append(row)
            elif d <= 60:
                tiered["warning"].append(row)
            else:
                tiered["watch"].append(row)
        return {
            "window_days": days,
            "total":       len(leases),
            "tiers":       tiered,
        }

    def concentration_risk(self, threshold_pct: float = 25.0) -> dict:
        """Tenants whose sqft share exceeds *threshold_pct* %."""
        rows   = self._graph.tenant_concentration()
        flagged = [r for r in rows if (r.get("concentration_pct") or 0) > threshold_pct]
        return {
            "threshold_pct": threshold_pct,
            "flagged":       flagged,
            "all_tenants":   rows,
        }

    def clause_risk(self) -> list[dict]:
        """All HIGH risk clauses with their lease context."""
        return self._graph.high_risk_clauses()

    def termination_window(self, months: int = 12) -> list[dict]:
        """Termination rights exercisable in the next *months* months."""
        return self._graph.termination_rights_window(months)

    # ── AI-generated risk report ────────────────────────────────────────────

    def full_risk_report(self) -> str:
        """
        Generate a comprehensive portfolio risk narrative using the LLM.

        Aggregates expiration, concentration, clause, and termination data
        into a single prompt and returns a structured risk report.
        """
        payload = {
            "expiration_90d":    self.expiration_risk(90),
            "concentration":     self.concentration_risk(),
            "high_risk_clauses": self.clause_risk()[:10],
            "termination_12m":   self.termination_window(12),
        }
        logger.info("Generating full portfolio risk report via LLM …")
        return self._llm.chat(
            system=RISK_SYSTEM,
            user=RISK_USER.format(lease_json=json.dumps(payload, default=str, indent=2)),
        )

    def score_lease(self, lease_id: str) -> dict:
        """
        Simple heuristic risk score (0–100) for one lease.

        Higher = riskier. Useful for sorting leases by risk in the dashboard.
        """
        detail = self._graph.lease_by_id(lease_id)
        if not detail:
            return {"lease_id": lease_id, "score": 0, "factors": []}

        score   = 0
        factors = []
        today   = date.today()

        # Expiry within 90 days → +40
        if detail.get("end_date"):
            days_left = (date.fromisoformat(detail["end_date"]) - today).days
            if days_left < 0:
                score += 50; factors.append("Lease already expired")
            elif days_left <= 30:
                score += 40; factors.append(f"Expires in {days_left} days (CRITICAL)")
            elif days_left <= 90:
                score += 25; factors.append(f"Expires in {days_left} days")

        # High-risk clauses → +15 each (max +30)
        clauses = detail.get("clauses") or []
        n_clauses = min(len([c for c in clauses if c]), 2)
        if n_clauses:
            score += n_clauses * 15
            factors.append(f"{n_clauses} high-risk clause(s)")

        # Termination rights → +10
        if detail.get("term_rights") and any(tr.get("ey") for tr in detail["term_rights"]):
            score += 10; factors.append("Active termination right")

        return {
            "lease_id": lease_id,
            "score":    min(score, 100),
            "factors":  factors,
            "detail":   detail,
        }
