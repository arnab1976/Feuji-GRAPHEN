"""
LeaseGuard FastAPI REST API

Run:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    # Swagger UI: http://localhost:8000/docs
"""
from __future__ import annotations
import json
import os
import sys
import tempfile
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from loguru import logger
from pydantic import BaseModel

# Ensure project root is on the path when running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from leaseguard.agents.lease_agent  import LeaseAgent
from leaseguard.agents.risk_agent   import RiskAgent
from leaseguard.graph.graph_queries import GraphQueries
from leaseguard.graph.neo4j_client  import Neo4jClient
from api.database import db_client
from api.cypher_detections import (
    CypherDetectionsRequest,
    build_cypher_detections,
    enrich_with_llm,
    refresh_raw_datasets_for_payload,
)
from api.crossdoc_discovery import (
    CrossDocDiscoveryRequest,
    build_crossdoc_payload,
    enrich_crossdoc_with_llm,
)
from api.intelligence_report import (
    IntelligenceReportRequest,
    IntelligenceReportSummaryRequest,
    build_intelligence_report,
    build_intelligence_report_summary,
    enrich_intelligence_report_with_llm,
    enrich_intelligence_report_summary_with_llm,
)
from api.final_report import (
    FinalReportRequest,
    FinalReportSummaryRequest,
    build_final_report,
    build_final_report_summary,
    enrich_final_report_with_llm,
    enrich_final_report_summary_with_llm,
)
from api.domain_configurator import (
    DomainConfiguratorRequest,
    TrendingUseCasesRequest,
    build_domain_configuration,
    build_trending_use_cases,
    enrich_domain_configuration_with_llm,
    enrich_trending_use_cases_with_llm,
)
from api.schema_registry import (
    SchemaRegistryRequest,
    build_schema_registry,
    enrich_schema_registry_with_llm,
)
from api.next_ai import (
    NextAIAskRequest,
    NextAIContextRequest,
    answer_next_ai,
    build_next_ai_status,
)
from api.kg_validation import (
    resolve_validation_context,
    run_kg_validation,
    validation_csv,
)

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="LeaseGuard API",
    version="0.1.0",
    description=(
        "Knowledge Graph–Powered Lease Intelligence API.\n\n"
        "All endpoints return graph-grounded data — no hallucination."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Singletons (created once at startup) ─────────────────────────────────────
_agent: LeaseAgent | None = None
_risk:  RiskAgent  | None = None
_gq:    GraphQueries | None = None


def get_agent() -> LeaseAgent:
    global _agent
    if _agent is None:
        _agent = LeaseAgent()
    return _agent


def get_risk() -> RiskAgent:
    global _risk
    if _risk is None:
        _risk = RiskAgent()
    return _risk


def get_queries() -> GraphQueries:
    global _gq
    if _gq is None:
        _gq = GraphQueries()
    return _gq


# ── Request / Response models ─────────────────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str

class CypherRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer:        str
    graph_context: list
    doc_context:   list
    question:      str

# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["ui"])
def root():
    # Read fresh bytes each request so browsers never keep a stale SPA shell
    from fastapi.responses import HTMLResponse

    html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    with open(html_path, "r", encoding="utf-8") as fh:
        html = fh.read()
    return HTMLResponse(
        content=html,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/api/health", tags=["health"])
def health():
    try:
        ok = Neo4jClient().ping()
        return {"neo4j": ok, "status": "ok" if ok else "neo4j_unreachable"}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(exc)})

import uuid
from typing import Dict, Any

_sessions: Dict[str, Any] = {}

class SessionRequest(BaseModel):
    session_id: str

_DOC_EXTS = (".pdf", ".doc", ".docx")
_TABULAR_EXTS = (".csv", ".xlsx", ".xls")
_ALLOWED_UPLOAD_EXTS = _DOC_EXTS + _TABULAR_EXTS


