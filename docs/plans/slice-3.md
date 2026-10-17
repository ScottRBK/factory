# Slice 3: Foreman setup and Forgetful access

Back to the [implementation plan](../plan.md).
Architecture: [agent profiles](../adrs/agent-profiles.md).

Status: closed on 2026-10-16 at Scott's request after the DinoLand onboarding trial.
Closure includes the [CLI onboarding follow-up](cli-onboarding.md), its trial-feedback fixes,
153-test validation on Python 3.12/3.13, packaging/smoke checks, passing SonarQube and Opus recheck.
The Foreman remains discussion-only. Remote authentication and clean host installations remain
unverified by the recorded automated validation; user acceptance does not expand that evidence.

The sections below preserve the original scope and implementation history, including superseded
choices. Current setup is CLI-only, with consented shared Pi login and explicit role resources,
not the separate Pi profile/MCP default below. The follow-up and [main plan](../plan.md) govern
current behavior, remaining limitations and the proposed next slices.

## Agreed scope

- Configure the Foreman's Pi profile, tools, extensions, and skill.
- Extend `forgetful-factory init` to configure the agents' Forgetful connection.
- The Foreman reads incoming issues and discusses them with the user. It must explain that
  automated implementation is not available yet. Do not add automatic plans, worktrees, or an
  alternative implementation workflow in this slice.
- In watcher output, report Foreman readiness/awaiting input after AgentShell session readiness.
  State that Forgetful was not checked at watcher startup; native Pi `/mcp` owns live MCP display.
  Do not add a factory Pi status extension or an automatic watch-time connection/auth probe.
- Keep issue-update notifications and durable restart tracking for a separate slice. Preserve
  the current watcher notification behaviour.
- Leave the separate Forgetful background-memory extension out of this slice.
- Do not build migration support for existing factories; only Scott's testing setups exist.

Feature-owner profile implementation, dispatch, watcher plan scaffolding, initial worktrees, and
existing Pi session attachment remain later work. The Foreman skill must distinguish current
behaviour from the future dispatch, recovery, and completion responsibilities in the main plan.

## Agreed profile behaviour

- Supply a factory baseline that users can edit. Re-running initialization must preserve edits
  or ask before replacing them; do not silently regenerate over custom work.
- Load selected factory resources and allow repository-provided resources and instructions.
- Exclude automatically discovered personal skills and extensions. Users can explicitly add
  extras. This controls configuration; it is not a host security sandbox.
- Initialization should install the role's extensions and skills.
- Check for Pi, tmux, and the Forgetful executable when the selected mode needs it. Ask permission
  before installing missing executables. Do not silently upgrade existing installations.

## Agreed Forgetful configuration

- During `init`, choose the connection method: MCP by default, with CLI as the alternative.
- Choose the Forgetful instance and save the connection choices in factory configuration.
- Support a local executable as well as an existing server; do not require a separate HTTP
  service for local use. Access method and local/server selection are separate choices.
- Use one shared connection method and instance for the Foreman and feature-owner.
- Implementation and review agents do not access Forgetful directly under the current plan.
- Configure independently of personal Pi settings. Importing or discovering an existing personal
  connection is out of scope; users can supply the same details themselves.
- Keep credentials out of committed configuration.
- The Foreman keeps its own Pi-managed credentials. Defer feature-owner credential sharing until
  its profile is implemented; do not copy tokens or build shared-token machinery in this slice.
  Shared connection settings do not require shared login tokens.

The implemented fields, database selection, and installation mechanics are recorded in the ADR.
Shared settings must identify the same data store for both roles, even if each launches its own
process. These choices do not change the separate extension's background memory integration.

## Verified execution modes

Source inspection of published Forgetful 0.5.4 and the local checkout confirmed:

- Local MCP: Pi can launch `forgetful serve --transport stdio` as a child process and communicate
  over stdin/stdout. No separately running HTTP service is needed.
- Remote MCP: Pi connects to an existing streamable HTTP MCP endpoint.
- Local CLI: `forgetful ... --local` executes directly against the configured database and exits.
  SQLite is the default; PostgreSQL requires its own database server.
- Remote CLI: `forgetful ... --server URL` sends operations through the server's MCP interface.

The executable comes from the `forgetful-ai` Python package, which requires Python 3.12+ and its
package dependencies. It is not a Pi extension. Pi has native MCP support; a separate MCP extension
is not required to launch the stdio process.

