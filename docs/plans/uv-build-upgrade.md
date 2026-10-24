# uv and build-backend security upgrade

Scott requested this upgrade after the Factory wheel checksum failure and a recent uv advisory.
The scope is project/CI uv, its separately pinned build backend, installer version checks and
packaging regression coverage. It does not authorize runtime repair, agent changes or a commit.

## Selected versions and security finding

- Build backend: `uv_build==0.13.5`, replacing `0.8.0`.
- CI uv: `0.13.5`, replacing `0.13.1`.
- Project and consent-gated installer minimum: `uv >=0.13.5`.
- The existing local uv already reports 0.13.5 and matches the audited binary; it is not replaced.
- `uv.lock` is unchanged: uv and the build backend are outside its runtime/dev graph.

The latest upstream [emSign advisory][emsign] affects uv before 0.13.4 and currently has no assigned
CVE. Compromised intermediate certificates can undermine HTTPS authentication. 0.13.4 removes the
root; [0.13.5][release] also rejects compromised intermediate keys. The separately published
build backend fixes the wheel RECORD format: its pinned source writes URL-safe Base64 rather than
0.8.0's hex output. These are separate fixes, not evidence that upgrading uv alone repairs an old
backend pin. Other Python/pip or system/custom certificate stores are not changed by this upgrade.

## Pre-install audit

Evidence: `/tmp/factory-build-upgrade-jv0gyqd3/audit`.

Official version-specific PyPI metadata identifies Astral's repository and MIT/Apache-2.0 licenses.
Both Linux x86-64 wheels were downloaded without execution and checked before installation:

```text
uv 0.13.5
fa8d26e08e34c29c0c4e820cf3181757086d547240b4f4d31ff1d8bd810ca946
uv_build 0.13.5
57399f778f42185ee92ec0648566ee5d7fa6e5a1ce393a5f28945f64430c140d
```

Archive membership, paths, types, sizes and every RECORD digest were verified. There are no `.pth`
startup files or Python runtime dependencies. Python wrappers only locate/dispatch their native
executables; they were inspected without running them. The installed uv binary matches the reviewed
wheel's executable. The standalone backend is installed only from that audited local wheel into a
scratch environment, offline, without dependencies. No global or project-venv tool upgrade occurs.

Root-package OSV queries find the emSign advisory on uv 0.13.1 and no reported advisory on the
selected root packages. The embedded SBOM scan is broader: 566 distinct Cargo package/version
queries return 14 advisories across 11 components. An independent source review assessed those
findings before the pins or installed backend changed. Its report is
`audit/advisory-review/AUDIT.md`; recommendation: proceed within the reviewed scope, with limits.

### Residual risks retained

- HTTP/2 client memory exhaustion remains relevant to downloads. Hash locks do not protect HTTP
  framing, and timeouts do not prove the affected queue is bounded.
- A conditional rustls key-share prediction issue can reduce a later connection's post-quantum
  protection, not certificate authentication. Server policy and session lifetime bound the impact.
- Backend hashing uses ordinary SHA-256, not the affected ctutils comparison/masking API. No direct
  AsyncFd call was found in pinned uv source. Indirect API reachability is not fully proven absent.
- Other findings include build-time/unmaintained components, bounded mapping/channel paths, and
  credential/TLS feature conditions not reached by the reviewed public-download/local build paths.
  This is not clearance for private-cloud signing, custom TLS settings or all native credentials.

All 11 component versions are unchanged between uv 0.13.1 and 0.13.5. Remaining on 0.13.1 would
retain them plus the compromised-CA problem. That comparison does not clear the old backend or
prove identical compiled features. Only the selected Linux wheels were audited; CI still pins the
release version rather than an artifact hash. Future added artifacts and other platforms are not
covered. No exploit testing, attestation verification, full transitive call proof or reproducible
source-to-binary audit was performed. Recheck these findings on the next upstream update.

## Regression boundary and implementation

`tests/check_package.py` checks built wheels without importing or extracting them. It verifies
unique archive/RECORD entries, membership, unpadded URL-safe SHA-256 digests and byte sizes.
CI runs it immediately after `uv build` on both Python versions. This is an explicit artifact check,
not a dependency install added to ordinary unittest discovery.

The old wheel fails at its first hex digest. A known-good release wheel passes; scratch controls
with hex hashes, changed contents, missing rows and duplicate rows all fail. This closes the earlier
gap: source-byte comparisons and successful CLI help did not check the RECORD encoding.

Installer coverage uses public init with controlled external commands. Affirmative consent still
cannot permit an older uv: 0.13.1, 0.13.3 and 0.13.4 must stop before any install or consent prompt.
0.13.4 includes the upstream CA fix, but is below this project's selected audited baseline. The new
test first failed because the old guard actually invoked the fake installer, not just because its
message differed. The updated installer module passes all ten checks. No automatic uv update,
consent bypass, receipt reset or runtime repair is introduced.

## Validation checkpoint

- [x] Independent pre-install audit accepted with the residual risks above.
- [x] Old wheel and old uv guard fail the intended regression checks.
- [x] Audited standalone backend installed offline into a disposable environment.
- [x] Built-in uv and standalone PEP 517 backend both produce 71 valid wheel digests.
- [x] All wheel file bytes match between those two build paths.
- [x] Offline `uv lock --check` passes; lock bytes and dependency versions are unchanged.
- [x] Ten installer tests, Ruff and all three import contracts pass.
- [x] Wheel/sdist contents match all 68 source/resource files and 41 test files.
- [x] Five extracted-wheel and five generated installed-CLI help commands pass, without inference.
- [x] Full native-enabled suites: 373 passes each on Python 3.12.3 and 3.13.5; no skips.
- [x] Final independent upgrade review accepted; 20 installer checks and 13 artifact controls pass.

The full suites took 510.583 seconds on 3.12.3 and 505.234 seconds on 3.13.5. Source/test hashes
remained stable throughout both runs. The existing 3.13 validation environment reuses SDK 0.5.0;
its external static linter still uses the existing 3.12 interpreter. No runtime/dev package changed.
The own-wheel installation was offline, without dependency resolution; existing SDK files were
reused through a path file. This validates the generated CLI, not fresh host/dependency setup.

The independent reviewer verified all 139 frozen files and all 109 source/test files unchanged,
with the narrow 16-file upgrade delta preserved. One valid wheel and 12 malformed artifact controls
exercised the permanent checksum checker. There was no blocking or actionable regression. The
review report is `final-review/REVIEW.md` under the evidence root. Later parent changes only record
completed validation in documentation; final artifacts are rebuilt and rechecked against those docs.

The regenerated map has 56 boxes, 1,843 filtered calls and 42 filtered type relationships. Repeat
exports match. External-base warnings remain; Mermaid was checked as text, not rendered.

The newer backend includes both a normalized `pyproject.toml` and the original
`pyproject.toml.orig` in the source distribution. Validation must compare normalized TOML semantics
and the original bytes, rather than reject this documented format change as a missing/extra file.

Native CLI/backend smoke has separate Pi/Forgetful/cache prerequisites. Its uv requirement
now follows 0.13.5; it has not been run as part of this upgrade. Factory hosted CI, live model
compliance and the unanswered runtime-repair policy are not established by these local checks.

[emsign]: https://github.com/astral-sh/uv/security/advisories/GHSA-hq85-5cpj-mr62
[release]: https://github.com/astral-sh/uv/releases/tag/0.13.5
