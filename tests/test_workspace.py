from pathlib import Path

from tools.osssec_public.workspace import create_workspace, next_action, validate_workspace


def test_create_workspace_validates(tmp_path):
    root = tmp_path / "SYNTH-UX-001"
    create_workspace(
        root,
        candidate_id="SYNTH-UX-001",
        project="example",
        component="component",
        mode="deep_impact_review",
    )

    results = validate_workspace(root)
    assert results
    assert all(result.ok for result in results)


def test_next_action_after_scaffold_is_ready_for_evidence(tmp_path):
    root = tmp_path / "SYNTH-UX-002"
    create_workspace(
        root,
        candidate_id="SYNTH-UX-002",
        project="example",
        component="component",
        mode="stable_credit",
    )

    action = next_action(root)
    assert action["status"] == "ready_for_authorized_evidence"
    assert "authorized evidence" in action["next_action"]


def test_next_action_reports_blocking_gate(tmp_path):
    root = tmp_path / "SYNTH-UX-003"
    create_workspace(
        root,
        candidate_id="SYNTH-UX-003",
        project="example",
        component="component",
        mode="stable_credit",
    )
    (root / "target-brief.json").write_text("{}", encoding="utf-8")

    action = next_action(root)
    assert action["status"] == "needs_repair"
    assert action["blocking_gate"] == "target-brief"
