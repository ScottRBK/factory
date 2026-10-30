# Bundled role resources

The adjacent archive contains source files, never an installer or built executable. First setup
verifies each file against `role-resources.json`, copies missing files, and preserves edited files.
Ordinary repeated init preserves the existing setup without repair or synchronization. The manifest
records full upstream commits and SHA-256 hashes. No moving URL runs at initialization.

Reviewed sources:

- ScottRBK/pi-agentshell-extension, commit `5acb6aabfaae7c4d889600f6a5fffbb1c412dc6b`
  (package 1.5.0). MIT license included. Imports Node built-ins and Pi-provided peer modules.
  Its Python worker has an independent agent-shell-py 0.5.0 lock. With explicit consent,
  setup runs upstream `uv sync` against the bundled lock, with source builds, dev dependencies,
  config discovery, and Python
  downloads disabled. Verified metadata is staged in an independent temporary uv workspace to
  exclude ancestor workspace overrides. A successful input-matching receipt and import check are
  required for readiness. It creates the extension's real `.venv`; no interpreter override is used.
- ScottRBK/pi-hide-tools-extension, commit `a811fd2a2fcdb2ab94bf11b4ce4d6c0c9e210029`
  (package 0.1.0). Imports Node built-ins and Pi-provided modules. No installer or network calls.
  No upstream license file was present. Source remains attributed to Scott's repository.
- ScottRBK/pi-forgetful-extension, base `e670a88e5aaedb45132bca05c2c4f1a827c44f3c`, with
  local patch `965ac4a729d4f9182d499542da8b8e49cc7c6f033b0a8e24a6e9ce0b80670055`.
  The original 40-file runtime closure was independently approved for inert internal inclusion.
  The runtime-alignment follow-up removes only the Factory-specific host gate from that closure.
  Its new patch hash covers the complete local diff against the same upstream revision. Its managed
  entrypoint is `pi-forgetful/factory.ts`; `index.ts` retains standalone behavior. New starter
  Foreman definitions select the managed entry, while child and edited legacy selections remain
  unchanged. No upstream license grant exists: internal use only, no public redistribution.
  The unused post-close permission change was removed. Scott accepted the remaining concurrent
  workspace-path replacement limitation rather than adding containment work. Existing checks
  remain; source approval does not claim sandboxing, live enablement or backend/model access.
  Original exact-source approval: `implementation/source-audit/v7/approval.json` under
  `/tmp/factory-foreman-forgetful-2ptedi1m/`. All 15 prior bundle members are byte-identical.

The 1.5.0 published archive passed independent signature/provenance and source-byte verification.
Its exact 11 runtime files were adopted after source and artifact review. All four hide-tools files
and the SDK project/lock remain unchanged. Normalized definitions and Codex/Claude prompt skill
references pass real Pi 1.4.0 SDK/fake-native probes without inference. These probes do not install
the worker or establish model compliance. Audit evidence is under
`/tmp/factory-normalized-approved-O7PbkX/extension/bundle-audit`.

Review covered import/dependency manifests, process launch paths, upstream setup consent,
configuration writes, worker protocol and tool rendering. AgentShell runs a fixed local Python
worker with argument arrays; that worker delegates agent execution to the AgentShell library.
Hide-tools writes only its preference file under the selected Pi directory. Both extensions run
with the host user's privileges. This review is not a guarantee of security or Pi compatibility.

The hide-tools package declares Pi 0.99.1/0.99.2 peers. The factory does not use npm to resolve
or replace those peers; native compatibility checks use the reviewed runtime below.
The adjacent `install-locks.zip` pins Pi 1.4.0 with its normal Undici 8.10.2 dependency, without an
override. Its SHA-256 is `eba2b047dfed011a219b5d4f53133cf51d687ce40dd25416dfe91ce9556727f6`.
Scott rejected the earlier Factory-only dependency policy. The follow-up changes one package entry;
all other npm entries and Python requirements remain unchanged. Before adoption, the Undici archive
was checked against npm's SHA-512 integrity and registry signature. It has no installation hooks or
runtime dependencies. Fresh OSV checks still report eight advisories; alignment is not a security
clearance or an exposure assessment. No package was installed during this change.
The experimental Milo parser remains disabled. Evidence and exact diffs are under
`/tmp/factory-pi-alignment-YYrJLb/`; see the
[runtime-alignment record](../../../docs/plans/foreman-memory.md#runtime-alignment).

The earlier independent audit of the overridden lock verified 119 archives and 15,012 installed
files. Its clean advisory result does not apply to this restored upstream dependency. Historical
evidence: `implementation/AUDIT.md` under `/tmp/factory-foreman-forgetful-2ptedi1m/`.
Installer audit and memory-source approval remain separate; neither grants public redistribution.
Pi installs with `npm ci --ignore-scripts` into `.factory/runtime/pi`. The hash-bearing Python
requirements are unchanged; Forgetful 0.5.5 uses wheel-only, hash-checked `uv pip sync` in its own
`.factory/runtime/forgetful` environment. The reviewed Python resolution targets Python 3.12.
The factory asks before either installation. Existing executables are never upgraded.

Ubuntu 24.04 amd64 has a consent-gated `apt-get` recipe for tmux 3.4-1ubuntu0.1. A simulation must
report zero upgrades and removals before proceeding. APT uses configured distro repositories;
privileged package installation and OS dependencies remain an explicit trust boundary. There is
no APT index update. Other platforms and custom executable names require manual installation.

The factory defaults Pi's fallback binary downloads and Forgetful model downloads to offline/cache
mode. Local checks need an already provisioned model cache. Review and prepare models separately.
## Historical audits

The 2026-10-17 independent extension audit verified release 1.4.0 and worker 0.5.0.
That upgrade changed seven agentshell archive members; hide-tools was unchanged.
Evidence: `/tmp/astra-factory-1.4-audit/report.md` (local audit handoff).

The 1.4.1 follow-up inspected the local official release tag and its delta from 1.4.0. Five
members changed: `package.json`, `config.ts`, `index.ts`, `limits.ts` and `runner.ts`. They rename
configuration keys and their uses to snake_case. Dependency declarations, package scripts and
the Python worker/lock are unchanged. Each bundled member matches the immutable source commit
and the manifest's SHA-256. Evidence: `/tmp/factory-extension-141/audit.json`.
Registry DNS was unavailable, so published npm artifact integrity/provenance and fresh advisory
checks were not repeated. That 1.4.1 bundle used inspected Git source, not an unverified download.

The narrow Forgetful 0.5.5 audit verified source commit
`8964f8e626bc4945d2ca3cc2bd38a69ff44082e6` and 114 wheels for CPython 3.12,
Linux x86-64, glibc 2.39. The other 113 transitive versions and npm locks are unchanged.
Forgetful wheel SHA-256:
`a9c4089a8fb6efb8fdadd64136c1ae7fd797fbf2522614d0296a72e924789602`.
Source archive SHA-256 (not installed under the wheel-only policy):
`435a46380f5440164a1e46b210cb3a763824e755967f83c8984b539742bc530a`.
Evidence: `/tmp/forgetful-055-audit/AUDIT.md` (local audit handoff).
Neither audit proves a fresh host installation, live authentication, or autonomous planning.
Existing executables and edited installed resources require explicit reconciliation.
