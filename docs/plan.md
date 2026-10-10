# Plan for implementing

## Slice 1: initialize a factory

Status: implemented, independently reviewed, and locally validated. Review findings were fixed
and regression-checked; live GitHub validation remains separately gated.
See [architecture](architecture.md) for the implemented first-slice structure.

- [x] Package a `forgetful-factory init` command with interactive and explicit configuration.
- [x] Configure one or several local repositories, watched labels, Foreman model, and effort.
- [x] Validate configuration and access before creating missing GitHub labels.
- [x] Save `.factory/factory.toml`, preserve existing configuration, and support safe reruns.
- [x] Validate the packaged command locally through `uvx`; do not publish to PyPI in this slice.
- [x] Independently validate tests and the local initialization journey.
- [ ] Validate real GitHub label setup against repositories explicitly approved for that step.

Scott approved two public test boundaries: the initialization CLI and configuration loading.
Use TDD through those boundaries, temporary real Git repositories/files, and a substitute `gh`
executable for the external GitHub boundary. Do not mutate live GitHub repositories in ordinary
local tests. Live label validation in Dark Business is a separate confirmation step.

This slice does not poll, launch agents, create Forgetful plans/worktrees, or run a background
service. GitHub is the first work-tracking adapter behind provider-independent domain contracts.
Build dependency checks are recorded in [dependency audit](dependency-audit.md).

Local validation: 31 tests passed on Python 3.12.3, including timeout and interruption checks.
`uv build --offline --no-python-downloads` produced a wheel and source distribution. Independent
wheel-installed CLI validation passed for multiple repositories, existing-label preservation,
repeat initialization, argument conflicts, denied access, and invalid NUL-containing settings.
All GitHub calls in these local checks used substitute executables. They did not configure
Dark Business, mutate live GitHub labels, or publish the package.

The initial Unicode checks missed NUL characters that TOML can decode but OS APIs cannot accept.
A public-loader regression and CLI invalid-config case reproduced the traceback before the fix;
validation now rejects NUL characters before external calls. The independent review also reproduced
an invalid second label allowing an earlier label creation; the exact CLI case now asserts no GitHub
calls or mutations. The review's unsupported-provider diagnostic advisory was fixed test-first.
No other review blockers were reported.

### Repository configuration update

- [x] Match Scott's revised spec: repeat `[[repository]]` tables instead of a `repositories` map.
- [x] Expose ordered repository records through the public loader and update initialization.
- [x] Reject duplicate local directories and old or mixed formats before GitHub calls.
- [x] Give existing configs header-conversion guidance without rewriting their bytes.
- [x] Use the approved CLI/loader seams for RED→GREEN regressions; all 31 local tests pass.
- [x] Rebuild and validate the local wheel with substitute `gh`; no live label mutations.

## Test CI

- [x] Add `.github/workflows/ci.yml` to run the existing suite on every push, without filters.
- [x] Use `ubuntu-latest` with separate Python 3.11 and 3.12 jobs and no Python dependencies.
- [x] Add pull-request checks and cancel older runs for the same workflow and ref.
- [x] Audit official actions; use read-only permissions and no saved checkout credentials.
- [x] Replace commit pins with verified `v7` tags for compatible updates, at Scott's request.
- [x] Validate workflow YAML, triggers, concurrency, matrix, references, and test command.
  The latest separate local test run passed all 28 tests.
- [x] Verify both hosted jobs after the workflow and implementation are committed and pushed.

