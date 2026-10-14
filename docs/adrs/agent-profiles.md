# Role-specific Pi profiles

Status: proposed; not implemented. Profile and Forgetful integration choices remain unresolved.

Back to [architecture](../architecture.md).
Sequencing: [Foreman setup](../plan.md#slice-3-foreman-setup-and-issue-updates).

## Context

Notification delivery does not yet configure Foreman or feature-owner tools, skills, or resources.
The roles need distinct configurations without claiming host-level sandboxing.

## Proposed design

Use role-specific Pi agent directories at `.factory/agents/foreman/` and
`.factory/agents/feature-owner/`, selected per process through `PI_CODING_AGENT_DIR`. The agent's
working directory remains the workspace or assigned repository/worktree. Profile resources and
host credentials/runtime files have different lifecycles; never commit credentials or session logs.

A profile directory alone does not isolate tools: Pi also discovers shared skills and project
resources. Explicit resource/tool selection must account for MCP and extension tools, preserve
repository instructions, and be checked against the actual callable tool set. This is configuration
isolation, not a host sandbox. Both roles retain Pi's standard `read`, `bash`, `edit`, and `write`
tools, plus the role capabilities specified in [FACTORY.md](../../FACTORY.md). GitHub uses the
existing `gh` CLI through `bash`. No custom permissions system is proposed.

The existing interactive Pi adapter does not support `allowed_tools`; profile environment and
resource-flag support must be checked before profile-aware launches are implemented. Forgetful's
extension and CLI/skills or MCP arrangement is being worked through separately. These integration
choices are deferred, not prerequisites for the slice 2 notification journey.

## Consequences

A role directory is not proof of tool isolation. Verify actual resource discovery, callable tools,
repository instructions, and credential handling before claiming profile support is implemented.
