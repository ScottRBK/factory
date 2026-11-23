# Bundled role resources

The adjacent archive contains source files, never an installer or built executable. First setup
verifies each file against `role-resources.json`, copies missing files, and preserves edited files.
Ordinary repeated init preserves the existing setup without repair or synchronization. The manifest
records full upstream commits and SHA-256 hashes. No moving URL runs at initialization.

`role-resources-history.json` lists every SHA-256 that Factory has shipped for each bundle path,
including the current bundle. `forgetful-factory update` uses it to replace unedited files from
earlier releases. When adopting a new bundle, append each new hash and remove none; update
refuses to run when a current hash is missing. See the
[update ADR](../../../docs/adrs/role-resource-update.md).

Reviewed sources:

- ScottRBK/pi-agentshell-extension, commit `5acb6aabfaae7c4d889600f6a5fffbb1c412dc6b`
  (package 1.5.0). MIT license included. Imports Node built-ins and Pi-provided peer modules.
  Its Python worker has an independent agent-shell-py 0.5.0 lock. With explicit consent,
  setup runs upstream `uv sync` against the bundled lock, with source builds, dev dependencies,
  config discovery, and Python
  downloads disabled. Verified metadata is staged in an independent temporary uv workspace to
  exclude ancestor workspace overrides. A successful input-matching receipt and import check are
  required for readiness. It creates the extension's real `.venv`; no interpreter override is used.
- ScottRBK/pi-hide-tools-extension, commit `a811fd2a2fcdb2ab94bf11b4ce4d6c0c9e210029`
  (package 0.1.0). Imports Node built-ins and Pi-provided modules. No installer or network calls.
  No upstream license file was present. Source remains attributed to Scott's repository.
- ScottRBK/pi-forgetful-extension, base `574a4e8bfb2de368445036fb8e3ce89b08c58065`, with
  local patch `4635923292215233dea361244b262079ad4bdaf6feee97a6ce3be67ace90fe49`. The patch
  hash is the SHA-256 of `git diff --cached --full-index --binary` in a checkout of the base after
  copying in the 40 bundled files and running `git add -A`. See the refreshes below.
  The original 40-file runtime closure was independently approved for inert internal inclusion.
  The runtime-alignment follow-up removes only the Factory-specific host gate from that closure.
  Its new patch hash covers the complete local diff against the same upstream revision. Its managed
  entrypoint is `pi-forgetful/factory.ts`; `index.ts` retains standalone behavior. New starter
  Foreman definitions select the managed entry, while child and edited legacy selections remain
  unchanged. Internal testing describes the audit scope, not a redistribution restriction.
  Retain applicable copyright and license notices when distributing bundled code.
  The unused post-close permission change was removed. Scott accepted the remaining concurrent
  workspace-path replacement limitation rather than adding containment work. Existing checks
  remain; source approval does not claim sandboxing, live enablement or backend/model access.
  Original exact-source approval: `implementation/source-audit/v7/approval.json` under
  `/tmp/factory-foreman-forgetful-2ptedi1m/`. All 15 prior bundle members are byte-identical.

The 1.5.0 published archive passed independent signature/provenance and source-byte verification.
Its exact 11 runtime files were adopted after source and artifact review. All four hide-tools files
and the SDK project/lock remain unchanged. Normalized definitions and Codex/Claude prompt skill
references pass real Pi 1.4.0 SDK/fake-native probes without inference. These probes do not install
the worker or establish model compliance. Audit evidence is under
`/tmp/factory-normalized-approved-O7PbkX/extension/bundle-audit`.

Review covered import/dependency manifests, process launch paths, upstream setup consent,
configuration writes, worker protocol and tool rendering. AgentShell runs a fixed local Python
worker with argument arrays; that worker delegates agent execution to the AgentShell library.
Hide-tools writes only its preference file under the selected Pi directory. Both extensions run
with the host user's privileges. This review is not a guarantee of security or Pi compatibility.

