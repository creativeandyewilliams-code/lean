#!/usr/bin/env bash
# Reproducible build for FSS Gravity Sector v12 routing skeleton.
# Requires an installed Lean 4 / Lake toolchain (elan recommended).
#   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
# The lean-toolchain file pins the exact compiler version.
set -euo pipefail

echo "== Lean toolchain =="
lean --version
lake --version

echo "== Structural pre-check (kernel-independent) =="
python3 verify_structure.py FssGravitySector/RoutingSkeleton.lean

echo "== lake build (kernel verification of all theorems) =="
lake build

echo "== BUILD OK: all declarations type-checked, no sorry/axiom =="
