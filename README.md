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

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Tests substitute GitHub and AgentShell; they make no live GitHub requests or Pi model calls.
