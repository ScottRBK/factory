# Forgetful Factory

A software factory for one repository or a group of repositories, coordinating work tracking,
Forgetful planning, and Pi agents. See [FACTORY.md](FACTORY.md) for the intended behaviour.

`init` configures the factory and creates missing GitHub labels. `watch` reads matching issues
and notifies one newly launched Pi session. Planning and agent dispatch come in later slices.

## Run locally

Requires Python 3.12+, `uv`, Git, and authenticated GitHub CLI on Linux/WSL or another POSIX host.
Watching also needs Pi and tmux. `uvx` installs the AgentShell dependency automatically.

The package is not published yet. Build it from this checkout:

```bash
uv build
wheel="$(realpath dist/forgetful_factory-0.1.0-py3-none-any.whl)"

# In the same shell, move to your repository or group of repositories
cd /absolute/path/to/workspace
uvx --refresh --from "$wheel" forgetful-factory init
uvx --refresh --from "$wheel" forgetful-factory watch
```

Follow the prompts. Settings are saved in `.factory/factory.toml`; edit it to change them.
The watcher prints how to view Pi. **Stopping the watcher closes its Pi session.** Only one
watcher may run per workspace. Use `watch --help` through the same `uvx` command for options,
including `--existing`, `--new-only`, and `--interval` (default: 30 seconds).
See [architecture](docs/architecture.md) for implemented behaviour and [plan](docs/plan.md)
for progress. Role-specific tools and skills are not configured yet.

## Development

Use uv 0.13.1 or newer. It creates `.venv` and installs the locked runtime and dev dependencies:

```bash
uv sync --locked
uv run --locked ruff check src tests
uv run --locked lint-imports --no-cache
uv run --locked python -m unittest discover -s tests -v
```

Dependencies live in `pyproject.toml`; commit `uv.lock` after reviewed dependency changes.
Dev tools are not installed with the published package. CI runs all three checks on Python 3.12
and 3.13. Tests substitute GitHub and AgentShell; they make no live service or model calls.
