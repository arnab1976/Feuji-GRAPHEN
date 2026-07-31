"""Unit tests for PDF extraction, NER, and entity resolution."""
from __future__ import annotations
import io
import pytest

from leaseguard.ingestion.pdf_extractor   import PDFExtractor
from leaseguard.ingestion.entity_extractor import EntityExtractor
from leaseguard.ingestion.entity_resolver  import EntityResolver


# ── PDFExtractor ──────────────────────────────────────────────────────────────

class TestPDFExtractor:
    def test_chunk_text_basic(self):
        ext = PDFExtractor()
        text = "word " * 1000   # 5000 chars
        chunks = ext.chunk_text(text, chunk_size=500, overlap=100)
        assert len(chunks) > 1
        assert all(len(c) <= 500 for c in chunks)

    def test_chunk_text_overlap(self):
        ext = PDFExtractor()
        text = "A" * 300 + "B" * 300
        chunks = ext.chunk_text(text, chunk_size=300, overlap=50)
        assert len(chunks) == 2
        # Last 50 chars of chunk0 should appear at start of chunk1
        assert chunks[0][-50:] in chunks[1] or chunks[1][:50] in chunks[0]

    def test_chunk_text_short_text(self):
        ext = PDFExtractor()
        text = "Hello world"
        chunks = ext.chunk_text(text, chunk_size=2000, overlap=200)
        assert chunks == ["Hello world"]

    def test_chunk_text_empty(self):
        ext = PDFExtractor()
        assert ext.chunk_text("") == []
        assert ext.chunk_text("   ") == []

    def test_extract_file_not_found(self):
        ext = PDFExtractor()
        with pytest.raises(FileNotFoundError):
            ext.extract("/tmp/nonexistent_lease_xyz.pdf")


# ── EntityExtractor ───────────────────────────────────────────────────────────

class TestEntityExtractor:
    def test_finds_rent_psf(self, sample_text):
        ext = EntityExtractor()
        result = ext.extract(sample_text)
        assert any(abs(r - 35.0) < 0.5 for r in result["rents_psf"]), \
            f"Expected ~35.0 in rents_psf, got {result['rents_psf']}"

    def test_finds_sqft(self, sample_text):
        ext = EntityExtractor()
        result = ext.extract(sample_text)
        assert 10000 in result["sqft_values"], \
            f"Expected 10000 in sqft_values, got {result['sqft_values']}"

    def test_finds_lease_type(self, sample_text):
        ext = EntityExtractor()
        result = ext.extract(sample_text)
        raw = (result.get("lease_type_raw") or "").upper()
        assert "NNN" in raw or "TRIPLE" in raw, f"Got lease_type_raw={raw!r}"

    def test_finds_tenant_org(self, sample_text):
        ext = EntityExtractor()
        result = ext.extract(sample_text)
        tenants = " ".join(result["candidate_tenants"]).lower()
        assert "acme" in tenants or "technology" in tenants, \
            f"Expected Acme in tenants, got {result['candidate_tenants']}"

    def test_finds_dates(self, sample_text):
        ext = EntityExtractor()
        result = ext.extract(sample_text)
        assert len(result["dates"]) >= 2, f"Expected >=2 dates, got {result['dates']}"
        assert "2024-01-01" in result["dates"] or "2028-12-31" in result["dates"]

    def test_empty_text_returns_empty_lists(self):
        ext = EntityExtractor()
        result = ext.extract("")
        assert result["rents_psf"]  == []
        assert result["sqft_values"] == []
        assert result["dates"]       == []

    def test_parse_date_iso(self):
        assert EntityExtractor._parse_date("January 1, 2024") == "2024-01-01"

    def test_parse_date_invalid(self):
        assert EntityExtractor._parse_date("not-a-date") is None

    def test_parse_date_none(self):
        assert EntityExtractor._parse_date(None) is None


# ── EntityResolver ────────────────────────────────────────────────────────────

class TestEntityResolver:
    def test_same_tenant_variations(self):
        er = EntityResolver(threshold=0.80)
        a = er.canonical_tenant("Acme Corporation Inc.")
        b = er.canonical_tenant("Acme Corporation, Inc")
        c = er.canonical_tenant("Acme Corporation")
        assert a == b == c, f"Expected same canonical name, got {a!r} {b!r} {c!r}"

    def test_different_tenants_not_merged(self):
        er = EntityResolver()
        a = er.canonical_tenant("Vantage Analytics LLC")
        b = er.canonical_tenant("Meridian Health Group")
        assert a != b

    def test_address_normalization_abbreviations(self):
        er = EntityResolver()
        a = er.canonical_address("123 Main St., Austin, TX 78701")
        b = er.canonical_address("123 Main Street Austin TX 78701")
        assert a == b, f"Expected same canonical address, got {a!r} {b!r}"

    def test_address_normalization_punct(self):
        er = EntityResolver()
        a = er.canonical_address("456, Commerce Blvd., Dallas, TX")
        b = er.canonical_address("456 Commerce Boulevard Dallas TX")
        assert a == b

    def test_unknown_address(self):
        er = EntityResolver()
        assert er.canonical_address(None)     == "Unknown Property"
        assert er.canonical_address("")       == "Unknown Property"
        assert er.canonical_address("   ")    == "Unknown Property"

    def test_unknown_tenant(self):
        er = EntityResolver()
        assert er.canonical_tenant(None)  == "Unknown Tenant"
        assert er.canonical_tenant("")    == "Unknown Tenant"

    def test_strips_legal_suffixes(self):
        er = EntityResolver()
        name = er.canonical_tenant("Brightline Legal LLC")
        assert "LLC" not in name and "Llc" not in name
