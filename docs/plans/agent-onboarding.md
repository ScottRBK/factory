# Agent onboarding improvements

## Implemented

- Consistent numbered Foreman model/effort and implementation/review app/model/effort menus.
  Native selectors are preserved exactly; command-line flags still accept native values.
- Selected, model-invokable Foreman `factory-maintenance` skill. New factories reference it in
  AGENTS.md; existing instruction files remain unchanged. The skill explains current setup/repair
  steps and stopped-session requirements, without overriding
  user edits, native permissions, accounts or readiness checks.
- Missing maintenance selections stop with correction guidance; re-init preserves edited skills.

[Design and limits](../adrs/agent-onboarding.md).

## Initial numbered-menu and maintenance validation

Public-boundary RED-to-GREEN checks reproduced numeric input failures and missing maintenance
provisioning. Additional cases cover all eight agent-choice prompts, invalid numbers/text,
repository catalog intersection, exact saved selectors, missing selections and preservation.
They use temporary repositories and controlled external commands, not real accounts or services.
Review follow-up adds a pre-maintenance resource fixture (not a historical executable) and a Pi
worker skill-update test, including the owner's embedded roster selection.

- Python 3.12.3: final 250 tests passed in 307.051 seconds.
- Python 3.13.5: final 250 tests passed in 304.884 seconds.
- Native Pi SDK checks enabled on both runs, with no skipped tests or inference requests.
  The loader confirms the maintenance skill is advertised from its selected local path.
- Ruff and all three import-boundary contracts pass.
- Offline wheel and source-distribution builds pass using the existing reviewed toolchain.
- Mycelium 0.4.5 map regenerated; repeat export matches. Mermaid checked as text, not rendered.

Opus found no blocking findings. Its independent checks included 109 focused tests on both Python
versions, native Pi loading, and a separate init probe using the actual baseline source. Follow-up
corrections spell out the Pi-worker parent-roster edit and prohibit init inside the watcher-owned
Foreman. Readiness checks paths, not whether edited frontmatter still advertises a skill.
Opus rechecked those corrections, the fixture and native loading on both interpreters: all five
findings resolved, with no material issues remaining in that pass.

The full Foreman terminal smoke has updated expected resources but was not rerun for this change.
No live maintenance, model access or autonomous agent behavior was tested. No personal settings or
DinoLand files were changed by this implementation.

## Independent groundwork implemented

The next implementation pass completed these parts without adding upstream workarounds:

- Init/watch exclusion before configuration reads or mutations, including readiness receipts.
  Existing watcher directory locks remain honored; fresh init does not create `.factory` just
  to acquire its workspace lock.
- Independent Pi research model/harness/effort flags and saved fields. Existing configurations
  retain owner-derived defaults. This is not the pending manual menu for every role.
- Init registration of role-local skills into resources and parent rosters, preserving content,
  required selections and existing TOML/comments. File paths are checked; YAML, metadata and name
  resolution are left to the native harness.
- Maintenance guidance and completion output explain registration and restart/reload limits.
  Known unsupported apps report their native/roster constraints, not a working new launch choice.

Implementation validation: 260 tests passed on Python 3.12 with four native tests skipped; all four
passed separately with the supplied native SDK. Fourteen focused tests also passed on Python 3.13.
Ruff and all three import contracts passed. Independent Opus review found registration bugs:
deleted skills and interrupted writes could block retries, a research-model typo could poison
setup, and content checks disagreed with Pi. The earlier green suite did not cover those cases.

Scott subsequently decided that YAML and skill-name validation belong to Pi or the selected
harness. Factory's attempted YAML parser, compatibility logic, parser dependency and differential
parser tests were removed. Public init regressions instead check unchanged path registration,
including headers the harness may reject. Factory must not claim that setup validates skill content.

Recovery fixes retain only automatic-selection ownership and bounded pending list changes. Tests
cover removal/rename, partial-write retry, conflicting manual edits, malformed receipts, symlinks,
manual selection preservation and research typo correction. Owner/research flag conflicts now
preserve readiness and fail before external calls. Final validation of this simplified version
is recorded below.

A separate isolated probe used real AgentShell 0.5/tmux with fake Pi and a private socket. Borrowed
text submission reached that process; disconnect preserved it and owned cleanup removed it. The
probe confirms transport/lifetime only, not live Pi settings or autonomous behavior.