Action dependency advisories and limits are recorded in [dependency audit](dependency-audit.md).
Implementation committed and pushed as `2ee6e6b`; the push workflow passed on 2026-10-10.
[CI run 38041488129](https://github.com/ScottRBK/factory/actions/runs/38041488129) tested that exact
commit: all 28 tests passed on Python 3.11 (36.928 seconds) and Python 3.12 (37.253 seconds).
Local pre-commit validation also passed all 28 tests. PR-event execution and cancellation of
outdated runs have not been exercised on GitHub; a passing push run does not verify those paths.
Python 3.11 remains unavailable locally, but is now verified on the hosted runner.

## Later slices

- [ ] Build the Python watcher to notify the Foreman of new GitHub issues.
- [ ] Validate sending a watcher notification to the chosen Foreman Pi session while idle
  and busy. The watcher just sends a message; the Foreman deals with it from there.
- [ ] Validate identifying and reusing live feature-owner sessions after a Foreman restart;
  saved session IDs and AgentShell Job IDs alone do not prove an owner is still running.
- [ ] Create the Foreman skill with the agreed reference locations, dispatch/recovery rules,
  and deployment/E2E completion responsibilities.
- [ ] Create the feature-owner skill with the agreed reference locations, ownership/assignment
  rules, and implementation completion/CI responsibilities.
- [ ] Validate that post-merge deployment/E2E stages identify the tested application revisions,
  including the deployed combination for a multi-repository epic.

## Watcher implementation decision

- Use Python rather than Bash for the watcher; reuse the existing AgentShell installation.
- Use AgentShell's experimental interactive tmux host to launch the Foreman's Pi terminal once.
- Send subsequent notifications through `session.terminal.send_text(message, submit=True)`;
  do not launch a new Foreman for each notification or add custom queueing behaviour.
- For a user-selected, already-running Foreman, target its existing tmux pane. AgentShell does
  not currently expose a public attach-to-existing-Foreman API.
- Validate the real notification path with both idle and busy Pi sessions before relying on it.

## Design questions

Checked items record agreed decisions. Work through the remaining questions before implementation.

Default to the responsible agent's discretion unless `FACTORY.md`, an agreed decision below,
or the affected repository's instructions specify otherwise. Capture this default in the agent
skills; do not invent factory-wide templates, retry budgets, or extra subsystems for judgment calls.

### 1. Prevent duplicate work

- [x] How should repeated polls identify and reuse the existing plan for an issue?
  - Use the plan's `external_ref` to associate the issue with its existing Forgetful plan.
  - The field will be optional and unique per user; factory-created issue plans will supply it.
  - Forgetful enhancement: [issue #83](https://github.com/ScottRBK/forgetful/issues/83).
  - This prevents duplicate plans, not duplicate running agents.
- [x] Who is responsible for ensuring only one feature-owner runs for an issue?
  - The Foreman is the sole dispatcher of feature-owners; the watcher only notifies the Foreman.
  - Before launching another owner, the Foreman checks the existing assignment and running job.
  - Repeated issue notifications should reach the existing owner rather than launch another.
- [x] How should the feature-owner's session be recorded?
  - Both the Foreman and feature-owner must be Pi agents.
  - The scaffold includes a feature-owner ownership/setup task.
  - The feature-owner reads its own `PI_SESSION_ID` and records it as `assigned_agent` when
    claiming that task in Forgetful, before starting feature work.
  - Forgetful's version-checked claim prevents competing claims from both succeeding.
  - The Foreman receives an AgentShell Job ID at launch and can read the owner's native session
    ID from the task assignment. Job IDs and native session IDs are different identifiers.
  - A stored session ID is not proof that the owner is still running.
- [x] How should an existing plan identify and reuse its worktrees?
  - For a single-repository issue, the watcher creates the initial worktree when scaffolding
    the plan and records its repository, branch, and path in the ownership task description.
  - For an epic, the feature-owner identifies affected repositories and coordinates a dedicated
    branch/worktree per repository, recording repository-to-branch/path mappings in that task.
  - On subsequent notifications, the Foreman reuses the recorded worktrees.
  - If a recorded worktree is missing or belongs to another branch, stop and report the problem
    rather than silently recreate it.
- [x] Should repository plus issue number be the common identifier across the factory?
  - Use `github:<owner>/<repo>#<issue-number>`, for example `github:ScottRBK/factory#42`.
  - Use this identifier as the plan's `external_ref` and in factory notifications and logs.
  - Session IDs and worktree paths remain separate references.
- [x] How should the watcher avoid duplicate watcher or Foreman sessions during startup?
  - For MVP, let the user choose which existing watcher or Foreman instance to use.
  - If existing instances are detected, present them for selection rather than launch another.
  - If an instance's status is uncertain, report that rather than automatically replace it.
  - Never stop or replace an existing instance without the user's permission.
  - Starting an additional factory instance is not an offered startup option.
- [x] How should a restarted Foreman rediscover an existing owner or recover a failed launch?
  - Read the ownership task to find the recorded feature-owner session.
  - Reuse the owner if it is still running.
  - Automatically resume or relaunch after confirming the owner stopped or launch failed;
    the Foreman does not need user approval for this recovery.
  - If the owner's status is uncertain, report that and do not launch a duplicate owner.
  - A claimed task without a running owner remains visible as unfinished work.
- [x] When is the ownership/setup task completed, and how should abandoned claims be handled?
  - Treat this as an "Own this feature" task, not just a setup task.
  - Keep it `doing` while the feature is underway; complete it when the feature is complete.
  - If the owner stops, the Foreman recovers ownership automatically.
  - Release the old claim for a replacement only after confirming the previous owner stopped.

### 2. Task states and assignment

- [x] Who claims the feature, and how does the feature-owner assign tasks in Forgetful?
  - The feature-owner claims the ownership task using its own Pi session ID.
  - The feature-owner assigns implementation and review tasks in Forgetful, passes the work
    through agent prompts, and updates task state from their reports.
  - Implementation agents do not claim tasks or use Forgetful themselves.
- [x] How do we distinguish waiting for clarification from waiting for review?
  - Use the existing `waiting` state when a task cannot proceed, recording the reason in its
    description rather than introducing new task states.
  - Review has its own task: `todo` before it starts and `doing` while the reviewer works.
  - Clarification requests record the question and where the reply is expected, such as GitHub.
- [x] When should an implementation task be marked completed?
  - The implementation agent finishes the assigned changes, runs local tests, and owns the
    CI feedback and correction loop for its exact commit.
  - It reports the commit, test results, and CI run link after the required checks pass.
  - The feature-owner verifies that evidence before marking the task `done`.
  - Unavailable CI or unresolved failures are reported as blockers, not completion.
  - Review and merge remain separate tasks.
- [x] When should the overall plan be marked completed?
  - Only after the change is merged, deployed to E2E, and passes E2E verification.
  - The feature-owner finishes its work after merge; the Foreman keeps the plan open until
    deployment and E2E verification succeed.
- [x] Where should we record the issue URL, PR URL, worktree path, and agent session references?
  - Issue URL: plan `source_url`; canonical issue identifier: plan `external_ref`.
  - PR URLs: plan `context`, identifying the repository for each PR in a multi-repo epic.
  - Repository-to-branch/worktree-path mappings: ownership task description.
  - Native agent session ID: corresponding task `assigned_agent`; keep AgentShell Job IDs
    separate from native session IDs.
  - Encode these conventions in both the Foreman and feature-owner skills.

### 3. Concurrency and Git responsibilities

- [x] Should implementation agents run sequentially within one repository worktree?
  - Leave sequential versus parallel implementation to the feature-owner's judgment.
  - The feature-owner is responsible for coordinating concurrent edits and Git operations.
- [x] When should parallel implementation across separate repositories be allowed?
  - The feature-owner decides based on task dependencies and shared API contracts.
  - Independent repository work can run in parallel; dependent work follows the plan's ordering.
- [x] How should multi-repository epics be managed?
  - Use one umbrella GitHub issue, one feature-owner, and one shared Forgetful plan.
  - Put the plan under the umbrella workspace's Forgetful project, such as Dark Business.
  - Apply the watched factory label only to the umbrella issue, not any child issues.
  - Use repo-specific implementation, review, merge, deployment, and E2E tasks within the same
    plan so Forgetful's same-plan dependencies can represent cross-repository ordering.
  - The feature-owner coordinates each repository's worktree, branch, PR, and merge order.
  - Cross-repository merges are not atomic; intermediate deployed versions must stay compatible.
  - The Foreman verifies the deployed revision of every affected application and the joined-up
    E2E journey before the epic plan completes.
  - Encode this coordination model in both the Foreman and feature-owner skills.
- [x] Who commits, pushes, creates PRs, merges, and cleans up?
  - Implementation agents commit and push their changes, including fixes.
  - The feature-owner creates PRs, coordinates merges, and cleans up worktrees and branches.
  - The feature-owner coordinates Git operations when multiple implementation agents share
    a worktree.
- [x] Who triggers CI after implementation and review fixes, and who checks its results?
  - The implementation agent triggers/checks CI and fixes failures for its exact commit,
    both after initial implementation and after review fixes.
  - The feature-owner verifies the reported evidence and retains control of review and merge.

### 4. Completion, failure, and recovery messages

- [x] What information should an agent return when it succeeds?
  - Implementation and review agents respond naturally, identifying the relevant task IDs.
  - No mandatory response wrapper, schema, or fixed report template is required.
  - The receiving Foreman or feature-owner verifies completion from the response and available
    evidence; the implementation/CI completion requirements still apply.
- [x] How should an agent report that it needs clarification or is blocked?
  - Implementation and review agents explain the problem naturally and include the task IDs.
  - The feature-owner records affected tasks as `waiting` and passes questions requiring user
    input to the Foreman; implementation and review agents do not update Forgetful.
- [x] Should we use AgentShell results, structured console signals, or a combination?
  - Use AgentShell's normal returned responses; no special structured console signals.
  - The feature-owner interprets implementation/review responses and updates Forgetful.
  - The Foreman interprets feature-owner responses and handles its own coordination tasks.
- [x] What should happen when an agent crashes, times out, or stops responding?
  - After confirming an agent stopped, the feature-owner checks saved work, then resumes or
    relaunches it for the same task using the existing worktree.
  - A timeout or silence is not proof of exit; check whether the agent is still running and
    do not start a replacement while its status is uncertain.
  - Preserve the worktree and changes, and escalate repeated failures to the Foreman.
  - The Foreman follows the same approach when recovering a feature-owner.
  - Retry and escalation decisions use agent discretion, subject to explicit repository rules.
- [x] How should a restarted factory discover and resume unfinished work?
  - Use Forgetful as the durable record; the Foreman loads unfinished factory plans, including
    plans whose GitHub issues closed at merge but still await deployment/E2E verification.
  - Read task states, assignments, PR links, and worktree mappings, then check current GitHub
    and agent status before continuing.
  - Reuse running owners, recover confirmed stopped owners, and avoid duplicates when status
    is uncertain.
  - The watcher reuses existing plans through `external_ref` rather than scaffolding them again.
- [x] How should work remain pending when the Foreman is busy or unavailable?
  - The watcher simply sends a message to the existing Foreman Pi session; the Foreman deals
    with it from there. No custom watcher queue or busy-session coordination is required.
  - Validate this notification path with an idle and a busy Foreman; it is not yet tested.
  - If the session is unavailable, the plan remains pending in Forgetful and restart recovery
    rediscovers it. Do not assume session messages survive a restart.
- [x] How should clarification replies from GitHub and direct user input reach the feature-owner?
  - Follow `FACTORY.md`: the watcher informs the Foreman of GitHub issue changes, or the user
    replies directly to the Foreman; the Foreman passes the update to the existing feature-owner.
  - Agents decide how to interpret the reply and resume affected tasks.
- [x] Does the Foreman need live steering of an already-running feature-owner for MVP?
  - No. If an update arrives while the feature-owner is busy, the Foreman waits for the run
    to return, then sends the update through `subagent` with the returned `resume_session_id`.
  - Clarification requests return control to the Foreman; replies resume the same conversation.
  - Never resume concurrently with a still-running process using that session.
  - Optional future enhancement: [live messaging for running Pi subagents][live-messaging].

[live-messaging]: https://github.com/ScottRBK/pi-agentshell-extension/issues/7

### 5. Correction limits and final-commit checks

- [x] Which review findings block progress, and which are advisory?
  - The reviewer assesses findings; the feature-owner decides the response using the agreed
    requirements and repository rules. No additional factory-wide severity scheme is needed.
- [x] How many review rounds and review-fix passes should be allowed?
  - The feature-owner uses discretion, respecting any explicit repository review limits.
- [x] What limits should apply to CI correction attempts and waiting for checks?
  - The implementation agent uses discretion and reports unresolved blockers to the
    feature-owner; no fixed factory-wide attempt or timeout budget is imposed.
- [x] When should repeated failures or lack of progress be escalated to the user?
  - The feature-owner escalates to the Foreman, who decides when user input is needed.
- [x] Which checks must pass before a PR can merge?
  - The feature-owner follows repository-required checks and the agreed implementation/CI
    completion rules, deciding any additional validation appropriate to the change.
- [x] How do we verify that check results belong to the exact final commit being merged?
  - Implementation agents provide exact-commit CI evidence; the feature-owner verifies it
    against the final PR head before merge. Older green results are not sufficient.
- [x] Should ADRs and other documentation be committed before the final validation pass?
  - `FACTORY.md` requires ADRs before merge. Include them in the final commit's required
    validation; the feature-owner chooses the working sequence without bypassing that check.

### 6. Safe cleanup

- [x] How do we verify that no agent or process is still using a worktree before removing it?
  - The feature-owner chooses the checks, but must confirm the worktree is no longer in use.
- [x] How do we verify that the worktree is clean and its changes are pushed and merged?
  - The feature-owner chooses the checks and follows repository cleanup rules. Preserve the
    worktree if clean, pushed, and merged status cannot be established.
- [x] What should be retained when implementation, merge, or cleanup fails?
  - The feature-owner uses discretion while preserving unfinished work and useful evidence.
    Failure is not permission to discard changes.
- [x] Who reports retained worktrees and decides when they can be cleaned up?
  - The feature-owner reports retained worktrees to the Foreman and decides when safe cleanup
    is possible, subject to repository rules and any required user permission.

### 7. Evidence and visibility from the demo

- [x] Should UI changes require screenshots of every affected screen?
  - The feature-owner decides appropriate UI evidence, subject to repository requirements;
    there is no factory-wide requirement to screenshot every screen.
- [x] Should PRs use a standard body containing requirements, changes, and validation evidence?
  - The feature-owner chooses useful PR content and follows any repository template; no new
    factory-wide PR template is required.
- [x] Should the factory generate before/after architecture diagrams for structural changes?
  - The feature-owner decides when diagrams are useful, respecting repository documentation
    requirements; they are not mandatory for every structural change.
- [x] Should a branch preview be available before merge, and who manages its lifetime?
  - The feature-owner decides whether an existing preview capability is useful and manages
    its lifetime. The factory does not require a new preview-hosting subsystem.
- [x] Should code-analysis feedback, such as SonarCloud findings, be part of the correction flow?
  - The feature-owner uses relevant existing analysis and follows repository gates; no new
    factory-wide analysis service is required.
- [x] Should agent costs be recorded per feature?
  - The Foreman decides what existing cost information is useful to report; no mandatory
    cost-tracking subsystem is required.
- [x] Is a progress dashboard needed for MVP, or are Foreman updates sufficient?
  - The Foreman chooses useful progress updates using available tools; a separate dashboard
    is not an MVP requirement.

### 8. Post-merge deployment and E2E completion

- [x] Does feature completion mean merged, or deployed and E2E-verified?
  - Deployed and E2E-verified, not just merged; the Foreman owns this final verification.
- [x] How should Forgetful represent implementation completion versus deployment verification?
  - The feature-owner chooses the task breakdown using existing Forgetful states. Keep
    deployment/E2E verification work explicitly open until the Foreman confirms success;
    completing implementation tasks must not auto-complete the whole plan prematurely.
- [x] How does the Foreman identify the deployment and E2E run for the exact merged revision?
  - Deployment and E2E execution are stages in the post-merge CI/CD workflow, with E2E running
    after deployment. The Foreman checks that merge revision's workflow run and stage results.
  - For multi-repository epics, correlate each repository's merge/deployment evidence and
    verify that the joined-up E2E stage tested the required deployed combination; one workflow
    run's source commit does not identify every application's deployed revision.
- [x] What should happen if deployment or E2E checks fail, time out, or never start?
  - `FACTORY.md` requires a follow-up GitHub issue for deployment/E2E failures, with the original
    plan left open. The Foreman uses discretion for diagnosis, waiting, and escalation when a
    run is delayed, missing, or inconclusive; those cases are not verification success.
- [x] How should a restarted Foreman resume monitoring an outstanding deployment?
  - Use the agreed Forgetful/GitHub restart recovery. The Foreman records sufficient deployment
    references with the unfinished verification task and rechecks live GitHub state on restart.
- [x] How should follow-up issues link to the original issue, plan, and failed run?
  - The Foreman includes the original issue, Forgetful plan, affected repositories/revisions,
    and relevant failed-run links, choosing a natural issue description rather than a template.
- [x] How do we avoid creating duplicate follow-up issues for the same failure?
  - The Foreman checks existing follow-ups and reuses an issue covering the same failure;
    it chooses the lookup approach without introducing another deduplication subsystem.
