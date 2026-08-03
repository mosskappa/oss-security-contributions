"""Advanced public-safe workflow gates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .core import MODES


CLAIM_BOUNDARY_FIELDS = {"proven", "plausible_not_proven", "do_not_claim"}
VERDICTS = {"KEEP", "KEEP_WITH_CAUTION", "REPAIR", "DOWNGRADE", "DROP"}
MAX_FORM_DECISIONS = {
    "CONTINUE_TO_REPORT",
    "BANK_AS_STABLE_CREDIT",
    "BANK_AS_HARDENING",
    "REPAIR_BEFORE_REPORT",
    "NO_GO_TRUST_MODEL",
    "MANUAL_BOUNDARY",
}
STOP_REASONS = {
    "REPORT_READY_NEEDS_USER_APPROVAL",
    "PUBLIC_WRITEUP_READY",
    "BANKED_HARDENING",
    "NO_GO_WITH_EVIDENCE",
    "BLOCKED_NEEDS_AUTHORITY",
    "ROUND_EXHAUSTED_WITH_NEXT_SCOPE",
}
VALIDATION_LEVELS = {
    "LEVEL_1_SUMMARY",
    "LEVEL_2_NATIVE_VALIDATION",
    "LEVEL_3_INTERNAL_PROOF_PRIVATE",
}
DISCLOSURE_ROUTES = {
    "PRIVATE_SECURITY_ADVISORY",
    "PROJECT_SECURITY_CONTACT",
    "MAINTAINER_REQUESTED_PRIVATE",
    "PUBLIC_HARDENING_ONLY",
    "PUBLIC_ALREADY_DISCLOSED",
}
RISKY_COMMAND_PATTERNS = [
    re.compile(r"(?i)\b(curl|nc|netcat|msfconsole|meterpreter)\b"),
    re.compile(r"(?i)\b(powershell\s+-enc|bash\s+-i|/dev/tcp)\b"),
    re.compile(r"(?i)\b(real\s+token|production|third[- ]party target)\b"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing(record: dict[str, Any], required: set[str]) -> list[str]:
    missing: list[str] = []
    for field in required:
        if field not in record:
            missing.append(field)
            continue
        value = record.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)
    return sorted(missing)


def _require_non_empty_list(record: dict[str, Any], field: str, warnings: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        warnings.append(f"{field} must be a non-empty list")


def _validate_claim_boundaries(record: dict[str, Any], warnings: list[str]) -> None:
    boundaries = record.get("claim_boundaries")
    if not isinstance(boundaries, dict):
        warnings.append("claim_boundaries must be an object")
        return
    for field in sorted(CLAIM_BOUNDARY_FIELDS):
        value = boundaries.get(field)
        if not isinstance(value, list) or not value:
            warnings.append(f"claim_boundaries.{field} must be a non-empty list")


def validate_start_mode(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = _missing(record, {"requested_mode", "chosen_mode", "reason", "next_action"})
    if missing:
        warnings.append(f"start mode missing fields: {', '.join(missing)}")
    if record.get("chosen_mode") not in MODES:
        warnings.append("chosen_mode must use the public mode vocabulary")
    if record.get("requested_mode") == "ambiguous" and "default" not in str(record.get("reason", "")).lower():
        warnings.append("ambiguous start mode should explain the default choice")
    return warnings


def validate_reproducer_ready(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = _missing(
        record,
        {
            "candidate_id",
            "authorization",
            "validation_level",
            "command_summary",
            "controls",
            "expected_markers",
            "cleanup",
            "run_id_policy",
            "non_claims",
        },
    )
    if missing:
        warnings.append(f"reproducer-ready missing fields: {', '.join(missing)}")
    if record.get("validation_level") not in VALIDATION_LEVELS:
        warnings.append("validation_level must use the public validation vocabulary")
    command_summary = str(record.get("command_summary", ""))
    for pattern in RISKY_COMMAND_PATTERNS:
        if pattern.search(command_summary):
            warnings.append(f"command_summary matched risky command pattern: {pattern.pattern}")
    controls = record.get("controls")
    if not isinstance(controls, dict):
        warnings.append("controls must be an object")
    else:
        for field in {"affected_case", "negative_control", "fixed_control"}:
            if not controls.get(field):
                warnings.append(f"controls missing {field}")
    _require_non_empty_list(record, "expected_markers", warnings)
    _require_non_empty_list(record, "non_claims", warnings)
    if "private" not in str(record.get("run_id_policy", "")).lower() and "synthetic" not in str(
        record.get("run_id_policy", "")
    ).lower():
        warnings.append("run_id_policy should say how private or synthetic run identifiers are handled")
    return warnings


def validate_hostile_review(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = _missing(
        record,
        {
            "candidate_id",
            "reviewer_mode",
            "maintainer_objections",
            "claim_boundaries",
            "prior_art_status",
            "max_form_decision",
            "verdict",
            "repair_items",
        },
    )
    if missing:
        warnings.append(f"hostile review missing fields: {', '.join(missing)}")
    _require_non_empty_list(record, "maintainer_objections", warnings)
    _validate_claim_boundaries(record, warnings)
    if record.get("max_form_decision") not in MAX_FORM_DECISIONS:
        warnings.append("max_form_decision must use the maximum-form decision vocabulary")
    if record.get("verdict") not in VERDICTS:
        warnings.append("verdict must use the hostile-review vocabulary")
    if record.get("verdict") == "KEEP" and record.get("repair_items"):
        warnings.append("KEEP verdict should not have repair_items")
    return warnings


def validate_long_run_final(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = _missing(
        record,
        {
            "mode",
            "candidate_id",
            "terminal_reason",
            "stop_allowed",
            "frontier_closure",
            "claim_boundaries",
            "tests_run",
            "files_updated",
            "next_action",
        },
    )
    if missing:
        warnings.append(f"long-run final missing fields: {', '.join(missing)}")
    if record.get("mode") not in MODES:
        warnings.append("mode must use the public mode vocabulary")
    if record.get("terminal_reason") not in STOP_REASONS:
        warnings.append("terminal_reason must use the public stop-reason vocabulary")
    if record.get("stop_allowed") is not True:
        warnings.append("stop_allowed must be true for a final handoff")
    closure = record.get("frontier_closure")
    if not isinstance(closure, dict):
        warnings.append("frontier_closure must be an object")
    else:
        for field in {"current_tier", "next_plausible_tier", "routes_closed", "why_no_more_now"}:
            if not closure.get(field):
                warnings.append(f"frontier_closure missing {field}")
    _validate_claim_boundaries(record, warnings)
    _require_non_empty_list(record, "tests_run", warnings)
    _require_non_empty_list(record, "files_updated", warnings)
    return warnings


def validate_disclosure_manifest(record: dict[str, Any], base_dir: Path | None = None) -> list[str]:
    warnings: list[str] = []
    missing = _missing(record, {"package_id", "route", "files", "excluded_material", "approval_required"})
    if missing:
        warnings.append(f"disclosure manifest missing fields: {', '.join(missing)}")
    if record.get("route") not in DISCLOSURE_ROUTES:
        warnings.append("route must use the public disclosure route vocabulary")
    files = record.get("files")
    if not isinstance(files, list) or not files:
        warnings.append("files must be a non-empty list")
    else:
        for item in files:
            if not isinstance(item, dict):
                warnings.append("file entries must be objects")
                continue
            for field in {"path", "purpose", "public_safe"}:
                if field not in item:
                    warnings.append(f"file entry missing {field}")
            if item.get("public_safe") is not True:
                warnings.append(f"{item.get('path', '<unknown>')}: public_safe must be true")
            if base_dir and item.get("path"):
                candidate = (base_dir / str(item["path"])).resolve()
                try:
                    candidate.relative_to(base_dir.resolve())
                except ValueError:
                    warnings.append(f"{item['path']}: file path escapes package directory")
                if not candidate.exists():
                    warnings.append(f"{item['path']}: listed file does not exist")
    _require_non_empty_list(record, "excluded_material", warnings)
    _require_non_empty_list(record, "approval_required", warnings)
    return warnings


def validate_synthetic_lab(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    missing = _missing(
        record,
        {
            "lab_id",
            "scope",
            "external_network",
            "third_party_targets",
            "destructive_actions",
            "scenarios",
            "success_markers",
        },
    )
    if missing:
        warnings.append(f"synthetic lab missing fields: {', '.join(missing)}")
    if record.get("scope") != "synthetic_only":
        warnings.append("scope must be synthetic_only")
    for field in {"external_network", "third_party_targets", "destructive_actions"}:
        if record.get(field) is not False:
            warnings.append(f"{field} must be false")
    scenarios = record.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        warnings.append("scenarios must be a non-empty list")
    else:
        for scenario in scenarios:
            if not isinstance(scenario, dict):
                warnings.append("scenario entries must be objects")
                continue
            for field in {"name", "actor", "consumer", "boundary", "controls"}:
                if not scenario.get(field):
                    warnings.append(f"scenario missing {field}")
    _require_non_empty_list(record, "success_markers", warnings)
    return warnings


def validate_file(kind: str, path: Path) -> list[str]:
    record = load_json(path)
    if kind == "start-mode":
        return validate_start_mode(record)
    if kind == "reproducer-ready":
        return validate_reproducer_ready(record)
    if kind == "hostile-review":
        return validate_hostile_review(record)
    if kind == "long-run-final":
        return validate_long_run_final(record)
    if kind == "disclosure-manifest":
        return validate_disclosure_manifest(record, base_dir=path.parent)
    if kind == "synthetic-lab":
        return validate_synthetic_lab(record)
    return [f"unknown advanced gate kind: {kind}"]
