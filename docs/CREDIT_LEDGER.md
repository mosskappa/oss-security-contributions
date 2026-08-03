# Public Security Credit Ledger

Public identity: `JUNYI LIU` / GitHub `mosskappa`

This ledger lists public-safe security contributions only. It avoids private
case identifiers, private emails, unpublished vulnerability details,
abuse-enabling steps, vendor correspondence, and coordinated-disclosure work.

## Public Reporter Credits

| Project | Public ID | Role | Public-safe summary |
|---|---|---|---|
| libheif | `CVE-2026-47709` / `GHSA-4h72-vqgp-9376` | Reporter | Reported a published libheif vulnerability. |
| pnpm | `CVE-2026-50017` / `GHSA-cjhr-43r9-cfmw` | Reporter | Reported a published pnpm credential-boundary issue involving npm registry configuration. |
| ORAS Go | `GHSA-vh4v-2xq2-g5cg` | Reporter | Reported a published ORAS Go registry credential-forwarding issue. |
| agentgateway | `GHSA-jwm2-83f3-52xc` | Reporter | Reported a published cross-namespace backend-reference issue. |
| mise | `CVE-2026-54557` / `GHSA-f94h-j2qg-fxw3` | Reporter | Reported a published install-root path-materialization issue. |
| GStreamer gst-plugins-bad AV1 parser | `CVE-2026-52718` | Reporter | Reported a published parser-handling issue. |
| GStreamer gst-plugins-bad JPEG parser | `CVE-2026-52719` | Reporter | Reported a published parser-handling issue. |
| GStreamer gst-plugins-bad rfbsrc/librfb | `CVE-2026-52720` | Reporter | Reported a published bounds-handling issue. |
| GStreamer gst-plugins-bad pcapparse | `CVE-2026-52721` | Reporter | Reported a published packet/header parsing issue. |
| GStreamer gst-plugins-bad vmncdec | `CVE-2026-52722` | Reporter | Reported a published cursor size-handling issue. |

## Public Analyst, Fix-Validation, Or Hardening Credits

| Project | Public ID | Role | Public-safe summary |
|---|---|---|---|
| crun | `CVE-2026-47766` / `GHSA-7vwr-4279-7gq5` | Analyst | Contributed analysis and fix-path validation for a published crun advisory. |
| fuse-overlayfs | `CVE-2026-52791` / `GHSA-2cc4-p72c-v85h` | Analyst | Contributed analysis and fix validation for a published fuse-overlayfs advisory. |
| go-containerregistry | `google/go-containerregistry#2306` | Fix author | Authored a merged security-hardening change for OCI layout blob handling. |
| Shipwright | Public hardening guidance / maintainer acknowledgement | Security contributor | Contributed to hardening guidance for a multi-tenant build-platform weakness; not claimed as a CVE/GHSA. |
| BuildKit | `CVE-2026-15788` / `GHSA-388v-wmr2-g2v2` | Analyst | Contributed analysis for a published BuildKit advisory. |

## Kernel Contributions

| Project | Public evidence | Public-safe summary |
|---|---|---|
| Linux kernel `ksmbd` | Upstream commit `69f030cf95488ae1186c72ac8c66fd279664ea7f` | Contributed a signed-off security fix related to SID validation. |
| Linux kernel `ksmbd` | Upstream commit `3515503322f4819277091839eed46b695096aca5` | Contributed a signed-off security fix related to durable reconnect lifetime handling. |

## Not Publicly Listed Here

The following categories are intentionally omitted until a public advisory,
public maintainer acknowledgement, or public CVE/GHSA record exists:

- Draft advisories.
- Coordinated-disclosure reports that are not yet public.
- Vendor-private program reports.
- Ongoing exploitability investigations.
- Reports closed as duplicate, informative, not applicable, or hardening-only
  unless there is public maintainer acknowledgement and conservative wording.

## Wording Rules

- Use `reported` only when public reporter credit exists.
- Use `analyst` only when public metadata records analyst-style credit.
- Use `security-hardening contribution` for merged defensive changes without a
  CVE or GHSA.
- Do not claim a CVE/GHSA until the advisory is public.
- Do not publish abuse-enabling details or private reproducer material in this
  repo.

## Needs Public Credit Verification Before Listing

These items may exist in private notes or historical local records, but should
not be used as public claims from this repository unless a public page visibly
confirms the identity and credit type.

| Project | Public ID | Current public-repo rule |
|---|---|---|
| LlamaIndex | `CVE-2025-3046` | Do not list as a `JUNYI LIU` public credit here unless a public Huntr/GHSA/vendor page visibly confirms the credit. |
