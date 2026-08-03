"""Public-safe research control-plane helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any

from .state_machine import STATES


MODES = {"stable_credit", "deep_impact_review", "maintenance_followup"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
REQUIRED_BOUNDARY_FIELDS = {
    "lower_trust_actor",
    "higher_trust_consumer",
    "protected_boundary",
    "expected_postcondition",
    "observed_or_suspected_postcondition",
}
READY_GATES = {
    "authorization",
    "boundary_model",
    "evidence",
    "maintainer_invariant",
    "prior_art",
    "hostile_review",
    "report_quality",
    "disclosure_route",
}


@dataclass(frozen=True)
class RegistrySummary:
    total: int
    by_status: dict[str, int]
    claimed: int
    next_steps: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "by_status": self.by_status,
            "claimed": self.claimed,
            "next_steps": self.next_steps,
        }


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def is_claim_active(claim: dict[str, Any] | None, at: datetime | None = None) -> bool:
    if not isinstance(claim, dict):
        return False
    expires = parse_iso(str(claim.get("expires_at", "")))
    if expires is None:
        return False
    return expires > (at or now_utc())


def candidate_ids(registry: dict[str, Any]) -> list[str]:
    return [str(candidate.get("candidate_id", "")) for candidate in registry.get("candidates", [])]


def find_candidate(registry: dict[str, Any], candidate_id: str) -> dict[str, Any] | None:
    for candidate in registry.get("candidates", []):
        if candidate.get("candidate_id") == candidate_id:
            return candidate
    return None


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    required = {
        "candidate_id",
        "project",
        "component",
        "mode",
        "status",
        "priority",
        "authorization",
        "boundary_model",
        "gates",
        "next_step",
    }
    missing = sorted(field for field in required if not candidate.get(field))
    if missing:
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: missing fields: {', '.join(missing)}")

    if candidate.get("mode") not in MODES:
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: invalid mode")
    if candidate.get("status") not in STATES:
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: invalid status")
    if candidate.get("priority") not in PRIORITIES:
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: invalid priority")

    boundary = candidate.get("boundary_model")
    if not isinstance(boundary, dict):
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: boundary_model must be an object")
    else:
        missing_boundary = sorted(field for field in REQUIRED_BOUNDARY_FIELDS if not boundary.get(field))
        if missing_boundary:
            warnings.append(
                f"{candidate.get('candidate_id', '<unknown>')}: boundary_model missing: {', '.join(missing_boundary)}"
            )

    gates = candidate.get("gates")
    if not isinstance(gates, dict):
        warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: gates must be an object")
    elif candidate.get("status") == "REPORT_READY":
        missing_gates = sorted(gate for gate in READY_GATES if not gates.get(gate))
        if missing_gates:
            warnings.append(
                f"{candidate.get('candidate_id', '<unknown>')}: REPORT_READY missing gates: {', '.join(missing_gates)}"
            )

    claim = candidate.get("claim")
    if claim is not None:
        if not isinstance(claim, dict):
            warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: claim must be null or an object")
        elif is_claim_active(claim):
            for field in {"owner", "purpose", "claimed_at", "expires_at"}:
                if not claim.get(field):
                    warnings.append(f"{candidate.get('candidate_id', '<unknown>')}: active claim missing {field}")

    return warnings


def validate_registry(registry: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if registry.get("registry_version") != 1:
        warnings.append("registry_version must be 1")
    candidates = registry.get("candidates")
    if not isinstance(candidates, list):
        return warnings + ["candidates must be a list"]

    ids = candidate_ids(registry)
    duplicates = sorted({candidate_id for candidate_id in ids if ids.count(candidate_id) > 1})
    if duplicates:
        warnings.append(f"duplicate candidate ids: {', '.join(duplicates)}")

    for candidate in candidates:
        if not isinstance(candidate, dict):
            warnings.append("candidate entries must be objects")
            continue
        warnings.extend(validate_candidate(candidate))

    return warnings


def validate_registry_file(path: Path) -> list[str]:
    return validate_registry(load_json(path))


def summarize_registry(registry: dict[str, Any]) -> RegistrySummary:
    by_status: dict[str, int] = {}
    claimed = 0
    next_steps: list[str] = []
    for candidate in registry.get("candidates", []):
        status = str(candidate.get("status", "UNKNOWN"))
        by_status[status] = by_status.get(status, 0) + 1
        if is_claim_active(candidate.get("claim")):
            claimed += 1
        next_step = candidate.get("next_step")
        if next_step:
            next_steps.append(f"{candidate.get('candidate_id')}: {next_step}")
    return RegistrySummary(
        total=len(registry.get("candidates", [])),
        by_status=dict(sorted(by_status.items())),
        claimed=claimed,
        next_steps=next_steps,
    )


def scaffold_candidate(candidate_id: str, project: str, component: str, mode: str = "stable_credit") -> dict[str, Any]:
    if mode not in MODES:
        raise ValueError(f"invalid mode: {mode}")
    return {
        "candidate_id": candidate_id,
        "project": project,
        "component": component,
        "mode": mode,
        "status": "INTAKE",
        "priority": "P2",
        "authorization": "public OSS review, local lab, owned code, or explicit authorization",
        "boundary_model": {
            "lower_trust_actor": "lower-trust actor or input",
            "higher_trust_consumer": "higher-trust component",
            "protected_boundary": "protected boundary",
            "expected_postcondition": "expected secure postcondition",
            "observed_or_suspected_postcondition": "observed or suspected broken postcondition",
        },
        "gates": {
            "authorization": "PASS",
            "boundary_model": "PENDING",
            "evidence": "PENDING",
            "maintainer_invariant": "PENDING",
            "prior_art": "PENDING",
            "hostile_review": "PENDING",
            "maximum_form": "PENDING",
            "report_quality": "PENDING",
            "disclosure_route": "PENDING",
            "public_credit": "PENDING",
        },
        "claim": None,
        "next_step": "write boundary model and evidence plan",
    }


def append_candidate(path: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    registry = load_json(path) if path.exists() else {"registry_version": 1, "candidates": []}
    if find_candidate(registry, str(candidate["candidate_id"])):
        raise ValueError(f"candidate already exists: {candidate['candidate_id']}")
    registry.setdefault("candidates", []).append(candidate)
    warnings = validate_registry(registry)
    if warnings:
        raise ValueError("; ".join(warnings))
    write_json(path, registry)
    return registry


def claim_candidate(path: Path, candidate_id: str, owner: str, purpose: str, ttl_hours: float) -> dict[str, Any]:
    registry = load_json(path)
    candidate = find_candidate(registry, candidate_id)
    if candidate is None:
        raise ValueError(f"candidate not found: {candidate_id}")
    claim = candidate.get("claim")
    if is_claim_active(claim) and claim.get("owner") != owner:
        raise ValueError(f"candidate already claimed by {claim.get('owner')} until {claim.get('expires_at')}")
    claimed_at = now_utc()
    candidate["claim"] = {
        "owner": owner,
        "purpose": purpose,
        "claimed_at": iso(claimed_at),
        "expires_at": iso(claimed_at + timedelta(hours=ttl_hours)),
    }
    write_json(path, registry)
    return candidate


def release_candidate(path: Path, candidate_id: str, owner: str | None = None) -> dict[str, Any]:
    registry = load_json(path)
    candidate = find_candidate(registry, candidate_id)
    if candidate is None:
        raise ValueError(f"candidate not found: {candidate_id}")
    claim = candidate.get("claim")
    if owner and is_claim_active(claim) and claim.get("owner") != owner:
        raise ValueError(f"candidate is claimed by {claim.get('owner')}, not {owner}")
    candidate["claim"] = None
    write_json(path, registry)
    return candidate
