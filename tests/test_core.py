import json
from pathlib import Path

import pytest

from tools.osssec_public.core import (
    append_candidate,
    claim_candidate,
    load_json,
    release_candidate,
    scaffold_candidate,
    summarize_registry,
    validate_registry_file,
)


def test_example_public_core_registry_validates():
    root = Path(__file__).resolve().parents[1]
    assert validate_registry_file(root / "examples" / "public-core-registry.json") == []


def test_registry_summary_counts_candidates():
    root = Path(__file__).resolve().parents[1]
    registry = load_json(root / "examples" / "public-core-registry.json")
    summary = summarize_registry(registry).as_dict()

    assert summary["total"] == 2
    assert summary["by_status"]["BOUNDARY_MODELED"] == 1
    assert summary["by_status"]["PRIOR_ART_REVIEWED"] == 1


def test_append_claim_and_release_candidate(tmp_path):
    path = tmp_path / "registry.json"
    candidate = scaffold_candidate("SYNTH-TEST-001", "example", "component")

    append_candidate(path, candidate)
    claimed = claim_candidate(path, "SYNTH-TEST-001", "session-a", "test claim", 1)
    assert claimed["claim"]["owner"] == "session-a"

    released = release_candidate(path, "SYNTH-TEST-001", owner="session-a")
    assert released["claim"] is None


def test_claim_blocks_other_active_owner(tmp_path):
    path = tmp_path / "registry.json"
    append_candidate(path, scaffold_candidate("SYNTH-TEST-002", "example", "component"))
    claim_candidate(path, "SYNTH-TEST-002", "session-a", "test claim", 1)

    with pytest.raises(ValueError, match="already claimed"):
        claim_candidate(path, "SYNTH-TEST-002", "session-b", "test claim", 1)


def test_registry_rejects_duplicate_ids(tmp_path):
    path = tmp_path / "registry.json"
    registry = {
        "registry_version": 1,
        "candidates": [
            scaffold_candidate("SYNTH-DUP", "example", "component"),
            scaffold_candidate("SYNTH-DUP", "example", "component"),
        ],
    }
    path.write_text(json.dumps(registry), encoding="utf-8")

    warnings = validate_registry_file(path)
    assert any("duplicate" in warning for warning in warnings)
