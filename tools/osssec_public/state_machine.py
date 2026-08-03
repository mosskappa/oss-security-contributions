"""Validate public-safe research state transitions."""

from __future__ import annotations

import json
from pathlib import Path


STATES = {
    "INTAKE",
    "BOUNDARY_MODELED",
    "EVIDENCE_BUILT",
    "INVARIANT_REVIEWED",
    "PRIOR_ART_REVIEWED",
    "HOSTILE_REVIEWED",
    "REPORT_READY",
    "DISCLOSED_PRIVATE",
    "PATCH_VALIDATION",
    "PUBLIC_CREDIT_READY",
    "BANKED_HARDENING",
    "NO_GO",
    "BLOCKED",
}

ALLOWED_TRANSITIONS = {
    "INTAKE": {"BOUNDARY_MODELED", "NO_GO", "BLOCKED"},
    "BOUNDARY_MODELED": {"EVIDENCE_BUILT", "BANKED_HARDENING", "NO_GO", "BLOCKED"},
    "EVIDENCE_BUILT": {"INVARIANT_REVIEWED", "BANKED_HARDENING", "NO_GO", "BLOCKED"},
    "INVARIANT_REVIEWED": {"PRIOR_ART_REVIEWED", "BANKED_HARDENING", "NO_GO", "BLOCKED"},
    "PRIOR_ART_REVIEWED": {"HOSTILE_REVIEWED", "NO_GO", "BLOCKED"},
    "HOSTILE_REVIEWED": {"REPORT_READY", "BANKED_HARDENING", "NO_GO", "BLOCKED"},
    "REPORT_READY": {"DISCLOSED_PRIVATE", "BLOCKED"},
    "DISCLOSED_PRIVATE": {"PATCH_VALIDATION", "BLOCKED"},
    "PATCH_VALIDATION": {"PUBLIC_CREDIT_READY", "BANKED_HARDENING", "BLOCKED"},
    "BANKED_HARDENING": {"PUBLIC_CREDIT_READY", "NO_GO"},
    "BLOCKED": {"BOUNDARY_MODELED", "EVIDENCE_BUILT", "REPORT_READY", "PATCH_VALIDATION", "NO_GO"},
}

REPORT_READY_REQUIRED_GATES = {
    "authorization",
    "boundary_model",
    "evidence",
    "maintainer_invariant",
    "prior_art",
    "hostile_review",
    "report_quality",
    "disclosure_route",
}

PUBLIC_CREDIT_REQUIRED_GATES = REPORT_READY_REQUIRED_GATES | {"public_credit"}

PUBLIC_CLAIM_LEVELS = {"PROVEN", "STRONGLY_SUPPORTED"}


def validate_state_record(record: dict) -> list[str]:
    warnings: list[str] = []
    current = record.get("current_state")
    previous = record.get("previous_state")
    gates = record.get("gates", {})

    if current not in STATES:
        warnings.append("current_state must use the public state vocabulary")
    if previous is not None and previous not in STATES:
        warnings.append("previous_state must use the public state vocabulary")

    if previous in ALLOWED_TRANSITIONS and current in STATES:
        if current != previous and current not in ALLOWED_TRANSITIONS[previous]:
            warnings.append(f"transition {previous} -> {current} is not allowed")

    if not isinstance(gates, dict):
        warnings.append("gates must be an object")
        gates = {}

    if current == "REPORT_READY":
        missing = sorted(REPORT_READY_REQUIRED_GATES - set(gates))
        if missing:
            warnings.append(f"REPORT_READY missing gates: {', '.join(missing)}")

    if current == "PUBLIC_CREDIT_READY":
        missing = sorted(PUBLIC_CREDIT_REQUIRED_GATES - set(gates))
        if missing:
            warnings.append(f"PUBLIC_CREDIT_READY missing gates: {', '.join(missing)}")
        if not str(record.get("public_evidence_url", "")).startswith("https://"):
            warnings.append("PUBLIC_CREDIT_READY requires an https public_evidence_url")
        if record.get("claim_level") not in PUBLIC_CLAIM_LEVELS:
            warnings.append("PUBLIC_CREDIT_READY requires a proven or strongly supported claim")

    if current == "BANKED_HARDENING" and record.get("claim_level") == "PROVEN":
        if record.get("public_wording") not in {"hardening", "maintainer_support"}:
            warnings.append("banked hardening must use hardening or maintainer-support wording")

    return warnings


def validate_state_file(path: Path) -> list[str]:
    return validate_state_record(json.loads(path.read_text(encoding="utf-8")))


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "examples" / "workflow-status.json"
    warnings = validate_state_file(path)
    if warnings:
        print("State-machine validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("State-machine validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
