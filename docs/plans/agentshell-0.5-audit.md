# AgentShell 0.5.0 dependency audit

Scope: upgrade the Factory's direct `agent-shell-py` dependency from 0.4.0 to 0.5.0.
The bundled Pi AgentShell extension has a separate 0.4.0 Python worker; it is not upgraded here.
Audit performed before changing the manifest, lockfile or installed Factory dependency.

## Evidence and decision

- Official [PyPI metadata][pypi] identifies `agent-shell-py` 0.5.0, Python >=3.12, no runtime
  dependencies, and an MIT license. The wheel is pure Python with no entry-point installation
  scripts, `.pth` startup files, or `sitecustomize.py`/`usercustomize.py` hooks.
- The [release tag][release] resolves to commit `b1e0587dcfd6065a1fe1d3057626e7a912547847`.
  Downloaded wheel and sdist hashes match PyPI and the GitHub release artifacts. Package source
  matches the tagged source, apart from the expected generated version file. Wheel RECORD entries
  were checked. Use the wheel rather than executing the sdist's Hatchling/Hatch-VCS build hooks.
- PyPI publish attestations identify the upstream commit and GitHub workflow. Statement
  signatures, certificate chains and signed Rekor timestamps were checked. Full Sigstore policy
  verification was not performed; the Git tag and commit are unsigned.
- OSV returned no direct-package advisories for 0.4.0 or 0.5.0 at review time. This is a dated
  advisory lookup, not proof that the software is vulnerability-free.
- Review covered changed resource, process, interactive and tmux paths. Argument-preparation
  fixtures confirmed that explicit local skills/extensions with discovery excluded do not invoke
  a package installer, keep the native agent-directory environment, and explicitly disable MCP.
  These fixtures did not launch Pi, authenticate, or contact model providers.

The pinned wheel is approved for the Factory development/runtime environment, subject to the
local-resource constraints below. No transitive runtime dependencies are introduced. This approval
is not approval for remote resource-package installation or a global Pi/uv upgrade.

## Artifact SHA-256

```text
agent_shell_py-0.5.0-py3-none-any.whl
57b0b8b8aa87ab165f1bcf301c2da447e3bae97afd9a69ed074a75ffcff59f43

agent_shell_py-0.5.0.tar.gz
987cdc093587c80c2304efd6735485c79538de190664a54caa25b29fa1bb717e
```

## Use constraints

- Supply already-provisioned local skill/extension paths. Leave session `packages` empty.
  Remote selections can automatically run `pi install` before launch, even when launch itself
  uses offline resource exclusion. This path is not the Factory's reviewed installer.
- An explicit Git ref may be a moving branch; it is not necessarily an immutable pin.
- Keep installation consent and the existing bundled-resource integrity checks. Resource selection
  stores path identity, not a content snapshot, and executes selected extension code.
- Native model authentication remains in the chosen shared Pi home. This also retains native
  configuration and state; it is not selected-provider credential isolation or a host sandbox.
- Keep the bundled extension's own reviewed 0.4.0 lock unchanged for this discussion-only Foreman.
  Upgrading the outer launcher does not add role selection to that extension's child-agent worker.
  Revisit the worker with its own audit and tests when feature-owner dispatch is implemented.

The older `slice-3-supply-chain.md` path referenced by existing documents is absent in this working
copy. This audit does not reconstruct or replace the earlier Pi/Forgetful installer audits.

[pypi]: https://pypi.org/pypi/agent-shell-py/0.5.0/json
[release]: https://github.com/ScottRBK/agent-shell/releases/tag/v0.5.0
