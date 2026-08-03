# Maximum-Form Review

Maximum-form review is the public-safe version of the private upgrade gate. It
asks whether a candidate has reached its strongest responsible claim under the
current authorization, lab, and evidence constraints.

This is not a severity inflation exercise. It is a discipline for avoiding both
under-analysis and overclaiming.

## Emergency Thesis

Before treating a candidate as high-impact, write one sentence:

```text
If this is true, maintainers would patch urgently because a lower-trust actor
can make a higher-trust deployed consumer produce a concrete security effect in
a common or documented workflow.
```

The sentence must name:

- the actor;
- the higher-trust consumer;
- the protected boundary;
- the concrete observed or safely modeled effect;
- the common workflow or documented promise.

## Impact Markers

Prefer concrete markers over adjectives:

- controlled command marker in a local lab;
- credential or secret exposure across a trust boundary;
- unauthorized write, cache, registry, artifact, or provenance mutation;
- privilege, namespace, tenant, container, host, or controller authority change;
- release-build memory corruption with realistic application reachability;
- maintainer-confirmed security invariant break relied on by downstream users.

If no marker is proven, the correct result may still be useful hardening, but it
should not be presented as a high-impact vulnerability.

## Maintainer Objection Prefilter

Write the strongest likely maintainer objection before packaging:

```text
A maintainer could reasonably say this is trusted configuration, expected
operator behavior, a same-host hardening issue, duplicate prior art, or a local
sanitizer edge case.
```

If that objection is accurate and no stronger boundary is proven, bank or
downgrade the candidate instead of sending an inflated report.

## Capability Closure

For each candidate, record:

- strongest proven capability;
- strongest plausible but unproven capability;
- cheapest safe experiment that would upgrade the claim;
- experiments already run;
- routes blocked by authorization, safety, or missing lab fidelity;
- final decision.

## Decisions

| Decision | Meaning |
|---|---|
| `CONTINUE_TO_REPORT` | Evidence is strong enough for conservative private reporting. |
| `BANK_AS_STABLE_CREDIT` | Useful, likely maintainer-actionable, but not the high-impact finish line. |
| `BANK_AS_HARDENING` | Useful hardening/design note, not a vulnerability claim. |
| `REPAIR_BEFORE_REPORT` | Needs stronger evidence, clearer wording, or prior-art cleanup. |
| `NO_GO_TRUST_MODEL` | The trusted model or design expectation defeats the claim. |
| `MANUAL_BOUNDARY` | The next proof requires user approval, maintainer input, or a safer environment. |

## Public Rule

This repository may store the review structure and synthetic examples. It should
not store real exploit chains, private reproducer commands, target-specific
payloads, or embargoed maintainer evidence.
