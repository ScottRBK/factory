# Slices 4 and 5 validation

Status: implemented and locally validated. Independent review findings are resolved.
The [plan](../plan.md) describes scope in plain terms. The
[issue-planning ADR](../adrs/issue-planning.md) records recovery rules; the
[profile ADR](../adrs/agent-profiles.md) describes role loading and shared credentials.

## Implemented

- Init selects a Forgetful project, checks planning capabilities and sets up the owner/research
  roles.
- Watch saves the plan, ownership task and ordinary-issue Git worktree before notifying Foreman.
- Issue revisions reuse those records. Restart restores unfinished work, including closed issues.
- Ambiguous task creation and conflicting worktrees stop without deleting saved work.
- Native role AGENTS files, selected skills and explicit child rosters configure Foreman, owner
  and research. The unchanged grill-me skill is read deliberately by the owner.
- Agent guidance covers versioned ownership claims, clarification and safe continuation. It leaves
  implementation/review execution and deployment completion for later slices.

Scott approved public init/watch tests with temporary repositories and controlled external commands,
plus isolated Pi/AgentShell checks without login or model calls. The extra `epic` label, attended
native OAuth and research delegation are approved. Native Git is used; no worktree extension.

## Dependency checks

The Forgetful 0.5.5 upgrade changed only its requirement/version and two artifact hashes. All 113
other dependency versions stayed fixed. All 114 wheels were checked for CPython 3.12 on Linux
x86-64/glibc 2.39, including artifact hashes, wheel records and dependency completeness. Published
source matched release commit `8964f8e626bc4945d2ca3cc2bd38a69ff44082e6`. Publisher signatures,
certificate chains and Rekor inclusion passed; full Sigstore TUF/SCT verification was not performed.

Extension 1.4.0 matched commit `de119eb16045d9cabe82bcc90bac7bb2775f7fb6`, npm integrity/signatures
and all packaged files. Its worker uses audited AgentShell 0.5.0 with no runtime dependencies.
Exactly seven archived extension members changed; other members and hide-tools stayed unchanged.
The top-level AgentShell dependency did not change. See the committed
[bundle provenance](../../src/forgetful_factory/resources/ROLE-SOURCES.md) and hash manifests.

## Test evidence

The implementation recorded RED/GREEN regressions for project/schema rejection, ordinary/epic
intake, changed issues, restart, lost create responses, uncertain task intent, damaged mappings,
origin changes, owner selection, stale runtime bytes and native role loading.

- Python 3.12.3: 180 tests passed, no skips, with native loading checks enabled.
- Python 3.13.5: 180 tests passed, no skips, with native loading checks enabled.
- Ruff and all three Import Linter contracts passed. The new files are covered by the existing
  package-level rules; no exceptions were added. CI checks both Python versions.
- Installed Pi 1.3.0 SDK loaded the generated roles and extension 1.4.0 without inference.
  Native AGENTS files/ancestor instructions and the intended child rosters were observed.
  Research exposed no subagent tool; grill-me retained its no-automatic-advertisement flag.
- The bundled worker's metadata path ran under actual AgentShell 0.5.0 without launching an agent.

A parent check independently installed the audited Forgetful 0.5.5 wheel closure offline into a
private temporary environment. Its temporary SQLite database passed native schema, unique
`external_ref`, task claim/version conflict and transition checks. A stale claim failed, and
returning a task to `todo` retained the old assignment as expected.

That check caught a real API mismatch hidden by the initial fixture: `get_current_user` does not
return an ID. At that stage a public-init regression used the real response shape. The later
two-call check replaced it with a regression rejecting user-profile requests. Factory verifies
user-scoped project access, without claiming a stable principal identity.

After that correction, public Factory init/watch passed against the actual local 0.5.5 CLI and
real Git. A plan and ownership task were persisted, and the notification contained their IDs and
the actual worktree/branch. GitHub and the Pi terminal were substitutes in this check. All data,
HOME/config paths and embedding caches were disposable; no personal credentials or live services
were used.

## Independent review and native smoke

Independent Astra review reproduced three defects beyond the initial green tests: a damaged
worktree `.git` pointer was accepted, Foreman could omit its dispatch resources, and project
selection for an older configuration could succeed without being saved. Public regression fixes
passed independent rechecks. A separate parent RED/GREEN test corrected rejection of Pi's valid
`max`
effort setting for Foreman, owner and research.

The updated `tests/smoke_foreman.py` passed a fresh public init/re-init/watch journey with actual
Pi 1.3.0, AgentShell 0.5.0 and local Forgetful 0.5.5. It used a committed temporary repository,
private database/project, copied caches, disposable Pi home and a private tmux socket. Worker
0.5.0 installation used the audited lock offline. After selecting the test probe, public re-init
created a genuine setup receipt.

