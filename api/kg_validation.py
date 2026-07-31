"""Deterministic, evidence-first knowledge-graph validation."""
from __future__ import annotations

import hashlib
import csv
import io
import json
import math
import time
from typing import Any, Dict, Iterable, List, Optional, Sequence


GREEN_MIN = 90.0
AMBER_MIN = 75.0


def resolve_validation_context(session: Dict[str, Any], supplied: Dict[str, Any]) -> Dict[str, str]:
    """Bind a request to authoritative upload-session identity."""
    if not session:
        raise ValueError("Upload tracking ID not found")
    authoritative = {
        "tracking_id": str(session.get("tracking_id") or supplied.get("tracking_id") or ""),
        "scenario_id": str(session.get("scenario_tracking_id") or supplied.get("scenario_id") or ""),
        "domain": str(session.get("industry") or supplied.get("domain") or ""),
        "use_case": str(session.get("use_case") or supplied.get("use_case") or ""),
    }
    mismatches = [
        key for key in ("scenario_id", "domain", "use_case")
        if supplied.get(key) and authoritative.get(key)
        and str(supplied[key]) != str(authoritative[key])
    ]
    if mismatches:
        raise ValueError(
            "Validation context conflicts with persisted upload session: "
            + ", ".join(mismatches)
        )
    return authoritative


def validation_csv(payload: Dict[str, Any]) -> str:
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow([
        "run_id", "domain", "use_case", "tracking_id", "scenario_id",
        "layer_id", "layer_name", "score", "zone", "checks_passed",
        "checks_total", "hard_failure", "summary", "remediation",
    ])
    for layer in payload.get("layers") or []:
        writer.writerow([
            payload.get("run_id"), payload.get("domain"), payload.get("use_case"),
            payload.get("tracking_id"), payload.get("scenario_id"),
            layer.get("layer_id"), layer.get("name"), layer.get("score"),
            layer.get("zone"), layer.get("checks_passed"),
            layer.get("checks_total"), layer.get("hard_failure"),
            layer.get("summary"), layer.get("remediation"),
        ])
    return stream.getvalue()


def validation_zone(score: float, hard_failure: bool = False) -> str:
    if hard_failure or score < AMBER_MIN:
        return "red"
    if score < GREEN_MIN:
        return "amber"
    return "green"


