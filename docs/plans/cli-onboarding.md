# CLI access and shared Pi login

Status: closed with Slice 3 on 2026-10-16 at Scott's request after his DinoLand trial.
Implemented and locally validated; final trial-feedback evidence below supersedes earlier runs.
Opus recheck found no blockers; the final SonarQube gate passes with zero open issues.

Back to [plan](../plan.md) and [agent profiles](../adrs/agent-profiles.md).
This follow-up supersedes Slice 3's MCP-default and separate model-login choices for new setup.
Historical Slice 3 evidence does not validate this change.

## Decision and scope

Scott chose Forgetful's native CLI for now after AgentShell's exact Pi MCP selection request
was closed as not planned. Docker remains a possible later investigation, not an implementation
requirement. See [AgentShell #27][mcp-gap] and the [0.5.0 resource capabilities][capabilities].

- Reuse the selected normal Pi home and native model login with explicit setup consent.
  Do not copy credentials, symlink token files, implement OAuth, or inspect token values.
- Select the Foreman's local, already provisioned skills/extensions through AgentShell 0.5.0.
  Exclude automatic personal and project resource loading together; explicitly disable native MCP.
  Extra repository skills/extensions must be explicitly selected. Keep instruction loading enabled.
- Use only Forgetful's CLI, targeting the configured local database or existing server.
  Keep Forgetful's configuration directory independent of the shared Pi home, with per-command XDG
  configuration and role working directory. Never export that XDG change across all agent commands.
- Preserve editable role resources. Do not silently convert old MCP profiles or edit personal
  configuration. Existing testing profiles can be reconciled explicitly; no migration framework.
- Use AgentShell model discovery to present exact provider/model selectors. Missing login must
  give native Pi `/login` instructions, not guessed commands or a separate authentication wrapper.
- Do not forward issues from an incomplete setup. Distinguish configured credentials, a started
  session, and successful inference. A configuration check does not verify provider/model access.
- Keep the Foreman discussion-only. Feature-owner dispatch, its bundled worker upgrade, durable
  issue delivery, Docker, and custom Factory extensions are outside this change.

## Limits that must remain visible

Shared Pi home means shared native settings, model configuration and login/logout state, not
selected-provider credential isolation. Personal `SYSTEM.md` is now excluded from Foreman launch;
other personal instruction and append files may load. Workspace `.pi/SYSTEM.md` blocks setup/watch
because AgentShell cannot preserve it while excluding the home prompt in interactive mode.
Resource switches are not a filesystem or security sandbox. Model discovery uses Pi's native
listing behavior rather than the session's selected-resource filters.

AgentShell cannot select a role's native append-system file through `SessionResources`. Role
instructions must use existing public skill/launch facilities, not a new Factory Pi extension.
A normal launch prompt makes a model request; it is not a free metadata or authentication check.

Automatic package fetching through AgentShell is not the Factory's consented, reviewed installer.
Pass local provisioned resources only. A top-level upgrade does not upgrade the bundled AgentShell
extension's Python runtime or expose resource selection to its child-agent tools.

Native CLI isolation remains instruction-dependent for arbitrary agent shell commands. If a command
omits the role cwd or scoped XDG setting, it can use personal or repository Forgetful settings.
A later provider failure after terminal submission remains outside the watcher's acknowledgement
contract: submission is not proof of a model response, and durable retries are not added here.

## Validation plan

Use the previously approved public CLI and configuration-loader test boundaries. Add integration
checks at the external Pi/AgentShell command boundary, not private implementation mocks.

- [x] Audit AgentShell 0.5.0 artifacts/dependencies before upgrading the lock and environment.
- [x] Verify consent/refusal, chosen Pi-home persistence, missing login and model selection.
- [x] Verify CLI defaults, explicit rejection of MCP setup, and local/server targeting.
- [x] Verify distinct Pi and role roots, safe diagnostics, and native CLI invocation semantics.
- [x] Verify selected resources, disabled MCP, preserved instructions and repository additions.
- [x] Verify incomplete setup blocks watch before polling; preserve issue-delivery behavior.
- [x] Run regression tests, Ruff, architecture checks, builds and installed-wheel validation.
- [x] Run an isolated real Pi/tmux smoke without personal credentials, model requests or downloads.
- [x] Refresh Mycelium, architecture and relevant ADRs; record current source locations.
- [x] Complete independent Opus review/recheck and fix actionable findings with regression tests.
- [x] Run SonarQube through envault and verify the final gate and issue results.

No live provider login, refresh or inference is authorized by this validation plan. Such checks need
separate consent. Personal Pi and DinoLand profiles remain untouched by this implementation.

## Evidence

The [AgentShell audit](agentshell-0.5-audit.md) preceded the dependency update. `uv lock`
changed only AgentShell's version/artifacts and the root constraint. The local Python 3.12
Factory environment and a temporary Python 3.13 validation environment now use 0.5.0; no global
Pi or user profile was changed. The bundled child-agent runtime remains pinned to 0.4.0.

The initial implementation passed 125 Python 3.12 tests. Opus then reproduced two blockers:
failed Forgetful setup could leave a usable receipt, and preserved old skill instructions could
target the shared Pi home instead of the role directory. Both were fixed with public init-to-watch
regressions. Completion is recorded only after successful setup and binds the model/home/connection.
It is invalidated before accepted reinitialization work. Obsolete commands block setup/watch with
manual reconciliation guidance; edited files are preserved. Generated receipts are safely replaced
and git-ignored. Explicit model validation precedes label/config writes, missing Pi homes give
native setup guidance, and consent describes shared extension preferences and native state.

Pre-refactor local evidence:

- Final Python 3.12: 143 tests passed in 171.170 seconds (`/tmp/factory-cli-final-312.log`).
- Final Python 3.13: 143 tests run, one expected Python 3.12 installer skip, in 169.764 seconds
  (`/tmp/factory-cli-final-313.log`).
- Ruff and all three import contracts pass. Offline wheel/sdist builds pass. A fresh installed-wheel
  environment using the audited 0.5.0 wheel passed public init/reinit, configuration loading and
  resource inclusion with external command doubles (`/tmp/factory-cli-wheel.log`).
- Real Pi 1.2.0 / AgentShell 0.5.0 CLI smoke passes after the review fixes. It uses a disposable
  home/socket, the cached reviewed 0.4.0 extension worker, and a synthetic loopback provider.
  Both inputs are intercepted before inference; zero provider requests were recorded. Selected
  role/repository resources load, automatic personal/project resources and native MCP do not,
  native Forgetful CLI lists the disposable database, and watcher shutdown removes its session.
  Evidence: `/tmp/factory-cli-parent-smoke.log` and `/tmp/factory-shared-pi-smoke-ruru5x89`.
  The cached Forgetful executable reports version 0.5.1; this is not a published 0.5.4 install test.
- Mycelium 0.4.5 was reused from its previously audited cache. The map has 36 boxes, one diagram
  and eight unresolved external-base warnings. Same-map repeat export matches byte-for-byte;
  Mermaid was checked as text, not rendered. Source navigation and the role ADR were updated.
- Opus independently reproduced both blocker fixes and found no remaining blockers. Its remaining
  advisories note intentional pattern-based old-guidance detection, interactive provisioning before
  GitHub access validation, and inherited database environment variables. A minor mistyped-home
  diagnostic was then fixed with a failing public-CLI regression: it now names the saved consent
  file and explains how to approve the corrected home. No new login or migration mechanism.
- A built-source-archive check found that the new legacy skill fixture was omitted. The source
  include list now ships `tests/fixtures/*.md`; the actual extracted-archive regression changed
  from a missing-file failure to a pass (`/tmp/factory-cli-sdist-red.log` and `...-green.log`).
- `FACTORY.md` remains byte-identical to the starting working tree, including Scott's existing
  changes. Bundled source/install archives were not upgraded. No commits or hosted CI runs.

## Six-smell refactor and final SonarQube evidence

The initial analysis `68ea2dfc-68f4-457a-9cc1-44765f8546ad` failed on six code smells only,
with zero duplication. Four `python:S1192` findings concerned repeated profile filenames;
two `python:S3776` findings concerned `launch_resources` (19) and CLI `main` (16), against 15.

The refactor names the four paths, extracts local-resource path validation, and moves the existing
init command body into `_initialise`. Validation order, messages, resource ordering, setup effects
and exception handling remain unchanged. No dependency or configuration contract changed.
Existing public-CLI regressions cover malformed/missing resources, editable-file preservation,
consent, incomplete setup, retries and watcher behavior; no helper-coupled tests were added.

Green/refactor/green validation used the existing suite:

- Baseline Python 3.12: all 143 tests passed in 171.020 seconds.
- Refactored Python 3.12: all 143 tests passed in 171.198 seconds.
- Refactored Python 3.13: 143 tests run in 171.884 seconds, with the expected Python 3.12 installer
  skip; all other tests passed. Both environments retained AgentShell 0.5.0.
- Ruff and all three import contracts passed without caches. Offline wheel/sdist builds passed.
  Context7 confirmed that Import Linter's no-cache run checks indirect dependencies too.
- Cached Mycelium 0.4.5 regenerated one diagram with 36 boxes and full member signatures. Its
  export predates `--detail`; the default retains full signatures and relationships. The same-map
  repeat export matched byte-for-byte. Eight unresolved external-base warnings remain; call edges
  are heuristic and bundled archives are not expanded. Mermaid was checked as text, not rendered.
- The extracted init body is AST-identical to its original. Hash checks confirmed all starting
  source/test/document files outside the eight intended changes, including `FACTORY.md`, remained
  unchanged. The overview, ADRs and plan reflect the completed scan and current source locations.

Final SonarQube analysis `37d8a03a-36b4-4454-85d1-c14d720c867d`, project `forgetful-factory`,
branch `main`, 2026-10-16 12:52:44 UTC, passed. The scanner and subsequent API query by analysis ID
both report a passing gate. All six findings are resolved: zero open issues, code smells, bugs,
vulnerabilities or security hotspots. Duplication is 0.0%, with zero duplicated lines or blocks.
New violations are 0 (allowed 0); new duplication is 0.0% (maximum 3%). Aggregate cognitive
complexity changed from 434 to 426; cyclomatic complexity from 472 to 473. These are project totals,
not per-function complexity reports. Coverage reads 0.0%; no coverage report was supplied or gated.

The existing envault aliases and project mapping supplied scanner/API credentials. No plaintext
secret file was read, no token was passed in argv, and no credential mappings or Sonar scripts were
edited. The supplied scanner command only gained a temporary working-directory override. Evidence
is under `/tmp/factory-sonar-refactor-7o8licti/`: `sonar-scan.log`, `sonar-before.json`,
`sonar-final.json`, and the scanner task receipt. Regression logs are `tests-before-312.log`,
`tests-312.log`, and `tests-313.log`; `build.log` and `dist/` retain the packaging evidence.
The scan covers the dirty working tree, not just the recorded HEAD revision; no commit was created.

Limits: the credential permits scanning, gate status, measures, issues and task lookup, but returns
HTTP 403 for analysis history and assigned-gate metadata. The previously recorded gate name,
`Sonar way sans code coverage`, could not be independently rechecked; no gate configuration was
changed. Sonar warns about UTF-8 decoding of the two bundled ZIP archives and missing blame for
25 dirty/untracked files. Archive contents are not validated by this source scan. Live provider
authentication/inference and personal Pi/DinoLand changes remain outside this validation.
Repository-wide `git diff --check` reports Scott's existing `FACTORY.md:224` trailing whitespace;
that file remains unchanged. Checks of the refactor's own files pass.

[mcp-gap]: https://github.com/ScottRBK/agent-shell/issues/27
[capabilities]:
  https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/development/agent_parameter_comparison.md

## Trial feedback: clearer consent, prompt exclusion and Python selection

Status: implemented and locally validated; Opus recheck found no remaining blockers.
This section supersedes earlier statements that personal `SYSTEM.md` stays enabled.

Scott's DinoLand trial exposed three onboarding problems:

- The Pi-sharing question was a dense implementation description. It now explains login reuse,
  shared settings/history, remaining instruction loading, model-listing execution and possible
  charges in short lines. Declining still stops before Pi or GitHub access.
- Personal `SYSTEM.md` was enabled despite the intended role separation. Foreman launch now uses
  AgentShell's public `include_home_system_prompt=False`. This suppresses that file's discovery
  and keeps Pi's built-in prompt; `AGENTS.md` and `APPEND_SYSTEM.md` remain separate inputs and are
  explicitly disclosed. No custom extension, launcher or credential copying was added. AgentShell
  0.5 cannot combine this choice with workspace `.pi/SYSTEM.md`; init/watch reject that case early
  with reconciliation guidance and leave the project file untouched.
- The reviewed Forgetful lock needs CPython 3.12, but init wrongly required Factory itself to run
  under it. Read-only uv discovery now selects an existing CPython 3.12 independently of Factory's
  interpreter. It ignores project/uv configuration, forbids downloads and validates the returned
  executable with an isolated version probe. Missing prerequisites stop before installation consent.
  The prompt now says **Forgetful CLI**, gives its local destination, names PyPI as its download
  source, displays the verified Python 3.12 path and explains that it will not start another server.
  Reviewed hashes, binary-only installs, retries and refusal remain intact.

The old installer regression accepted failure on Python 3.13, so it could not catch this journey
problem. It now requires successful setup on both supported test interpreters. The old resource test
explicitly required no system-prompt exclusion flag; it tested the prior implementation rather than
Scott's expectation. It now checks public AgentShell launch arguments, while the real smoke checks
actual prompt contents. New public init/watch tests cover unsupported project prompts, refusal,
missing/old uv, invalid Python, sanitized discovery, failed installs and successful retry.

Validation:

- Python 3.12: 153 tests passed in 186.279 seconds; Python 3.13: all 153 passed in 183.602 seconds,
  with no installer skip. Logs: `/tmp/factory-feedback-tests-312-final.log` and
  `/tmp/factory-feedback-tests-313-final.log`. The final CLI wording then passed the nine installer
  tests on both versions. Earlier concurrent suite attempts timed out; final runs were sequential.
- Ruff, all three import contracts and offline wheel/sdist builds pass. A fresh Python 3.13
  environment ran 21 public installer/onboarding tests against the rebuilt installed wheel, with
  source imports disabled (`/tmp/factory-feedback-wheel-final.log`). External commands were doubles;
  no host package install was performed. The PyPI/interpreter wording passed the nine installer
  tests on each Python version after a failing prompt regression. A final full Python 3.13 run
  passed all 153 tests in 180.832 seconds (`/tmp/factory-feedback-postreview-313.log`).
- The existing uv 0.13.1 found the already installed CPython 3.12.11 without downloads. Context7
  confirmed uv interpreter selection and Pi's separate prompt controls; exact installed
  AgentShell source and Pi observations supplied the runtime evidence. Independent research also
  verified Pi 1.2.0's parser, loader and prompt builder are byte-identical to installed 1.3.0;
  six isolated parser/loader cases and public AgentShell capture-host checks passed. Model listing
  can still read home `SYSTEM.md` because it has no session resource filter. This correction is
  launch-only, not complete personal-instruction exclusion. Evidence and source references:
  `/tmp/factory-consent-research-amwtlwyh/findings.md`.
- Real Pi 1.3.0 / AgentShell 0.5.0 smoke passed using disposable homes and an isolated tmux socket.
  It confirmed personal `SYSTEM.md` exclusion, retained personal append/AGENTS and repository
  instructions, selected role resources, native CLI access, zero provider requests and owned-session
  cleanup. Evidence: `/tmp/factory-feedback-smoke.log` and
  `/tmp/factory-shared-pi-smoke-_ir_7z1q`. Pi was already installed; no Pi upgrade was performed.
  The cached worker remains 0.4.0 and cached Forgetful remains 0.5.1, not a fresh 0.5.4 install.
- Cached Mycelium 0.4.5 regenerated the 36-box map; a same-map repeat export was byte-identical.
  Eight unresolved external-base warnings remain. Mermaid was checked as text, not rendered.
- Final SonarQube analysis `379846af-8014-4808-93f0-12b110c3566d` completed at
  `2026-10-16T17:40:10+0000`. Gate **Sonar way sans code coverage** passed, with zero open issues,
  smells, bugs, vulnerabilities or hotspots and 0.0% duplication. The replacement envault token now
  permits assigned-gate lookup; the earlier 403 limitation does not apply to this scan. Evidence:
  `/tmp/factory-feedback-sonar-final.log` and `/tmp/factory-feedback-sonar-final-result.json`.

Opus independently checked the public launch path and real smoke, ran 65 affected tests, and
confirmed five reverted fixes each fail the new tests. Its only blocker was stale Forgetful consent
wording; the prompt and regression now cover the CLI, destination, PyPI source and interpreter.
Opus rechecked the final code, ran 93 affected tests on Python 3.12, and reported no remaining
blockers. Evidence: `/tmp/factory-feedback-opus-recheck.md` and
`/tmp/factory-review-recheck-312.log`.
The old scan/test section above is historical; the final 3.13 environment has AgentShell installed
and no skipped installer cases. Scott's original version-check failure preceded runtime creation,
so it did not create a 3.13 Forgetful environment requiring migration.

Nonblocking review notes retained: prerequisites are checked before each executable's own install
question, not as an all-installations batch; workspace SYSTEM conflicts are detected during profile
preparation rather than before all interactive questions; and watch currently repeats its harmless
read-only guidance check. Broader first-run ordering and unsupported-runtime migration are deferred.

The rebuilt artifact is `dist/forgetful_factory-0.1.0-py3-none-any.whl`; no special `uvx --python`
workaround is required. `FACTORY.md` matches its starting hash. DinoLand and the personal Pi profile
were not edited. No dependencies changed, no live auth/inference ran and no commits were made.

## Close-out and carried-forward work

Scott confirmed the onboarding trial was sufficient to move on and requested Slice 3 closure.
This is acceptance of the discussion-only Foreman/setup scope, not evidence of automatic planning,
feature-owner dispatch, live model access or all supported installation/authentication paths.

Two later trial observations remain recorded in the [main plan](../plan.md): interactive remote
setup still requires a separate consent flag/check, and role-directory `AGENTS.md`/`SYSTEM.md`
are not automatically loaded. Role `APPEND_SYSTEM.md` is an opening user message, not a system
prompt. No implementation changes were made during close-out; these limits were not silently fixed.

The plan review also verified that AgentShell 0.5.0 already ships existing-terminal attachment,
while Factory has not integrated it. Forgetful's unique plan-reference enhancement is upstream but
absent from the published 0.5.4 installer target. Future slices must verify backend capabilities
rather than infer them from closed issues. See the main plan for evidence and proposed sequencing.
