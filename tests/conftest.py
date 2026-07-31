"""Shared pytest fixtures for LeaseGuard tests."""
from __future__ import annotations
import os
import sys
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SKIP_NEO4J = os.getenv("SKIP_NEO4J_TESTS", "true").lower() != "false"

# ── Sample lease text fixture ─────────────────────────────────────────────────
SAMPLE_LEASE_TEXT = """\
COMMERCIAL LEASE AGREEMENT

PARTIES
LANDLORD: CBRE Property Management LLC
TENANT:   Acme Technology Corporation
INDUSTRY: Technology

PREMISES
Property Address:  123 Main Street, Austin, TX 78701
Property Class:    Class A
Rentable Area:     10,000 square feet

LEASE TERM
Commencement Date: January 1, 2024
Expiration Date:   December 31, 2028
Lease Term:        60 months (5.0 years)

FINANCIAL TERMS
Base Rent:         $35.00 per rentable square foot per annum
Annual Base Rent:  $350,000.00
Monthly Base Rent: $29,166.67
Annual Escalation: 3.0% per Lease Year
Lease Type:        Triple Net (NNN)
Security Deposit:  $87,500.00

RENEWAL & OPTIONS
Renewal Option:    One (5)-year option at Fair Market Rent
Renewal Notice:    12 months prior written notice required

SPECIAL PROVISIONS
Termination Right:
Tenant shall have the right to terminate this Lease effective as of the last
day of the 3 Lease Year, provided Tenant delivers written notice to Landlord
no later than twelve (12) months prior to the effective date of such
termination together with payment of a termination fee equal to six (6)
months Base Rent.
"""

SAMPLE_EXTRACTED = {
    "tenant_name":       "Acme Technology Corporation",
    "property_address":  "123 Main Street, Austin, TX 78701",
    "city":              "Austin",
    "state":             "TX",
    "lease_start_date":  "2024-01-01",
    "lease_end_date":    "2028-12-31",
    "base_rent_psf":     35.0,
    "rentable_sqft":     10000,
    "annual_rent":       350000.0,
    "lease_type":        "NNN",
    "escalation_pct":    3.0,
    "renewal_options":   [{"term_years": 5, "notice_months": 12, "rent_basis": "FMR"}],
    "termination_rights": [{"effective_after_year": 3, "notice_months": 12, "penalty_months": 6}],
    "risk_clauses":      ["Termination right after Year 3 with 12 months notice"],
    "tenant_industry":   "Technology",
}

@pytest.fixture
def sample_text() -> str:
    return SAMPLE_LEASE_TEXT

@pytest.fixture
def sample_extracted() -> dict:
    return SAMPLE_EXTRACTED

@pytest.fixture
def neo4j_skip():
    """Skip this test if Neo4j integration tests are disabled."""
    if SKIP_NEO4J:
        pytest.skip("Set SKIP_NEO4J_TESTS=false to run Neo4j integration tests")
