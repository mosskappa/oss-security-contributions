"""One-command public-safe workflow workspace orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import advanced_gates, core, gate_records, handoff, package_hygiene, safety


WORKSPACE_FILES = {
    "registry": "registry.json",
    "target": "target-brief.json",
    "experiment": "experiment-log.json",
    "max_form": "maximum-form-review.json",
    "reproducer": "reproducer-ready.json",
    "hostile": "hostile-review.json",
    "long_run": "long-run-final.json",
    "session": "session-close.json",
    "handoff": "final-handoff.md",
    "package_dir": "public-package",
    "package_report": "public-package/report.md",
    "package_boundaries": "public-package/public-boundaries.md",
    "package_manifest": "public-package/disclosure-manifest.json",
    "lab_manifest": "synthetic-lab/manifest.json",
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    path: Path
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.warnings

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path),
            "ok": self.ok,
            "warnings": self.warnings,
        }


def _write_json(path: Path, data: dict[str, Any]) -> None:
    core.write_json(path, data)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _candidate_defaults(candidate_id: str, project: str, component: str, mode: str) -> dict[str, Any]:
    candidate = core.scaffold_candidate(candidate_id, project, component, mode=mode)
    candidate["status"] = "BOUNDARY_MODELED"
    candidate["priority"] = "P2"
    candidate["gates"]["boundary_model"] = "PASS"
    candidate["next_step"] = "fill or review experiment-log.json, then run validate"
    return candidate


def create_workspace(
    root: Path,
    candidate_id: str,
    project: str,
    component: str,
    mode: str,
    force: bool = False,
) -> Path:
    if root.exists() and any(root.iterdir()) and not force:
        raise FileExistsError(f"workspace already exists and is not empty: {root}")
    root.mkdir(parents=True, exist_ok=True)

    registry = {"registry_version": 1, "candidates": [_candidate_defaults(candidate_id, project, component, mode)]}
    _write_json(root / WORKSPACE_FILES["registry"], registry)

    target = gate_records.scaffold_record("target-brief", candidate_id, project, component)
    target["mode"] = mode
    target["status"] = "BOUNDARY_MODELED"
    target["affected_version"] = "synthetic-or-public-commit"
    target["boundary_model"] = registry["candidates"][0]["boundary_model"]
    _write_json(root / WORKSPACE_FILES["target"], target)

    experiment = gate_records.scaffold_record("experiment", candidate_id, project, component)
    experiment["tested_version"] = "synthetic-or-public-commit"
    experiment["claim_level"] = "PLAUSIBLE_NOT_PROVEN"
    experiment["status"] = "EVIDENCE_BUILT"
    _write_json(root / WORKSPACE_FILES["experiment"], experiment)

    max_form = gate_records.scaffold_record("max-form", candidate_id, project, component)
    max_form["current_state"] = "HOSTILE_REVIEWED"
    max_form["decision"] = "REPAIR_BEFORE_REPORT"
    _write_json(root / WORKSPACE_FILES["max_form"], max_form)

    _write_json(
        root / WORKSPACE_FILES["reproducer"],
        {
            "candidate_id": candidate_id,
            "authorization": "synthetic local lab or explicit authorization only",
            "validation_level": "LEVEL_2_NATIVE_VALIDATION",
            "command_summary": "project-native synthetic validation command shape; exact private commands are not published",
            "controls": {
                "affected_case": "synthetic marker appears in the affected flow",
                "negative_control": "marker is absent when the boundary is not crossed",
                "fixed_control": "marker is rejected after the synthetic fix",
            },
            "expected_markers": ["SYNTHETIC_BOUNDARY_MARKER", "NEGATIVE_CONTROL_CLEAN", "FIXED_CONTROL_CLEAN"],
            "cleanup": "synthetic workspace removal only",
            "run_id_policy": "synthetic run identifiers are allowed; private run identifiers stay outside this workspace",
            "non_claims": [
                "no real vulnerability is claimed",
                "no target-specific proof material is included",
                "no third-party system is tested",
            ],
        },
    )

    _write_json(
        root / WORKSPACE_FILES["hostile"],
        {
            "candidate_id": candidate_id,
            "reviewer_mode": "maintainer_objection",
            "maintainer_objections": [
                "The behavior may be expected design unless the boundary promise is documented.",
                "The synthetic marker does not prove impact in a real project.",
            ],
            "claim_boundaries": {
                "proven": ["the public-safe candidate has a written boundary model"],
                "plausible_not_proven": ["a real project may have a similar issue shape"],
                "do_not_claim": ["no real affected project, CVE, or production impact"],
            },
            "prior_art_status": "synthetic example; no novelty claim",
            "max_form_decision": "REPAIR_BEFORE_REPORT",
            "verdict": "REPAIR",
            "repair_items": ["replace synthetic placeholders with authorized evidence before any report-ready claim"],
        },
    )

    _write_json(
        root / WORKSPACE_FILES["long_run"],
        {
            "mode": mode,
            "candidate_id": candidate_id,
            "terminal_reason": "ROUND_EXHAUSTED_WITH_NEXT_SCOPE",
            "stop_allowed": True,
            "frontier_closure": {
                "current_tier": "public-safe scaffold",
                "next_plausible_tier": "authorized evidence with affected, negative, and fixed controls",
                "routes_closed": ["real-project testing is outside the scaffold"],
                "why_no_more_now": "the next step requires user-supplied authorized evidence",
            },
            "claim_boundaries": {
                "proven": ["public-safe workflow artifacts validate"],
                "plausible_not_proven": ["real-world impact"],
                "do_not_claim": ["no real vulnerability or private report"],
            },
            "tests_run": [f"osssec-public validate {root.as_posix()}"],
            "tests_blocked": [],
            "files_updated": ["registry.json", "target-brief.json", "experiment-log.json"],
            "next_action": "replace synthetic placeholders with authorized evidence and rerun validate",
        },
    )

    _write_json(
        root / WORKSPACE_FILES["session"],
        {
            "date": "2099-01-01",
            "mode": mode,
            "candidate_id": candidate_id,
            "current_state": "BOUNDARY_MODELED",
            "work_completed": ["created public-safe workflow workspace"],
            "evidence_or_artifacts": ["target-brief.json", "experiment-log.json", "maximum-form-review.json"],
            "decisions": ["continue only with public, local, owned, or explicitly authorized evidence"],
            "state_changes": ["INTAKE -> BOUNDARY_MODELED"],
            "blockers": [],
            "tests_run": [f"osssec-public validate {root.as_posix()}"],
            "claim_boundaries": {
                "proven": ["public-safe artifacts exist"],
                "plausible_not_proven": ["real project impact"],
                "do_not_claim": ["no real vulnerability is claimed by this scaffold"],
            },
            "next_concrete_step": "fill evidence-specific fields and rerun validate",
        },
    )

    _write_text(
        root / WORKSPACE_FILES["handoff"],
        f"""# Public-Safe Final Handoff

