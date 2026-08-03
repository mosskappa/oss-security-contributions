"""Validate public evidence links for CVE/GHSA and OSS hardening claims."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


PUBLIC_ID_RE = re.compile(
    r"\b(?:CVE-\d{4}-\d{4,7}|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}|[a-f0-9]{12,40}|[\w.-]+/[\w.-]+#\d+)\b",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https://[^\s)]+")


@dataclass(frozen=True)
class EvidenceEntry:
    project: str
    public_id: str
    evidence_url: str
    claim: str

    def as_dict(self) -> dict[str, str]:
        return {
            "project": self.project,
            "public_id": self.public_id,
            "evidence_url": self.evidence_url,
            "claim": self.claim,
        }


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_evidence_index(path: Path) -> list[EvidenceEntry]:
    entries: list[EvidenceEntry] = []
    in_table = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("|---"):
            in_table = True
            continue
        if not in_table or not line.startswith("|"):
            continue

        cells = _split_markdown_row(line)
        if len(cells) < 4 or cells[0].lower() == "project":
            continue

        url_match = URL_RE.search(cells[2])
        entries.append(
            EvidenceEntry(
                project=cells[0],
                public_id=cells[1],
                evidence_url=url_match.group(0) if url_match else cells[2],
                claim=cells[3],
            )
        )

    return entries


def validate_evidence(entries: list[EvidenceEntry]) -> list[str]:
    warnings: list[str] = []
    seen: set[tuple[str, str]] = set()

    for entry in entries:
        key = (entry.project.lower(), entry.public_id.lower())
        if key in seen:
            warnings.append(f"{entry.project}: duplicate public id {entry.public_id}")
        seen.add(key)

        if not PUBLIC_ID_RE.search(entry.public_id):
            warnings.append(f"{entry.project}: public id needs CVE/GHSA/PR/commit evidence")
        if not entry.evidence_url.startswith("https://"):
            warnings.append(f"{entry.project}: evidence URL must be https")
        if "private" in entry.claim.lower() or "pending" in entry.claim.lower():
            warnings.append(f"{entry.project}: public evidence claim should not rely on private state")

    if not entries:
        warnings.append("evidence index has no entries")

    return warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    path = root / "docs" / "PUBLIC_EVIDENCE_INDEX.md"
    entries = parse_evidence_index(path)
    warnings = validate_evidence(entries)

    print(f"Parsed {len(entries)} evidence entries from {path}.")
    if warnings:
        print("Evidence validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

