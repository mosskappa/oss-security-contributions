# Getting Started

This guide shows how to use the public-safe research core from a clean checkout.
It uses synthetic or generic candidates only. Do not put private reports,
target-specific proof material, credentials, browser state, or coordinated
disclosure correspondence in this repository.

## 1. Run The Baseline Checks

```bash
python scripts/validate_public_repo.py
python -m pytest
```

The first command runs the public-safety, ledger, evidence, workflow, gate,
registry, handoff, package, and Markdown checks. The second command runs the
test suite.

## 2. Start Or Validate A Candidate Registry

Use the example registry first:

```bash
python -m tools.osssec_public.cli public-core examples/public-core-registry.json
python -m tools.osssec_public.cli status examples/public-core-registry.json
```

For local experimentation, create a scratch registry. The `scratch/` directory is
ignored by Git.

```bash
python -m tools.osssec_public.cli init-candidate scratch/registry.json SYNTH-NEW-001 --project example-project --component example-component
python -m tools.osssec_public.cli claim scratch/registry.json SYNTH-NEW-001 --owner local-session
```

Release the claim when the local session is done:

```bash
python -m tools.osssec_public.cli release scratch/registry.json SYNTH-NEW-001 --owner local-session
```

## 3. Write The Core Gate Records

Validate the included examples:

```bash
python -m tools.osssec_public.cli gate-record target-brief examples/target-brief.json
python -m tools.osssec_public.cli gate-record experiment examples/experiment-log.json
python -m tools.osssec_public.cli gate-record max-form examples/maximum-form-review.json
```

Create a new scaffold in ignored local space:

```bash
python -m tools.osssec_public.cli scaffold target-brief scratch/target-brief.json --candidate-id SYNTH-NEW-001 --project example-project --component example-component
```

## 4. Run Advanced Workflow Gates

These gates model the stricter parts of the private workflow without publishing
private operational material.

```bash
python -m tools.osssec_public.cli advanced-gate start-mode examples/start-mode.json
python -m tools.osssec_public.cli advanced-gate reproducer-ready examples/reproducer-ready.json
python -m tools.osssec_public.cli advanced-gate hostile-review examples/hostile-review.json
python -m tools.osssec_public.cli advanced-gate long-run-final examples/long-run-final.json
python -m tools.osssec_public.cli advanced-gate synthetic-lab examples/synthetic-lab/manifest.json
```

Use `reproducer-ready` for validation shape only. It checks controls, expected
markers, cleanup, run-id handling, and non-claims. It does not execute private
proof material.

## 5. Close A Session

Before calling work done, validate the close record and final handoff:

```bash
python -m tools.osssec_public.cli session-close examples/session-close.json
python -m tools.osssec_public.cli handoff examples/final-handoff.md
```

A good close record names work completed, evidence, decisions, tests, claim
boundaries, blockers, state changes, and the next concrete step.

## 6. Check A Public Package

Public packages should be small, text-based, and explicit about what is excluded.

```bash
python -m tools.osssec_public.cli package-hygiene examples/public-package
python -m tools.osssec_public.cli advanced-gate disclosure-manifest examples/public-package/disclosure-manifest.json
```

The package checks are guardrails. Manual disclosure review is still required
before anything is sent or published.

## 7. Safe Publication Rule

Before committing public changes:

```bash
python scripts/validate_public_repo.py
python -m pytest
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_public_safety.ps1
```

If a warning appears, treat it as a stop point until the file is reviewed.
