"""AI-assisted domain and use-case configuration for GRAPHEN journeys."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field


INDUSTRY_CONFIG: dict[str, dict[str, Any]] = {
    "Financial Services": {
        "use_cases": ["Financial Crime & AML", "Customer 360", "Credit Risk Intelligence", "KYC & Regulatory Compliance"],
        "entities": ["Customer", "Account", "Transaction", "Company"],
        "relationships": ["OWNS", "TRANSFERRED_TO", "CONNECTED_TO"],
        "standards": ["FIBO", "ISO 20022"],
        "detections": ["transaction rings", "sanctions exposure", "identity overlap"],
    },
    "Healthcare & Life Sciences": {
        "use_cases": ["Patient Journey 360", "Clinical Trial Intelligence", "Drug Safety & Pharmacovigilance", "Provider & Referral Integrity"],
        "entities": ["Patient", "Provider", "Claim", "Product"],
        "relationships": ["TREATED_BY", "HAS_CLAIM", "REFERRED_TO"],
        "standards": ["FHIR", "SNOMED CT"],
        "detections": ["referral loops", "safety signals", "care-path anomalies"],
    },
    "Manufacturing & Supply Chain": {
        "use_cases": ["Digital Twin", "Supplier Risk Intelligence", "Quality & Recall Traceability", "Predictive Maintenance"],
        "entities": ["Product", "Asset", "Supplier", "Component"],
        "relationships": ["CONTAINS", "SOURCED_FROM", "INSTALLED_AT"],
        "standards": ["ISA-95", "ISO 10303 STEP"],
        "detections": ["dependency concentration", "quality propagation", "asset failure paths"],
    },
    "Telecommunications": {
        "use_cases": ["Telecom Fraud", "Fault Propagation", "Customer 360", "Churn Prediction"],
        "entities": ["Subscriber", "Device", "Network Element", "Service"],
        "relationships": ["USES", "CONNECTED_TO", "DEPENDS_ON"],
        "standards": ["TM Forum SID", "3GPP"],
        "detections": ["SIM/device overlap", "network fault paths", "churn signals"],
    },
    "Retail & E-Commerce": {
        "use_cases": ["Product Knowledge Graph", "Personalized Recommendation", "Customer 360", "Inventory & Demand Intelligence"],
        "entities": ["Customer", "Product", "Order", "Location"],
        "relationships": ["PURCHASED", "VIEWED", "FULFILLED_BY"],
        "standards": ["GS1", "schema.org"],
        "detections": ["product affinity", "returns anomalies", "inventory dependency"],
    },
}

TRENDING_USE_CASES: dict[str, list[dict[str, str]]] = {
    "Financial Services": [
        {"title": "Agentic Financial Crime Investigation", "description": "AI-led case triage across transactions, identities, devices, and sanctions.", "icon": "🔎"},
        {"title": "Real-Time Payment Fraud", "description": "Connected payment, beneficiary, device, and mule-account risk signals.", "icon": "⚡"},
        {"title": "Customer 360 & Next Best Action", "description": "Unified customer context for service, retention, and responsible growth.", "icon": "👤"},
        {"title": "Climate & Counterparty Risk", "description": "Graph exposure across borrowers, assets, sectors, and climate events.", "icon": "🌍"},
        {"title": "Continuous KYC & UBO Monitoring", "description": "Dynamic identity, ownership, watchlist, and regulatory change tracking.", "icon": "🛡️"},
        {"title": "Credit Early Warning", "description": "Connected borrower, covenant, collateral, and market deterioration signals.", "icon": "📉"},
        {"title": "Regulatory Obligation Intelligence", "description": "Map policies, controls, evidence, and obligations to accountable owners.", "icon": "📜"},
    ],
    "Healthcare & Life Sciences": [
        {"title": "AI Patient Journey 360", "description": "Connected clinical, claims, medication, provider, and outcome pathways.", "icon": "🩺"},
        {"title": "Clinical Trial Site Intelligence", "description": "Site, investigator, enrollment, protocol, and safety performance graph.", "icon": "🧪"},
        {"title": "Drug Safety Signal Detection", "description": "Adverse events, products, literature, labels, and regulatory signals.", "icon": "💊"},
        {"title": "Provider Network Integrity", "description": "Referral, claim, facility, and provider relationship anomalies.", "icon": "🔗"},
        {"title": "Precision Medicine Knowledge Graph", "description": "Connect phenotype, genomic, treatment, and research evidence.", "icon": "🧬"},
        {"title": "Healthcare Data Interoperability", "description": "FHIR-aligned patient, encounter, observation, and terminology links.", "icon": "🏥"},
        {"title": "Medical Supply Resilience", "description": "Product, supplier, facility, inventory, and shortage dependencies.", "icon": "📦"},
    ],
    "Manufacturing & Supply Chain": [
        {"title": "Industrial Digital Twin", "description": "Connected products, assets, assemblies, components, and operating context.", "icon": "🏗️"},
        {"title": "Multi-Tier Supplier Resilience", "description": "Hidden supplier dependencies, disruption paths, and concentration risk.", "icon": "🚚"},
        {"title": "Quality & Recall Traceability", "description": "Defect propagation from supplier and batch through customer shipment.", "icon": "✅"},
        {"title": "Predictive Asset Maintenance", "description": "Asset, sensor, failure, work-order, part, and procedure relationships.", "icon": "⚙️"},
        {"title": "Supply Chain Control Tower", "description": "Orders, shipments, inventory, suppliers, and disruption event intelligence.", "icon": "🎛️"},
        {"title": "Product Carbon Traceability", "description": "Material, supplier, transport, production, and emissions lineage.", "icon": "🌱"},
        {"title": "Engineering Change Impact", "description": "Trace design and specification changes through BOM and production.", "icon": "🔧"},
    ],
    "Telecommunications": [
        {"title": "AI Network Fault Propagation", "description": "Predict service impact across topology, alarms, dependencies, and regions.", "icon": "⚡"},
        {"title": "Telecom Fraud Fusion", "description": "Connect subscriber, SIM, device, CDR, payment, and case evidence.", "icon": "🔍"},
        {"title": "Customer Experience 360", "description": "Unify usage, billing, network quality, complaints, and service history.", "icon": "👥"},
        {"title": "Graph-Based Churn Prevention", "description": "Connected usage, complaint, payment, offer, and retention signals.", "icon": "📉"},
        {"title": "5G Service Assurance", "description": "Slice, service, network element, SLA, and customer-impact dependencies.", "icon": "📡"},
        {"title": "Network Energy Optimization", "description": "Site, equipment, traffic, energy, and emissions relationship analysis.", "icon": "🔋"},
        {"title": "Partner & Roaming Intelligence", "description": "Operator, route, settlement, quality, and roaming anomaly connections.", "icon": "🌐"},
    ],
    "Retail & E-Commerce": [
        {"title": "Generative Product Knowledge Graph", "description": "Products, attributes, content, categories, suppliers, and rich assets.", "icon": "🏷️"},
        {"title": "Hyper-Personalized Recommendations", "description": "Customer intent, session, product affinity, and contextual offers.", "icon": "✨"},
        {"title": "Omnichannel Customer 360", "description": "Orders, stores, digital behavior, service, returns, and loyalty context.", "icon": "👤"},
        {"title": "Inventory & Demand Intelligence", "description": "Stock, forecast, promotion, supplier, and replenishment dependencies.", "icon": "📦"},
        {"title": "Returns & Abuse Detection", "description": "Connected order, customer, product, payment, device, and return patterns.", "icon": "↩️"},
        {"title": "Retail Media Intelligence", "description": "Audience, campaign, product, placement, conversion, and incrementality links.", "icon": "📣"},
        {"title": "Sustainable Product Traceability", "description": "Product material, supplier, certification, transport, and claim lineage.", "icon": "🌱"},
    ],
}

USE_CASE_PROFILES: dict[str, list[tuple[tuple[str, ...], dict[str, list[str]]]]] = {
    "Financial Services": [
        (("fraud", "crime", "aml", "payment"), {
            "entities": ["Customer", "Account", "Transaction", "Device", "Beneficiary"],
            "relationships": ["OWNS", "TRANSFERRED_TO", "USES_DEVICE", "BENEFITS"],
            "detections": ["transaction rings", "mule-account clusters", "device overlap", "sanctions paths"],
        }),
        (("credit", "borrower", "counterparty", "climate"), {
            "entities": ["Borrower", "Facility", "Collateral", "Counterparty", "Covenant"],
            "relationships": ["HAS_FACILITY", "SECURED_BY", "EXPOSED_TO", "BOUNDED_BY"],
            "detections": ["connected exposure", "collateral gaps", "covenant deterioration", "counterparty concentration"],
        }),
        (("kyc", "ubo", "ownership", "regulatory"), {
            "entities": ["Party", "LegalEntity", "BeneficialOwner", "Document", "Obligation"],
            "relationships": ["OWNS", "CONTROLS", "IDENTIFIED_BY", "SUBJECT_TO"],
            "detections": ["hidden ownership", "identity inconsistency", "watchlist exposure", "control gaps"],
        }),
        (("customer", "next best", "360"), {
            "entities": ["Customer", "Product", "Interaction", "Channel", "Offer"],
            "relationships": ["HOLDS", "INTERACTED_VIA", "RESPONDED_TO", "ELIGIBLE_FOR"],
            "detections": ["relationship gaps", "service friction", "product affinity", "responsible-offer opportunities"],
        }),
    ],
    "Healthcare & Life Sciences": [
        (("discovery", "molecule", "compound", "target", "candidate", "assay"), {
            "entities": ["DrugCandidate", "MolecularTarget", "Compound", "Assay", "Indication", "Study"],
            "relationships": ["BINDS_TO", "MODULATES", "TESTED_IN", "INDICATED_FOR", "SUPPORTED_BY"],
            "detections": ["target-compound affinity gaps", "assay inconsistency", "indication mismatch", "evidence sparsity"],
        }),
        (("trial", "site", "investigator", "enrollment"), {
            "entities": ["ClinicalTrial", "Site", "Investigator", "Participant", "Protocol", "AdverseEvent"],
            "relationships": ["RUNS_AT", "LED_BY", "ENROLLS", "FOLLOWS_PROTOCOL", "REPORTED_EVENT"],
            "detections": ["site underperformance", "enrollment bottlenecks", "protocol deviations", "safety clusters"],
        }),
        (("drug", "safety", "pharmacovigilance", "adverse"), {
            "entities": ["MedicinalProduct", "AdverseEvent", "Patient", "SafetyReport", "Label", "Study"],
            "relationships": ["EXPERIENCED", "SUSPECTS", "DOCUMENTED_IN", "DESCRIBED_BY", "SUPPORTED_BY"],
            "detections": ["unexpected safety signals", "event clusters", "label inconsistencies", "evidence gaps"],
        }),
        (("provider", "referral", "integrity"), {
            "entities": ["Provider", "Facility", "Patient", "Claim", "Referral", "Service"],
            "relationships": ["WORKS_AT", "TREATED", "SUBMITTED", "REFERRED_TO", "BILLED_FOR"],
            "detections": ["referral loops", "billing anomalies", "network concentration", "service inconsistency"],
        }),
        (("patient", "journey", "interoperability", "fhir"), {
            "entities": ["Patient", "Encounter", "Provider", "Condition", "Medication", "Observation"],
            "relationships": ["HAS_ENCOUNTER", "TREATED_BY", "DIAGNOSED_WITH", "TAKES", "HAS_OBSERVATION"],
            "detections": ["care-path gaps", "duplicate treatment", "medication conflicts", "follow-up delays"],
        }),
    ],
    "Manufacturing & Supply Chain": [
        (("maintenance", "asset", "failure"), {
            "entities": ["Asset", "Sensor", "FailureMode", "WorkOrder", "Component", "Technician"],
            "relationships": ["HAS_SENSOR", "EXHIBITS", "REQUIRES", "CONTAINS", "SERVICED_BY"],
            "detections": ["failure propagation", "anomalous sensor paths", "maintenance recurrence", "critical-part dependency"],
        }),
        (("quality", "recall", "defect", "trace"), {
            "entities": ["Product", "Batch", "Component", "Supplier", "Defect", "Shipment"],
            "relationships": ["PRODUCED_IN", "CONTAINS", "SOURCED_FROM", "HAS_DEFECT", "SHIPPED_TO"],
            "detections": ["defect propagation", "recall scope", "supplier concentration", "affected shipment paths"],
        }),
        (("supplier", "resilience", "supply", "control tower"), {
            "entities": ["Supplier", "Facility", "Component", "PurchaseOrder", "Shipment", "Disruption"],
            "relationships": ["OPERATES", "SUPPLIES", "FULFILLS", "MOVES", "IMPACTED_BY"],
            "detections": ["multi-tier dependency", "single-source exposure", "disruption propagation", "late-order clusters"],
        }),
        (("digital twin", "engineering", "change"), {
            "entities": ["Asset", "Assembly", "Component", "Specification", "ChangeOrder", "Process"],
            "relationships": ["CONTAINS", "DEFINED_BY", "CHANGED_BY", "BUILT_THROUGH", "DEPENDS_ON"],
            "detections": ["change impact", "configuration mismatch", "component dependency", "process bottlenecks"],
        }),
    ],
    "Telecommunications": [
        (("fault", "assurance", "5g", "network", "alarm"), {
            "entities": ["NetworkElement", "Service", "Alarm", "Region", "Ticket", "CustomerImpact"],
            "relationships": ["DEPENDS_ON", "SUPPORTS", "RAISED", "SERVES", "TRACKED_BY", "CAUSES"],
            "detections": ["fault propagation", "service-impact paths", "alarm correlation", "SLA exposure"],
        }),
        (("fraud", "sim", "roaming"), {
            "entities": ["Subscriber", "SIM", "Device", "CallRecord", "Payment", "Location"],
            "relationships": ["USES_SIM", "USES_DEVICE", "GENERATED", "PAID_BY", "OBSERVED_AT"],
            "detections": ["SIM/device overlap", "subscription fraud rings", "roaming anomalies", "payment linkage"],
        }),
        (("customer", "churn", "experience"), {
            "entities": ["Subscriber", "Service", "UsageEvent", "Complaint", "Offer", "NetworkExperience"],
            "relationships": ["SUBSCRIBES_TO", "GENERATED", "RAISED", "RECEIVED", "EXPERIENCED"],
            "detections": ["churn communities", "experience deterioration", "complaint recurrence", "retention opportunities"],
        }),
    ],
    "Retail & E-Commerce": [
        (("return", "abuse", "fraud"), {
            "entities": ["Customer", "Order", "Return", "Product", "Payment", "Device"],
            "relationships": ["PLACED", "RETURNED", "CONTAINS", "PAID_BY", "USED_DEVICE"],
            "detections": ["return-abuse rings", "shared-device clusters", "serial-return patterns", "payment anomalies"],
        }),
        (("inventory", "demand", "replenish"), {
            "entities": ["Product", "Inventory", "Warehouse", "Store", "Supplier", "Promotion"],
            "relationships": ["HAS_STOCK", "STORED_AT", "SOLD_AT", "SUPPLIED_BY", "AFFECTED_BY"],
            "detections": ["stockout propagation", "demand anomalies", "supplier dependency", "promotion lift gaps"],
        }),
        (("product", "knowledge", "catalog"), {
            "entities": ["Product", "Category", "Attribute", "Supplier", "Asset", "Claim"],
            "relationships": ["BELONGS_TO", "HAS_ATTRIBUTE", "SUPPLIED_BY", "HAS_ASSET", "MAKES_CLAIM"],
            "detections": ["catalog gaps", "duplicate products", "claim inconsistency", "supplier-content gaps"],
        }),
        (("recommend", "personal", "next best"), {
            "entities": ["Customer", "Session", "Product", "Interaction", "Order", "Offer"],
            "relationships": ["STARTED", "VIEWED", "PURCHASED", "CONTAINS", "RECEIVED"],
            "detections": ["product affinity", "journey drop-off", "next-best-action paths", "offer fatigue"],
        }),
    ],
}


def _use_case_profile(industry: str, use_case: str, base: dict[str, Any]) -> dict[str, Any]:
    lowered = use_case.lower()
    for keywords, profile in USE_CASE_PROFILES.get(industry, []):
        if any(keyword in lowered for keyword in keywords):
            return {
                "entities": profile["entities"],
                "relationships": profile["relationships"],
                "detections": profile["detections"],
                "standards": base["standards"],
            }
    return {
        "entities": base["entities"],
        "relationships": base["relationships"],
        "detections": base["detections"],
        "standards": base["standards"],
    }


class DomainConfiguratorRequest(BaseModel):
    industry: str
    use_case: str = ""
    organization_context: str = ""
    objective: str = ""
    data_available: str = ""
    geography: str = ""
    decision_audience: str = ""
    notes: str = ""
    skip_llm: bool = False


class TrendingUseCasesRequest(BaseModel):
    industry: str
    organization_context: str = ""
    geography: str = ""
    objective: str = ""
    refresh_seed: int = 0
    skip_llm: bool = False


def _clean(value: Any, limit: int = 600) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def _industry(req: DomainConfiguratorRequest) -> tuple[str, dict]:
    if req.industry in INDUSTRY_CONFIG:
        return req.industry, INDUSTRY_CONFIG[req.industry]
    return "Financial Services", INDUSTRY_CONFIG["Financial Services"]


def _suggest_use_case(req: DomainConfiguratorRequest, config: dict) -> str:
    if req.use_case.strip():
        return _clean(req.use_case, 120)
    blob = f"{req.objective} {req.data_available} {req.notes}".lower()
    scores = []
    for use_case in config["use_cases"]:
        words = re.findall(r"[a-z0-9]+", use_case.lower())
        score = sum(1 for word in words if len(word) > 3 and word in blob)
        scores.append((score, use_case))
    scores.sort(key=lambda item: (-item[0], config["use_cases"].index(item[1])))
    return scores[0][1]


def build_trending_use_cases(req: TrendingUseCasesRequest) -> dict:
    industry = req.industry if req.industry in INDUSTRY_CONFIG else "Financial Services"
    candidates = list(TRENDING_USE_CASES[industry])
    # Rotate fallback rankings between refreshes so the API is not a fixed five-card response.
    rotation = abs(int(req.refresh_seed or 0)) % len(candidates)
    ranked = candidates[rotation:] + candidates[:rotation]
    period = datetime.now(timezone.utc).strftime("%b %Y")
    return {
        "source": "trend_fallback",
        "industry": industry,
        "period": period,
        "trend_label": "Trending now",
        "use_cases": [
            {
                **item,
                "rank": index + 1,
                "trend_note": f"Trending now · {period}",
            }
            for index, item in enumerate(ranked[:5])
        ],
    }


def enrich_trending_use_cases_with_llm(payload: dict, req: TrendingUseCasesRequest) -> dict:
    system = (
        "You are an enterprise knowledge-graph market analyst. Return STRICT JSON only with "
        "keys period and use_cases. Rank exactly five currently trending, distinct use cases "
        "for the selected industry. Adapt to the organization context, geography, and objective "
        "when supplied. Do not merely repeat a static catalog. Each use_cases item must have "
        "keys title, description, icon, trend_note. title <= 7 words; description <= 18 words; "
        "icon is one relevant emoji; trend_note is a short phrase beginning 'Trending now'. "
        "The use cases must be feasible for a knowledge-graph and document-intelligence journey."
    )
    user = json.dumps({
        "current_date": datetime.now(timezone.utc).date().isoformat(),
        "industry": payload["industry"],
        "organization_context": req.organization_context,
        "geography": req.geography,
        "objective": req.objective,
        "refresh_seed": req.refresh_seed,
        "fallback_candidates": payload["use_cases"],
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        cleaned: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in parsed.get("use_cases") or []:
            if not isinstance(item, dict):
                continue
            title = _clean(item.get("title"), 100)
            key = title.lower()
            if not title or key in seen:
                continue
            seen.add(key)
            cleaned.append({
                "rank": len(cleaned) + 1,
                "title": title,
                "description": _clean(item.get("description"), 220),
                "icon": _clean(item.get("icon"), 8) or "◆",
                "trend_note": _clean(item.get("trend_note"), 80) or "Trending now · AI-ranked",
            })
            if len(cleaned) == 5:
                break
        if len(cleaned) == 5:
            payload["use_cases"] = cleaned
            payload["period"] = _clean(parsed.get("period"), 40) or payload["period"]
            payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Trending use-case LLM enrichment failed: {exc}")
    return payload


def _pillar_blueprint(
    industry: str,
    use_case: str,
    objective: str,
    preview: dict[str, Any],
) -> dict[str, Any]:
    """Concise fallback configuration consumed by every downstream UI pillar."""
    entities = list(preview.get("primary_entities") or ["Entity", "Record", "Evidence"])
    relationships = list(preview.get("key_relationships") or ["RELATED_TO", "EVIDENCED_BY"])
    detections = list(preview.get("detection_focus") or ["connected risk", "evidence gaps"])
    standards = list(preview.get("ontology_standards") or ["Domain ontology"])
    entity_text = ", ".join(entities[:4])
    relationship_text = ", ".join(relationships[:4])
    detection_text = ", ".join(detections[:3])
    return {
        "upload_files": {
            "title": f"Upload Evidence for {use_case}",
            "subtitle": (
                f"Load structured and unstructured evidence for {industry}. "
                f"Sources should help connect {entity_text} for the objective: {objective}"
            ),
            "structured_examples": [f"{item} master or event table" for item in entities[:4]],
            "unstructured_examples": [
                f"{use_case} policies and procedures",
                "Reports, correspondence, contracts, and supporting records",
                "Images, transcripts, and external reference material",
            ],
        },
        "structured_pipeline": {
            "title": f"Structured Evidence Pipeline — {use_case}",
            "subtitle": f"Map uploaded tables into the {industry} graph model.",
            "steps": [
                {"name": "Ingest", "description": f"Profile uploaded tables for {entity_text}.", "technology": "Schema profiler · file agents"},
                {"name": "Validate", "description": "Validate keys, references, data types, duplicates, and quality rules.", "technology": "Data quality agents"},
                {"name": "Map", "description": f"Map columns to configured entity labels and {standards[0]}.", "technology": "LLM schema mapper"},
                {"name": "Load", "description": "Create use-case-specific nodes and relationship candidates.", "technology": "Neo4j parameterized load"},
                {"name": "Detect", "description": f"Evaluate early signals: {detection_text}.", "technology": "Cypher pattern agents"},
                {"name": "Label", "description": "Write provenance, confidence, and review labels for downstream traversal.", "technology": "Governed graph writer"},
            ],
        },
        "unstructured_pipeline": {
            "title": f"Unstructured Evidence Pipeline — {use_case}",
            "subtitle": f"Convert documents and media into evidence linked to {entity_text}.",
            "steps": [
                {"name": "Ingest", "description": "Classify documents, images, text, and audio by source and format.", "technology": "Document ingestion agents"},
                {"name": "Extract", "description": "Extract text, tables, OCR content, and available transcripts.", "technology": "PDF · OCR · transcription"},
                {"name": "Chunk", "description": "Create semantic chunks while retaining source and page provenance.", "technology": "Semantic text splitter"},
                {"name": "Entity Extract", "description": f"Extract configured entity types: {entity_text}.", "technology": "NER · LLM extraction"},
                {"name": "Relation Extract", "description": f"Extract candidate relationships: {relationship_text}.", "technology": "Triple extraction agent"},
                {"name": "Resolve", "description": "Match extracted mentions to structured graph identities.", "technology": "Fuzzy + embedding resolution"},
                {"name": "Classify", "description": "Classify unresolved evidence and preserve confidence for human review.", "technology": "Ontology classifier"},
            ],
        },
        "entity_resolution": {
            "title": f"Entity Resolution for {use_case}",
            "subtitle": (
                f"Consolidate structured and unstructured mentions of {entity_text} "
                "into governed graph identities with source-level proof."
            ),
            "method_steps": [
                {"title": "Collect candidates", "description": f"Collect {entity_text} mentions from all uploaded modalities."},
                {"title": "Score identity", "description": "Compare authoritative keys, normalized attributes, fuzzy similarity, and embeddings."},
                {"title": "Merge safely", "description": "Merge only above the configured confidence threshold; retain unresolved candidates."},
                {"title": "Preserve proof", "description": "Store source, method, confidence, and reviewed attributes on every resolved identity."},
            ],
            "examples": [
                {
                    "source": f"Document mention · {entities[index % len(entities)]}",
                    "target": f"Structured record · {entities[index % len(entities)]}-00{index + 1}",
                    "method": "Authoritative key plus attribute and semantic similarity",
                    "confidence": "Above configured merge threshold",
                    "enrichment": f"Consolidated {entities[index % len(entities)]} identity with provenance and confidence.",
                }
                for index in range(min(4, max(3, len(entities))))
            ],
        },
        "graph_construction": {
            "title": f"Building the {use_case} Knowledge Graph",
            "subtitle": f"Create {entity_text} nodes and {relationship_text} relationships from the active evidence session.",
            "node_labels": entities[:6],
            "relationship_types": relationships[:6],
            "detection_focus": detections[:5],
        },
        "interactive_graph": {
            "title": f"{use_case} — Interactive Knowledge Graph",
            "subtitle": f"Explore {industry} entities, evidence, relationships, and {detection_text}.",
            "focus_tabs": detections[:4],
            "legend_labels": entities[:6],
        },
        "cypher_detection": {
            "title": f"Cypher Detection — {use_case}",
            "intro": f"Traverse {relationship_text} paths to evaluate {detection_text} using the active uploaded evidence.",
            "detection_focus": detections[:5],
        },
        "cross_doc_discovery": {
            "title": f"Cross-Document Discovery — {use_case}",
            "subtitle": (
                f"Connect structured and unstructured {industry} evidence to surface "
                f"findings that support {objective}"
            ),
            "eyebrow": f"{industry} · Requirement-Specific Cross-Source Reasoning",
            "focus": f"Compare evidence across sources for {objective}",
        },
        "intelligence_report": {
            "title": f"{use_case} Intelligence Report",
            "focus": f"Decision intelligence for {objective}",
        },
        "final_report": {
            "title": f"{use_case} Executive Action Report",
            "focus": f"Leadership actions, obligations, recommendations, and way forward for {objective}",
        },
        "next_ai": {
            "persona": f"{use_case} evidence assistant",
            "scope": f"Answer from uploaded {industry} evidence and its graph relationships.",
            "hint_topics": detections[:5],
        },
        "control_tower": {
            "title": f"Control Tower — {use_case}",
            "subtitle": f"Govern the active {industry} journey, its agents, evidence controls, and model operations.",
            "governance_focus": [
                f"{standards[0]} alignment",
                "Entity and relationship quality",
                "Evidence provenance and human review",
                "LLM grounding, privacy, and safety",
            ],
            "monitoring_focus": [
                f"{use_case} pipeline health",
                f"Coverage for {entity_text}",
                f"Detection monitoring: {detection_text}",
                "RAG retrieval and Cypher execution quality",
            ],
        },
    }


def _clean_blueprint(value: Any, depth: int = 0) -> Any:
    if depth > 4:
        return None
    if isinstance(value, str):
        return _clean(value, 800)
    if isinstance(value, list):
        return [_clean_blueprint(item, depth + 1) for item in value[:10]]
    if isinstance(value, dict):
        return {
            _clean(key, 80): _clean_blueprint(item, depth + 1)
            for key, item in list(value.items())[:30]
        }
    return value if isinstance(value, (int, float, bool)) else None


def build_domain_configuration(req: DomainConfiguratorRequest) -> dict:
    industry, config = _industry(req)
    use_case = _suggest_use_case(req, config)
    profile = _use_case_profile(industry, use_case, config)
    objective = _clean(req.objective) or f"Build decision intelligence for {use_case}."
    caption = f"{industry} · {use_case} — {objective}"
    payload = {
        "source": "configured",
        "industry": industry,
        "use_case": use_case,
        "objective": objective,
        "journey_caption": caption,
        "organization_context": _clean(req.organization_context),
        "geography": _clean(req.geography),
        "decision_audience": _clean(req.decision_audience) or "Business and executive stakeholders",
        "intake_summary": _clean(
            f"{req.organization_context}. Objective: {objective}. "
            f"Available evidence: {req.data_available}. Geography: {req.geography}. {req.notes}",
            1200,
        ),
        "preview": {
            "primary_entities": profile["entities"],
            "key_relationships": profile["relationships"],
            "ontology_standards": profile["standards"],
            "detection_focus": profile["detections"],
            "structured_focus": _clean(req.data_available) or "User-provided structured datasets",
            "unstructured_focus": "Policies, reports, contracts, transcripts, images, and other supporting evidence",
        },
        "ai_guidance": (
            f"Start with {use_case}; upload evidence that can connect "
            f"{', '.join(profile['entities'][:3])} and validate {profile['detections'][0]}."
        ),
    }
    pillar_blueprint = _pillar_blueprint(
        industry, use_case, objective, payload["preview"]
    )
    # These two processing pipelines are universal platform behavior, not
    # domain-configurable pillars.
    pillar_blueprint.pop("structured_pipeline", None)
    pillar_blueprint.pop("unstructured_pipeline", None)
    payload["pillar_blueprint"] = pillar_blueprint
    return payload


def enrich_domain_configuration_with_llm(payload: dict, req: DomainConfiguratorRequest) -> dict:
    config = INDUSTRY_CONFIG[payload["industry"]]
    system = (
        "You are a knowledge-graph journey configurator. Return STRICT JSON only. Use the "
        "selected industry and selected use case as authoritative. The use case may be a "
        "user-defined scenario, so do not replace it with a catalog item. Tailor the journey "
        "to the intake without inventing data. Return keys: use_case, objective, journey_caption, "
        "ai_guidance, primary_entities, key_relationships, ontology_standards, detection_focus, "
        "structured_focus, unstructured_focus. Arrays must contain 2..6 concise strings. "
        "structured_focus and unstructured_focus must be short plain-language phrases describing "
        "the evidence the user should upload. journey_caption must be one plain-language "
        "sentence suitable for the heading on every downstream page. Also return pillar_blueprint "
        "with concise domain/use-case-specific configuration for upload_files, entity_resolution, "
        "graph_construction, interactive_graph, "
        "cypher_detection, cross_doc_discovery, intelligence_report, final_report, next_ai, and "
        "control_tower. Preserve the same object shape as fallback.pillar_blueprint. Do not return "
        "structured_pipeline or unstructured_pipeline because those are fixed platform workflows. "
        "entity_resolution must contain exactly 4 method_steps and 3..5 examples. Each example "
        "must contain source, target, method, confidence, and enrichment. Confidence should be a "
        "plain-language decision such as 'above configured merge threshold', not an invented "
        "numeric score. Do not include "
        "AML, lease, patient, supplier, telecom, or retail terminology unless relevant to the "
        "authoritative selected industry and use case."
    )
    user = json.dumps({
        "selected_industry": payload["industry"],
        "selected_use_case": req.use_case,
        "illustrative_use_cases": config["use_cases"],
        "organization_context": req.organization_context,
        "objective": req.objective,
        "data_available": req.data_available,
        "geography": req.geography,
        "decision_audience": req.decision_audience,
        "notes": req.notes,
        "fallback": payload,
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload
        payload["use_case"] = _clean(req.use_case, 120) or payload["use_case"]
        payload["objective"] = _clean(parsed.get("objective"), 600) or payload["objective"]
        payload["journey_caption"] = (
            _clean(parsed.get("journey_caption"), 500)
            or f"{payload['industry']} · {payload['use_case']} — {payload['objective']}"
        )
        payload["ai_guidance"] = _clean(parsed.get("ai_guidance"), 700) or payload["ai_guidance"]
        for source_key, target_key in (
            ("primary_entities", "primary_entities"),
            ("key_relationships", "key_relationships"),
            ("ontology_standards", "ontology_standards"),
            ("detection_focus", "detection_focus"),
        ):
            values = parsed.get(source_key)
            if isinstance(values, list) and values:
                payload["preview"][target_key] = [_clean(item, 80) for item in values[:6]]
        structured_focus = _clean(parsed.get("structured_focus"), 220)
        unstructured_focus = _clean(parsed.get("unstructured_focus"), 220)
        if structured_focus:
            payload["preview"]["structured_focus"] = structured_focus
        if unstructured_focus:
            payload["preview"]["unstructured_focus"] = unstructured_focus
        if _clean(req.decision_audience):
            payload["decision_audience"] = _clean(req.decision_audience)
        if _clean(req.geography):
            payload["geography"] = _clean(req.geography)
        fallback_blueprint = _pillar_blueprint(
            payload["industry"], payload["use_case"], payload["objective"], payload["preview"]
        )
        fallback_blueprint.pop("structured_pipeline", None)
        fallback_blueprint.pop("unstructured_pipeline", None)
        candidate = parsed.get("pillar_blueprint")
        if isinstance(candidate, dict):
            cleaned = _clean_blueprint(candidate)
            for pillar, fallback_value in fallback_blueprint.items():
                if isinstance(cleaned.get(pillar), dict):
                    merged_pillar = {
                        **fallback_value,
                        **cleaned[pillar],
                    }
                    for list_key, fallback_list in fallback_value.items():
                        if not isinstance(fallback_list, list):
                            continue
                        candidate_list = merged_pillar.get(list_key)
                        minimum = len(fallback_list)
                        expects_objects = bool(fallback_list) and isinstance(fallback_list[0], dict)
                        invalid_objects = expects_objects and (
                            not isinstance(candidate_list, list)
                            or not all(isinstance(item, dict) for item in candidate_list)
                        )
                        if (
                            not isinstance(candidate_list, list)
                            or len(candidate_list) < minimum
                            or invalid_objects
                        ):
                            merged_pillar[list_key] = fallback_list
                    fallback_blueprint[pillar] = merged_pillar
        payload["pillar_blueprint"] = fallback_blueprint
        payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Domain configuration LLM enrichment failed: {exc}")
    return payload
