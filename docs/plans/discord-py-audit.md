# discord.py 2.7.1 dependency audit

Scope: add `discord.py==2.7.1` as an optional extra named `discord`, for CPython 3.12 and 3.13 on
Linux x86_64. Audit only, done on 2026-11-27, before any change to the manifest, lock or virtual
environment. Scott approves installation separately.

## Lock diff

Method: copy `pyproject.toml` and `uv.lock` into a scratch project, add
`[project.optional-dependencies] discord = ["discord.py==2.7.1"]`, then run `uv lock --no-build`
(uv 0.13.6, CPython 3.12.16). Result: `Resolved 29 packages`.

```text
Added aiohappyeyeballs v2.7.1
Added aiohttp v3.14.5
Added aiosignal v1.4.0
Added attrs v26.1.0
Added audioop-lts v0.2.2
Added discord-py v2.7.1
Added frozenlist v1.8.0
Added idna v3.20
Added multidict v7.2.1
Added propcache v0.5.4
Added yarl v1.25.1
```

- 11 packages added, 0 removed, 0 existing versions changed. The lock gains top-level
  `resolution-markers`, split at Python 3.13.
- `audioop-lts` installs on Python 3.13 only. It backports the stdlib `audioop` module that
  Python 3.13 removed.
- `typing-extensions` 4.16.0 is already locked for the dev group. With the extra it also becomes
  a runtime dependency on Python 3.12 only (from `aiohttp` and `aiosignal`). It is audited here.
- Each locked version is the latest stable release on PyPI. discord.py 2.7.1 (uploaded
  2026-03-03) is the latest stable release; GitHub `master` is 34 commits past the tag, with no
  newer tag.

## Packages

| Package | Version | License | Uploaded | Locked Linux x86_64 files |
|---|---|---|---|---|
| discord.py | 2.7.1 | MIT | 2026-03-03 | pure wheel (sdist reviewed) |
| aiohttp | 3.14.5 | Apache-2.0 AND MIT | 2026-10-11 | cp312, cp313 manylinux |
| aiohappyeyeballs | 2.7.1 | PSF-2.0 | 2026-07-01 | pure wheel |
| aiosignal | 1.4.0 | Apache-2.0 | 2025-07-03 | pure wheel |
| attrs | 26.1.0 | MIT | 2026-03-19 | pure wheel |
| audioop-lts | 0.2.2 | PSF-2.0 | 2025-08-05 | cp313-abi3 manylinux (3.13 only) |
| frozenlist | 1.8.0 | Apache-2.0 | 2025-10-06 | cp312, cp313 manylinux |
| idna | 3.20 | BSD-3-Clause | 2026-09-17 | pure wheel |
| multidict | 7.2.1 | Apache-2.0 | 2026-10-24 | cp312, cp313 manylinux |
| propcache | 0.5.4 | Apache-2.0 | 2026-09-16 | cp312, cp313 manylinux |
| yarl | 1.25.1 | Apache-2.0 | 2026-09-15 | cp312, cp313 manylinux |
| typing-extensions | 4.16.0 | PSF-2.0 | 2026-07-02 | pure wheel (runtime on 3.12 only) |

## Evidence and decision

- PyPI metadata: no locked file is yanked. The newest upload is multidict 7.2.1, 34 days before
  review. No name is typosquat-like. Project URLs point to `Rapptz/discord.py`, the `aio-libs`
  organisation, `python-attrs/attrs`, `kjd/idna`, `AbstractUmbra/audioop` and
  `python/typing_extensions`.
- Maintainers: discord.py has one PyPI maintainer, `rapptz`. PyPI returned a JavaScript challenge
  for most other project pages, so those lists were not obtained; provenance (below) ties those
  files to their upstream repositories instead. `audioop-lts` comes from a long-time discord.py
  contributor, and discord.py itself requires it on Python 3.13.
- Hashes: all 17 wheels and the discord.py sdist match the SHA-256 in PyPI JSON and in the
  scratch `uv.lock`.
- Wheel contents: each file's RECORD hash verifies. No `.pth` files, no
  `sitecustomize.py`/`usercustomize.py`, no `.data/scripts`. Native code is only the expected
  CPython extension modules (`aiohttp`, `frozenlist`, `multidict`, `propcache`, `yarl`,
  `audioop`).
- Entry points: only `idna` adds one, the `idna` console script (an IDNA encode/decode CLI).
- Unusual but explained: `multidict/_testcapi*.so` is an upstream C-API test helper that runtime
  code does not import. discord.py ships Windows-only libopus DLLs; `opus.py` loads them only on
  Windows when voice is used.
- PEP 740 provenance exists for all 16 dependency wheels, published by trusted publishing from
  their upstream GitHub workflows (aiohappyeyeballs from `main`, the others from release tags).
  Statement subjects, DSSE signatures, Fulcio certificate chains and Rekor entries verified; a
  tampered control failed. The trust root came from `sigstore/root-signing` without TUF
  verification; full Sigstore policy verification was not performed.
