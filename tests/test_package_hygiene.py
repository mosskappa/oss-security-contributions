from pathlib import Path

from tools.osssec_public.package_hygiene import validate_package


def test_example_public_package_validates():
    root = Path(__file__).resolve().parents[1]
    assert validate_package([root / "examples" / "public-package"]) == []


def test_package_rejects_disallowed_extension(tmp_path):
    package = tmp_path / "package"
    package.mkdir()
    (package / "report.md").write_text("safe report", encoding="utf-8")
    (package / "public-boundaries.md").write_text("safe boundaries", encoding="utf-8")
    (package / "payload.py").write_text("print('no')", encoding="utf-8")

    warnings = validate_package([package])
    assert any("disallowed package extension" in warning for warning in warnings)
