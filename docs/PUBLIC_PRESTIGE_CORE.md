# Public-Safe Research Core

This repository now includes a public-safe research control plane inspired by a
private research workspace. It keeps the workflow discipline while removing
private targets, payloads, vendor state, browser sessions, and disclosure
automation.

## Core Capabilities

| Capability | Public-safe command |
|---|---|
| Registry validation | `python -m tools.osssec_public.cli public-core examples/public-core-registry.json` |
| Status summary | `python -m tools.osssec_public.cli status examples/public-core-registry.json` |
| Add generic candidate | `python -m tools.osssec_public.cli init-candidate scratch/registry.json SYNTH-NEW-001 --project example --component parser` |
| Claim candidate lease | `python -m tools.osssec_public.cli claim scratch/registry.json SYNTH-NEW-001 --owner local-session` |
| Release candidate lease | `python -m tools.osssec_public.cli release scratch/registry.json SYNTH-NEW-001 --owner local-session` |
| Session-close validation | `python -m tools.osssec_public.cli session-close examples/session-close.json` |
| Final handoff validation | `python -m tools.osssec_public.cli handoff examples/final-handoff.md` |
| Public package hygiene | `python -m tools.osssec_public.cli package-hygiene examples/public-package` |

## What This Adds

- a generic candidate registry with status, priority, mode, gates, and next
  action;
- a short-lived claim lease so multiple sessions can avoid colliding on the same
  public-safe candidate;
- session-close validation that requires evidence, decisions, tests, claim
  boundaries, and a concrete next step;
- final handoff validation that prevents incomplete "done" messages;
- package hygiene checks for public-safe report bundles.

## What Still Stays Private

- real target registry rows;
- exploit payloads and target-specific commands;
- private reproducer execution harnesses;
- vendor-specific report packages;
- browser/login/submission state;
- coordinated-disclosure logs and correspondence.

The result is not an exploit-finding engine. It is the public research control
plane: the part that proves discipline, repeatability, and disclosure hygiene.
