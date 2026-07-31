"""
Generate synthetic commercial lease PDFs for development and testing.

Usage:
    python -m leaseguard.ingestion.lease_generator            # 25 leases
    python -m leaseguard.ingestion.lease_generator --count 50
"""
from __future__ import annotations
import os
import random
import sys
import textwrap
from datetime import date, timedelta
from pathlib import Path

from faker import Faker  # type: ignore
from reportlab.lib.pagesizes import letter  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore

from leaseguard.config import LEASE_DIR

fake = Faker()

INDUSTRIES    = ["Technology", "Finance", "Healthcare", "Retail", "Legal",
                 "Consulting", "Manufacturing", "Media", "Education", "Logistics"]
CITIES        = [
    ("Austin",       "TX", "78701"), ("Dallas",   "TX", "75201"),
    ("Houston",      "TX", "77002"), ("Denver",   "CO", "80202"),
    ("Atlanta",      "GA", "30303"), ("Chicago",  "IL", "60601"),
    ("New York",     "NY", "10001"), ("Seattle",  "WA", "98101"),
    ("San Francisco","CA", "94102"), ("Boston",   "MA", "02101"),
]
LEASE_TYPES   = ["Triple Net (NNN)", "Gross", "Modified Gross", "Ground Lease"]
PROP_CLASSES  = ["Class A", "Class B", "Class C"]
RISK_CLAUSES  = [
    ("Termination Right",
     "Tenant shall have the right to terminate this Lease effective as of the last "
     "day of the {year} Lease Year, provided Tenant delivers written notice to "
     "Landlord no later than twelve (12) months prior to the effective date of "
     "such termination together with payment of a termination fee equal to "
     "six (6) months' Base Rent."),
    ("Co-Tenancy Provision",
     "This Lease is conditioned upon co-tenancy. If the anchor tenant vacates "
     "the Property, Tenant shall have the right to reduce its Base Rent by "
     "twenty-five percent (25%) until a replacement anchor tenant of comparable "
     "stature commences operations."),
    ("Exclusivity Right",
     "Landlord covenants that, during the Lease Term, Landlord shall not lease "
     "any other space in the Property to any business primarily engaged in the "
     "same type of business as Tenant ({industry})."),
    ("Right of First Refusal",
     "Tenant shall have a Right of First Refusal to lease any adjacent space that "
     "becomes available on the same floor as the Premises. Landlord shall deliver "
     "written notice to Tenant, and Tenant shall have fifteen (15) Business Days "
     "to exercise such right."),
    ("Assignment Restriction",
     "Tenant shall not assign this Lease or sublet all or any part of the Premises "
     "without the prior written consent of Landlord, which consent shall not be "
     "unreasonably withheld, conditioned, or delayed."),
]