Evidence: [Forgetful 0.5.4 connectivity guide][forgetful-connectivity] and
[CLI documentation][forgetful-cli]. Generated-profile live checks are recorded below.

## Authentication and launch findings

Checked Pi 1.2.0 documentation/source, AgentShell 0.4.0, and Forgetful 0.5.4/source.
Context7 supplied some Pi resource documentation; official docs and source supplied missing
MCP and CLI details.
These findings do not establish new minimum dependency versions for the factory.

### MCP OAuth

Pi's [MCP documentation][pi-mcp] describes dynamic client registration for HTTP servers:

- A server URL can be sufficient; users normally do not supply a client ID or client secret.
- `pi mcp login <server>` works outside an agent session. Pi registers the client, opens browser
  authorization, and waits for approval. A terminal also accepts a pasted redirect URL when the
  browser is on another machine.
- Pi owns token storage and refresh. Credentials are stored in `mcp-auth.json` under its agent
  directory and are associated with server name and URL.
- Separate role directories use separate credential stores by default. No independent credential
  path override was found in the CLI/environment interface. Do not assume token copying or
  symlinking is safe, especially during concurrent refresh.
- `pi mcp list --json` checks all enabled connections; distinguish Forgetful from unrelated servers.
- Servers without dynamic registration can use a preregistered client.

The watcher must not implement OAuth or manage Pi tokens. This agent connection does not implement
or settle the future watcher-to-Forgetful plan-scaffolding connection.

### Forgetful CLI

- Remote commands support bearer authentication through `FORGETFUL_TOKEN` and browser OAuth,
  including dynamic registration and token refresh.
- Successful `forgetful auth login --server URL` changes the user's default server configuration.
  Factory setup must avoid unintended changes to personal settings.
- On Linux/WSL, `XDG_CONFIG_HOME` can redirect CLI configuration and token storage. The final
  layout is locally validated; remote authentication and concurrent refresh remain unverified.
- Planning/task operations are available through `forgetful call OPERATION --args JSON`.
  Availability depends on server configuration and permissions.
- Validation calls can trigger OAuth or refresh credentials; do not treat them as guaranteed
  non-interactive probes. Connectivity alone does not prove access to required planning operations.

### Profile loading through AgentShell

- `PI_CODING_AGENT_DIR` reaches Pi through the controller's inherited environment.
- AgentShell 0.4.0's `open_interactive()` has no arbitrary Pi resource-flags parameter; its Pi
  adapter rejects `allowed_tools`. Investigation found no newer published release resolving this.
- Pi settings can exclude shared personal skills. Trusted project resources use project settings
  and can override role settings, including MCP configuration.
- Repository instruction loading is separate from resource filters. Preserve it.
- Validate actual resource loading through the supported AgentShell lifecycle; do not bypass it
  with factory-owned tmux commands or rewrite repository settings to force isolation.

[pi-mcp]: https://pi.dev/docs/latest/mcp#authenticate-with-oauth
[forgetful-connectivity]:
  https://github.com/ScottRBK/forgetful/blob/v0.5.4/docs/connectivity_guide.md
[forgetful-cli]: https://github.com/ScottRBK/forgetful/tree/v0.5.4/app/routes/cli

## Implemented initialization flow

1. Collect the shared access method and local executable/database or existing server.
2. Save configuration and prepare editable role resources without overwriting customizations.
3. Ask before missing-executable or role-runtime installation. Use reviewed dependency locks;
   unsupported install targets require a manual handoff and recheck. Never silently upgrade.
4. Check local access. For remote access, require an explicit connection-check or login choice;
   Pi or the CLI owns OAuth and tokens. Unchecked remote setup is labelled as such.
5. Fail with retry guidance on refusal, interruption, mismatched configuration, or failed checks.
   Preserve completed setup steps for retry; never equate a partial runtime with readiness.
6. Before watch launches, validate local resources/runtime and shared targets without contacting
   a remote service. Structurally complete remote profiles may launch with unknown connection
   status.

CLI credential isolation is supported only on Linux/WSL. Remote transport requires HTTPS except
for localhost/loopback HTTP. Local model caches must be provisioned separately; factory-launched
Forgetful runs offline/cache-only rather than silently downloading models.

## Initial implementation

Scott confirmed the final installation and credential choices and requested implementation after
compaction, followed by a SonarQube scan and independent Opus review. Proceed with the agreed scope;
no further general planning round is required. Implement in vertical slices using TDD, with
dependency audits before installation or upgrades.

