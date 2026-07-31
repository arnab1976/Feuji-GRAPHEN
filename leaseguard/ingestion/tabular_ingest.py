"""Parse CSV / Excel uploads into LeaseGuard structured lease dicts."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger

# Flexible column aliases ? canonical lease schema keys
_COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "tenant_name": (
        "tenant_name", "tenant", "tenant name", "lessee", "company",
        "company_name", "occupant",
    ),
    "property_address": (
        "property_address", "property", "address", "building",
        "property address", "property (building)", "site", "location",
    ),
    "city": ("city", "town"),
    "state": ("state", "province", "region"),
    "lease_start_date": (
        "lease_start_date", "start_date", "start", "commencement",
        "lease start", "begin_date",
    ),
    "lease_end_date": (
        "lease_end_date", "end_date", "end", "expiration", "expiry",
        "lease end", "expiration_date",
    ),
    "base_rent_psf": (
        "base_rent_psf", "rent_psf", "rent", "base rent", "psf",
        "$/sf", "rent psf",
    ),
    "rentable_sqft": (
        "rentable_sqft", "sqft", "square_feet", "area", "rsf",
        "rentable area", "size",
    ),
    "annual_rent": ("annual_rent", "yearly_rent", "annual rent", "total_rent"),
    "lease_type": ("lease_type", "type", "lease type", "deal_type"),
    "escalation_pct": (
        "escalation_pct", "escalation", "escalation %", "bump", "increase_pct",
    ),
    "tenant_industry": ("tenant_industry", "industry", "sector", "vertical"),
    "source_file": ("source_file", "source", "filename", "file"),
    "lease_id": ("lease_id", "id", "lease", "lease id"),
    "risk_clauses": (
        "risk_clauses", "special_clauses", "clauses", "special clauses",
        "clause",
    ),
    "renewal_options": (
        "renewal_options", "renewal", "options", "renewal options",
    ),
    "termination_rights": (
        "termination_rights", "termination", "term_rights",
        "termination rights",
    ),
}


def _norm(name: Any) -> str:
    s = str(name or "").strip().lower()
    s = re.sub(r"[_\-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _map_columns(columns: list[Any]) -> dict[str, str]:
    """Return {canonical_key: actual_dataframe_column}."""
    actual = { _norm(c): c for c in columns }
    mapped: dict[str, str] = {}
    for canon, aliases in _COLUMN_ALIASES.items():
        for alias in aliases:
            key = _norm(alias)
            if key in actual:
                mapped[canon] = actual[key]
                break
    return mapped


def _cell(row: dict, col: str | None) -> Any:
    if not col:
        return None
    v = row.get(col)
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, str) and not v.strip():
        return None
    return v


def _as_str(v: Any) -> str | None:
    if v is None:
        return None
    if hasattr(v, "strftime"):
        try:
            return v.strftime("%Y-%m-%d")
        except Exception:
            pass
    s = str(v).strip()
    # Excel serial-looking dates already converted by pandas when possible
    if re.match(r"^\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    # MM/DD/YYYY
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    return s or None


def _as_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("%", "").strip())
    except (TypeError, ValueError):
        return None


def _as_int(v: Any) -> int | None:
    f = _as_float(v)
    if f is None:
        return None
    return int(f)


def _split_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    s = str(v).strip()
    if not s:
        return []
    parts = re.split(r"[;|]|\n", s)
    return [p.strip() for p in parts if p.strip()]


def _parse_renewals(v: Any) -> list[dict]:
    items = _split_list(v)
    out = []
    for item in items:
        m = re.search(r"(\d+)\s*yr", item, re.I)
        nm = re.search(r"notice\s*=?\s*(\d+)", item, re.I)
        out.append({
            "term_years": int(m.group(1)) if m else 5,
            "notice_months": int(nm.group(1)) if nm else 12,
            "rent_basis": "FMR" if "fmr" in item.lower() else "Fixed" if "fixed" in item.lower() else "FMR",
        })
    if not out and items:
        out.append({"term_years": 5, "notice_months": 12, "rent_basis": "FMR"})
    return out


def _parse_term_rights(v: Any) -> list[dict]:
    items = _split_list(v)
    out = []
    for item in items:
        ey = re.search(r"(?:after[_\s]?year|year)\s*=?\s*(\d+)", item, re.I)
        nm = re.search(r"notice\s*=?\s*(\d+)", item, re.I)
        pm = re.search(r"penalty\s*=?\s*(\d+)", item, re.I)
        out.append({
            "effective_after_year": int(ey.group(1)) if ey else 3,
            "notice_months": int(nm.group(1)) if nm else 12,
            "penalty_months": int(pm.group(1)) if pm else 0,
        })
    if not out and items:
        out.append({"effective_after_year": 3, "notice_months": 12, "penalty_months": 0})
    return out


def row_to_lease(row: dict, colmap: dict[str, str], source_file: str = "") -> dict[str, Any] | None:
    """Convert one tabular row into a LeaseGuard lease dict. Returns None if essential fields missing."""
    get = lambda k: _cell(row, colmap.get(k))

    tenant = _as_str(get("tenant_name"))
    address = _as_str(get("property_address"))
    if not tenant and not address:
        return None

    rent = _as_float(get("base_rent_psf"))
    sqft = _as_int(get("rentable_sqft"))
    annual = _as_float(get("annual_rent"))
    if annual is None and rent is not None and sqft is not None:
        annual = rent * sqft

    lease: dict[str, Any] = {
        "tenant_name": tenant or "Unknown Tenant",
        "property_address": address or "Unknown Property",
        "city": _as_str(get("city")) or "",
        "state": _as_str(get("state")) or "",
        "lease_start_date": _as_str(get("lease_start_date")) or "2000-01-01",
        "lease_end_date": _as_str(get("lease_end_date")) or "2099-12-31",
        "base_rent_psf": rent if rent is not None else 0.0,
        "rentable_sqft": sqft if sqft is not None else 0,
        "annual_rent": annual if annual is not None else 0.0,
        "lease_type": _as_str(get("lease_type")) or "Unknown",
        "escalation_pct": _as_float(get("escalation_pct")) or 0.0,
        "tenant_industry": _as_str(get("tenant_industry")) or "",
        "renewal_options": _parse_renewals(get("renewal_options")),
        "termination_rights": _parse_term_rights(get("termination_rights")),
        "risk_clauses": _split_list(get("risk_clauses")),
        "_source": source_file or _as_str(get("source_file")) or "",
        "_extraction_method": "tabular",
    }
    lid = _as_str(get("lease_id"))
    if lid:
        lease["_hint_lease_id"] = lid
    return lease


def load_tabular_file(path: str | Path, filename: str = "") -> tuple[list[dict[str, Any]], str]:
    """
    Load CSV/Excel and return (list_of_lease_dicts, summary_text).

    Raises ValueError on empty / unmapped files.
    """
    path = Path(path)
    ext = path.suffix.lower()
    name = filename or path.name

    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    elif ext == ".xls":
        try:
            df = pd.read_excel(path)  # needs xlrd for legacy .xls
        except Exception as exc:
            raise ValueError(
                "Could not read .xls. Prefer .xlsx, or install xlrd. "
                f"Detail: {exc}"
            ) from exc
    else:
        raise ValueError(f"Unsupported tabular format: {ext}")

    if df.empty:
        raise ValueError("File contains no data rows.")

    # Drop fully empty columns / rows
    df = df.dropna(how="all").dropna(axis=1, how="all")
    colmap = _map_columns(list(df.columns))
    if "tenant_name" not in colmap and "property_address" not in colmap:
        raise ValueError(
            "Could not find tenant/property columns. "
            "Expected headers like: tenant, property/address, start_date, end_date, rent_psf, sqft."
        )

    leases: list[dict[str, Any]] = []
    for _, series in df.iterrows():
        row = series.to_dict()
        lease = row_to_lease(row, colmap, source_file=name)
        if lease:
            leases.append(lease)

    if not leases:
        raise ValueError("No valid lease rows found after parsing.")

    # Build readable text for vectorization / preview
    lines = [f"TABULAR LEASE IMPORT: {name}", f"Rows parsed: {len(leases)}", ""]
    for i, lease in enumerate(leases, 1):
        lines.append(f"--- Lease {i} ---")
        for k, v in lease.items():
            if k.startswith("_"):
                continue
            lines.append(f"{k}: {v}")
        lines.append("")
    text = "\n".join(lines)
    logger.info(f"Tabular ingest  file={name}  leases={len(leases)}  mapped={list(colmap)}")
    return leases, text


def dataframe_preview(leases: list[dict[str, Any]], limit: int = 3) -> list[dict]:
    """Compact preview for the UI JSON panel."""
    keys = [
        "tenant_name", "property_address", "city", "state",
        "lease_start_date", "lease_end_date", "base_rent_psf",
        "rentable_sqft", "lease_type",
    ]
    return [{k: lease.get(k) for k in keys} for lease in leases[:limit]]
