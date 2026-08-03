# Public Operations Model

This document describes the public-safe operating discipline behind the
templates and checks in this repository.

## Working Modes

| Mode | Goal | Default finish line |
|---|---|---|
| Stable credit | Maximize accepted maintainer outcomes, CVE/GHSA/advisory credit, and clean patch validation. | Conservative report or public evidence update. |
| Deep impact review | Test whether a signal reaches a stronger boundary or concrete capability. | Maximum-form decision: upgrade, bank, downgrade, or no-go. |
| Maintenance follow-up | Support maintainers after a report, patch, advisory, or PR is in motion. | Verified fix, clarified report, or public-safe ledger update. |

## Anti-Sprawl Rules

- Every candidate needs one current status record.
- Public-safe candidate queues live in registry JSON files and can be checked
  with `python -m tools.osssec_public.cli public-core <registry>`.
- When more than one session may work from the same public-safe registry, claim
  a short-lived lease with `python -m tools.osssec_public.cli claim <registry>
  <candidate-id> --owner <session>`.
- Every meaningful experiment needs an evidence note or explicit no-go reason.
- Every report candidate needs hostile review before maintainer contact.
- Every public claim needs a public evidence link.
- Old candidates should be marked banked, blocked, or no-go instead of left as
  ambiguous open work.

## Session Lifecycle

Start:

- identify the current mode;
- load the current target brief or workflow status;
- check whether the next step is local, authorized, and safe.

During work:

- record evidence in reproducible language;
- separate proven behavior from plausible impact;
- downgrade quickly when a maintainer objection is likely correct;
- stop before login, payment, identity, live-third-party, or final-submit
  boundaries.

Close:

- update state;
- record the next concrete action;
- note blockers and user-approval points;
- validate session close and final handoff records when a session produces a
  handoff;
- keep public artifacts free of private material.

Useful close commands:

```bash
python -m tools.osssec_public.cli session-close examples/session-close.json
python -m tools.osssec_public.cli handoff examples/final-handoff.md
```

Advanced gate commands:

```bash
python -m tools.osssec_public.cli advanced-gate reproducer-ready examples/reproducer-ready.json
python -m tools.osssec_public.cli advanced-gate hostile-review examples/hostile-review.json
python -m tools.osssec_public.cli advanced-gate long-run-final examples/long-run-final.json
```

## External Action Boundaries

The workflow can prepare reports, summaries, and validation material, but these
actions require explicit user approval:

- sending a disclosure;
- creating or updating a public issue with security content;
- contacting maintainers or program staff;
- using real third-party accounts, tokens, production systems, or payment/KYC
  flows;
- publishing a new public repository or pushing to GitHub.

## Safe Evidence Principle

Public evidence should answer "why is this contribution real?" without teaching
"how to abuse this exact system." Prefer advisories, merged fixes, commit links,
public acknowledgements, and sanitized validation summaries.

Before publishing a public report package, run:

```bash
python -m tools.osssec_public.cli package-hygiene examples/public-package
```
