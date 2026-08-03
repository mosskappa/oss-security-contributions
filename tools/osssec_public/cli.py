"""Command-line interface for public-safe OSS security contribution checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import (
    core,
    evidence,
    gate_records,
    handoff,
    ledger,
    markdown_policy,
    package_hygiene,
    safety,
    state_machine,
    workflow,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _print_warnings(title: str, warnings: list[str]) -> int:
    if warnings:
        print(f"{title}:")
        for warning in warnings:
            print(f"- {warning}")
        return 1
    print(f"{title}: passed")
    return 0


def cmd_safety(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    return _print_warnings("Public safety scan", safety.scan_repo(root))


def cmd_ledger(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    entries = ledger.parse_ledger(path)
    warnings = ledger.validate_entries(entries)
    if args.json:
        print(json.dumps([entry.as_dict() for entry in entries], indent=2))
    else:
        print(f"Parsed {len(entries)} ledger entries from {path}.")
    return _print_warnings("Ledger validation", warnings)


def cmd_evidence(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    entries = evidence.parse_evidence_index(path)
    warnings = evidence.validate_evidence(entries)
    if args.json:
        print(json.dumps([entry.as_dict() for entry in entries], indent=2))
    else:
        print(f"Parsed {len(entries)} evidence entries from {path}.")
    return _print_warnings("Evidence validation", warnings)


def cmd_markdown_policy(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    warnings = markdown_policy.scan_markdown_tree(root)
    return _print_warnings("Markdown disclosure policy", warnings)


def cmd_workflow(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = workflow.validate_workflow_file(path)
    return _print_warnings("Workflow validation", warnings)


def cmd_state(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = state_machine.validate_state_file(path)
    return _print_warnings("State-machine validation", warnings)


def cmd_gate_record(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = gate_records.validate_record_file(args.kind, path)
    return _print_warnings(f"{args.kind} validation", warnings)


def cmd_scaffold(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    record = gate_records.scaffold_record(args.kind, args.candidate_id, args.project, args.component)
    gate_records.write_scaffold(path, record, force=args.force)
    print(f"Created {args.kind} record: {path}")
    return 0


def cmd_public_core(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = core.validate_registry_file(path)
    return _print_warnings("Public core registry validation", warnings)


def cmd_status(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    registry = core.load_json(path)
    warnings = core.validate_registry(registry)
    if warnings:
        return _print_warnings("Public core registry validation", warnings)
    print(json.dumps(core.summarize_registry(registry).as_dict(), indent=2))
    return 0


def cmd_init_candidate(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    candidate = core.scaffold_candidate(args.candidate_id, args.project, args.component, mode=args.mode)
    registry = core.append_candidate(path, candidate)
    print(f"Added {args.candidate_id} to {path}. Total candidates: {len(registry['candidates'])}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    candidate = core.claim_candidate(path, args.candidate_id, args.owner, args.purpose, args.ttl_hours)
    print(json.dumps({"candidate_id": candidate["candidate_id"], "claim": candidate["claim"]}, indent=2))
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    candidate = core.release_candidate(path, args.candidate_id, owner=args.owner)
    print(f"Released claim for {candidate['candidate_id']}")
    return 0


def cmd_session_close(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = handoff.validate_session_close_file(path)
    return _print_warnings("Session-close validation", warnings)


def cmd_handoff(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    warnings = handoff.validate_final_handoff_file(path)
    return _print_warnings("Final handoff validation", warnings)


def cmd_package_hygiene(args: argparse.Namespace) -> int:
    paths = [Path(path).resolve() for path in args.paths]
    warnings = package_hygiene.validate_package(paths)
    return _print_warnings("Package hygiene validation", warnings)


def cmd_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    checks = [
        ("Public safety scan", safety.scan_repo(root)),
        (
            "Ledger validation",
            ledger.validate_entries(ledger.parse_ledger(root / "docs" / "CREDIT_LEDGER.md")),
        ),
        (
            "Evidence validation",
            evidence.validate_evidence(
                evidence.parse_evidence_index(root / "docs" / "PUBLIC_EVIDENCE_INDEX.md")
            ),
        ),
        (
            "Workflow validation",
            workflow.validate_workflow_file(root / "examples" / "workflow-status.json"),
        ),
        (
            "State-machine validation",
            state_machine.validate_state_file(root / "examples" / "workflow-status.json"),
        ),
        (
            "Target brief validation",
            gate_records.validate_record_file("target-brief", root / "examples" / "target-brief.json"),
        ),
        (
            "Experiment log validation",
            gate_records.validate_record_file("experiment", root / "examples" / "experiment-log.json"),
        ),
        (
            "Maximum-form validation",
            gate_records.validate_record_file("max-form", root / "examples" / "maximum-form-review.json"),
        ),
        (
            "Public core registry validation",
            core.validate_registry_file(root / "examples" / "public-core-registry.json"),
        ),
        (
            "Session-close validation",
            handoff.validate_session_close_file(root / "examples" / "session-close.json"),
        ),
        (
            "Final handoff validation",
            handoff.validate_final_handoff_file(root / "examples" / "final-handoff.md"),
        ),
        (
            "Package hygiene validation",
            package_hygiene.validate_package([root / "examples" / "public-package"]),
        ),
        ("Markdown disclosure policy", markdown_policy.scan_markdown_tree(root)),
    ]

    failed = 0
    for title, warnings in checks:
        failed |= _print_warnings(title, warnings)
    return failed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="osssec-public",
        description="Validate public-safe OSS security contribution repositories.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    safety_parser = subparsers.add_parser("safety", help="scan for sensitive material")
    safety_parser.add_argument("root", nargs="?", default=str(repo_root()))
    safety_parser.set_defaults(func=cmd_safety)

    ledger_parser = subparsers.add_parser("ledger", help="validate the public credit ledger")
    ledger_parser.add_argument("path", nargs="?", default=str(repo_root() / "docs" / "CREDIT_LEDGER.md"))
    ledger_parser.add_argument("--json", action="store_true", help="print parsed entries as JSON")
    ledger_parser.set_defaults(func=cmd_ledger)

    evidence_parser = subparsers.add_parser("evidence", help="validate public evidence links")
    evidence_parser.add_argument(
        "path", nargs="?", default=str(repo_root() / "docs" / "PUBLIC_EVIDENCE_INDEX.md")
    )
    evidence_parser.add_argument("--json", action="store_true", help="print parsed entries as JSON")
    evidence_parser.set_defaults(func=cmd_evidence)

    markdown_parser = subparsers.add_parser(
        "markdown-policy", help="scan Markdown for disclosure-risky wording"
    )
    markdown_parser.add_argument("root", nargs="?", default=str(repo_root()))
    markdown_parser.set_defaults(func=cmd_markdown_policy)

    workflow_parser = subparsers.add_parser("workflow", help="validate a workflow status record")
    workflow_parser.add_argument(
        "path", nargs="?", default=str(repo_root() / "examples" / "workflow-status.json")
    )
    workflow_parser.set_defaults(func=cmd_workflow)

    state_parser = subparsers.add_parser("state", help="validate a research state record")
    state_parser.add_argument(
        "path", nargs="?", default=str(repo_root() / "examples" / "workflow-status.json")
    )
    state_parser.set_defaults(func=cmd_state)

    gate_parser = subparsers.add_parser(
        "gate-record", help="validate a target brief, experiment log, or maximum-form record"
    )
    gate_parser.add_argument("kind", choices=["target-brief", "experiment", "max-form"])
    gate_parser.add_argument("path")
    gate_parser.set_defaults(func=cmd_gate_record)

    scaffold_parser = subparsers.add_parser(
        "scaffold", help="create a public-safe JSON record scaffold"
    )
    scaffold_parser.add_argument("kind", choices=["target-brief", "experiment", "max-form"])
    scaffold_parser.add_argument("path")
    scaffold_parser.add_argument("--candidate-id", default="SYNTH-NEW-001")
    scaffold_parser.add_argument("--project", default="example-project")
    scaffold_parser.add_argument("--component", default="example-component")
    scaffold_parser.add_argument("--force", action="store_true", help="overwrite an existing file")
    scaffold_parser.set_defaults(func=cmd_scaffold)

    public_core_parser = subparsers.add_parser("public-core", help="validate a public-safe candidate registry")
    public_core_parser.add_argument("path", nargs="?", default=str(repo_root() / "examples" / "public-core-registry.json"))
    public_core_parser.set_defaults(func=cmd_public_core)

    status_parser = subparsers.add_parser("status", help="summarize a public-safe candidate registry")
    status_parser.add_argument("path", nargs="?", default=str(repo_root() / "examples" / "public-core-registry.json"))
    status_parser.set_defaults(func=cmd_status)

    init_parser = subparsers.add_parser("init-candidate", help="add a generic public-safe candidate")
    init_parser.add_argument("path")
    init_parser.add_argument("candidate_id")
    init_parser.add_argument("--project", required=True)
    init_parser.add_argument("--component", required=True)
    init_parser.add_argument("--mode", choices=sorted(core.MODES), default="stable_credit")
    init_parser.set_defaults(func=cmd_init_candidate)

    claim_parser = subparsers.add_parser("claim", help="claim a public-safe candidate lease")
    claim_parser.add_argument("path")
    claim_parser.add_argument("candidate_id")
    claim_parser.add_argument("--owner", required=True)
    claim_parser.add_argument("--purpose", default="local public-safe review")
    claim_parser.add_argument("--ttl-hours", type=float, default=4.0)
    claim_parser.set_defaults(func=cmd_claim)

    release_parser = subparsers.add_parser("release", help="release a public-safe candidate lease")
    release_parser.add_argument("path")
    release_parser.add_argument("candidate_id")
    release_parser.add_argument("--owner")
    release_parser.set_defaults(func=cmd_release)

    session_close_parser = subparsers.add_parser("session-close", help="validate a session close record")
    session_close_parser.add_argument("path", nargs="?", default=str(repo_root() / "examples" / "session-close.json"))
    session_close_parser.set_defaults(func=cmd_session_close)

    handoff_parser = subparsers.add_parser("handoff", help="validate a final handoff note")
    handoff_parser.add_argument("path", nargs="?", default=str(repo_root() / "examples" / "final-handoff.md"))
    handoff_parser.set_defaults(func=cmd_handoff)

    package_parser = subparsers.add_parser("package-hygiene", help="validate public report package hygiene")
    package_parser.add_argument("paths", nargs="+")
    package_parser.set_defaults(func=cmd_package_hygiene)

    check_parser = subparsers.add_parser("check", help="run all public-readiness checks")
    check_parser.add_argument("root", nargs="?", default=str(repo_root()))
    check_parser.set_defaults(func=cmd_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
