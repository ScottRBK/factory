# Slice 6: implementation, review and merge

Status: implemented and locally validated; Sonar gate passed. The live trial remains open.

## Scope

- Explicit implementation/review worker setup; older factories stay planning-only.
- Feature-specific plans, acceptance criteria and tests, not generic lifecycle task names.
- Proceed when requirements are clear unless repository rules require plan approval.
- Implementation owns tests, commits, pushes, PR creation/reuse and exact-commit CI correction.
- Feature-owner verifies PRs/CI and owns task updates, independent review, fixes, merge and cleanup.
- Deployment/E2E and overall plan completion remain Slice 7.

See the [delivery ADR](../adrs/feature-delivery.md) for contracts and limitations. Scott updated
`FACTORY.md` to give PR creation to implementation; agents have preserved that edit. The protected
Design questions section of [the plan](../plan.md) is unchanged; its earlier PR assignment is
superseded by this decision.

## What the checks establish

Public init/watch/configuration tests use temporary repositories and controlled external commands.
Native tests load the real Pi SDK, bundled extension, worker and AgentShell with fake child
executables and temporary homes. They verify worktree cwd, selected instructions/resources,
returned session IDs, continuation restrictions and call-only permission controls.

Python enforces setup readiness and worktree reconciliation. Delivery procedures are agent
instructions: tests cannot prove that models follow TDD, repair CI, review well or merge safely.
No live model, login, production backend, GitHub delivery or deployment trial was run.

## Validation

- Python 3.12: 242 tests passed in 299.197s, native checks enabled, no skips.
- Python 3.13: 242 tests passed in 300.448s, native checks enabled, no skips.
- These full runs include the PR-ownership regression and all test-fixture isolation changes.
  Final assertion-only tightening passed all seven worker-profile tests on both runtimes afterward;
  production instructions stayed unchanged.
- Ruff and all three import contracts pass: 47 files and 85 dependencies checked. The suite's
  deliberate direct/indirect violations confirm those contracts cover new files too.
- Offline wheel/sdist builds pass. All packaged source/resources match the checkout; 47 public and
  native tests passed against the extracted wheel, including cleanup recovery.
- Opus independently reproduced the earlier fixes: 75 affected tests and the mixed-case URL repro
  passed. It also approved the PR-ownership follow-up, passing seven public-init tests and checking
  that reversions of the workflow rules fail the regression.
- Mycelium 0.4.5 map refreshed: 47 boxes, one nonempty diagram, repeat export byte-identical.
  Ten external-base warnings remain; static call edges are heuristic. Mermaid was not rendered.

Test-first fixes cover skill-path retries, blank input, preserved roster diagnostics,
execution-only criterion permissions, symlink guards and per-init catalog reuse. Cleanup tests use
real Git: removed mappings survive restart; missing active trees, uncertain cleanup, occupied
paths, stale registrations and altered Git identity stop without mutation. Mixed-case GitHub URLs
are accepted without changing the stored record.

The first full run caught an expected-exit race in a rejection test and a setup timeout. The race
was fixed without weakening its assertions. Non-auth completion/watch/profile fixtures now avoid
optional HTTP policy discovery; independent loopback policy tests retain that coverage. The original
child-environment Python 3.13 subprocess issue did not reproduce in the parent's plain-echo probe.
No production workaround or increased timeout was added.

## SonarQube

Analysis `8e1bea50-e22b-4bb9-8895-a824e53d7fce` on `main` passed the assigned
**Sonar way sans code coverage** gate. It reports zero open issues, bugs, vulnerabilities,
hotspots and duplication. All complexity, repeated-literal and test-helper findings are fixed.

With Scott's approval, the three type findings at `cli/main.py:381–382,448` (S5890, S5886,
S5655) were marked false positive, with an explanation recorded on each issue. Opus independently
confirmed that Python's `dataclasses.replace` preserves `FactoryConfiguration`, but the analyzer
reports the generic `DataclassInstance` bound. Official Python documentation, type stubs and
probes on both runtimes confirm the same-type contract.

The latest scan includes the PR-ownership follow-up and retains those classifications. Rules, gate,
exclusions and source suppressions were unchanged. This validates the uncommitted checkout, not
hosted CI for a new commit. Bundled ZIP encoding and missing-blame warnings remain.

## PR ownership follow-up

Scott's revised flow is reflected in implementation, feature-owner and Foreman guidance. The IA
opens or reuses the repository PR, then checks/fixes CI for the exact commit. The owner verifies
that PR and evidence, arranges independent review and controls merge. Required checks still gate
implementation completion. No draft-only restriction or broader tool permissions were added.

A public-init regression failed against the old instructions, then passed after the role updates.
Opus prompted stronger assertions for CI completion, approval/merge limits, draft status and PR
reuse. Reverting each of those rules now fails its intended assertion. Shared-branch briefings name
the PR-opening task; the owner still chooses PR content. Closed/merged PRs need reconciliation.
These tests check provisioned guidance, not model compliance. Existing editable role files remain
create-only and need explicit reconciliation; setup does not silently replace user instructions.

## Single-review guidance follow-up

Scott requested one independent review per repository PR after a session reached 11 iterations.
Bundled owner and reviewer instructions now require one pass, followed by acceptance of the
implementation fix report once required exact-final-commit CI passes. The owner must not perform
another code-review pass itself. Resuming an owner does not reset the limit. CI corrections remain
allowed; unresolved blockers and conflicting repository review requirements go to Foreman.
Required approvals, deployment and E2E gates remain unchanged. Existing editable role files are
not automatically updated by this source change.

No new phrase-presence tests were added: they cannot establish that an agent follows this policy.
The existing worker-profile suite could not validate this checkout in the current environment:
`uv run --no-sync` could not import the project from the incompatible local virtual environment.
A retry with `PYTHONPATH=src python3` reached all seven tests, but each failed during setup with
`pi model listing failed; native catalog unavailable`, before its guidance assertions. No passing
suite, live-agent trial or hosted CI result is claimed for this follow-up. Only instructions and
documentation changed; no Python source, dependency or generated class-map changes were needed.

## Before the live trial

- Agree the disposable GitHub repository with Scott; none has been created or modified for a trial.
- Check native worker permissions for linked-worktree Git metadata, network and tools. Factory does
  not silently enable bypass mode or widen tool permissions.

Temporary implementation/review evidence is under `/tmp/factory-slice6/`, not stored in the repo.
No dependencies, bundled third-party packages, personal settings or credentials were changed.
