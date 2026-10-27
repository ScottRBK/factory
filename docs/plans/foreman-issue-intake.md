# Foreman watched-label awareness

## Status

Implemented locally as starter Foreman guidance. Scott requested this while the separate Forgetful
extension integration was in progress. It has not been committed, pushed or applied to DinoLand.
See the [decision record](../adrs/foreman-issue-intake.md).

## Validation

The existing approved public init/resource-delivery test boundary was used. Tests run real Factory
init against temporary repositories and controlled external programs, without live GitHub or model
calls. Tests prove guidance delivery and preservation, not that a model follows it.

- A new custom/multiple-label test first failed because root and skill guidance lacked the config
  source and consent rules. Minimal guidance changes made it pass.
- A second watch-all test failed before the wildcard consent paragraph was added, then passed.
- A preservation check confirms repeated init leaves edited guidance and configuration unchanged,
  without another external-program call.
- The three new checks, nine owner-profile checks and three native no-inference resource checks
  passed sequentially on Python 3.12.3 and 3.13.5: 15 tests each, no skips; 6.324s and 6.051s.

These runs used an immutable reviewed runtime-work snapshot plus this slice, isolated from the
concurrent memory-setup implementation. A combined snapshot subsequently passed 25 focused checks
on each Python, without skips, in 10.326s and 10.567s. A later assertion-only line wrap fixes the
100-column lint limit without changing the expected text; final-byte checks remain separate.
The final-byte phase-1 snapshot then passed 25 checks per Python, no skips, in 10.381s/10.080s.
Offline package checks passed: 72 RECORD hashes, 69 source/resource matches and preserved/new tests.
Actual Claude Code Opus 5.5 approved that snapshot, conditional on a separate memory-setup wording
fix. It found no label-guidance blocker. Its precision suggestion now names the exact `*` list
entry, not a character within a label name. The reviewed-fix snapshot passed full suites
sequentially: 491 tests each, no skips, in 598.162s on Python 3.12.3 and 594.287s on 3.13.5.
Exact unique IDs and unchanged source hashes were checked. The private audited Pi SDK was used;
no running or globally installed runtime changed. A separate actual Claude Code Opus 5.5
text-only closure approved the exact source and evidence, with no remaining blocker. It did not
rerun tests. The preceding tool-enabled follow-up passed 12 new tests per Python but hit its
turn limit before a verdict; that incomplete review is not approval.

A shared preliminary SonarQube scan found one complexity issue in the separate memory validator.
After its behavior-preserving extraction, analysis `be3a4abd-3889-4cca-ac34-720d877173ae` completed
successfully: assigned gate OK, zero unresolved issues, zero bugs/vulnerabilities/smells/hotspots
and 0.0% duplication. Separate `caycStatus` remains non-compliant. Gate/profile settings were
unchanged. Post-review-fix analysis `22593daf-9dd3-4ae5-b2c2-18fa2bd8eeaa` also passes with zero
unresolved findings and duplication. These scans cover Factory source/tests, not future bundled
TypeScript. The earlier shutdown issue remains unexplained; these passes are not a claimed fix.

Evidence: `/tmp/factory-foreman-forgetful-2ptedi1m/labels/`, including the `source/` snapshot.
Red and green logs are retained. No real issue was created or watcher behavior changed.
No live adoption or hosted CI result is claimed.
