# Normalized agent definitions

## Status

Scott approved this direction. Extension 1.5.0 is published, independently audited and bundled.
Factory passes 373 tests on Python 3.12.3 and 3.13.5, with native SDK probes enabled and no skips.
Core fixes and the final small delta passed independent review. Runtime repair policy remains
open. Audited uv/build-backend 0.13.5 fixes the checksum defect; package checks and independent
upgrade review pass. This contract does not establish live delivery or model compliance.

## Decision

Each agent has one `agent.json` containing its own launch settings and references to its children.
A parent does not copy the child's model, effort or resources. The AgentShell extension resolves
those references. Names are user-defined, not a Factory role enumeration.

`factory.toml` contains repository, watcher and Forgetful settings, plus `foreman_agent_file`.
That path resolves relative to the TOML file's directory. Agent choices no longer belong in TOML.
Planning/execution permission checks remain a Factory responsibility, independent of agent names.

Init provisions a factory once; later agent edits must not require init to synchronize files or
renew a model/resource fingerprint. Existing installations are not silently converted. Preserve
plans, worktrees, credentials and custom files. Do not maintain two competing configuration formats.

The approved standalone commands are `forgetful-factory foreman` and `foreman --attach`.
They now launch or reconnect without starting the watcher, using the existing owner, lease,
uncertainty protections and shared native Pi home.
Selecting a Foreman definition does not select a separate Pi authentication directory.

## Shared file contract

A normalized document has exactly two top-level sections:

- `agent`: required name, description, agent_type, model and effort; optional cwd and resources.
- `roster`: the existing enabled/roles envelope, with reference-only entries such as
  `{"agent_file": "../feature-owner/agent.json"}`. Omitted keys default to disabled/empty.

Each child supplies its own case-sensitive name, unique among immediate siblings. There are no
parent overrides or aliases. Relative references resolve from the containing file; absolute local
references are also accepted. Resource paths and cwd resolve from the referenced child's file.
Omitted worker cwd permits the caller to supply the assigned worktree. Omitted root cwd inherits
the Factory CLI process directory; starter coordinators explicitly select their own directory.
Native instructions and selected skills remain the instruction mechanisms; no prompt field is added.

Keep the existing `PI_AGENTSHELL_ROSTER_FILE` and `roster_file` selection interfaces. Selecting an
agent document through them selects only its roster; it does not change the running parent's own
model or resources. Factory reads the root Foreman definition when it starts that process; the
root must select Pi. Root resource options are forwarded, not replaced by controller defaults.
Starter definitions explicitly select the earlier exclusion policy; omitted options retain native
SDK defaults. Required Foreman/maintenance guidance and the audited extension remain launch checks.

Required workflow guidance uses Factory's explicit `foreman/SKILL.md` and
`factory-maintenance/SKILL.md` folder-name convention, independently of agent names or locations.
The selection walk stops at a directory's own skill, skips hidden child directories/node_modules,
follows lexical symlink directories, and rejects ancestor cycles or ambiguous required copies.
It does not interpret frontmatter, native ignore files or every native loader feature. Renaming
these workflow folders while retaining a frontmatter name does not satisfy the Factory convention.

Pi children receive their own agent file as their roster source. Non-Pi agents are leaves with a
disabled, empty roster. Resource capabilities and unsupported combinations remain native runtime
concerns, except for the explicit Codex/Claude prompt-skill mapping below. Existing native inline
rosters and ad-hoc calls remain supported extension features; Factory does not generate a second
inline copy of normalized definitions.

Loading is one level at a time, not a recursive expansion of the entire agent graph. Cyclic
references do not cause recursive parsing; native delegation-depth limits still apply at runtime.

## Selected worker skills

Scott approved preserving prompt-based skills for Codex and Claude, without adding native SDK
skill loading. The local extension implements the mapping below and passes public-tool tests,
including interactive Codex/Claude delivery. Independent source and final release-delta reviews
passed, as did exact-commit hosted CI. Factory's audited bundle now passes real SDK/fake-native
checks for selected skill references, worktree launch, native resume and same-session reload.

