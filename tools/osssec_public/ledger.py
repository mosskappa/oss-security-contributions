"""Utilities for validating the public credit ledger."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


PUBLIC_ID_RE = re.compile(
    r"\b(?:CVE-\d{4}-\d{4,7}|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LedgerEntry:
    section: str
    project: str
    public_id: str
    role: str
    summary: str

    def as_dict(self) -> dict[str, str]:
        return {
            "section": self.section,
            "project": self.project,
            "public_id": self.public_id,
            "role": self.role,
            "summary": self.summary,
        }


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_ledger(path: Path) -> list[LedgerEntry]:
    """Parse simple Markdown tables from docs/CREDIT_LEDGER.md."""

    entries: list[LedgerEntry] = []
    section = ""
    in_table = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line.removeprefix("## ").strip()
            in_table = False
            continue

        if line.startswith("|---"):
            in_table = True
            continue

        if not in_table or not line.startswith("|"):
            continue

        cells = _split_markdown_row(line)
        if len(cells) < 4 or cells[0].lower() == "project":
            continue

        entries.append(
            LedgerEntry(
                section=section,
                project=cells[0],
                public_id=cells[1],
                role=cells[2],
                summary=cells[3],
            )
        )

    return entries


def validate_entries(entries: list[LedgerEntry]) -> list[str]:
    """Return public-ledger validation warnings."""

    warnings: list[str] = []
    for entry in entries:
        if entry.section.startswith("Public") and entry.public_id != "Public evidence":
            ids = PUBLIC_ID_RE.findall(entry.public_id)
            if not ids and "#" not in entry.public_id and "Public" not in entry.public_id:
                warnings.append(
                    f"{entry.project}: public id does not look like CVE/GHSA/PR evidence"
                )
        if "Reporter" in entry.role and "reported" not in entry.summary.lower():
            warnings.append(f"{entry.project}: reporter entry should use conservative wording")
        if any(term in entry.summary.lower() for term in ("exploit", "payload", "0day")):
            warnings.append(f"{entry.project}: summary contains abuse-enabling wording")
    return warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    ledger_path = root / "docs" / "CREDIT_LEDGER.md"
    entries = parse_ledger(ledger_path)
    warnings = validate_entries(entries)

    print(f"Parsed {len(entries)} ledger entries from {ledger_path}.")
    if warnings:
        print("Ledger validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Ledger validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