Completion sequence:

These completed items record the original implementation only. The correction checklist at the
end of this document controls the current completion claim.

- [x] Run the agreed regression suite, lint, architecture checks, and live validation as authorized.
- [x] Regenerate the Mycelium map after code changes; update the overview and relevant ADRs.
- [x] Run SonarQube and inspect findings and the quality gate.
- [x] Send the completed implementation and validation evidence to Opus for independent review.
- [x] Fix initial review findings with regression tests; rerun checks and SonarQube.
- [x] Complete independent Opus recheck and address further findings.
- [x] Record actual validation and review evidence here, including anything still unverified.

## Validation evidence

Historical evidence: the following runs tested the former wrapper/status-extension design.
They are retained for provenance, superseded by Scott's correction below, and are not evidence
that the current native CLI/watcher design has passed live smoke or independent review.

- Before implementation, the existing 61 tests passed on Python 3.12 (129.5 seconds).
  The configuration loader used the pre-existing installed package; CLI fixtures target source.
  Final validation must rebuild/install the changed package and test that artifact as well.
- Live prerequisite check: the existing Forgetful checkout executable returned an empty project
  list against a disposable SQLite database using local CLI. Pi 1.2.0 then connected to that same
  database through stdio MCP and reported all three Forgetful discovery/execution tools. Neither
  check used an HTTP server, credentials, model calls, or personal configuration. These checks
  establish the underlying modes, not yet the generated factory profile or AgentShell launch.
- A generated local-MCP Foreman profile was launched through real AgentShell 0.4.0 and Pi 1.2.0
  with a disposable HOME, repository, and SQLite database. The probe found the three Forgetful
  tools, AgentShell tools, `/hide-tools`, Foreman instructions, repository instructions and skill;
  the test personal shared skill was excluded. Startup reached its awaiting-input status.
  No model call, remote authentication, token copying, or live GitHub operation was performed;
  the owned session was closed. Evidence: `/tmp/factory-slice3-live-ready.log`.
- The repeatable opt-in check is now `tests/smoke_foreman.py`. It also verifies `/hide-tools`
  toggles its role-local preference and asserts the exact connected/awaiting-input message.
  Both local MCP and local CLI pass using an explicitly supplied existing FastEmbed cache with
  downloads disabled. The final checks install the real role-local AgentShell Python environment
  from its audited lock and the existing uv cache, with network access disabled for the installer.
  No global package installation, model inference, or remote login ran. Evidence:
  `/tmp/factory-slice3-committed-smoke.log` and `/tmp/factory-slice3-committed-smoke-cli.log`.
  Earlier disposable-HOME checks did allow Forgetful to fetch its default model files; they were
  not fully offline. The committed check requires a cache and sets offline/cache-only controls.
- An earlier live launch exposed a startup ordering problem in the status extension; status
  polling must not block the later native MCP session-start handler. Validation now waits for
  the UI's status message, not just AgentShell's earlier session-ready event.
- The initial SonarQube scan found five maintainability issues. Refactoring the connection-choice,
  installer, and startup-status code, reusing the MCP path, and simplifying test fixtures cleared
  them without suppressions. Analysis `efb8c650-bb47-42a9-99ab-8f172ac14db7` passed the assigned
  gate with zero open issues and 0.0% new duplication. Coverage is not part of this gate.
  The scan covers uncommitted working-tree changes; SCM metadata still names the previous commit.
- All 95 tests pass on Python 3.12 (149.1 seconds) and Python 3.13 (148.6 seconds), including
  installer refusal/failure, interrupted authentication, profile preservation, and lifecycle tests.
  An intermediate test-fixture refactor missed one helper reference; the full suite caught it,
  and both complete suites passed after correction.
- Ruff and all three dependency contracts pass. Wheel and source-archive builds pass using
  audited uv 0.13.1. A separate cached wheel install passed actual CLI initialization, resource
  inclusion, and public configuration loading with only external-command fixtures. No root
  package dependency was added or upgraded.
- Opus identified two blockers: a partially installed AgentShell runtime could be accepted on
  retry, and `watch` could launch from a half-finished profile. Both now have regression fixes.
  Related review work covers watch-time target consistency, user ignore rules, CLI wrapper
  interpreter lifetime, interrupt guidance, platform credential isolation, and transport security.
