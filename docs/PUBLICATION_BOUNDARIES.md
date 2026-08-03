# Publication Boundaries

This repository is public-safe by design. It documents open-source security
contributions without publishing material that could harm users, violate vendor
trust, or weaken coordinated disclosure.

## Allowed

- Public CVE and GHSA identifiers.
- Public advisory names and public merged PR references.
- High-level vulnerability class summaries.
- Defensive workflow templates.
- Patch-validation notes that do not include abuse-enabling steps.
- Public maintainer acknowledgements that are already visible on the web.

## Not Allowed

- Private emails, message IDs, case identifiers, compensation details, or
  screenshots from private systems.
- Cookies, sessions, browser profiles, bearer tokens, credentials, API keys,
  recovery codes, or account identifiers.
- Embargoed or unpublished vulnerability details.
- Full proof-of-concept code for active or recently disclosed vulnerabilities.
- Target-specific paths or step-by-step abuse instructions that materially
  increase exploitation capability.
- Vendor-specific details before the vendor publishes an advisory or gives
  explicit public-credit permission.

## Sanitization Checklist

Before publishing:

- Confirm every CVE/GHSA/advisory entry is public.
- Remove private correspondence and internal evidence IDs.
- Replace exploitation mechanics with vulnerability-class language.
- Keep proof material private unless maintainers explicitly request it through a
  responsible disclosure channel.
- Run `scripts/check_public_safety.ps1`.
- Run `python -m tools.osssec_public.cli package-hygiene <public-package>` for
  public report packages.
- Manually review every warning.

## Disclosure Philosophy

The goal is to help maintainers, not to race them. Public writing should make
the contribution legible without turning the repository into an abuse guide.