### Validation after removing Factory-side content validation

- Public init regression was RED with Factory YAML checks, then GREEN after their removal.
  Headerless, malformed and alias-containing content is forwarded unchanged for the harness.
- Python 3.12: 35 focused setup/registration/recovery tests passed, then eight maintenance/native
  checks passed. Python 3.13: the combined 39 focused/native tests passed, with no skips.
- Native checks used isolated Pi/AgentShell loading and fake child processes, without inference.
- Ruff, all three import contracts, offline lock and whitespace checks passed.
- The dependency manifest and uv lock match their pre-parser bytes. The parser was uninstalled
  from both test environments; no replacement dependency was added.
- The architecture map was regenerated and its repeat export matched. Mermaid checked as text.

These are targeted checks, not a fresh full-suite, hosted CI or autonomous-agent result. The earlier
review's content-validation findings are superseded by the native-harness boundary, not claimed
fixed by another parser. The simplified recovery changes have not had a fresh independent review.

## Follow-up: add skills after agent setup

DinoLand testing exposed that numbered worker setup still asked for a mandatory TDD path. The
folder-registration tests started with explicit skill flags, so they missed this user journey.
Scott confirmed that onboarding should omit skill questions and show each agent's skill folder,
with the option to ask Foreman for help.

Implemented: init ends the worker questions after app/model/effort choices. A separate TDD file is
optional; bundled implementation guidance still requires TDD. Existing explicit skill flags,
saved selections and file checks remain supported. Completion lists only provisioned role folders
and explains adding `<skill-name>/SKILL.md`, rerunning init with work stopped, and restart limits.
The maintenance skill now gives the same advice. Existing edited role instructions are preserved.

Validation:

- Public init regression failed at the old TDD prompt before the change, then passed with input
  ending immediately after review effort. Maintenance guidance also demonstrated RED-to-GREEN.
- Regression checks cover optional saved TDD values, explicit-skill compatibility, partial worker
  configuration rejection, planning-only output, and post-setup drop-in registration for Pi and
  Codex workers without manual TOML/JSON edits. Existing retry and preservation checks remain.
- 56 focused/native tests passed. Both full suites passed all 275 tests: Python 3.12.3 in 322.915
  seconds and Python 3.13.5 in 326.303 seconds. Native checks were enabled, with no skips/inference.
- Ruff, all three import contracts, whitespace checks and offline wheel/source builds passed.
- Mycelium map regenerated; same-map repeat export matched. Mermaid checked as text, not rendered.

Opus approved with no correctness findings; it independently ran 34 focused tests. Follow-up
reflowed one line, documented the optional saved `tdd_skill` setting and added standalone-setting
cases to the public loader regression. No production Python changed after the full runs. The final
38 focused/native checks passed on both Python versions after those guidance/test edits.

No hosted CI, live onboarding, autonomous skill use or Sonar scan was performed for this follow-up.
No dependencies, personal settings or DinoLand files changed.

## Next phase: assisted setup, attachment and skills

