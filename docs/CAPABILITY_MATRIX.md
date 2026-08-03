# Capability Matrix

This repository is not intended to be functionally identical to a private
research workspace. It preserves the public-safe, reviewer-visible parts of the
workflow and deliberately excludes sensitive operational automation.

## Capability Comparison

| Capability | Public repository | Private research workspace |
|---|---:|---:|
| Public CVE/GHSA contribution ledger | Yes | Yes |
| Public evidence link validation | Yes | Partial |
| Disclosure-safety scan | Yes | Yes |
| Markdown overclaiming scan | Yes | Yes |
| Workflow and state-machine validation | Yes | Yes |
| Target brief / experiment / maximum-form record validation | Yes | Yes |
| Public-safe record scaffolding | Yes | Partial |
| Generic candidate registry | Yes | Yes |
| Public-safe target leasing | Yes | Yes |
| Session close / final handoff gates | Yes | Yes |
| Public package hygiene checking | Yes | Yes |
| Start-mode selection gate | Yes | Yes |
| Reproducer-readiness shape gate | Yes | Yes |
| Hostile reviewer marker validation | Yes | Yes |
| Long-run final stop validation | Yes | Yes |
| Synthetic lab manifest validation | Yes | Partial |
| Hostile review templates | Yes | Yes |
| Maintainer-native validation templates | Yes | Yes |
| Private target registry with live target state | No | Yes |
| Runtime target leasing for parallel sessions | No | Yes |
| Long-run stop hooks and prompt hooks | No | Yes |
| Vendor-specific disclosure packaging | No | Yes |
| Kernel or project-specific preflight scripts | No | Yes |
| Private reproducer execution harnesses | No | Yes |
| Browser/login/submission workflow memory | No | Yes |
| Cookies, sessions, credentials, private logs, reports | No | Yes |

## Interpretation

The public repository is suitable for proving OSS security contribution process,
public evidence hygiene, claim discipline, and maintainer-facing workflow. It is
not a replacement for the private workspace used to run sensitive research.

For a public OSS or access application, this is the desired split:

- show public credit and safe tooling here;
- keep private research operations in the private workspace;
- reference real public advisories, PRs, commits, and maintainer-visible
  outcomes instead of publishing raw proof material.

## Functional Surface Today

Runnable public commands include:

```bash
python -m tools.osssec_public.cli check
python -m tools.osssec_public.cli safety
python -m tools.osssec_public.cli ledger --json
python -m tools.osssec_public.cli evidence
python -m tools.osssec_public.cli workflow
python -m tools.osssec_public.cli state
python -m tools.osssec_public.cli gate-record target-brief examples/target-brief.json
python -m tools.osssec_public.cli gate-record experiment examples/experiment-log.json
python -m tools.osssec_public.cli gate-record max-form examples/maximum-form-review.json
python -m tools.osssec_public.cli scaffold target-brief scratch/new-target.json
python -m tools.osssec_public.cli public-core examples/public-core-registry.json
python -m tools.osssec_public.cli status examples/public-core-registry.json
python -m tools.osssec_public.cli claim scratch/registry.json SYNTH-NEW-001 --owner local-session
python -m tools.osssec_public.cli session-close examples/session-close.json
python -m tools.osssec_public.cli handoff examples/final-handoff.md
python -m tools.osssec_public.cli package-hygiene examples/public-package
python -m tools.osssec_public.cli advanced-gate reproducer-ready examples/reproducer-ready.json
python -m tools.osssec_public.cli advanced-gate hostile-review examples/hostile-review.json
python -m tools.osssec_public.cli advanced-gate long-run-final examples/long-run-final.json
```

This is enough for a public-safe research control plane. It is not enough to run
private deep research by itself, and that limitation is intentional.
