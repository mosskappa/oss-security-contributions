# OSS Security Contributions

Public-safe toolkit for maintaining OSS security contribution ledgers, validating
public evidence, and preventing accidental disclosure of private vulnerability
material.

Maintained by Junyi Liu (`mosskappa`), this repository supports responsible
open-source security work without publishing exploit material or private vendor
correspondence. It combines a public CVE/GHSA contribution ledger with reusable
checks, templates, and examples for maintainer-friendly security workflows.

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
- Synthetic examples and templates for safe maintainer-facing workflows.
- Tests and GitHub Actions workflow for repeatable public-readiness checks.

## Quick Start

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

## Highlights

- Public reporter credits across libheif, pnpm, mise, GStreamer, ORAS Go, and
  agentgateway.
- Analyst or fix-validation contributions for container and filesystem-adjacent
  projects including crun, fuse-overlayfs, and BuildKit.
- Public security-hardening contribution to `google/go-containerregistry`.
- Linux kernel `ksmbd` security-fix contributions with signed-off commits.

See [docs/CREDIT_LEDGER.md](docs/CREDIT_LEDGER.md) for the public-safe ledger.

## Repository Layout

- `docs/CREDIT_LEDGER.md` - public-safe security contribution ledger.
- `docs/PUBLIC_EVIDENCE_INDEX.md` - public links supporting public claims.
- `docs/PUBLICATION_BOUNDARIES.md` - what may and may not be published here.
- `docs/RESEARCH_WORKFLOW_MAPPING.md` - how private research workflow concepts
  are translated into public-safe artifacts.
- `docs/CAPABILITY_MATRIX.md` - what this public toolkit can do, and what
  deliberately stays private.
- `docs/PUBLIC_PRESTIGE_CORE.md` - public-safe research control-plane commands.
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