- Two advisories are documented rather than expanded into new features: offline mode also prevents
  automatic catalog refresh, and startup status is a bounded snapshot rather than a health monitor.
  Context7 supplied general model-refresh guidance; installed Pi 1.2.0 source/docs confirmed the
  offline flag's exact behaviour. Final post-review validation and recheck will be recorded below.

## Planned validation

- [x] Use TDD for initialization choices, MCP defaults, local/server selection, and persistence.
- [x] Verify local MCP subprocess and local CLI access without a separately running HTTP service.
- [x] Store one shared instance/database configuration; only the Foreman profile is generated now.
- [x] Verify resource installation and re-initialization preserve user edits as agreed.
- [x] Cover missing Pi/tmux, installation permission, refusal, and installation failure with
      fixtures.
- [x] Check secret-field rejection, ignored credential paths, and redacted failure diagnostics.
- [x] Cover simulated sign-in cancellation, failures, interrupted setup, and retry without false
      success; live remote sign-in remains unverified.
- [x] Validate registered tools, personal-resource exclusion, and retained repository resources and
      instructions in an isolated Pi session launched through AgentShell.
- [x] Verify short startup status and discussion-only role instructions without owner dispatch.
      Live model-driven issue discussion was not exercised.
- [ ] With permission, test HTTP dynamic registration, restart credential reuse, and token refresh.
- [x] Validate CLI targeting and isolated authentication configuration with fixtures and local
      smoke.
      Remote CLI OAuth remains unverified.
- [x] Preserve initialization and watcher regressions, Ruff, and architecture checks.

Initial planning did not change code or run sign-in. The original implementation added no root
dependency or upgrade. Its referenced `slice-3-supply-chain.md` is absent from this checkout;
[bundled source notes][bundled-sources] identify retained provenance and install locks, not a full
audit replacement. The later AgentShell 0.5.0 audit covers only that separate dependency update.
No live remote sign-in or server-side registration was performed.

[bundled-sources]: ../../src/forgetful_factory/resources/ROLE-SOURCES.md

## Post-review validation

- Runtime receipts, metadata fingerprints, isolated import probes, and watch preflight address the
  two blockers. Tests also cover failed-install retry, target edits, static repository overrides,
  user ignore rules, launcher lifetime/edit preservation, interrupted setup, HTTPS, and CLI OS
  guards.
- The CLI launcher uses the persistent role interpreter. Even interpreter-only user edits are
  preserved with a clear error; no legacy migration heuristic silently rewrites them. A failing
  public-init regression was observed before the correction.
- All 110 tests passed on Python 3.12 (155.3 seconds). Python 3.13 completed the same suite in
  156.7 seconds with one expected skip: the managed Forgetful recipe targets Python 3.12.
  Evidence: `/tmp/factory-slice3-final-review-312.log` and the corresponding `313.log`.
  An initial parallel run exceeded the tool deadline; complete serial reruns supplied these results.
- Post-review SonarQube found four maintainability issues. Named runtime-input constants, a shared
  settings path, and a separate server validator cleared them without suppressions. Final analysis
  `886038b6-eaeb-4082-9cda-08b46913b846` passed the assigned gate, with zero open issues and 0.0%
  new duplication. No coverage claim is made. Evidence:
  `/tmp/factory-slice3-final-review-sonar.json`.
- Ruff and all three import contracts passed. Wheel and source archive built offline; a separate
  installed-wheel test passed actual init, bundled-resource checks, and the public config loader.
- Final real-runtime MCP and CLI checks passed with cached models and offline role-runtime setup:
  `/tmp/factory-slice3-final-review-smoke-mcp.log` and `...-smoke-cli.log`. Both used the public
  AgentShell lifecycle and closed their owned sessions. No model call or remote sign-in ran.
- Mycelium 0.4.5 regenerated the 37-box map; repeat export from the same map matched byte-for-byte.
  Eight external-base warnings and heuristic call-edge limitations remain documented in the
  overview. Mermaid was checked as text, not rendered. `FACTORY.md` remains unchanged.
- Live remote OAuth/DCR, refresh/reuse, actual Pi/Forgetful/tmux installation transactions, and
  model-driven issue discussion remain unverified. There is no hosted CI result for these
  uncommitted changes. No commits or pushes were made.
