"""Check public-safe report packages before publication."""

from __future__ import annotations

from pathlib import Path

from .safety import scan_file


ALLOWED_EXTENSIONS = {".md", ".txt", ".json", ".diff", ".patch"}
BLOCKED_NAMES = {
    "cookies.txt",
    "session.json",
    "browser-profile",
    "submission-bundle.zip",
}
REQUIRED_FILENAMES = {"report.md", "public-boundaries.md"}


def iter_package_files(path: Path):
    if path.is_file():
        yield path
        return
    for child in path.rglob("*"):
        if child.is_file():
            yield child


def validate_package(paths: list[Path]) -> list[str]:
    warnings: list[str] = []
    seen_names: set[str] = set()
    for root in paths:
        if not root.exists():
            warnings.append(f"path does not exist: {root}")
            continue
        for file_path in iter_package_files(root):
            name = file_path.name.lower()
            seen_names.add(name)
            if name in BLOCKED_NAMES:
                warnings.append(f"blocked package filename: {file_path}")
            if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
                warnings.append(f"disallowed package extension: {file_path}")
            if file_path.stat().st_size > 1_000_000:
                warnings.append(f"large package file requires manual review: {file_path}")
            warnings.extend(scan_file(file_path))
    if any(path.is_dir() for path in paths):
        missing = sorted(REQUIRED_FILENAMES - seen_names)
        if missing:
            warnings.append(f"package directory missing files: {', '.join(missing)}")
    return warnings
