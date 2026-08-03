"""Validate public-safe target, experiment, and maximum-form records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CLAIM_LEVELS = {
    "PROVEN",
    "STRONGLY_SUPPORTED",
    "PLAUSIBLE_NOT_PROVEN",
    "SPECULATIVE",
    "DO_NOT_CLAIM",
}

TARGET_MODES = {"stable_credit", "deep_impact_review", "maintenance_followup"}
TARGET_STATES = {
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
MAX_FORM_DECISIONS = {
    "CONTINUE_TO_REPORT",
    "BANK_AS_STABLE_CREDIT",
    "BANK_AS_HARDENING",
    "REPAIR_BEFORE_REPORT",
    "NO_GO_TRUST_MODEL",
    "MANUAL_BOUNDARY",
}
IMPACT_MARKERS = {
    "CONTROLLED_COMMAND_MARKER",
    "CREDENTIAL_OR_SECRET_EXPOSURE",
    "UNAUTHORIZED_WRITE",
    "AUTHORITY_CHANGE",
    "TRUSTED_ARTIFACT_MUTATION",
    "RELEASE_BUILD_MEMORY_CORRUPTION",
    "MAINTAINER_CONFIRMED_INVARIANT_BREAK",
    "NONE",
}


def _missing_fields(record: dict[str, Any], fields: set[str]) -> list[str]:
    return sorted(field for field in fields if not record.get(field))


def _require_object(record: dict[str, Any], field: str) -> tuple[dict[str, Any], list[str]]:
    value = record.get(field)
    if not isinstance(value, dict):
        return {}, [f"{field} must be an object"]
    return value, []


def _looks_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    lowered = value.strip().lower()
    return lowered in {"", "todo", "tbd", "unknown", "n/a", "<todo>", "<unknown>"}


def validate_target_brief(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    required = {
        "candidate_id",
        "project",
        "component",
        "mode",
        "status",
        "authorization",
        "affected_version",
        "disclosure_route",
        "boundary_model",
        "next_step",
    }
    missing = _missing_fields(record, required)
    if missing:
        warnings.append(f"target brief missing fields: {', '.join(missing)}")

    if record.get("mode") not in TARGET_MODES:
        warnings.append("mode must be stable_credit, deep_impact_review, or maintenance_followup")
    if record.get("status") not in TARGET_STATES:
        warnings.append("status must use the public research state vocabulary")
    if _looks_placeholder(record.get("authorization")):
        warnings.append("authorization must be explicit")

    boundary, boundary_warnings = _require_object(record, "boundary_model")
    warnings.extend(boundary_warnings)
    boundary_required = {
        "lower_trust_actor",
        "higher_trust_consumer",
        "protected_boundary",
        "expected_postcondition",
        "observed_or_suspected_postcondition",
    }
    boundary_missing = _missing_fields(boundary, boundary_required)
    if boundary_missing:
        warnings.append(f"boundary_model missing fields: {', '.join(boundary_missing)}")

    return warnings


def validate_experiment_log(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    required = {
        "candidate_id",
        "project",
        "component",
        "authorization",
        "tested_version",
        "hypothesis",
        "controls",
        "claim_level",
        "status",
        "public_handling",
    }
    missing = _missing_fields(record, required)
    if missing:
        warnings.append(f"experiment log missing fields: {', '.join(missing)}")

    if record.get("claim_level") not in CLAIM_LEVELS:
        warnings.append("claim_level must use the public claim vocabulary")
    if record.get("status") not in TARGET_STATES:
        warnings.append("status must use the public research state vocabulary")
    if _looks_placeholder(record.get("authorization")):
        warnings.append("authorization must be explicit")

    controls, control_warnings = _require_object(record, "controls")
    warnings.extend(control_warnings)
    control_missing = _missing_fields(controls, {"vulnerable_case", "negative_control", "fixed_control"})
    if control_missing:
        warnings.append(f"controls missing fields: {', '.join(control_missing)}")

    public_handling, handling_warnings = _require_object(record, "public_handling")
    warnings.extend(handling_warnings)
    if public_handling.get("safe_to_publish_summary") is True:
        if record.get("claim_level") in {"SPECULATIVE", "DO_NOT_CLAIM"}:
            warnings.append("speculative or do-not-claim experiments cannot be marked safe to publish")

    return warnings


def validate_maximum_form_review(record: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    required = {
        "candidate_id",
        "project",
        "component",
        "current_state",
        "emergency_thesis",
        "impact_marker",
        "claim_level",
        "maintainer_objection",
        "capability_closure",
        "decision",
    }
    missing = _missing_fields(record, required)
    if missing:
        warnings.append(f"maximum-form review missing fields: {', '.join(missing)}")

    if record.get("current_state") not in TARGET_STATES:
        warnings.append("current_state must use the public research state vocabulary")
    if record.get("claim_level") not in CLAIM_LEVELS:
        warnings.append("claim_level must use the public claim vocabulary")
    if record.get("impact_marker") not in IMPACT_MARKERS:
        warnings.append("impact_marker must use the public maximum-form marker vocabulary")
    if record.get("decision") not in MAX_FORM_DECISIONS:
        warnings.append("decision must use the public maximum-form decision vocabulary")

    thesis = str(record.get("emergency_thesis", ""))
    if len(thesis.split()) < 12:
        warnings.append("emergency_thesis must name actor, consumer, effect, and workflow")

    closure, closure_warnings = _require_object(record, "capability_closure")
    warnings.extend(closure_warnings)
    closure_missing = _missing_fields(
        closure,
        {"current_proven_capability", "plausible_unproven_capability", "blocked_routes"},
    )
    if closure_missing:
        warnings.append(f"capability_closure missing fields: {', '.join(closure_missing)}")

    if record.get("decision") == "CONTINUE_TO_REPORT":
        if record.get("claim_level") not in {"PROVEN", "STRONGLY_SUPPORTED"}:
            warnings.append("CONTINUE_TO_REPORT requires a proven or strongly supported claim")
        if record.get("impact_marker") == "NONE":
            warnings.append("CONTINUE_TO_REPORT requires a concrete impact marker")

    return warnings


def validate_record(kind: str, record: dict[str, Any]) -> list[str]:
    if kind == "target-brief":
        return validate_target_brief(record)
    if kind == "experiment":
        return validate_experiment_log(record)
    if kind == "max-form":
        return validate_maximum_form_review(record)
    return [f"unknown record kind: {kind}"]


def validate_record_file(kind: str, path: Path) -> list[str]:
    return validate_record(kind, json.loads(path.read_text(encoding="utf-8")))


def scaffold_record(kind: str, candidate_id: str, project: str, component: str) -> dict[str, Any]:
    if kind == "target-brief":
        return {
            "candidate_id": candidate_id,
            "project": project,
            "component": component,
            "mode": "stable_credit",
            "status": "INTAKE",
            "authorization": "local lab, owned code, public OSS review, or explicit authorization",
            "affected_version": "commit-or-version",
            "disclosure_route": "private security advisory or project security policy",
            "boundary_model": {
                "lower_trust_actor": "lower-trust actor or input",
                "higher_trust_consumer": "higher-trust component",
                "protected_boundary": "protected boundary",
                "expected_postcondition": "expected secure postcondition",
                "observed_or_suspected_postcondition": "observed or suspected broken postcondition",
            },
            "next_step": "build authorized evidence and controls",
        }
    if kind == "experiment":
        return {
            "candidate_id": candidate_id,
            "project": project,
            "component": component,
            "authorization": "local lab, owned code, public OSS review, or explicit authorization",
            "tested_version": "commit-or-version",
            "hypothesis": "security hypothesis to test",
            "controls": {
                "vulnerable_case": "authorized vulnerable observation",
                "negative_control": "case that should not trigger the behavior",
                "fixed_control": "patched or mitigated behavior when available",
            },
            "claim_level": "PLAUSIBLE_NOT_PROVEN",
            "status": "EVIDENCE_BUILT",
            "public_handling": {
                "safe_to_publish_summary": False,
                "private_material_retained_elsewhere": True,
                "public_evidence_url": "",
            },
        }
    if kind == "max-form":
        return {
            "candidate_id": candidate_id,
            "project": project,
            "component": component,
            "current_state": "HOSTILE_REVIEWED",
            "emergency_thesis": (
                "A lower-trust actor can make a higher-trust deployed consumer "
                "produce a concrete security effect in a common workflow."
            ),
            "impact_marker": "NONE",
            "claim_level": "PLAUSIBLE_NOT_PROVEN",
            "maintainer_objection": "strongest likely maintainer objection",
            "capability_closure": {
                "current_proven_capability": "current proven capability",
                "plausible_unproven_capability": "stronger capability not yet proven",
                "blocked_routes": ["routes blocked by authorization, safety, or lab fidelity"],
            },
            "decision": "REPAIR_BEFORE_REPORT",
        }
    raise ValueError(f"unknown record kind: {kind}")


def write_scaffold(path: Path, record: dict[str, Any], force: bool = False) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
