# Dependency audit

Audit date: 2026-10-09. This records checks performed before adding the first build dependency.
No runtime Python dependencies are required for initialization; tests use Python's `unittest`.

## uv_build 0.8.0 — build only

Decision: use the exact pin `uv_build==0.8.0` as the PEP 517 build backend. It matches the installed
uv 0.8.0 tooling, supports the intended `src/` package layout, and requires no uv upgrade.

Checks:

- Publisher/project: Astral's uv project, confirmed against the official tagged source and PyPI
  metadata. Repository: <https://github.com/astral-sh/uv>.
- Official source: <https://github.com/astral-sh/uv/blob/0.8.0/crates/uv-build/pyproject.toml>.
- Package metadata: <https://pypi.org/pypi/uv_build/0.8.0/json>.
- The selected Linux x86-64 wheel was uploaded on 2025-07-17 and is not marked as yanked.
- Python dependency list: none, in both PyPI metadata and inspected wheel metadata.
- Downloaded the wheel without installing or executing it; inspected its file list, metadata,
  and Python build hooks. It contains a compiled `uv-build` executable and standard PEP 517 shims.
  Those shims invoke the build executable; building is code execution, not a passive file copy.
- Verified the downloaded wheel's SHA-256 against the PyPI artifact metadata:
  `438a6451440d631da28183807181d30e420d575f9a4a2fc0dd7441c85ca47884`.
- Queried OSV for PyPI `uv_build` version `0.8.0`; response `{}` listed no vulnerabilities.
  This is a point-in-time database check, not proof that the package is vulnerability-free.
- License: MIT OR Apache-2.0, confirmed in tagged source and wheel metadata.

Artifact checked:

```text
uv_build-0.8.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

Scope: this audit covers the selected build backend and artifact, not every platform's wheel.
No unrelated dependency installation or upgrade is authorized by this audit. Reaudit before
changing the pin or adding dependencies.

## Existing uv tool warning

The broader OSV check for the installed `uv` 0.8.0 tool returned advisories, including:

- [GHSA-4gg8-gxpx-9rph](https://github.com/advisories/GHSA-4gg8-gxpx-9rph): malicious entry-point
  names can write outside the scripts directory; fixed in uv 0.11.15.
- [GHSA-pjjw-68hj-v9mw](https://github.com/advisories/GHSA-pjjw-68hj-v9mw): malicious wheel RECORD
  entries can cause deletion outside the environment on uninstall; fixed in uv 0.11.6.
- [GHSA-8qf3-x8v5-2pj8](https://github.com/advisories/GHSA-8qf3-x8v5-2pj8),
  [GHSA-pqhf-p39g-3x64](https://github.com/advisories/GHSA-pqhf-p39g-3x64), and
  [GHSA-w476-p2h3-79g9](https://github.com/advisories/GHSA-w476-p2h3-79g9): archive parsing
  differentials, fixed across uv 0.8.6, 0.9.6, and 0.9.5 respectively.

These are reported against the uv installer/tool, not the `uv_build` package query above. Do not
interpret the backend's empty OSV response as a clean bill of health for the installed uv tool.
Recommend a separately audited upgrade to a current supported uv version. No global upgrade is
performed in this slice. Local package validation uses this repository's built wheel, with inspected
normal entry points and archive paths; it does not fetch an unknown tool from a package index.

## Documentation consulted

Context7's uv documentation confirmed PEP 517 configuration with `uv_build`, the default `src/`
layout, distribution builds with `uv build`, and running isolated commands with `uvx --from`.
The installed uv version is older than the current documentation; local builds and packaged-command
validation must confirm compatibility rather than relying on documentation alone.

## GitHub Actions — CI only

Audit date: 2026-10-09, before adding CI. Verified official GitHub-owned repositories, latest
release tags, their resolved commit SHAs, MIT licenses, action manifests, and runtime lockfiles.
Both actions use Node 24; use GitHub-hosted Ubuntu runners, not an older self-hosted runner.

Audited release commits (initially used as pins):

- `actions/checkout` v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`.
  Release: <https://github.com/actions/checkout/releases/tag/v7.0.1>.
- `actions/setup-python` v7.0.0: `5fda3b95a4ea91299a34e894583c3862153e4b97`.
  Release: <https://github.com/actions/setup-python/releases/tag/v7.0.0>.

Public repository advisory searches returned no entries, but OSV queries of runtime lockfile
versions found inherited npm advisories. This is not a clean vulnerability result:

- Checkout: 24 runtime entries checked; `undici` 6.27.0 has six advisories:
  `GHSA-3wwx-pv8p-q78v`, `GHSA-8xcm-r25x-g524`, `GHSA-m8rv-5g2x-5cg5`,
  `GHSA-r53p-7pc4-xj5r`, `GHSA-rfgv-xxqx-mfg5`, `GHSA-v3r7-h72x-cjcm`.
  They concern WebSocket denial of service, retry response handling, blob bodies, and cookie fields.
- Setup Python: 50 runtime entries checked; the same `undici` advisories, plus:
  - `brace-expansion` 1.1.15 and 5.0.6: `GHSA-3jxr-9vmj-r5cp`, `GHSA-6j4f-fj2g-mc7p`,
    `GHSA-mh99-v99m-4gvg`, `GHSA-q2hr-2g5m-vwhr`, `GHSA-qhr7-859c-m2p7`,
    `GHSA-rgw5-rvv9-x895` (malicious pattern denial of service).
  - `fast-xml-parser` 5.9.3: `GHSA-8r6m-32jq-jx6q` (entity expansion limits bypass).

Current decision: Scott requested movable major-version tags instead of commit pins. Rechecked
both official `v7` tags: checkout resolves to v7.0.1 and setup-python to v7.0.0, exactly the audited
commits above. No action code changed at verification; the inherited findings still apply.
Future tag moves receive compatible releases automatically and are outside this point-in-time
audit. `v8` or another major version still requires an explicit workflow change and review.

The workflow now runs on pushes and ordinary pull requests, not privileged PR-target events.
Its inputs are fixed Python versions, normal checkout, and the existing test command. Cache options,
custom XML, WebSockets, custom request bodies, and cookie manipulation are not configured. This
reduces exposure but does not prove those vulnerable paths unreachable within bundled action code.
The lockfile query is not a complete audit of bundled JavaScript or downloaded Python binaries.

The workflow grants only `contents: read`, disables persisted checkout credentials, accesses no
project secrets, and installs no Python packages. No publishing or repository-write job is added.
Reaudit before deliberately changing action versions or enabling caches, additional inputs, or
privileged triggers. Context7 confirmed major-version tags track compatible minor/patch releases;
this trades immutable code selection for automatic updates. Manifests at the audited SHAs confirmed
their inputs and Node runtime. No global tools or Python packages were installed or upgraded.
