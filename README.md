# OSS Security Contributions

**Junyi Liu** · [mosskappa](https://github.com/mosskappa)

This repository collects my upstream code changes, security reports, and
maintainer acknowledgements. It also includes Python tools for maintaining
contribution records and source links.

## Selected Engineering Contributions

Updated: **2026-10-20**.

| Project | Engineering work | Role and status | Sources |
|---|---|---|---|
| ZenML | Resource-update authorization for single and batch tagging, bulk SQL resource lookup, and regression tests. | PR author; merged 2026-06-12 after maintainer review. | [PR #4927](https://github.com/zenml-io/zenml/pull/4927) |
| Google go-containerregistry | OCI layout blob-read checks for symlinks, non-regular files, and file identity across open operations. | PR author; merged 2026-06-02 and included in v0.21.7. | [PR #2306](https://github.com/google/go-containerregistry/pull/2306), [release v0.21.7](https://github.com/google/go-containerregistry/releases/tag/v0.21.7) |
| Linux kernel ksmbd | SID bounds validation during ACL inheritance and session-aware cleanup on durable-reconnect error paths. | Author of two upstream C fixes, associated with CVE-2026-64138 and CVE-2026-64016. | [SID validation commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=69f030cf95488ae1186c72ac8c66fd279664ea7f), [reconnect lifetime commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3515503322f4819277091839eed46b695096aca5) |
| fuse-overlayfs | Clearing SUID/SGID bits on truncate. | Fix author; incorporated with maintainer adjustments on 2026-06-09. Analyst credit in the related advisory. | [Upstream commit](https://github.com/containers/fuse-overlayfs/commit/97e0d968a782fc259ebde112db1e9b9ff1ad724f), [CVE-2026-52791 advisory](https://github.com/containers/fuse-overlayfs/security/advisories/GHSA-2cc4-p72c-v85h) |

## Contribution Records

- [Contribution ledger](docs/CREDIT_LEDGER.md): security reports, upstream fixes,
  and maintainer acknowledgements.
- [Source index](docs/PUBLIC_EVIDENCE_INDEX.md): project advisories, pull requests,
  commits, and acknowledgements for the listed work.

## Contribution Toolkit

The Python CLI supports repeatable research documentation and record maintenance:

- Validate advisory identifiers and source links.
- Track research status and review records.
- Check Markdown and file packages before publication.
- Create project briefs, review templates, and handoff records.

## Quick Start

```bash
python -m pip install -e .
osssec-public doctor
osssec-public demo
python -m tools.osssec_public.cli ledger --json
python -m tools.osssec_public.cli evidence
```

See the [getting started guide](docs/GETTING_STARTED.md) for a complete walkthrough.

## Development Checks

```bash
python scripts/validate_public_repo.py
python -m pytest
```

## Documentation

- [Getting started](docs/GETTING_STARTED.md)
- [Toolkit design](docs/DESIGN.md)
- [Research workflow](docs/WORKFLOW.md)
- [Templates](templates/) and [examples](examples/)
- [Contribution guidelines](CONTRIBUTING.md)
- [Publication guidelines](docs/PUBLICATION_BOUNDARIES.md)
- [Security policy](SECURITY.md)

## License

[MIT](LICENSE)
