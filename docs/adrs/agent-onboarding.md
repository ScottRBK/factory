# Agent setup and factory maintenance

Status: numbered choices, maintenance guidance, init/watch exclusion, independent Pi research
settings and role-folder registration are implemented. Registration checks paths and consistency;
content validation belongs to the native harness. See the progress plan for current checks.
Assisted setup and watcher attachment remain unimplemented; broader apps need upstream changes.

Back to [architecture](../architecture.md).

## Why change onboarding

The Foreman model prompt accepted a number, but implementation/review prompts required typing
native app/model names. The worker-versus-planning-only question also obscured which settings
would be saved. Scott wants two understandable routes after setting up Foreman: configure each
remaining agent manually, or finish the configuration with Foreman's help.

Scott also wants a skill for setting up and maintaining the factory. Users should be able to put
skills in the appropriate role folder, or ask an agent to do that work, without manually maintaining
several resource lists.

## Implemented changes

Interactive Foreman model/effort and implementation/review app/model/effort choices use numbered
menus. Each number maps to the displayed native value; saved selectors remain exact. Command-line
flags still accept native values directly. Saved configuration, conflict handling, model catalog
caching and native-login consent are unchanged. Invalid or missing numbers stop setup clearly.
This does not introduce separate interactive owner/research menus. Owner flags retain their
existing behavior. Independent research model/harness/effort flags and TOML fields are now supported
for Pi; omit all three to retain owner-derived defaults. Research model discovery uses its role cwd.
Other known AgentShell apps report specific upstream limitations; they are not working new choices.

New factories provision and select `foreman/skills/factory-maintenance/SKILL.md`. Native role
instructions point to it, and its description lets Pi select it for setup and maintenance questions.
Its procedures cover choosing settings, preserving accounts and work, reconciling resources, and
rerunning public init. The skill distinguishes validated setup from successful inference.

The maintenance skill is required alongside Foreman's dispatch skill and AgentShell extension.
Existing edited `resources.json` files are preserved; if the new selection is missing, init/watch
name the required paths rather than silently changing selections. Re-init preserves edits to the
skill itself and existing AGENTS.md files, which may lack the new pointer. Pi can still advertise
the selected description. Pi or the chosen harness owns YAML parsing, metadata validation and
name-clash handling. Factory does not duplicate those rules, inspect ignore-file semantics or
require a discoverable native SDK. The proposed YAML parser dependency and compatibility code
were removed at Scott's request. Native loader tests cover valid bundled and local examples;
init success alone does not prove a skill loads or is advertised.

Init scans `<role>/skills/*/SKILL.md` for provisioned roles after checking existing selections.
It checks real, readable regular files before adding missing paths to resources and parent rosters.
Required guidance, external selections, file contents and saved TOML/comments are preserved.
Worker selections may include additional local files alongside their required configured skills.
Existing contradictory selections still need explicit reconciliation.

`.factory/agents/skill-registration.json` records only Factory's automatic additions and pending
before/after skill-list changes. Re-init removes missing automatic selections, registers renamed
paths and finishes interrupted writes only when the affected lists match recorded states. Parent
updates change only the affected child's skills, not the whole roster. Malformed receipts,
symlinks and conflicting edits stop recovery. Untracked older/manual selections remain manual.
Individual writes are atomic; the receipt makes a partial multi-file update retryable. Recovery
runs under the init lease after completion invalidation and before checking missing resources.

Init and watch now acquire the workspace lease at the CLI boundary, before configuration validation
or mutation. The lock also covers bootstrap/readiness checks and remains held through cleanup.
The existing workspace directory is locked even before `.factory` exists, with the original factory
lock retained when present for compatibility with running older watchers. No PID files are added.
A rejected init preserves the active setup receipt; a rejected watch cannot inspect partial setup.

Maintenance still requires confirmed-stopped delegated work. A watcher owns the Foreman session,
so that Foreman can gather choices but cannot stop itself and complete subsequent changes.
The user applies them from a separate session. The lease guards init/watch, not arbitrary agent
file edits or every native child process. Registration does not alter already-running selections.

## Agreed direction, not yet implemented

Replace the ambiguous interactive worker/planning question with manual setup or Foreman-assisted
setup after the Foreman is configured. Keep existing command-line compatibility separate from that
interactive experience. Manual setup should expose each remaining role's choices consistently.

### Setup Foreman and watcher attachment

Scott selected a dedicated tmux setup session. Init should launch Foreman after its own setup,
then take the user into that session. The watcher must not poll, restore issue work or dispatch
anything while delivery setup is incomplete. Both setup routes must save and validate the same
configuration; an agent must not manufacture completion receipts or remove readiness checks.