## Terminal Reason

Workspace scaffold is ready for authorized evidence.

## Current State

- candidate id: {candidate_id}
- state: BOUNDARY_MODELED
- decision: continue to evidence gate

## Evidence

- public-safe target brief exists
- public-safe registry entry validates
- no real vulnerability or private target is included

## Claim Boundaries

PROVEN: public-safe workflow scaffold validates.

PLAUSIBLE_NOT_PROVEN: whether a real project has the same issue.

DO_NOT_CLAIM: no real exploitability, CVE, bounty, or maintainer impact is claimed.

## Tests

- osssec-public validate {root.as_posix()}

## Files Updated

- registry.json
- target-brief.json
- experiment-log.json

## Next Action

Replace synthetic placeholders with authorized evidence and rerun validate.
""",
    )

    _write_text(
        root / WORKSPACE_FILES["package_report"],
        f"""# Public-Safe Synthetic Report

Candidate `{candidate_id}` demonstrates package shape only. It does not
describe a real vulnerability, exploit, target, vendor case, or private
disclosure.

## Summary

A lower-trust synthetic input is modeled as reaching a higher-trust synthetic
consumer. This report is useful only for validating public package hygiene.

## Non-Claims

- no real affected project;
- no real CVE or GHSA;
- no exploit material;
- no private correspondence.
""",
    )
    _write_text(
        root / WORKSPACE_FILES["package_boundaries"],
        """# Public Boundaries

