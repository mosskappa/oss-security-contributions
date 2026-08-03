from pathlib import Path

from tools.osssec_public.workflow import validate_workflow_file, validate_workflow_record


def test_example_workflow_status_validates():
    root = Path(__file__).resolve().parents[1]
    assert validate_workflow_file(root / "examples" / "workflow-status.json") == []


def test_workflow_requires_all_gates():
    warnings = validate_workflow_record(
        {
            "phase": "PUBLIC_CREDIT_GATE",
            "gates": {"authorization": "PASS"},
            "public_claim_level": "PROVEN",
            "public_evidence_url": "https://example.org/advisory",
        }
    )

    assert warnings
    assert any("missing gates" in warning for warning in warnings)


def test_workflow_rejects_speculative_public_credit():
    record = {
        "phase": "PUBLIC_CREDIT_GATE",
        "gates": {gate: "PASS" for gate in {
            "authorization",
            "boundary_model",
            "evidence",
            "maintainer_invariant",
            "prior_art",
            "hostile_review",
            "report_quality",
            "maintainer_native_validation",
            "disclosure_route",
            "public_credit",
        }},
        "public_claim_level": "SPECULATIVE",
        "public_evidence_url": "https://example.org/advisory",
    }
    record["gates"]["public_credit"] = "PUBLIC_CREDIT_READY"

    warnings = validate_workflow_record(record)

    assert warnings
    assert any("speculative" in warning.lower() for warning in warnings)