The first intercepted Pi input was the issue notification, after the real plan/task/worktree
existed. Native role AGENTS, selected resources and roster were observed; personal SYSTEM and
automatic resources/MCP stayed excluded. Both inputs were handled before inference, the provider
recorder saw zero requests, and watch removed its owned session. This validates Foreman wiring;
child dispatch, claims, planning and resume were not exercised.

The first smoke completed during the fixes. A fresh parent rerun after all fixes also passed,
with unchanged source/test hashes throughout. Its evidence is retained under
`/tmp/factory-shared-pi-smoke-6mcz3iu5`; these scratch files are not runtime dependencies.

## Final checks

- Python 3.12.3: all 188 tests passed in 264 seconds, with native loading enabled.
- Python 3.13.5: all 188 tests passed in 263 seconds, with native loading enabled.
- Ruff and all three unchanged architecture import contracts passed (45 files, 78 dependencies).
- Independent public-boundary repros verified all three review fixes, healthy worktree reuse,
  optional hide-tools, existing-config edit/retry and valid/invalid effort selection.
- Fresh post-fix public init/re-init/watch smoke passed with real Pi/AgentShell/Forgetful and Git,
  zero provider requests, and owned-session cleanup.
- Offline wheel/sdist builds passed. Wheel source/resources matched the working copy byte-for-byte;
  the source archive contains the current planning/native tests and smoke.
- Installing the wheel and audited AgentShell wheel offline in a temporary environment passed
  public init/re-init with controlled external commands, including `max` and all role files.
- Cached audited Mycelium 0.4.5 refreshed the map: 43 boxes, one diagram, full signatures,
  tests excluded and identical same-map repeat export. Ten external-base warnings remain;
  static call edges are heuristic. Mermaid was checked as text, not rendered.

An earlier parent run started both full suites during the native smoke and hit timing failures
and the outer timeout. Individual affected tests passed immediately on their own. Both subsequent
full suites above passed; no timing assertions were weakened. The Design questions section and
Scott's FACTORY.md remained unchanged by this implementation. Hosted CI and SonarQube were not
rerun for these slices; earlier green results do not cover these changes.

## Proof limits

No live model inference, autonomous owner planning, remote OAuth/refresh, production database
migration or personal-profile operation has been validated by these tests. Native resource loading
does not prove a child follows its instructions, claims ownership, asks useful questions or resumes
correctly. Unknown process liveness remains a reason to stop recovery.

Fresh host tool installation and existing-user-profile migration are separate checks. The offline
wheel installation above validates the audited closure on this host, not every platform. Resource
selection is not a security sandbox. No changes were committed, pushed or released in this work.

## Project onboarding feedback

Init now offers an existing project or a confirmed new project. An empty account goes directly
to the creation prompt. The suggested name is the workspace name; no repository-to-project
mapping is assumed. The saved ID comes from Forgetful's response. There is no skip option.

The earlier tests always supplied an existing project, so they missed the empty-account dead end.
New public-init regressions cover empty/nonempty lists, custom/default names, selection, refusal,
EOF, invalid choices, malformed responses, creation failure and retry. Lost responses do not cause
an automatic second create. Re-init keeps the saved choice.

Independent review caught an interruption gap: Ctrl-C after the backend saved a project omitted
the uncertain-outcome warning. A failing public-init regression reproduced it. The fix retains
exit code 130, warns to check the list, and keeps the saved project. Independent reproduction
confirmed that rerunning init selects that project without creating another; ordinary Ctrl-C
messages are unchanged.

Context7 confirmed native project creation. The exact 0.5.5 source and a real local CLI check
resolved differences in the documentation: creation requires name, description and project type,
and the response uses `id`, not `project_id`.

Public init and re-init passed against the existing audited Forgetful 0.5.5 CLI with a temporary
SQLite database and copied offline model cache. One project was created and reused, and its ID
was saved in both configuration and the setup receipt. GitHub, Pi and worker processes were test
doubles; no personal credentials, remote services, authentication or inference were exercised.
The rebuilt wheel also passed all nine project-onboarding tests through public init.

Evidence is retained under `/tmp/factory-project-choice`; it is not a runtime dependency.

Final feedback checks after the review fix: 197 tests passed on each of Python 3.12 and 3.13,
including native role-loading checks. Ruff and all three unchanged import contracts passed.
Offline wheel/sdist builds passed; wheel source/resources matched the working tree.
The Mycelium map was refreshed
with the existing audited 0.4.5 exporter; repeat export matched and the documented warnings remain.
An initial background test invocation inherited ignored Ctrl-C signals and failed shutdown tests.
Both complete reruns used normal signal handling; no application or test assertion was weakened.

## Extension setting-name follow-up

Factory now bundles AgentShell extension 1.4.1 and checks lowercase `max_sub_agent_depth`.
Depth 1 lets Foreman launch the owner and lets the owner launch research; research cannot delegate
further through that extension. The application still does not modify shared Pi preferences.

