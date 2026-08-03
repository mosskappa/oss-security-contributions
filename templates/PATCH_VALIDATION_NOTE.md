# Patch Validation Note Template

## Summary

Briefly describe the boundary that the patch is intended to protect.

## Public Status

- Advisory/CVE/GHSA public: yes/no
- Public issue or PR: link or `not public`
- Credit wording: reporter / analyst / fix author / hardening contributor

## Validation

- [ ] Added or reviewed regression coverage.
- [ ] Confirmed the old behavior is no longer reachable in the authorized test
      environment.
- [ ] Checked adjacent code paths for equivalent bypasses.
- [ ] Confirmed the patch does not rely only on documentation or caller trust.
- [ ] Confirmed public writeup avoids abuse-enabling instructions.

## Notes For Maintainers

Write concise maintainer-facing notes here. Keep sensitive reproducer material
private.
