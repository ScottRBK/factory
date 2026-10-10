# Forgetful Factory

A software factory for one repository or a group of repositories, coordinating work tracking,
Forgetful planning, and Pi agents. See [FACTORY.md](FACTORY.md) for the intended behaviour.

Currently, only `init` is implemented: it configures repositories, labels, and Foreman settings,
creates missing GitHub labels, and saves `.factory/factory.toml`. It does not launch agents or poll.

## Run locally

Requires Python 3.11+, `uv`, Git, and authenticated GitHub CLI (`gh auth login`) on Linux/WSL or
another POSIX system. Your GitHub account needs permission to create repository labels.
The package is not published yet, so build and run the local wheel:

```bash
# From this checkout
uv build
wheel="$(realpath dist/forgetful_factory-0.1.0-py3-none-any.whl)"

# From your repository or a directory containing several repositories
cd /absolute/path/to/workspace
uvx --from "$wheel" forgetful-factory init
```

Follow the prompts to select repositories, confirm their origins, and enter labels, model, and
effort. Run `init` again to reuse existing settings. To change them, edit `.factory/factory.toml`.
For noninteractive usage, see `forgetful-factory init --help` through the same `uvx` command.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Tests use temporary repositories and a substitute `gh`; they do not contact GitHub.
See [architecture](docs/architecture.md) for the implementation and [plan](docs/plan.md) for
progress.
