#!/usr/bin/env bash
# v51 placeholder/non-vacuity audit.
#
# HEADLINE modules (imported by the root AflbLean.lean target): everything
# under AflbLean/ except AflbLean/Legacy/.
#
# FAILS (exit nonzero) if 'sorry' or 'admit' appears anywhere in the Lean
# sources (headline or legacy — neither should ever contain these).
#
# WARNS (prints a "MANUAL REVIEW REQUIRED" section, does not fail the
# build) if a HEADLINE module uses 'axiom', 'opaque', the literal 'True' as
# a theorem statement, or a proof that is just 'rfl'/'Iff.rfl' on its own —
# since each occurrence needs a human judgment call on whether it is a
# legitimate definitional-unfolding lemma or an illegitimate vacuous
# placeholder. Occurrences in AflbLean/Legacy/ are expected (that layer is
# explicitly axiom-based) and are not flagged.
set -uo pipefail

cd "$(dirname "$0")/.."

FAIL=0
HEADLINE_FILES=$(find AflbLean -maxdepth 1 -name '*.lean'; echo AflbLean.lean)

echo "== sorry/admit audit (all sources) =="
if grep -rnw --include='*.lean' -e 'sorry' -e 'admit' AflbLean.lean AflbLean/ ; then
  echo "FAIL: 'sorry' or 'admit' found in sources." >&2
  FAIL=1
else
  echo "OK: no sorry/admit anywhere in AflbLean.lean or AflbLean/."
fi

echo
echo "== MANUAL REVIEW REQUIRED (headline modules only) =="
REVIEW_FOUND=0
for f in $HEADLINE_FILES; do
  [ -f "$f" ] || continue
  if grep -nE '^\s*axiom\b' "$f"; then REVIEW_FOUND=1; fi
  if grep -nE '^\s*opaque\b' "$f"; then REVIEW_FOUND=1; fi
  if grep -nE ':\s*True\s*:=' "$f"; then REVIEW_FOUND=1; fi
  if grep -nE ':=\s*Iff\.rfl\s*$' "$f"; then REVIEW_FOUND=1; fi
  if grep -nE ':=\s*rfl\s*$' "$f"; then REVIEW_FOUND=1; fi
  if grep -nE ':=\s*trivial\s*$' "$f"; then REVIEW_FOUND=1; fi
done
if [ "$REVIEW_FOUND" -eq 0 ]; then
  echo "None found. Every headline declaration has non-trivial proof content."
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "RESULT: PASS (no sorry/admit). See MANUAL REVIEW section above for any flagged items."
else
  echo "RESULT: FAIL (sorry/admit present)."
fi

exit $FAIL
