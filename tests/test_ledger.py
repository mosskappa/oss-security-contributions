from pathlib import Path

from tools.osssec_public.ledger import parse_ledger, validate_entries


def test_public_ledger_parses_and_validates():
    root = Path(__file__).resolve().parents[1]
    entries = parse_ledger(root / "docs" / "CREDIT_LEDGER.md")

    assert entries
    assert any(entry.project == "pnpm" for entry in entries)
    assert validate_entries(entries) == []


def test_ledger_rejects_overclaiming_wording(tmp_path):
    ledger = tmp_path / "CREDIT_LEDGER.md"
    ledger.write_text(
        "\n".join(
            [
                "## Public Reporter Credits",
                "| Project | Public ID | Role | Public-safe summary |",
                "|---|---|---|---|",
                "| demo | `CVE-2099-12345` | Reporter | Found exploit payload. |",
            ]
        ),
        encoding="utf-8",
    )

    warnings = validate_entries(parse_ledger(ledger))

    assert warnings
    assert any("abuse-enabling" in warning for warning in warnings)

