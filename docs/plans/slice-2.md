# Slice 2: watch issues and notify Pi

Back to the [implementation plan](../plan.md).

Status: implemented, locally validated, and independently reviewed by Opus. Review advisories
about user messages were fixed and regression-checked; operational follow-ups are deferred.

## Scope

- Load the repositories and watched labels from `.factory/factory.toml`.
- Poll GitHub for matching issues; honour `*` as watch-all and exclude pull requests.
- Notify new matches only after the startup choice; changes to already-seen issues are deferred.
- Launch one new Pi session through AgentShell's interactive tmux runner.
- Forward issue notifications through that AgentShell session; no direct tmux calls in the factory.
- Connecting to an already-running Pi session is deferred.
- Use the configured Foreman model and effort when launching; defer role-specific profiles.
- Reuse that session for subsequent notifications; do not create a session per issue.
- Allow one watcher per workspace; reject a concurrent second watcher before launching another Pi.
- Validate delivery while Pi is idle and busy. Pi handles the submitted message naturally;
  do not add a custom notification queue or busy-session coordination.
- Report polling and delivery failures clearly; submitting a message is not proof Pi acted on it.

This slice does not scaffold plans, create worktrees, dispatch feature-owners, or implement Foreman
behaviour. Profiles, role tools/skills, hide-tools setup, and Forgetful wiring come later.
Do not implement role-specific tool configuration in this slice.

## Implemented flow

```text
load factory configuration and validate options
acquire the workspace watcher lease
choose existing matches or new matches only, then show the startup attachment hint
launch a new Pi session through AgentShell and wait for its session-start event
repeat
  read matching open issues from each distinct work source
  on read failure, report and retry that source next poll
  for new-only startup, baseline each source's first successful read
  submit unseen matching issues through the same AgentShell session
  remember successfully submitted issue IDs
  wait until the next poll, stopping if Pi exits
on exit, close owned Pi and release the lease
```

Keep GitHub polling behind the work-tracking service and terminal delivery behind an application
port. Adapters handle `gh` and AgentShell; the application coordinates the watch loop.
Launch Pi through AgentShell's tmux runner and send through
`session.terminal.send_text(message, submit=True)`. Terminal interaction stays in AgentShell;
no factory-owned tmux commands or existing-pane fallback. The host still requires tmux at runtime.
Implementation uses host-installed `gh`, Pi, and tmux. The package now declares AgentShell 0.4.0
as a runtime dependency, so `uvx` installs it automatically into the factory environment.
A separately selected AgentShell interpreter remains an optional override, not a prerequisite.

Notifications include the repository, issue number, title, and URL, not the issue body. Treat issue
content as external input, not factory instructions.

## Agreed decisions

