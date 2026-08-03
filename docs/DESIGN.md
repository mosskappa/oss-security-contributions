# Design

This repository separates three concerns that are often mixed together in
security portfolios.

## Public Claims

`docs/CREDIT_LEDGER.md` states what can be claimed publicly. Each claim should be
conservative, role-specific, and free of operational abuse details.

## Public Evidence

`docs/PUBLIC_EVIDENCE_INDEX.md` links claims to public URLs. Private emails,
ticket systems, bounty portals, and unpublished reports are intentionally not
acceptable evidence sources for this public repository.

## Public-Readiness Checks

`tools/osssec_public/` contains validators that help catch accidental disclosure
before publishing:

- `safety.py` scans for secrets and private identifiers.
- `ledger.py` checks ledger shape and wording.
- `evidence.py` checks public evidence rows.
- `workflow.py` checks public-safe workflow status records.
- `markdown_policy.py` checks public Markdown for risky disclosure shape.
- `cli.py` exposes the checks as a small command-line tool.

The checks are intentionally lightweight and dependency-free so maintainers can
run them before publishing, in CI, or from constrained environments.
