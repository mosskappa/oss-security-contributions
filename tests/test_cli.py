from tools.osssec_public.cli import main


def test_cli_check_passes():
    assert main(["check"]) == 0


def test_cli_ledger_json_passes():
    assert main(["ledger", "--json"]) == 0


def test_cli_gate_record_passes():
    assert main(["gate-record", "target-brief", "examples/target-brief.json"]) == 0


def test_cli_scaffold_writes_file(tmp_path):
    path = tmp_path / "max-form.json"
    assert main(["scaffold", "max-form", str(path), "--candidate-id", "SYNTH-3"]) == 0
    assert path.exists()


def test_cli_public_core_passes():
    assert main(["public-core", "examples/public-core-registry.json"]) == 0


def test_cli_status_passes():
    assert main(["status", "examples/public-core-registry.json"]) == 0


def test_cli_claim_and_release(tmp_path):
    path = tmp_path / "registry.json"
    assert main(
        [
            "init-candidate",
            str(path),
            "SYNTH-CLI-001",
            "--project",
            "example",
            "--component",
            "component",
        ]
    ) == 0
    assert main(["claim", str(path), "SYNTH-CLI-001", "--owner", "session-a"]) == 0
    assert main(["release", str(path), "SYNTH-CLI-001", "--owner", "session-a"]) == 0


def test_cli_session_handoff_and_package_pass():
    assert main(["session-close", "examples/session-close.json"]) == 0
    assert main(["handoff", "examples/final-handoff.md"]) == 0
    assert main(["package-hygiene", "examples/public-package"]) == 0


def test_cli_advanced_gate_passes():
    assert main(["advanced-gate", "reproducer-ready", "examples/reproducer-ready.json"]) == 0
    assert main(["advanced-gate", "long-run-final", "examples/long-run-final.json"]) == 0
