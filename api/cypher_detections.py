"""
Cypher Detection scenarios - dynamic from uploads + use-case heuristics / LLM.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel


class CypherDetectionsRequest(BaseModel):
    tabular_files: list[str] = []
    document_files: list[str] = []
    image_files: list[str] = []
    audio_files: list[str] = []
    text_files: list[str] = []
    hint: str = ""
    tracking_id: Optional[str] = None
    industry: Optional[str] = None
    use_case: Optional[str] = None
    primary_entities: list[str] = []
    key_relationships: list[str] = []
    skip_llm: bool = False


def _names_blob(req: CypherDetectionsRequest) -> str:
    return " ".join(
        req.tabular_files + req.document_files + req.image_files
        + req.audio_files + req.text_files + [req.hint or "", req.industry or "", req.use_case or ""]
    ).lower()


def _infer_industry(blob: str) -> tuple[str, str]:
    if re.search(r"health|patient|clinical|hipaa|claim|pharma|hospital|referral", blob):
        return "Healthcare", "Healthcare claims & care-network intelligence"
    if re.search(r"lease|tenant|property|rent|cbre|portfolio|sqft", blob):
        return "Real Estate / Lease", "Lease & portfolio knowledge graph"
    if re.search(r"supply|procurement|invoice|vendor|logistics|warehouse", blob):
        return "Supply Chain", "Procurement & vendor-risk intelligence"
    if re.search(r"aml|sanction|kyc|ofac|pmla|transaction|account|ds[1..8]|bank|fraud", blob):
        return "Financial Crime / AML", "AML investigation knowledge graph"
    return "General", "Multi-source pattern detection"


def _preview_csv(data: bytes, max_rows: int = 4) -> tuple[list[str], list[list[str]]]:
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        return [], []
    reader = csv.reader(io.StringIO(text))
    rows = [r for r in reader if any(cell.strip() for cell in r)]
    if not rows:
        return [], []
    header = [c.strip() or f"col_{i}" for i, c in enumerate(rows[0])]
    body = rows[1 : max_rows + 1]
    return header, body


def _guess_flag_column(columns: list[str]) -> Optional[str]:
    for c in columns:
        cl = c.lower()
        if any(k in cl for k in ("flag", "risk", "alert", "score", "sanction", "fraud", "aml", "phi", "typology", "exposure", "referral", "expiry", "concentration")):
            return c
    return None


def _detection_affinity_patterns(det: dict) -> list[str]:
    """Infer which tabular file name patterns a detection will traverse."""
    blob = " ".join([
        str(det.get("id") or ""),
        str(det.get("title") or ""),
        str(det.get("cypher_snippet") or ""),
        str(det.get("flags_message") or ""),
        " ".join(det.get("tags") or []),
    ]).lower()
    patterns: list[str] = []
    if any(k in blob for k in ("ring", "circular", "transaction", "transfer", "payment", "aml", "volume")):
        patterns.extend(["transaction", "txn", "account", "payment", "ds4", "ds3", "transfer"])
    if any(k in blob for k in ("sanction", "ofac", "exposure", "kyc", "breach", "sdn")):
        patterns.extend(["sanction", "individual", "person", "relationship", "kyc", "ds1", "ds7", "ds8", "ubo"])
    if any(k in blob for k in ("device", "imei", "shared", "synthetic", "fraud")):
        patterns.extend(["device", "imei", "mobile", "ds5"])
    if any(k in blob for k in ("referral", "patient", "claim", "phi", "provider", "clinical")):
        patterns.extend(["claim", "patient", "referral", "provider", "clinical", "ehr"])
    if any(k in blob for k in ("lease", "tenant", "expiry", "concentration", "portfolio", "property", "rent")):
        patterns.extend(["lease", "tenant", "property", "rent", "sqft", "portfolio", "landlord"])
    if any(k in blob for k in ("invoice", "vendor", "supplier", "procurement", "loop")):
        patterns.extend(["invoice", "vendor", "supplier", "procurement", "purchase", "po_"])
    if any(k in blob for k in ("company", "organisation", "organization", "shell", "ubo")):
        patterns.extend(["compan", "org", "vendor", "ds2"])
    if any(k in blob for k in ("address", "location", "geo")):
        patterns.extend(["address", "location", "geo", "ds6"])
    return list(dict.fromkeys(patterns))


def _target_flag_from_detection(det: dict, fname: str) -> str:
    """Flag / column Cypher will write for this detection on this dataset."""
    msg = str(det.get("flags_message") or "")
    m = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", msg)
    if m:
        return m.group(1).lower()
    det_id = str(det.get("id") or "").lower()
    fn = fname.lower()
    if "device" in det_id or "device" in fn or "imei" in fn:
        return "fraud_flag"
    if "sanction" in det_id:
        return "sanction_exposure"
    if "ring" in det_id or "transaction" in fn:
        return "aml_ring"
    if "referral" in det_id:
        return "referral_flag"
    if "phi" in det_id:
        return "phi_exposure"
    if "concentration" in det_id:
        return "concentration_flag"
    if "expiry" in det_id:
        return "expiry_cluster"
    if "invoice" in det_id:
        return "vendor_risk"
    return "risk_flag"


def _industry_file_boost(industry: str, fname: str) -> float:
    fl = fname.lower()
    ind = industry.lower()
    score = 0.0
    if "financial" in ind or "aml" in ind:
        weights = [
            ("transaction", 8), ("ds4", 8), ("account", 7), ("ds3", 7),
            ("device", 6), ("ds5", 6), ("relationship", 6), ("ds8", 6),
            ("sanction", 5), ("ds7", 5), ("individual", 4), ("ds1", 4),
            ("compan", 3), ("ds2", 3),
        ]
    elif "health" in ind:
        weights = [
            ("claim", 9), ("patient", 8), ("referral", 7), ("provider", 6),
            ("clinical", 5), ("diagnosis", 4),
        ]
    elif "lease" in ind or "real estate" in ind:
        weights = [
            ("lease", 9), ("tenant", 8), ("property", 8), ("rent", 6),
            ("portfolio", 5), ("expir", 5),
        ]
    elif "supply" in ind:
        weights = [
            ("invoice", 9), ("vendor", 8), ("supplier", 8), ("purchase", 6),
            ("shipment", 5), ("procurement", 5),
        ]
    else:
        weights = [("relationship", 4), ("entity", 3), ("record", 2)]
    for kw, pts in weights:
        if kw in fl:
            score += pts
    return score


def _score_tabular_file(fname: str, industry: str, detections: list[dict]) -> tuple[float, list[str], str, str]:
    """Return (score, linked_detection_ids, target_flag, role)."""
    fl = fname.lower()
    linked: list[str] = []
    flags: list[str] = []
    score = _industry_file_boost(industry, fname)

    for det in detections or []:
        patterns = _detection_affinity_patterns(det)
        if patterns and any(p in fl for p in patterns):
            score += 12
            did = str(det.get("id") or "")
            if did and did not in linked:
                linked.append(did)
                flags.append(_target_flag_from_detection(det, fname))

    cols = _infer_columns(fname)
    if _guess_flag_column(cols):
        score += 1.5
    elif flags:
        score += 2

    target_flag = flags[0] if flags else (_guess_flag_column(cols) or "risk_flag")
    if not linked and score >= 4:
        linked = ["session_graph"]

    role = "Cypher target"
    if linked and linked[0] != "session_graph":
        titles = [str(d.get("title", "")).split("-")[-1].strip() for d in detections if d.get("id") in linked]
        if titles:
            role = "Feeds: " + titles[0][:40]
    elif score >= 6:
        role = "Traversal source"

    return score, linked, str(target_flag).lower(), role


def _select_prominent_files(
    files: list[str],
    industry: str,
    detections: list[dict],
) -> list[tuple[str, float, list[str], str, str]]:
    """Dynamic count: all tabular sources materially used by active detections."""
    if not files:
        return []

    scored: list[tuple[str, float, list[str], str, str]] = []
    for fname in files:
        s, linked, flag, role = _score_tabular_file(fname, industry, detections)
        if s > 0:
            scored.append((fname, s, linked, flag, role))

    scored.sort(key=lambda x: (-x[1], x[0]))

    if not scored:
        return [(files[0], 1.0, [], "risk_flag", "Traversal source")]

    top = scored[0][1]
    threshold = max(3.0, top * 0.38)
    prominent = [row for row in scored if row[1] >= threshold]

    # Prefer detection-linked tables; drop unlinked only if we have enough linked ones
    linked_rows = [r for r in prominent if r[2] and "session_graph" not in r[2]]
    if len(linked_rows) >= 1:
        prominent = linked_rows if len(linked_rows) >= len(prominent) // 2 else prominent

    # Cap for layout sanity on very large uploads
    if len(prominent) > 8:
        prominent = prominent[:8]

    return prominent if prominent else [scored[0]]


def _score_unstructured_file(
    fname: str,
    detections: list[dict],
) -> tuple[float, list[str], str]:
    """Score a non-tabular source against the active LLM/rules detections."""
    filename_blob = Path(fname).stem.lower().replace("_", " ").replace("-", " ")
    linked: list[str] = []
    score = 0.5
    for det in detections or []:
        det_blob = " ".join([
            str(det.get("id") or ""),
            str(det.get("title") or ""),
            str(det.get("cypher_snippet") or ""),
            " ".join(det.get("tags") or []),
        ]).lower()
        patterns = _detection_affinity_patterns(det)
        keyword_match = patterns and any(pattern in filename_blob for pattern in patterns)
        name_tokens = {
            token for token in re.findall(r"[a-z0-9]+", filename_blob)
            if len(token) > 3
        }
        token_match = any(token in det_blob for token in name_tokens)
        if keyword_match or token_match:
            score += 12 if keyword_match else 6
            det_id = str(det.get("id") or "")
            if det_id and det_id not in linked:
                linked.append(det_id)
    role = "Evidence for: " + ", ".join(
        str(det.get("title") or det.get("id") or "").split("-")[-1].strip()
        for det in detections if det.get("id") in linked
    )[:70] if linked else "Cross-source traversal evidence"
    return score, linked, role


def _select_prominent_unstructured(
    req: CypherDetectionsRequest,
    detections: list[dict],
) -> list[tuple[str, str, float, list[str], str]]:
    files: list[tuple[str, str]] = []
    files.extend((name, "document") for name in req.document_files)
    files.extend((name, "image") for name in req.image_files)
    files.extend((name, "audio") for name in req.audio_files)
    files.extend((name, "text") for name in req.text_files)
    scored: list[tuple[str, str, float, list[str], str]] = []
    for fname, modality in files:
        score, linked, role = _score_unstructured_file(fname, detections)
        scored.append((fname, modality, score, linked, role))
    scored.sort(key=lambda row: (-row[2], row[0]))
    linked = [row for row in scored if row[3]]
    if linked:
        return linked[:4]
    return scored[: min(2, len(scored))]


def _unstructured_excerpts(req: CypherDetectionsRequest, db_client=None) -> dict[str, str]:
    excerpts: dict[str, str] = {}
    if not req.tracking_id or not db_client:
        return excerpts
    try:
        for item in db_client.get_files_for_session(req.tracking_id):
            fname = item.get("filename") or ""
            if fname not in set(
                req.document_files + req.image_files + req.audio_files + req.text_files
            ):
                continue
            content = db_client.get_file_content(item["id"]) or {}
            data = content.get("file_data") or b""
            ext = Path(fname).suffix.lower()
            text = ""
            if ext in (".txt", ".md", ".rtf", ".json", ".xml"):
                text = data.decode("utf-8", errors="replace")
            elif ext == ".pdf":
                try:
                    from pypdf import PdfReader

                    reader = PdfReader(io.BytesIO(data))
                    text = " ".join((page.extract_text() or "") for page in reader.pages[:2])
                except Exception:
                    text = ""
            elif ext in (".doc", ".docx"):
                try:
                    import docx

                    document = docx.Document(io.BytesIO(data))
                    text = " ".join(p.text for p in document.paragraphs[:40])
                except Exception:
                    text = ""
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                excerpts[fname] = text[:420]
    except Exception as exc:
        logger.warning(f"unstructured source preview failed: {exc}")
    return excerpts


def _demo_tabular_files() -> list[str]:
    return [
        "Entity_Registry.csv",
        "Business_Records.csv",
        "Relationship_Evidence.csv",
    ]


def _synthetic_rows(filename: str, columns: list[str], n: int = 4) -> list[list[str]]:
    fn = filename.lower()
    rows: list[list[str]] = []
    for i in range(n):
        row: list[str] = []
        for col in columns:
            cl = col.lower()
            if "txn" in cl or cl == "id" and "txn" in fn:
                row.append(f"TXN-{100 + i}")
            elif "from" in cl and "acc" in cl:
                row.append(f"ACC-{200 + i}")
            elif "to" in cl and "acc" in cl:
                row.append(f"ACC-{300 + i}")
            elif "amount" in cl or "amt" in cl or "inr" in cl:
                row.append(f"{(i + 1) * 2500000:,}")
            elif "date" in cl:
                row.append(f"2024-0{i + 1}-15")
            elif "channel" in cl:
                row.append(["NEFT", "RTGS", "SWIFT", "IMPS"][i % 4])
            elif "mac" in cl:
                row.append(f"AA:BB:CC:DD:0{i}:FF")
            elif "ip" in cl and "type" in cl:
                row.append(["Static IP", "Shared IP", "Dynamic IP", "VPN"][i % 4])
            elif "ip" in cl:
                row.append(f"10.0.{i + 1}.{20 + i}")
            elif "entity_name" in cl or ("name" in cl and "holder" not in cl):
                row.append(["Priya Sharma", "Rahul Singh", "Apex Retail", "Metro Holdings"][i % 4])
            elif "entity_type" in cl or cl == "rel_type":
                row.append(["Individual", "Company", "Account", "Trust"][i % 4])
            elif "holder" in cl:
                row.append(f"Holder-{i + 1}")
            elif "bank" in cl:
                row.append(["HDFC", "ICICI", "SBI", "Axis"][i % 4])
            elif "balance" in cl:
                row.append(f"{(i + 1) * 1.2:.1f}M")
            elif "device" in cl:
                row.append(f"DEV-{i + 1:03d}")
            elif "imei" in cl:
                row.append(f"IMEI-{3300 + i}")
            elif "used" in cl or "user" in cl:
                row.append(f"IND-{i + 1:03d}")
            elif "rel" in cl and "id" in cl:
                row.append(f"REL-{i + 1:03d}")
            elif cl == "type":
                row.append(["CONTROLS", "CONNECTED_TO", "OWNS", "TRANSFERRED_TO"][i % 4])
            elif "from" == cl or cl.endswith("_from"):
                row.append(f"ENT-{i + 1:03d}")
            elif "to" == cl or cl.endswith("_to"):
                row.append(f"ENT-{i + 2:03d}")
            elif "patient" in cl:
                row.append(f"PAT-{i + 1:04d}")
            elif "provider" in cl:
                row.append(f"PRV-{i + 1:03d}")
            elif "claim" in cl:
                row.append(f"CLM-{440 + i}")
            elif "tenant" in cl:
                row.append(f"TNT-{i + 1:03d}")
            elif "property" in cl or "address" in cl:
                row.append(f"Site-{i + 1}")
            elif "flag" in cl or "risk" in cl or "alert" in cl or "score" in cl:
                row.append("")
            else:
                row.append(f"VAL-{i + 1}")
        rows.append(row)
    return rows


def _infer_columns(filename: str, target_flag: Optional[str] = None) -> list[str]:
    fn = filename.lower()
    flag = (target_flag or "").lower()
    if "transaction" in fn or "ds4" in fn or "txn" in fn:
        cols = ["txn_id", "from_account_id", "to_account_id", "amount_inr", "txn_date", "channel"]
        if flag and flag not in [c.lower() for c in cols]:
            cols.append(flag)
        elif "aml" not in " ".join(cols):
            cols.append("aml_typology")
        return cols
    if "device" in fn or "ds5" in fn or "imei" in fn:
        return ["device_id", "imei_hash", "mac_address", "ip_address", "ip_type", flag or "fraud_flag"]
    if "relationship" in fn or "ds8" in fn or "rel" in fn:
        return ["rel_id", "from_entity_name", "from_entity_type", "to_entity_id", "rel_type", flag or "risk_flag"]
    if "account" in fn or "ds3" in fn:
        return ["account_id", "holder_name", "bank", "balance_inr", flag or "aml_ring"]
    if "sanction" in fn or "ds7" in fn:
        return ["entity_id", "name", "list", "country", flag or "sanction_flag"]
    if "individual" in fn or "ds1" in fn or "patient" in fn:
        return ["entity_id", "name", "role", "region", flag or "alert_flag"]
    if "compan" in fn or "ds2" in fn or "vendor" in fn:
        return ["org_id", "name", "sector", "country", flag or "risk_flag"]
    if "claim" in fn:
        return ["claim_id", "patient_id", "provider_id", "amount_inr", flag or "referral_flag"]
    if "lease" in fn or "tenant" in fn:
        return ["lease_id", "property_id", "tenant_name", "rent_psf", flag or "expiry_cluster"]
    if "invoice" in fn or "vendor" in fn:
        return ["invoice_id", "vendor_id", "org_id", "amount_inr", flag or "vendor_risk"]
    base = ["id", "field_a", "field_b", "value"]
    if flag:
        base.append(flag)
    else:
        base.append("status_flag")
    return base


def build_raw_datasets(
    req: CypherDetectionsRequest,
    db_client=None,
    industry: str = "General",
    detections: Optional[list[dict]] = None,
) -> list[dict]:
    files = list(req.tabular_files)
    detections = detections or []

    previews: dict[str, tuple[list[str], list[list[str]]]] = {}
    if req.tracking_id and db_client:
        try:
            session_files = db_client.get_files_for_session(req.tracking_id)
            for sf in session_files:
                fname = sf.get("filename") or ""
                if not fname.lower().endswith((".csv", ".xlsx", ".xls", ".tsv")):
                    continue
                content = db_client.get_file_content(sf["id"])
                if not content or not content.get("file_data"):
                    continue
                if fname.lower().endswith(".csv") or fname.lower().endswith(".tsv"):
                    hdr, body = _preview_csv(content["file_data"])
                    if hdr:
                        previews[fname] = (hdr, body)
        except Exception as exc:
            logger.warning(f"raw dataset preview failed: {exc}")

    prominent = _select_prominent_files(files, industry, detections)
    prominent_unstructured = _select_prominent_unstructured(req, detections)
    excerpts = _unstructured_excerpts(req, db_client)

    out: list[dict] = []
    for i, (fname, score, linked, target_flag, role) in enumerate(prominent):
        short = re.sub(r"\.[^.]+$", "", fname).replace("_", " ")
        columns = _infer_columns(fname, target_flag)
        if fname in previews:
            raw_cols, raw_rows = previews[fname]
            columns = raw_cols[:10]
            if target_flag and target_flag not in [c.lower() for c in columns]:
                columns = list(columns) + [target_flag]
            rows = raw_rows
        else:
            rows = _synthetic_rows(fname, columns)

        flag_col = target_flag
        if fname in previews:
            existing = _guess_flag_column(columns)
            if existing:
                flag_col = existing

        out.append({
            "id": f"source_structured_{i}",
            "title": short[:48],
            "filename": fname,
            "modality": "structured",
            "preview_kind": "table",
            "columns": columns[:10],
            "rows": [r[: len(columns)] for r in rows[:5]],
            "flag_column": flag_col,
            "flag_status": f"{flag_col} : NOT WRITTEN",
            "prominence_score": round(score, 1),
            "detection_ids": linked,
            "cypher_role": role,
        })

    for i, (fname, modality, score, linked, role) in enumerate(prominent_unstructured):
        short = re.sub(r"\.[^.]+$", "", fname).replace("_", " ")
        excerpt = excerpts.get(fname) or (
            f"{modality.title()} evidence selected because its entities, clauses, or observations "
            "are relevant to the active Cypher traversal plan."
        )
        out.append({
            "id": f"source_unstructured_{i}",
            "title": short[:56],
            "filename": fname,
            "modality": modality,
            "preview_kind": "excerpt",
            "excerpt": excerpt,
            "columns": [],
            "rows": [],
            "flag_column": None,
            "flag_status": "EVIDENCE SOURCE",
            "prominence_score": round(score, 1),
            "detection_ids": linked,
            "cypher_role": role,
        })

    out.sort(key=lambda source: (-float(source.get("prominence_score") or 0), source["filename"]))
    if len(out) > 8:
        out = out[:8]
    return out


def _graph_nodes_links(
    det_id: str,
    industry: str,
    primary_entities: Optional[list[str]] = None,
    key_relationships: Optional[list[str]] = None,
) -> tuple[list[dict], list[dict]]:
    """Small traversal graph per detection theme."""
    entities = [
        re.sub(r"[^A-Za-z0-9_ ]", "", str(value)).strip()[:40]
        for value in (primary_entities or [])[:5]
        if str(value).strip()
    ]
    relationships = [
        re.sub(r"[^A-Za-z0-9_]", "_", str(value)).upper().strip("_")[:50]
        for value in (key_relationships or [])[:5]
        if str(value).strip()
    ]
    if len(entities) >= 2:
        colors = ["#4C8DFF", "#27D199", "#F5A623", "#9B7CF6", "#FB5A6A"]
        nodes = [
            {
                "id": f"n{index + 1}",
                "label": f"{entity}-{index + 1:03d}",
                "type": entity,
                "color": colors[index % len(colors)],
            }
            for index, entity in enumerate(entities)
        ]
        links = [
            {
                "id": f"e{index + 1}",
                "source": nodes[index]["id"],
                "target": nodes[(index + 1) % len(nodes)]["id"],
                "label": relationships[index % len(relationships)]
                if relationships else "RELATED_TO",
            }
            for index in range(len(nodes))
        ]
        return nodes, links
    det_key = det_id.lower()
    industry_key = industry.lower()
    if "referral" in det_key:
        nodes = [
            {"id": "n1", "label": "PAT-1042", "type": "Patient", "color": "#4C8DFF"},
            {"id": "n2", "label": "PRV-12", "type": "Provider", "color": "#27D199"},
            {"id": "n3", "label": "PRV-44", "type": "Provider", "color": "#F5A623"},
            {"id": "n4", "label": "PRV-91", "type": "Provider", "color": "#FB5A6A"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "REFERRED_TO"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "REFERRED_TO"},
            {"id": "e3", "source": "n3", "target": "n4", "label": "REFERRED_TO"},
            {"id": "e4", "source": "n4", "target": "n1", "label": "CLAIM_FOR"},
        ]
        return nodes, links
    if "phi" in det_key or ("health" in industry_key and "exposure" in det_key):
        nodes = [
            {"id": "n1", "label": "Clinical PDF", "type": "Document", "color": "#9B7CF6"},
            {"id": "n2", "label": "PAT-1188", "type": "Patient", "color": "#4C8DFF"},
            {"id": "n3", "label": "CLM-442", "type": "Claim", "color": "#27D199"},
            {"id": "n4", "label": "PRV-44", "type": "Provider", "color": "#F5A623"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "MENTIONS"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "HAS_CLAIM"},
            {"id": "e3", "source": "n3", "target": "n4", "label": "SUBMITTED_BY"},
        ]
        return nodes, links
    if any(key in det_key for key in ("lease", "expiry", "concentration", "tenant")) or "real estate" in industry_key:
        nodes = [
            {"id": "n1", "label": "TNT-204", "type": "Tenant", "color": "#4C8DFF"},
            {"id": "n2", "label": "LEASE-31", "type": "Lease", "color": "#27D199"},
            {"id": "n3", "label": "PROP-08", "type": "Property", "color": "#F5A623"},
            {"id": "n4", "label": "Clause PDF", "type": "Document", "color": "#9B7CF6"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "HAS_LEASE"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "LOCATED_AT"},
            {"id": "e3", "source": "n4", "target": "n2", "label": "GOVERNS"},
        ]
        return nodes, links
    if any(key in det_key for key in ("vendor", "invoice", "procurement", "supplier")) or "supply" in industry_key:
        nodes = [
            {"id": "n1", "label": "VND-018", "type": "Vendor", "color": "#4C8DFF"},
            {"id": "n2", "label": "INV-442", "type": "Invoice", "color": "#27D199"},
            {"id": "n3", "label": "ORG-07", "type": "Organisation", "color": "#F5A623"},
            {"id": "n4", "label": "PO-118", "type": "PurchaseOrder", "color": "#9B7CF6"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "ISSUED"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "BILLED_TO"},
            {"id": "e3", "source": "n4", "target": "n2", "label": "RECONCILES_WITH"},
        ]
        return nodes, links
    if "ring" in det_key or "circular" in det_key:
        nodes = [
            {"id": "n1", "label": "ACC-101", "type": "Account", "color": "#27D199"},
            {"id": "n2", "label": "ACC-204", "type": "Account", "color": "#F5A623"},
            {"id": "n3", "label": "ACC-318", "type": "Account", "color": "#4C8DFF"},
            {"id": "n4", "label": "ACC-442", "type": "Account", "color": "#FB5A6A"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "TRANSFERRED_TO"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "TRANSFERRED_TO"},
            {"id": "e3", "source": "n3", "target": "n4", "label": "TRANSFERRED_TO"},
            {"id": "e4", "source": "n4", "target": "n1", "label": "TRANSFERRED_TO"},
        ]
        return nodes, links
    if "sanction" in det_key or "exposure" in det_key:
        nodes = [
            {"id": "n1", "label": "Priya S.", "type": "Individual", "color": "#4C8DFF"},
            {"id": "n2", "label": "ACC-882", "type": "Account", "color": "#27D199"},
            {"id": "n3", "label": "Shell Co", "type": "Company", "color": "#F5A623"},
            {"id": "n4", "label": "OFAC-441", "type": "Sanctioned", "color": "#FB5A6A"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "OWNS"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "PAYMENT_TO"},
            {"id": "e3", "source": "n3", "target": "n4", "label": "CONNECTED_TO"},
        ]
        return nodes, links
    if "telecom" in industry_key and "fault" in det_key:
        nodes = [
            {"id": "n1", "label": "RAN-104", "type": "NetworkElement", "color": "#4C8DFF"},
            {"id": "n2", "label": "CORE-12", "type": "NetworkElement", "color": "#27D199"},
            {"id": "n3", "label": "SVC-Voice", "type": "Service", "color": "#F5A623"},
            {"id": "n4", "label": "REGION-07", "type": "ServiceArea", "color": "#FB5A6A"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "DEPENDS_ON"},
            {"id": "e2", "source": "n2", "target": "n3", "label": "SUPPORTS"},
            {"id": "e3", "source": "n3", "target": "n4", "label": "SERVES"},
        ]
        return nodes, links
    if "telecom" in industry_key and any(key in det_key for key in ("subscriber", "device", "sim")):
        nodes = [
            {"id": "n1", "label": "DEV-001", "type": "Device", "color": "#9B7CF6"},
            {"id": "n2", "label": "SUB-118", "type": "Subscriber", "color": "#4C8DFF"},
            {"id": "n3", "label": "SUB-204", "type": "Subscriber", "color": "#F5A623"},
            {"id": "n4", "label": "SIM-882", "type": "Subscription", "color": "#27D199"},
        ]
        links = [
            {"id": "e1", "source": "n2", "target": "n1", "label": "USES"},
            {"id": "e2", "source": "n3", "target": "n1", "label": "USES"},
            {"id": "e3", "source": "n2", "target": "n4", "label": "SUBSCRIBES_WITH"},
        ]
        return nodes, links
    if "device" in det_key or "shared" in det_key:
        nodes = [
            {"id": "n1", "label": "DEV-001", "type": "Device", "color": "#9B7CF6"},
            {"id": "n2", "label": "Rahul S.", "type": "Individual", "color": "#4C8DFF"},
            {"id": "n3", "label": "Sushila P.", "type": "Individual", "color": "#F5A623"},
            {"id": "n4", "label": "ACC-019", "type": "Account", "color": "#27D199"},
        ]
        links = [
            {"id": "e1", "source": "n1", "target": "n2", "label": "USED_BY"},
            {"id": "e2", "source": "n1", "target": "n3", "label": "USED_BY"},
            {"id": "e3", "source": "n2", "target": "n4", "label": "OWNS"},
        ]
        return nodes, links
    if "health" in industry_key:
        generic_types = ("Patient", "Claim", "Provider")
    elif "manufactur" in industry_key:
        generic_types = ("Asset", "WorkOrder", "Supplier")
    elif "pharma" in industry_key:
        generic_types = ("Product", "Batch", "Site")
    elif "telecom" in industry_key:
        generic_types = ("Subscriber", "Device", "NetworkElement")
    elif "retail" in industry_key or "commerce" in industry_key:
        generic_types = ("Customer", "Product", "Order")
    else:
        generic_types = ("Entity", "Record", "Evidence")
    nodes = [
        {"id": "n1", "label": f"{generic_types[0]} A", "type": generic_types[0], "color": "#4C8DFF"},
        {"id": "n2", "label": f"{generic_types[1]} B", "type": generic_types[1], "color": "#27D199"},
        {"id": "n3", "label": f"{generic_types[2]} C", "type": generic_types[2], "color": "#F5A623"},
    ]
    links = [
        {"id": "e1", "source": "n1", "target": "n2", "label": "RELATED_TO"},
        {"id": "e2", "source": "n2", "target": "n3", "label": "RELATED_TO"},
    ]
    return nodes, links


def _build_steps(det: dict, nodes: list[dict], links: list[dict]) -> list[dict]:
    cypher_lines = det.get("cypher_lines") or []
    n_steps = max(3, min(6, len(cypher_lines) or 4))
    steps: list[dict] = []
    for i in range(n_steps):
        hop = min(i + 1, len(links))
        edge = links[min(i, len(links) - 1)] if links else None
        src = next((n for n in nodes if n["id"] == edge["source"]), nodes[0]) if edge else nodes[0]
        tgt = next((n for n in nodes if n["id"] == edge["target"]), nodes[-1]) if edge else nodes[-1]
        rel = edge["label"] if edge else "MATCH"
        steps.append({
            "hop": hop,
            "hop_total": len(links) or 1,
            "step": i + 1,
            "step_total": n_steps,
            "narrative": det.get("step_narratives", [""] * n_steps)[i] if i < len(det.get("step_narratives", [])) else (
                f"GRAPHEN traverses hop {hop}: {src['label']} -{rel}? {tgt['label']} and binds variables for the next Cypher clause."
            ),
            "flags_written": i == n_steps - 1,
            "flags_message": det.get("flags_message") if i == n_steps - 1 else None,
            "console_lines": [
                f"[Step {i + 1}] {src['label']} -> {rel} -> {tgt['label']}"
                + (" - PATTERN MATCH" if i == n_steps - 2 else "")
                + (" - FLAGS WRITTEN" if i == n_steps - 1 else "")
            ],
            "cypher_line_through": min(i + 1, len(cypher_lines)),
            "bindings": det.get("final_bindings", {}) if i == n_steps - 1 else {
                "current_node": src["label"],
                "relationship": rel,
                "hop": hop,
            },
            "highlight_nodes": [n["id"] for n in nodes[: i + 2]],
            "highlight_edges": [l["id"] for l in links[: i + 1]],
            "popup": {
                "from": src["label"],
                "rel": rel,
                "to": tgt["label"],
            },
        })
    return steps


def _heuristic_detections(
    industry: str,
    use_case: str,
    primary_entities: Optional[list[str]] = None,
    key_relationships: Optional[list[str]] = None,
) -> list[dict]:
    ind = industry.lower()
    if "health" in ind:
        templates = [
            {
                "id": "referral_ring",
                "title": "Referral Loop Detection",
                "theme": "health",
                "cypher_snippet": "MATCH (p:Patient)-[:REFERRED_TO*2..6]->(p)",
                "tags": ["care network", "multi-hop", "referral loop"],
                "cypher_lines": [
                    "MATCH (p:Patient)-[r:REFERRED_TO*2..6]->(p)",
                    "WHERE ALL(rel IN r WHERE rel.claim_amount > 50000)",
                    "WITH p, r, count(DISTINCT rel) AS hops",
                    "WHERE hops >= 3",
                    "SET p.referral_flag = 'SUSPECT_LOOP'",
                    "RETURN p.patient_id, hops, collect(rel.provider_id) AS providers",
                ],
                "step_narratives": [
                    "Seed patients with high claim volume - no referral flags exist in raw claims yet.",
                    "Traverse REFERRED_TO edges across providers in the uploaded care-network graph.",
                    "Filter paths that return to the same patient within 2..6 hops.",
                    "Bind provider IDs and hop count; prepare PHI-safe alert payload.",
                    "GRAPHEN writes referral_flag on matched patient nodes - first automated flag in this session.",
                ],
                "flags_message": "referral_flag = 'SUSPECT_LOOP' written on matched patient records",
                "final_bindings": {
                    "pattern_type": "REFERRAL_LOOP",
                    "patients_flagged": ["PAT-1042", "PAT-1188"],
                    "providers_in_loop": ["PRV-12", "PRV-44", "PRV-91"],
                },
            },
            {
                "id": "phi_exposure",
                "title": "PHI Cross-Source Exposure",
                "theme": "health",
                "cypher_snippet": "MATCH (doc:Document)-[:MENTIONS]->(p:Patient)",
                "tags": ["PHI", "cross-source", "document link"],
                "cypher_lines": [
                    "MATCH (doc:Document)-[:MENTIONS]->(p:Patient)",
                    "WHERE doc.modality IN ['pdf','image','audio']",
                    "AND NOT exists(p.phi_screened)",
                    "WITH doc, p, count(*) AS mentions",
                    "SET p.phi_exposure = 'REVIEW'",
                    "RETURN doc.source_file, p.patient_id, mentions",
                ],
                "step_narratives": [
                    "Link unstructured clinical documents to patient entities from tabular claims.",
                    "Identify patients referenced in evidence without prior PHI screening metadata.",
                    "Aggregate mention counts across modalities from your upload session.",
                    "GRAPHEN writes phi_exposure review flags - evidence trail preserved for audit.",
                ],
                "flags_message": "phi_exposure = 'REVIEW' on patients linked from unstructured evidence",
                "final_bindings": {
                    "exposure_type": "CROSS_SOURCE_PHI",
                    "documents": ["clinical_note.pdf", "lab_report.png"],
                    "patients_flagged": ["PAT-2201"],
                },
            },
        ]
    elif "real estate" in ind or "lease" in ind:
        templates = [
            {
                "id": "tenant_concentration",
                "title": "Tenant Concentration Risk",
                "theme": "lease",
                "cypher_snippet": "MATCH (t:Tenant)-[:HAS_LEASE]->(p:Property)",
                "tags": ["concentration", "portfolio", "sqft"],
                "cypher_lines": [
                    "MATCH (t:Tenant)-[:HAS_LEASE]->(p:Property)",
                    "WITH t, sum(p.sqft) AS total_sqft",
                    "MATCH (all:Property) WITH t, total_sqft, sum(all.sqft) AS portfolio",
                    "WHERE total_sqft / portfolio > 0.25",
                    "SET t.concentration_flag = 'HIGH'",
                    "RETURN t.name, total_sqft, portfolio",
                ],
                "step_narratives": [
                    "Roll up leased square footage per tenant from uploaded lease tabular sources.",
                    "Compare each tenant's footprint to total portfolio sqft in the merged graph.",
                    "Flag tenants exceeding concentration threshold - no flags in raw lease CSV yet.",
                    "GRAPHEN writes concentration_flag for portfolio risk review.",
                ],
                "flags_message": "concentration_flag = 'HIGH' on tenants above 25% portfolio sqft",
                "final_bindings": {
                    "pattern_type": "TENANT_CONCENTRATION",
                    "tenants_flagged": ["Apex Retail", "Metro Holdings"],
                    "portfolio_pct": "31.2%",
                },
            },
            {
                "id": "expiry_cluster",
                "title": "Lease Expiry Cluster",
                "theme": "lease",
                "cypher_snippet": "MATCH (l:Lease)-[:ON_PROPERTY]->(p:Property)",
                "tags": ["expiry", "cluster", "renewal"],
                "cypher_lines": [
                    "MATCH (l:Lease)-[:ON_PROPERTY]->(p:Property)",
                    "WHERE l.end_date < date() + duration('P90D')",
                    "WITH p.city AS city, collect(l) AS expiring",
                    "WHERE size(expiring) >= 3",
                    "SET l.expiry_cluster = 'Q_RENEWAL'",
                    "RETURN city, size(expiring) AS leases, collect(l.lease_id) AS ids",
                ],
                "step_narratives": [
                    "Scan lease end dates from structured uploads - expiry_flag column is empty on day 1.",
                    "Group properties by city/market for cluster detection.",
                    "Surface markets with 3+ leases expiring within 90 days.",
                    "GRAPHEN tags leases with expiry_cluster for renewal planning.",
                ],
                "flags_message": "expiry_cluster = 'Q_RENEWAL' written on clustered lease nodes",
                "final_bindings": {
                    "pattern_type": "EXPIRY_CLUSTER",
                    "markets": ["Dallas", "Austin"],
                    "leases_flagged": ["LG-1042", "LG-1098", "LG-1103"],
                },
            },
        ]
    elif "financial" in ind or "aml" in ind:
        templates = [
            {
                "id": "circular_ring",
                "title": "Circular Money Ring",
                "theme": "finance",
                "cypher_snippet": "MATCH (a:Account)-[:TRANSFERRED_TO*2..10]->(a)",
                "tags": ["ring", "multi-hop", "payments"],
                "cypher_lines": [
                    "MATCH (a:Account)-[t:TRANSFERRED_TO*2..10]->(a)",
                    "WHERE ALL(edge IN t WHERE edge.amount > 1000000)",
                    "WITH a, t, length(t) AS hops",
                    "WHERE hops >= 3",
                    "SET a.aml_ring = 'SUSPECT'",
                    "RETURN a.account_id, hops, reduce(s=0, e IN t | s + e.amount) AS volume",
                ],
                "step_narratives": [
                    "Start from accounts in raw transaction feeds - AML_FLAG column is blank on day 1.",
                    "Walk TRANSFERRED_TO chains up to 10 hops looking for cycles back to the seed account.",
                    "Filter paths with material transfer amounts across all hops.",
                    "Bind hop count and total volume; prepare SAR-ready evidence package.",
                    "GRAPHEN writes aml_ring on accounts in the closed loop - first graph-derived alert.",
                ],
                "flags_message": "aml_ring = 'SUSPECT' written on ring participant accounts",
                "final_bindings": {
                    "pattern_type": "CIRCULAR_RING",
                    "accounts_flagged": ["ACC-101", "ACC-204", "ACC-318", "ACC-442"],
                    "hops": 4,
                    "volume": "?15.0 Cr",
                },
            },
            {
                "id": "sanction_exposure",
                "title": "Sanctioned Entity Exposure",
                "theme": "finance",
                "cypher_snippet": "MATCH (i)-[*1..4]->(se:SanctionedEntity)",
                "tags": ["sanctions", "OFAC", "path"],
                "cypher_lines": [
                    "MATCH (i:Individual)-[*1..4]->(se:SanctionedEntity)",
                    "WHERE se.list IN ['OFAC', 'UN', 'EU']",
                    "WITH i, se, shortestPath((i)-[*..4]->(se)) AS p",
                    "SET i.sanction_exposure = 'BREACH'",
                    "RETURN i.name, se.entity_id, length(p) AS distance",
                ],
                "step_narratives": [
                    "Map individuals and companies from uploaded KYC / ownership tables.",
                    "Traverse up to 4 hops toward sanctioned entities in the merged graph.",
                    "Select shortest exposure path per individual for analyst review.",
                    "GRAPHEN writes sanction_exposure breach flags with path evidence.",
                ],
                "flags_message": "sanction_exposure = 'BREACH' on individuals with ?4-hop sanctioned path",
                "final_bindings": {
                    "pattern_type": "SANCTIONS_PATH",
                    "individuals_flagged": ["Priya Sharma"],
                    "sanctioned_entity": "OFAC SDN-4412",
                    "distance": 3,
                },
            },
            {
                "id": "shared_device",
                "title": "Shared Device Fraud",
                "theme": "finance",
                "cypher_snippet": "MATCH (dev:Device)-[:USED_BY]->(p:Individual)",
                "tags": ["device", "IMEI", "synthetic ID"],
                "cypher_lines": [
                    "MATCH (dev:Device)-[:USED_BY]->(p:Individual)",
                    "WITH dev, collect(p) AS users",
                    "WHERE size(users) > 1",
                    "SET dev.fraud_flag = 'SHARED_DEVICE'",
                    "RETURN dev.device_id, dev.imei, [u IN users | u.name] AS identities",
                ],
                "step_narratives": [
                    "Ingest device registry from raw DS5 - FRAUD_FLAG column has no values yet.",
                    "Group individuals per device via USED_BY relationships.",
                    "Detect devices linked to more than one identity (synthetic ID indicator).",
                    "GRAPHEN writes fraud_flag on shared devices and linked accounts.",
                ],
                "flags_message": "fraud_flag = 'SHARED_DEVICE' on DEV-001 and linked identities frozen for review",
                "final_bindings": {
                    "fraud_type": "SYNTHETIC_IDENTITY_FRAUD",
                    "device_id": "DEV-001",
                    "imei": "IMEI-3312",
                    "identities": ["Rahul Singh", "Sushila Patel"],
                    "accounts_frozen": ["ACC-019", "ACC-044"],
                },
            },
        ]
    elif "supply" in ind:
        templates = [
            {
                "id": "invoice_loop",
                "title": "Invoice Loop Detection",
                "theme": "supply",
                "cypher_snippet": "MATCH (v:Vendor)-[:INVOICED]->(o:Org)-[:PAID]->(v)",
                "tags": ["invoice", "loop", "vendor"],
                "cypher_lines": [
                    "MATCH (v:Vendor)-[:INVOICED]->(o:Organisation)",
                    "MATCH (o)-[:PAID]->(v)",
                    "WHERE o.invoice_total > 500000",
                    "SET v.vendor_risk = 'INVOICE_LOOP'",
                    "RETURN v.name, o.org_id, o.invoice_total",
                ],
                "step_narratives": [
                    "Connect vendor invoices to payer organisations from procurement uploads.",
                    "Detect reciprocal payment loops indicative of shell invoicing.",
                    "GRAPHEN flags vendors participating in invoice loops.",
                ],
                "flags_message": "vendor_risk = 'INVOICE_LOOP' written on matched vendors",
                "final_bindings": {"pattern_type": "INVOICE_LOOP", "vendors_flagged": ["Vendor-88"]},
            },
        ]
    elif "telecom" in ind:
        templates = [
            {
                "id": "subscriber_device_overlap",
                "title": "Subscriber and Device Overlap",
                "theme": "telecom",
                "cypher_snippet": "MATCH (d:Device)<-[:USES]-(s:Subscriber)",
                "tags": ["subscriber", "device", "shared identity"],
                "cypher_lines": [
                    "MATCH (d:Device)<-[:USES]-(s:Subscriber)",
                    "WITH d, collect(DISTINCT s) AS subscribers",
                    "WHERE size(subscribers) >= 3",
                    "SET d.network_signal = 'SHARED_DEVICE'",
                    "RETURN d.id, subscribers",
                ],
                "step_narratives": [
                    "Connect subscribers, subscriptions, and devices across available records.",
                    "Identify devices shared across an unusual number of subscriber identities.",
                    "Write a network signal for investigation and customer-impact review.",
                ],
                "flags_message": "network_signal = 'SHARED_DEVICE' written on matched devices",
                "final_bindings": {"pattern_type": "SHARED_DEVICE", "devices_flagged": 3},
            },
            {
                "id": "fault_propagation",
                "title": "Network Fault Propagation Path",
                "theme": "telecom",
                "cypher_snippet": "MATCH p=(n:NetworkElement)-[:DEPENDS_ON*1..6]->(x)",
                "tags": ["network", "dependency", "fault path"],
                "cypher_lines": [
                    "MATCH p=(n:NetworkElement)-[:DEPENDS_ON*1..6]->(x:NetworkElement)",
                    "WHERE n.alarm_state = 'ACTIVE'",
                    "WITH p, length(p) AS hops",
                    "SET x.impact_signal = 'PROPAGATION_PATH'",
                    "RETURN p, hops",
                ],
                "step_narratives": [
                    "Traverse service and network-element dependencies from the active alarm.",
                    "Rank downstream elements by dependency path and potential service impact.",
                    "Write an impact signal for operations prioritization.",
                ],
                "flags_message": "impact_signal = 'PROPAGATION_PATH' written on affected elements",
                "final_bindings": {"pattern_type": "FAULT_PROPAGATION", "paths_found": 4},
            },
        ]
    elif "retail" in ind or "commerce" in ind:
        templates = [
            {
                "id": "product_affinity",
                "title": "Product Affinity Cluster",
                "theme": "retail",
                "cypher_snippet": "MATCH (c:Customer)-[:PURCHASED]->(p:Product)",
                "tags": ["customer", "product", "affinity"],
                "cypher_lines": [
                    "MATCH (c:Customer)-[:PURCHASED]->(p:Product)",
                    "WITH p, collect(DISTINCT c) AS customers",
                    "WHERE size(customers) >= 3",
                    "SET p.affinity_signal = 'HIGH_COOCCURRENCE'",
                    "RETURN p.id, size(customers)",
                ],
                "step_narratives": [
                    "Connect customers, products, orders, and interaction evidence.",
                    "Find products sharing significant customer and basket relationships.",
                    "Write an affinity signal for recommendation and merchandising review.",
                ],
                "flags_message": "affinity_signal = 'HIGH_COOCCURRENCE' written on matched products",
                "final_bindings": {"pattern_type": "PRODUCT_AFFINITY", "products_flagged": 5},
            },
            {
                "id": "returns_anomaly",
                "title": "Returns and Fulfilment Anomaly",
                "theme": "retail",
                "cypher_snippet": "MATCH (c:Customer)-[:PLACED]->(o:Order)-[:RETURNED]->(p)",
                "tags": ["orders", "returns", "fulfilment"],
                "cypher_lines": [
                    "MATCH (c:Customer)-[:PLACED]->(o:Order)-[:RETURNED]->(p:Product)",
                    "WITH c, count(o) AS returns, collect(p.id) AS products",
                    "WHERE returns >= 3",
                    "SET c.review_signal = 'RETURN_PATTERN'",
                    "RETURN c.id, returns, products",
                ],
                "step_narratives": [
                    "Traverse order, product, fulfilment, and return relationships.",
                    "Identify concentrated return patterns requiring operational validation.",
                    "Write a review signal without assuming fraud or customer intent.",
                ],
                "flags_message": "review_signal = 'RETURN_PATTERN' written on matched customers",
                "final_bindings": {"pattern_type": "RETURN_PATTERN", "customers_flagged": 2},
            },
        ]
    else:
        templates = [
            {
                "id": "anomaly_cluster",
                "title": "Cross-Source Anomaly Cluster",
                "theme": "general",
                "cypher_snippet": "MATCH (a)-[r]->(b) WHERE r.confidence IS NULL",
                "tags": ["cluster", "cross-source", "anomaly"],
                "cypher_lines": [
                    "MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity)",
                    "WHERE r.score IS NULL",
                    "WITH a, b, count(r) AS links",
                    "WHERE links >= 2",
                    "SET a.anomaly_flag = 'CLUSTER'",
                    "RETURN a.id, b.id, links",
                ],
                "step_narratives": [
                    "Merge entities from all uploaded modalities into a single graph.",
                    "Find dense relationship clusters without pre-existing risk scores.",
                    "GRAPHEN writes anomaly_flag for analyst triage.",
                ],
                "flags_message": "anomaly_flag = 'CLUSTER' on dense relationship hubs",
                "final_bindings": {"pattern_type": "ANOMALY_CLUSTER", "entities_flagged": 3},
            },
        ]

    detections: list[dict] = []
    for i, tpl in enumerate(templates):
        nodes, links = _graph_nodes_links(
            tpl["id"], industry, primary_entities, key_relationships
        )
        steps = _build_steps(tpl, nodes, links)
        detections.append({
            "id": tpl["id"],
            "index": i + 1,
            "title": f"Detection {i + 1} - {tpl['title']}",
            "subtitle": tpl.get("cypher_snippet", "")[:80],
            "theme": tpl.get("theme", "general"),
            "cypher_snippet": tpl["cypher_snippet"],
            "tags": tpl.get("tags", []),
            "cypher_lines": tpl["cypher_lines"],
            "flags_message": tpl.get("flags_message"),
            "final_bindings": tpl.get("final_bindings", {}),
            "steps": steps,
            "graph": {"nodes": nodes, "links": links},
        })
    return detections


def _parse_flag_value(flags_message: Optional[str]) -> str:
    if not flags_message:
        return "FLAGGED"
    m = re.search(r"=\s*'([^']+)'", flags_message)
    if m:
        return m.group(1)
    m2 = re.search(r'=\s*"([^"]+)"', flags_message)
    if m2:
        return m2.group(1)
    return "FLAGGED"


def _link_detections_to_datasets(detections: list[dict], raw_datasets: list[dict]) -> None:
    """Attach target_dataset_ids and written_flag_value on each detection."""
    for det in detections:
        did = str(det.get("id") or "")
        patterns = _detection_affinity_patterns(det)
        targets: list[str] = []
        for ds in raw_datasets:
            ds_id = str(ds.get("id") or "")
            if not ds_id:
                continue
            if did in (ds.get("detection_ids") or []):
                targets.append(ds_id)
            elif patterns and any(p in (ds.get("filename") or "").lower() for p in patterns):
                targets.append(ds_id)
        det["target_dataset_ids"] = list(dict.fromkeys(targets))
        msg = det.get("flags_message")
        if not msg:
            steps = det.get("steps") or []
            if steps:
                msg = steps[-1].get("flags_message")
        det["written_flag_value"] = _parse_flag_value(msg)


def _attach_execution_metadata(detections: list[dict], sources: list[dict]) -> None:
    """Build relationship-table rows for the highest-significance graph path."""
    source_by_id = {str(source.get("id")): source for source in sources}
    for det in detections:
        graph = det.get("graph") or {}
        nodes = {str(node.get("id")): node for node in graph.get("nodes") or []}
        links = graph.get("links") or []
        evidence_names = [
            source_by_id[source_id].get("filename")
            for source_id in det.get("target_dataset_ids") or []
            if source_id in source_by_id
        ]
        rows: list[dict] = []
        for index, link in enumerate(links):
            source_id = str(link.get("source") or "")
            target_id = str(link.get("target") or "")
            source_node = nodes.get(source_id, {"label": source_id, "type": "Entity"})
            target_node = nodes.get(target_id, {"label": target_id, "type": "Entity"})
            rows.append({
                "id": str(link.get("id") or f"path_edge_{index + 1}"),
                "path_rank": 1,
                "sequence": index + 1,
                "source": source_node.get("label") or source_id,
                "source_type": source_node.get("type") or "Entity",
                "relationship": link.get("label") or "RELATED_TO",
                "target": target_node.get("label") or target_id,
                "target_type": target_node.get("type") or "Entity",
                "hops": index + 1,
                "significance_score": max(55, 98 - index * 7),
                "evidence_source": ", ".join(evidence_names[:3]) or "Unified session graph",
                "flag_result": det.get("flags_message") or "Pattern candidate",
            })
        det["significant_paths"] = rows
        det["result_summary"] = {
            "nodes_evaluated": len(nodes),
            "relationships_traversed": len(links),
            "significant_path_hops": len(rows),
            "target_sources": len(evidence_names),
        }


def _build_detection_intro(
    req: CypherDetectionsRequest,
    industry: str,
    use_case: str,
    detections: list[dict],
    sources: list[dict],
) -> str:
    structured = sum(1 for source in sources if source.get("modality") == "structured")
    unstructured = len(sources) - structured
    detection_names = [
        str(det.get("title") or "").split("-")[-1].strip()
        for det in detections[:4]
    ]
    plan = ", ".join(name for name in detection_names if name)
    return (
        f"For {use_case}, Cypher will traverse the most relevant {structured} structured "
        f"and {unstructured} unstructured source(s), execute {len(detections)} "
        f"{industry} detection scenario(s), expose each significant relationship path, "
        f"and write flags only when a traversal completes. Planned scenarios: {plan}."
    )


def build_cypher_detections(req: CypherDetectionsRequest, db_client=None) -> dict:
    if not any((
        req.tabular_files,
        req.document_files,
        req.image_files,
        req.audio_files,
        req.text_files,
    )):
        req = req.model_copy(update={
            "tabular_files": _demo_tabular_files(),
            "document_files": [
                "Policy_Evidence.pdf", "Supporting_Records.pdf",
            ],
            "hint": req.hint or "demo session",
        })
        demo = True
    else:
        demo = False

    blob = _names_blob(req)
    industry = req.industry or _infer_industry(blob)[0]
    use_case = req.use_case or _infer_industry(blob)[1]

    detections = _heuristic_detections(
        industry,
        use_case,
        req.primary_entities,
        req.key_relationships,
    )
    raw_datasets = build_raw_datasets(req, db_client, industry, detections)
    _link_detections_to_datasets(detections, raw_datasets)
    _attach_execution_metadata(detections, raw_datasets)
    intro = _build_detection_intro(req, industry, use_case, detections, raw_datasets)

    return {
        "industry": industry,
        "use_case": use_case,
        "source": "heuristic",
        "demo": demo,
        "phase_label": "Phase 2 of 4",
        "intro": intro,
        "banner": "No detection has run yet. Select Run on one scenario or execute all detections sequentially.",
        "raw_section_title": "PROMINENT STRUCTURED + UNSTRUCTURED SOURCES TARGETED BY CYPHER",
        "raw_datasets_subtitle": (
            f"Showing {len(raw_datasets)} use-case-specific source(s) selected for active Cypher traversals."
        ),
        "raw_datasets": raw_datasets,
        "detections": detections,
    }


def enrich_with_llm(payload: dict, req: CypherDetectionsRequest) -> dict:
    """Optional LLM pass to rename detections / add industry-specific scenarios."""
    try:
        from leaseguard.llm.llm_client import LLMClient

        system = (
            "You are GRAPHEN's Cypher detection planner. Given uploads and industry, "
            "return STRICT JSON with keys: industry, use_case, intro, detections (array).\n"
            "intro must be 1-2 concise sentences explaining exactly what this page will "
            "traverse and detect for the supplied requirement and source modalities.\n"
            "Each detection: id, title (without 'Detection N' prefix), cypher_snippet, "
            "tags (array of 2..4 short strings), cypher_lines (array of 4..6 Cypher lines), "
            "step_narratives (array, same length as meaningful steps), flags_message, "
            "final_bindings (object with 3..5 keys).\n"
            "Provide 2..4 detections tailored to the industry. "
            "Do NOT use AML/sanctions scenarios unless data is clearly financial crime. "
            "Healthcare: referral/PHI. Real estate: lease/tenant. Supply chain: vendor/invoice."
        )
        user = json.dumps({
            "hint": req.hint,
            "industry": payload.get("industry"),
            "use_case": payload.get("use_case"),
            "tabular": req.tabular_files,
            "documents": req.document_files,
            "images": req.image_files,
            "audio": req.audio_files,
        })
        parsed = LLMClient().extract_json(system, user)
        if not parsed or not isinstance(parsed, dict):
            return payload

        llm_dets = parsed.get("detections") or []
        if not llm_dets:
            return payload

        merged: list[dict] = []
        for i, d in enumerate(llm_dets[:4]):
            if not isinstance(d, dict) or not d.get("title"):
                continue
            det_id = re.sub(
                r"[^a-z0-9_]+",
                "_",
                str(d.get("id") or f"det_{i}").lower().replace(" ", "_"),
            ).strip("_")[:40] or f"det_{i}"
            nodes, links = _graph_nodes_links(
                det_id,
                payload.get("industry", ""),
                req.primary_entities,
                req.key_relationships,
            )
            tpl = {
                "id": det_id,
                "cypher_lines": d.get("cypher_lines") or ["MATCH (n) RETURN n LIMIT 1"],
                "step_narratives": d.get("step_narratives") or [],
                "flags_message": d.get("flags_message"),
                "final_bindings": d.get("final_bindings") or {},
            }
            steps = _build_steps(tpl, nodes, links)
            merged.append({
                "id": det_id,
                "index": i + 1,
                "title": f"Detection {i + 1} - {str(d['title'])[:56]}",
                "subtitle": str(d.get("cypher_snippet", ""))[:80],
                "theme": "llm",
                "cypher_snippet": str(d.get("cypher_snippet", ""))[:120],
                "tags": [str(t)[:24] for t in (d.get("tags") or [])[:4]],
                "cypher_lines": tpl["cypher_lines"],
                "flags_message": d.get("flags_message"),
                "final_bindings": d.get("final_bindings") or {},
                "steps": steps,
                "graph": {"nodes": nodes, "links": links},
            })
        if merged:
            industry = str(parsed.get("industry") or payload["industry"])[:80]
            use_case = str(parsed.get("use_case") or payload["use_case"])[:120]
            payload["detections"] = merged
            payload["industry"] = industry
            payload["use_case"] = use_case
            if parsed.get("intro"):
                payload["intro"] = str(parsed.get("intro"))[:600]
            payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Cypher detections LLM enrich failed: {exc}")
    return payload


def refresh_raw_datasets_for_payload(
    payload: dict,
    req: CypherDetectionsRequest,
    db_client=None,
) -> dict:
    """Recompute prominent mixed sources and execution metadata after LLM changes."""
    industry = payload.get("industry") or "General"
    detections = payload.get("detections") or []
    raw = build_raw_datasets(req, db_client, industry, detections)
    _link_detections_to_datasets(detections, raw)
    _attach_execution_metadata(detections, raw)
    payload["raw_datasets"] = raw
    payload["raw_datasets_subtitle"] = (
        f"Showing {len(raw)} use-case-specific structured and unstructured source(s) "
        "selected for active Cypher traversals."
    )
    payload["raw_section_title"] = (
        "PROMINENT STRUCTURED + UNSTRUCTURED SOURCES TARGETED BY CYPHER"
    )
    if not payload.get("intro"):
        payload["intro"] = _build_detection_intro(
            req,
            industry,
            payload.get("use_case") or "the active requirement",
            detections,
            raw,
        )
    return payload
