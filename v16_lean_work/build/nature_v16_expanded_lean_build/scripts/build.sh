#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
lake update
lake build 2>&1 | tee build.log
lake env lean AxiomReport.lean 2>&1 | tee axiom-report.txt
bash scripts/audit.sh
