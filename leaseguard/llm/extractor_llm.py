"""LLM-based structured lease extraction — aligned to the OWL ontology schema."""
from __future__ import annotations
from loguru import logger

from leaseguard.config import LLM_EXTRACT_CHARS
from leaseguard.llm.llm_client import LLMClient
from leaseguard.llm.prompts import EXTRACTION_SYSTEM, EXTRACTION_USER


class LLMExtractor:
    """
    Send raw lease text to the LLM with a strict JSON-schema system prompt.

    The schema is derived from the OWL ontology (ontology/cbre_lease.owl)
    so every extracted field maps directly to a graph node property.
    """

    def __init__(self, client: LLMClient | None = None) -> None:
        self._llm = client or LLMClient()

    def extract(self, text: str) -> dict:
        """
        Extract all lease fields from *text* and return a validated dict.

        Uses only the first LLM_EXTRACT_CHARS characters to stay within
        model token limits while still capturing most standard lease headers.
        """
        chunk = text[:LLM_EXTRACT_CHARS]
        logger.info(f"LLM extraction  chars={len(chunk)}")

        result = self._llm.extract_json(
            system=EXTRACTION_SYSTEM,
            user=EXTRACTION_USER.format(text=chunk),
        )

        result["_extraction_method"] = "llm"
        result["_text_chars_used"]   = len(chunk)

        # Coerce numeric fields that sometimes arrive as strings
        for field in ("base_rent_psf", "annual_rent", "monthly_rent",
                      "escalation_pct", "cam_charges_psf", "security_deposit"):
            if isinstance(result.get(field), str):
                try:
                    result[field] = float(result[field].replace(",", "").replace("$", ""))
                except (ValueError, AttributeError):
                    result[field] = None

        for field in ("rentable_sqft", "term_months"):
            if isinstance(result.get(field), str):
                try:
                    result[field] = int(result[field].replace(",", ""))
                except (ValueError, AttributeError):
                    result[field] = None

        return result