The maintenance skill should let Foreman start, check and stop its watcher through supported
Factory commands. Once setup is validated, the watcher connects to that same running Foreman;
the user should not have to close the setup conversation and start a second one. This brings
forward part of [Slice 8](../plan.md#slice-8-use-a-foreman-that-is-already-running). Initially,
only target Foreman launched by init; arbitrary-terminal discovery remains outside this phase.

Keep one watcher per workspace. Before attachment, verify the intended Foreman's terminal identity
and readiness; monitor its liveness while watching. A saved Pi conversation ID alone does not
identify a running terminal. Terminal attachment and notification delivery use AgentShell.
Stopping an attached watcher leaves Foreman running. Foreman exit stops the watcher without
launching a replacement. Keep the existing watcher-owned launch option and its cleanup behavior.

Scott explicitly removed live model, effort and loaded-resource verification from attachment.
Configuration validation belongs to setup and maintenance. The watcher still requires completed
saved setup, but does not inspect the running Foreman's current selections. Changing its model or
effort does not require reconnecting the watcher. Recorded launch settings are not live-state proof.

This needs launcher and lifecycle support as well as skill instructions. Init now takes the watch
lease, but the current controller still closes sessions it launches when its caller disconnects.
Command names, setup finalization, independent session ownership and any resource reload/restart
still need implementation design. Attachment cannot alter an already-running Foreman's model or
prove that it received a notification.

### Agent-local skills

Use `.factory/agents/<role>/skills/<skill-name>/SKILL.md`, preserving bundled role guidance and user
edits. The user can place files there or ask Foreman to help. Setup or an explicit refresh should
validate those files and update the appropriate selections, including parent roster entries, without
requiring the user to edit several JSON files. Do not silently change running agents' selections.
Tell the user where to put skills and when a reload or restart is required.

The init registration path and completion message are implemented. Copying alone still does not
activate a file: rerun init after stopping watching and delegated work. The native harness may
reject its contents on load; Factory must not claim otherwise. An independent refresh command
and changes to running agents are not implemented.

### Downstream apps and skill delivery

Foreman and feature-owner remain Pi. Beyond the feature-owner, research, implementation and review
should be limited by the apps AgentShell supports, not Factory's current Pi/Codex/Claude allowlist.
App launch support and selected-skill support are separate capabilities. Model discovery, effort,
native permissions and continuation must be checked for each supported app; do not guess selectors
or silently discard unsupported settings.

Factory selects the app and local skill files. The AgentShell extension forwards those selections.
AgentShell's per-app adapters are responsible for translating them into supported native mechanisms
or reporting unsupported capabilities. Missing native skill delivery belongs in AgentShell, rather
than new app-specific workarounds in Factory.

At the checked AgentShell 0.5.0 version, Pi accepts selected skill paths. The Codex adapter rejects
explicit skill resources; Claude Code accepts plugins/MCP but not the direct skills field. The
extension already forwards resources. Factory currently uses task-prompt reading instructions for
Codex/Claude skills; that must not be described as native skill loading. These adapter limits do
not establish that the apps themselves lack skills. Broader support needs upstream investigation
and validation; no upstream implementation or dependency upgrade is included in this decision.

No changes to personal agent preferences, native permissions, credential handling, Forgetful
project requirements, feature ownership or PR/CI responsibilities are part of this change.

## Pinned-contract findings

Source review covered AgentShell 0.5.0, bundled extension 1.4.1 and installed Pi 1.3.0. These are
version-specific limits, not claims about the latest releases or native apps in general.

- A launched Pi needs its owner process to remain alive. A separate long-lived Factory controller
  can retain ownership; borrowed attachment cannot transfer it. No such setup owner is implemented.
- Attachment exposes terminal controls, not readiness or agent exit. The owner can observe actual
  exit through public `terminal.wait()`; attachment must use that owner and its startup evidence.
  It need not observe current model, effort or loaded resources. Their absence from the public
  attachment API is not a blocker, and no live-settings observer is required.
- Automatic user entry requires native tmux client attachment/switching, distinct from notification
  delivery. AgentShell 0.5 has no client-focus method for a new session. Resolve that boundary
  before adding direct terminal commands; message delivery must continue through AgentShell.
- The extension requires nonempty roster effort. OpenCode and Cursor need effort omitted, so an
  optional-effort upstream change is required. Never invent a sentinel effort to pass validation.
- Pi and OpenCode accept selected skills in AgentShell; OpenCode's SKILL.md-file behavior still
  needs native validation. Other adapters need supported native translation before Factory can
  claim uniform skill delivery. All seven apps list models, but none exposes a public per-model
  effort catalog. No new app choices or native-delivery fallback were added in this pass.

Upstream changes require separate authorization and audited adoption. Until then, the independent
Factory changes above do not make assisted onboarding or all-app support complete.

## Validation boundary

Public init/watch tests use temporary repositories and controlled external commands. They check
number-to-selector mapping, invalid input, skill provisioning, selection and edit preservation.
An isolated native Pi loader checks that the maintenance skill is available for model selection;
it sends no model requests. These checks do not prove an agent follows the maintenance procedure.
Results and outstanding validation belong in [the progress record](../plans/agent-onboarding.md).