def generate_lease(output_path: str | Path) -> dict:
    """
    Generate one synthetic commercial lease PDF.

    Returns a dict of the generated metadata (useful for seeding tests).
    """
    output_path = Path(output_path)
    c = canvas.Canvas(str(output_path), pagesize=letter)
    w, h = letter

    # ── Generate random but plausible lease data ─────────────────────────────
    tenant    = fake.company()
    industry  = random.choice(INDUSTRIES)
    city, state, zipcode = random.choice(CITIES)
    street    = f"{random.randint(100, 9999)} {fake.street_name()}"
    address   = f"{street}, {city}, {state} {zipcode}"
    prop_cls  = random.choice(PROP_CLASSES)
    start_date = date.today() - timedelta(days=random.randint(0, 730))
    term_months = random.choice([12, 24, 36, 48, 60, 84, 120])
    end_date   = start_date + timedelta(days=int(term_months * 30.44))
    rent_psf   = round(random.uniform(15, 85), 2)
    sqft       = random.randint(2_000, 60_000)
    annual_rent = round(rent_psf * sqft, 2)
    monthly_rent = round(annual_rent / 12, 2)
    escal_pct  = round(random.choice([2.0, 2.5, 3.0, 3.5, 4.0]), 1)
    lease_type = random.choice(LEASE_TYPES)
    renew_yrs  = random.choice([3, 5, 7])
    notice_mo  = random.choice([6, 9, 12])
    deposit    = round(monthly_rent * random.choice([1, 2, 3]), 2)
    lease_id   = f"LG-{random.randint(10000, 99999)}"
    term_year  = random.choice([3, 4, 5])
    cam_rate   = round(random.uniform(4, 15), 2) if "NNN" in lease_type else 0.0

    # Choose 0–2 special risk clauses
    n_clauses = random.randint(0, 2)
    chosen_clauses = random.sample(RISK_CLAUSES, k=min(n_clauses, len(RISK_CLAUSES)))

    # ── Write PDF content ────────────────────────────────────────────────────
    y = h - 50

    def ln(text: str, bold: bool = False, size: int = 10, indent: int = 72):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(indent, y, text)
        y -= (size + 4)

    def para(text: str, size: int = 9, width: int = 65, indent: int = 72):
        nonlocal y
        c.setFont("Helvetica", size)
        for line in textwrap.wrap(text, width):
            c.drawString(indent, y, line)
            y -= (size + 3)
        y -= 4

    def rule():
        nonlocal y
        c.setLineWidth(0.4)
        c.line(72, y, w - 72, y)
        y -= 10

    # Title
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(w / 2, y, "COMMERCIAL LEASE AGREEMENT")
    y -= 24
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, y, f"Lease Reference: {lease_id}")
    y -= 20
    rule()

    # Parties
    ln("PARTIES", bold=True, size=11)
    ln(f"LANDLORD:  CBRE Property Management LLC"); ln(f"TENANT:    {tenant}")
    ln(f"INDUSTRY:  {industry}"); y -= 6; rule()

    # Premises
    ln("PREMISES", bold=True, size=11)
    ln(f"Property Address:    {address}")
    ln(f"Property Class:      {prop_cls}")
    ln(f"Rentable Area:       {sqft:,} square feet")
    y -= 6; rule()

    # Term
    ln("LEASE TERM", bold=True, size=11)
    ln(f"Commencement Date:   {start_date.strftime('%B %d, %Y')}")
    ln(f"Expiration Date:     {end_date.strftime('%B %d, %Y')}")
    ln(f"Lease Term:          {term_months} months ({round(term_months/12,1)} years)")
    y -= 6; rule()

    # Financial terms
    ln("FINANCIAL TERMS", bold=True, size=11)
    ln(f"Base Rent:           ${rent_psf:.2f} per rentable square foot per annum")
    ln(f"Annual Base Rent:    ${annual_rent:,.2f}")
    ln(f"Monthly Base Rent:   ${monthly_rent:,.2f}")
    if cam_rate > 0:
        ln(f"CAM / OpEx:          ${cam_rate:.2f} per sq ft per annum (estimated)")
    ln(f"Annual Escalation:   {escal_pct}% per Lease Year")
    ln(f"Lease Type:          {lease_type}")
    ln(f"Security Deposit:    ${deposit:,.2f}")
    y -= 6; rule()

    # Options
    ln("RENEWAL & OPTIONS", bold=True, size=11)
    ln(f"Renewal Option:      One ({renew_yrs})-year option at Fair Market Rent")
    ln(f"Renewal Notice:      {notice_mo} months prior written notice required")
    y -= 6; rule()

    # Special clauses
    if chosen_clauses:
        ln("SPECIAL PROVISIONS", bold=True, size=11)
        for clause_name, clause_tmpl in chosen_clauses:
            clause_text = clause_tmpl.format(
                year=term_year, industry=industry
            )
            ln(f"{clause_name}:", bold=True, size=9); para(clause_text, size=9)
            y -= 4
        rule()

    # Signatures
    ln("EXECUTION", bold=True, size=11)
    ln(f"LANDLORD: ___________________________  Date: ___________")
    ln(f"TENANT:   ___________________________  Date: ___________")
    y -= 10
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(w / 2, 28, "Synthetic document — generated for LeaseGuard POC testing only")

    c.save()

    return {
        "lease_id":         lease_id,
        "tenant":           tenant,
        "industry":         industry,
        "address":          address,
        "city":             city,
        "state":            state,
        "property_class":   prop_cls,
        "start_date":       start_date.isoformat(),
        "end_date":         end_date.isoformat(),
        "rent_psf":         rent_psf,
        "sqft":             sqft,
        "annual_rent":      annual_rent,
        "lease_type":       lease_type,
        "escalation_pct":   escal_pct,
        "renew_years":      renew_yrs,
        "notice_months":    notice_mo,
        "deposit":          deposit,
        "filename":         output_path.name,
        "risk_clauses":     [name for name, _ in chosen_clauses],
    }


def generate_batch(count: int = 25) -> list[dict]:
    """Generate *count* synthetic lease PDFs into the data/sample_leases folder."""
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for i in range(1, count + 1):
        path = LEASE_DIR / f"lease_{i:02d}.pdf"
        meta = generate_lease(path)
        results.append(meta)
        print(f"  ✅  {path.name}  —  {meta['tenant'][:30]:<30}  {meta['city']}, {meta['state']}")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate synthetic lease PDFs")
    parser.add_argument("--count", type=int, default=25, help="Number of PDFs to generate")
    args = parser.parse_args()
    print(f"\n🏗  Generating {args.count} synthetic lease PDFs …\n")
    metas = generate_batch(args.count)
    print(f"\n✅  Done — {len(metas)} PDFs in {LEASE_DIR}\n")
