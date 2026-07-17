#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PROJ="$ROOT/lean_project"
OUT="${1:-$ROOT/run_output}"
rm -rf "$OUT"; mkdir -p "$OUT"
{
  date -u +%FT%TZ
  uname -a
  command -v lean || true
  command -v lake || true
  lean --version || true
  lake --version || true
} > "$OUT/environment.txt" 2>&1
cd "$PROJ"
cp -a . "$OUT/source_snapshot"
find . -type f -print0 | sort -z | xargs -0 sha256sum > "$OUT/source_before.sha256"
set +e
lake build > "$OUT/lake_build.stdout" 2> "$OUT/lake_build.stderr"
BUILD_EXIT=$?
set -e
echo "$BUILD_EXIT" > "$OUT/lake_build.exit"
if [[ "$BUILD_EXIT" -ne 0 ]]; then
  echo "Lean build failed; preserve logs and repair only genuine elaboration/type errors." >&2
  exit "$BUILD_EXIT"
fi
lake env lean AxiomReport.lean > "$OUT/axiom_report.txt" 2>&1
bash scripts/audit.sh > "$OUT/static_audit.txt" 2>&1
# MutationChecks is imported by the root build; also run directly to expose local diagnostics.
lake env lean FmiCnsFull/Tests/MutationChecks.lean > "$OUT/mutation_checks.txt" 2>&1
find . -type f -print0 | sort -z | xargs -0 sha256sum > "$OUT/source_after.sha256"
diff -u "$OUT/source_before.sha256" "$OUT/source_after.sha256" > "$OUT/source_mutation.diff" || true
if [[ -s "$OUT/source_mutation.diff" ]]; then
  echo "Build modified source tree unexpectedly" >&2; exit 4
fi
python "$ROOT/collect_results.py" --out "$OUT"
echo "Lean experiment completed."
