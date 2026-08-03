# Public Gate Catalog

This catalog names the gates used by the public workflow. The gates are suitable
for public documentation because they describe process, not private findings.

| Gate | Purpose | Public-safe artifact |
|---|---|---|
| Authorization Gate | Confirm the work belongs in an owned, local, CTF, lab, OSS, or explicitly authorized setting. | Scope note. |
| Boundary Model Gate | Convert the observation into a trust-boundary claim. | Boundary summary. |
| Evidence Gate | Check affected behavior, negative control, and fixed control where available. | Evidence summary. |
| Maintainer Invariant Gate | Avoid reporting expected design or trusted-operator behavior as a vulnerability. | Invariant note. |
| Prior-Art Gate | Avoid duplicate or already-fixed reports. | Prior-art summary. |
| Hostile Review Gate | Challenge root cause, impact, duplicate risk, and overclaiming. | Hostile review decision. |
| Maximum-Form Gate | Decide whether to upgrade, bank, downgrade, or stop at the strongest responsible claim. | Maximum-form review. |
| Report Quality Gate | Make the first maintainer read concise, conservative, and actionable. | Report outline. |
| Maintainer-Native Validation Gate | Prefer validation material that matches the project's normal workflow. | Validation level. |
| Disclosure Route Gate | Choose private reporting unless the issue is already public or hardening-only. | Route decision. |
| Public Credit Gate | Publish only claims backed by public evidence. | Ledger entry. |

## Claim Level Vocabulary

Use this vocabulary when reviewing impact.

| Level | Meaning | Public wording |
|---|---|---|
| `PROVEN` | Directly observed in an authorized environment. | May be stated as observed behavior. |
| `STRONGLY_SUPPORTED` | Supported by code path plus partial validation. | Use careful language and name assumptions. |
| `PLAUSIBLE_NOT_PROVEN` | Reasonable but not validated. | Keep out of the lead; mention only if useful. |
| `SPECULATIVE` | Interesting but not evidence-backed. | Do not include in public claims. |
| `DO_NOT_CLAIM` | False, duplicate, out of scope, or too risky to state. | Exclude. |

## Disclosure Decision Vocabulary

| Decision | Meaning |
|---|---|
| `SEND_PRIVATE_CONSERVATIVE` | Ready for private maintainer report with conservative wording. |
| `REPAIR_BEFORE_REPORT` | Needs evidence, wording, or prior-art repair first. |
| `DOWNGRADE_TO_HARDENING` | Useful hardening or design discussion, not a vulnerability claim. |
| `DROP` | Do not pursue as a security report. |
| `PUBLIC_WRITEUP_READY` | Public evidence exists and the writeup avoids private material. |

## Research State Vocabulary

| State | Meaning |
|---|---|
| `INTAKE` | Candidate is scoped and authorized. |
| `BOUNDARY_MODELED` | Trust boundary and invariant are written. |
| `EVIDENCE_BUILT` | Authorized evidence and controls exist. |
| `INVARIANT_REVIEWED` | Maintainer trust-model risk was checked. |
| `PRIOR_ART_REVIEWED` | Duplicate and prior-fix risk was checked. |
| `HOSTILE_REVIEWED` | The claim survived adversarial review or was downgraded. |
| `REPORT_READY` | Conservative private report is ready for user approval. |
| `DISCLOSED_PRIVATE` | Sent through an authorized private route. |
| `PATCH_VALIDATION` | Fix or mitigation is being validated. |
| `PUBLIC_CREDIT_READY` | Public evidence supports a ledger entry. |
| `BANKED_HARDENING` | Useful work, but public wording must be hardening/support. |
| `NO_GO` | Do not pursue or claim. |
| `BLOCKED` | Needs approval, maintainer input, or a safer lab. |