Status: assisted setup and same-Foreman watcher connection are implemented, reviewed and locally
validated. Broader app support remains separate; existing resource/effort capabilities are not
absent.
The earlier 250-test evidence covers the numbered-menu/maintenance pass only. Detailed boundaries
and contract findings are in the
[onboarding ADR](../adrs/agent-onboarding.md#assisted-setup-and-remaining-work).

- [x] Replace the worker/planning-only question with manual or Foreman-assisted setup after
  configuring Foreman. Manual setup should expose each remaining role, including research.
- [x] Launch the setup Foreman in a dedicated tmux session and take the user into it. Do not start
  issue processing while configuration is incomplete.
- [x] Let that Foreman start, check and stop a watcher connected to its own running terminal.
  Reuse the conversation instead of launching another Foreman. Bring forward the required
  [Slice 8 attachment work](../plan.md#slice-8-use-a-foreman-that-is-already-running), initially
  for init-launched Foreman rather than arbitrary terminal discovery.
- [x] Require completed saved setup and verify the intended Foreman's terminal identity,
  readiness and liveness. Do not inspect its current model, effort or loaded resources; those
  are setup/maintenance concerns. Keep one watcher per workspace. Stopping an attached watcher
  leaves Foreman running; Foreman exit stops its watcher. Preserve owned-session launch separately.
- [x] Register role-folder paths and recover removal/rename or interrupted updates without
  overwriting custom edits. Leave YAML, metadata and name resolution to the native harness.
  Retain `.factory/agents/<role>/skills/<skill-name>/SKILL.md` and init as the entry point.
  No standalone refresh or live-selection update is implemented.
- [ ] Keep Foreman and feature-owner on Pi, but remove Factory's three-app restriction for research,
  implementation and review. Check each app against the installed AgentShell capabilities.
- [x] Recheck released AgentShell capabilities. Latest Python release 0.5.0 already supports
  selected resources; extension 1.4.2 retains mandatory roster effort. Pi/OpenCode accept skill
  paths; Claude/Copilot/Cursor accept native plugins that can bundle skills. Codex/Grok adapters
  reject nondefault explicit resources. Current Factory prompt-reading is not native loading.
  No upgrade or upstream change was made. Audit any dependency adoption.

Scott removed the proposed live-settings check from attachment. No such observer or verification
was implemented. A long-lived owner can supply startup/exit evidence; attachment needs terminal
identity, readiness and liveness, not inspection of current model/effort/resources. Launch settings
remain distinct from live state. Upstream permission and native skill-delivery work remain separate.

Both setup routes must save and validate the same configuration. Preserve plans, worktrees,
custom resources and native login state. A maintenance skill cannot bypass incomplete setup or
silently change a running agent's selections. The implemented init/watch routes, receipt-last
finalization and explicit reload/restart rules are described in the onboarding ADR.

### Lifecycle implementation and review

The design review simplified the first integration to reuse the setup owner's existing AgentShell
connection. A connected watcher borrows delivery through that controller, rather than launching a
second AgentShell helper. General terminal attachment remains later work. The existing completion
receipt is the final setup gate; runtime-roster publication happens before it, with no second
pending-setup receipt. All canonical role files remain editable and preserved.

A fresh pre-change baseline passed 275 tests on Python 3.12 in 306.784 seconds, with native SDK
checks enabled and no skips. Source/test hashes stayed unchanged during that run. This is baseline
evidence, not validation of the lifecycle implementation now in progress.

Independent contract probes used real AgentShell 0.5.0, fake Pi and a private tmux server. They
confirmed startup events, captured target identity, borrowed disconnect survival, refusal of a
changed target and actual process exit. A tmux pane can retain its identity after Pi exits, so pane
existence alone is insufficient. Separate client probes verified outside attachment and inside
switching; shell-invoked inside attachment produced a nesting warning. No model/backend calls ran.
A later integration fixture exercised the real Pi SDK's session reload without inference, alongside
fake-Pi transport tests. Finalization and later child-skill registration changed the roster while
preserving the SDK session ID, process and selected top-level Foreman paths. This is not a live
model conversation or proof that an agent follows setup guidance.

The first frozen implementation passed all 293 tests on Python 3.12 in 360.852 seconds. Python 3.13
ran the same suite but had ten fixture errors: this build does not expose `os.pidfd_open`, although
the host libc provides it. No tests are being skipped; test-only descriptor handling is being fixed.

Opus reproduced two lifecycle defects despite the targeted green tests: known failed launches could
leave an unretryable owner state, and a send exceeding AgentShell's timeout could close the
persistent Foreman. Earlier tests covered explicit uncertain records and short stalls, not these
real failure paths. Review also found a missing workspace in Foreman's status instruction, early
model-catalog path checks and malformed-message handling. Public regressions now cover all five
findings, including a real AgentShell send held beyond five seconds. Interpreter preflight prevents
known failed starts from recording launch intent; confirmed cleanup permits retry while actual
owner loss remains uncertain. Protocol errors fail cleanly, and runtime commands name the workspace.

The corrected freeze passed all 306 tests on both runtimes, without skips: Python 3.12 in 407.715
seconds and Python 3.13 in 400.407 seconds. Native SDK checks were enabled with no inference. Ruff,
all three import contracts and offline wheel/source builds passed. Packaged sources and tests
matched the checkout. Those results do not close the review: Opus then reproduced a missing case
where closing the Foreman pane left its owner alive in an unknown state. That repair and explicit
failed-send recovery guidance were completed in the next reviewed pass.

The exact SDK source showed that simply closing after a failed wait could kill a live Pi. The fix
pins the original live pane worker, revalidates it against AgentShell's captured target, and
observes
its exit without signals. Transient query failure preserves ownership; paced SDK wait continuation
can still observe a later real Pi exit. Worker-only exit ends ownership with unknown state, not a
fabricated successful stop. Tests cover closed panes, transient queries, invalid capture and slow
cancellation. Fixtures now capture their owner's live handle before readiness and assert cleanup.

Final validation of that freeze:

- Python 3.12.3: **311 tests passed in 434.227 seconds**.
- Python 3.13.5: **311 tests passed in 427.592 seconds**.
- Native Pi SDK checks enabled, with no skips or model/backend requests.
- All 102 source/test hashes matched before and after; no new surviving owner processes remained
  after the full runs. Thirteen independently identified abandoned current-phase fixture owners
  from earlier failed runs were cleaned through verified live handles; older runs were not swept.
- Ruff and all three import contracts passed. Offline wheel/source builds passed; all 66 packaged
  source/resource files matched the checkout, as did source-distribution tests and README.
- Mycelium 0.4.5 regenerated one 53-box diagram; a repeat export matched byte-for-byte. The overview
  and ADRs were refreshed. Ten external-base warnings and same-name call heuristics remain
  documented.
  Mermaid was checked as text, not rendered. Protected intent, decisions and dependency files match.

Opus's final review found no blocking findings. It independently ran 40 focused tests on each
interpreter and public native reproductions for pane, session and server loss, including a running
watcher with preserved setup receipt. Previous interpreter, send, workspace and protocol fixes still
passed. No identifiable review-repro workspace retained an owner. It checked the actual SDK FIFO
ownership caveat and the validated-handle solution; no source edits occurred during review.

Remaining limitations are explicit: unsupported pidfd capture retains uncertain ownership, transient
query failure blocks watching until deliberate exit/relaunch, and failed delivery is never replayed
automatically. Unknown stopped-owner recovery requires independent confirmation before archiving
only
its generated owner/socket records. Native fixtures prove lifecycle, transport and SDK reload, not
that a real model follows instructions. No live assisted setup, autonomous delivery, hosted CI or
Sonar scan ran. No dependencies, bundles, personal settings or DinoLand data changed.

### CI native-test prerequisite

The lifecycle regressions now use real tmux, an existing Factory runtime requirement. CI explicitly
installs it from the runner's configured Ubuntu archives, records candidate policy and checks its
version. No new action or Python dependency was added. The job timeout is now 15 minutes: the prior
hosted baseline was already near the old ten-minute limit, before these additional native tests.

The read-only prerequisite audit was completed before adding that step. Cached package pages
reported 3.4-1ubuntu0.1; a fresh signed Noble-updates index instead resolved 3.4-1ubuntu0.2. The
parent verified the InRelease signature with the installed Ubuntu archive keyring, then matched the
compressed package index's SHA-256 and size to that signed release. The current package retains the
five native dependencies reviewed: libc, libevent-core, libsystemd, libtinfo and libutempter. The
official changelog's new patch prevents notification of uninitialized clients (LP 2169164).

Ubuntu's cached security assessment reported Noble unaffected by CVE-2026-11623; the direct advisory
refresh timed out. No blocking finding was identified in this bounded prerequisite audit, but it is
not certification of all runner libraries. No package was installed or executed during the audit.
APT must retain archive signature verification; no PPA, new key or authentication bypass is added.
Unpinned Ubuntu archive resolution and runner images remain mutable and outside this point-in-time
check. The explicit step ensures availability, not identical package bytes across future CI runs.

The native fixture uses pidfds to observe and signal only its own processes. On Python builds that
omit the wrappers it uses typed libc functions, requiring glibc 2.36 or newer; Ubuntu 24.04 supplies
those functions. This fallback is test-only and does not change production dependencies.

Sources: [signed release][tmux-release], [current changelog][tmux-changelog],
[archive verification][ubuntu-verification] and [Ubuntu advisory][tmux-advisory].

[tmux-release]: https://archive.ubuntu.com/ubuntu/dists/noble-updates/InRelease
[tmux-changelog]:
  https://changelogs.ubuntu.com/changelogs/pool/main/t/tmux/tmux_3.4-1ubuntu0.2/changelog
[ubuntu-verification]:
  https://documentation.ubuntu.com/security/software-integrity/archive-verification/
[tmux-advisory]: https://ubuntu.com/security/CVE-2026-11623

### Setup wording follow-up

Scott approved replacing "Setup route choices" with "How would you like to set up your factory?"
Each numbered option explains what happens; input asks "Select 1 or 2:". Selection and validation
behavior are unchanged. Earlier tests checked only the option names, so missed the missing context.
The public init regression now checks the approved menu text, alongside EOF and invalid choices.

The wording assertions failed before the change. Afterward, 77 init, assisted-setup, worker,
maintenance, project and shared-Pi tests passed on Python 3.12, without skips. Ruff and all three
import contracts passed. The detailed map was regenerated and its repeat export matched; overview
line references were refreshed. The earlier full-suite/review results apply to the preceding freeze;
this wording follow-up did not rerun full native lifecycle suites or use a live model.

### Skill guidance and manual launch follow-up

Implemented Scott's approved completion text: show a copyable init command, explain preserved
choices and setup rechecks, and say new skills load on future agent starts/restarts. Manual setup
also prints its watch command and offers `Launch factory now? [y/N]:` only with terminal input.
The init lease is released before launch. Yes starts ordinary watch and its issue-scope choice.
Decline, EOF and cancellation leave completed setup intact. Piped Yes cannot start a watcher.

Assisted setup, finalization and a live/uncertain setup owner do not get the CLI offer. Foreman's
maintenance skill says it starts the watcher in the same conversation after validation and explicit
user reload, using the agreed issue scope. Existing custom guidance is not overwritten.

Public CLI regressions first failed for the new skill text, absent launch offer, and misleading
EOF/Ctrl-C diagnostics. They then passed with a real terminal input, real AgentShell/private tmux,
fake Pi and external-command fixtures. Tests execute copied init/watch commands from another cwd,
including quoted workspace names, and preserve setup state and the selected interpreter. Original
resource, settings and lifecycle assertions remain; obsolete output assertions track approved copy.

Independent review found no blocking findings and passed all 51 focused tests. It also reproduced
an ordinary init rerun with a live setup Foreman and confirmed no launch offer or replacement.
Its minor relative-path finding led to a failing copied-command test, then absolute-path handling
without resolving the virtualenv executable symlink. Bare names retain PATH lookup. The docs note
that printed uvx interpreter paths depend on the cache remaining available.

Final source/test freeze: **319 tests passed on Python 3.12 in 423.214 seconds**, with native SDK
checks enabled and no skips. All 103 source/test hashes matched before/after, with no new surviving
owner processes. An earlier full run was interrupted by an accidental Escape and is not counted.
Seven focused launch tests passed after the relative-path correction. Ruff and all three import
contracts passed. The 53-box Mycelium map was regenerated; a repeat export matched byte-for-byte.
Python 3.13 was not rerun for this follow-up. No live model/backend trial or hosted CI ran.

The independent follow-up approved the relative-path fix and passed all seven launch tests.
A parent smoke check also passed with both input and output on a real terminal: Yes, new-only,
watcher readiness, baseline and Ctrl-C cleanup, all using fake Pi with no inference. Offline wheel
and source builds passed; all 66 packaged source/resource files, tests and README matched checkout.
The default isolated build could not resolve its backend from the local index cache, so validation
reused the existing pinned uv-build 0.8.0 archive with build isolation disabled. Its files matched
its RECORD hashes; no installation, download or dependency change was made.

### Validation boundaries and remaining trial

The completed checks use public init/watch boundaries and isolated no-inference native fixtures.
They prove incomplete setup blocks polling/restoration, connection uses the intended terminal,
duplicates and stale targets are refused, watcher stop preserves Foreman, and known Foreman exit
stops watching. They also cover path registration and resource/roster preservation. No-dispatch
instructions and correct agent behavior are not proved by those fixtures.

A live assisted-setup or delivery trial remains separate. Agree its repository and native
permissions before use, including idle/busy delivery and agent use of explicit reload. Attachment
does not inspect current model/effort/resources. Broader downstream app integration still needs
its own exact-selector, effort and native-resource tests; it is not part of this completed phase.
