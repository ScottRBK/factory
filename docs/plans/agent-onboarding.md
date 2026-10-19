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

## Next phase: assisted setup, attachment and skills

Status: partially implemented as listed above. Assisted setup and same-Foreman watcher attachment
still need implementation. Broader app support needs upstream work. The earlier 250-test evidence
covers the numbered-menu/maintenance pass only. Detailed boundaries and contract findings are in the
[onboarding ADR](../adrs/agent-onboarding.md#agreed-direction-not-yet-implemented).

- [ ] Replace the worker/planning-only question with manual or Foreman-assisted setup after
  configuring Foreman. Manual setup should expose each remaining role, including research.
- [ ] Launch the setup Foreman in a dedicated tmux session and take the user into it. Do not start
  issue processing while configuration is incomplete.
- [ ] Let that Foreman start, check and stop a watcher connected to its own running terminal.
  Reuse the conversation instead of launching another Foreman. Bring forward the required
  [Slice 8 attachment work](../plan.md#slice-8-use-a-foreman-that-is-already-running), initially
  for init-launched Foreman rather than arbitrary terminal discovery.
- [ ] Require completed saved setup and verify the intended Foreman's terminal identity,
  readiness and liveness. Do not inspect its current model, effort or loaded resources; those
  are setup/maintenance concerns. Keep one watcher per workspace. Stopping an attached watcher
  leaves Foreman running; Foreman exit stops its watcher. Preserve owned-session launch separately.
- [x] Register role-folder paths and recover removal/rename or interrupted updates without
  overwriting custom edits. Leave YAML, metadata and name resolution to the native harness.
  Retain `.factory/agents/<role>/skills/<skill-name>/SKILL.md` and init as the entry point.
  No standalone refresh or live-selection update is implemented.
- [ ] Keep Foreman and feature-owner on Pi, but remove Factory's three-app restriction for research,
  implementation and review. Check each app against the installed AgentShell capabilities.
- [x] Investigate missing native skill delivery in AgentShell. The extension already forwards
  selections. Native adapter gaps and optional roster effort need upstream changes; authorization
  is pending. Current prompt-based reading is not native loading. Audit any dependency adoption.

Scott removed the proposed live-settings check from attachment. No such observer or verification
was implemented. A long-lived owner can supply startup/exit evidence; attachment needs terminal
identity, readiness and liveness, not inspection of current model/effort/resources. Launch settings
remain distinct from live state. Upstream permission and native skill-delivery work remain separate.

Both setup routes must save and validate the same configuration. Preserve plans, worktrees,
custom resources and native login state. A maintenance skill cannot bypass incomplete setup or
silently change a running agent's selections. The current init/watch lifecycle needs changes;
command names, safe finalization and resource reload/restart behavior remain implementation design.

### Validation to add

Use the existing public init/watch boundaries and isolated no-inference native checks where they
fit. Confirm any additional public command/test seams before writing their tests.

- Incomplete assisted setup performs no polling, plan restoration or owner dispatch.
- Watcher attachment uses the intended ready terminal, rejects duplicates and stale/wrong targets,
  preserves Foreman on watcher shutdown, and stops when Foreman exits. Check idle and busy delivery.
  Changing Foreman's model/effort must not require reconnecting its watcher.
- Skill registration preserves contents, checks file availability and updates affected selections.
  Native loading/metadata diagnostics belong to the harness; registration does not promise loading.
- Each downstream app preserves its exact model selection and supported effort/resource behavior.

A live assisted-setup or delivery trial remains separate from no-inference wiring checks. Agree
its repository and native permissions before use.
