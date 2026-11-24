# Watcher lifecycle observation

Both watcher modes support read-only lifecycle status. Saved observations remain historical and
functional health is unchecked. The [status work record](../plans/watch-status.md) covers all nine
review corrections. See [current validation](../plan.md#current-status).
Back to [architecture](../architecture.md).

## Decision

`watch --status` covers plain watch and owner-managed watch without changing either lifetime.
Plain watch still owns its AgentShell session and closes it during normal cleanup. Managed watch
still borrows the persistent Foreman's connection. `--stop` remains managed-only. Status neither
attaches to a terminal nor authorizes delivery, replacement, process signals or replay.

The CLI starts `PlainWatchObservation` after the workspace lease and interval/configuration/owner
admission checks, immediately before watch composition and native startup. Refused admission cannot
create discovery or replace an earlier invocation's evidence. It lives inside that process;
there is no detached daemon or persistent Foreman owner for plain watch. Its private discovery
record is `.factory/runtime/watch/status.json`. A random run ID locates a Linux abstract Unix
socket without workspace path-length limits or stale socket unlinking. Same-user peer credentials,
process ID, run ID, process-start identity and a repeated discovery read bind a reply to the
advertised invocation. Process-start metadata is read from `/proc/self` at creation, never by
opening a handle from a saved PID. The record is observation data, not lifecycle authority.

`ObservedTerminal` delegates every terminal operation unchanged. It observes startup acknowledgement
and cleanup calls through the existing `ForemanTerminal` port. It does not add AgentShell calls,
inspect model settings, attach to a target, or use direct tmux input. Plain status currently has no
captured native target: `target: null` means unavailable, including after session readiness.

The observer thread answers while the watcher thread may be waiting on startup, polling, sign-in,
delivery or cleanup. Responsiveness establishes observer/process presence, not watcher progress.
`updated_at` records the last lifecycle transition; it is not a heartbeat or health check.
After startup, each transition makes one bounded-size history publication attempt without retry.
Readers see a transition after that attempt completes; failed publication leaves history stale,
not authoritative. Abrupt loss retains the last successfully published phase/readiness rather than
the initial startup snapshot. The client rechecks only workspace, run, PID and process-start
identity, so a same-run history update does not become an identity mismatch.

## Evidence and selection

- `source` identifies `plain_watch`, `managed_owner`, `combined` or `none`.
- `observation` distinguishes a live response, saved evidence and unavailable observation.
- `process` reports the responding watcher/owner as present, or unknown without that proof.
  `process_role` distinguishes a plain watcher process from a persistent Foreman owner.
- `foreman` reports session lifecycle evidence. Plain readiness is the last successful startup
  acknowledgement, not a query of the current foreground program or model access.
- `watcher` and `phase` describe lifecycle, with `watching` meaning the watch loop was entered.
  It does not claim polling or planning is succeeding; those can pause while supervision stays up.
- `health` is always `not_checked`. No functional monitoring is introduced.
- `recorded_*` fields retain historical lifecycle values without promoting them to current facts.

A live plain observer takes precedence over an old managed record. Otherwise a live managed-owner
query takes precedence over stale, missing or malformed plain discovery. The managed query retains
its actual child-handle lifecycle and existing terminal/delivery uncertainty safeguards.

When both sources are nonlive, neither replaces the other: `source: combined` reports current
Foreman, watcher, phase and process as unknown. Managed warning, recovery, target, owner identity
and recorded lifecycle metadata remain at the top level; `plain_watch` retains the separate plain
observation, warning and recorded values. The combined observation is saved when either supplies
saved evidence, otherwise unavailable. An old stopped owner cannot turn a timed-out plain process
into a current stop. Single-source saved-stop reporting likewise retains stopped only as history.

Code (since slice 5 of the [domain contexts plan](../plans/domain-contexts.md)): the factory
service `factory/services/watch_status.py` makes this choice and adds the setup state. The owner
adapter (`AgentShellOwner.report` in `agents/adapters/agentshell/owner_client.py`) reads the owner
record, because its recovery text names the owner's own files. `factory/adapters/watch_status.py`
reads the plain watcher. Golden transcripts in `tests/test_operator_transcripts.py` pin the output.

Offline records cannot establish current watcher presence or absence. In particular, a saved
Foreman stop does not establish watcher stop: owner snapshots can precede watcher cleanup and
watcher transitions are not all persisted. A saved confirmed Foreman stop remains labeled saved;
current Foreman/watcher/process/phase remain unknown. Clean stops acquire no invented recovery.
Other saved Foreman states retain the existing recovery guidance. Missing discovery also means
unknown, allowing for older uninstrumented
watchers. A shared lease is never used as watcher-presence or health evidence: init holds it too.

Queries use bounded frames and deadlines, preserve discovery/configuration, and perform no lifecycle
operations. Inaccessible transports, malformed records, reused/mismatched identities and changing
discovery retain uncertainty. Atomic snapshots reduce partial reads; they do not make saved state a
live observation. The endpoint is same-user local observation, not a security sandbox.
Within-limit JSON that exceeds parser depth is converted to controlled invalid-input observation;
it cannot kill the observer thread or replace the watch command's underlying exit status.

Shutdown closes the observer before final historical publication and retains the workspace lease
through its one attempt. An invocation exiting before session start records stopped with
`exited_before_session` evidence. Publication FactoryError/OSError/invalid-input failures are
ignored after startup, preserving the underlying interrupt/fatal result and diagnostic.
Initial observer startup is optional under the approved policy below. A normal invocation cannot
race final publication. Changed, missing or unreadable discovery is preserved on exit.
Same-user writes that bypass the lease are not a transactional filesystem boundary; hardening beyond
the existing no-follow/private-path rules is outside this correction.

Cleanup failure leaves Foreman unknown and retains `recorded_evidence: cleanup_uncertain` after
the endpoint closes. Completed cleanup calls are historical evidence, not current process proof.

## Validation limits

The status review exercised the public CLI with temporary factories, external commands and
AgentShell doubles. The peer-identity regression passed with the guard enabled and failed when
the guard was disabled in a private copy. The Nix host's tmux lived outside the fixture's
`/usr/bin:/bin` search path. With only that fixture path adapted, the native cases passed on both
Python versions. SonarQube passed the assigned gate for that source without imported coverage.

The broader runs exposed an obsolete assertion about approval guidance. Commit `b7e5f33`
corrected the assertion, and the push CI for `454c210` passed on both supported Python versions.
A separate intermittent shutdown timeout occurred in the parallel Python 3.13 run. Its trace
was consistent with SIGINT inside `Popen.__del__`. Five targeted repeats and a sequential full
rerun did not reproduce it. Its cause remains unknown.

Context7's CLI and MCP were unavailable; its anonymous public search returned the unrelated
xenodium Emacs package for the ScottRBK AgentShell query. The existing pinned
[AgentShell 0.5.0 examples][examples] were used instead. They distinguish owned-session close from
attachment disconnect and explain that a target alone does not prove the foreground agent.
Factory adds no new third-party API calls for status.

[examples]: https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/examples.md

## Approved saved-stop and optional-startup policies

Scott explicitly approved both recommendations. Single-source offline stopped-owner status reports
current Foreman unknown, with stopped only in recorded history; clean stops acquire no invented
recovery instructions. Initial plain-observer failure warns safely on stderr and allows actual
watching to continue with observation unavailable. Constructor identity reads are inside the
optional boundary along with directory, bind/listen, discovery and thread startup. This is optional
observation, preserving configuration, lease, owner-conflict and native watcher checks. Partially
started observer resources must close, original watcher results/diagnostics must survive, and
newer discovery must not be replaced. Partial startup closes its listener and any started thread,
then attempts identity-checked history. Constructor failure has no created listener to close.
The optional context does not catch actual watcher/application errors; observer teardown failure
also preserves their result. Five public regression tests failed before the corrections and passed
afterward on both supported Python versions.
Real filesystem faults cover a 0755 directory refusal before listener creation and a 0500
publication failure after bind. Direct `/proc` identity-read, bind or thread-start fault injection
is not covered; the constructor and entry code are inside the optional boundary. This is not
exhaustive OS-fault coverage. No production test hook or config was added; no policy holds remain.
