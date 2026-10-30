# Issue plan placeholder: validation

Status: implemented and locally validated through the approved public watch CLI boundary.
Back to [plan](../plan.md), [decision](../adrs/issue-planning.md) and
[architecture](../architecture.md).

## Failure and scope

DinoLand #9 exposed a real server constraint: the full serialized issue made plan context about
4288 characters, above Forgetful's default 2000. The native fake accepted arbitrary context, so
previous short-issue tests did not expose this failure. The external fake now rejects both
`create_plan` and `update_plan` contexts above 2000 characters, before changing stored records.
It records rejections for diagnostics. No private scaffold methods are tested. Read-only inspection
of `/home/scott/development/ai/mcp/forgetful/app/config/settings.py`, lines 173–174, confirmed the
2000-character goal/context defaults. `app/models/plan_models.py`, lines 155–156 and 195–196,
apply those limits to plan creation and updates.

Scott approved a placeholder, not truncation. New snapshots retain the recovery schema and replace
only body with a description naming the reporting provider, number and full title. Live issue
notifications retain the original full body. Both context writes disable ASCII escape expansion;
the test includes 240 astral Unicode title characters plus quotes, a backslash and a newline.
The ownership-intent update must fit too. Recovery accepts old full-body snapshots without writes.

Owner/Foreman starter guidance requires the owner to read the full provider issue before enriching
the plan. Goal and task descriptions hold planning detail within their limits. Context stays valid
JSON with brief notes/links and preserved recovery fields; it must not become a full issue copy.
Tests do not assert brittle prompt phrases or claim autonomous model compliance.

## RED then GREEN

The initial test ran before production changes. With the external limit enforced, it failed:

```text
Ran 1 test in 0.475s
AssertionError: 0 != 1 : ['plan.context exceeds 2000 characters']
FAILED (failures=1)
```

Exact RED command (from the repository root):

```bash
PYTHONPATH=src:tests \
  PATH="$HOME/.local/share/uv/python/cpython-3.12.16-linux-x86_64-gnu/bin:$PATH" \
  ~/.local/share/uv/python/cpython-3.12.16-linux-x86_64-gnu/bin/python3.12 \
  -m unittest \
  test_planning_watch.PlanningWatchTests.\
test_long_issue_uses_placeholder_and_recovers_closed_work_with_stable_ids -v
```

The same command after the minimal production change passed: one test in 0.831s.
The watch module then passed all 20 tests in 15.577s, including the added short-body placeholder
assertions and old full-snapshot recovery check.

The long-issue test proves full-body delivery, valid context on initial create and ownership-intent
update, saved workspace/source/revision/reference/URL, placeholder recovery after closure under
`--new-only`, stable plan/task/worktree IDs and no repeated plan/task creation. Existing tests
cover revised live issue bodies and new-only updates to recovered open work. The short-issue test
retains the notification/worktree contract while deliberately changing saved body semantics.

## Runtime setup and broader GREEN

A broader run with bare cached Python reached 168 tests but reported 24 failures, including subtest
failures, at native catalog setup. `InitFixture` replaces `PYTHONPATH` with source-only paths and
needs the installed AgentShell SDK; watch fixtures supply their own external SDK double. This was
an interpreter/import setup problem, not a context-limit blocker.

The repository's old `.venv` points to the former system Python. Reuse its existing Python 3.12
packages with the cached compatible interpreter in a disposable environment; no dependency is
installed, resolved or upgraded:

```bash
uv venv --offline \
  --python "$HOME/.local/share/uv/python/cpython-3.12.16-linux-x86_64-gnu/bin/python3.12" \
  /tmp/factory-placeholder-venv
printf '%s\n' "$PWD/.venv/lib/python3.12/site-packages" \
  > /tmp/factory-placeholder-venv/lib/python3.12/site-packages/existing-project.pth
```

SDK imports succeeded. The initially affected setup/guidance group passed 21 tests in 6.670s.
The complete selected regression command then passed **168 tests in 134.835s**, with no skips:

```bash
PYTHONPATH=src:tests PATH="/tmp/factory-placeholder-venv/bin:$PATH" \
  /tmp/factory-placeholder-venv/bin/python -m unittest \
  test_planning_watch test_planning_setup test_planning_adapter test_watch \
  test_watcher_alerts test_watcher_followup test_foreman_setup_repair \
  test_cleanup_recovery test_owner_profiles test_watcher_guidance \
  test_foreman_issue_intake -q
```

After the final guidance wording clarification, the focused watch/owner/intake command also passed
32 tests in 18.270s:

```bash
PYTHONPATH=src:tests PATH="/tmp/factory-placeholder-venv/bin:$PATH" \
  /tmp/factory-placeholder-venv/bin/python -m unittest \
  test_planning_watch test_owner_profiles test_foreman_issue_intake -q
```

Static checks:

```bash
.venv/bin/ruff check src tests
PATH="/tmp/factory-placeholder-venv/bin:$PATH" PYTHONPATH=src \
  /tmp/factory-placeholder-venv/bin/python .venv/bin/lint-imports --no-cache
git diff --check
```

Ruff passed; all three import contracts were kept (58 files, 122 dependencies); diff check passed.
Production changes use only the standard library, with no third-party library API changes.

## Mycelium

Reused the cached, previously audited Mycelium 0.4.5 wheel contents and existing dependencies.
No tool installation or upgrade occurred. The older CLI has no `--detail` option; its default
output was checked for full signatures and the complete relationship list before adoption.

```bash
export PYTHONPATH="$HOME/.cache/uv/archive-v0/wqd_0Wuk9G26z5MV"
/tmp/factory-placeholder-venv/bin/python -m mycelium.cli analyze . \
  -o /tmp/factory-placeholder-map.json --quiet
/tmp/factory-placeholder-venv/bin/python -m mycelium.cli export \
  /tmp/factory-placeholder-map.json -o /tmp/factory-placeholder-map.md \
  --max-classes 1000 --test-path tests
/tmp/factory-placeholder-venv/bin/python -m mycelium.cli export \
  /tmp/factory-placeholder-map.json -o /tmp/factory-placeholder-repeat.md \
  --max-classes 1000 --test-path tests
cmp /tmp/factory-placeholder-map.md /tmp/factory-placeholder-repeat.md
```

Repeat exports matched byte-for-byte. The map retains one nonempty class diagram and 77 boxes,
covering CLI, workflows, contracts, domain and adapters. Test filtering removed 3714 calls and
56 type relationships. The same twelve unresolved external-base warnings and heuristic call-edge
limits remain. Mermaid was checked as text, not rendered. The overview and relevant ADR were
updated; the existing AGENTS navigation still applies.

## Limits and safety

- These are selected regression checks, not a full-suite, hosted CI or live model trial.
- Arbitrarily large paths or other metadata can still exceed the server limit. No metadata is
  truncated and no general storage redesign is claimed.
- Owner guidance is provisioned for new starter resources; existing edited/live resources are not
  overwritten. Actual owner compliance and live adoption remain untested.
- No changes to Scott's FACTORY.md edit, live DinoLand files, running watcher/Foreman, shared
  Forgetful server or records. No retry writes to live services, commit or push occurred.
