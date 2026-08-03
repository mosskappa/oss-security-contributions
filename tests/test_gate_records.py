import json
from pathlib import Path

from tools.osssec_public.gate_records import (
    scaffold_record,
    validate_experiment_log,
    validate_maximum_form_review,
    validate_record_file,
    validate_target_brief,
    write_scaffold,
)


def test_example_gate_records_validate():
    root = Path(__file__).resolve().parents[1]

    assert validate_record_file("target-brief", root / "examples" / "target-brief.json") == []
    assert validate_record_file("experiment", root / "examples" / "experiment-log.json") == []
    assert validate_record_file("max-form", root / "examples" / "maximum-form-review.json") == []


def test_target_brief_requires_boundary_model():
    warnings = validate_target_brief(
        {
            "candidate_id": "SYNTH-1",
            "project": "example",
            "component": "parser",
            "mode": "stable_credit",
            "status": "INTAKE",
            "authorization": "local lab",
            "affected_version": "v1",
            "disclosure_route": "private advisory",
            "next_step": "build controls",
        }
    )

    assert any("boundary_model" in warning for warning in warnings)


def test_experiment_rejects_speculative_public_summary():
    warnings = validate_experiment_log(
        {
            "candidate_id": "SYNTH-1",
            "project": "example",
            "component": "parser",
            "authorization": "local lab",
            "tested_version": "v1",
            "hypothesis": "test",
            "controls": {
                "vulnerable_case": "observed",
                "negative_control": "not observed",
                "fixed_control": "fixed",
            },
            "claim_level": "SPECULATIVE",
            "status": "EVIDENCE_BUILT",
            "public_handling": {
                "safe_to_publish_summary": True,
                "private_material_retained_elsewhere": True,
            },
        }
    )

    assert any("speculative" in warning.lower() for warning in warnings)


def test_max_form_continue_requires_marker():
    warnings = validate_maximum_form_review(
        {
            "candidate_id": "SYNTH-1",
            "project": "example",
            "component": "cache",
            "current_state": "HOSTILE_REVIEWED",
            "emergency_thesis": "A low trust input reaches a high trust consumer in a common workflow.",
            "impact_marker": "NONE",
            "claim_level": "PROVEN",
            "maintainer_objection": "trusted config",
            "capability_closure": {
                "current_proven_capability": "none",
                "plausible_unproven_capability": "artifact mutation",
                "blocked_routes": [],
            },
            "decision": "CONTINUE_TO_REPORT",
        }
    )

    assert any("impact marker" in warning for warning in warnings)


def test_scaffold_writes_json(tmp_path):
    path = tmp_path / "brief.json"
    record = scaffold_record("target-brief", "SYNTH-2", "example", "component")
    write_scaffold(path, record)

    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["candidate_id"] == "SYNTH-2"
    assert validate_target_brief(loaded) == []
