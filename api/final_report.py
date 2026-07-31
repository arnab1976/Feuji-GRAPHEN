"""Executive final reports derived from the complete user pipeline."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field

from api.crossdoc_discovery import _clean_text, _collect_sources
from api.intelligence_report import (
    IntelligenceReportRequest,
    _confidence,
    _severity,
    build_intelligence_report,
)


class FinalReportRequest(IntelligenceReportRequest):
    intelligence_report: dict[str, Any] = Field(default_factory=dict)


class FinalReportSummaryRequest(BaseModel):
    report: dict[str, Any] = Field(default_factory=dict)
    skip_llm: bool = False


def _action_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def build_final_report_summary(report: dict[str, Any]) -> dict:
    """Produce a concise, deduplicated five-action leadership brief."""
    candidates: list[dict] = []
    for item in report.get("top_action_points") or []:
        candidates.append({
            "action": _clean_text(item.get("action"), 240),
            "owner": _clean_text(item.get("owner"), 100) or "Executive Sponsor",
            "timing": _clean_text(item.get("timeframe"), 100) or "Next review cycle",
            "reason": _clean_text(item.get("rationale"), 260),
        })
    for item in report.get("top_recommendations") or []:
        candidates.append({
            "action": _clean_text(item.get("recommendation"), 240),
            "owner": "Business Owner",
            "timing": "Next review cycle",
            "reason": _clean_text(item.get("why_now"), 260),
        })
    for item in report.get("leadership_decisions") or []:
        candidates.append({
            "action": _clean_text(item.get("decision"), 240),
            "owner": "Executive Leadership",
            "timing": _clean_text(item.get("decision_by"), 100) or "Governance review",
            "reason": _clean_text(item.get("why_it_matters"), 260),
        })
    for item in report.get("obligations") or []:
        if "no explicit obligation" in str(item.get("obligation") or "").lower():
            continue
        candidates.append({
            "action": _clean_text(f"Validate and assign: {item.get('obligation')}", 240),
            "owner": _clean_text(item.get("owner"), 100) or "Legal / Compliance Owner",
            "timing": _clean_text(item.get("trigger_or_due"), 100) or "Before approval",
            "reason": _clean_text(item.get("verification"), 260),
        })
    for item in report.get("way_forward") or []:
        candidates.append({
            "action": _clean_text(item.get("objective"), 240),
            "owner": "Executive Sponsor",
            "timing": _clean_text(item.get("horizon"), 100),
            "reason": _clean_text(item.get("deliverables"), 260),
        })

    actions = []
    seen: set[str] = set()
    for item in candidates:
        key = _action_key(item["action"])
        if not key or key in seen:
            continue
        seen.add(key)
        actions.append({
            "rank": len(actions) + 1,
            **item,
        })
        if len(actions) == 5:
            break
    return {
        "source": "deterministic",
        "title": "Five Actions for Leadership",
        "intro": (
            "These are the five highest-value actions distilled from the complete report. "
            "Execute them in order unless leadership records a different priority."
        ),
        "actions": actions,
    }


def enrich_final_report_summary_with_llm(payload: dict, report: dict[str, Any]) -> dict:
    system = (
        "You are an executive action editor. Return STRICT JSON only with keys title, intro, "
        "actions. Distill the supplied report into no more than five distinct, precise actions "
        "for a non-technical leader. Merge duplicates. Do not invent facts, owners, deadlines, "
        "obligations, or recommendations. Each action must have keys rank, action, owner, timing, "
        "reason. Each action sentence must be direct and no longer than 24 words. Preserve "
        "evidence uncertainty. Provide no markdown."
    )
    user = json.dumps({
        "report_summary": report.get("report_summary"),
        "leadership_decisions": report.get("leadership_decisions"),
        "top_action_points": report.get("top_action_points"),
        "top_recommendations": report.get("top_recommendations"),
        "obligations": report.get("obligations"),
        "way_forward": report.get("way_forward"),
        "baseline_summary": payload,
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        cleaned = []
        seen: set[str] = set()
        for item in parsed.get("actions") or []:
            if not isinstance(item, dict):
                continue
            action = _clean_text(item.get("action"), 240)
            key = _action_key(action)
            if not key or key in seen:
                continue
            seen.add(key)
            cleaned.append({
                "rank": len(cleaned) + 1,
                "action": action,
                "owner": _clean_text(item.get("owner"), 100),
                "timing": _clean_text(item.get("timing"), 100),
                "reason": _clean_text(item.get("reason"), 260),
            })
            if len(cleaned) == 5:
                break
        if cleaned:
            payload["actions"] = cleaned
            payload["title"] = _clean_text(parsed.get("title"), 120) or payload["title"]
            payload["intro"] = _clean_text(parsed.get("intro"), 420) or payload["intro"]
            payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Final report summary LLM failed: {exc}")
    return payload


def _obligation_candidates(sources: list[dict]) -> list[dict]:
    obligations: list[dict] = []
    pattern = re.compile(
        r"[^.!?]{0,180}\b(must|shall|required to|is required|obligation|within \d+)\b[^.!?]{0,240}[.!?]",
        re.IGNORECASE,
    )
    for source in sources:
        excerpt = str(source.get("excerpt") or "")
        for match in pattern.finditer(excerpt):
            statement = _clean_text(match.group(0), 420)
            if not statement:
                continue
            obligations.append({
                "obligation": statement,
                "source": source["filename"],
                "trigger_or_due": "Confirm trigger and due date in the cited source",
                "owner": "Legal / Compliance Owner",
                "verification": "Validate the exact clause, applicability, and effective date.",
                "status": "Evidence candidate - validation required",
            })
            if len(obligations) >= 6:
                return obligations
    if not obligations:
        obligations.append({
            "obligation": "No explicit obligation was confirmed from the currently extracted evidence.",
            "source": "Current evidence set",
            "trigger_or_due": "Before approving final organizational action",
            "owner": "Legal / Compliance Owner",
            "verification": "Review governing documents and record applicable obligations or a reasoned none-found conclusion.",
            "status": "Open validation requirement",
        })
    return obligations


def _top_actions(intelligence: dict) -> list[dict]:
    actions = []
    seen: set[str] = set()
    for index, action in enumerate((intelligence.get("recommended_actions") or [])[:6]):
        action_text = _clean_text(action.get("action"), 650)
        key = _action_key(action_text)
        if not key or key in seen:
            continue
        seen.add(key)
        actions.append({
            "rank": index + 1,
            "action": action_text,
            "owner": _clean_text(action.get("owner"), 120) or "Executive Sponsor",
            "timeframe": _clean_text(action.get("timeframe"), 120) or "Next review cycle",
            "rationale": _clean_text(action.get("rationale"), 600),
            "success_measure": "Action completed, evidence recorded, and outcome approved by the accountable owner.",
            "status": "Proposed",
        })
    if not actions:
        actions.append({
            "rank": 1,
            "action": "Commission targeted evidence validation before taking a substantive decision.",
            "owner": "Executive Sponsor",
            "timeframe": "Before approval",
            "rationale": "The current pipeline did not produce a sufficiently grounded action.",
            "success_measure": "Evidence gaps are closed or formally accepted with documented rationale.",
            "status": "Proposed",
        })
    return actions


def _dedupe_report_actions(actions: list[Any]) -> list[dict]:
    unique: list[dict] = []
    seen: set[str] = set()
    for item in actions:
        if not isinstance(item, dict):
            continue
        key = _action_key(item.get("action"))
        if not key or key in seen:
            continue
        seen.add(key)
        clean = dict(item)
        clean["rank"] = len(unique) + 1
        unique.append(clean)
        if len(unique) == 6:
            break
    return unique


def _recommendations(intelligence: dict) -> list[dict]:
    recommendations = []
    for index, insight in enumerate((intelligence.get("priority_insights") or [])[:5]):
        priority = _severity(insight.get("priority"))
        recommendations.append({
            "rank": index + 1,
            "recommendation": _clean_text(
                insight.get("recommended_response")
                or f"Validate and respond to {insight.get('title')}",
                650,
            ),
            "why_now": _clean_text(insight.get("implication"), 550),
            "expected_outcome": (
                "A documented decision supported by corroborated evidence and an accountable owner."
            ),
            "priority": priority,
            "confidence": _confidence(insight.get("confidence")),
        })
    return recommendations


def build_final_report(req: FinalReportRequest, db_client=None) -> dict:
    intelligence = req.intelligence_report or build_intelligence_report(req, db_client)
    sources = _collect_sources(req, db_client)
    industry = intelligence.get("industry") or req.industry or "General"
    use_case = intelligence.get("use_case") or req.use_case or "Organizational Intelligence"
    requirement = intelligence.get("requirement") or req.requirement or use_case
    insights = intelligence.get("priority_insights") or []
    elevated = sum(
        1 for insight in insights
        if _severity(insight.get("priority")) in {"critical", "high"}
    )
    actions = _top_actions(intelligence)
    recommendations = _recommendations(intelligence)
    generated_at = datetime.now(timezone.utc)
    report_id = f"GR-{generated_at.strftime('%Y%m%d-%H%M%S')}"

    return {
        "source": "pipeline_summary",
        "phase_label": "Step 10 of 11 - Final Executive Report",
        "report_id": report_id,
        "generated_at": generated_at.isoformat(),
        "classification": "Confidential - Internal Decision Support",
        "industry": industry,
        "use_case": use_case,
        "requirement": requirement,
        "title": f"{use_case} - Executive Action Report",
        "subtitle": (
            "A non-technical, decision-ready report derived from uploaded evidence, "
            "pipeline processing, graph detections, cross-document discovery, and intelligence synthesis."
        ),
        "report_summary": {
            "objective": f"Provide precise organizational actions for: {requirement}.",
            "executive_conclusion": (
                f"The pipeline produced {len(insights)} prioritized insight(s), including "
                f"{elevated} elevated item(s). The proposed response focuses on evidence "
                "validation, accountable ownership, and measurable decision closure."
            ),
            "scope": (
                f"{len(sources)} source(s), {len(req.prior_findings)} cross-document finding(s), "
                f"and {sum(1 for item in req.detection_results if item.get('status') == 'complete')} "
                "completed Cypher detection(s)."
            ),
            "key_message": (
                "Act on validated evidence first; where evidence is incomplete, assign an owner "
                "and close the gap before approving irreversible action."
            ),
        },
        "key_metrics": [
            {"label": "Evidence sources", "value": len(sources)},
            {"label": "Priority insights", "value": len(insights)},
            {"label": "Elevated items", "value": elevated},
            {"label": "Proposed actions", "value": len(actions)},
        ],
        "leadership_decisions": [{
            "decision": "Approve, modify, or reject the proposed action plan and named accountability.",
            "why_it_matters": "Delayed ownership increases the chance that evidence gaps remain unresolved.",
            "decision_by": actions[0].get("timeframe") or "Next governance review",
        }, {
            "decision": "Confirm which evidence candidates may be treated as established facts.",
            "why_it_matters": "This prevents assumptions from being presented as confirmed organizational intelligence.",
            "decision_by": "Before external communication or irreversible action",
        }],
        "top_action_points": actions,
        "top_recommendations": recommendations,
        "obligations": _obligation_candidates(sources),
        "way_forward": [{
            "phase": "Mobilize",
            "horizon": "0-5 business days",
            "objective": "Confirm executive sponsorship, owners, and evidence requiring immediate validation.",
            "deliverables": "Approved action register, named owners, and validation plan.",
            "decision_gate": "Leadership accepts scope and accountability.",
        }, {
            "phase": "Validate and Act",
            "horizon": "5-30 business days",
            "objective": "Validate high-priority evidence and execute approved corrective or investigative actions.",
            "deliverables": "Evidence log, completed actions, obligation assessment, and exception decisions.",
            "decision_gate": "Each elevated item is resolved, mitigated, or formally accepted.",
        }, {
            "phase": "Embed and Monitor",
            "horizon": "30-90 days",
            "objective": "Convert validated lessons into controls, monitoring, and recurring governance.",
            "deliverables": "Updated controls, monitoring indicators, and executive progress review.",
            "decision_gate": "Control effectiveness and residual exposure are accepted.",
        }],
        "evidence_basis": [{
            "filename": source["filename"],
            "modality": source["modality"],
            "role": "Pipeline evidence",
        } for source in sources[:25]],
        "assurance_statement": (
            "The report distinguishes evidence-supported conclusions from validation candidates. "
            "It does not replace legal, regulatory, financial, clinical, or other professional judgment."
        ),
        "sign_off": [
            {"role": "Executive Sponsor", "name": "", "decision": "", "date": ""},
            {"role": "Business Owner", "name": "", "decision": "", "date": ""},
            {"role": "Legal / Compliance Review", "name": "", "decision": "", "date": ""},
        ],
    }


def enrich_final_report_with_llm(
    payload: dict,
    req: FinalReportRequest,
    db_client=None,
) -> dict:
    sources = _collect_sources(req, db_client)
    context = [{
        "filename": source["filename"],
        "modality": source["modality"],
        "excerpt": source["excerpt"][:1400],
    } for source in sources[:18]]
    system = (
        "You are an executive report editor. Return STRICT JSON only. Rewrite the supplied "
        "pipeline report into a board-quality, plain-language action report for non-technical "
        "leaders. Be precise, concise, and evidence bounded. Never invent facts, laws, dates, "
        "obligations, monetary values, entities, or deadlines. An obligation may only be stated "
        "when supported by a named source excerpt; otherwise preserve it as a validation "
        "requirement. Return keys: title, subtitle, report_summary, leadership_decisions, "
        "top_action_points, top_recommendations, obligations, way_forward, assurance_statement. "
        "Preserve these object shapes exactly from baseline_report. Provide no markdown."
    )
    user = json.dumps({
        "industry": payload["industry"],
        "use_case": payload["use_case"],
        "requirement": payload["requirement"],
        "source_evidence": context,
        "cross_document_findings": req.prior_findings[:8],
        "detection_results": req.detection_results[:8],
        "intelligence_report": req.intelligence_report,
        "baseline_report": {
            key: payload[key] for key in (
                "report_summary", "leadership_decisions", "top_action_points",
                "top_recommendations", "obligations", "way_forward",
                "assurance_statement",
            )
        },
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        payload["title"] = _clean_text(parsed.get("title"), 200) or payload["title"]
        payload["subtitle"] = _clean_text(parsed.get("subtitle"), 600) or payload["subtitle"]
        for key in (
            "report_summary", "leadership_decisions", "top_action_points",
            "top_recommendations", "way_forward",
        ):
            value = parsed.get(key)
            if isinstance(value, (dict, list)) and value:
                payload[key] = value
        known_sources = {source["filename"] for source in sources}
        clean_obligations = []
        for item in parsed.get("obligations") or []:
            if not isinstance(item, dict):
                continue
            source = str(item.get("source") or "")
            if source not in known_sources and source != "Current evidence set":
                continue
            clean_obligations.append({
                "obligation": _clean_text(item.get("obligation"), 500),
                "source": source,
                "trigger_or_due": _clean_text(item.get("trigger_or_due"), 220),
                "owner": _clean_text(item.get("owner"), 140),
                "verification": _clean_text(item.get("verification"), 500),
                "status": _clean_text(item.get("status"), 140),
            })
        if clean_obligations:
            payload["obligations"] = clean_obligations[:6]
        payload["top_action_points"] = _dedupe_report_actions(
            payload.get("top_action_points") or []
        )
        payload["assurance_statement"] = (
            _clean_text(parsed.get("assurance_statement"), 1000)
            or payload["assurance_statement"]
        )
        payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Final report LLM enrichment failed: {exc}")
    return payload
