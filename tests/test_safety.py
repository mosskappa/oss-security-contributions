from pathlib import Path

from tools.osssec_public.safety import scan_repo


def test_public_repo_safety_scan_passes():
    root = Path(__file__).resolve().parents[1]
    assert scan_repo(root) == []


def test_safety_scan_detects_private_email(tmp_path):
    (tmp_path / "note.md").write_text(
        "Do not publish " + "researcher" + "@gmail.com style evidence.",
        encoding="utf-8",
    )

    warnings = scan_repo(tmp_path)

    assert warnings
    assert any("gmail" in warning.lower() for warning in warnings)
