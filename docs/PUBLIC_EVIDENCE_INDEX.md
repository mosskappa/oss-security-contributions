# Contribution Sources

Updated: **2026-10-20**.

Project advisories, pull requests, commits, and acknowledgements supporting the
[contribution ledger](CREDIT_LEDGER.md).

## Published GitHub Advisories

These 14 distinct GHSA records credit `mosskappa` as **9 Reporter, 2 Finder,
and 3 Analyst**. Dates below are the project advisory publication dates.

| Project | Public ID | Evidence URL | Source detail |
|---|---|---|---|
| libheif | `CVE-2026-47709` / `GHSA-4h72-vqgp-9376` | https://github.com/strukturag/libheif/security/advisories/GHSA-4h72-vqgp-9376 | Published 2026-05-19; credits `mosskappa` as Reporter. |
| pnpm | `CVE-2026-50017` / `GHSA-cjhr-43r9-cfmw` | https://github.com/pnpm/pnpm/security/advisories/GHSA-cjhr-43r9-cfmw | Published 2026-05-28; credits `mosskappa` as Reporter. |
| ORAS Go | `GHSA-vh4v-2xq2-g5cg` | https://github.com/oras-project/oras-go/security/advisories/GHSA-vh4v-2xq2-g5cg | Published 2026-06-11; credits `mosskappa` as Reporter. |
| agentgateway | `GHSA-jwm2-83f3-52xc` | https://github.com/agentgateway/agentgateway/security/advisories/GHSA-jwm2-83f3-52xc | Published 2026-06-29; credits `mosskappa` as Reporter and a maintainer as Remediation developer. |
| mise | `CVE-2026-54557` / `GHSA-f94h-j2qg-fxw3` | https://github.com/jdx/mise/security/advisories/GHSA-f94h-j2qg-fxw3 | Published 2026-06-12; credits `mosskappa` as Reporter. |
| Argo Workflows | `CVE-2026-54526` / `GHSA-48p8-g2fx-3wwm` | https://github.com/argoproj/argo-workflows/security/advisories/GHSA-48p8-g2fx-3wwm | Published 2026-06-10; credits `mosskappa` as one of several Reporters. |
| runc | `CVE-2026-41579` / `GHSA-xjvp-4fhw-gc47` | https://github.com/opencontainers/runc/security/advisories/GHSA-xjvp-4fhw-gc47 | Published 2026-06-13; credits `mosskappa` as Reporter and explicitly identifies Junyi as a later reporter. |
| container-libs | `CVE-2025-11395` / `GHSA-3gcv-x57j-xqxv` | https://github.com/podman-container-tools/container-libs/security/advisories/GHSA-3gcv-x57j-xqxv | Published 2026-09-17; credits `mosskappa` as one of several Reporters. |
| Buildah copier Go package | `CVE-2026-79705` / `GHSA-3528-5p26-cf44` | https://github.com/podman-container-tools/buildah/security/advisories/GHSA-3528-5p26-cf44 | Published 2026-09-17; credits `mosskappa` as Reporter. The advisory covers external package use and excludes Buildah itself. |
| kgateway | `CVE-2026-102688` / `GHSA-36fr-64g3-wqx4` | https://github.com/kgateway-dev/kgateway/security/advisories/GHSA-36fr-64g3-wqx4 | Published 2026-08-11; credits `mosskappa` as Finder. |
| Buildah | `CVE-2026-44517` / `GHSA-49p4-px3h-rq49` | https://github.com/podman-container-tools/buildah/security/advisories/GHSA-49p4-px3h-rq49 | Published 2026-06-12; credits `mosskappa` and another contributor as Finders. |
| crun | `CVE-2026-47766` / `GHSA-7vwr-4279-7gq5` | https://github.com/containers/crun/security/advisories/GHSA-7vwr-4279-7gq5 | Published 2026-05-27; credits `mosskappa` as Analyst and documents analysis of the affected behavior. |
| fuse-overlayfs | `CVE-2026-52791` / `GHSA-2cc4-p72c-v85h` | https://github.com/containers/fuse-overlayfs/security/advisories/GHSA-2cc4-p72c-v85h | Published 2026-06-09; credits `mosskappa` as Analyst. The upstream fix for this advisory is linked below. |
| BuildKit | `CVE-2026-15788` / `GHSA-388v-wmr2-g2v2` | https://github.com/moby/buildkit/security/advisories/GHSA-388v-wmr2-g2v2 | Published 2026-07-16; credits `mosskappa` as Analyst. |

## GStreamer Reporting Acknowledgements

The Red Hat pages below identify the reporter, in addition to documenting the
underlying CVE. These five CVEs are separate from the 14 GHSA records above.