- Opus independently reproduced both original blocker scenarios after the fixes and confirmed
  they no longer pass incomplete setup. Its recheck found no new blockers and four advisories:
  more Pi-generated state needed ignoring; managed Pi needed failed-install protection; hidden
  MCP tools should not count as usable access; and watch should apply init's launcher check.
  All four now have passing regression tests. Context7 was unavailable for the exposure lookup;
  installed official Pi 1.2.0 types/source establish that hidden tools are registered but
  unreachable, while codemode tools remain usable.

### Final advisory-fix checks

- Full suite: 116 tests passed on Python 3.12 (172.9 seconds); Python 3.13 completed in
  169.4 seconds with the one expected Python-3.12 installer skip. Evidence:
  `/tmp/factory-slice3-complete-312.log` and `/tmp/factory-slice3-complete-313.log`.
- SonarQube analysis `50deaa89-d882-49bd-b493-b59a7eda9d01`: assigned gate passed, zero open
  issues, 0.0% new duplication. Evidence: `/tmp/factory-slice3-complete-sonar.json`.
- Both real cached-runtime smoke checks passed again and closed owned sessions. Evidence:
  `/tmp/factory-slice3-complete-smoke-mcp.log` and `...-smoke-cli.log`.
- Ruff, all three architecture contracts, offline wheel/sdist builds, and installed-wheel
  init/resource/public-loader verification passed again. The final map was regenerated and its
  repeat export matched. Evidence: `/tmp/factory-slice3-complete-build.log` and `...-wheel.log`.
- Opus independently confirmed all four advisory fixes and both original blocker fixes, with no
  blockers. Its final small edge-case finding was a traceback on non-UTF-8 launcher contents.
  The public init/watch regression reproduced it, then raw-byte comparison fixed it while
  preserving the file. The error also explains moved workspaces. Evidence:
  `/tmp/factory-slice3-red-binary-wrapper.log` and `...-green-binary-wrapper.log`.
  The full validation results above were rerun after that correction. The byte-comparison
  correction follows Opus's recommendation; it did not receive another independent review pass.

## Follow-up: use Forgetful's native CLI

Scott requested removing `factory-forgetful`: the factory should configure access, not expose
another command interface or duplicate Forgetful's argument/authentication handling.
The wrapper is removed. The earlier wrapper review evidence above is historical; it does not make
that wrapper a requirement.

The change must retain shared targeting, custom executable paths, and role-local credentials.
Credential-directory settings must apply only to the Forgetful process, not redirect `gh` or the
whole Pi shell. MCP behaviour, remote-login consent, and editable resource preservation stay intact.

## Correction: watcher status and native CLI isolation

Scott explicitly clarified that startup status belongs in watcher output, not Pi UI. The bundled
`factory-status.ts`, its generated settings entry, required-resource check, and obsolete startup
extension tests are removed. New profiles contain the requested AgentShell and hide-tools
extensions plus the Foreman skill. There is no replacement extension, command wrapper, forwarding
script, alias, custom tool, model prompt, or private AgentShell hook.

The existing public lifecycle still waits for a system event with a session ID. After that
acknowledgement, the watcher reports Foreman readiness and that Forgetful was not checked.
Attach instructions still appear before startup. Session readiness is not connectivity evidence;
native Pi `/mcp` owns live MCP display. Watch performs no automatic remote auth/connection probe,
and ownership, polling, notification submission, busy/idle behaviour, and shutdown are preserved.
Deliberate initialization checks remain native Pi/Forgetful operations.

Official Forgetful v0.5.4/local `app/config/settings.py` lists `.env`, `docker/.env`, and the user
configuration `.env`; `app/routes/cli/paths.py` uses the XDG directory on Linux/WSL. Therefore XDG
alone does not isolate repository dotenv files. Generated skill commands now use a role-directory
subshell with per-command XDG. Local launch explicitly sets `FORGETFUL_SERVER=''` to override saved
remote defaults, including native `auth status`, which accepts no target flag. Remote launch sets
the configured URL. `auth logout` also takes no target flag. Personal bearer tokens are excluded;
the Linux/WSL guard remains. Init checks retain role cwd. Relative executable paths resolve before
the directory change; custom absolute paths/spaces are preserved. CLI arguments are not rerouted.

Context7 returned general Forgetful dotenv guidance, but no relevant AgentShell lifecycle match or
precise CLI precedence details. Official local source supplied those details. AgentShell's public
`session.events()` maps Pi session-start to a system event with session ID. No dependency was
installed or upgraded for this correction.

