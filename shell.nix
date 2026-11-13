# nix-shell entry point (flake-compat); the flake is the source of truth.
# Delegates to the flake's own dev shell - never re-declares it.
(import ./default.nix).devShells.${builtins.currentSystem}.default
