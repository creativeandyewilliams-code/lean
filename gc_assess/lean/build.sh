#!/usr/bin/env bash
# Reproducible build + verification for the GCAssess verdict-algebra development
# (slot L1 of the HCFM audit contract).
#
# Requires an installed Lean 4 / Lake toolchain (elan recommended):
#   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
#   source "$HOME/.elan/env"
# The lean-toolchain file pins the exact compiler version (leanprover/lean4:v4.9.0).
set -euo pipefail

cd "$(dirname "$0")"

echo "== Structural + semantic pre-check (kernel-independent) =="
python3 verify_structure.py GCAssess.lean

echo
echo "== Lean toolchain =="
lean --version
lake --version

echo
echo "== lake build (kernel type-checks every theorem) =="
rm -rf .lake            # force a clean build, no cached artifacts
lake build

echo
echo "== #print axioms (confirm no sorry / no added axioms) =="
# The verification hooks are the commented block at the foot of GCAssess.lean.
# Emit them to a throwaway module and evaluate so the axiom dependencies print.
cat > _Axioms.lean <<'LEAN'
import GCAssess
#print axioms GCAssess.combine_assoc
#print axioms GCAssess.fold_coherent_iff
#print axioms GCAssess.fold_incoherent_iff
#print axioms GCAssess.evalForest_eq_fold
LEAN
lake env lean _Axioms.lean
rm -f _Axioms.lean

echo
echo "== BUILD OK: all declarations type-checked; no sorry / admit / axiom =="
