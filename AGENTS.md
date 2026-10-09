# Forgetful Factory

This repository defines and implements a configurable software factory for a repository or group
of repositories. It coordinates work tracking, Forgetful planning, and Pi agents through AgentShell.
GitHub is the first work-tracking provider; the architecture keeps provider integrations separate
from the factory's workflows.

## Read before working

- [FACTORY.md](FACTORY.md) is the **what**: factory behaviour, components, and responsibilities.
- [Architecture](docs/architecture.md) is the **how**: structure, boundaries, and implementation
  design.
- [Plan](docs/plan.md) is the **when**: implementation work, sequencing, and agreed decisions.

`FACTORY.md` is owned by Scott (the user) and describes his intent. Scott is responsible for
updating it. Agents must not modify it without his explicit instruction. If implementation exposes
an ambiguity or requires a change to that intent, raise it with Scott rather than silently editing
the document or choosing conflicting behaviour.

Read the relevant documents before changing behaviour or implementation. Keep
`docs/architecture.md` up to date whenever changes affect the architecture, including component
responsibilities, service contracts, dependencies, configuration, or execution flow. Clearly
separate proposed architecture from implemented behaviour. Update the plan as work progresses.
