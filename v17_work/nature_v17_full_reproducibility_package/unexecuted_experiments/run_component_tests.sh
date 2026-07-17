#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
for d in   formalization_fidelity_multi_agent   receiver_regenerative_multi_agent   cst_geometry_utility_multi_agent   external_trace   historical_lift   physical_fss_mapping; do
  echo "== component test: $d =="
  bash "$ROOT/experiments/$d/component_test.sh"
done
bash "$ROOT/experiments/lean_formal_closure/preflight_test.sh"
echo "All component tests passed."
