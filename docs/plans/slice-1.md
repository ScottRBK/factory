# Slice 1: initialize a factory

Back to the [implementation plan](../plan.md).

Status: implemented, independently reviewed, and locally validated. Review findings were fixed
and regression-checked; live GitHub validation remains separately gated.
See [architecture](../architecture.md) for the implemented first-slice structure.

- [x] Package a `forgetful-factory init` command with interactive and explicit configuration.
- [x] Configure one or several local repositories, watched labels, Foreman model, and effort.
- [x] Validate configuration and access before creating missing GitHub labels.
- [x] Save `.factory/factory.toml`, preserve existing configuration, and support safe reruns.
- [x] Validate the packaged command locally through `uvx`; do not publish to PyPI in this slice.
- [x] Independently validate tests and the local initialization journey.
- [ ] Validate real GitHub label setup against repositories explicitly approved for that step.

Scott approved two public test boundaries: the initialization CLI and configuration loading.
Use TDD through those boundaries, temporary real Git repositories/files, and a substitute `gh`
executable for the external GitHub boundary. Do not mutate live GitHub repositories in ordinary
local tests. Live label validation in Dark Business is a separate confirmation step.

This slice does not poll, launch agents, create Forgetful plans/worktrees, or run a background
service. GitHub is the first work-tracking adapter behind provider-independent domain contracts.
Build dependency checks are recorded in [dependency audit](../dependency-audit.md).

Local validation: 31 tests passed on Python 3.12.3, including timeout and interruption checks.
`uv build --offline --no-python-downloads` produced a wheel and source distribution. Independent
wheel-installed CLI validation passed for multiple repositories, existing-label preservation,
repeat initialization, argument conflicts, denied access, and invalid NUL-containing settings.
All GitHub calls in these local checks used substitute executables. They did not configure
Dark Business, mutate live GitHub labels, or publish the package.

The initial Unicode checks missed NUL characters that TOML can decode but OS APIs cannot accept.
A public-loader regression and CLI invalid-config case reproduced the traceback before the fix;
validation now rejects NUL characters before external calls. The independent review also reproduced
an invalid second label allowing an earlier label creation; the exact CLI case now asserts no GitHub
calls or mutations. The review's unsupported-provider diagnostic advisory was fixed test-first.
No other review blockers were reported.

### Repository configuration update

- [x] Match Scott's revised spec: repeat `[[repository]]` tables instead of a `repositories` map.
- [x] Expose ordered repository records through the public loader and update initialization.
- [x] Reject duplicate local directories and old or mixed formats before GitHub calls.
- [x] Give existing configs header-conversion guidance without rewriting their bytes.
- [x] Use the approved CLI/loader seams for RED→GREEN regressions; all 31 local tests pass.
- [x] Rebuild and validate the local wheel with substitute `gh`; no live label mutations.

## Test CI

- [x] Add `.github/workflows/ci.yml` to run the existing suite on every push, without filters.
- [x] Use `ubuntu-latest` with separate Python 3.11 and 3.12 jobs and no Python dependencies.
- [x] Add pull-request checks and cancel older runs for the same workflow and ref.
- [x] Audit official actions; use read-only permissions and no saved checkout credentials.
- [x] Replace commit pins with verified `v7` tags for compatible updates, at Scott's request.
- [x] Validate workflow YAML, triggers, concurrency, matrix, references, and test command.
  The latest separate local test run passed all 28 tests.
- [x] Verify both hosted jobs after the workflow and implementation are committed and pushed.

Action dependency advisories and limits are recorded in [dependency audit](../dependency-audit.md).
Implementation committed and pushed as `2ee6e6b`; the push workflow passed on 2026-10-10.
[CI run 38041488129](https://github.com/ScottRBK/factory/actions/runs/38041488129) tested that exact
commit: all 28 tests passed on Python 3.11 (36.928 seconds) and Python 3.12 (37.253 seconds).
Local pre-commit validation also passed all 28 tests. PR-event execution and cancellation of
outdated runs have not been exercised on GitHub; a passing push run does not verify those paths.
Python 3.11 remains unavailable locally, but is now verified on the hosted runner.
