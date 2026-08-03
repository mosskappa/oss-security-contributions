"""Markdown checks that keep public writeups conservative."""

from __future__ import annotations

import re
from pathlib import Path

from .safety import SKIP_DIRS


RISKY_MARKDOWN_PATTERNS = [
    re.compile(r"(?i)\b(step[s]?\s+to\s+reproduce|full\s+reproducer)\b"),
    re.compile(r"(?i)\b(curl|nc|netcat|msfconsole|meterpreter)\b"),
    re.compile(r"(?i)\b(reverse\s+shell|arbitrary\s+command\s+execution)\b"),
    re.compile(r"(?i)\b(exfiltrate|credential\s+theft|steal\s+token)\b"),
]


ALLOWLIST = {
    "docs/PUBLICATION_BOUNDARIES.md",
    "templates/MAINTAINER_DISCLOSURE_CHECKLIST.md",
    "templates/PATCH_VALIDATION_NOTE.md",
}


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        relative_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        yield path


def scan_markdown_file(root: Path, path: Path) -> list[str]:
    relative = path.relative_to(root).as_posix()
    if relative in ALLOWLIST:
        return []

    text = path.read_text(encoding="utf-8")
    warnings: list[str] = []
    for pattern in RISKY_MARKDOWN_PATTERNS:
        if pattern.search(text):
            warnings.append(f"{relative}: matched {pattern.pattern}")
    return warnings


def scan_markdown_tree(root: Path) -> list[str]:
    warnings: list[str] = []
    for path in iter_markdown_files(root):
        warnings.extend(scan_markdown_file(root, path))
    return warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    warnings = scan_markdown_tree(root)
    if warnings:
        print("Markdown disclosure-policy warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Markdown disclosure-policy scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
