# Project dependency management with uv

Status: dependency management is implemented. Current tool versions and local upgrade evidence are
in the [security-upgrade record](../plans/uv-build-upgrade.md). Earlier hosted migration evidence is
in the [quality-checks plan](../plans/quality-checks.md); it does not validate this update.

Back to [architecture](../architecture.md).

## Decision

Declare runtime dependencies in `[project.dependencies]` and local development tools in
`[dependency-groups].dev` in `pyproject.toml`. Commit uv's generated `uv.lock` for exact versions,
artifact hashes for the runtime/dev graph, and platform-specific dependencies. Do not maintain
a second constraints file. The lock does not cover the uv executable or the build backend;
`uv_build==0.13.5` is separately pinned in `[build-system]`. The original build, runtime,
and Actions checks remain available in the [historical audit][original-audit].

Use `uv sync --locked` and `uv run --locked` locally and in CI. The lock must agree with the
manifest; CI must not silently update it. Development groups are not published package extras
or runtime dependencies. A normal wheel/uvx install must still install only runtime dependencies.

Keep the existing Python 3.12/3.13 CI matrix and check commands. CI installs a pinned uv release
using its existing Python setup, without adding another GitHub Action. Dependency updates still
require review and a pre-install audit; a lockfile is not a security audit.
`[tool.uv].required-version = ">=0.13.5"` rejects outdated uv before project operations; the
consent-gated installer enforces that minimum. CI pins uv 0.13.5, builds wheel/sdist artifacts and
checks wheel RECORD digests with `tests/check_package.py`. Editable installation or a successful
build command alone does not establish correct artifact checksums.

## Current tool audit

The 0.13.5 upgrade addresses the upstream emSign certificate advisory and replaces the old backend's
invalid wheel checksum encoding. Both official Linux wheels passed pre-install artifact review;
the native backend and uv executable remain separate artifacts. The independent audit also records
14 Rust dependency advisories and bounded reachability assessments, including retained HTTP/2
client DoS and conditional TLS key-share risks. The candidate is not vulnerability-free.
See the [upgrade record](../plans/uv-build-upgrade.md) for hashes, scope and validation.

## Historical migration audit

Checked 2026-10-14, using official PyPI release metadata for `uv==0.13.1` and the OSV API.
The package identifies Astral's [uv repository](https://github.com/astral-sh/uv), is licensed
MIT OR Apache-2.0, and declares no Python runtime dependencies. This is a development/CI tool,
not a factory dependency. Context7's uv documentation confirms dependency groups and locked sync.

The selected Linux x86-64 wheel was downloaded without executing it. Its SHA-256 matches PyPI:

```text
uv-0.13.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
696dcf6d807d85da978f4db8472da81dccc1254b18b52cbd1367c4d923c421e0
```

This hash identifies the exact wheel used for local validation. CI pins the version, not this
artifact hash; pip selects a compatible PyPI wheel. Added release artifacts are not covered by
that point-in-time artifact inspection. This is not an immutable CI bootstrap guarantee.

Inspected wheel paths and metadata: no absolute/traversal member paths, expected `uv`/`uvx`
executables, and no Python dependency installers declared in metadata. OSV returned no known
advisories for 0.13.1. This does not prove the native executable or upstream infrastructure safe;
there was no full source-to-binary audit. uv accesses package indexes and installs/builds packages,
so it runs with ordinary user/CI filesystem and network privileges.

The then-installed uv 0.8.0 had archive-extraction, entry-point and RECORD-handling advisories.
That migration used 0.13.1 in CI/isolated checks, leaving the global installation unchanged.
The first lock contains exactly the existing ten runtime/checker packages plus the project;
no platform-only packages or version upgrades were introduced. Audit any new packages introduced
by future lock updates before installation.

## Validation

The first lock preserves all existing checker/runtime versions, with no additional packages.
Locked environments pass lint, architecture checks, and all tests on Python 3.12/3.13.
Normal wheel installs and `uv sync --locked --no-dev` exclude the dev tools. A deliberately
changed manifest is rejected by locked sync. See the
[quality-checks plan](../plans/quality-checks.md#uv-dependency-management-migration) for evidence.

[original-audit]: https://github.com/ScottRBK/factory/blob/31df9bd/docs/dependency-audit.md
