# Public Security Credit Ledger

Public identity: `JUNYI LIU` / GitHub `mosskappa`

Public sources last reviewed: **2026-10-20**.

This ledger lists public-safe security contributions only. It avoids private
case identifiers, private emails, unpublished vulnerability details,
abuse-enabling steps, vendor correspondence, and coordinated-disclosure work.

The published GitHub advisory records below contain **14 personal credits:
9 Reporter, 2 Finder, and 3 Analyst**. The count refers to distinct GHSA records;
it does not claim that every issue was independently or initially discovered by
one person. Patch authorship, maintainer acknowledgement, and stable backports
are recorded separately and do not increase that advisory count.

Primary URLs and source-specific credit details are in the
[public evidence index](PUBLIC_EVIDENCE_INDEX.md).

## Public Reporter Credits

This section contains nine GitHub advisory credits and five separate GStreamer
CVE reporting acknowledgements from Red Hat.

| Project | Public ID | Role | Public-safe summary |
|---|---|---|---|
| libheif | `CVE-2026-47709` / `GHSA-4h72-vqgp-9376` | Reporter | Reported a malformed-image handling issue that can cause a null-pointer dereference in a public libheif API. |
| pnpm | `CVE-2026-50017` / `GHSA-cjhr-43r9-cfmw` | Reporter | Reported a credential-boundary issue involving user-level credentials and repository-selected registry configuration. |
| ORAS Go | `GHSA-vh4v-2xq2-g5cg` | Reporter | Reported a registry credential-forwarding issue across HTTP origin boundaries. |
| agentgateway | `GHSA-jwm2-83f3-52xc` | Reporter | Reported a cross-namespace backend-reference authorization issue in a multi-tenant configuration. |
| mise | `CVE-2026-54557` / `GHSA-f94h-j2qg-fxw3` | Reporter | Reported an install-root boundary issue in HTTP-backend version-path handling. |
| Argo Workflows | `CVE-2026-54526` / `GHSA-48p8-g2fx-3wwm` | Reporter | Reported incomplete nested-field validation in template-referencing restrictions; credited alongside other reporters. |
| runc | `CVE-2026-41579` / `GHSA-xjvp-4fhw-gc47` | Reporter | Reported a rootfs device-directory symlink-handling issue; the advisory identifies Junyi as one of the later reporters. |
| container-libs | `CVE-2025-11395` / `GHSA-3gcv-x57j-xqxv` | Reporter | Reported an archive-extraction boundary issue affecting specific import paths; credited alongside other reporters. |
| Buildah copier Go package | `CVE-2026-79705` / `GHSA-3528-5p26-cf44` | Reporter | Reported an archive-extraction boundary issue in external uses of the copier package; Buildah itself is not affected by this advisory. |
| GStreamer gst-plugins-bad AV1 parser | `CVE-2026-52718` | Reporter | Reported byte/bit unit confusion in AV1 parser handling; acknowledged by Red Hat. |
| GStreamer gst-plugins-bad VA JPEG decoder | `CVE-2026-52719` | Reporter | Reported insufficient JPEG segment-length validation; acknowledged by Red Hat. |
| GStreamer gst-plugins-bad rfbsrc/librfb | `CVE-2026-52720` | Reporter | Reported incorrect rectangle-boundary validation; acknowledged by Red Hat. |
| GStreamer gst-plugins-bad pcapparse | `CVE-2026-52721` | Reporter | Reported insufficient IPv4/TCP header bounds validation in custom debugging pipelines; acknowledged by Red Hat. |
| GStreamer gst-plugins-bad vmncdec | `CVE-2026-52722` | Reporter | Reported integer overflow in cursor-size handling; acknowledged by Red Hat. |

## Public Finder Credits

| Project | Public ID | Role | Public-safe summary |
|---|---|---|---|
| kgateway | `CVE-2026-102688` / `GHSA-36fr-64g3-wqx4` | Finder | Credited as Finder for a cross-namespace OAuth2 GatewayExtension authorization issue. |
| Buildah | `CVE-2026-44517` / `GHSA-49p4-px3h-rq49` | Finder | Credited as one of the finders of a build-context boundary issue involving remote Git or tar inputs. |

## Public Analyst, Fix-Validation, Or Hardening Credits

| Project | Public ID | Role | Public-safe summary |
|---|---|---|---|
| crun | `CVE-2026-47766` / `GHSA-7vwr-4279-7gq5` | Analyst | Contributed analysis of rootfs device-directory symlink handling; the public advisory records Analyst credit. |
| fuse-overlayfs | `CVE-2026-52791` / `GHSA-2cc4-p72c-v85h` | Analyst | Contributed analysis and candidate-fix validation for truncate privilege-bit handling; the authored upstream fix is linked separately below as the same case. |
| BuildKit | `CVE-2026-15788` / `GHSA-388v-wmr2-g2v2` | Analyst | Contributed analysis of Windows container cache-mount path resolution; the public advisory records Analyst credit. |
| go-containerregistry | `google/go-containerregistry#2306` | Fix author | Authored a merged Go change that rejects symlinks and non-regular OCI blob files and checks file identity across open operations; included in v0.21.7. |
| ZenML | `zenml-io/zenml#4927` | Fix author | Authored merged resource-update authorization checks for single and batch tagging, bulk SQL resource lookup, and regression tests, with maintainer review. |
| Pants | `pantsbuild/pants#23401` | Discovery and fix credit | The maintainer explicitly credits Junyi for discovery and the fix of remote-cache writes escaping materialization roots; the maintainer submitted the merged PR. |
| Dagger | `dagger/dagger#13222` | Maintainer credit | Publicly credited in the merged Changeset removal-path validation fix; the PR and commit were authored by maintainer Marcos Nils. |
| fuse-overlayfs upstream fix | `CVE-2026-52791` / Public commit `97e0d968a782fc259ebde112db1e9b9ff1ad724f` | Fix author | Authored the upstream C fix clearing SUID/SGID bits on truncate, incorporated with maintainer adjustments; this is the same case as the Analyst advisory above. |
| Shipwright | `shipwright-io/website#228` / Public maintainer acknowledgement | Security contributor | The original security report received public maintainer acknowledgement in the hardening-guidance issue; no CVE/GHSA is claimed. |
| Synology | Public acknowledgement | Acknowledged contributor | The Security Bug Bounty Program acknowledgement list includes JUNYI LIU (@mosskappa); the listing does not specify individual issues or compensation. |

## Kernel Contributions

| Project | Public evidence | Public-safe summary |
|---|---|---|
| Linux kernel `ksmbd` | Upstream commit `69f030cf95488ae1186c72ac8c66fd279664ea7f`; `CVE-2026-64138` | Authored a C fix validating SID offsets, lengths, and arithmetic bounds before ACL inheritance. |
| Linux kernel `ksmbd` | Upstream commit `3515503322f4819277091839eed46b695096aca5`; `CVE-2026-64016` | Authored a C fix using session-aware cleanup for a republished file on durable-reconnect error paths. |

Both fixes have upstream signed-off author records and public Linux CVE
cross-references. Stable backports are downstream adoption of these same fixes,
not additional original patches or independently discovered vulnerabilities.

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
