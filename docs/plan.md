# Implementation plan

Factory implements setup, issue planning, owner/worker coordination, agreed completion checks and
automatic cleanup. The [current status](#current-status) separates implementation, verified results
and remaining work. Earlier slice records retain the evidence for their original revisions.

This document covers the work order. The [architecture overview](architecture.md) explains the
code structure. The [design decisions below](#design-questions) record the agreed behaviour.

The approved issue-change correction and local evidence are tracked in
[issue change notifications](plans/issue-change-notifications.md).

## Completed slices

### Slice 1: set up a factory

Choose the repositories and GitHub labels to watch, then save the factory configuration.
Implemented and reviewed; live GitHub label testing remains a separate check.
[Details and test results](plans/slice-1.md).

### Slice 2: send new issues to Pi

The watcher checks GitHub and sends matching issues to one Pi session started through AgentShell.
Delivery was tested while Pi was idle and busy. Sending a message does not prove Pi processed it.
[Details and test results](plans/slice-2.md).

We also added automatic code-style and architecture checks, locally and in CI.
[Quality checks](plans/quality-checks.md).

### Slice 3: set up the Foreman and Forgetful

Closed on 2026-10-16 after Scott's DinoLand trial.

- Reuse the user's Pi login with permission, and choose the Foreman's model.
- Set up editable Foreman skills/extensions and native Forgetful CLI access, locally or to a server.
- Ask before installing missing tools. Block the watcher if setup is incomplete.
- Let the Foreman discuss incoming issues. Later slices added automatic planning and feature-owners.

Tests, packaging, local smoke checks, SonarQube and independent review passed.
Those checks did not establish live token refresh or fresh-host installation. Later installation
evidence is recorded under [current status](#current-status).
[Current results and limits][trial-feedback]. The [original record](plans/slice-3.md)
includes earlier MCP and separate-login choices that no longer apply.

## Current status

Core setup, issue planning, owner/worker coordination, DoD agreements and completed-plan cleanup
are implemented. Agent guidance governs delivery and completion; Python does not interpret the
DoD or prove that a model followed it. Existing factories are not automatically migrated.

### Confirmed results

- **Hosted CI:** [push run 44640083122][current-ci] passed for `454c210` on Python 3.12 and 3.13.
  Both jobs passed package verification, lint, import contracts and tests: 648 tests each,
  639 passes and nine skips. Test times were 798.740 and 782.815 seconds respectively.
  This proves that revision's push checks, not PR-event behaviour, deployment or E2E.
- **CI correction:** `b7e5f33` fixed the obsolete permission-guidance assertion. Its own 3.13 job
  timed out; the later run above passed.
  [Details](plans/ci-test-runtime.md#current-hosted-results).
- **CI job limit:** docs-only commit `1364cbb` (run 45049755719) hit the 15-minute limit on both
  Pythons while tests still passed. The suite had grown to use most of the limit. The parallel
  test runner is implemented locally; hosted CI is not yet verified.
  [Parallel runner](plans/ci-test-runtime.md#parallel-runner).
- **DinoLand installation:** cleanup revision `337d02c` was installed and its watcher/owned
  Foreman restarted with approval. Package bytes, 17 installed-package tests, preserved settings
  and live startup were checked. This establishes installation and readiness, not a complete
  deployment/E2E trial.
  [Rollout record](plans/cleanup-performance.md#dinoland-installation-and-restart).
- **Cleanup:** fair three-set batches, cycle-local discovery reuse, fresh selected-plan checks and
  durable receipts are implemented. The isolated unchanged-CLI trial took 50.455 seconds versus
  112.445 seconds for three sets. This is one local measurement, not a latency guarantee.
  [Validation](plans/cleanup-performance.md#final-parent-validation-and-cleanup).
  Plan records (receipt version 2) let a cycle with no open completed plan stop after one plan
  list call. Local tests only; not yet run in a live factory.
  [Plan records](plans/cleanup-performance.md#plan-records-and-the-plan-list-fast-path).

### Remaining work

- Verify the full live DoD workflow, including required deployment/deployed E2E evidence,
  failure handling and restart recovery. Installation or a successful merge alone is not this proof.
- Verify the parallel test runner on hosted CI for its exact commit, on both Pythons, three runs.
- Add general selection of an already-running Foreman. The setup-owned connection already works.
- Revisit CLI-backed Foreman extension calls and local SQLite extension support. Local Factory
  planning already works through the native CLI; the extension currently needs a server.
- Settle the documented memory capture/source-URL policy and explicit runtime-repair behaviour.
  One approved installation does not introduce an automatic upgrade or repair mechanism.
- Prepare a package release. No release is recorded. The corrected licensing wording does not
  impose an internal-use-only restriction; retain applicable notices when distributing code.
- Split the package into domain contexts (ticketing, forge, planning, workspace, agents, runtime,
  channels) with their own ports and adapters. See the [domain contexts
  plan](plans/domain-contexts.md); slices 0–6 and both reviews are done.

### Recent delivered changes

- [Memory settings](plans/memory-settings.md) for issue #5: Foreman's `forgetful.json` takes the
  extension's own settings, such as `context_limit_tokens` and `logging`, with the extension's
  rules. Factory refuses only the keys it sets and unknown keys. `init` leaves out `model` when
  none is chosen.
- [Role-resource update](plans/role-resource-update.md) adds `forgetful-factory update` for
  issue #4. It replaces unedited bundled resources from earlier releases, refuses edited files
  unless `--force` backs them up, and preserves agent definitions. The bundle now carries
  `pi-forgetful` `d9a7c98` with the private-task compaction, summary-reply and 404-rejection
  fixes.
  `update` no longer takes `--delegated-work-stopped`; it checks the lease and Foreman state
  only. It installs a changed AgentShell runtime lock unless `--no-install-role-runtime`. Live
  factory updates are Scott's next step. Removal of files that a bundle drops is deferred.
- [Issue and comment notifications](plans/issue-change-notifications.md) ignore timestamp-only
  changes while retaining planning-relevant content and paginated comments.
- [Watcher observation](plans/watch-status.md) distinguishes live process state, lifecycle phase
  and readiness. Its historical baseline wording failure was corrected by `b7e5f33`; an older
  intermittent shutdown timeout still has no proven cause or fix.
- [Reviewer and Foreman guidance](plans/agent-onboarding.md) covers original requirements,
  maintainable code, concise updates and the difference between reload and restart.
- [Research working directories](plans/slice-7.md#research-cwd-guidance-correction) preserve role
  instructions; implementation/review still run in their assigned worktrees.
- [Issue context bounds](plans/issue-plan-placeholder.md),
  [GitHub CLI readiness](plans/github-cli-readiness.md),
  [problem isolation](plans/watcher-problems.md) and
  [watched-label consent](plans/foreman-issue-intake.md) are implemented. The linked records retain
  their original validation scope and failures.
- [Normalized definitions](plans/agent-definitions.md), [onboarding](plans/agent-onboarding.md) and
  [server memory integration](plans/foreman-memory.md) are implemented. Settings and edited local
  resources require deliberate maintenance; installing a wheel does not update running agents.

[current-ci]: https://github.com/ScottRBK/factory/actions/runs/44640083122

## Current and next slices

### Slice 4: create a plan and working copy for each issue

- Create one Forgetful plan per issue, with a task recording who owns the feature.
- For a single-repository issue, create a branch and worktree (a separate working copy).
- Save their details in Forgetful before notifying the Foreman.
- Notify the Foreman when an issue changes. Reuse the plan and worktree after failures or restarts,
  rather than creating duplicates.

Init lets you select an existing Forgetful project or create one. It suggests the workspace name
and asks before creating. A project is required for planning. Init always checks connection and
planning access before completing setup; no extra flag is needed. The watcher and agents use the
same Forgetful login and project. Browser sign-in is allowed during setup and attended watching;
cancellation or failure leaves saved work available for retry.

An issue carrying the additional `epic` label leaves repository and worktree selection to its owner.
Other issues get an initial worktree in their source repository, using native Git commands.
No worktree extension is required.

[Forgetful 0.5.5][published-plan-model] includes the unique issue reference (`external_ref`). Its
bundled-installer upgrade passed the dependency audit. Setup checks the selected local backend
or remote server; updating the bundled CLI does not upgrade an existing server.

The approved [placeholder fix](plans/issue-plan-placeholder.md) removes full issue bodies from
new plan context without truncation. Live notifications retain the full body. Owner guidance now
requires a full provider read before plan enrichment and keeps human planning in goal/tasks.
Public watch regressions pass, including the real context limit, Unicode serialization,
closed/new-only recovery and old full-snapshot compatibility. No live DinoLand repair was attempted.

### Slice 5: let a feature-owner plan the work

The Foreman starts one feature-owner for an issue. That agent manages the feature's tasks.

- Give it its own model, skills and instructions, using the shared Pi login and Forgetful instance.
- Use the grill-me skill to ask for missing details, then resume the same conversation with answers.
- Break the feature into tasks. For work spanning repositories, prepare each branch and worktree.
- Record the owner's session. Reuse it while running; recover stopped owners without starting
  duplicates when their status is uncertain.

Scott has added research agents to `FACTORY.md`. The feature-owner can delegate fact-finding while
using the unchanged grill-me skill. Research agents report back to the owner; implementation and
PR review follow the implemented Slice 6 responsibilities below.

The audited AgentShell extension 1.5.0 supports normalized child references and role resources.
Factory provisions and selects them. Native role `AGENTS.md` files provide the coordinators'
instructions. Existing edited guidance is preserved or requires explicit reconciliation.
Owner delegation needs Pi's root maximum depth to be at least 1; Factory must not silently change
that shared preference. See the [profile limits](adrs/agent-profiles.md).

For a busy owner, wait for its run to finish before resuming with updates. A missing job record is
not proof that its process stopped. Keep work pending when the owner's status is uncertain.

### Slice 6: implement, review and merge

Implemented and locally tested; see [validation and remaining checks](plans/slice-6.md).
Owner guidance requires actual changes and tests in the plan, not just workflow stages. It proceeds
when requirements are clear, unless repository rules require explicit plan approval. A controlled
full-workflow trial still needs an agreed repository, required workflows and native permissions;
existing live use does not by itself validate every delivery and recovery path.
Scott's updated `FACTORY.md` assigns PR creation to implementation, so PR-triggered CI can run.
Required checks still must pass before implementation is complete; no draft-only rule is imposed.

- Set up the implementation and review agents' models, tools and skills.
- Implementation agents make changes, run tests, open or reuse PRs and fix CI for their commits.
  Owner guidance now uses `auto_approve=true` for implementation, including review fixes. Codex
  bypasses its sandbox and approval prompts; research/review are unchanged. Repository gates and
  Codex resume safeguards remain. See the
  [policy follow-up](plans/slice-6.md#implementation-launch-policy).
- The feature-owner verifies PRs and CI evidence, arranges one review per repository PR and sends
  findings back for fixes. It accepts implementation's fix report after required exact-final-commit
  CI passes, without another review pass. It updates Forgetful; workers do not.
- Include architecture decision records and check the final commit before merging.
- For multiple repositories, merge in a compatible order. The earlier Slice 6 cleanup guidance is
  historical: new 7A roles retain resources and hand back to Foreman. Keep required checks and
  ownership open until Foreman verifies the agreement; excluded checks need no placeholder tasks.

### Slice 7: agree completion, verify evidence, then clean up

DoD setup/guidance, cleanup receipts, fair three-set rotation and stop handling are implemented.
The [original local validation](plans/slice-7.md#parent-final-local-validation) retains its baseline
failure and host limits. Later batching checks, installation and hosted CI are recorded under
[current status](#current-status); they do not prove the full live DoD verification workflow.

[Slice 7A](plans/slice-7.md#7a-local-implementation) implements first-setup selection/confirmation
of
plain Markdown at `.factory/definition_of_done.md`, or a real Foreman discussion. Existing files and
one-time-init behaviour are preserved; there is no silent merge-only default or policy parser.

- The DoD is a project/programme agreement, separate from plan acceptance criteria; both must be
met.
- Foreman guidance reads it before planning/completion, supplies it to owners and requires explicit
  user decisions about changes to open plans. Presets are starting points, not an exhaustive enum.
- The owner records merged revisions and handoff evidence. Foreman owns final completion, even for
  merge-only work. Deployment/E2E are required only when agreed. Missing/stale required evidence
  blocks completion; excluded checks create no unfinished placeholder tasks.
- Existing closed-issue/restart recovery, owner-liveness and uncertain-delivery boundaries remain.
- Watch independently discovers full completed plans and safely removes recorded worktrees and
  local/remote feature refs, including dirty/ignored content and extra commits. Native state drives
  partial retries/restart recovery; closed/new-only intake and GitHub failures do not hide cleanup.
  Save evidence elsewhere first. Resource names remain reserved until durable cleanup confirmation.
  Preserve cleanup receipts; confirmed sets are not deleted again, and recorded plans are not
  read again. DinoLand adoption is recorded above; automatic migration of other factories is not
  provided.
- The [cleanup ADR](adrs/completed-plan-cleanup.md) records shared identity checks, target_branch,
  conflict isolation and explicit review of older completed mappings before enabling this version.
- Automated tests check setup/recovery, not model compliance. One independent review and the final
  parent SonarQube scan are complete; implementation owns the fixes. The full live DoD verification
  trials remain unverified, including deployment/E2E, failure and restart. Installation is not that
  validation.

### Slice 8: use a Foreman that is already running

The first integration lets init launch a persistent setup Foreman, which can start, check and stop
its watcher without leaving the conversation. It uses the owner's held AgentShell connection;
independent lifecycle/reload validation and review are recorded in the
[onboarding plan](plans/agent-onboarding.md). Selecting arbitrary running terminals remains
later work.

- Keep the option to start a new Foreman.
- Confirm the selected terminal is the intended Foreman, is ready, and remains alive.
  Setup and maintenance validate configuration; attachment does not inspect live model,
  effort or loaded resources.
- Leave an existing Foreman running when the watcher stops. Stop a Foreman the watcher started.
- Test delivery while idle and busy. Report missing or stopped sessions without replacing them.

AgentShell [0.5.0 supports attachment][agentshell-release]; [issue #25][attach] records the
upstream discussion. Factory's setup-owner integration does not use arbitrary-pane attachment.
Connection cannot change an agent's settings or prove receipt; see the
[attachment docs][attach-contract].

### Slice 9: Discord channel (implemented; live check pending)

Plain `watch` starts a Discord relay child. It posts 🟢 and 🔴 (with the stop reason) and every
Foreman reply, so a stop is seen away from the machine. Allowed users can write to the Foreman
from Discord, and a restart counts the messages that came while watch was off. Tests use fake
Discord and fake AgentShell; a check on a real Discord server is still to do. See the
[decision](adrs/discord-channel.md), the [work plan](plans/discord-channel.md) and the
[discord.py audit](plans/discord-py-audit.md).

### Later slice: CLI-backed Foreman extension and local Forgetful support

The extension currently uses server HTTP. A later slice may move its planning, recall and capture
calls onto the native Forgetful CLI used by Factory. This transport change is deferred. Local setup
initializes or reuses `.factory/data/forgetful.db`; it does not start an HTTP server. Both CLI
callers must use that same database/project, or the same server/project when in server mode.

- Preserve server support, setup preferences and Foreman-only resources; agree authentication
  reuse during that later design. Separate authentication remains the current approach.
- Replace the local-extension warning with supported local behavior only after validation.
- Test local/server routing, existing database reuse, fixed projects, background login, saved-work
  isolation, uncertain saves and local startup cost through supported interfaces.
- Determine any minimal upstream CLI changes from demonstrated gaps; the earlier broad list is
  not an approved prerequisite for the server-first slice.
- Keep migration and live adoption separate; do not create a second backend or silently start a
  server for a local factory. See the [memory work plan](plans/foreman-memory.md).

## Other follow-ups

- README cleanup keeps setup, commands and safety warnings in the introduction. Detailed contracts
  and validation history stay in the ADRs and work records; missing operator details are retained
  there. This changes documentation only, not runtime behaviour or release status.
- Foreman delegation guidance now defaults to handing feature work to owners/workers. Direct work
  requires explicit user instruction in Foreman's conversation; blocked delegation is not permission
  to take over. Public setup and native loading checks pass without claiming model compliance.
  See the
  [decision](adrs/agent-definitions.md#foreman-delegation-guidance) and
  [validation](plans/agent-definitions.md#foreman-delegation-follow-up).
- Normalized agent definitions: implemented and independently reviewed. Each agent owns one
  `agent.json`; parent rosters reference it rather than duplicate model/resources. Factory retains
  its settings and a Foreman pointer. Init provisions the team once; Foreman launch/attach is
  separate. Native SDK checks pass. The uv upgrade and runtime repair decision are tracked in the
  [work plan](plans/agent-definitions.md) and [decision](adrs/agent-definitions.md).
- Agent onboarding: numbered choices, maintenance guidance, init/watch exclusion and separate Pi
  research settings are implemented. Setup no longer asks for skill paths; it lists configured
  agents' skill folders and offers Foreman's help. Selected-root readiness checks validate portable
  required-guidance paths; YAML, metadata and skill loading remain native harness concerns.
  Manual/assisted setup and a persistent setup Foreman with connected watcher are implemented.
  Manual completion now offers terminal-only launch and copyable commands; assisted Foreman starts
  its own watcher. Connection checks identity, readiness and liveness, not live agent settings.
  Broader downstream apps remain separate. AgentShell already supports skills/plugins and effort;
  narrower adapter/optional-roster-effort gaps need individual treatment. See the
  [work plan](plans/agent-onboarding.md) and [design boundaries](adrs/agent-onboarding.md).
- Explain the remote Forgetful `/mcp` URL more clearly during setup.
- Personal AGENTS/append instructions can still apply. Model listing during setup can also read
  personal SYSTEM instructions. Role AGENTS loading does not provide full profile isolation.
- Check log growth during days-long runs, and GitHub request limits for large repositories.
- Docker remains a possible later investigation; no container work is planned.

Older status notes in the protected Design questions section describe their original slice.
The summaries above give the current implementation status. The protected section's earlier
assignment of PR creation to the feature-owner is superseded by Scott's updated `FACTORY.md` and
the Slice 6 summary above; the protected section is preserved as requested.

[trial-feedback]:
  plans/cli-onboarding.md#trial-feedback-clearer-consent-prompt-exclusion-and-python-selection
[agentshell-release]: https://github.com/ScottRBK/agent-shell/releases/tag/v0.5.0
[attach]: https://github.com/ScottRBK/agent-shell/issues/25
[attach-contract]:
  https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/examples.md
[external-ref]: https://github.com/ScottRBK/forgetful/issues/83
[published-plan-model]:
  https://github.com/ScottRBK/forgetful/blob/v0.5.5/app/models/plan_models.py


## Design questions

Checked items record agreed design decisions, not implemented features. The slice statuses above
state what is shipped. Resolve the remaining per-slice choices before implementation.

Default to the responsible agent's discretion unless `FACTORY.md`, an agreed decision below,
or the affected repository's instructions specify otherwise. Capture this default in the agent
skills; do not invent factory-wide templates, retry budgets, or extra subsystems for judgment calls.

### Watcher implementation decision

- Use Python rather than Bash for the watcher. Package AgentShell as a runtime dependency so
  `uvx` installs it automatically; require Python 3.12+ and test 3.12/3.13 in CI. Slice 2 used
  0.4.0; shared-login resource selection now pins audited 0.5.0.
- Use AgentShell's experimental interactive tmux host to launch the Foreman's Pi terminal once.
- Send subsequent notifications through `session.terminal.send_text(message, submit=True)`;
  do not launch a new Foreman for each notification or add custom queueing behaviour.
- Factory currently launches a new Pi session only. All terminal interaction goes through
  AgentShell; do not add direct tmux delivery. Upstream attachment shipped in 0.5.0; proposed
  Slice 8 integrates it while preserving the different owned/borrowed cleanup contracts.
- Validate the real notification path with both idle and busy Pi sessions before relying on it.

### 1. Prevent duplicate work

- [x] How should repeated polls identify and reuse the existing plan for an issue?
  - Use the plan's `external_ref` to associate the issue with its existing Forgetful plan.
  - The field will be optional and unique per user; factory-created issue plans will supply it.
  - Forgetful [issue #83][external-ref] is implemented upstream but absent from published 0.5.4;
    verify the backend/version before implementing this dependency.
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
  - Slice 2 launches new sessions only and rejects a concurrent second watcher for the workspace.
    AgentShell 0.5.0 now supports attachment; Factory discovery/selection is still unimplemented.
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
  - Slice 2 validated submission to the same new Pi session while idle and busy through AgentShell.
    Slice 3 adds discussion-only Foreman guidance; feature coordination remains future work.
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
  - One independent review per repository PR. After findings return to implementation, accept its
    reported fixes when required exact-final-commit CI passes; do not repeat reviewer or owner code
    review. Resumed sessions retain this limit. CI corrections remain allowed. Escalate unresolved
    blockers or conflicting repository review requirements to Foreman; do not bypass approvals,
    repository gates, deployment or E2E checks.
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

Historical Slice 6 decisions below describe the previous owner-led cleanup. The approved
[Slice 7 cleanup contract](plans/slice-7.md#cleanup-contract) replaces that authority at 7B rollout.
New roles do not delete resources. Completed-plan watcher cleanup is now implemented locally;
existing edited guidance and older mappings still need explicit adoption/reconciliation. No live
rollout was performed. The historical decisions below do not override completion-driven disposal.

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

The historical universal deployment/E2E answers below are superseded by the
[agreed DoD](adrs/completion-agreement.md): both feature acceptance criteria and the user-confirmed
project/programme agreement must be met. Required deployment/E2E retain the revision/evidence checks
below; excluded checks need no tasks. Foreman owns completion for every agreement, including
merge-only.

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
