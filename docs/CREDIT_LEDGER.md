# Security and Engineering Contributions

**Junyi Liu** · [mosskappa](https://github.com/mosskappa)

Updated: **2026-10-20**.

Published GitHub advisories credit Junyi Liu as **Reporter in nine records,
Finder in two, and Analyst in three**. This ledger also includes GStreamer
reporting acknowledgements, upstream fixes, and maintainer credits.

[View the source index](PUBLIC_EVIDENCE_INDEX.md) for project advisories,
pull requests, commits, and acknowledgements.

## Public Reporter Credits

This section contains nine GitHub advisory credits and five separate GStreamer
CVE reporting acknowledgements from Red Hat.

| Project | Public ID | Role | Contribution |
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

| Project | Public ID | Role | Contribution |
|---|---|---|---|
| kgateway | `CVE-2026-102688` / `GHSA-36fr-64g3-wqx4` | Finder | Credited as Finder for a cross-namespace OAuth2 GatewayExtension authorization issue. |
| Buildah | `CVE-2026-44517` / `GHSA-49p4-px3h-rq49` | Finder | Credited as one of the finders of a build-context boundary issue involving remote Git or tar inputs. |

## Public Analyst Credits

| Project | Public ID | Role | Contribution |
|---|---|---|---|
| crun | `CVE-2026-47766` / `GHSA-7vwr-4279-7gq5` | Analyst | Analyzed rootfs device-directory symlink handling. |
| fuse-overlayfs | `CVE-2026-52791` / `GHSA-2cc4-p72c-v85h` | Analyst | Analyzed truncate privilege-bit handling and validated the candidate fix. The upstream patch is listed under Engineering Contributions. |
| BuildKit | `CVE-2026-15788` / `GHSA-388v-wmr2-g2v2` | Analyst | Analyzed Windows container cache-mount path resolution. |

## Public Engineering Contributions

| Project | Public ID | Role | Contribution |
|---|---|---|---|
| go-containerregistry | `google/go-containerregistry#2306` | Fix author | Authored a merged Go change that rejects symlinks and non-regular OCI blob files and checks file identity across open operations; included in v0.21.7. |
| ZenML | `zenml-io/zenml#4927` | Fix author | Authored merged resource-update authorization checks for single and batch tagging, bulk SQL resource lookup, and regression tests, with maintainer review. |
| Pants | `pantsbuild/pants#23401` | Discovery and fix credit | The maintainer explicitly credits Junyi for discovery and the fix of remote-cache writes escaping materialization roots; the maintainer submitted the merged PR. |
| Dagger | `dagger/dagger#13222` | Maintainer credit | Publicly credited in the merged Changeset removal-path validation fix; the PR and commit were authored by maintainer Marcos Nils. |
| fuse-overlayfs upstream fix | `CVE-2026-52791` / Public commit `97e0d968a782fc259ebde112db1e9b9ff1ad724f` | Fix author | Authored the upstream C fix for CVE-2026-52791, clearing SUID/SGID bits on truncate; incorporated with maintainer adjustments. |
| Shipwright | `shipwright-io/website#228` / Public maintainer acknowledgement | Security contributor | Received maintainer acknowledgement for the original security report in the project's hardening-guidance issue. |
| Synology | Public acknowledgement | Acknowledged contributor | Listed as JUNYI LIU (@mosskappa) in the Security Bug Bounty Program acknowledgements. |

## Kernel Contributions

| Project | Public evidence | Contribution |
|---|---|---|
| Linux kernel `ksmbd` | Upstream commit `69f030cf95488ae1186c72ac8c66fd279664ea7f`; `CVE-2026-64138` | Authored a C fix validating SID offsets, lengths, and arithmetic bounds before ACL inheritance. |
| Linux kernel `ksmbd` | Upstream commit `3515503322f4819277091839eed46b695096aca5`; `CVE-2026-64016` | Authored a C fix using session-aware cleanup for a republished file on durable-reconnect error paths. |

Upstream commits and linked Linux CVE records document both fixes and their
stable backports.
