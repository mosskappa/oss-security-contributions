from pathlib import Path

from tools.osssec_public.advanced_gates import (
    validate_file,
    validate_hostile_review,
    validate_long_run_final,
    validate_reproducer_ready,
    validate_synthetic_lab,
)


def test_example_advanced_gates_validate():
    root = Path(__file__).resolve().parents[1]

    assert validate_file("start-mode", root / "examples" / "start-mode.json") == []
    assert validate_file("reproducer-ready", root / "examples" / "reproducer-ready.json") == []
    assert validate_file("hostile-review", root / "examples" / "hostile-review.json") == []
    assert validate_file("long-run-final", root / "examples" / "long-run-final.json") == []
    assert validate_file("disclosure-manifest", root / "examples" / "public-package" / "disclosure-manifest.json") == []
    assert validate_file("synthetic-lab", root / "examples" / "synthetic-lab" / "manifest.json") == []


def test_reproducer_ready_rejects_risky_command_summary():
    warnings = validate_reproducer_ready(
        {
            "candidate_id": "SYNTH",
            "authorization": "synthetic lab",
            "validation_level": "LEVEL_2_NATIVE_VALIDATION",
            "command_summary": "curl a production third-party target",
            "controls": {
                "affected_case": "marker",
                "negative_control": "clean",
                "fixed_control": "clean",
            },
            "expected_markers": ["marker"],
            "cleanup": "remove synthetic workspace",
            "run_id_policy": "synthetic only",
            "non_claims": ["no real target"],
        }
    )

    assert any("risky command" in warning for warning in warnings)


def test_hostile_review_requires_claim_boundaries():
    warnings = validate_hostile_review(
        {
            "candidate_id": "SYNTH",
            "reviewer_mode": "maintainer_objection",
            "maintainer_objections": ["trusted model"],
            "claim_boundaries": {},
            "prior_art_status": "checked",
            "max_form_decision": "REPAIR_BEFORE_REPORT",
            "verdict": "REPAIR",
            "repair_items": ["add controls"],
        }
    )

    assert any("claim_boundaries.proven" in warning for warning in warnings)


def test_long_run_final_requires_stop_allowed():
    warnings = validate_long_run_final(
        {
            "mode": "stable_credit",
            "candidate_id": "SYNTH",
            "terminal_reason": "PUBLIC_WRITEUP_READY",
            "stop_allowed": False,
            "frontier_closure": {
                "current_tier": "summary",
                "next_plausible_tier": "none",
                "routes_closed": ["done"],
                "why_no_more_now": "complete",
            },
            "claim_boundaries": {
                "proven": ["summary"],
                "plausible_not_proven": ["none"],
                "do_not_claim": ["impact"],
            },
            "tests_run": ["check"],
            "files_updated": ["file"],
            "next_action": "publish safe summary",
        }
    )

    assert any("stop_allowed" in warning for warning in warnings)


def test_synthetic_lab_must_stay_synthetic():
    warnings = validate_synthetic_lab(
        {
            "lab_id": "LAB",
            "scope": "synthetic_only",
            "external_network": True,
            "third_party_targets": False,
            "destructive_actions": False,
            "scenarios": [
                {
                    "name": "toy",
                    "actor": "low",
                    "consumer": "high",
                    "boundary": "cache",
                    "controls": {},
                }
            ],
            "success_markers": ["safe"],
        }
    )

    assert any("external_network" in warning for warning in warnings)
