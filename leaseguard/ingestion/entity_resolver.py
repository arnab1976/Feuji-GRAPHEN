"""Cross-document entity deduplication using fuzzy string matching."""
from __future__ import annotations
import re
from difflib import SequenceMatcher

from leaseguard.config import ENTITY_MATCH_THRESHOLD


class EntityResolver:
    """
    Canonicalise property addresses and tenant names so the same real-world
    entity receives a single graph node regardless of how it is spelled across
    different lease documents.

    Uses SequenceMatcher (stdlib) — no external API needed.
    """

    def __init__(self, threshold: float = ENTITY_MATCH_THRESHOLD) -> None:
        self.threshold = threshold
        self._prop_cache: dict[str, str] = {}   # normalised → canonical
        self._tenant_cache: dict[str, str] = {}

    # ── Property address ────────────────────────────────────────────────────

    def canonical_address(self, raw: str | None) -> str:
        if not raw or not raw.strip():
            return "Unknown Property"
        norm = self._norm_address(raw)
        for cached, canonical in self._prop_cache.items():
            if SequenceMatcher(None, norm, cached).ratio() >= self.threshold:
                return canonical
        self._prop_cache[norm] = norm
        return norm

    # ── Tenant / company name ───────────────────────────────────────────────

    def canonical_tenant(self, raw: str | None) -> str:
        if not raw or not raw.strip():
            return "Unknown Tenant"
        norm = self._norm_tenant(raw)
        key = norm.upper()
        for cached, canonical in self._tenant_cache.items():
            if SequenceMatcher(None, key, cached).ratio() >= self.threshold:
                return canonical
        self._tenant_cache[key] = norm
        return norm

    # ── Normalisation helpers ───────────────────────────────────────────────

    @staticmethod
    def _norm_address(raw: str) -> str:
        s = raw.strip().upper()
        s = re.sub(r"[.,#]", "", s)
        # Expand common abbreviations
        s = re.sub(r"\bST\b",   "STREET",   s)
        s = re.sub(r"\bAVE\b",  "AVENUE",   s)
        s = re.sub(r"\bBLVD\b", "BOULEVARD",s)
        s = re.sub(r"\bDR\b",   "DRIVE",    s)
        s = re.sub(r"\bRD\b",   "ROAD",     s)
        s = re.sub(r"\bLN\b",   "LANE",     s)
        s = re.sub(r"\bPKWY\b", "PARKWAY",  s)
        s = re.sub(r"\bSTE\b",  "SUITE",    s)
        return re.sub(r"\s+", " ", s).strip()

    @staticmethod
    def _norm_tenant(raw: str) -> str:
        # Strip legal suffixes
        s = re.sub(
            r"\b(inc\.?|llc\.?|ltd\.?|corp\.?|co\.?|company|plc|lp|llp)\b",
            "", raw, flags=re.IGNORECASE,
        )
        s = re.sub(r"[.,]", "", s)
        s = re.sub(r"\s+", " ", s).strip().title()
        return s
