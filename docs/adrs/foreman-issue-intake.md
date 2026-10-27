# Foreman issue-intake guidance

## Decision and implementation

When a user asks Foreman to log an issue, Foreman should ask whether it should be eligible for
Factory's automatic handling. A request to log an issue alone is not permission to add an intake
label. An explicit request for a particular watched label already supplies that permission.

Foreman's starter instructions read `watcher_label` and `repository` from
`"$FACTORY_WORKSPACE/.factory/factory.toml"` at startup and before issue creation. The selected
Foreman skill explains how to use them. There is no copied label list, new configuration field,
label environment snapshot or separate issue-creation service. The role cwd is not the workspace.

- Confirm the target repository if unclear; only configured repositories are watched.
- Offer the actual configured labels. Any one matching label suffices. Matching is case-insensitive;
  use GitHub's existing label spelling and treat names as data, not shell instructions.
- Ask before issue creation so labelling cannot trigger intake before consent. If declined, leave
  watched labels off, except that watch-all has no such opt-out.
- If `watcher_label` contains the entry `*`, all open issues in configured repositories are watched,
  including unlabelled issues. Explain this and ask whether to proceed. Never add a literal `*`
  label, invent an opt-out label or silently change Factory settings.
- Eligibility does not prove that watching is running, a notification arrived or work started.
  Check status, explain blockers and retain the normal setup, ownership and dispatch checks.
  Changed watch settings require a deliberate watcher restart; saved settings are not a live
  watcher snapshot. Logging an issue does not authorize starting or reconfiguring the watcher.

This is agent guidance, not Python enforcement or a model-compliance claim. Existing issue polling,
label matching, scaffolding and delegation remain unchanged. Ordinary repeated init preserves
edited instructions; existing factories need deliberate reconciliation to adopt the new guidance.
No running Foreman or DinoLand configuration was changed.

Validation and remaining checks are recorded in the [work record](../plans/foreman-issue-intake.md).
