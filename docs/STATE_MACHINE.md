# Public Research State Machine

This state machine captures how a security signal moves through the public-safe
workflow. It is intentionally stricter than a normal task board because each
transition affects what may be claimed or published.

## States

| State | Meaning |
|---|---|
| `INTAKE` | Candidate is recorded with authorization, scope, component, and version. |
| `BOUNDARY_MODELED` | The low-trust actor, higher-trust consumer, protected boundary, and invariant are written down. |
| `EVIDENCE_BUILT` | Authorized evidence exists with an affected case and at least one control where feasible. |
| `INVARIANT_REVIEWED` | The behavior has been checked against documented design and maintainer expectations. |
| `PRIOR_ART_REVIEWED` | Advisories, issues, PRs, commits, and related reports have been checked. |
| `HOSTILE_REVIEWED` | The strongest maintainer objections and overclaiming risks have been recorded. |
| `REPORT_READY` | A conservative private report or maintainer-native validation package is ready for user approval. |
| `DISCLOSED_PRIVATE` | The report was sent through an authorized private route. |
| `PATCH_VALIDATION` | A fix, mitigation, or maintainer response is being verified. |
| `PUBLIC_CREDIT_READY` | Public evidence exists and a safe ledger entry can be published. |
| `BANKED_HARDENING` | The work is useful but should be described as hardening, not a vulnerability claim. |
| `NO_GO` | The candidate is duplicate, out of scope, unsupported, or unsafe to pursue. |
| `BLOCKED` | Progress requires maintainer input, user approval, login, private material, or a safer lab. |

## Allowed Transitions

| From | To |
|---|---|
| `INTAKE` | `BOUNDARY_MODELED`, `NO_GO`, `BLOCKED` |
| `BOUNDARY_MODELED` | `EVIDENCE_BUILT`, `BANKED_HARDENING`, `NO_GO`, `BLOCKED` |
| `EVIDENCE_BUILT` | `INVARIANT_REVIEWED`, `BANKED_HARDENING`, `NO_GO`, `BLOCKED` |
| `INVARIANT_REVIEWED` | `PRIOR_ART_REVIEWED`, `BANKED_HARDENING`, `NO_GO`, `BLOCKED` |
| `PRIOR_ART_REVIEWED` | `HOSTILE_REVIEWED`, `NO_GO`, `BLOCKED` |
| `HOSTILE_REVIEWED` | `REPORT_READY`, `BANKED_HARDENING`, `NO_GO`, `BLOCKED` |
| `REPORT_READY` | `DISCLOSED_PRIVATE`, `BLOCKED` |
| `DISCLOSED_PRIVATE` | `PATCH_VALIDATION`, `BLOCKED` |
| `PATCH_VALIDATION` | `PUBLIC_CREDIT_READY`, `BANKED_HARDENING`, `BLOCKED` |
| `BANKED_HARDENING` | `PUBLIC_CREDIT_READY`, `NO_GO` |
| `BLOCKED` | `BOUNDARY_MODELED`, `EVIDENCE_BUILT`, `REPORT_READY`, `PATCH_VALIDATION`, `NO_GO` |

## Transition Rules

- A record cannot become `REPORT_READY` without authorization, boundary,
  evidence, invariant, prior-art, hostile-review, report-quality, and route
  gates.
- A record cannot become `PUBLIC_CREDIT_READY` without an HTTPS public evidence
  URL.
- A speculative or do-not-claim item cannot become public credit.
- A hardening-only item can be public only as hardening or maintainer-support
  work, not as a vulnerability claim.
- Any state can be downgraded when new evidence weakens the claim.

## Claim Levels

Use the same claim vocabulary across notes, templates, and ledger entries:

- `PROVEN`
- `STRONGLY_SUPPORTED`
- `PLAUSIBLE_NOT_PROVEN`
- `SPECULATIVE`
- `DO_NOT_CLAIM`

Only `PROVEN` and carefully scoped `STRONGLY_SUPPORTED` claims should appear in
public summaries.
