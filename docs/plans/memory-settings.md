# Memory settings in forgetful.json

Work record for [issue #5][issue]. The [memory ADR](../adrs/foreman-memory.md#memory-settings)
records the design.

## Scope and decisions

Scott's aim: Factory must not hardcode forgetful rules. `forgetful.json` holds the extension's
settings, and the extension's code resolves them.

- D1. No upstream change. The bundled extension already exports `loadForgetfulConfig()`, which
  takes a settings file path. The managed entry calls it with `forgetful.json` as the only
  settings layer (user and project file), so no "untrusted project" warning appears.
- D2. All extension settings follow the extension's rules, including `enabled`, `capture_mode`
  and `model`. Logging is allowed and stays `off` by default.
- D3. Pi compaction settings are out of scope. They belong to the shared Pi profile.
- D4. Nothing rewrites `forgetful.json`. `update` and repeated `init` keep it byte-for-byte.
- D5. `init` keeps its input checks and starter file.
- D6. `init` leaves out `model` when no model is chosen. The extension itself never writes
  `null`, and `null` warns at each start.
- D7. A non-boolean `enabled` counts as `true` without a warning. That is the extension's rule;
  it goes to [upstream issue 6][enabled-issue].
- D8. In managed mode, the no-model warning and the blocked-command message point to the
  selected Foreman `forgetful.json`.
- D9. Native tests stay local; [issue #6][ci-issue] covers running them in CI.

Factory refuses keys it sets (`base_url`, `token`, `token_env`, `log_directory`,
`planning_panel`) and unknown keys, including `scope`. Strict type-checking fails at a bundle
refresh when the extension adds or removes a setting, until Factory's key list matches.

## Vertical slices

1. `init` with no model writes `{"enabled": false, "capture_mode": "off"}`. Red first in
   `tests/test_foreman_memory_setup.py`; the change is in `coordinator_profiles.py`.
2. Characterisation: repeated `init` and `update` keep a user-edited `forgetful.json` with extra
   settings byte-for-byte (`test_foreman_memory_setup.py`, `test_resource_update.py`).
3. Native red/green in `tests/test_native_roles.py`, `NativeManagedMemorySettingsTests`, through
   the real bundle, native Pi and a fixture Forgetful server:
   - the memory-off starter file loads with no warning;
   - a larger and an invalid `context_limit_tokens`, recall-only, `observe`, an invalid
     `capture_mode`, memory on without a model, `{}` and the ready state follow the extension;
   - each Factory-owned key, an unknown key, `scope` and a non-object file make memory
     unavailable with no request to the server;
   - `logging: "debug"` writes owner-only logs only below `.factory/data/pi-forgetful/logs`;
   - a blocked command names the Foreman settings files.
   All cases failed on the earlier bundle except the non-object file, which stays as a guard.

## Validation

- Factory patch: base `574a4e8` unchanged. The old patch hash reproduced before the change.
  Changed files: `src/bootstrap/factory.ts` and `src/extension.ts`.
- Strict `tsc --noEmit`, including the root `factory.ts`, passes. Removing a key from the list
  fails with the missing key's name; adding a key the extension lacks also fails.
- Upstream checks on the patched tree: architecture tests 23 pass; 1359 tests give 990 pass,
  0 fail, 369 skipped, the same as the earlier bundle. The architecture script reports the same
  2 errors on the earlier and new trees: the `node_modules` link and the root `factory.ts`.
- Factory suite with native tests (Pi SDK 1.6.0, Node 24.22.1): 658 passed, 3 skipped. Without
  native tests, as in CI: 647 passed, 14 skipped. Ruff and the 3 import contracts pass.
- The Mycelium map does not change: no production class, method or call changed.
- Read-only `update --dry-run`, 0 edited and 0 to add in both: DinoLand plans 9 replacements,
  dark-business 3. Both current `forgetful.json` files are valid under the new rules.

## Not verified

- Recall-only and `observe` with a real model call.
- The pinned Pi 1.4.0 runtime. The native tests used the installed Pi 1.6.0 SDK.
- Native tests do not run in CI ([issue #6][ci-issue]).

[issue]: https://github.com/ScottRBK/factory/issues/5
[ci-issue]: https://github.com/ScottRBK/factory/issues/6
[enabled-issue]: https://github.com/ScottRBK/pi-forgetful-extension/issues/6