- [x] For slice 2, support launching a new Pi session only, entirely through AgentShell.
  - Existing-session support is deferred to [AgentShell issue #25][existing-session].
- [x] Prompt at startup: forward existing matching open issues, or watch for new matches only.
  - For new matches only, use the initial results as a baseline without sending notifications.
- [x] Keep issue-update notifications out of slice 2. Consider updates, including changes made
  while stopped, in slice 3 when the Foreman's tools are introduced.
- [x] Poll every 30 seconds by default; allow an override with `--interval`.
- [x] Remember notified issue IDs in memory, not on disk; record them after successful submission.
  - The new-matches-only startup choice seeds the seen set from the initial results.
  - Restarts use the startup prompt; durable update/restart tracking is deferred.
- [x] Use `forgetful-factory watch` to launch Pi and start polling.
- [x] Retry failed GitHub reads on the next poll; do not treat a failure as an empty result.
- [x] Stop with a clear error if delivery to Pi fails; do not silently replace the target.
- [x] Send repository, issue number, title, and URL; leave the body out for this slice.
- [x] Preserve the earlier no-duplicate-instance rule with a per-workspace watcher lock.
  - A concurrent second invocation reports the existing watcher rather than launching another Pi.
  - Existing-session discovery/selection still belongs to the later AgentShell attachment slice.

## AgentShell integration constraints

Scott's final decision is AgentShell-only delivery, with new-session launches for slice 2.
Passing a Pi session ID reopens a conversation in a new process, not the already-running terminal.
Existing-session attach/send support is requested in [AgentShell issue #25][existing-session] and
belongs to a later slice, not a prerequisite for the current new-session path.

[existing-session]: https://github.com/ScottRBK/agent-shell/issues/25

### Launch lifecycle

Inspection of the existing AgentShell checkout found that its interactive tmux launcher owns the
Pi process lifetime. When the controller exits, AgentShell stops that process; it does not provide
a public detach operation. This constraint applies to the new-session path in this slice.

The watcher owns its newly launched Pi session and closes it when the watcher stops. This follows
AgentShell's current lifecycle and was called out before implementation. Independently running Pi
sessions remain untouched; detached operation is not part of this slice.

Initial validation used a separate source-checkout environment because the system's AgentShell
0.1.11 lacked the interactive API. Scott subsequently requested the latest published release and
then a factory dependency. AgentShell 0.4.0 supplies the API; the factory now requires Python 3.12+
and installs AgentShell through its package metadata. No checkout path is required.

## Validation

Scott approved TDD through the public watcher command, using temporary configuration, a substitute
`gh`, and substitute terminal delivery, followed by real isolated tmux checks.

- Configured repositories, concrete labels, wildcard labels, and issue-only filtering.
- Pagination, multiple local copies of a work source, and empty results.
- Repeated polls, new matches, startup choices, and no notifications for already-seen issue edits.
- Polling errors, delivery failures, and clean interruption without silent loss or false success.
- A second watcher cannot launch another Pi; stopping the first releases the workspace lock.
- Real Pi delivery in isolated tmux sessions while idle and processing a message.
- Repeated notifications reach the same newly launched session, not new agents.
- Slice 1 regressions stay green; ordinary tests make no live GitHub mutations.

### Completion checks

- [x] Implement using RED→GREEN cycles through the approved test boundary.
- [x] Pass watcher tests, slice 1 regressions, and local packaged-command validation.
- [x] Verify the real idle/busy Pi notification journey in isolated tmux sessions.
- [x] Run local SonarQube analysis and inspect the resulting findings and quality gate.
- [x] Send the implementation to Opus for independent review after implementation and scanning.
- [x] Fix review findings with regression tests; rerun tests and SonarQube after fixes.
  - Opus found no blockers; its three misleading-message advisories were corrected.
- [x] Update architecture and plan with implemented behaviour and actual validation evidence.

## Validation evidence

- The implementation agent recorded 11 observed RED→GREEN rounds through the approved public CLI
  seam, from the missing watch command through matching, baselines, failures, and startup deadlines.
  The master added a further RED→GREEN regression for exclusive workspace ownership.
- Public CLI tests cover matching, pagination, startup choices, per-source first-success baselines,
  duplicate work sources, literal external data, unavailable interpreters, bounded waits, dead Pi,
  EOF, interruption, cleanup failures, and exclusive watcher ownership.
- The workspace-lock regression first failed because two watchers launched, then passed after
  adding the lease. It also proves stopping the first watcher permits a later fresh launch.
- Python 3.12: 54 tests passed after all review fixes in 124.8 seconds.
- Python 3.11: the same 54 tests passed in 124.5 seconds.
- Further RED→GREEN checks corrected two misleading diagnostics: a Pi exit pending during a GitHub
  read was labelled a cleanup failure, and readiness timeouts suggested attaching to the old session
  after shutdown. The tests previously covered each failure separately but not exit timing during
  polling, and checked trust-help keywords rather than whether the suggested action was still valid.
- Offline wheel/source-distribution builds passed. Fresh-cache wheel-installed watch journeys
  passed on Python 3.11 and 3.12 with substitute GitHub/AgentShell and a separate interpreter.
- Real public watch journey: three substitute GitHub issues reached one real AgentShell-owned Pi.
  Issue 1 was acknowledged while idle; issue 3 arrived while Pi's Bash tool ran `sleep 8` and was
  acknowledged. The final run used session `01a1273a-763f-7198-99ae-ff373725b16b` and exited 130
  on interruption; its owned tmux session was removed. No live GitHub calls or changes were made.
- The initial SonarQube scan found two complexity findings and one cancellation-propagation
  finding. Behaviour-preserving refactors fixed them without changing the approved test boundary.
  The final analysis (`5ef68468-66b0-4a37-968c-d3c88548ecda`, main, 2026-10-10 19:11 UTC)
  passed `Sonar way sans code coverage`:
  zero open issues, bugs, vulnerabilities, hotspots, code smells, and duplication. Aggregate
  cyclomatic/cognitive complexity was 218/211. Coverage is not a gate condition.
- Opus reported no blockers. Its review passed all 52 then-current tests on Python 3.12; its
  Python 3.11 run was interrupted, so the independent master runs provide that version's evidence.
  All three message advisories were corrected: rejected second watchers no longer prompt or print
  phantom attach commands; pending Pi exits are not labelled cleanup failures; startup timeouts
  advise retrying and using the new startup hint rather than attaching to the old session.
  The exclusive-lock test first failed on the phantom hint, then passed after startup choice and
  reporting moved inside the lease. The exit-before-send reproduction also has explicit coverage.
- No commit, push, publication, live GitHub mutation, or Dark Business watcher launch was performed.

### Packaged AgentShell follow-up — 2026-10-13

- Scott requested AgentShell as a runtime dependency and removal of Python 3.11 CI testing.
- Added `agent-shell-py==0.4.0`; raised the factory minimum to Python 3.12, matching AgentShell.
  CI now tests Python 3.12/3.13 and installs the package before running tests.
- The isolated old-wheel check failed with `ModuleNotFoundError: agent_shell`; after rebuilding,
  isolated `uvx` environments imported the required AgentShell APIs on Python 3.12 and 3.13.
- Fresh-cache wheel-installed watcher validation passed without `--agentshell-python`, using only
  external GitHub/AgentShell substitutes. Existing CLI regressions now exercise that default too.
- All 54 tests passed on Python 3.12 in 124.7 seconds and Python 3.13 in 124.6 seconds.
- SonarQube's `Sonar way sans code coverage` gate passed, with zero open findings, zero new
  violations, and 0.0% new duplicated lines. The local scanner now targets Python 3.12/3.13.
- README now shows plain `watch`; the interpreter override remains optional. This follow-up has
  not been committed, pushed, or verified on hosted CI. No further live Pi/model calls were made.

## Operational follow-ups

- Investigate AgentShell's Pi event-log growth upstream before relying on days-long sessions:
  streamed updates include full partial messages. This was identified by source inspection, not
  measured live. Do not implement factory-side rotation through private SDK paths.
- Revisit polling for repositories with many open issues: provider-side label queries and quota
  handling may be needed. Current reads fetch every open-issue page under the 30-second timeout;
  very small user-selected intervals can exceed quotas.
- Opus reproduced controller SIGKILL handling: the watcher stops with a clear error and AgentShell's
  owner pipe stops Pi. Regular tests cover EOF and catchable signals, not that exact kill scenario.

## Deferred agent-profile work

The profile proposal uses `.factory/agents/foreman/` and `.factory/agents/feature-owner/`, selected
with `PI_CODING_AGENT_DIR`. Scott specified standard Pi tools plus the role
capabilities in `FACTORY.md`. Resource isolation, credential reuse, and profile-aware AgentShell
launches belong to a later slice. Forgetful's extension and CLI/skills or MCP arrangement is being
worked through separately; do not assume a transport switch or build a competing integration here.
