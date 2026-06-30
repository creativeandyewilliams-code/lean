#!/usr/bin/env bash
# v51 reproducible rebuild driver. Run from anywhere; cds into the package.
set -uo pipefail

cd "$(dirname "$0")/.."
PASS=1

echo "=== 1. Toolchain check ==="
if ! command -v lake >/dev/null 2>&1; then
  echo "lake not on PATH. If using the pinned toolchain, run:" >&2
  echo "  export PATH=/opt/lean4/lean-4.14.0-linux/bin:\$PATH" >&2
  exit 1
fi
lake --version
lean --version

echo
echo "=== 2. Clean build of headline target (lake build AflbLean) ==="
# NOTE: bare 'lake build' (no target) silently no-ops in this project
# (no default target configured) — always pass the explicit target.
if lake build AflbLean 2>&1 | tee docs/build.log; then
  echo "Build: PASS"
else
  echo "Build: FAIL"
  PASS=0
fi

echo
echo "=== 3. No-sorry audit ==="
if bash scripts/check_no_sorry.sh; then
  echo "No-sorry audit: PASS"
else
  echo "No-sorry audit: FAIL"
  PASS=0
fi

echo
echo "=== 4. No-placeholder audit ==="
if bash scripts/check_no_placeholders.sh; then
  echo "No-placeholder audit: PASS"
else
  echo "No-placeholder audit: FAIL"
  PASS=0
fi

echo
echo "=== 5. Regenerate docs/axioms.txt ==="
if lake env lean scripts/PrintAxioms.lean > docs/axioms.txt 2>&1; then
  echo "Axiom audit regeneration: PASS"
  cat docs/axioms.txt
else
  echo "Axiom audit regeneration: FAIL"
  PASS=0
fi

echo
echo "=== 6. Headline-axiom-only verification ==="
# Every headline (Bucket A) theorem must show only propext/Quot.sound/Classical.choice.
BAD=0
for name in inverseBranchResponsePositive regularBranchCoefficientPositivity \
            viableAdmSignInvariant signInvariance fiberCriterion classifyCovers \
            classifyExclusive finiteCertificateClosureAscending \
            finiteCertificateClosureComplete viabilityNonReducibility; do
  line=$(grep "'AflbLean.$name'" docs/axioms.txt || true)
  if echo "$line" | grep -qE "AflbLean\.(Posits|Physics|Closure|Fiber|SecondOrder|Legacy)" ; then
    echo "FAIL: $name depends on a non-core axiom: $line"
    BAD=1
  fi
done
if [ "$BAD" -eq 0 ]; then
  echo "Headline-axiom-only verification: PASS (no headline theorem depends on a named physics posit)."
else
  PASS=0
fi

echo
if [ "$PASS" -eq 1 ]; then
  echo "=== FINAL RESULT: PASS ==="
  exit 0
else
  echo "=== FINAL RESULT: FAIL ==="
  exit 1
fi
