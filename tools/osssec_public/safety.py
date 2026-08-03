"""Public-safety scanning for this repository."""

from __future__ import annotations

import re
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".browser-profiles",
    ".runtime",
    "artifacts",
    "audits",
    "disclosures",
    "downloads",
    "logs",
    "out_",
    "programs",
    "scratch",
    "targets",
    "tmp",
    "__pycache__",
}

SENSITIVE_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+\-]+@gmail\.com", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+\-]+@(corp|internal|private)\.[A-Za-z0-9.\-]+", re.IGNORECASE),
    re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._\-]+", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}", re.IGNORECASE),
    re.compile(r"(api[_-]?key|secret|password|cookie|session)[\s:=]+[A-Za-z0-9._\-]{12,}", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(ticket|case)\s*[#:]\s*[A-Za-z0-9._\-]{5,}", re.IGNORECASE),
    re.compile(r"\b(message|thread)\s+id\s*[#:]?\s*[A-Za-z0-9._\-]{8,}", re.IGNORECASE),
    re.compile(r"DocuSign\s+(envelope|certificate|id)", re.IGNORECASE),
    re.compile(r"bounty\s+payment\s+(processed|pending|amount|usd|us\$)", re.IGNORECASE),
    re.compile(r"\b(active|embargoed|undisclosed)\s+(vulnerability|finding|report)\b", re.IGNORECASE),
]


def iter_public_files(root: Path):
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        yield path


def scan_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{path}: non-text file requires manual review"]

    warnings: list[str] = []
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            warnings.append(f"{path}: matched {pattern.pattern}")
    return warnings


def scan_repo(root: Path) -> list[str]:
    warnings: list[str] = []
    for path in iter_public_files(root):
        relative = path.relative_to(root).as_posix()
        if relative in {"tools/osssec_public/safety.py", "scripts/check_public_safety.ps1"}:
            continue
        warnings.extend(scan_file(path))
    return warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    warnings = scan_repo(root)
    if warnings:
        print("Public safety warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Public safety scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