| Project | Public ID | Evidence URL | Source detail |
|---|---|---|---|
| GStreamer AV1 parser | `CVE-2026-52718` | https://access.redhat.com/security/cve/cve-2026-52718 | Red Hat publicly thanks `JUNYI LIU` for reporting this issue. |
| GStreamer VA JPEG decoder | `CVE-2026-52719` | https://access.redhat.com/security/cve/cve-2026-52719 | Red Hat publicly thanks `JUNYI LIU` for reporting this issue. |
| GStreamer rfbsrc/librfb | `CVE-2026-52720` | https://access.redhat.com/security/cve/cve-2026-52720 | Red Hat publicly thanks `JUNYI LIU` for reporting this issue. |
| GStreamer pcapparse | `CVE-2026-52721` | https://access.redhat.com/security/cve/cve-2026-52721 | Red Hat publicly thanks `JUNYI LIU` for reporting this issue. |
| GStreamer vmncdec | `CVE-2026-52722` | https://access.redhat.com/security/cve/cve-2026-52722 | Red Hat publicly thanks `JUNYI LIU` for reporting this issue. |

## Upstream Fixes And Maintainer Credits

| Project | Public ID | Evidence URL | Source detail |
|---|---|---|---|
| go-containerregistry | `google/go-containerregistry#2306` | https://github.com/google/go-containerregistry/pull/2306 | PR authored by `mosskappa`; merged 2026-06-02. Implements OCI blob-read checks with focused regression coverage. |
| ZenML | `zenml-io/zenml#4927` | https://github.com/zenml-io/zenml/pull/4927 | PR authored by `mosskappa`; merged 2026-06-12. Includes authorization checks, bulk SQL resource lookup, regression tests, and review revisions. |
| Pants | `pantsbuild/pants#23401` | https://github.com/pantsbuild/pants/pull/23401#issuecomment-4654499109 | Maintainer `benjyw` explicitly credits Junyi for discovery and the fix; the maintainer-submitted PR merged 2026-06-26. |
| Dagger | `dagger/dagger#13222` | https://github.com/dagger/dagger/pull/13222 | Maintainer-authored PR credits `JUNYI LIU`; merged 2026-05-29. |
| Dagger | `60f9baabe9ea8a7ef9a27cea84670869238163fe` | https://github.com/dagger/dagger/commit/60f9baabe9ea8a7ef9a27cea84670869238163fe | Commit dated 2026-05-26 credits `JUNYI LIU`; author and committer are Marcos Nils. Supports the same contribution as PR #13222. |
| fuse-overlayfs | `97e0d968a782fc259ebde112db1e9b9ff1ad724f` | https://github.com/containers/fuse-overlayfs/commit/97e0d968a782fc259ebde112db1e9b9ff1ad724f | Upstream fix for CVE-2026-52791, dated 2026-06-09; `JUNYI LIU` is the author and Giuseppe Scrivano is the committer. |
| Linux kernel ksmbd SID validation | `69f030cf95488ae1186c72ac8c66fd279664ea7f` | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=69f030cf95488ae1186c72ac8c66fd279664ea7f | Upstream signed-off commit identifies Junyi as author of the SID-validation fix. |
| Linux kernel ksmbd reconnect lifetime | `3515503322f4819277091839eed46b695096aca5` | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3515503322f4819277091839eed46b695096aca5 | Upstream signed-off commit identifies Junyi as author of the durable-reconnect lifetime fix. |
| Linux kernel ksmbd SID validation | `CVE-2026-64138` | https://kernel.googlesource.com/pub/scm/linux/security/vulns/+/532b7a5822a5879693dafb0e357333cf92f8271b/cve/published/2026/CVE-2026-64138.mbox | Linux CVE record links the SID-validation issue to its original upstream fix and stable backports. |
| Linux kernel ksmbd reconnect lifetime | `CVE-2026-64016` | https://kernel.googlesource.com/pub/scm/linux/security/vulns/+/532b7a5822a5879693dafb0e357333cf92f8271b/cve/published/2026/CVE-2026-64016.mbox | Linux CVE record links the reconnect lifetime issue to its original upstream fix and stable backports. |
| Shipwright | `shipwright-io/website#228` | https://github.com/shipwright-io/website/issues/228 | Maintainer acknowledgement of the original security report in the project's hardening-guidance issue. |

The [go-containerregistry v0.21.7 release notes](https://github.com/google/go-containerregistry/releases/tag/v0.21.7)
also list PR #2306.

## Other Public Acknowledgements

**Synology:** the [Security Bug Bounty Program acknowledgement list](https://www.synology.com/en-us/security/bounty_program/acknowledgement)
includes `JUNYI LIU (@mosskappa)`.
