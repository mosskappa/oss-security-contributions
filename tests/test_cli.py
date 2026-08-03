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
