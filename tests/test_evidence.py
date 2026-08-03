from pathlib import Path

from tools.osssec_public.evidence import parse_evidence_index, validate_evidence


def test_public_evidence_index_validates():
    root = Path(__file__).resolve().parents[1]
    entries = parse_evidence_index(root / "docs" / "PUBLIC_EVIDENCE_INDEX.md")

    assert entries
    assert any(entry.project == "pnpm" for entry in entries)
    assert validate_evidence(entries) == []


def test_evidence_requires_https(tmp_path):
    index = tmp_path / "PUBLIC_EVIDENCE_INDEX.md"
    index.write_text(
        "\n".join(
            [
                "| Project | Public ID | Evidence URL | Public-safe claim |",
                "|---|---|---|---|",
                "| demo | `CVE-2099-12345` | http://example.org/cve | Public advisory. |",
            ]
        ),
        encoding="utf-8",
    )

    warnings = validate_evidence(parse_evidence_index(index))

    assert warnings
    assert any("https" in warning.lower() for warning in warnings)