This package contains synthetic material only. Private targets, payloads,
credentials, logs, browser state, reports, and vendor correspondence are not
included.
""",
    )
    _write_json(
        root / WORKSPACE_FILES["package_manifest"],
        {
            "package_id": f"{candidate_id}-PACKAGE",
            "route": "PUBLIC_HARDENING_ONLY",
            "files": [
                {"path": "report.md", "purpose": "synthetic public-safe report body", "public_safe": True},
                {"path": "public-boundaries.md", "purpose": "public handling boundaries", "public_safe": True},
            ],
            "excluded_material": [
                "private reports",
                "target-specific proof material",
                "credentials or session data",
                "vendor correspondence",
            ],
            "approval_required": [
                "user approval before external submission",
                "maintainer approval before publishing non-public vulnerability details",
            ],
        },
    )
    _write_json(
        root / WORKSPACE_FILES["lab_manifest"],
        {
            "lab_id": f"{candidate_id}-LAB",
            "scope": "synthetic_only",
            "external_network": False,
            "third_party_targets": False,
            "destructive_actions": False,
            "scenarios": [
                {
                    "name": "synthetic boundary toy model",
                    "actor": "synthetic lower-trust producer",
                    "consumer": "synthetic higher-trust consumer",
                    "boundary": "materialization boundary",
                    "controls": {
                        "affected_case": "marker appears",
                        "negative_control": "marker absent",
                        "fixed_control": "marker rejected",
                    },
                }
            ],
            "success_markers": ["SYNTHETIC_ONLY", "NO_EXTERNAL_NETWORK", "NO_REAL_TARGETS"],
        },
    )
    return root


def validate_workspace(root: Path) -> list[CheckResult]:
    checks = [
        CheckResult("public-core", root / WORKSPACE_FILES["registry"], core.validate_registry_file(root / WORKSPACE_FILES["registry"])),
        CheckResult(
            "target-brief",
            root / WORKSPACE_FILES["target"],
            gate_records.validate_record_file("target-brief", root / WORKSPACE_FILES["target"]),
        ),
        CheckResult(
            "experiment",
            root / WORKSPACE_FILES["experiment"],
            gate_records.validate_record_file("experiment", root / WORKSPACE_FILES["experiment"]),
        ),
        CheckResult(
            "max-form",
            root / WORKSPACE_FILES["max_form"],
            gate_records.validate_record_file("max-form", root / WORKSPACE_FILES["max_form"]),
        ),
        CheckResult(
            "reproducer-ready",
            root / WORKSPACE_FILES["reproducer"],
            advanced_gates.validate_file("reproducer-ready", root / WORKSPACE_FILES["reproducer"]),
        ),
        CheckResult(
            "hostile-review",
            root / WORKSPACE_FILES["hostile"],
            advanced_gates.validate_file("hostile-review", root / WORKSPACE_FILES["hostile"]),
        ),
        CheckResult(
            "long-run-final",
            root / WORKSPACE_FILES["long_run"],
            advanced_gates.validate_file("long-run-final", root / WORKSPACE_FILES["long_run"]),
        ),
        CheckResult(
            "session-close",
            root / WORKSPACE_FILES["session"],
            handoff.validate_session_close_file(root / WORKSPACE_FILES["session"]),
        ),
        CheckResult(
            "handoff",
            root / WORKSPACE_FILES["handoff"],
            handoff.validate_final_handoff_file(root / WORKSPACE_FILES["handoff"]),
        ),
        CheckResult(
            "package-hygiene",
            root / WORKSPACE_FILES["package_dir"],
            package_hygiene.validate_package([root / WORKSPACE_FILES["package_dir"]]),
        ),
        CheckResult(
            "disclosure-manifest",
            root / WORKSPACE_FILES["package_manifest"],
            advanced_gates.validate_file("disclosure-manifest", root / WORKSPACE_FILES["package_manifest"]),
        ),
        CheckResult(
            "synthetic-lab",
            root / WORKSPACE_FILES["lab_manifest"],
            advanced_gates.validate_file("synthetic-lab", root / WORKSPACE_FILES["lab_manifest"]),
        ),
    ]
    return checks


def validate_bundled_examples(repo_root: Path) -> list[CheckResult]:
    examples = repo_root / "examples"
    return [
        CheckResult(
            "public-core",
            examples / "public-core-registry.json",
            core.validate_registry_file(examples / "public-core-registry.json"),
        ),
        CheckResult(
            "target-brief",
            examples / "target-brief.json",
            gate_records.validate_record_file("target-brief", examples / "target-brief.json"),
        ),
        CheckResult(
            "experiment",
            examples / "experiment-log.json",
            gate_records.validate_record_file("experiment", examples / "experiment-log.json"),
        ),
        CheckResult(
            "max-form",
            examples / "maximum-form-review.json",
            gate_records.validate_record_file("max-form", examples / "maximum-form-review.json"),
        ),
        CheckResult(
            "reproducer-ready",
            examples / "reproducer-ready.json",
            advanced_gates.validate_file("reproducer-ready", examples / "reproducer-ready.json"),
        ),
        CheckResult(
            "hostile-review",
            examples / "hostile-review.json",
            advanced_gates.validate_file("hostile-review", examples / "hostile-review.json"),
        ),
        CheckResult(
            "long-run-final",
            examples / "long-run-final.json",
            advanced_gates.validate_file("long-run-final", examples / "long-run-final.json"),
        ),
        CheckResult(
            "session-close",
            examples / "session-close.json",
            handoff.validate_session_close_file(examples / "session-close.json"),
        ),
        CheckResult(
            "handoff",
            examples / "final-handoff.md",
            handoff.validate_final_handoff_file(examples / "final-handoff.md"),
        ),
        CheckResult(
            "package-hygiene",
            examples / "public-package",
            package_hygiene.validate_package([examples / "public-package"]),
        ),
        CheckResult(
            "disclosure-manifest",
            examples / "public-package" / "disclosure-manifest.json",
            advanced_gates.validate_file(
                "disclosure-manifest",
                examples / "public-package" / "disclosure-manifest.json",
            ),
        ),
        CheckResult(
            "synthetic-lab",
            examples / "synthetic-lab" / "manifest.json",
            advanced_gates.validate_file("synthetic-lab", examples / "synthetic-lab" / "manifest.json"),
        ),
    ]


def next_action(root: Path) -> dict[str, Any]:
    checks = validate_workspace(root)
    failing = [check for check in checks if not check.ok]
    if failing:
        first = failing[0]
        return {
            "status": "needs_repair",
            "blocking_gate": first.name,
            "path": str(first.path),
            "warnings": first.warnings,
            "command": f"osssec-public validate {root}",
        }
    registry = core.load_json(root / WORKSPACE_FILES["registry"])
    summary = core.summarize_registry(registry).as_dict()
    return {
        "status": "ready_for_authorized_evidence",
        "blocking_gate": None,
        "summary": summary,
        "next_action": "replace synthetic placeholders with public, local, owned, or explicitly authorized evidence",
        "command": f"osssec-public validate {root}",
    }


def doctor(repo_root: Path) -> list[CheckResult]:
    return [
        CheckResult("repo-safety", repo_root, safety.scan_repo(repo_root)),
        CheckResult(
            "bundled-examples",
            repo_root / "examples",
            [warning for result in validate_bundled_examples(repo_root) for warning in result.warnings],
        ),
    ]
