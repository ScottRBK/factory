# Issue change notifications

Scott approved notifications for eligible new issues, changed planning fields, and new or edited
comments by any author. An issue timestamp alone must not trigger a notification. The
[watcher decision](../adrs/issue-watcher.md) records the adapter design and its request cost.

The GitHub adapter computes a deterministic revision from issue fields and a complete paginated
comment read per eligible issue. The watcher has no provider-specific state; no comments are cached.
A failed or malformed comment response fails the source poll, so no partial snapshot is consumed.
Issue and comment API reads are not atomic and GitHub can return stale data; subsequent polls
reconcile the observed snapshots. No live GitHub operation was performed for this change.

The first public adapter test failed before implementation because `first != second` when only
`updated_at` changed; it passed after the revision change. Further red/green checks covered a
case-insensitive GitHub repository URL and rejection of an empty outer comments page list.
The public watcher subprocess tests exercise timestamp suppression, content changes, new and edited
comments with an unchanged issue timestamp, and failed comment reads followed by retry.

The initial worker could not find Context7 on PATH. The parent used the existing cached CLI without
installing anything. Context7's `/websites/github_en_rest` documentation confirmed the per-issue
comments endpoint, case-insensitive repository names and 100-item page limit. Its
`/websites/cli_github_manual` documentation confirmed that `--paginate --slurp` returns an outer
array of complete pages. The sources are the official
[GitHub comments API](https://docs.github.com/en/rest/issues/comments) and
[gh api manual](https://cli.github.com/manual/gh_api). Query output is stored outside the repository
under `/tmp/factory-issue-change-parent/context7-*.txt`.

Local checks used the existing offline environment. The focused adapter, watcher and planning
run passed 53 tests. The eligibility and setup-repair run passed 35 tests, and the watcher-alert
run passed 46. Cleanup, cancellation and permission regressions passed 54 tests. A separate native
SDK resource-loading run passed five tests using the existing 1.5.0 installation. Ruff passed on the
changed Python files. Full discovery ran 636 tests with 69 failures and nine skips: 50 fixtures
could not find tmux in their hard-coded `/usr/bin:/bin` search, seven could not find `lint-imports`,
and one existing guidance assertion expected `auto_approve false` while the existing guidance uses
`auto_approve=true`. The remaining eleven failures used old timestamp revision assertions; their
updated suites passed in the reruns above. Discovery started before those test edits and does not
validate the final tree. No hosted CI, live GitHub, model inference or production delivery is
claimed.

## Request-cost refinement

The public adapter regression first failed on the old repository-wide comments endpoint and passed
after switching to per-eligible-issue reads. It checks two issues, attribution, no unrelated read,
and no comment requests when none is eligible. Existing adapter checks cover pagination, edits,
authors, malformed reads, title, epic, label ordering and case-insensitive source identity.

Fresh discovery selected 575 of 638 tests; the 63 excluded tests are listed in
`/tmp/factory-cost-exclusions.txt` (seven architecture checks needing the missing import linter,
50 native lifecycle fixtures needing `/usr/bin` tmux, and six native SDK checks). It reported six
failures, 280 errors and three skips in `/tmp/factory-cost-discovery.log`. Of those failures and
errors, 285 contained the sandbox's `Operation not permitted`; the remaining failure is the
previously recorded unrelated guidance assertion. The watcher CLI fixture could not bind its Unix
socket, so this run cannot establish final-tree watcher behavior. The three public adapter tests
passed; the fresh five-test native SDK rerun passed four and failed one loopback listener with the
same sandbox restriction. Red, green, focused and native logs are in `/tmp/factory-cost-*.log`.

## Parent final-tree validation

The parent reran validation outside the worker's socket-restricted sandbox, without changing the
source or test fixtures. All five new adapter/public-watcher tests passed. Fresh filtered discovery
selected 575 tests: 571 passed, one existing guidance assertion failed, and three skipped. The same
63 exclusions remain explicit in `/tmp/factory-issue-change-parent/exclusions.txt`; this is not a
full-suite pass. The failure at `tests/test_review_regressions.py:396` expects `auto_approve false`
without an equals sign; the unchanged guidance contains `auto_approve=false` for research/review
and `auto_approve=true` for implementation. It was not altered as part of this fix.

The five native role/worker tests also passed with the already-installed Pi 1.5.0 SDK, including the
loopback listener blocked in the worker sandbox. Ruff and `git diff --check` passed. Logs and the
filtered discovery runner are under `/tmp/factory-issue-change-parent/`. These are controlled local
checks, not live GitHub or model inference evidence. No runtime install, DinoLand change, watcher
restart, commit or push was performed. `FACTORY.md` retains its original SHA-256.

Mycelium 0.4.5 regenerated the source map with 92 boxes and tests excluded; a second export from
the same map was byte-identical. Its 13 external-base warnings and heuristic call edges remain;
the output was inspected as text, not rendered. The architecture overview remains under 500 lines.
The exporter retains three pre-existing generated lines at 101–102 columns.