Keep selections in `agent.resources.skills`. The feature-owner reads the selected definition and
supplies the full role briefing, task context, and absolute skill-file references in its prompt.
For normalized Codex/Claude children only, the extension also appends a deterministic
read-before-work block of selected file paths. This prevents a missing reference in the caller's
briefing from silently losing a selected skill. It does not prove the model read the files or
followed their instructions.

After the existing selection/resume checks, derive an outbound request with native `skills: []`.
Keep every other resource option unchanged, including native errors for unsupported selections.
The saved definition and request retain the complete canonical selection. Pi, other native apps,
inline rosters and ad-hoc native resource calls keep their existing behavior.

Prompt-only discovery accepts an explicit readable regular file, a directory's `SKILL.md`, or
nested skill roots beneath a collection directory. Stop descending at each skill root; ignore
hidden child directories and `node_modules`. Preserve lexical paths, deduplicate equal paths and
reject missing/unreadable selections, empty collections and directory cycles before dispatch.
This is file discovery, not YAML validation or a replacement native skill loader. No skill bodies
are embedded automatically. Directory membership and file contents remain unfrozen and are resolved
again for each call, including resumes.

## Changes and running sessions

The parent sees a roster snapshot from extension load. Before launch, changed or missing child
settings must cause a clear error instead of silently using that old snapshot. Reload adopts new
choices for new launches. It must not silently retarget a resumed native session. Root model, cwd
and launch-resource changes need a Foreman restart; reloading its child roster does not apply them.

Selected resumes retain their original definition and resource contracts. Changed selections fail
rather than bypassing those contracts. Native approval/tool controls remain per-call. Unknown
liveness never authorizes replacement; notification failures never authorize automatic replay.

No live settings observer, recursive graph fingerprint, generated agent registry or automatic
migration is part of this work. File validation is not an atomic snapshot of the later native
launch, and skill/extension file contents are not frozen by a selected path.

## Factory integration

Scott confirmed that init provisions the whole factory and starter team once, not just Foreman.
Keep the initial team setup; later edits go directly into TOML and agent documents, followed by
reload/restart as needed. Do not impose starter names on later runtime validation.
The normal workflow still needs clear ownership, safe continuation and independent review; removing
fixed configuration fields must not remove those responsibilities from the agent guidance.
A partial first-init retry reuses equal parsed definitions without changing their formatting.
Different or invalid existing definitions cause a clear refusal and remain untouched; retry cannot
silently retain other choices while reporting success.

The completion fingerprint, generated runtime roster and skill-registration synchronization have
been removed. `.factory/setup-complete.json` records first completion, not agent settings.
`.factory/pi-profile.json` records native-home consent, and `.factory/resources` holds audited
runtime files independently of agent directories. Required initial setup, consent, runtime
integrity, permission checks and watcher ownership remain. Schema loading stays outside issue
handling.

First assisted setup has the complete starter definitions but no completion receipt. Instructions
keep the conversation in setup mode; Python refuses watching before completion. Finalization leaves
those definitions and the native conversation intact. There is no separate empty runtime roster,
and neither instructions nor a roster are a security sandbox.

Ordinary repeat init makes no catalog/backend calls, consumes no launch consent and does not update
skills or definitions. Explicit first finalization saves newly approved missing native-home consent
without recreating templates, validates access and writes completion last. Its output names the
selected root definition rather than assuming starter folders still exist.
Whether it should also offer runtime repair is awaiting Scott's decision; ordinary init remains
non-reconciling. The five optional native probes now pass against the audited published bundle,
including added-skill discovery without init. These checks use real Pi SDK loading and controlled
child processes; they do not establish live model access or skill compliance.

`FACTORY.md` remains Scott-owned. Its agent setup/configuration sections describe the older fixed
role fields and will need his explicit update. This ADR records the newer direction without editing
that intent document or the protected historical Design questions section.

Progress and checks are in the [implementation plan](../plans/agent-definitions.md).
