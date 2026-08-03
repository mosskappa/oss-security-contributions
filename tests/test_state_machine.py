from pathlib import Path

from tools.osssec_public.state_machine import validate_state_file, validate_state_record


def test_example_workflow_status_matches_state_machine():
    root = Path(__file__).resolve().parents[1]
    assert validate_state_file(root / "examples" / "workflow-status.json") == []


def test_rejects_invalid_transition():
    warnings = validate_state_record(
        {
            "previous_state": "INTAKE",
            "current_state": "PUBLIC_CREDIT_READY",
            "claim_level": "PROVEN",
            "gates": {},
            "public_evidence_url": "https://example.org/advisory",
        }
    )

    assert any("not allowed" in warning for warning in warnings)


def test_public_credit_requires_public_evidence():
    warnings = validate_state_record(
        {
            "previous_state": "PATCH_VALIDATION",
            "current_state": "PUBLIC_CREDIT_READY",
            "claim_level": "PROVEN",
            "gates": {
                "authorization": "PASS",
                "boundary_model": "PASS",
                "evidence": "PASS",
                "maintainer_invariant": "PASS",
                "prior_art": "PASS",
                "hostile_review": "KEEP",
                "report_quality": "PASS",
                "disclosure_route": "SEND_PRIVATE_CONSERVATIVE",
                "public_credit": "PUBLIC_CREDIT_READY",
            },
            "public_evidence_url": "",
        }
    )

    assert any("public_evidence_url" in warning for warning in warnings)
