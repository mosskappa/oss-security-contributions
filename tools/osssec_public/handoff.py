"""Validate public-safe session close and final handoff records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SESSION_CLOSE_REQUIRED = {
    "date",
    "mode",
    "candidate_id",
    "current_state",
    "work_completed",
    "evidence_or_artifacts",
    "decisions",
    "state_changes",
    "blockers",
    "tests_run",
    "claim_boundaries",
    "next_concrete_step",
}

FINAL_HANDOFF_REQUIRED_HEADINGS = {
    "Terminal Reason",
    "Current State",
    "Evidence",
    "Claim Boundaries",
    "Tests",
    "Files Updated",
    "Next Action",
}


def validate_session_close(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = sorted(field for field in SESSION_CLOSE_REQUIRED if field not in record)
    if missing:
        warnings.append(f"session close missing fields: {', '.join(missing)}")
    for field in {"work_completed", "evidence_or_artifacts", "decisions", "state_changes", "tests_run"}:
        value = record.get(field)
        if not isinstance(value, list) or not value:
            warnings.append(f"{field} must be a non-empty list")
    boundaries = record.get("claim_boundaries")
    if not isinstance(boundaries, dict):
        warnings.append("claim_boundaries must be an object")
    else:
        for field in {"proven", "plausible_not_proven", "do_not_claim"}:
            if field not in boundaries:
                warnings.append(f"claim_boundaries missing {field}")
    if not str(record.get("next_concrete_step", "")).strip():
        warnings.append("next_concrete_step must be explicit")
    return warnings


def validate_session_close_file(path: Path) -> list[str]:
    return validate_session_close(json.loads(path.read_text(encoding="utf-8")))


def validate_final_handoff_text(text: str) -> list[str]:
    warnings: list[str] = []
    for heading in sorted(FINAL_HANDOFF_REQUIRED_HEADINGS):
        if f"## {heading}" not in text:
            warnings.append(f"final handoff missing heading: {heading}")
    for marker in {"PROVEN:", "PLAUSIBLE_NOT_PROVEN:", "DO_NOT_CLAIM:"}:
        if marker not in text:
            warnings.append(f"final handoff missing claim marker: {marker}")
    if "tests blocked" in text.lower() and "reason" not in text.lower():
        warnings.append("blocked tests must include a reason")
    if "Next Action" in text and "<" in text:
        warnings.append("next action appears to contain a placeholder")
    return warnings


def validate_final_handoff_file(path: Path) -> list[str]:
    return validate_final_handoff_text(path.read_text(encoding="utf-8"))
