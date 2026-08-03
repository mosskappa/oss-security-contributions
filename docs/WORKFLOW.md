# Public-Safe OSS Security Workflow

This workflow is the public version of the research process used to move from a
weak security signal to a maintainer-ready report or public-safe credit entry.

It is intentionally conservative. The workflow is designed to prevent three
common failures:

- publishing private or coordinated-disclosure material too early;
- overclaiming impact beyond the evidence;
- sending maintainers reports that are hard to triage.

## Phase 0: Intake

Goal: decide whether the candidate belongs in responsible security research.

Required outputs:

- project and component name;
- authorization basis;
- affected version or commit;
- initial trust boundary;
- what is known, unknown, and explicitly not claimed.

Stop if:

- authorization is unclear;
- the only path requires unauthorized production testing;
- the candidate depends on private data or third-party credentials.

Public artifact: `templates/TARGET_BRIEF.md`.

## Phase 1: Boundary Model

Goal: write the issue as a precise boundary claim.

Required outputs:

- low-trust actor or input;
- higher-trust consumer, parser, resolver, controller, or runtime;
- protected asset or invariant;
- observed consequence.

Good claim shape:

```text
An untrusted input can cause a higher-trust component to act across a boundary
that the project appears to protect.
```

## Phase 2: Evidence Build

Goal: prove observed behavior without turning public material into an abuse
guide.

Required outputs:

- clean local or authorized environment;
- affected version;
- observed vulnerable behavior;
- negative control;
- fixed control when available;
- concise evidence excerpts.

Public repository rule: keep only high-level evidence shape here. Private
commands, private samples, and target-specific materials stay out of this repo.

Public artifact: `templates/EXPERIMENT_LOG_PUBLIC.md`.

## Phase 3: Maintainer Invariant Gate

Goal: avoid reporting behavior that is merely documented trust model,
administrator intent, or expected design.

Required questions:

- What invariant does the project appear to promise?
- Where is that invariant documented or implied?
- Why does the observed behavior violate it?
- Why is this not only trusted-operator behavior?

Decision:

- `PASS`: continue.
- `DOWNGRADE`: use hardening or design-discussion wording.
- `DROP`: do not report as a vulnerability.

## Phase 4: Prior-Art Gate

Goal: avoid duplicate reports and learn from existing fixes.

Required outputs:

- advisories reviewed;
- public issues or PRs reviewed;
- relevant commits reviewed;
- novelty statement.

Decision:

- `NEW`: continue.
- `VARIANT`: explain the new sink, trigger, version, or impact boundary.
- `DUPLICATE`: do not claim new credit.

Public artifact: `templates/PRIOR_ART_REVIEW.md`.

## Phase 5: Hostile Review Gate

Goal: challenge the report before a maintainer has to.

Required questions:

- What is the single primary root cause?
- What is the strongest proven default-path impact?
- Which impact claims are only plausible?
- Which high-impact words should be removed or moved out of the lead?
- What are the top reasons a maintainer might close or downgrade this?

Claim levels:

- `PROVEN`
- `STRONGLY_SUPPORTED`
- `PLAUSIBLE_NOT_PROVEN`
- `SPECULATIVE`
- `DO_NOT_CLAIM`

Decision:

- `KEEP`
- `KEEP_WITH_CAUTION`
- `REPAIR`
- `DOWNGRADE`
- `DROP`

Public artifact: `templates/HOSTILE_REVIEW_PUBLIC.md`.

## Phase 5.5: Maximum-Form Review

Goal: decide whether the strongest responsible claim has been reached, or
whether the candidate should be upgraded, banked, downgraded, or dropped.

Required questions:

- What is the emergency-patch thesis?
- What is the strongest concrete marker actually proven?
- What is the strongest reasonable maintainer objection?
- What upgrade routes were tested or closed?
- What would be unsafe, unauthorized, or speculative to keep pursuing?

Decision:

- `CONTINUE_TO_REPORT`
- `BANK_AS_STABLE_CREDIT`
- `BANK_AS_HARDENING`
- `REPAIR_BEFORE_REPORT`
- `NO_GO_TRUST_MODEL`
- `MANUAL_BOUNDARY`

Public artifact: `templates/MAXIMUM_FORM_REVIEW_PUBLIC.md`.

## Phase 6: Report Quality Gate

Goal: make the first maintainer read useful in five minutes.

Required sections:

- summary;
- affected component and version;
- security boundary;
- observed impact;
- root cause;
- evidence summary;
- expected behavior;
- suggested validation or defensive note;
- non-claims.

Tone rules:

- one primary vulnerability sentence;
- conservative impact wording;
- no pressure for bounty, CVE, or timeline in first contact;
- no unexplained AI/tool framing;
- no scanner-like output dump.

## Phase 7: Maintainer-Native Validation Gate

Goal: ensure the maintainer can understand or rerun the evidence without
depending on private local machinery.

Decision levels:

- `LEVEL_1_SUMMARY`: concise report evidence only.
- `LEVEL_2_NATIVE_VALIDATION`: small project-native validation material.
- `LEVEL_3_INTERNAL_PROOF`: retained privately unless requested and sanitized.

Public repository rule: this repo may describe the levels, but it must not store
private validation material for real findings.

Public artifact: `templates/MAINTAINER_NATIVE_VALIDATION.md`.

## Phase 8: Disclosure Route Gate

Goal: choose the safest route.

Preferred order:

- project private security advisory or private reporting channel;
- security contact listed by the project;
- maintainer-requested private route;
- public issue only for non-sensitive hardening or already-public issues.

Do not use a public issue for a non-public vulnerability.

## Phase 9: Public Credit Gate

Goal: decide what can be listed publicly after disclosure.

Required public evidence:

- public CVE, GHSA, advisory, PR, commit, release note, or maintainer
  acknowledgement;
- visible credit identity or conservative role wording;
- no reliance on private messages as public proof.

Decision:

- `PUBLIC_CREDIT_READY`
- `PUBLIC_HARDENING_ONLY`
- `PRIVATE_ONLY_FOR_NOW`
- `DO_NOT_LIST`

## Continuous Rule

Every phase can downgrade the claim. Downgrading is not failure; it is how the
workflow stays useful and trustworthy.

See also:

- `docs/STATE_MACHINE.md`
- `docs/OPERATIONS.md`
- `docs/MAXIMUM_FORM_REVIEW.md`
- `docs/RESEARCH_WORKFLOW_MAPPING.md`
