# Foreman Forgetful integration

## Agreed scope

Foreman alone should load the Pi Forgetful extension. Scott chose server-only extension support
for the first runtime slice. The CLI and extension must use the same Factory-configured server
and explicit project. The extension can use the server's HTTP API while Factory planning keeps
using the native CLI. This supersedes the earlier proposal to require a CLI-backed extension with
local/server parity before delivering any runtime support.

The CLI and extension keep their own authentication. Their credentials must permit access to
Factory's selected project, but sharing a server/project does not require sharing a login or token.
Keep server/project selection authoritative; do not introduce another target selector, implicit
personal-settings fallback, copied credentials or Git-origin project guessing. The shared Pi
profile supplies model access, not Forgetful authentication. Scott deferred the CLI transport
change and does not want Forgetful changed for this integration now.

Scott requested setup choices for automatic recall/capture and its model. For the DinoLand test
only, he authorized using his current main extension's model choice. That is test input, not a
hard-coded product default. No migration or repair of DinoLand is implied.

## Setup and saved preferences

First init accepts `--foreman-memory` / `--no-foreman-memory` and
`--foreman-memory-model provider/model`. The manual setup route offers automatic memory off/on,
then a numbered native Pi model selection when needed. The opt-in explicitly covers both recall
and capture. Fully specified existing CLI calls and assisted setup default off. If piped input ends
at the new on/off question, it also stays off; ending input after opting in does not waive model
selection. Other setup prompts retain their existing cancellation behavior.

`InitialAgentChoices` holds these transient choices. The filesystem profile checks a supplied
model against the native Pi catalog and writes starter preferences beside Foreman's `agent.json`:

```json
{"enabled": false, "capture_mode": "off", "model": null}
```

The starter file is `.factory/agents/foreman/forgetful.json`. Opt-in writes `enabled: true` and
`capture_mode: "auto"`, with an exact selected model. A model alone does not enable memory.
The file contains no backend, project, token or copied authentication settings. Matching partial
setup preserves formatting; conflicting/invalid preserved preferences are refused. The read-back
uses the existing protected JSON reader rather than following a replaced file or directory link.
Ordinary repeated init does not synchronize preferences or edited agent files.

Saving preferences does not verify extension authentication or memory-model access. Native CLI
planning checks use the CLI's login. The managed extension performs its own runtime and project
checks when Foreman starts, before any automatic memory-model request.

## Local setup and the current transport difference

Successful local Factory setup initializes or reuses a SQLite database. Its default path is
`.factory/data/forgetful.db`; an explicitly selected database may already exist. Local CLI calls
use that database directly. Factory does not start a Forgetful HTTP server for local setup.
The inspected Pi extension uses HTTP and cannot open that database directly. Pointing it at the
same database path is therefore insufficient. A server on the same computer still counts as a
server connection when configured that way.

## Server runtime (internal)

The managed entrypoint is included in the internal bundle after exact-source approval. Aggregate
Factory suites, package checks and independent integration review are recorded in the work record.
Source approval is not live enablement: no existing Factory or runtime was updated automatically.

New starter Foreman definitions select `.factory/resources/pi-forgetful/factory.ts`. Select that
file for managed behavior, not the package directory or standalone `index.ts`. Child roles do not
select it. Existing edited or legacy definitions can leave it unselected and continue using
native CLI planning. Ordinary init does not activate it, synchronize resources or repair those
files. Direct and watcher launches report that saved memory preferences are inactive when the
managed entrypoint is unselected. Only selected managed resources require the new bundle checks;
existing required-resource and hash checks remain.

Factory exports the absolute `FACTORY_FOREMAN_AGENT_FILE` for the selected root launch. The
extension reads `forgetful.json` beside that lexical path. Display names such as `foreman` are
not identifiers: renamed, relocated and external absolute definitions remain supported. Config
reads use nonblocking, no-follow regular-file descriptors, a 64 KiB limit, and identity checks.
Personal extension settings and Git-origin project discovery are not fallback configuration.

For a server instance, the managed entry uses Factory's explicit project and derived REST endpoint.
It verifies that project before recall or capture can call a model. It does not list unrelated
projects or create a replacement project. Capture rejects a different destination. In the TUI,
`/forgetful plans` remains available with memory off and no memory model selected. Runtime status
explains unavailable configuration or access; managed settings commands cannot redirect the target
or rewrite personal preferences. Standalone extension behavior keeps its original entrypoint.

Factory follows Pi and the extension's supported dependency choices. Scott rejected the earlier
Factory-specific Undici override and exact-runtime gate after standard Pi was refused during the
DinoLand trial. The installer still locks Pi for reproducibility, but does not override its HTTP
dependency. The managed entrypoint no longer inspects Pi/Undici version metadata or rejects
`PI_PACKAGE_DIR`; Pi owns runtime selection. Configuration, authentication and selected-project
checks remain. Existing environment defaults still disable the experimental Milo parser.

