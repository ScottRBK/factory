{
  description = "Forgetful Factory - coordinate GitHub work tracking, Forgetful planning and Pi agents";

  # A2: nixos-unstable, matching agent-shell and forgetful. The estate consumes
  # inputs rather than this runtime, so riding unstable ages the build toolchain
  # here, not a 26.05 host. See docs/nix.md.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # A5: follow shared inputs onto our own nixpkgs so the closure holds exactly
    # one nix source. flake-parts -> nixpkgs-lib is mandatory, not advisory.
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };

    # A17: non-flake entry points (default.nix / shell.nix). flake = false: to
    # Nix this is a function, not a flake, and it contributes no outputs.
    flake-compat = {
      url = "github:NixOS/flake-compat";
      flake = false;
    };

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        pyproject-nix.follows = "pyproject-nix";
      };
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
      };
    };

    # A6: hooks via the flake-parts flakeModule. Following our flake-compat edge
    # keeps one node in the lock instead of one per consumer.
    git-hooks-nix = {
      url = "github:cachix/git-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-compat.follows = "flake-compat";
      };
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.git-hooks-nix.flakeModule ];

      # A16: only x86_64-linux has a builder today, so only it is verified.
      # aarch64-linux and aarch64-darwin are listed for consistency with
      # forgetful and agent-shell (pure Python, likely portable) and are
      # INTENT, NOT VERIFICATION - `nix flake check` will report them as
      # omitted incompatible systems. x86_64-darwin is omitted (deprecated
      # upstream). See docs/nix.md.
      #
      # Deliberately a literal list rather than inputs.systems.default: that
      # default set includes x86_64-darwin, which the house rule omits as
      # deprecated upstream. Declaring nix-systems without consuming it would
      # only add a lock node, so it is not declared at all (same as
      # agent-shell and forgetful).
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];

      perSystem =
        { config, pkgs, ... }:
        let
          inherit (pkgs) lib;
          python = pkgs.python312;

          # A14: version identity. House pattern is scm-stamp, but uv_build
          # ignores SETUPTOOLS_SCM_PRETEND_VERSION, so the sibling recipe would
          # silently do nothing here. Instead: read the single in-tree source at
          # eval time from the RAW path (never the filtered fileset), with an
          # env override for release naming. NEVER a version literal in this
          # file - that is how kyojin shipped 17 releases behind, silently.
          #
          # Release (needs --impure so getEnv is visible to a pure evaluator):
          #   FACTORY_VERSION=$(git describe --tags --abbrev=0) nix build --impure
          # --abbrev=0 matters: raw describe output is not a clean version.
          #
          # NOTE: uv_build stamps wheel metadata from pyproject.toml, so this
          # controls the derivation name and nothing the built binary reports.
          # Recorded in docs/nix.md; revisit when the project adopts dynamic
          # versioning or cuts its first tag.
          pyprojectVersion =
            let
              lines = lib.splitString "\n" (builtins.readFile ./pyproject.toml);
              picked = lib.filter (l: lib.hasPrefix "version = " l) lines;
              bare = lib.removeSuffix "\"" (
                lib.removePrefix "\"" (lib.removePrefix "version = " (lib.head picked))
              );
            in
            if picked == [ ] then throw "Could not find a 'version = \"...\"' line in pyproject.toml" else bare;

          version =
            let
              r = builtins.tryEval (builtins.getEnv "FACTORY_VERSION");
              e = if r.success then r.value else "";
            in
            if e != "" then e else pyprojectVersion;

          # 1. Workspace: pyproject.toml + uv.lock, read at eval time.
          workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

          # 2. Overlay from the lock. Wheels are the house default.
          #
          # Source decision (plan 57 task 344): agent-shell-py==0.5.0 resolves as
          # a PyPI wheel straight from uv.lock. agent-shell also ships its own
          # flake (#agent-shell-py, #env); consuming it as a flake input is the
          # estate-consumption alternative and is deliberately NOT used here, so
          # this repo stays lockfile-driven and adds no extra input.
          #
          # Measured: uv2nix logs "Not using uv_build direct build for . because
          # uv_build==0.13.5 is not a known compatible range" and falls back to
          # the PEP 517 API, which builds cleanly.
          uvLockedOverlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };

          pythonSet =
            (pkgs.callPackage inputs.pyproject-nix.build.packages { inherit python; }).overrideScope
              (
                lib.composeManyExtensions [
                  inputs.pyproject-build-systems.overlays.wheel
                  uvLockedOverlay
                ]
              );

          # 3. Runtime environment from the lock's default group, and a dev
          # environment adding the locked `dev` group (ruff, import-linter) so the
          # dev shell cannot drift from what CI runs.
          factoryEnv = pythonSet.mkVirtualEnv "forgetful-factory-env" workspace.deps.default;
          factoryDevEnv = pythonSet.mkVirtualEnv "forgetful-factory-dev-env" workspace.deps.groups;

          # A9 source filtering: MEASURED, not assumed. uv2nix builds this
          # workspace from its own fileset, which already excludes docs/, .github/
          # and root markdown - a docs-only edit leaves both the package drv and
          # the env drv byte-identical (verified 2026-11-08 by comparing
          # `nix show-derivation` names across a docs-only change). An extra
          # cleanSourceWith filter here would therefore be dead code, so none is
          # declared; docs/nix.md records where the stability actually comes from.

          # A9 source filtering is documented above; nothing to declare here.
          factoryApp = {
            type = "app";
            program = "${factoryEnv}/bin/forgetful-factory";
          };
        in
        {
          packages = {
            # The distribution itself (site-packages layout), as built from the lock.
            forgetful-factory = pythonSet.forgetful-factory.overrideAttrs (_: {
              inherit version;
              # Intentional: uv_build stamps wheel metadata from pyproject.toml,
              # so FACTORY_VERSION renames the derivation only - it cannot change
              # what the built wheel reports. Recorded in docs/nix.md; revisit if
              # the project adopts dynamic versioning or cuts its first tag.
              __intentionallyOverridingVersion = true;
            });
            # What to install when something must actually run the factory CLI:
            # an interpreter with the locked dependencies already inside it.
            env = factoryEnv.overrideAttrs (_: {
              inherit version;
            });
            dev = factoryDevEnv.overrideAttrs (_: {
              inherit version;
            });
            default = factoryEnv.overrideAttrs (_: {
              inherit version;
            });
          };

          apps = {
            forgetful-factory = factoryApp;
            default = factoryApp;
          };

          # A6: hooks mirror the checks upstream already runs (ruff + import-linter)
          # plus Nix hygiene. Nothing here imposes a new gate on the repo owner.
          #
          # ruff-format is wired but pinned to the MANUAL stage only: measured on
          # 2026-11-08, `ruff format --check src tests` reports 96 of 128 files
          # would be reformatted, so a default-stage hook would rewrite most of the
          # tree on an unrelated commit (agent-shell hit exactly this, 73 files, via
          # a pre-push stage). Never pre-push - it still runs on `git push`.
          # Promotion to the default stage is a tracked task, not a comment.
          #
          # import-linter is deliberately not a hook: it needs src/ on PYTHONPATH
          # and belongs in checks instead (task 588).
          pre-commit.settings.hooks = {
            nixfmt.enable = true;
            statix.enable = true;
            deadnix.enable = true;
            ruff.enable = true;
            ruff-format.enable = true;
            ruff-format.stages = [ "manual" ];
          };

          formatter = pkgs.writeShellScriptBin "fmt" ''
            ${lib.getExe config.pre-commit.settings.package} run --all-files --config ${config.pre-commit.settings.configFile}
          '';

          # A8: passes the utility test - a locked toolchain (including the dev
          # group) plus the host-tier test dependencies (tmux, gh) that the Nix
          # sandbox cannot provide.
          devShells.default = pkgs.mkShell {
            packages = [
              factoryDevEnv
              pkgs.uv
              pkgs.tmux
              pkgs.gh
              # The product installs Pi via `npm ci`; host_dependency tests need it.
              pkgs.nodejs
            ]
            ++ config.pre-commit.settings.enabledPackages;
            shellHook = ''
              ${config.pre-commit.shellHook}
              export PYTHONPATH="$PWD/src''${PYTHONPATH:+:$PYTHONPATH}"
              # Nix owns the environment; uv must not provision a competing venv.
              export UV_NO_SYNC=1
            '';
          };

          # git-hooks.nix contributes checks.pre-commit automatically; do not
          # re-declare it. Authored domain checks (task 588) get added here.
          #
          # A15: the ENTIRE unittest suite runs here - no module and no test is
          # excluded. Measured on 2026-11-08: 550 tests discovered, matching
          # upstream, with 545 passing in the sandbox and 4 skipping cleanly
          # (Ubuntu-24.04 and node prerequisites, which is what those tests
          # already do on any other host). tmux, git and gh are nativeBuildInputs
          # because the suite drives real Git and real tmux; the sandbox still has
          # no network, so anything reaching for the network fails closed.
          #
          # Expected red, and deliberately not hidden: one pre-existing flaky test
          # (test_watch_status.WatchStatusTests.
          # test_discovery_replacement_is_preserved_during_status_and_original_exit)
          # fails roughly 1 run in 5 outside Nix as well, so this check is
          # intermittently red on upstream alone. Raise with Scott at PR time.
          checks = {
            # A7 authored domain check: the three import contracts are the
            # hexagonal architecture's only mechanical enforcement, so `nix flake
            # check` must run them, not just ruff and the test suite. Upstream runs
            # the same command (`lint-imports --no-cache`) in CI.
            import-contracts =
              pkgs.runCommand "forgetful-factory-import-contracts"
                {
                  nativeBuildInputs = [ factoryDevEnv ];
                }
                ''
                  export PYTHONPATH="${./.}/src"
                  lint-imports --no-cache --config ${./.}/pyproject.toml
                  mkdir -p "$out"
                  echo "import contracts kept" > "$out/passstamp"
                '';

            # A7 authored domain check: the published artifact's RECORD must match
            # the wheel spec. Upstream CI does this after `uv build`; here the same
            # check runs hermetically. UV_PYTHON_DOWNLOADS=never plus an explicit
            # UV_PYTHON are required: uv otherwise probes FHS paths (/bin/sh,
            # /usr/bin/env) that the Nix sandbox does not have.
            wheel-record = pkgs.stdenv.mkDerivation {
              pname = "forgetful-factory-wheel-record";
              inherit version;
              src = lib.cleanSource ./.;
              nativeBuildInputs = [
                factoryDevEnv
                pkgs.uv
              ];
              dontBuild = true;
              doCheck = true;
              checkPhase = ''
                runHook preCheck
                export HOME="$TMPDIR"
                export UV_PYTHON_DOWNLOADS=never
                export UV_PYTHON="$(command -v python)"
                uv build --offline --wheel --out-dir dist .
                python tests/check_package.py dist/*.whl
                runHook postCheck
              '';
              installPhase = ''
                runHook preInstall
                mkdir -p "$out"
                echo "wheel RECORD validated" > "$out/passstamp"
                runHook postInstall
              '';
            };

            tests = pkgs.stdenv.mkDerivation {
              pname = "forgetful-factory-tests";
              inherit version;
              src = lib.cleanSource ./.;
              nativeBuildInputs = [
                factoryDevEnv
                pkgs.git
                pkgs.gh
                pkgs.tmux
                # Pi is installed with `npm ci` (host_dependencies.py), so the
                # installer tests drive a real npm; without node they cannot run.
                pkgs.nodejs
              ];
              dontBuild = true;
              doCheck = true;
              checkPhase = ''
                runHook preCheck
                # The Nix sandbox leaves HOME unset; the suite writes fixtures under it.
                export HOME="$TMPDIR"
                export PYTHONPATH="$PWD/src:$PWD/tests"
                python -m unittest discover -s tests --durations 25
                runHook postCheck
              '';
              installPhase = ''
                runHook preInstall
                mkdir -p "$out"
                echo "unittest suite passed" > "$out/passstamp"
                runHook postInstall
              '';
            };
          };
        };
    };
}
