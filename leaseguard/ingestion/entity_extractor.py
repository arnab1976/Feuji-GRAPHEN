"""Rule-based entity extraction — spaCy NER + regex. No API cost."""
from __future__ import annotations
import re
from typing import Optional

from loguru import logger

# ── spaCy (lazy load) ─────────────────────────────────────────────────────────
_NLP = None

def _get_nlp():
    global _NLP
    if _NLP is None:
        import spacy  # type: ignore
        try:
            _NLP = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess, sys
            logger.info("Downloading spaCy model en_core_web_sm …")
            subprocess.run(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                check=True,
            )
            _NLP = spacy.load("en_core_web_sm")
    return _NLP


class EntityExtractor:
    """
    Fast, deterministic extraction using regex patterns + spaCy NER.

    Covers: dates, dollar amounts, square footage, lease type,
    renewal options, termination notice periods, company names, locations.
    """

    # ── Compiled patterns ─────────────────────────────────────────────────
    _DATE      = re.compile(
        r"\b(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{1,2},?\s+\d{4}"
        r"|\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b",
        re.IGNORECASE,
    )
    _RENT      = re.compile(
        r"\$\s*([\d,]+(?:\.\d{1,2})?)\s*(?:per|/)\s*(?:rentable\s+)?(?:square\s+feet?|sq\.?\s*ft\.?|SF)",
        re.IGNORECASE,
    )
    _RENT2     = re.compile(            # annual / monthly rent totals
        r"\$\s*([\d,]+(?:\.\d{1,2})?)\s*(?:per\s+annum|per\s+year|annually|per\s+month|monthly)",
        re.IGNORECASE,
    )
    _SQFT      = re.compile(
        r"([\d,]+)\s*(?:rentable\s+)?(?:square\s+feet?|sq\.?\s*ft\.?|SF)\b",
        re.IGNORECASE,
    )
    _LEASE_TYPE = re.compile(
        r"\b(triple\s*net|NNN|gross\s+lease|modified\s+gross|ground\s+lease|"
        r"net\s+lease|full\s+service)\b",
        re.IGNORECASE,
    )
    _ESCALATION = re.compile(
        r"([\d.]+)\s*%\s*(?:per\s+(?:lease\s+)?year|annually|per\s+annum)",
        re.IGNORECASE,
    )
    _RENEWAL    = re.compile(
        r"(\d+)\s*[\-–]\s*year\s+(?:renewal|extension)\s+option",
        re.IGNORECASE,
    )
    _NOTICE     = re.compile(
        r"(\d+)\s*month[s]?\s+(?:prior\s+)?(?:written\s+)?notice",
        re.IGNORECASE,
    )
    _TERMINAT   = re.compile(
        r"terminat\w+.*?after\s+(?:the\s+)?(?:end\s+of\s+)?(?:year|month|lease\s+year)\s+(\d+)",
        re.IGNORECASE,
    )
    _DEPOSIT    = re.compile(
        r"security\s+deposit\s+of\s+\$\s*([\d,]+(?:\.\d{1,2})?)",
        re.IGNORECASE,
    )

    # ── Public API ─────────────────────────────────────────────────────────

    def extract(self, text: str) -> dict:
        """
        Return a dict of candidate values extracted by rule from *text*.

        All lists may be empty if nothing was found.
        Caller should pass this alongside LLM results for reconciliation.
        """
        # Limit to 50 K chars for spaCy speed
        doc_text = text[:50_000]
        nlp = _get_nlp()
        doc = nlp(doc_text)

        orgs  = [e.text.strip() for e in doc.ents if e.label_ == "ORG"]
        locs  = [e.text.strip() for e in doc.ents if e.label_ in ("GPE", "LOC", "FAC")]
        money = [e.text.strip() for e in doc.ents if e.label_ == "MONEY"]

        dates_raw = self._DATE.findall(text)
        dates = sorted(set(filter(None, [self._parse_date(d) for d in dates_raw])))

        rents_psf = [
            float(r.replace(",", "")) for r in self._RENT.findall(text)
        ]
        sqfts = [
            int(s.replace(",", "")) for s in self._SQFT.findall(text)
        ]
        lease_types = self._LEASE_TYPE.findall(text)
        escalations = [float(e) for e in self._ESCALATION.findall(text)]
        renewal_yrs = [int(y) for y in self._RENEWAL.findall(text)]
        notices     = [int(n) for n in self._NOTICE.findall(text)]
        termination_yr = next(
            (int(y) for y in self._TERMINAT.findall(text)), None
        )
        deposits = [
            float(d.replace(",", "")) for d in self._DEPOSIT.findall(text)
        ]

        return {
            "candidate_tenants":   list(dict.fromkeys(orgs))[:8],
            "candidate_locations": list(dict.fromkeys(locs))[:8],
            "candidate_money":     list(dict.fromkeys(money))[:8],
            "dates":               dates,
            "rents_psf":           rents_psf,
            "sqft_values":         sqfts,
            "lease_type_raw":      lease_types[0] if lease_types else None,
            "escalation_pcts":     escalations,
            "renewal_years":       renewal_yrs,
            "notice_months":       notices,
            "termination_after_year": termination_yr,
            "security_deposits":   deposits,
        }

    @staticmethod
    def _parse_date(raw: str) -> Optional[str]:
        """Parse a raw date string to ISO YYYY-MM-DD, or None on failure."""
        try:
            import dateparser  # type: ignore
            dt = dateparser.parse(raw, settings={"PREFER_DAY_OF_MONTH": "first",
                                                  "RETURN_AS_TIMEZONE_AWARE": False})
            return dt.strftime("%Y-%m-%d") if dt else None
        except Exception:
            return None
