#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/rebuild"
rm -rf "$OUT"
mkdir -p "$OUT"

python "$ROOT/experiments/gate_zero/code/run_gate_zero.py" --out "$OUT/gate_zero"
python "$ROOT/experiments/direct_recurrence/code/run_recurrence.py" --out "$OUT/direct_recurrence"
python "$ROOT/experiments/semantic_equivalence_structural/code/run_semantic_equivalence.py" --out "$OUT/semantic_equivalence_structural"
python "$ROOT/experiments/governance_option_monotonicity/code/run_governance.py" --out "$OUT/governance_option_monotonicity"
python "$ROOT/experiments/gf_branch_hazard_robust/code/run_gf_branch_hazard.py" --out "$OUT/gf_branch_hazard_robust"
python "$ROOT/experiments/cst_computational_geometry/code/run_cst_geometry.py" --out "$OUT/cst_computational_geometry"
python "$ROOT/tools/compare_fingerprints.py" --frozen "$ROOT/experiments" --rebuilt "$OUT"
echo "All executable experiments rebuilt successfully."
