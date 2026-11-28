# Role-resource update

`forgetful-factory update` brings an existing factory's bundled role resources up to the bundle
in the installed Factory package. It answers [issue #4][issue]. The
[work record](../plans/role-resource-update.md) has the validation evidence.
Back to [architecture](../architecture.md).

## Context

First setup copies the audited `agentshell`, `hide-tools` and `pi-forgetful` files from
`role-resources.zip` to `.factory/resources/`. Foreman and watch then refuse any file whose
SHA-256 differs from `role-resources.json`. Before this command, a newer Factory bundle could not
reach an existing factory: old unedited files failed the new hashes, ordinary `init` does not
synchronize, and first-setup provisioning refuses to overwrite. A fresh factory loses the user's
customized `.factory/agents/` definitions and skills.

## Decision

The command plans every change before it writes anything. Each bundled path has one state:

| State | Condition | Action |
| --- | --- | --- |
| current | Hash matches the installed bundle. | None. |
| replace | Hash matches a version that Factory shipped earlier for that path. | Replace. |
| add | File is missing from the workspace. | Add. |
| edited | Hash matches no shipped version. | Refuse the update, or back up with `--force`. |

A symlink in the path, or a path that is not a regular file, stops the update before writing.

### Shipped history

`resources/role-resources-history.json` lists every SHA-256 that Factory has shipped for each
bundle path, including the current bundle. It was built from the four committed manifests
(`97f34b1`, `1e294fa`, `688c926`, `62231f7`). The list is append-only. When a new bundle is
adopted, add each new hash and remove nothing. The command refuses to run when the history lacks
a hash from the current manifest, so an incomplete adoption fails every update test.

The issue offered a second option: record the installed manifest in each workspace. Factories
created before this change have no such record, so the shipped history is needed anyway. A
workspace record would add no capability, so it was not added.

### Edited files and `--force`

Scott chose an explicit `--force` with a backup. Without it, an edited file stops the whole update
and the command names each edited file. Nothing changes. With `--force`, each edited file is
copied to `.factory/resource-backups/<UTC time>-<random>/<bundle path>`, then replaced.

### Write order

1. Stage each new file as a temporary file in its target directory.
2. With `--force`, copy each edited file to the new backup folder.
3. Rename each staged file into place, then validate every bundled file against the manifest.

A failure before step 3 changes no bundled file; temporary files are removed. An interruption
during step 3 leaves each file at a shipped version or at the new version, so a rerun completes
the update. This is not an atomic transaction across files.

### Stopped factory

A real update holds the workspace lease and refuses when the Foreman owner state is anything other
than `stopped`. The lease blocks plain watch, init and a `foreman` start. Managed watch runs
inside the Foreman owner, so the owner check covers it.

Python cannot prove that detached delegated work stopped (AgentShell issue #28). The first version
required `--delegated-work-stopped` as the user's confirmation, but the flag checked nothing.
Scott removed it on 2026-11-23: stopping delegated workers is the user's step, stated in the
[configuration guide](../configuration.md#update-role-resources). `init --finalize` keeps its own
flag.

`--dry-run` prints each planned change and writes nothing. It takes no lease, so it also works
while the factory runs. It exits 1 when edited files would stop
the update without `--force`.

### Scope

- The command writes only bundle paths under `.factory/resources/` and a new backup folder.
  It never writes `.factory/agents/`, `.factory/data/`, `factory.toml` or the setup receipt.
- It updates `pi-forgetful` even when Foreman does not select the managed extension, because
  first setup provisions every bundled file.
- `ROLE-SOURCES.md` is a package record that is never copied into a workspace. Bundle adoption
  updates it at build time; the command does not.
- Pi and Forgetful runtimes (`install-locks.zip`) and agent guidance templates are out of scope.
- Running agents keep their loaded files. Start Foreman or watch after the update.

### AgentShell runtime

After the files pass validation, the command checks the AgentShell worker runtime: its sync
receipt must match `pyproject.toml` and `uv.lock`, and its import probe must pass. A changed lock
makes the runtime not ready. `update` then runs the existing locked installer, the same one that
`init --install-role-runtime` uses. Scott chose this default on 2026-11-23: an update is expected
to update, and the lock was reviewed when the bundle was adopted. `init` keeps asking for consent
because it is the first install. `--no-install-role-runtime` skips the install; the command then
exits 1 and the updated files stay in place, so a plain rerun completes the work.

## Deferred

Removing files that a bundle drops is deferred. No bundle has dropped a file, so the real bundle
cannot test removal. Scott chose to add removal, with a CLI test, when a bundle first drops a file.
Until then a dropped file stays in place; validation ignores it.

## Testing boundary

Scott chose public CLI tests with the real installed bundle and no adapter-level seam.
`tests/fixtures/previous-pi-forgetful-factory.ts` holds the exact previous-release bytes of the
only file that changed in `62231f7` (SHA-256 `8187b43b…`, shipped in `688c926`).

[issue]: https://github.com/ScottRBK/factory/issues/4
