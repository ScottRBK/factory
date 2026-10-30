# GitHub CLI readiness

## Scope and cause

DinoLand's migrated host selected Ubuntu's GitHub CLI 2.46.0. Factory launched Foreman and
passed Forgetful planning checks, but every issue poll failed because that CLI lacks `--slurp`.
The reported authentication advice was misleading: this was a missing command capability.

Scott approved a public `forgetful-factory watch` regression boundary: incompatible GitHub CLI
must stop startup clearly, before launching Foreman or polling GitHub. Compatible startup must
continue. This is not a new automatic installer or an init migration feature.

Existing tests controlled GitHub's replies and assumed the executable accepted Factory's flags.
They did not model an older host CLI. The earlier manual readiness check inspected `gh --version`
and repository access but did not test pagination support. The new regression closes that gap.

## Implementation

- The GitHub adapter runs local `gh api --help` under its existing command deadline.
- Successful help must contain the exact `--slurp` option line. A prose example or a longer option
  name does not establish support. No minimum version is guessed.
- Watcher composition checks this before preparing or connecting Foreman. Failure exits startup;
  it does not enter the polling retry loop or print an attach command for an unstarted session.
- Command failure and expiry use a GitHub CLI readiness diagnostic. Missing support tells the
  user to install or upgrade `gh` on `PATH`, then restart watch. No API call or login is required.
- The existing work-tracking domain contract and application workflow are unchanged. Managed
  watcher children share composition, but their pre-existing Foreman is not replaced or closed.
- Standalone Foreman, init and watcher status remain outside this watcher-specific check.

The [watcher ADR](../adrs/issue-watcher.md) records the boundary and execution order.

## TDD and checks

The first regression failed on the original code: the controlled Foreman launched and exited with
status 7 instead of reporting incompatible GitHub CLI. After the production change, it passes and
proves no terminal events or issue API calls occurred. Additional public CLI cases cover failed
help, a real short command timeout, and misleading option text. The existing successful issue
submission case now confirms exactly one local help check while retaining its delivery assertions.
Shared external-command fixtures advertise supported help for compatible startup cases.

- Initial Python 3.13 watcher module: 29 passed in 20.490 seconds.
- Review found that regex `\s` could cross a blank line and accept unindented prose. An added
  public-CLI subcase failed by launching the controlled Foreman. Restricting whitespace to spaces
  and tabs fixes it. Final watcher modules pass all 29 cases: 20.251 seconds on Python 3.12 and
  20.564 seconds on Python 3.13. Broader results below predate this narrow review correction.
- Ruff: passed. All three import contracts: passed.
- Wheel/sdist rebuilt offline using the already audited, hash-constrained build backend. All 75
  wheel RECORD digests pass; all 72 source/resource files match the current source.
- Extracted-wheel smoke accepts actual GitHub CLI 2.103.3. A public watcher invocation with actual
  `/usr/bin/gh` 2.46.0 and isolated state rejects it before any Foreman event or attach hint.
  The compatible CLI's live, read-only paginated API checks are recorded below.
- Broader Python 3.12.16 run: 467 cases, 275.648 seconds; 463 passed, three skipped, one failed.
- Broader Python 3.13.18 run: 467 cases, 287.312 seconds; the same outcomes.
- These runs excluded 48 native lifecycle cases. Their existing fixture searches for tmux only
  in `/usr/bin` or `/bin`; this device provides it through Nix. No fixture or system path was
  changed to conceal that limit.
- Three installer cases skip outside Ubuntu 24.04; this device uses Ubuntu 26.04.
- The failing native managed-memory probe expects one controlled REST project request but observes
  none. It fails identically on a separate, unchanged `300aa24` source snapshot on both Python
  versions. It is not fixed here, and no full-suite green result is claimed.
- Native SDK probes used installed Pi 1.4.0 with isolated homes, fake children and loopback HTTP;
  no live model or service account was used by the regression runs.

Evidence is in `/tmp/factory-gh-audit-XFpFGG/`: `watch-tests.log`, `tests-312.log`, `tests-313.log`,
`baseline-native-312.log`, `baseline-native-313.log` and `excluded-native-lifecycle.txt`.
Temporary runners, environments, downloaded tools and the baseline copy remain outside the repo.
Independent read-only Claude review approved the original diff with no blocking findings. The
regex suggestion is corrected with red/green evidence; managed-start error routing is documented.
The review did not run tests. It also noted that init and a missing-executable regression remain
outside this coverage; generic command failure handling is unchanged. Hosted CI has not been run.
No commit, push, real watcher or Foreman launch is part of this change.

## Host upgrade and documentation tooling

Scott separately approved installing GitHub CLI 2.103.3 under `~/.local/opt`, with a command link
in `~/.local/bin`. The distro executable and GitHub login files were preserved. Release asset
hashes, the published checksum list and GitHub build attestation verified. Real read-only API
requests returned the expected page-array shape: no open issues and 11 label pages in DinoLand.
An initial smoke command incorrectly combined `--slurp` with `--jq`; the corrected check parses
JSON separately, as Factory does.

The 162-module advisory scan matched OpenPGP and HTML component advisories. The HTML package is
present. The audit permits Factory's JSON issue/label API use, not a blanket security clearance
for every GitHub CLI command; no full symbol-level reachability proof was performed.

Mycelium 0.4.5 regenerated the detailed map with full signatures, excluding `tests`. Its 77 boxes
have no missing in-scope call endpoints; 3,691 test calls and 56 type relationships were filtered.
Repeated export of the same map is byte-identical. The twelve external-base warnings and documented
heuristic call-edge limits remain. Mermaid was checked as text, not rendered.
The tool was installed only in a disposable environment after wheel/metadata/RECORD and component
review; existing Python tool dependencies were reused. Its component scan has native-library
advisory matches. The scoped trusted-source, local export and its limits are recorded in
`mycelium-audit.txt` under the evidence directory. Project dependency pins did not change.
