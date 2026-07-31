from __future__ import annotations

import csv
import io

import pytest

from api.database import DBClient
from api.kg_validation import (
    canonical_snapshot_hash,
    resolve_validation_context,
    run_kg_validation,
    validation_csv,
    validation_zone,
)


def complete_snapshot():
    return {
        "schema": {"nodes": [{"label": "Company"}, {"label": "Document"}]},
        "entity_resolution": {"completed": True, "merged": 1},
        "construction": {"completed": True, "metrics": {"nodes_total": 3, "edges_total": 2}},
        "graph": {
            "nodes": [
                {"id": "A", "type": "Company", "source_file": "entities.csv"},
                {"id": "B", "type": "Company", "source_file": "entities.csv"},
                {"id": "D", "type": "Document", "source_file": "evidence.pdf"},
            ],
            "links": [
                {
                    "source": "A", "target": "B", "type": "RELATED_TO",
                    "source_files": ["entities.csv", "evidence.pdf"],
                    "evidence": "Known fixture relationship",
                },
                {
                    "source": "B", "target": "D", "type": "MENTIONED_IN",
                    "source_files": ["entities.csv", "evidence.pdf"],
                    "evidence": "Cross-source mention",
                },
            ],
        },
        "detections": {
            "detections": [{
                "id": "R1",
                "completed": True,
                "evidence": "A-B matched",
                "positive_test": True,
                "negative_test": True,
                "boundary_test": True,
                "severity": "high",
            }]
        },
        "cross_document": {
            "findings": [{
                "id": "F1", "severity": "high",
                "source_file": "evidence.pdf", "evidence": "page 1",
            }]
        },
        "intelligence_report": {"report_id": "IR1", "findings": []},
        "final_report": {"report_id": "FR1", "findings": []},
        "next_ai": {"vector_store": "ready", "source_count": 2},
    }


def context():
    return {
        "tracking_id": "TRACK-1",
        "scenario_id": "SCENARIO-1",
        "domain": "Test Domain",
        "use_case": "Known Pattern",
    }


def files():
    return [
        {"id": 1, "filename": "entities.csv", "content_type": "text/csv"},
        {"id": 2, "filename": "evidence.pdf", "content_type": "application/pdf"},
    ]


def test_zone_boundaries_and_hard_failure():
    assert validation_zone(90) == "green"
    assert validation_zone(89.99) == "amber"
    assert validation_zone(75) == "amber"
    assert validation_zone(74.99) == "red"
    assert validation_zone(100, hard_failure=True) == "red"


def test_all_eight_layers_execute_and_first_run_creates_amber_baseline():
    result = run_kg_validation(context(), complete_snapshot(), files())
    assert [layer["layer_id"] for layer in result["layers"]] == [
        "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8",
    ]
    assert result["layers"][2]["zone"] == "green"
    assert result["layers"][5]["zone"] == "amber"
    assert result["overall_zone"] == "green"


def test_missing_graph_evidence_forces_required_red():
    snapshot = complete_snapshot()
    snapshot["graph"] = {"nodes": [], "links": []}
    result = run_kg_validation(context(), snapshot, files())
    assert result["layers"][0]["zone"] == "red"
    assert result["required_layer_failure"] is True
    assert result["overall_zone"] == "red"


def test_canonical_hash_ignores_layout_and_timestamps_and_regression_passes():
    first = complete_snapshot()
    second = complete_snapshot()
    first["graph"]["nodes"][0]["x"] = 12
    second["graph"]["nodes"][0]["x"] = 900
    first["generated_at"] = "yesterday"
    second["generated_at"] = "today"
    assert canonical_snapshot_hash(first) == canonical_snapshot_hash(second)
    baseline = run_kg_validation(context(), first, files())
    previous = {
        "snapshot_hash": baseline["snapshot_hash"],
        "overall_score": baseline["overall_score"],
    }
    rerun = run_kg_validation(context(), second, files(), previous)
    assert rerun["layers"][5]["zone"] == "green"


def test_context_identity_mismatch_is_rejected():
    session = {
        "tracking_id": "TRACK-1",
        "scenario_tracking_id": "SCENARIO-1",
        "industry": "Healthcare",
        "use_case": "Drug Discovery",
    }
    assert resolve_validation_context(session, {"tracking_id": "TRACK-1"})["domain"] == "Healthcare"
    with pytest.raises(ValueError, match="domain"):
        resolve_validation_context(session, {
            "tracking_id": "TRACK-1",
            "domain": "Financial Services",
        })


def test_sqlite_validation_history_round_trip_and_csv_export(tmp_path):
    client = DBClient.__new__(DBClient)
    client.use_postgres = False
    client.sqlite_db = str(tmp_path / "validation.db")
    client._init_sqlite()
    client.create_session("TRACK-1", "SCENARIO-1", "Test Domain", "Known Pattern")
    client.save_file("TRACK-1", "entities.csv", "text/csv", b"id\nA\n")
    client.save_file("TRACK-1", "evidence.pdf", "application/pdf", b"%PDF-test")

    result = run_kg_validation(
        context(), complete_snapshot(), client.get_files_for_session("TRACK-1")
    )
    saved = client.save_validation_run("KGV-TEST", result)
    assert saved["run_id"] == "KGV-TEST"
    assert len(saved["layers"]) == 8
    assert client.get_previous_validation_run("TRACK-1", "SCENARIO-1")["run_id"] == "KGV-TEST"
    assert client.get_validation_contexts()[0]["tracking_id"] == "TRACK-1"

    rows = list(csv.reader(io.StringIO(validation_csv(saved))))
    assert rows[0][0] == "run_id"
    assert len(rows) == 9
    assert rows[1][0] == "KGV-TEST"