The hide-tools package declares Pi 0.99.1/0.99.2 peers. The factory does not use npm to resolve
or replace those peers; native compatibility checks use the reviewed runtime below.
The adjacent `install-locks.zip` pins Pi 1.4.0 with its normal Undici 8.10.2 dependency, without an
override. Its SHA-256 is `eba2b047dfed011a219b5d4f53133cf51d687ce40dd25416dfe91ce9556727f6`.
Scott rejected the earlier Factory-only dependency policy. The follow-up changes one package entry;
all other npm entries and Python requirements remain unchanged. Before adoption, the Undici archive
was checked against npm's SHA-512 integrity and registry signature. It has no installation hooks or
runtime dependencies. Fresh OSV checks still report eight advisories; alignment is not a security
clearance or an exposure assessment. No package was installed during this change.
The experimental Milo parser remains disabled. Evidence and exact diffs are under
`/tmp/factory-pi-alignment-YYrJLb/`; see the
[runtime-alignment record](../../../docs/plans/foreman-memory.md#runtime-alignment).

The earlier independent audit of the overridden lock verified 119 archives and 15,012 installed
files. Its clean advisory result does not apply to this restored upstream dependency. Historical
evidence: `implementation/AUDIT.md` under `/tmp/factory-foreman-forgetful-2ptedi1m/`.
Installer audit and memory-source approval remain separate from licensing and release readiness.
Pi installs with `npm ci --ignore-scripts` into `.factory/runtime/pi`. The hash-bearing Python
requirements are unchanged; Forgetful 0.5.5 uses wheel-only, hash-checked `uv pip sync` in its own
`.factory/runtime/forgetful` environment. The reviewed Python resolution targets Python 3.12.
The factory asks before either installation. Existing executables are never upgraded.

Ubuntu 24.04 amd64 has a consent-gated `apt-get` recipe for tmux 3.4-1ubuntu0.1. A simulation must
report zero upgrades and removals before proceeding. APT uses configured distro repositories;
privileged package installation and OS dependencies remain an explicit trust boundary. There is
no APT index update. Other platforms and custom executable names require manual installation.

The factory defaults Pi's fallback binary downloads and Forgetful model downloads to offline/cache
mode. Local checks need an already provisioned model cache. Review and prepare models separately.
## Adopting a new bundle

1. Fetch the exact upstream commit; never a moving branch name.
2. For `pi-forgetful`, rebuild the Factory patch as the diff between the bundled files and the
   recorded base. Apply it with `git apply --3way`. Resolve conflicts by keeping upstream's code
   and re-applying Factory behavior: the managed `factory.ts` entry, fixed project, no host gate.
3. Recompute the runtime import closure from the entry points. Removal of a dropped file is not
   implemented yet; add it, with a CLI test, before adopting a bundle that drops one.
4. Review the runtime diff: imports, process launches, network, file writes, environment reads,
   logging and dependency manifests. Type-check and run upstream tests on the patched tree.
5. Rebuild the zip (sorted names, deflate, 2026-01-01 timestamps, mode 0600). Update the manifest
   revision, patch hash and file hashes. Append every new hash to the history file.
6. Run the full suite and `update --dry-run` against real factories. Record the evidence here.

## 2026-11-23 pi-forgetful refresh

Moved from base `45a0b79` to `574a4e8` (one upstream commit). In the 40-file runtime closure,
only `src/model-context.ts` changed, and its imports did not. `agentshell` and `hide-tools`
bytes, `package.json` and the npm lock are unchanged.

- `574a4e8`: history summaries keep Pi's full summary reply (80% of `reserveTokens`, capped by
  `maxTokens`). Before, a batch that filled most of the private window got a reply cut to the
  space left. The provider then stopped at "length", so the capture job failed and blocked later
  jobs on its branch. Now such a batch splits between whole records; one record that cannot fit
  fails with the existing "cannot fit" error. Task replies keep their cap. The change is local
  token budgeting only: no new imports, processes, network, file writes or environment reads.

The old patch hash reproduced from the bundled files against `45a0b79`. The Factory patch does
not touch `model-context.ts`, and no patched file changed upstream, so the patch applied without
conflicts and its hash is unchanged.

