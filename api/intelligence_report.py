"""User-specific intelligence reports synthesized from prior pipeline outcomes."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field

from api.crossdoc_discovery import (
    CrossDocDiscoveryRequest,
    _candidate_findings,
    _clean_text,
    _collect_sources,
)
from api.cypher_detections import _infer_industry


class IntelligenceReportRequest(CrossDocDiscoveryRequest):
    prior_findings: list[dict[str, Any]] = Field(default_factory=list)
    detection_results: list[dict[str, Any]] = Field(default_factory=list)


class IntelligenceReportSummaryRequest(BaseModel):
    report: dict[str, Any] = Field(default_factory=dict)
    skip_llm: bool = False


def _summary_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def build_intelligence_report_summary(report: dict[str, Any]) -> dict:
    candidates: list[dict] = []
    for item in report.get("recommended_actions") or []:
        candidates.append({
            "action": _clean_text(item.get("action"), 240),
            "owner": _clean_text(item.get("owner"), 100) or "Business Owner",
            "timing": _clean_text(item.get("timeframe"), 100) or "Next review cycle",
            "reason": _clean_text(item.get("rationale"), 260),
        })
    for item in report.get("priority_insights") or []:
        priority = _severity(item.get("priority"))
        title = _clean_text(item.get("title"), 170)
        action = (
            f"Escalate and validate: {title}"
            if priority in {"critical", "high"}
            else f"Validate and resolve: {title}"
        )
        candidates.append({
            "action": _clean_text(action, 240),
            "owner": "Investigation Lead" if priority in {"critical", "high"} else "Domain Analyst",
            "timing": "Immediate review" if priority == "critical" else "Next review cycle",
            "reason": _clean_text(item.get("implication"), 260),
        })
    brief = report.get("decision_brief") or {}
    if brief.get("decision_needed"):
        candidates.append({
            "action": _clean_text(brief.get("decision_needed"), 240),
            "owner": "Executive Sponsor",
            "timing": "Before final approval",
            "reason": _clean_text(brief.get("assessment"), 260),
        })
    actions = []
    seen: set[str] = set()
    for item in candidates:
        key = _summary_key(item["action"])
        if not key or key in seen:
            continue
        seen.add(key)
        actions.append({"rank": len(actions) + 1, **item})
        if len(actions) == 5:
            break
    return {
        "source": "deterministic",
        "title": "Five Priority Actions",
        "intro": (
            "A concise leadership view of the actions supported by this intelligence report, "
            "ordered to minimize further analysis."
        ),
        "actions": actions,
    }


def enrich_intelligence_report_summary_with_llm(payload: dict, report: dict[str, Any]) -> dict:
    system = (
        "You are an executive intelligence editor. Return STRICT JSON only with title, intro, "
        "actions. Produce no more than five distinct, precise actions from the supplied report. "
        "Merge duplicates and do not invent facts, deadlines, owners, or obligations. Each action "
        "must have rank, action, owner, timing, reason. Keep each action under 24 words and use "
        "plain language for non-technical leaders. Provide no markdown."
    )
    user = json.dumps({
        "executive_summary": report.get("executive_summary"),
        "decision_brief": report.get("decision_brief"),
        "priority_insights": report.get("priority_insights"),
        "recommended_actions": report.get("recommended_actions"),
        "baseline_summary": payload,
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        actions = []
        seen: set[str] = set()
        for item in parsed.get("actions") or []:
            if not isinstance(item, dict):
                continue
            action = _clean_text(item.get("action"), 240)
            key = _summary_key(action)
            if not key or key in seen:
                continue
            seen.add(key)
            actions.append({
                "rank": len(actions) + 1,
                "action": action,
                "owner": _clean_text(item.get("owner"), 100),
                "timing": _clean_text(item.get("timing"), 100),
                "reason": _clean_text(item.get("reason"), 260),
            })
            if len(actions) == 5:
                break
        if actions:
            payload["actions"] = actions
            payload["title"] = _clean_text(parsed.get("title"), 120) or payload["title"]
            payload["intro"] = _clean_text(parsed.get("intro"), 420) or payload["intro"]
            payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Intelligence summary LLM failed: {exc}")
    return payload


def _severity(value: Any) -> str:
    severity = str(value or "review").lower()
    return severity if severity in {"critical", "high", "medium", "review"} else "review"


def _confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.5


def _clean_prior_findings(req: IntelligenceReportRequest, sources: list[dict]) -> list[dict]:
    known = {source["filename"]: source["modality"] for source in sources}
    cleaned: list[dict] = []
    for index, finding in enumerate(req.prior_findings[:8]):
        if not isinstance(finding, dict):
            continue
        finding_sources = []
        for source in finding.get("sources") or []:
            if not isinstance(source, dict):
                continue
            filename = str(source.get("filename") or "")
            if filename in known:
                finding_sources.append({"filename": filename, "modality": known[filename]})
        cleaned.append({
            "id": str(finding.get("id") or f"prior_{index + 1}")[:60],
            "title": _clean_text(finding.get("title"), 160),
            "summary": _clean_text(finding.get("summary"), 900),
            "business_impact": _clean_text(finding.get("business_impact"), 700),
            "severity": _severity(finding.get("severity")),
            "confidence": _confidence(finding.get("confidence")),
            "sources": finding_sources,
            "evidence": _clean_text(finding.get("evidence"), 900),
        })
    return cleaned


def _priority_insights(findings: list[dict], requirement: str) -> list[dict]:
    severity_order = {"critical": 0, "high": 1, "medium": 2, "review": 3}
    ordered = sorted(
        findings,
        key=lambda finding: (
            severity_order[_severity(finding.get("severity"))],
            -_confidence(finding.get("confidence")),
        ),
    )
    insights = []
    for index, finding in enumerate(ordered[:6]):
        severity = _severity(finding.get("severity"))
        sources = [
            source.get("filename") for source in finding.get("sources") or []
            if source.get("filename")
        ]
        if severity in {"critical", "high"}:
            action = "Escalate for owner review and validate the connected evidence before the next decision cycle."
        elif severity == "medium":
            action = "Assign an analyst to test the relationship and record corroborating or contradictory evidence."
        else:
            action = "Retain as a validation candidate and collect stronger evidence before treating it as confirmed."
        insights.append({
            "id": str(finding.get("id") or f"insight_{index + 1}")[:60],
            "title": _clean_text(finding.get("title"), 160) or f"Priority insight {index + 1}",
            "priority": severity,
            "confidence": _confidence(finding.get("confidence")),
            "assessment": _clean_text(finding.get("summary"), 900),
            "implication": _clean_text(finding.get("business_impact"), 700)
            or f"Potential impact on {requirement}.",
            "evidence": _clean_text(finding.get("evidence"), 900),
            "evidence_sources": sources,
            "recommended_response": action,
        })
    return insights


def _recommended_actions(insights: list[dict], requirement: str) -> list[dict]:
    actions = []
    for index, insight in enumerate(insights[:5]):
        priority = insight["priority"]
        actions.append({
            "priority": index + 1,
            "action": insight["recommended_response"],
            "owner": "Investigation Lead" if priority in {"critical", "high"} else "Domain Analyst",
            "timeframe": "Immediate" if priority == "critical" else (
                "Within 5 business days" if priority == "high" else "Next review cycle"
            ),
            "rationale": _clean_text(insight.get("implication"), 500)
            or f"Supports the active requirement: {requirement}.",
            "linked_insight_id": insight["id"],
        })
    if not actions:
        actions.append({
            "priority": 1,
            "action": "Add or connect more user evidence before making an intelligence decision.",
            "owner": "Report Owner",
            "timeframe": "Before approval",
            "rationale": "No sufficiently grounded cross-source finding is available yet.",
            "linked_insight_id": "",
        })
    return actions


def build_intelligence_report(
    req: IntelligenceReportRequest,
    db_client=None,
) -> dict:
    sources = _collect_sources(req, db_client)
    names_blob = " ".join(
        [source["filename"] for source in sources]
        + [req.requirement, req.industry or "", req.use_case or ""]
    ).lower()
    inferred_industry, inferred_use_case = _infer_industry(names_blob)
    industry = req.industry or inferred_industry
    use_case = req.use_case or inferred_use_case
    requirement = req.requirement or use_case
    findings = _clean_prior_findings(req, sources) or _candidate_findings(sources, requirement)
    insights = _priority_insights(findings, requirement)

    modalities = Counter(source["modality"] for source in sources)
    high_priority = sum(
        1 for insight in insights if insight["priority"] in {"critical", "high"}
    )
    completed_detections = sum(
        1 for result in req.detection_results
        if str(result.get("status") or "").lower() == "complete"
    )
    evidence_matrix = []
    for source in sources[:20]:
        supported = [
            insight["id"] for insight in insights
            if source["filename"] in insight.get("evidence_sources", [])
        ]
        evidence_matrix.append({
            "filename": source["filename"],
            "modality": source["modality"],
            "role": "Corroborating evidence" if supported else "Context / validation source",
            "insights_supported": supported,
        })

    return {
        "source": "evidence_summary",
        "industry": industry,
        "use_case": use_case,
        "requirement": requirement,
        "phase_label": "Step 9 of 10 - Intelligence Report",
        "title": f"{use_case} Intelligence Report",
        "subtitle": (
            f"A decision-ready synthesis built specifically from this user's {len(sources)} "
            f"source(s), {len(findings)} prior finding(s), and {completed_detections} completed detection(s)."
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "executive_summary": (
            f"The current {industry} evidence supports {len(insights)} prioritized intelligence "
            f"insight(s) for {requirement}. {high_priority} item(s) require elevated attention. "
            "Conclusions remain bounded by the uploaded evidence and completed graph traversals."
        ),
        "report_metrics": [
            {"label": "Sources assessed", "value": len(sources), "detail": f"{len(modalities)} modalities"},
            {"label": "Priority insights", "value": len(insights), "detail": f"{high_priority} elevated"},
            {"label": "Detections completed", "value": completed_detections, "detail": "Cypher outcomes"},
            {"label": "Evidence coverage", "value": f"{len(evidence_matrix)}/{len(sources)}", "detail": "sources mapped"},
        ],
        "decision_brief": {
            "situation": f"Evidence was evaluated for {requirement} across the active {industry} workflow.",
            "assessment": (
                f"{len(insights)} cross-source or graph-supported insight(s) were prioritized "
                "according to evidence strength and potential business impact."
            ),
            "decision_needed": (
                "Approve the recommended validation and escalation actions, or record why an "
                "identified intelligence gap is accepted."
            ),
        },
        "priority_insights": insights,
        "evidence_matrix": evidence_matrix,
        "recommended_actions": _recommended_actions(insights, requirement),
        "methodology": [
            f"Scoped the report to the user's active requirement: {requirement}.",
            f"Compared {len(sources)} uploaded source(s) across {', '.join(sorted(modalities)) or 'available'} evidence.",
            "Carried forward prior cross-document findings and completed Cypher outcomes.",
            "Ranked insights by severity, confidence, source support, and decision impact.",
        ],
        "limitations": (
            "This report is an evidence-grounded intelligence aid, not a confirmed adjudication. "
            "Items marked for review require human validation; missing or inaccessible sources can change conclusions."
        ),
    }


def enrich_intelligence_report_with_llm(
    payload: dict,
    req: IntelligenceReportRequest,
    db_client=None,
) -> dict:
    sources = _collect_sources(req, db_client)
    if not sources:
        return payload
    source_context = [{
        "filename": source["filename"],
        "modality": source["modality"],
        "identifiers": source["identifiers"][:12],
        "excerpt": source["excerpt"][:1200],
    } for source in sources[:18]]
    system = (
        "You are an intelligence-report editor. Return STRICT JSON only. Build a concise, "
        "decision-ready report specific to the supplied user requirement and evidence. Never "
        "reuse a fixed industry template. Do not invent entities, events, risks, regulations, "
        "or conclusions absent from the supplied evidence and prior findings. Weak evidence "
        "must be framed as a validation candidate. Return keys: title, subtitle, "
        "executive_summary, decision_brief, priority_insights, recommended_actions, limitations. "
        "decision_brief keys: situation, assessment, decision_needed. priority_insights must "
        "contain 1..6 objects with keys: id, title, priority "
        "(critical|high|medium|review), confidence (0..1), assessment, implication, evidence, "
        "evidence_sources (array of exact filenames), recommended_response. "
        "recommended_actions must contain 1..6 objects with keys: priority (integer), action, "
        "owner, timeframe, rationale, linked_insight_id."
    )
    user = json.dumps({
        "industry": payload["industry"],
        "use_case": payload["use_case"],
        "requirement": payload["requirement"],
        "sources": source_context,
        "prior_findings": req.prior_findings[:8],
        "detection_results": req.detection_results[:8],
        "baseline_report": {
            "decision_brief": payload["decision_brief"],
            "priority_insights": payload["priority_insights"],
            "recommended_actions": payload["recommended_actions"],
        },
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        known_sources = {source["filename"] for source in sources}
        clean_insights = []
        for index, item in enumerate(parsed.get("priority_insights") or []):
            if not isinstance(item, dict):
                continue
            evidence_sources = [
                str(filename) for filename in item.get("evidence_sources") or []
                if str(filename) in known_sources
            ]
            clean_insights.append({
                "id": _clean_text(item.get("id"), 60) or f"insight_{index + 1}",
                "title": _clean_text(item.get("title"), 160),
                "priority": _severity(item.get("priority")),
                "confidence": _confidence(item.get("confidence")),
                "assessment": _clean_text(item.get("assessment"), 900),
                "implication": _clean_text(item.get("implication"), 700),
                "evidence": _clean_text(item.get("evidence"), 900),
                "evidence_sources": evidence_sources,
                "recommended_response": _clean_text(item.get("recommended_response"), 700),
            })
        if clean_insights:
            payload["priority_insights"] = clean_insights[:6]

        clean_actions = []
        for index, item in enumerate(parsed.get("recommended_actions") or []):
            if not isinstance(item, dict):
                continue
            clean_actions.append({
                "priority": index + 1,
                "action": _clean_text(item.get("action"), 600),
                "owner": _clean_text(item.get("owner"), 100),
                "timeframe": _clean_text(item.get("timeframe"), 100),
                "rationale": _clean_text(item.get("rationale"), 500),
                "linked_insight_id": _clean_text(item.get("linked_insight_id"), 60),
            })
        if clean_actions:
            payload["recommended_actions"] = clean_actions[:6]

        brief = parsed.get("decision_brief")
        if isinstance(brief, dict):
            payload["decision_brief"] = {
                "situation": _clean_text(brief.get("situation"), 700),
                "assessment": _clean_text(brief.get("assessment"), 700),
                "decision_needed": _clean_text(brief.get("decision_needed"), 700),
            }
        payload["title"] = _clean_text(parsed.get("title"), 180) or payload["title"]
        payload["subtitle"] = _clean_text(parsed.get("subtitle"), 400) or payload["subtitle"]
        payload["executive_summary"] = (
            _clean_text(parsed.get("executive_summary"), 1800) or payload["executive_summary"]
        )
        payload["limitations"] = _clean_text(parsed.get("limitations"), 1000) or payload["limitations"]
        payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Intelligence report LLM enrichment failed: {exc}")
    return payload
