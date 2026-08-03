# Contributing

This project accepts public-safe improvements only.

Good contributions:

- Improve validators, schemas, examples, or documentation.
- Add tests for public-readiness checks.
- Improve conservative wording rules.
- Add public evidence links for already-published advisories or merged PRs.

Do not submit:

- Private reports, private emails, screenshots from vendor systems, or case IDs.
- Exploit code, private reproducers, target-specific probes, or active findings.
- Secrets, cookies, sessions, API keys, tokens, or credentials.
- Claims that are not backed by a public advisory, public PR, public commit, or
  public maintainer acknowledgement.

Before opening a pull request:

```bash
python scripts/validate_public_repo.py
python -m pytest
```