A public-init regression first reproduced rejection of the new lowercase key, then passed with
1.4.1 provisioned and the preference file unchanged. Existing fixtures and the manual smoke now
use that spelling. The 31 focused tests, including native Pi role loading, passed without inference.

The narrow dependency review compared every bundled file with the official local 1.4.1 Git tag.
Five source members changed. Dependency declarations, package scripts, the Python worker and its
lock are unchanged. Registry DNS was unavailable, so no fresh npm provenance or advisory result
is claimed. The bundle uses inspected source at commit
`df2855129ed2dd9d5aadc27554719ceb62fd38e1`; see the
[bundle provenance](../../src/forgetful_factory/resources/ROLE-SOURCES.md) for the audit scope.

Final checks: all 198 tests passed on Python 3.12 and 3.13, including native loading. Ruff and the
three unchanged import contracts passed. Offline builds passed, and 17 public owner/project setup
tests passed against the rebuilt wheel's contents. The refreshed map repeated byte-for-byte.
No live agent inference, login or package installation was needed.

## Automatic connection checks

Scott's next onboarding trial reached the end of server setup, then failed solely because
`--check-connection` was absent. Init now always checks the connection, selected project and
planning support. The old flag remains accepted but is unnecessary. `--login` still explicitly
runs native Forgetful sign-in before the final check; normal checks reuse native credentials.

The previous tests enforced opt-in checking, so they encoded the awkward flow rather than catching
it. A public-init regression reproduced the failure before the guard was removed. Tests now cover
automatic server checks, re-init, compatibility with the old flag, explicit login, missing access,
unsupported planning schemas and interruption. Failed checks remove completion evidence and block
watch while preserving configuration. Cancellation also stops the owned command process.

Validation: 199 tests passed on Python 3.12 and 3.13, including native role loading without
inference. Ruff and all three import contracts passed. Offline wheel/sdist builds passed, and five
public init/watch regressions passed against the rebuilt wheel's contents. Mycelium's repeat
export matched; its documented warnings remain. Evidence is under `/tmp/factory-always-check`.
No real server, browser login or model request was used. FACTORY.md and Design questions remain
unchanged.

## Connection-check cost and authentication notice

Scott observed machine activity during the automatic check. It launched fourteen sequential
Forgetful CLI processes: user, project and twelve tool descriptions. An isolated, no-network
`forgetful --help` measurement on the audited 0.5.5 runtime took 3.22 seconds, 2.39 user CPU seconds
and 142 MiB peak RSS. Import tracing showed the entry point loads server/bootstrap code before
CLI dispatch. This explains repeated startup work, not the exact earlier machine spike; the later
WSL sample was idle and no production onboarding run was repeated for measurement.

That first reduction used three commands (reduced to two in the follow-up below). Native
`tools list` already returns permitted tool names and
parameter metadata, so it can verify every required operation and both `external_ref` parameters
without separate schema processes. Public init tests first reproduced the fourteen-startup path,
then verified three calls. Missing permissions, malformed catalogs and unsupported parameters still
block completion. This does not fix Forgetful's own startup imports or cache access across runs.

The configured DinoLand server's public policy reported disabled authentication. The old notice
was unconditional for servers. A failing public-init HTTP-fixture test reproduced it; the notice
now requires advertised OAuth. Disabled/JWT/introspection, malformed, oversized, unavailable and
redirect responses do not suggest browser login. A timed-out metadata request still reaches the
real access check. No credentials or returned login URLs are used by the policy request.

Context7 confirmed native discovery; exact 0.5.5 source confirmed catalog parameters, permission
filtering and `/api/v1/auth/info`. Evidence is under `/tmp/factory-check-cost`. No dependencies,
personal settings, server configuration or stored credentials were changed.

Final validation: 206 tests passed on each of Python 3.12 and 3.13, including native role loading
without inference. Ruff and all three package-level import contracts passed, including the new
HTTP adapter. Offline builds passed; seven public regressions passed against the rebuilt wheel.
The map was regenerated with audited Mycelium 0.4.5, with 44 boxes and matching repeat export;
its ten known external-base warnings remain. Hosted CI, a live planning preflight and browser
OAuth were not run. FACTORY.md and the protected Design questions remain unchanged.
Independent Astra review found no actionable issues. It confirmed the three-call check against
0.5.5 and ran one additional public-init loopback case. The socket timeout is not a total elapsed
time deadline; no live authentication or native planning check was added by that review.

## Live issue-reply feedback

Scott confirmed that a GitHub issue reply was picked up during his manual test. This is
user-reported evidence for live reply detection; automated tests still cover revision changes.
It does not establish the separate feature-owner clarification/resume workflow.

## Remove the redundant connection request