Validation: strict `tsc --noEmit`, including `factory.ts`, passes. Upstream's 1359 tests give
the same result on the patched and plain trees: 990 pass, 0 fail, 369 skipped. That includes the
three new tests: the near-window split, the single-record failure and the real Pi SDK queue
drain. Dev dependencies came from Scott's clean upstream checkout at `574a4e8`, whose package
files match; nothing was installed. Factory's full parallel suite: 646 passed, 9 skipped; ruff
and import contracts pass. Read-only `update --dry-run` from the built wheel, 0 edited
and 0 to add in both: dark-business, already on `45a0b79`, plans 1 replacement; DinoLand plans 8.

## 2026-11-22 pi-forgetful refresh

Moved from base `e670a88` to `45a0b79` (five upstream commits). The runtime closure stays at the
same 40 files; 8 changed: `model-context.ts`, `logging.ts`, `model.ts`, `capture.ts`,
`config.ts`, `extension.ts` and both `planning.ts` files. `agentshell` and `hide-tools` bytes,
external imports and `package.json` are unchanged.

- `b4630a8`: private memory tasks always compact when needed. Pi's `compaction.enabled` now
  controls only the main session. Before, a profile with it off failed every long-session capture.
- `4cdf632`: debug logging keeps complete events as numbered trace chunks, plus event and task
  IDs. Rows still pass credential exclusion and sanitizing. The log folder is now created 0700 and
  files 0600. Logging stays `off` unless a user selects `debug`; Factory does not change it.
- `d2a04ea`: the default recall model timeout rises from 5 to 15 seconds.
- `45a0b79`: SonarQube refactor of status and planning code; no new capabilities, imports or
  process, network or file access.
- `a0587f7`: tests only.

The old patch hash method was not recorded and its evidence folder no longer exists, so the patch
was rebuilt from the bundled files against `e670a88`: 10 modified and 3 Factory-only files. Two
conflicts were resolved by hand. In `extension.ts`, upstream's new `refreshStatusProject` keeps
Factory's managed-mode skip and `config` argument, and status keeps Factory's managed and fixed
project text. In `application/planning.ts`, upstream's new `readProject` keeps the fixed project.

Validation: strict `tsc --noEmit`, including `factory.ts`, passes. Upstream's 1356 tests give
the same result on the patched and plain trees: 987 pass, 0 fail, 369 skipped. That includes the
new Pi SDK test with auto-compaction off. Factory's native probes pass with the Pi 1.3.0 SDK. The
Pi 1.4.0 pin was not probed. Read-only `update --dry-run` on DinoLand and dark-business plans 8
replacements, 0 additions and 0 edited files each. Evidence was in this session's scratch folder.

## Historical audits

The 2026-10-17 independent extension audit verified release 1.4.0 and worker 0.5.0.
That upgrade changed seven agentshell archive members; hide-tools was unchanged.
Evidence: `/tmp/astra-factory-1.4-audit/report.md` (local audit handoff).

The 1.4.1 follow-up inspected the local official release tag and its delta from 1.4.0. Five
members changed: `package.json`, `config.ts`, `index.ts`, `limits.ts` and `runner.ts`. They rename
configuration keys and their uses to snake_case. Dependency declarations, package scripts and
the Python worker/lock are unchanged. Each bundled member matches the immutable source commit
and the manifest's SHA-256. Evidence: `/tmp/factory-extension-141/audit.json`.
Registry DNS was unavailable, so published npm artifact integrity/provenance and fresh advisory
checks were not repeated. That 1.4.1 bundle used inspected Git source, not an unverified download.

The narrow Forgetful 0.5.5 audit verified source commit
`8964f8e626bc4945d2ca3cc2bd38a69ff44082e6` and 114 wheels for CPython 3.12,
Linux x86-64, glibc 2.39. The other 113 transitive versions and npm locks are unchanged.
Forgetful wheel SHA-256:
`a9c4089a8fb6efb8fdadd64136c1ae7fd797fbf2522614d0296a72e924789602`.
Source archive SHA-256 (not installed under the wheel-only policy):
`435a46380f5440164a1e46b210cb3a763824e755967f83c8984b539742bc530a`.
Evidence: `/tmp/forgetful-055-audit/AUDIT.md` (local audit handoff).
Neither audit proves a fresh host installation, live authentication, or autonomous planning.
Existing executables and edited installed resources require explicit reconciliation.
