from tools.osssec_public.markdown_policy import scan_markdown_tree


def test_markdown_policy_detects_risky_reproducer_language(tmp_path):
    (tmp_path / "public-note.md").write_text(
        "# Note\n\n## Steps to reproduce\n\nSynthetic unsafe shape.",
        encoding="utf-8",
    )

    warnings = scan_markdown_tree(tmp_path)

    assert warnings
    assert any("public-note.md" in warning for warning in warnings)


def test_markdown_policy_allows_safe_example():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    warnings = scan_markdown_tree(root)

    assert warnings == []