The user-profile response was unused. Native `get_project` already authenticates the caller and
checks access to the selected project. Init/watch now run only `get_project` and `tools list`;
all twelve planning permissions and both `external_ref` checks remain required. Explicit `--login`
still runs native sign-in first when requested.

Public init/watch regressions failed on the old third request, then passed with its removal.
The command double now rejects user-profile requests and applies simulated login failures to
project access. Existing login-failure, cancellation, wrong-project and invalid-catalog tests still
block completion. The earlier count test deliberately expected three calls, so it protected the
previous implementation rather than detecting the redundant work.

Context7 describes project access and discovery. Exact Forgetful v0.5.5 adapter/service source
confirms authentication and user-scoped project lookup. No dependency or credential changes were
needed. Evidence is under `/tmp/factory-two-call-check`.

SonarQube analyzed `forgetful-factory` on `main`, analysis
`d1c425f2-aa07-42bc-ab3f-c1a2b559318e`. The assigned **Sonar way sans code coverage** gate failed
on thirteen code smells: nine complexity findings and four repeated-literal findings. Twelve are
in files untouched by this task; the remaining connection-check complexity already existed, with
no branching changed here. No bugs, vulnerabilities or security hotspots were reported;
duplication was 0%. These wider Slice 4/5 findings remain open, not suppressed or fixed by this
narrow change. Scanner warnings include missing blame for uncommitted files and binary archive
encoding. Authentication used the shared envault aliases; no tokens were printed or stored.

Validation: 206 tests passed on each of Python 3.12 and 3.13, including native role loading without
inference. All 72 focused tests and seven rebuilt-wheel public regressions passed. Ruff, all three
import contracts and offline wheel/sdist builds passed. Mycelium 0.4.5 regeneration retained
44 boxes and its ten known external-base warnings; repeat export matched. FACTORY.md and the
protected Design questions were preserved. No live login, provider call or production onboarding
was performed. The Sonar gate failure above remains separate from these passing checks.

Independent Opus review found no blocking issues and passed 97 focused tests. It confirmed that
the two native calls use the same authentication path and project access remains user-scoped.
Its stale historical test description was corrected above. Scott clarified that agents may use
user-profile information to understand the user, unlike the discarded preflight response.
Foreman and feature-owner user-info instructions are intentionally retained. This change applies
only to init/watch; role procedures and existing installations are unchanged.

## Code-smell cleanup

The four repeated filenames now have local constants. Nine complex functions were shortened by
extracting resource-path checks, selection-file loading, Git worktree parsing, tool-catalog
validation, plan lookup/filtering and CLI input stages into named helpers. Checks, command order,
error messages and recovery rules are unchanged. No new dependency, architecture exception or
Sonar suppression was added. Agent user-info requests remain intact.

This was green/refactor/green using the existing public tests. The fresh Python 3.12 baseline and
implementation's final run each passed 206 tests, with native Pi loading enabled and no inference.
Focused runs passed 54 profile, 19 planning/watch, 9 setup and 76 CLI tests. The same tests were
used before and after; none were weakened or rewritten to fit the refactor.

SonarQube analysis `81b064fa-3bc7-4e87-936b-65c0cedb8c91` for `forgetful-factory` on `main`
passed **Sonar way sans code coverage**. All thirteen findings are resolved: zero open issues,
code smells, bugs, vulnerabilities or security hotspots; duplication remains 0%. The gate and
rules were not changed. Existing binary-archive encoding and missing-blame warnings remain.
Credentials were supplied through the shared envault aliases, without a repository manifest.

Ruff and all three import contracts passed. Offline wheel/sdist builds passed; 38 public
regressions passed against the rebuilt wheel's extracted contents, which matched source/resources.
Mycelium 0.4.5 produced one diagram with 45 boxes, including the new Git parser module container.
Repeat export matched byte-for-byte; the ten known external-base warnings remain. Source links
were refreshed in the architecture overview; component responsibilities and boundaries did not
change. The diagram was checked as Markdown, not rendered.

Evidence is under `/tmp/factory-smells-cleanup`. No protected documents, role skills, dependencies,
bundles, personal settings or credentials were changed. No live login or provider request was made.

The parent's final full runs also passed all 206 tests on each of Python 3.12 and 3.13, including
native role loading. Source hashes stayed fixed across the scan, package checks and test runs.

Independent Opus review approved the refactor and passed 59 focused tests with native loading
and no skips. Applying the recorded patch to the baseline reproduced the reviewed source exactly.
It found no introduced behaviour changes or blocking/medium findings. Three pre-existing coverage
gaps remain as follow-ups: owner-option conflicts on re-init, restart filtering of unrelated or
finished plans, and invalid child-role selections. They were not treated as behaviour changes in
this cleanup. Review evidence is in `/tmp/factory-smells-cleanup/review`.
