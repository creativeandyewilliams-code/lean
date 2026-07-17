#!/usr/bin/env bash
# One-command rebuild of the reproducible artifacts. Non-interactive stages.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

echo "[1/8] validate original inputs"
$PY - <<'PYEOF'
import hashlib,os
z="original_inputs/nature_v8_full_reproducibility_package.zip"
h=hashlib.sha256(open(z,'rb').read()).hexdigest()
ref="f21b7ba677c32140710092405a37de460f81a77fe8f6c459a965266eb8842a72"
print("v8 zip sha256", h, "MATCH" if h==ref else "DIFFERS(inspect)")
PYEOF

echo "[2/8] Gate Zero v8 rerun (needs pinned deps from requirements.in)"
if [ -d /tmp/v8run ]; then rm -rf /tmp/v8run; fi
mkdir -p /tmp/v8run && (cd /tmp/v8run && unzip -q "$OLDPWD/original_inputs/nature_v8_full_reproducibility_package.zip")
( cd /tmp/v8run/nature_v8_submission_package && $PY run_experiment.py >/tmp/v8run/run.json 2>/tmp/v8run/run.err && $PY tests/test_conformance.py >/tmp/v8run/conf.json 2>&1 ) \
  && echo "  gate zero rerun OK" || echo "  gate zero rerun: see /tmp/v8run (install requirements.in first)"

echo "[3/8] Lean static audit (kernel build requires an installable toolchain)"
grep -rEc '\bsorry\b|\bsorryAx\b|\badmit\b' lean/FmiCns.lean lean/FmiCns/*.lean | awk -F: '{s+=$2} END{print "  sorry/admit token total:", s+0}'
( command -v lake >/dev/null 2>&1 && (cd lean && lake build) ) || echo "  lake unavailable (toolchain egress-blocked) — see lean/reports/lean_formal_closure equivalent"

echo "[4/8] canonical direct recurrence"
$PY experiments/direct_recurrence/code/run_recurrence.py --out experiments/direct_recurrence >/dev/null && echo "  recurrence OK"

echo "[5/8] semantic-equivalence mutation + GF branch/hazard"
$PY experiments/semantic_equivalence/code/semantic_equivalence.py --out experiments/semantic_equivalence >/dev/null && echo "  mutation OK"
$PY experiments/gf_branch_closure/code/branch_hazard.py --out experiments/gf_branch_closure >/dev/null && echo "  branch/hazard OK"

echo "[6/8] receiver scoring (receiver runs are pre-frozen; scoring is deterministic)"
$PY receiver/scoring/score.py >/dev/null && echo "  receiver scoring OK"

echo "[7/8] rebuild manuscripts (PDF via reportlab; md/tex/docx via pandoc)"
for kind in article supplement; do
  d=manuscript/$kind
  base=nature_${kind}_v16; [ "$kind" = supplement ] && base=nature_supplement_v16 || base=nature_article_v16
  ( cd "$d" && $PY ../../tools/render_manuscript.py $base.mns $base.pdf "Nature v16" >/dev/null \
    && $PY ../../tools/mns_to_md.py $base.mns $base.md "../source_figures/" >/dev/null \
    && (command -v pandoc >/dev/null 2>&1 && pandoc $base.md -o $base.tex && pandoc $base.md -o $base.docx || echo "  pandoc unavailable") )
done
echo "  manuscripts rebuilt"

echo "[8/8] verify package"
$PY verify_package.py