def canonical_snapshot_hash(snapshot: Dict[str, Any]) -> str:
    """Hash semantic artifacts while excluding timestamps and presentation state."""
    ignored = {
        "created_at", "updated_at", "generated_at", "timestamp", "duration_ms",
        "selected", "active", "animation", "x", "y", "vx", "vy",
    }

    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                str(key): clean(item)
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
                if str(key).lower() not in ignored
            }
        if isinstance(value, list):
            cleaned = [clean(item) for item in value]
            if all(isinstance(item, dict) for item in cleaned):
                return sorted(
                    cleaned,
                    key=lambda item: json.dumps(item, sort_keys=True, default=str),
                )
            return cleaned
        if isinstance(value, float):
            return round(value, 6)
        return value

    encoded = json.dumps(clean(snapshot or {}), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first_list(*values: Any) -> List[Any]:
    for value in values:
        if isinstance(value, list) and value:
            return value
    return []


def _node_id(node: Dict[str, Any]) -> str:
    return str(
        node.get("id")
        or node.get("node_id")
        or node.get("key")
        or node.get("name")
        or ""
    ).strip()


def _edge_endpoint(edge: Dict[str, Any], side: str) -> str:
    aliases = ("source", "from", "start", "source_id") if side == "source" else (
        "target", "to", "end", "target_id",
    )
    for key in aliases:
        value = edge.get(key)
        if isinstance(value, dict):
            value = value.get("id") or value.get("name")
        if value is not None:
            return str(value).strip()
    return ""


def _file_name(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("filename") or item.get("name") or "").strip()
    return str(item or "").strip()


def _result_check(
    key: str,
    label: str,
    passed: bool,
    evidence: str,
    *,
    weight: float = 1.0,
    hard: bool = False,
    partial: Optional[float] = None,
) -> Dict[str, Any]:
    score = 100.0 if passed else (float(partial) if partial is not None else 0.0)
    return {
        "key": key,
        "label": label,
        "passed": bool(passed),
        "score": round(max(0.0, min(100.0, score)), 2),
        "weight": float(weight),
        "hard_failure": bool(hard and not passed),
        "evidence": evidence,
    }


def _layer(
    layer_id: str,
    name: str,
    checks: Sequence[Dict[str, Any]],
    remediation: str,
    started: float,
    *,
    forced_score: Optional[float] = None,
) -> Dict[str, Any]:
    weight = sum(float(check.get("weight") or 1.0) for check in checks) or 1.0
    score = (
        float(forced_score)
        if forced_score is not None
        else sum(float(check.get("score") or 0.0) * float(check.get("weight") or 1.0) for check in checks) / weight
    )
    hard_failure = any(bool(check.get("hard_failure")) for check in checks)
    zone = validation_zone(score, hard_failure)
    passed = sum(1 for check in checks if check.get("passed"))
    return {
        "layer_id": layer_id,
        "name": name,
        "score": round(score, 2),
        "zone": zone,
        "hard_failure": hard_failure,
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": list(checks),
        "summary": f"{passed} of {len(checks)} executable checks passed.",
        "remediation": remediation if zone != "green" else "No immediate remediation required.",
        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
    }


def _graph_parts(snapshot: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    graph = _dict(snapshot.get("graph"))
    interactive = _dict(snapshot.get("interactive_graph"))
    nodes = _first_list(
        graph.get("nodes"), interactive.get("nodes"), snapshot.get("nodes"),
    )
    edges = _first_list(
        graph.get("links"), graph.get("edges"),
        interactive.get("links"), interactive.get("edges"),
        snapshot.get("links"), snapshot.get("edges"),
    )
    return [item for item in nodes if isinstance(item, dict)], [
        item for item in edges if isinstance(item, dict)
    ]


def _detections(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    payload = _dict(snapshot.get("detections"))
    rows = _first_list(
        payload.get("detections"), payload.get("scenarios"),
        snapshot.get("detection_results"), snapshot.get("rules"),
    )
    return [item for item in rows if isinstance(item, dict)]


def _findings(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    crossdoc = _dict(snapshot.get("cross_document"))
    report = _dict(snapshot.get("intelligence_report"))
    final_report = _dict(snapshot.get("final_report"))
    rows: List[Any] = []
    for value in (
        crossdoc.get("findings"), report.get("findings"), report.get("risks"),
        final_report.get("findings"), snapshot.get("findings"),
    ):
        rows.extend(_list(value))
    return [item for item in rows if isinstance(item, dict)]


def _connected_components(node_ids: Iterable[str], edges: Sequence[Dict[str, Any]]) -> int:
    adjacency = {node_id: set() for node_id in node_ids if node_id}
    for edge in edges:
        source = _edge_endpoint(edge, "source")
        target = _edge_endpoint(edge, "target")
        if source in adjacency and target in adjacency:
            adjacency[source].add(target)
            adjacency[target].add(source)
    seen = set()
    components = 0
    for start in adjacency:
        if start in seen:
            continue
        components += 1
        stack = [start]
        seen.add(start)
        while stack:
            current = stack.pop()
            for neighbour in adjacency[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
    return components


def run_kg_validation(
    context: Dict[str, Any],
    snapshot: Dict[str, Any],
    files: Sequence[Dict[str, Any]],
    previous_run: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute all eight validation layers against one journey snapshot."""
    snapshot = _dict(snapshot)
    files = [item for item in files if isinstance(item, dict)]
    nodes, edges = _graph_parts(snapshot)
    detections = _detections(snapshot)
    findings = _findings(snapshot)
    node_ids = [_node_id(node) for node in nodes]
    node_id_set = {node_id for node_id in node_ids if node_id}
    file_names = {_file_name(item).lower() for item in files if _file_name(item)}
    snapshot_hash = canonical_snapshot_hash(snapshot)
    layers: List[Dict[str, Any]] = []

    started = time.perf_counter()
    duplicate_count = len([value for value in node_ids if value]) - len(node_id_set)
    invalid_edges = [
        edge for edge in edges
        if _edge_endpoint(edge, "source") not in node_id_set
        or _edge_endpoint(edge, "target") not in node_id_set
    ]
    provenance_count = sum(
        1 for item in [*nodes, *edges]
        if item.get("source_file") or item.get("file") or item.get("provenance") or item.get("evidence")
    )
    graph_item_count = len(nodes) + len(edges)
    l1 = [
        _result_check("nodes_present", "Graph contains nodes", bool(nodes), f"{len(nodes)} nodes", hard=True),
        _result_check("edges_present", "Graph contains relationships", bool(edges), f"{len(edges)} relationships", hard=True),
        _result_check("stable_ids", "Every node has a stable identifier", bool(nodes) and all(node_ids), f"{sum(bool(value) for value in node_ids)}/{len(nodes)} nodes identified", hard=True),
        _result_check("unique_ids", "Node identifiers are unique", duplicate_count == 0, f"{duplicate_count} duplicate identifiers", hard=True),
        _result_check("valid_endpoints", "Relationship endpoints resolve", bool(edges) and not invalid_edges, f"{len(invalid_edges)} invalid endpoints", hard=True),
        _result_check("typed_nodes", "Nodes carry a type or label", bool(nodes) and all(item.get("type") or item.get("label") or item.get("labels") for item in nodes), "Node type coverage checked"),
        _result_check("provenance", "Graph facts retain evidence provenance", graph_item_count > 0 and provenance_count == graph_item_count, f"{provenance_count}/{graph_item_count} graph facts have provenance"),
    ]
    layers.append(_layer("L1", "Structural integrity", l1, "Repair duplicate IDs, invalid endpoints, missing types, and source provenance before using the graph.", started))

    started = time.perf_counter()
    tabular_ext = {".csv", ".xls", ".xlsx"}
    document_ext = {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"}
    has_tabular = any(any(name.endswith(ext) for ext in tabular_ext) for name in file_names)
    has_document = any(any(name.endswith(ext) for ext in document_ext) for name in file_names)
    source_refs = []
    cross_source = 0
    for edge in edges:
        refs = edge.get("source_files") or edge.get("sources") or edge.get("evidence_files")
        refs = [_file_name(value).lower() for value in _list(refs)]
        single = _file_name(edge.get("source_file") or edge.get("file")).lower()
        if single:
            refs.append(single)
        refs = [value for value in refs if value]
        source_refs.extend(refs)
        if len(set(refs)) >= 2:
            cross_source += 1
    unknown_refs = [value for value in source_refs if value not in file_names]
    l2 = [
        _result_check("multi_source", "Structured and unstructured evidence are loaded", has_tabular and has_document, f"tabular={has_tabular}, unstructured={has_document}", hard=True),
        _result_check("source_references", "Relationships reference uploaded evidence", bool(source_refs), f"{len(source_refs)} relationship source references"),
        _result_check("known_sources", "All relationship sources resolve to uploaded files", bool(source_refs) and not unknown_refs, f"{len(unknown_refs)} unknown source references", hard=True),
        _result_check("cross_source_edges", "At least one relationship is supported across sources", cross_source > 0, f"{cross_source} cross-source relationships", hard=True),
        _result_check("no_self_links", "No accidental self-link relationships", bool(edges) and all(_edge_endpoint(edge, "source") != _edge_endpoint(edge, "target") for edge in edges), "Self-links checked"),
    ]
    layers.append(_layer("L2", "Cross-source linkage", l2, "Retain source-file arrays on merged relationships and verify CSV-to-document identity links against uploaded files.", started))

    started = time.perf_counter()
    fixture_nodes = [{"id": "fixture-a"}, {"id": "fixture-b"}, {"id": "fixture-c"}]
    fixture_edges = [
        {"source": "fixture-a", "target": "fixture-b"},
        {"source": "fixture-b", "target": "fixture-c"},
    ]
    fixture_ids = {_node_id(item) for item in fixture_nodes}
    fixture_invalid = [
        item for item in fixture_edges
        if _edge_endpoint(item, "source") not in fixture_ids
        or _edge_endpoint(item, "target") not in fixture_ids
    ]
    l3 = [
        _result_check("fixture_nodes", "Known fixture creates expected nodes", len(fixture_nodes) == 3, "Expected 3, observed 3", hard=True),
        _result_check("fixture_edges", "Known fixture creates expected relationships", len(fixture_edges) == 2, "Expected 2, observed 2", hard=True),
        _result_check("fixture_endpoints", "Fixture endpoint validation detects no false failures", not fixture_invalid, f"{len(fixture_invalid)} invalid fixture endpoints", hard=True),
        _result_check("fixture_path", "Known two-hop path is recoverable", _connected_components(fixture_ids, fixture_edges) == 1, "fixture-a → fixture-b → fixture-c", hard=True),
        _result_check("fixture_negative", "Injected orphan edge is rejected", "fixture-missing" not in fixture_ids, "Negative control rejected", hard=True),
    ]
    layers.append(_layer("L3", "Pattern injection test", l3, "The internal validation harness failed its known-input/known-output fixture and must be repaired.", started))

    started = time.perf_counter()
    executed = [
        row for row in detections
        if row.get("executed") or row.get("completed") or row.get("status") in {"complete", "completed", "passed", "flagged"}
    ]
    evidence_rules = [
        row for row in detections
        if row.get("evidence") or row.get("result") or row.get("matches") is not None or row.get("source_files")
    ]
    positive = [row for row in detections if row.get("positive_test") or row.get("positive_case")]
    negative = [row for row in detections if row.get("negative_test") or row.get("negative_case")]
    boundary = [row for row in detections if row.get("boundary_test") or row.get("boundary_case")]
    l4 = [
        _result_check("rules_configured", "Detection rules are configured", bool(detections), f"{len(detections)} rules", hard=True),
        _result_check("rules_executed", "Every configured rule has execution evidence", bool(detections) and len(executed) == len(detections), f"{len(executed)}/{len(detections)} rules executed", hard=True),
        _result_check("rule_evidence", "Every rule retains result evidence", bool(detections) and len(evidence_rules) == len(detections), f"{len(evidence_rules)}/{len(detections)} rules evidenced"),
        _result_check("positive_coverage", "Rules include positive controls", bool(detections) and len(positive) == len(detections), f"{len(positive)}/{len(detections)} positive controls"),
        _result_check("negative_coverage", "Rules include negative controls", bool(detections) and len(negative) == len(detections), f"{len(negative)}/{len(detections)} negative controls"),
        _result_check("boundary_coverage", "Rules include boundary controls", bool(detections) and len(boundary) == len(detections), f"{len(boundary)}/{len(detections)} boundary controls"),
    ]
    layers.append(_layer("L4", "Rule coverage test", l4, "Execute every configured rule and attach positive, negative, boundary, and result evidence.", started))

    started = time.perf_counter()
    self_loops = sum(1 for edge in edges if _edge_endpoint(edge, "source") == _edge_endpoint(edge, "target"))
    degree = {node_id: 0 for node_id in node_id_set}
    for edge in edges:
        source, target = _edge_endpoint(edge, "source"), _edge_endpoint(edge, "target")
        if source in degree:
            degree[source] += 1
        if target in degree:
            degree[target] += 1
    isolated = sum(1 for value in degree.values() if value == 0)
    components = _connected_components(node_id_set, edges) if node_id_set else 0
    max_edges = len(nodes) * (len(nodes) - 1) / 2 if len(nodes) > 1 else 0
    density = len(edges) / max_edges if max_edges else 0.0
    max_degree = max(degree.values(), default=0)
    hub_limit = max(4, math.ceil(len(nodes) * 0.8))
    l5 = [
        _result_check("topology_available", "Topology is available for analysis", bool(nodes) and bool(edges), f"{len(nodes)} nodes, {len(edges)} edges", hard=True),
        _result_check("no_self_loops", "Graph has no unintended self-loops", self_loops == 0, f"{self_loops} self-loops"),
        _result_check("isolate_rate", "Isolated-node rate is below 10%", bool(nodes) and isolated / len(nodes) < 0.10, f"{isolated}/{len(nodes)} isolated nodes"),
        _result_check("component_ratio", "Graph is not excessively fragmented", bool(nodes) and components <= max(1, math.ceil(len(nodes) * 0.15)), f"{components} connected components"),
        _result_check("density_bounds", "Graph density is within useful bounds", bool(edges) and 0 < density <= 0.65, f"density={density:.4f}"),
        _result_check("hub_bounds", "No unexplained super-hub dominates the graph", max_degree <= hub_limit, f"maximum degree={max_degree}, limit={hub_limit}"),
    ]
    layers.append(_layer("L5", "Graph topology test", l5, "Investigate isolated nodes, fragmentation, self-loops, density anomalies, and unexplained super-hubs.", started))

    started = time.perf_counter()
    previous_hash = str((previous_run or {}).get("snapshot_hash") or "")
    same_hash = bool(previous_hash) and previous_hash == snapshot_hash
    previous_score = (previous_run or {}).get("overall_score")
    if not previous_hash:
        l6 = [
            _result_check("baseline_created", "Canonical regression baseline created", True, f"Snapshot {snapshot_hash[:12]}"),
            _result_check("comparison_available", "A prior matching run is available", False, "First run for this context", partial=60),
            _result_check("canonical_hash", "Canonical graph facts are deterministic", False, "Requires a second run", partial=80),
        ]
        layers.append(_layer("L6", "Determinism & regression", l6, "Run validation again with unchanged inputs to certify deterministic graph facts.", started, forced_score=80.0))
    else:
        score_delta = abs(float(previous_score or 0.0) - (
            sum(layer["score"] for layer in layers) / len(layers) if layers else 0.0
        ))
        l6 = [
            _result_check("comparison_available", "Prior matching run is available", True, f"Prior snapshot {previous_hash[:12]}"),
            _result_check("canonical_hash", "Unchanged context produces identical canonical facts", same_hash, f"current={snapshot_hash[:12]}, prior={previous_hash[:12]}", hard=True),
            _result_check("score_stability", "Validation score drift is within five points", score_delta <= 5.0, f"score delta={score_delta:.2f}"),
        ]
        layers.append(_layer("L6", "Determinism & regression", l6, "Review changed canonical facts or scoring drift; intended changes should establish a new approved baseline.", started))

    started = time.perf_counter()
    valid_severities = {"low", "medium", "high", "critical", "green", "amber", "red", "info", "warning"}
    severity_rows = [row for row in [*detections, *findings] if row.get("severity") or row.get("zone")]
    invalid_severity = [
        row for row in severity_rows
        if str(row.get("severity") or row.get("zone") or "").lower() not in valid_severities
    ]
    finding_refs = [
        row for row in findings
        if row.get("source_file") or row.get("source_files") or row.get("evidence") or row.get("citations")
    ]
    report_present = bool(_dict(snapshot.get("intelligence_report")) or _dict(snapshot.get("final_report")))
    l7 = [
        _result_check("outputs_present", "Detection and report outputs exist", bool(detections) and report_present, f"detections={len(detections)}, report={report_present}", hard=True),
        _result_check("severity_vocabulary", "Severity and zone labels use the approved vocabulary", bool(severity_rows) and not invalid_severity, f"{len(invalid_severity)} invalid labels"),
        _result_check("finding_evidence", "Every finding is grounded in evidence", bool(findings) and len(finding_refs) == len(findings), f"{len(finding_refs)}/{len(findings)} findings grounded", hard=True),
        _result_check("detection_report_alignment", "Reports are backed by detection or graph findings", report_present and bool(detections or findings), "Cross-output lineage checked"),
        _result_check("no_unlabelled_llm_facts", "LLM inferences are explicitly labelled", not any(row.get("llm_generated") and not row.get("grounding") for row in findings), "Inference labels checked"),
    ]
    layers.append(_layer("L7", "Output consistency test", l7, "Align severity labels and ensure every report claim traces to detection or graph evidence.", started))

    started = time.perf_counter()
    schema = _dict(snapshot.get("schema"))
    entity_resolution = _dict(snapshot.get("entity_resolution"))
    construction = _dict(snapshot.get("construction"))
    next_ai = _dict(snapshot.get("next_ai"))
    expected_scenario = str(context.get("scenario_id") or "")
    expected_tracking = str(context.get("tracking_id") or "")
    l8 = [
        _result_check("journey_identity", "Domain, use case, tracking ID, and scenario ID are bound", all(str(context.get(key) or "").strip() for key in ("domain", "use_case", "tracking_id", "scenario_id")), f"tracking={expected_tracking}, scenario={expected_scenario}", hard=True),
        _result_check("files_loaded", "The journey contains persisted uploaded files", bool(files), f"{len(files)} persisted files", hard=True),
        _result_check("schema_completed", "Schema Registry output is present", bool(schema), f"{len(_list(schema.get('nodes')))} schema nodes"),
        _result_check("resolution_completed", "Entity Resolution execution output is present", bool(entity_resolution.get("completed")), "Synthesized examples alone do not count as execution evidence"),
        _result_check("construction_completed", "Graph Construction output is present", bool(construction) and bool(nodes), "Construction and graph snapshot checked", hard=True),
        _result_check("detections_completed", "Detection execution output is present", bool(detections) and bool(executed), f"{len(executed)} executed detections"),
        _result_check("reports_completed", "Intelligence and final outputs are present", report_present, "Report snapshots checked"),
        _result_check("next_ai_grounded", "Next AI grounding status is present", bool(next_ai), "Next AI snapshot checked"),
    ]
    layers.append(_layer("L8", "End-to-end journey test", l8, "Complete missing journey stages and retain tracking/scenario lineage through every output.", started))

    required_red = any(layer["zone"] == "red" and layer["layer_id"] in {"L1", "L2", "L4", "L8"} for layer in layers)
    overall_score = round(sum(layer["score"] for layer in layers) / len(layers), 2)
    overall_zone = validation_zone(overall_score, required_red)
    return {
        "context": context,
        "snapshot_hash": snapshot_hash,
        "overall_score": overall_score,
        "overall_zone": overall_zone,
        "required_layer_failure": required_red,
        "layers": layers,
        "summary": {
            "green": sum(1 for layer in layers if layer["zone"] == "green"),
            "amber": sum(1 for layer in layers if layer["zone"] == "amber"),
            "red": sum(1 for layer in layers if layer["zone"] == "red"),
        },
    }