@app.post("/api/ingest/step1_extract", tags=["ingestion"])
async def step1_extract(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(_ALLOWED_UPLOAD_EXTS):
        raise HTTPException(
            400,
            "Supported formats: PDF, Word (.doc/.docx), CSV, or Excel (.xlsx/.xls).",
        )
    data = await file.read()
    if len(data) == 0:
        raise HTTPException(400, "Uploaded file is empty.")

    session_id = str(uuid.uuid4())
    import tempfile, os
    from pathlib import Path

    ext = Path(file.filename).suffix.lower()
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        if ext in _TABULAR_EXTS:
            from leaseguard.ingestion.tabular_ingest import (
                dataframe_preview,
                load_tabular_file,
            )

            leases, text = load_tabular_file(tmp_path, filename=file.filename)
            chunks = get_agent()._pdf.chunk_text(text)
            _sessions[session_id] = {
                "filename": file.filename,
                "raw_text": text,
                "pages": 1,
                "chunks": chunks,
                "source_type": "tabular",
                "tabular_leases": leases,
                "extracted_data": leases[0],
            }
            return {
                "session_id": session_id,
                "filename": file.filename,
                "pages": 1,
                "chunks_count": len(chunks),
                "sample_text": chunks[:2] if chunks else [],
                "source_type": "tabular",
                "rows_parsed": len(leases),
                "preview": dataframe_preview(leases),
            }

        raw = {"full_text": "", "filename": file.filename, "page_count": 1}
        if ext == ".pdf":
            raw = get_agent()._pdf.extract(tmp_path)
        elif ext in (".docx", ".doc"):
            try:
                import docx
                doc = docx.Document(tmp_path)
                raw["full_text"] = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                logger.warning(f"Failed to parse docx using python-docx: {e}")
                raw["full_text"] = data.decode("utf-8", errors="ignore")

        chunks = get_agent()._pdf.chunk_text(raw["full_text"])
        _sessions[session_id] = {
            "filename": file.filename,
            "raw_text": raw["full_text"],
            "pages": raw.get("page_count", 1),
            "chunks": chunks,
            "source_type": "document",
        }

        return {
            "session_id": session_id,
            "filename": file.filename,
            "pages": raw.get("page_count", 1),
            "chunks_count": len(chunks),
            "sample_text": chunks[:2] if chunks else [],
            "source_type": "document",
        }
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        logger.exception(f"Step 1 failed for {file.filename}")
        raise HTTPException(500, f"Extraction failed: {exc}")
    finally:
        os.unlink(tmp_path)

@app.post("/api/ingest/step2_ner", tags=["ingestion"])
def step2_ner(req: SessionRequest):
    if req.session_id not in _sessions:
        raise HTTPException(404, "Session not found.")
    sess = _sessions[req.session_id]
    if sess.get("source_type") == "tabular":
        return {
            "status": "success",
            "info": "Skipped NER — columns already mapped from CSV/Excel",
            "source_type": "tabular",
            "rows": len(sess.get("tabular_leases") or []),
        }
    return {"status": "success", "info": "Regex / NER complete"}

@app.post("/api/ingest/step3_llm", tags=["ingestion"])
def step3_llm(req: SessionRequest):
    if req.session_id not in _sessions:
        raise HTTPException(404, "Session not found.")
    sess = _sessions[req.session_id]
    try:
        if sess.get("source_type") == "tabular":
            leases = sess.get("tabular_leases") or []
            if not leases:
                raise HTTPException(400, "No tabular lease rows in session.")
            data = leases[0]
            sess["extracted_data"] = data
            return {
                "extracted": data,
                "source_type": "tabular",
                "rows_parsed": len(leases),
                "all_leases": leases,
                "info": "Structured fields mapped from spreadsheet columns (LLM skipped).",
            }
        data = get_agent()._llm_ext.extract(sess["raw_text"])
        sess["extracted_data"] = data
        return {"extracted": data}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Step 3 LLM failed")
        raise HTTPException(500, f"LLM Extraction failed: {exc}")

@app.post("/api/ingest/step4_resolve", tags=["ingestion"])
def step4_resolve(req: SessionRequest):
    if req.session_id not in _sessions:
        raise HTTPException(404, "Session not found.")
    # Simulated resolution step
    return {"status": "success", "info": "Entity resolution complete"}

@app.post("/api/ingest/step5_graph", tags=["ingestion"])
def step5_graph(req: SessionRequest):
    if req.session_id not in _sessions:
        raise HTTPException(404, "Session not found.")
    sess = _sessions[req.session_id]
    try:
        writer = get_agent()._writer
        if sess.get("source_type") == "tabular":
            leases = sess.get("tabular_leases") or [sess.get("extracted_data")]
            lease_ids = []
            for lease in leases:
                if not lease:
                    continue
                lid = writer.write_lease(lease, source_file=sess["filename"])
                lease_ids.append(lid)
            if not lease_ids:
                raise HTTPException(400, "No lease rows to write.")
            sess["lease_id"] = lease_ids[0]
            sess["lease_ids"] = lease_ids
            return {
                "lease_id": lease_ids[0],
                "lease_ids": lease_ids,
                "rows_written": len(lease_ids),
                "source_type": "tabular",
            }

        lease_id = writer.write_lease(sess["extracted_data"], source_file=sess["filename"])
        sess["lease_id"] = lease_id
        return {"lease_id": lease_id}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Step 5 Graph Write failed")
        raise HTTPException(500, f"Graph Write failed: {exc}")

@app.post("/api/ingest/step6_vector", tags=["ingestion"])
def step6_vector(req: SessionRequest):
    if req.session_id not in _sessions:
        raise HTTPException(404, "Session not found.")
    sess = _sessions[req.session_id]
    try:
        n_chunks = get_agent()._vector.add_chunks(
            sess["chunks"], sess["lease_id"], sess["filename"]
        )

        payload = {
            "status": "success",
            "lease_id": sess["lease_id"],
            "filename": sess["filename"],
            "pages": sess["pages"],
            "chunks": n_chunks,
            "extracted": sess["extracted_data"],
            "source_type": sess.get("source_type", "document"),
        }
        if sess.get("lease_ids"):
            payload["lease_ids"] = sess["lease_ids"]
            payload["rows_written"] = len(sess["lease_ids"])
        return payload
    except Exception as exc:
        logger.exception("Step 6 Vectorization failed")
        raise HTTPException(500, f"Vectorization failed: {exc}")

# ── Lease data ────────────────────────────────────────────────────────────────

@app.get("/api/leases", tags=["leases"])
def list_leases(limit: int = Query(default=100, le=500)):
    """List all leases with property and tenant details."""
    return get_queries().all_leases(limit=limit)


@app.get("/api/leases/{lease_id}", tags=["leases"])
def get_lease(lease_id: str):
    """Fetch a single lease by its ID (e.g. LG-A3F9B2)."""
    detail = get_queries().lease_by_id(lease_id.upper())
    if not detail:
        raise HTTPException(404, f"Lease {lease_id!r} not found.")
    return detail


@app.get("/api/expiring", tags=["risk"])
def expiring_leases(days: int = Query(default=90, ge=1, le=730)):
    """Leases expiring within the next *days* calendar days."""
    return get_queries().expiring_leases(days)


@app.get("/api/concentration", tags=["risk"])
def tenant_concentration():
    """Tenant concentration analysis — sqft share per tenant."""
    return get_queries().tenant_concentration()


@app.get("/api/clauses", tags=["risk"])
def high_risk_clauses():
    """All leases containing AI-flagged high-risk clauses."""
    return get_queries().high_risk_clauses()


@app.get("/api/summary", tags=["analytics"])
def portfolio_summary():
    """High-level portfolio statistics."""
    return get_queries().portfolio_summary()


@app.get("/api/cities", tags=["analytics"])
def city_breakdown():
    """Lease count and sqft by city."""
    return get_queries().city_breakdown()


@app.get("/api/graph", tags=["analytics"])
def graph_data(limit: int = Query(default=50, le=200)):
    """
    Return nodes + edges for graph visualisation.
    Compatible with pyvis and D3 force-directed layouts.
    """
    return get_queries().graph_for_visualisation(limit=limit)


@app.get("/api/relationships", tags=["analytics"])
def relationships(limit: int = Query(default=500, le=2000)):
    """
    Lease-centric relationship table from the knowledge graph:
    Lease ID · Property · Tenant · path · special clauses.
    """
    try:
        return get_queries().relationships_table(limit=limit)
    except Exception as exc:
        logger.exception("Relationships query failed")
        raise HTTPException(500, f"Relationships query failed: {exc}")

# ── Q&A ───────────────────────────────────────────────────────────────────────

@app.post("/api/ask", response_model=QuestionResponse, tags=["ai"])
def ask(req: QuestionRequest):
    """Graph-grounded natural language Q&A."""
    if not req.question.strip():
        raise HTTPException(400, "Question must not be empty.")
    try:
        result = get_agent().ask(req.question)
        return QuestionResponse(**result)
    except Exception as exc:
        logger.exception("Q&A failed")
        raise HTTPException(500, f"Q&A failed: {exc}")


@app.post("/api/cypher", tags=["ai"])
def cypher_query(req: CypherRequest):
    """Translate a natural-language question to Cypher and execute it."""
    try:
        return get_agent().cypher(req.question)
    except Exception as exc:
        raise HTTPException(500, f"Cypher translation failed: {exc}")


@app.get("/api/risk/{lease_id}", tags=["risk"])
def lease_risk(lease_id: str):
    """AI-generated TOP-3 risk analysis for a specific lease."""
    try:
        summary = get_agent().risk(lease_id.upper())
        score   = get_risk().score_lease(lease_id.upper())
        return {"lease_id": lease_id, "risk_summary": summary, "risk_score": score}
    except Exception as exc:
        raise HTTPException(500, f"Risk analysis failed: {exc}")


@app.get("/api/risk/portfolio/report", tags=["risk"])
def portfolio_risk_report():
    """Full AI-generated portfolio risk report."""
    try:
        return {"report": get_risk().full_risk_report()}
    except Exception as exc:
        raise HTTPException(500, f"Report generation failed: {exc}")


@app.get("/api/risk/portfolio/narrative", tags=["risk"])
def portfolio_narrative():
    """Short AI-generated executive narrative of the portfolio."""
    try:
        return {"narrative": get_agent().portfolio_narrative()}
    except Exception as exc:
        raise HTTPException(500, f"Narrative generation failed: {exc}")


# ── File Upload Tracking ───────────────────────────────────────────────────────
import uuid
from typing import List
from fastapi import Response

@app.post("/api/uploads", tags=["uploads"])
async def upload_files(
    files: List[UploadFile] = File(...),
    scenario_tracking_id: str = Form(""),
    industry: str = Form(""),
    use_case: str = Form(""),
):
    tracking_id = str(uuid.uuid4())[:8].upper()
    db_client.create_session(
        tracking_id, scenario_tracking_id, industry, use_case
    )
    saved = 0
    skipped = []
    seen = set()
    for f in files:
        name = f.filename or ""
        key = name.lower()
        if not key or key in seen:
            if name:
                skipped.append(name)
            continue
        seen.add(key)
        data = await f.read()
        db_client.save_file(tracking_id, name, f.content_type, data)
        saved += 1
    return {
        "tracking_id": tracking_id,
        "status": "success",
        "scenario_tracking_id": scenario_tracking_id,
        "industry": industry,
        "use_case": use_case,
        "files_uploaded": saved,
        "files_skipped": skipped,
    }

@app.get("/api/uploads/recent", tags=["uploads"])
def get_recent_uploads():
    sessions = db_client.get_recent_sessions(limit=5)
    return {"recent": sessions}

@app.delete("/api/uploads/{tracking_id}", tags=["uploads"])
def delete_upload_session(tracking_id: str):
    result = db_client.delete_session(tracking_id)
    if not result["deleted"]:
        raise HTTPException(status_code=404, detail="Upload session not found")
    return {
        "status": "deleted",
        "tracking_id": tracking_id,
        "files_deleted": result["file_count"],
    }

@app.get("/api/uploads/{tracking_id}/files", tags=["uploads"])
def get_session_files(tracking_id: str):
    files = db_client.get_files_for_session(tracking_id)
    return {
        "tracking_id": tracking_id,
        "session": db_client.get_session(tracking_id),
        "files": files,
    }

@app.post("/api/uploads/{tracking_id}/append", tags=["uploads"])
async def append_to_session(
    tracking_id: str,
    files: List[UploadFile] = File(...),
    scenario_tracking_id: str = Form(""),
    industry: str = Form(""),
    use_case: str = Form(""),
):
    # Ensure session row exists
    db_client.create_session(
        tracking_id, scenario_tracking_id, industry, use_case
    )
    existing = {
        str(f.get("filename") or "").lower()
        for f in (db_client.get_files_for_session(tracking_id) or [])
    }
    saved = 0
    skipped = []
    for f in files:
        name = f.filename or ""
        key = name.lower()
        if not key or key in existing:
            if name:
                skipped.append(name)
            continue
        data = await f.read()
        db_client.save_file(tracking_id, name, f.content_type, data)
        existing.add(key)
        saved += 1
    return {
        "tracking_id": tracking_id,
        "status": "success",
        "scenario_tracking_id": scenario_tracking_id,
        "industry": industry,
        "use_case": use_case,
        "files_appended": saved,
        "files_skipped": skipped,
    }

@app.get("/api/files/{file_id}", tags=["uploads"])
def get_file(file_id: int):
    file_record = db_client.get_file_content(file_id)
    if not file_record:
        raise HTTPException(404, "File not found")
    return Response(content=file_record["file_data"], media_type=file_record["content_type"] or "application/octet-stream")


class KGValidationRequest(BaseModel):
    tracking_id: str
    scenario_id: str = ""
    domain: str = ""
    use_case: str = ""
    snapshot: dict = {}


@app.get("/api/validation/contexts", tags=["validation"])
def validation_contexts(limit: int = Query(100, ge=1, le=500)):
    """List persisted domain/use-case/scenario/upload combinations."""
    contexts = db_client.get_validation_contexts(limit=limit)
    history = db_client.list_validation_runs(limit=200)
    latest = {}
    for run in history:
        key = (run.get("tracking_id") or "", run.get("scenario_id") or "")
        if key not in latest:
            latest[key] = {
                "run_id": run.get("run_id"),
                "overall_score": run.get("overall_score"),
                "overall_zone": run.get("overall_zone"),
                "started_at": run.get("started_at"),
            }
    for context in contexts:
        key = (
            context.get("tracking_id") or "",
            context.get("scenario_tracking_id") or "",
        )
        context["latest_validation"] = latest.get(key)
    return {"contexts": contexts}


@app.post("/api/validation/runs", tags=["validation"])
def execute_validation(req: KGValidationRequest):
    """Execute and persist all eight evidence-first validation layers."""
    session = db_client.get_session(req.tracking_id)
    if not session:
        raise HTTPException(status_code=404, detail="Upload tracking ID not found")
    supplied = {
        "tracking_id": req.tracking_id,
        "scenario_id": req.scenario_id,
        "domain": req.domain,
        "use_case": req.use_case,
    }
    try:
        authoritative = resolve_validation_context(session, supplied)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
    previous = db_client.get_previous_validation_run(
        authoritative["tracking_id"], authoritative["scenario_id"]
    )
    files = db_client.get_files_for_session(req.tracking_id)
    result = run_kg_validation(authoritative, req.snapshot, files, previous)
    run_id = f"KGV-{uuid.uuid4().hex[:12].upper()}"
    return db_client.save_validation_run(run_id, result)


@app.get("/api/validation/runs", tags=["validation"])
def validation_history(
    limit: int = Query(25, ge=1, le=200),
    tracking_id: str = "",
    scenario_id: str = "",
    domain: str = "",
    use_case: str = "",
):
    return {
        "runs": db_client.list_validation_runs(
            limit=limit,
            tracking_id=tracking_id,
            scenario_id=scenario_id,
            domain=domain,
            use_case=use_case,
        )
    }


@app.get("/api/validation/runs/{run_id}", tags=["validation"])
def validation_run(run_id: str):
    payload = db_client.get_validation_run(run_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Validation run not found")
    return payload


@app.delete("/api/validation/runs/{run_id}", tags=["validation"])
def delete_validation_run(run_id: str):
    if not db_client.delete_validation_run(run_id):
        raise HTTPException(status_code=404, detail="Validation run not found")
    return {"status": "deleted", "run_id": run_id}


@app.get("/api/validation/runs/{run_id}/export", tags=["validation"])
def export_validation_run(run_id: str, format: str = Query("json", pattern="^(json|csv)$")):
    payload = db_client.get_validation_run(run_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Validation run not found")
    filename = f"kg_validation_{run_id}.{format}"
    if format == "json":
        return Response(
            content=json.dumps(payload, indent=2, default=str),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    return Response(
        content=validation_csv(payload),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/domain/configure", tags=["configuration"])
def configure_domain(req: DomainConfiguratorRequest):
    """Build an authoritative, AI-assisted context for the full GRAPHEN journey."""
    payload = build_domain_configuration(req)
    if not req.skip_llm:
        payload = enrich_domain_configuration_with_llm(payload, req)
    return payload


@app.post("/api/domain/trending-use-cases", tags=["configuration"])
def trending_domain_use_cases(req: TrendingUseCasesRequest):
    """Return five dynamically ranked trending use cases for an industry."""
    payload = build_trending_use_cases(req)
    if not req.skip_llm:
        payload = enrich_trending_use_cases_with_llm(payload, req)
    return payload


@app.post("/api/schema/registry", tags=["configuration"])
def schema_registry(req: SchemaRegistryRequest):
    """Return domain/use-case entity and relationship guidelines before upload."""
    payload = build_schema_registry(req)
    if not req.skip_llm:
        payload = enrich_schema_registry_with_llm(payload, req)
    return payload


@app.post("/api/next-ai/status", tags=["ai"])
def next_ai_status(req: NextAIContextRequest):
    """Prepare the active uploaded-session hybrid RAG index and dynamic chatbot context."""
    return build_next_ai_status(req, db_client)


@app.post("/api/next-ai/ask", tags=["ai"])
def next_ai_ask(req: NextAIAskRequest):
    """Answer from session-scoped semantic and graph retrieval, with guarded fallback."""
    return answer_next_ai(req, db_client)


# ── Interactive Graph: LLM use-case tabs ───────────────────────────────────────

class GraphTabsRequest(BaseModel):
    tabular_files: List[str] = []
    document_files: List[str] = []
    image_files: List[str] = []
    audio_files: List[str] = []
    text_files: List[str] = []
    hint: str = ""
    industry: str = ""
    use_case: str = ""


def _modality_tabs(req: GraphTabsRequest) -> list[dict]:
    """Always-on filters driven by what was actually uploaded (not fixed CSV/PDF labels)."""
    tabs: list[dict] = [
        {"id": "all", "label": "All", "filter": "all", "emphasis": False, "icon": None},
    ]
    if req.tabular_files:
        tabs.append({
            "id": "tabular",
            "label": f"Tabular ({len(req.tabular_files)})",
            "filter": "modality:tabular",
            "emphasis": False,
            "icon": None,
        })
    if req.document_files or req.text_files:
        n = len(req.document_files) + len(req.text_files)
        tabs.append({
            "id": "documents",
            "label": f"Documents ({n})",
            "filter": "modality:document",
            "emphasis": False,
            "icon": None,
        })
    if req.image_files:
        tabs.append({
            "id": "images",
            "label": f"Images ({len(req.image_files)})",
            "filter": "modality:image",
            "emphasis": False,
            "icon": None,
        })
    if req.audio_files:
        tabs.append({
            "id": "audio",
            "label": f"Audio ({len(req.audio_files)})",
            "filter": "modality:audio",
            "emphasis": False,
            "icon": None,
        })
    # Cross-source only when ≥2 modalities present
    modalities = sum([
        1 if req.tabular_files else 0,
        1 if (req.document_files or req.text_files) else 0,
        1 if req.image_files else 0,
        1 if req.audio_files else 0,
    ])
    if modalities >= 2:
        tabs.append({
            "id": "cross",
            "label": "Cross-Source",
            "filter": "cross_source",
            "emphasis": False,
            "icon": None,
        })
    return tabs


def _heuristic_graph_tabs(req: GraphTabsRequest) -> dict:
    """Industry / use-case tabs when LLM is unavailable — never hardcodes AML for non-finance."""
    names = " ".join(
        req.tabular_files + req.document_files + req.image_files + req.audio_files
        + req.text_files + [req.hint, req.industry, req.use_case]
    ).lower()

    industry = "General"
    use_case = "Multi-source Knowledge Graph"
    pattern_tabs: list[dict] = []
    alert_label = "Risk patterns"
    legend = [
        {"key": "Individual", "color": "#4C8DFF", "dashed": False},
        {"key": "Organisation", "color": "#F5A623", "dashed": False},
        {"key": "Account / Record", "color": "#27D199", "dashed": False},
        {"key": "Evidence (doc)", "color": "#EAB308", "dashed": True},
        {"key": "Image / Audio", "color": "#2DD4D4", "dashed": True},
    ]

    finance_kw = ("aml", "sanction", "ofac", "pmla", "kyc", "bank", "txn", "transaction",
                  "account", "swift", "str", "laundering", "payment", "ds1", "ds4", "hdfc", "rbi")
    health_kw = ("health", "hospital", "patient", "clinical", "phi", "hipaa", "claim", "provider",
                 "diagnosis", "ehr", "medical", "pharma", "referral")
    lease_kw = ("lease", "tenant", "property", "rent", "sqft", "renewal", "landlord", "cbre", "portfolio")
    supply_kw = ("supplier", "shipment", "invoice", "procurement", "sku", "warehouse",
                 "logistics", "manufacturing", "supply chain", "digital twin", "component")
    telecom_kw = ("telecom", "telecommunication", "subscriber", "sim", "network element",
                  "churn", "fault propagation", "3gpp")
    retail_kw = ("retail", "e-commerce", "ecommerce", "product catalog", "recommendation",
                 "shopping", "order", "inventory", "customer 360")
    hr_kw = ("employee", "payroll", "hr ", "resume", "cv_", "onboarding", "timesheet")
    cyber_kw = ("malware", "siem", "ioc", "threat", "firewall", "cve", "incident", "soc")

    if any(k in names for k in health_kw):
        industry, use_case = "Healthcare", "Healthcare claims & care-network intelligence"
        alert_label = "Referral / PHI flags"
        pattern_tabs = [
            {"id": "referral_ring", "label": "Referral Ring", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
            {"id": "phi_risk", "label": "PHI Exposure", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]
        legend = [
            {"key": "Patient", "color": "#4C8DFF", "dashed": False},
            {"key": "Provider", "color": "#F5A623", "dashed": False},
            {"key": "Claim", "color": "#27D199", "dashed": False},
            {"key": "Clinical doc", "color": "#EAB308", "dashed": True},
            {"key": "Imaging / Audio", "color": "#2DD4D4", "dashed": True},
        ]
    elif any(k in names for k in finance_kw):
        industry, use_case = "Financial Crime / AML", "AML investigation knowledge graph"
        alert_label = "AML alerts"
        pattern_tabs = [
            {"id": "aml_ring", "label": "AML Ring", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
            {"id": "sanctions", "label": "Sanctions Path", "filter": "pattern:sanctions",
             "emphasis": True, "icon": "warning"},
        ]
        legend = [
            {"key": "Individual", "color": "#4C8DFF", "dashed": False},
            {"key": "Company", "color": "#F5A623", "dashed": False},
            {"key": "Account", "color": "#27D199", "dashed": False},
            {"key": "Sanctioned", "color": "#FB5A6A", "dashed": False},
            {"key": "Device", "color": "#9B7CF6", "dashed": False},
            {"key": "Regulation (doc)", "color": "#EAB308", "dashed": True},
            {"key": "Policy (doc)", "color": "#2DD4D4", "dashed": True},
        ]
    elif any(k in names for k in lease_kw):
        industry, use_case = "Real Estate / Lease", "Lease & portfolio knowledge graph"
        alert_label = "Lease risk flags"
        pattern_tabs = [
            {"id": "concentration", "label": "Tenant Concentration", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
            {"id": "expiry_cluster", "label": "Expiry Cluster", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
        ]
        legend = [
            {"key": "Property", "color": "#4C8DFF", "dashed": False},
            {"key": "Tenant", "color": "#27D199", "dashed": False},
            {"key": "Lease", "color": "#9B7CF6", "dashed": False},
            {"key": "Clause (doc)", "color": "#FB5A6A", "dashed": True},
            {"key": "Site image / Audio", "color": "#2DD4D4", "dashed": True},
        ]
    elif any(k in names for k in supply_kw):
        industry, use_case = "Supply Chain", "Procurement & logistics knowledge graph"
        alert_label = "Supply risk flags"
        pattern_tabs = [
            {"id": "invoice_loop", "label": "Invoice Loop", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
            {"id": "vendor_risk", "label": "Vendor Risk", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]
    elif any(k in names for k in telecom_kw):
        industry, use_case = "Telecommunications", "Telecommunications network intelligence"
        alert_label = "Network / subscriber signals"
        pattern_tabs = [
            {"id": "network_path", "label": "Network Path", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
            {"id": "subscriber_signal", "label": "Subscriber Signals", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]
    elif any(k in names for k in retail_kw):
        industry, use_case = "Retail & E-Commerce", "Customer and product intelligence"
        alert_label = "Customer / product signals"
        pattern_tabs = [
            {"id": "product_affinity", "label": "Product Affinity", "filter": "pattern:custom",
             "emphasis": True, "icon": None},
            {"id": "customer_signal", "label": "Customer Signals", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]
    elif any(k in names for k in hr_kw):
        industry, use_case = "Human Resources", "Workforce & identity knowledge graph"
        alert_label = "HR anomaly flags"
        pattern_tabs = [
            {"id": "identity_overlap", "label": "Identity Overlap", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
        ]
    elif any(k in names for k in cyber_kw):
        industry, use_case = "Cybersecurity", "Threat & incident knowledge graph"
        alert_label = "Threat patterns"
        pattern_tabs = [
            {"id": "lateral_path", "label": "Lateral Path", "filter": "pattern:ring",
             "emphasis": True, "icon": "warning"},
            {"id": "ioc_hits", "label": "IOC Hits", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]
    else:
        # Generic investigation — still no AML-specific tab
        pattern_tabs = [
            {"id": "risk_cluster", "label": "Risk Cluster", "filter": "pattern:alerts",
             "emphasis": True, "icon": "warning"},
        ]

    if req.industry.strip():
        industry = req.industry.strip()[:80]
    if req.use_case.strip():
        use_case = req.use_case.strip()[:120]
    tabs = _modality_tabs(req) + pattern_tabs
    return {
        "use_case": use_case,
        "industry": industry,
        "confidence": 0.72,
        "rationale": "Heuristic classification from uploaded filenames and modalities (LLM fallback).",
        "source": "heuristic",
        "alert_label": alert_label,
        "tabs": tabs,
        "legend": legend,
    }


@app.post("/api/graph/tabs", tags=["graph"])
def graph_use_case_tabs(req: GraphTabsRequest):
    """
    LLM identifies industry / use-case and returns Interactive Graph filter tabs.
    Modality tabs (Tabular / Documents / Images / Audio) are driven by uploads.
    Pattern tabs (e.g. AML Ring vs Referral Ring) depend on detected use case.
    """
    fallback = _heuristic_graph_tabs(req)
    all_names = (
        req.tabular_files + req.document_files + req.image_files
        + req.audio_files + req.text_files
    )
    if not all_names and not req.hint.strip():
        # Keep the empty state neutral or use the explicit configured domain.
        out = fallback
        out["source"] = "configured_empty_state" if (req.industry or req.use_case) else "empty_state"
        out["demo"] = True
        return out

    system = (
        "You are GRAPHEN's ontology analyst. Given uploaded file names and modalities, "
        "identify the industry and investigation use-case. Return STRICT JSON only with keys:\n"
        "use_case (string), industry (string), confidence (0-1), rationale (short string),\n"
        "alert_label (short string for badge),\n"
        "pattern_tabs (array of {id, label, filter, emphasis, icon}),\n"
        "legend (array of {key, color, dashed}).\n"
        "Rules:\n"
        "- filter must be one of: pattern:ring | pattern:alerts | pattern:sanctions | pattern:custom\n"
        "- emphasis true for risk/warning tabs; icon 'warning' or null\n"
        "- NEVER suggest AML / sanctions / laundering tabs unless the data clearly indicates "
        "banking, payments, KYC, sanctions, or financial crime.\n"
        "- For Healthcare use Referral Ring / PHI Exposure / Claims Anomaly — not AML Ring.\n"
        "- For Real Estate use Tenant Concentration / Expiry Cluster — not AML Ring.\n"
        "- For Supply Chain use Invoice Loop / Vendor Risk.\n"
        "- For Telecommunications use Network Path / Subscriber Signals / Fault Propagation.\n"
        "- For Retail & E-Commerce use Product Affinity / Customer Signals / Inventory Dependencies.\n"
        "- The explicitly selected industry and use case are authoritative; do not replace them.\n"
        "- Provide 1-3 pattern_tabs max, tailored to the use case.\n"
        "- legend colors should be hex; dashed true for unstructured evidence types.\n"
    )
    user = (
        f"Hint: {req.hint or '(none)'}\n"
        f"Selected industry: {req.industry or '(none)'}\n"
        f"Selected use case: {req.use_case or '(none)'}\n"
        f"Tabular: {req.tabular_files}\n"
        f"Documents: {req.document_files}\n"
        f"Text: {req.text_files}\n"
        f"Images: {req.image_files}\n"
        f"Audio: {req.audio_files}\n"
    )
    try:
        from leaseguard.llm.llm_client import LLMClient
        parsed = LLMClient().extract_json(system, user)
        if not parsed or not isinstance(parsed, dict):
            return fallback
        pattern_tabs = parsed.get("pattern_tabs") or []
        clean_patterns = []
        for t in pattern_tabs[:3]:
            if not isinstance(t, dict) or not t.get("label"):
                continue
            fid = str(t.get("id") or t["label"]).lower().replace(" ", "_")[:40]
            fltr = str(t.get("filter") or "pattern:alerts")
            if not fltr.startswith("pattern:"):
                fltr = "pattern:alerts"
            clean_patterns.append({
                "id": fid,
                "label": str(t["label"])[:48],
                "filter": fltr,
                "emphasis": bool(t.get("emphasis", True)),
                "icon": t.get("icon") if t.get("icon") in (None, "warning") else "warning",
            })
        if not clean_patterns:
            clean_patterns = fallback["tabs"][len(_modality_tabs(req)):]

        legend = parsed.get("legend") if isinstance(parsed.get("legend"), list) else fallback["legend"]
        # Sanitize legend entries
        clean_legend = []
        for item in legend[:8]:
            if not isinstance(item, dict) or not item.get("key"):
                continue
            clean_legend.append({
                "key": str(item["key"])[:40],
                "color": str(item.get("color") or "#4C8DFF")[:16],
                "dashed": bool(item.get("dashed", False)),
            })
        if not clean_legend:
            clean_legend = fallback["legend"]

        return {
            "use_case": str(req.use_case or parsed.get("use_case") or fallback["use_case"])[:120],
            "industry": str(req.industry or parsed.get("industry") or fallback["industry"])[:80],
            "confidence": float(parsed.get("confidence") or 0.8),
            "rationale": str(parsed.get("rationale") or "")[:400],
            "source": "llm",
            "alert_label": str(parsed.get("alert_label") or fallback["alert_label"])[:40],
            "tabs": _modality_tabs(req) + clean_patterns,
            "legend": clean_legend,
            "demo": False,
        }
    except Exception as exc:
        logger.warning(f"graph tabs LLM failed, using heuristic: {exc}")
        fallback["rationale"] = f"LLM unavailable ({exc}); heuristic used."
        return fallback


@app.post("/api/cypher/detections", tags=["cypher"])
def cypher_detection_scenarios(req: CypherDetectionsRequest):
    """
    Dynamic Cypher detection scenarios from uploaded files + use case.
    Returns raw dataset previews (day-1, no flags) and step-by-step traversals.
    """
    payload = build_cypher_detections(req, db_client)
    if not req.skip_llm:
        try:
            payload = enrich_with_llm(payload, req)
            payload = refresh_raw_datasets_for_payload(payload, req, db_client)
        except Exception as exc:
            logger.warning(f"cypher detections LLM skipped: {exc}")
    return payload


@app.post("/api/crossdoc/discover", tags=["cross-document"])
def cross_document_discoveries(req: CrossDocDiscoveryRequest):
    """
    Generate evidence-grounded, requirement-specific findings across uploaded
    sources. A fast candidate pass is available with skip_llm; the full pass
    uses the configured LLM and falls back safely if it is unavailable.
    """
    payload = build_crossdoc_payload(req, db_client)
    if not req.skip_llm:
        payload = enrich_crossdoc_with_llm(payload, req, db_client)
    return payload


@app.post("/api/intelligence/report", tags=["outcome"])
def intelligence_report(req: IntelligenceReportRequest):
    """Create a user-specific report from prior findings and session evidence."""
    payload = build_intelligence_report(req, db_client)
    if not req.skip_llm:
        payload = enrich_intelligence_report_with_llm(payload, req, db_client)
    return payload


@app.post("/api/intelligence/report/summarize", tags=["outcome"])
def summarize_intelligence_report(req: IntelligenceReportSummaryRequest):
    """Return a concise top-five action summary of the intelligence report."""
    payload = build_intelligence_report_summary(req.report)
    if not req.skip_llm:
        payload = enrich_intelligence_report_summary_with_llm(payload, req.report)
    return payload


@app.post("/api/final-report", tags=["outcome"])
def final_executive_report(req: FinalReportRequest):
    """Create a board-quality action report from all prior pipeline outcomes."""
    payload = build_final_report(req, db_client)
    if not req.skip_llm:
        payload = enrich_final_report_with_llm(payload, req, db_client)
    return payload


@app.post("/api/final-report/summarize", tags=["outcome"])
def summarize_final_executive_report(req: FinalReportSummaryRequest):
    """Return a deduplicated top-five action brief for executive consumption."""
    payload = build_final_report_summary(req.report)
    if not req.skip_llm:
        payload = enrich_final_report_summary_with_llm(payload, req.report)
    return payload