- discord.py has no provenance. The tag `v2.7.1` is a lightweight, unsigned tag on commit
  `dfd1144b2246a7adafe3f1c64a4dd9bc2187fcee`; PyPI got the files about two minutes later. The
  files were most likely built and uploaded by hand.
- OSV (queried 2026-11-27, exact versions): no advisories for any of the 12 package versions.
  aiohttp has many older advisories; the latest batch was fixed in 3.14.4. This is a dated
  lookup, not proof that the software is free of vulnerabilities.

## discord.py source review

- Each `discord/` file in the wheel and sdist is byte-identical to the tag, with one exception:
  `discord/search.py` (418 lines) is in both files and in the 2.7.0 wheel, but not in the tag or
  in Git history. It holds plain data classes for message-search filters, no I/O, and no module
  imports it. It is a stray, inert file from the build tree.
- Network endpoints (static scan of all modules): REST `https://discord.com/api/v10`, gateway
  `wss://gateway.discord.gg/`, CDN `cdn.discordapp.com` and `media.discordapp.net`, plus URLs
  that Discord returns at run time. No telemetry, analytics or update checks.
- Import-time code: version info, a logging `NullHandler`, sentinels, regexes and optional
  `orjson`/`zstandard` fallbacks. Nothing reads files, starts processes or opens sockets at import.
- Code that runs only when called (and the relay does not call): FFmpeg through `subprocess` for
  voice, libopus through `ctypes`, extension loading in `ext.commands`, and `setup_logging`.
- Optional extras were not audited: discord.py `voice` and `speed`, and aiohttp `speedups`.

## Artifact SHA-256

```text
discord_py-2.7.1-py3-none-any.whl
849dca2c63b171146f3a7f3f8acc04248098e9e6203412ce3cf2745f284f7439

discord_py-2.7.1.tar.gz
24d5e6a45535152e4b98148a9dd6b550d25dc2c9fb41b6d670319411641249da

aiohappyeyeballs-2.7.1-py3-none-any.whl
9243213661e29250eb41368e5daa826fc017156c3b8a11440826b2e3ed376472

aiohttp-3.14.5-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
20f085697d7e911f1f73c43ed03fafbed1e7121797e2eb5428efa80398060584

aiohttp-3.14.5-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
1ffa3a523a36d8628f98c06492ae16a31a23d14c0b4ec721757b477319f656d6

aiosignal-1.4.0-py3-none-any.whl
053243f8b92b990551949e63930a839ff0cf0b0ebbe0597b0f3fb19e1a0fe82e

attrs-26.1.0-py3-none-any.whl
c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309

audioop_lts-0.2.2-cp313-abi3-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl
51c916108c56aa6e426ce611946f901badac950ee2ddaf302b7ed35d9958970d

frozenlist-1.8.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl
494a5952b1c597ba44e0e78113a7266e656b9794eec897b19ead706bd7074383

frozenlist-1.8.0-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl
fb30f9626572a76dfe4293c7194a09fb1fe93ba94c7d4f720dfae3b646b45027

idna-3.20-py3-none-any.whl
ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c

multidict-7.2.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
1fb8c1a3480c130c3a6422d5f16f3cad6552bf08c2089dd288ba7134649183b5

multidict-7.2.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
cd69c99affd1b4debc1f9a53058ea6e3a9b34f2e733840bb45891666cd8ede0a

propcache-0.5.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
2814ecd8e818f487bee4b0f921bc4d1c176cc5fc71ac0f072d0fa67eda4ac14b

propcache-0.5.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
f85915e00dcb1cd9f2f890ead064ed40a27df06f0db65be427b29482ae357572

yarl-1.25.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
c6f117789d22dce188e5754e8bc65b7e6ebf8cb73963b9fa761f672a5883769d

yarl-1.25.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
be80550d9bfe83d9b62398a37081a90434e6df2d978ec345c3d2820de6beddab

typing_extensions-4.16.0-py3-none-any.whl
481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8
```

## Use constraints

- Install only from a lock that matches this diff, so uv checks the hashes above. Each locked
  package has a wheel for cp312/cp313 Linux x86_64; never build the discord.py sdist.
- discord.py has no provenance. Its integrity depends on one PyPI account and the lock hash. For
  any discord.py upgrade, repeat the tag-to-wheel comparison and look for untracked files.
- Keep aiohttp at 3.14.4 or later. discord.py allows `aiohttp>=3.7.4,<4`, so a lock refresh can
  move it. Re-run OSV for aiohttp, yarl, multidict and idna on each lock change.
- `uvx --from "forgetful-factory[discord] @ $wheel"` resolves the extra's dependencies freshly,
  not from this lock. The direct pin is exact; the others follow discord.py's ranges.
- Do not enable discord.py `voice` or `speed`, or aiohttp `speedups`, without a separate audit.

## Verdict

**Pass with notes.** All 18 files match the lock and PyPI. No exact-version advisories. No
install-time or import-time hooks. 16 of 18 files have verified provenance from upstream
workflows. Notes: (1) discord.py has no provenance and was built by hand from a tree that held one
untracked, inert file (`discord/search.py`); (2) aiohttp has high advisory churn, so recheck it on
each lock change; (3) `idna` adds a console script.
