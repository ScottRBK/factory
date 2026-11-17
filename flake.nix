{
  description = "Forgetful Factory - coordinate GitHub work tracking, Forgetful planning and Pi agents";

  # nixpkgs is nixos-unstable. Anything consuming this flake takes its inputs, not
  # this runtime, so tracking unstable moves this repo's build toolchain and
  # leaves the host system alone. See docs/nix.md.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # Follow shared inputs onto our own nixpkgs so the closure holds exactly one
    # nix source. flake-parts pulls nixpkgs-lib, so the follows edge below is a
    # requirement, not an optimisation.
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };

    # Non-flake entry points (default.nix / shell.nix). flake = false because to
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

    # Hooks arrive as a flake-parts module. Pointing this input's flake-compat at
    # our own edge keeps one flake-compat node in the lock instead of one per
    # consumer.
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

      # Only x86_64-linux has a builder today, so only it is verified.
      # aarch64-linux and aarch64-darwin are listed because the package is pure
      # Python and likely portable, but they are INTENT, NOT VERIFICATION:
      # `nix flake check` does not build them and warns that it omitted them as
      # incompatible systems. That warning is expected output, not a failure.
      # x86_64-darwin is left out because nixpkgs deprecates it upstream, so it
      # is not reported at all. See docs/nix.md.
      #
      # Deliberately a literal list rather than inputs.systems.default: that
      # default set includes x86_64-darwin, which is not targeted here. The
      # nix-systems input is not declared at all, since declaring it without
      # consuming it would only add a lock node.
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

          # Version identity. The common recipe stamps the version from git via
          # SETUPTOOLS_SCM_PRETEND_VERSION, but uv_build ignores that variable, so
          # copying the recipe here would silently do nothing. Instead the single
          # in-tree source is read at eval time from the RAW path (never the
          # filtered fileset), with an env override for release naming. NEVER a
          # version literal in this file: a hand-maintained literal is how one
          # project shipped 17 releases behind without anybody noticing.
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

          # 2. Overlay from the lock, resolving packages to wheels.
          #
          # agent-shell-py==0.5.0 resolves to a PyPI wheel straight from uv.lock.
          # That dependency also publishes a flake exposing the same package;
          # taking it as a flake input is the other option and is deliberately NOT
          # used here, so this repo stays lockfile-driven and adds no input.
          #
          # Measured: `uv build` takes the fast path for this project. The uv
          # frontend (0.13.5, from nixpkgs) uses its bundled uv_build backend
          # because pyproject.toml pins uv_build==0.13.5, so the uv-build-0.13.6
          # that the build-systems overlay puts on PATH never runs. The resulting
          # wheel reports `Generator: uv 0.13.5`, matching the pin; docs/nix.md
          # records the measurement.
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

          # Source filtering: none declared. uv2nix builds from the workspace root
          # as-is, so every git-tracked file - docs/, .github/ and root markdown
          # included - is derivation input: measured 2026-11-08, a docs-only edit
          # to docs/nix.md changed the drvPath of this package and of both
          # environments. The shipped modules stay identical; only 59 .pyc files,
          # which embed the source store path, and nix-support/setup-hook differ in
          # the output tree. A filter here would cut those rebuilds.
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
              # No `license` here on purpose: the repository has no LICENSE file
              # yet, and stating one would be a claim nobody has made. Add it in
              # the same change that adds the file.
              meta = {
                description = "Run and supervise CLI coding agents against Forgejo issues";
                mainProgram = "forgetful-factory";
              };
            });
          };

          apps = {
            forgetful-factory = factoryApp;
            default = factoryApp;
          };

          # Hooks cover what CI already runs (ruff) plus Nix hygiene. Nothing here
          # adds a gate the repository did not already have.
          #
          # ruff-format is wired but pinned to the MANUAL stage only: measured on
          # 2026-11-08, `ruff format --check src tests` reports 96 of 128 paths
          # would be reformatted, so a default-stage hook would rewrite most of the
          # tree on an unrelated commit. The 128 is 115 Python plus 13 Markdown -
          # ruff 0.17 formats Markdown too, so promoting this hook rewrites prose as
          # well as code. A pre-push stage is no safer: it still runs on every
          # `git push`. Promotion to the default stage needs a formatting-only
          # commit first.
          #
          # import-linter is deliberately not a hook: it needs src/ on PYTHONPATH,
          # which a check can supply, so it lives in `checks` instead.
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

          # A locked toolchain (including the dev group) plus the host-tier test
          # dependencies (tmux, gh) that the Nix sandbox cannot provide.
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
          # re-declare it. The project's own checks are added below.
          #
          # The ENTIRE unittest suite runs here - no module and no test is
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
          # intermittently red on the repository's own HEAD. It predates this
          # packaging work and is not hidden here.
          checks = {
            # The three import contracts are the hexagonal architecture's only
            # mechanical enforcement, so `nix flake check` must run them, not just
            # ruff and the test suite. CI runs the same command
            # (`lint-imports --no-cache`).
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

            # The published artifact's RECORD must match the wheel spec. CI does
            # this after `uv build`; here the same check runs hermetically.
            # UV_PYTHON_DOWNLOADS=never plus an explicit UV_PYTHON are required: uv
            # otherwise probes FHS paths (/bin/sh, /usr/bin/env) that the Nix
            # sandbox does not have.
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