Existing testing profiles require a manual refresh: update the Foreman skill, remove the old status
entry from settings, and review old status/wrapper files before deleting them. Init preserves
existing user resources and custom settings. The initial correction left DinoLand untouched;
the separately authorized refresh is recorded below.
No generic migration framework is introduced. `FACTORY.md` is unchanged.

Correction validation:

- [x] TDD red/green at public init/watch seams for requested resources and old-file preservation.
- [x] TDD red/green for status after session readiness, no false-ready on startup failure, and
      no automatic watch-time connection/auth commands.
- [x] TDD red/green executing generated native CLI examples through the external AgentShell fixture
      and controller-inherited environment: role cwd, empty local server, exact native auth flags,
      absolute/relative paths with spaces, unchanged surrounding cwd/XDG, and token exclusion.
- [x] Update the opt-in smoke to assert AgentShell readiness and watcher output, retain native MCP
      registration checks and deliberate native CLI init check, and remove deleted UI assertions.
- [x] Targeted Python 3.12: 54 tests passed in 15.240 seconds. Ruff and three import contracts pass.
- [x] Targeted Python 3.13: 54 tests in 14.991 seconds, with one expected 3.12 installer skip.
- [x] Full Python 3.12: all 113 tests passed in 151.323 seconds, including startup timeout,
      shutdown, ownership, polling, and notification regressions. Evidence:
      `/tmp/factory-correction-full-312.log`. Targeted logs use the same prefix and `targeted-312`
      or `targeted-313` suffix.
- [x] Full Python 3.13: 113 tests in 153.699 seconds, with the expected installer skip.
      Evidence: `/tmp/factory-correction-full-313.log`.
- [x] Regenerated the Mycelium map using the existing cached 0.4.5 executable after offline
      `uvx` resolution failed. No package installation was needed. The map has 35 boxes and eight
      external-base warnings; same-map repeat export matched. Mermaid was checked as text only.
- [x] Offline wheel/sdist build and installed-wheel init/resource/public-loader checks passed.
      Packaging checks also confirm the removed wrapper and status extension are absent.
- [x] Final SonarQube analysis `386cd832-f110-4ef6-bf97-3f3b7bce1df6`: assigned gate passed,
      zero open issues, 0.0% new duplication. The assigned gate does not require coverage.
- [x] Real cached MCP/CLI smoke checks passed, including watcher readiness and owned shutdown.
      The first MCP probe exposed a smoke timing assumption: session readiness precedes tool
      registration. The fixture now polls fresh tool snapshots with a separate 40-second bound;
      MCP passed after five snapshots and CLI after one. No product timing workaround was added.
      Evidence: `/tmp/factory-correction-poll-smoke-mcp.log` and `...-cli.log`.
      Both owned sessions closed. No model calls, remote auth, or downloads occurred.
- [x] Independent Opus review found no blockers, confirmed alignment with `FACTORY.md`, and
      reproduced the earlier install/readiness/ignore/target fixes successfully. No replacement
      tool, wrapper, or custom status extension was found. Its CLI isolation advisory is recorded
      in the ADR and README: arbitrary agent shell commands are not forced to follow the skill.
      Old editable profiles are preserved rather than automatically migrated.
- [x] Version evidence is qualified: live smoke used the editable Forgetful checkout `7e817d4`
      (`v0.5.4-13`), whose installed package metadata still reports `0.5.1.dev4`. It did not test
      a clean published 0.5.4 wheel. Native CLI/auth and dotenv source were also inspected at the
      official `v0.5.4` tag; Opus independently inspected its available 0.5.1 source.

All correction checks above passed on the uncommitted working tree. Hosted CI was not run for
these changes. Remote OAuth/refresh and actual missing-host installation transactions remain
unverified. No remote authentication, model call, host upgrade, or commit ran in this correction.

### Authorized DinoLand refresh

After validation and review, refreshed DinoLand's Foreman skill, removed the status extension
settings entry, and removed the old status and wrapper files. Custom settings, MCP configuration,
credentials, runtime, and session files were preserved. Read-only local setup/runtime/target
preflight passed before and after; no remote connection or login was attempted. Backups of only
the changed files are outside either repository under
`~/.local/state/forgetful-factory/profile-backups/DinoLand-20261014T233436Z`.
The existing Foreman must be restarted to pick up the refreshed profile and launch environment.
