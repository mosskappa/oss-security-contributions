# Private-To-Public Research Workflow Mapping

This repository is derived from a private security research operating model, but
it is not a mirror of that workspace. The public repository keeps the durable
process, evidence discipline, and maintainer-support lessons while excluding
private targets, reports, logs, credentials, browser state, and exploit detail.

## What Moves Publicly

| Private concept | Public-safe form in this repository |
|---|---|
| Target registry | Target brief template with synthetic examples only. |
| Run state | Workflow status JSON and state-machine validation. |
| Experiment logs | Public experiment-log shape without real private commands or samples. |
| Upgrade gate | Capability and claim-level review vocabulary. |
| High-impact hard gate | Public maximum-form review that focuses on evidence, boundary, and downgrade rules. |
| Hostile review | Maintainer-objection review template. |
| Reproducer-ready gate | Maintainer-native validation levels. |
| Disclosure checklist | First-contact and route-selection templates. |
| Patch validation | Patch-validation note and fixed-control language. |
| Public credit tracking | Public evidence ledger backed only by visible advisories, PRs, commits, or acknowledgements. |

## What Does Not Move

The following materials stay private unless a maintainer or program explicitly
asks for them through an authorized channel:

- coordinated-disclosure reports before public disclosure;
- vendor correspondence, ticket IDs, compensation records, and private program
  names;
- real exploit material, target-specific payloads, private samples, or full
  attack chains;
- browser profiles, cookies, tokens, session databases, email exports, and
  local machine paths;
- internal target IDs, private lane names, operational logs, and personal notes;
- evidence from live third-party systems or any environment without explicit
  authorization.

## Public Design Goal

The goal is to prove research maturity without publishing unsafe material. A
reviewer should be able to see that the contributor can:

- choose targets by authorization, boundary, and maintainer route;
- distinguish weak signals from report-ready findings;
- challenge their own claims before sending them to maintainers;
- provide useful validation while avoiding abuse-enabling publication;
- update public credit only when public evidence supports the claim.

## Translation Rules

Use these rules when moving a private lesson into this repository:

1. Convert target-specific details into a generic process rule.
2. Replace private project names with neutral component classes.
3. Replace commands and payloads with evidence requirements.
4. Replace internal grades with public claim levels and disclosure decisions.
5. Keep only information that would still be safe if copied into a public issue.

When in doubt, leave the detail private and publish only the control that would
have caught the mistake.
