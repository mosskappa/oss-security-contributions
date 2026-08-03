from pathlib import Path

from tools.osssec_public.handoff import (
    validate_final_handoff_file,
    validate_final_handoff_text,
    validate_session_close,
    validate_session_close_file,
)


def test_example_session_close_validates():
    root = Path(__file__).resolve().parents[1]
    assert validate_session_close_file(root / "examples" / "session-close.json") == []


def test_example_final_handoff_validates():
    root = Path(__file__).resolve().parents[1]
    assert validate_final_handoff_file(root / "examples" / "final-handoff.md") == []


def test_session_close_requires_claim_boundaries():
    warnings = validate_session_close(
        {
            "date": "2099-01-01",
            "mode": "stable_credit",
            "candidate_id": "SYNTH",
            "current_state": "INTAKE",
            "work_completed": ["started"],
            "evidence_or_artifacts": ["brief"],
            "decisions": ["continue"],
            "state_changes": ["none"],
            "blockers": [],
            "tests_run": ["check"],
            "claim_boundaries": {},
            "next_concrete_step": "write boundary model",
        }
    )

    assert any("claim_boundaries missing proven" in warning for warning in warnings)


def test_final_handoff_requires_headings():
    warnings = validate_final_handoff_text("# Missing most headings")

    assert any("Terminal Reason" in warning for warning in warnings)