Dependency audit findings remain visible and unresolved unless separately verified. Following
upstream is not a security clearance, and Factory must not silently patch the user's runtime to
satisfy a private compatibility rule. Existing installations are not repaired or upgraded by this
source change. Regression tests check installation consent, safe installer options and actual
extension/project access, not dependency version literals. The existing native project-access test
reproduced the refusal and passes unchanged after removing the gate.

Explicit automatic-memory opt-in refuses local instances and unmappable server paths before saving
`factory.toml` or memory preferences. When Foreman's model is not supplied, earlier setup can still
provision profile/resources before this refusal. Memory-off setup preserves native CLI targets,
including custom MCP paths. Local runtime status reports the extension unavailable while SQLite/CLI
planning remains usable. No HTTP server is started and no backend conversion occurs.

Target/project environment is a launch-time snapshot. Restart Foreman after changing that
configuration; `/reload` alone cannot update the process environment.

### Separate authentication; shared-login helper withdrawn

Source inspection confirms that Forgetful 0.5.5 verifies REST bearer tokens through the same
provider as its MCP endpoint (`app/middleware/auth.py:157-214`). This permits compatible tokens
on both paths; it does not require the clients to share one login.

The inspected extension uses its own bearer-token configuration (`src/http.ts:394-446,495-505`).
It does not obtain or refresh the CLI's saved OAuth login. Scott clarified that separate
client authentication is intended for now. Validate the extension's access to the configured
server/project using its existing authentication rather than building a shared-login dependency.
This does not authorize reading or copying personal credentials.

The proposed native authenticated-request helper is withdrawn, not awaiting approval. No helper,
cache reader or authentication change was implemented. Revisit transport and authentication when
considering the later CLI-backed slice; no Forgetful changes are part of the current approach.

An optional `forgetful-auth.json` beside the selected definition contains only the extension's
existing `token_env` setting, for example:

```json
{"token_env": "FACTORY_FORGETFUL_EXTENSION_TOKEN"}
```

This is a variable name, not a token. Factory does not create this file. A configured missing
variable fails closed; an absent file permits the server's normal unauthenticated behavior, still
subject to selected-project access checks. Native `FORGETFUL_TOKEN` stripping remains in place;
use a distinct variable for extension authentication. Native CLI login is neither copied nor
refreshed by this extension path. The named variable is inherited by the Foreman process tree;
separate client authentication does not provide credential isolation between those processes.

An empty/root URL or exact terminal `/mcp` maps to the sibling `/api/v1`, retaining the proxy
prefix. Case variants, arbitrary paths and trailing `/mcp/` are not guessed. Credential-bearing,
query-bearing and fragment-bearing URLs are refused. These are managed REST eligibility rules;
ordinary native CLI connections retain their existing URL validation.

## State and capture source inspection

The planning panel saves only `planning_panel` as a boolean in
`.factory/data/pi-forgetful/planning.json`. Managed reads are bounded and reject links, non-regular
files and changed content. Saves refuse unsafe existing state rather than merging arbitrary fields.
New files request owner-only permissions and honor the process mask; no later permission change
occurs. Replacement is atomic, but concurrent replacement of parent directories or temporary names
is not fully contained. Scott explicitly deferred additional workspace protection for this internal
slice. Existing checks remain; this limitation is accepted, not fixed. Standalone settings retain
their existing merge behavior.

Durable queues are stored under the Factory workspace and separated by endpoint, credential-derived
identity and project. Tokens are not stored in queue paths. Existing uncertain-write receipts and
retry protections remain. Changing a credential can select a different queue partition; old work
is retained rather than automatically replayed under a different identity. File logging stays off.

The workspace is the state location, not additional read authority. File inspection stays within
Pi's trusted selected cwd. File and HTTP response reads have a 1 MiB limit before paging or model
use. Existing URL credential checks, DNS pinning, private-address restrictions and redirect limits
remain. The source-reader change preserves URL inspection rather than removing that capability.

Scott has not answered whether managed capture should inspect only exact URLs supplied by the user.
Neither that narrower policy nor a blanket URL ban is approved. This choice remains open before
live memory enablement. It does not alone prevent audited inert internal bundle inclusion and
controlled testing. The unlicensed extension is authorized for internal use only; no public
redistribution is approved.

## Later slice: shared CLI transport and local support

Revisit moving the extension's planning, recall and capture calls onto the native CLI used by
Factory. The intended follow-up would support the selected local database as well as the configured
server and explicit project. Settle authentication reuse as part of that later design. Preserve
server-first behavior and existing preferences; no transport switch, automatic backend conversion
or database migration is authorized now.

Validate local startup cost, background authentication, queue ownership and uncertain-save
handling through supported CLI/tool interfaces. Add upstream capabilities only where those checks
prove them necessary. Earlier proposals for account IDs, richer errors and noninteractive auth
are investigation inputs for this slice, not an approved package of backend changes.

Progress and validation are in the [work record](../plans/foreman-memory.md).
