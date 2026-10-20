# OSS Security Contributions

Public-safe toolkit for maintaining OSS security contribution ledgers, validating
public evidence, and preventing accidental disclosure of private vulnerability
material.

Maintained by Junyi Liu (`mosskappa`), this repository supports responsible
open-source security work without publishing exploit material or private vendor
correspondence. It combines a public CVE/GHSA contribution ledger with reusable
checks, templates, and examples for maintainer-friendly security workflows.

## Selected Engineering Contributions

Public sources last reviewed: **2026-10-20**.

| Project | Engineering work | Personal role and upstream status | Public evidence |
|---|---|---|---|
| ZenML | Resource-update authorization for single and batch tagging, bulk SQL resource lookup, and regression tests. | PR author; merged 2026-06-12 after maintainer review. | [PR #4927](https://github.com/zenml-io/zenml/pull/4927) |
| Google go-containerregistry | OCI layout blob-read checks for symlinks, non-regular files, and file identity across open operations. | PR author; merged 2026-06-02 and included in v0.21.7. | [PR #2306](https://github.com/google/go-containerregistry/pull/2306), [release v0.21.7](https://github.com/google/go-containerregistry/releases/tag/v0.21.7) |
| Linux kernel ksmbd | SID bounds validation during ACL inheritance and session-aware cleanup on durable-reconnect error paths. | Author of two upstream C fixes, associated with CVE-2026-64138 and CVE-2026-64016. | [SID validation commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=69f030cf95488ae1186c72ac8c66fd279664ea7f), [reconnect lifetime commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3515503322f4819277091839eed46b695096aca5) |
| fuse-overlayfs | Clearing SUID/SGID bits on truncate. | Fix author; incorporated with maintainer adjustments on 2026-06-09. The related advisory records an Analyst credit. | [Upstream commit](https://github.com/containers/fuse-overlayfs/commit/97e0d968a782fc259ebde112db1e9b9ff1ad724f), [CVE-2026-52791 advisory](https://github.com/containers/fuse-overlayfs/security/advisories/GHSA-2cc4-p72c-v85h) |

The complete [credit ledger](docs/CREDIT_LEDGER.md) includes **14 published
GitHub security advisories: 9 Reporter, 2 Finder, and 3 Analyst credits**, five
GStreamer reporting acknowledgements, and additional maintainer credits from
Pants and Dagger. Each role is recorded separately from patch authorship and
downstream adoption. These are advisory-credit counts, not a count of independent
discoveries.

The [public evidence index](docs/PUBLIC_EVIDENCE_INDEX.md) links each claim to
project advisories, upstream changes, or public acknowledgements.

## Features

- CVE/GHSA and public-hardening contribution ledger.
- Public evidence index for linking claims to public advisory or PR pages.
- CLI checks for sensitive material, ledger consistency, evidence links, and
  public Markdown disclosure policy.
- Public-safe gate catalog covering authorization, boundary modeling, hostile
  review, report quality, maintainer-native validation, and public credit.
- Public mapping of the private research workflow into safe, reusable OSS
  process artifacts.
- State-machine validation for research status transitions and public-credit
  readiness.
- Gate-record validation and scaffolding for target briefs, experiment logs,
  and maximum-form reviews.
- Public-safe PRESTIGE Core features: generic candidate registry, claim leases,
  status summaries, session-close gates, final handoff gates, and package
  hygiene checks.
- Advanced public-safe gates for start-mode selection, reproducer-readiness
  shape, hostile review, long-run final handoff, disclosure manifests, and
  synthetic lab manifests.
- Synthetic examples and templates for safe maintainer-facing workflows.
- Tests and GitHub Actions workflow for repeatable public-readiness checks.

## Quick Start

New users should start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

Fast path:

```bash
python -m pip install -e .
osssec-public start scratch/SYNTH-001 --candidate-id SYNTH-001 --project example-project --component example-component --mode deep_impact_review
osssec-public next scratch/SYNTH-001
osssec-public validate scratch/SYNTH-001
osssec-public doctor
osssec-public demo
```

Run every check:

```bash
python scripts/validate_public_repo.py
```

or use the CLI directly:

```bash
python -m tools.osssec_public.cli check
python -m tools.osssec_public.cli ledger --json
python -m tools.osssec_public.cli evidence
python -m tools.osssec_public.cli workflow
python -m tools.osssec_public.cli state
python -m tools.osssec_public.cli gate-record target-brief examples/target-brief.json
python -m tools.osssec_public.cli scaffold max-form scratch/example-max-form.json
python -m tools.osssec_public.cli public-core examples/public-core-registry.json
python -m tools.osssec_public.cli status examples/public-core-registry.json
python -m tools.osssec_public.cli session-close examples/session-close.json
python -m tools.osssec_public.cli handoff examples/final-handoff.md
python -m tools.osssec_public.cli package-hygiene examples/public-package
python -m tools.osssec_public.cli advanced-gate reproducer-ready examples/reproducer-ready.json
python -m tools.osssec_public.cli start scratch/SYNTH-001 --candidate-id SYNTH-001 --project example --component component
python -m tools.osssec_public.cli validate scratch/SYNTH-001
```

Run tests:

```bash
python -m pytest
```

## Scope

Included:

- Public CVE, GHSA, advisory, merged-fix, and maintainer-credit records.
- Conservative summaries of vulnerability classes after public disclosure.
- Templates for responsible disclosure, patch validation, and public-safe notes.
- Guardrails for keeping private reports, exploit material, and personal data
  out of public repositories.

Excluded:

- Non-public or coordinated-disclosure vulnerability details.
- Vendor-private reports, private program correspondence, case identifiers, or
  compensation details.
- Abuse-enabling code, weaponized proof-of-concept material, secrets, cookies, browser
  profiles, session data, private emails, and internal logs.

## Why This Exists

Open-source maintainers often need careful help with triage, reproduction,
impact scoping, patch review, and regression testing. This project documents
that work in a way that is useful for reviewers while respecting coordinated
disclosure boundaries.

The project is intentionally not an exploit archive. Public entries focus on
what was responsibly disclosed or fixed, not on operational abuse steps. Private
proof material belongs in maintainer-approved disclosure channels, not in this
repository.

## Repository Layout

- `docs/CREDIT_LEDGER.md` - public-safe security contribution ledger.
- `docs/PUBLIC_EVIDENCE_INDEX.md` - public links supporting public claims.
- `docs/PUBLICATION_BOUNDARIES.md` - what may and may not be published here.
- `docs/RESEARCH_WORKFLOW_MAPPING.md` - how private research workflow concepts
  are translated into public-safe artifacts.
- `docs/CAPABILITY_MATRIX.md` - what this public toolkit can do, and what
  deliberately stays private.
- `docs/PUBLIC_PRESTIGE_CORE.md` - public-safe research control-plane commands.
- `docs/GETTING_STARTED.md` - step-by-step usage guide for the public-safe
  workflow.
- `docs/WORKFLOW.md` - full public-safe research-to-disclosure workflow.
- `docs/GATES.md` - compact gate catalog and decision vocabulary.
- `docs/STATE_MACHINE.md` - status vocabulary and allowed transitions.
- `docs/OPERATIONS.md` - working modes, anti-sprawl rules, session lifecycle,
  and external action boundaries.
- `docs/MAXIMUM_FORM_REVIEW.md` - public-safe maximum-form and downgrade review.
- `docs/OPEN_SOURCE_IMPACT.md` - how the work supports OSS maintainers.
- `docs/CODEX_FOR_OSS_APPLICATION.md` - concise application text snippets.
- `examples/` - synthetic examples that show safe public-writing shape.
- `schemas/` - schema for public ledger-style records.
- `templates/` - reusable maintainer-support templates.
- `tools/osssec_public/` - Python validators for the public ledger and safety
  checks, workflow state, gate records, public-safe candidate registries,
  session handoffs, and package hygiene.
- `scripts/check_public_safety.ps1` - lightweight local safety scan before
  publishing.
- `scripts/validate_public_repo.py` - cross-platform public-readiness checks.

## Checks

Run all checks:

```bash
python scripts/validate_public_repo.py
```

Run individual checks:

```bash
python -m tools.osssec_public.cli safety
python -m tools.osssec_public.cli ledger
python -m tools.osssec_public.cli evidence
python -m tools.osssec_public.cli workflow
python -m tools.osssec_public.cli state
python -m tools.osssec_public.cli gate-record experiment examples/experiment-log.json
python -m tools.osssec_public.cli gate-record max-form examples/maximum-form-review.json
python -m tools.osssec_public.cli public-core examples/public-core-registry.json
python -m tools.osssec_public.cli session-close examples/session-close.json
python -m tools.osssec_public.cli handoff examples/final-handoff.md
python -m tools.osssec_public.cli package-hygiene examples/public-package
python -m tools.osssec_public.cli advanced-gate hostile-review examples/hostile-review.json
python -m tools.osssec_public.cli advanced-gate disclosure-manifest examples/public-package/disclosure-manifest.json
python -m tools.osssec_public.cli markdown-policy
```

## Public Safety Rule

Before publishing or updating this repository, run:

```powershell
pwsh scripts/check_public_safety.ps1
```

or:

```bash
python -m tools.osssec_public.safety
```

Review every warning manually. The script is a guardrail, not a substitute for
human disclosure review.
