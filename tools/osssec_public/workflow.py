"""Validate public-safe workflow status records."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_GATES = {
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
}

CLAIM_LEVELS = {
    "PROVEN",
    "STRONGLY_SUPPORTED",
    "PLAUSIBLE_NOT_PROVEN",
    "SPECULATIVE",
    "DO_NOT_CLAIM",
}


def validate_workflow_record(record: dict) -> list[str]:
    warnings: list[str] = []

    gates = record.get("gates")
    if not isinstance(gates, dict):
        return ["workflow record must contain a gates object"]

    missing = sorted(REQUIRED_GATES - set(gates))
    if missing:
        warnings.append(f"missing gates: {', '.join(missing)}")

    claim_level = record.get("public_claim_level")
    if claim_level not in CLAIM_LEVELS:
        warnings.append("public_claim_level must use the public claim vocabulary")

    evidence_url = record.get("public_evidence_url", "")
    if record.get("phase") == "PUBLIC_CREDIT_GATE" and not str(evidence_url).startswith("https://"):
        warnings.append("public credit phase requires an https public evidence URL")

    if gates.get("public_credit") == "PUBLIC_CREDIT_READY" and claim_level in {
        "SPECULATIVE",
        "DO_NOT_CLAIM",
    }:
        warnings.append("public credit cannot be ready for speculative or do-not-claim items")

    return warnings


def validate_workflow_file(path: Path) -> list[str]:
    record = json.loads(path.read_text(encoding="utf-8"))
    return validate_workflow_record(record)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "examples" / "workflow-status.json"
    warnings = validate_workflow_file(path)
    if warnings:
        print("Workflow validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Workflow validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

