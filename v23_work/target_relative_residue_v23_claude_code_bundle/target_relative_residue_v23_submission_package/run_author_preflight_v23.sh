#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
TRANSCRIPT=AuthorPreflightTranscript_v23.txt
: > "$TRANSCRIPT"
exec > >(tee -a "$TRANSCRIPT") 2>&1

echo "=== VERSION 23 AUTHOR PREFLIGHT ==="
date -u +"UTC=%Y-%m-%dT%H:%M:%SZ"
uname -a || true
python3 --version

for tex in target_relative_residue_main_v23.tex target_relative_residue_supplement_v23.tex; do
  echo "=== COMPILE $tex ==="
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$tex"
done

for pdf in target_relative_residue_main_v23.pdf target_relative_residue_supplement_v23.pdf; do
  echo "=== PDFINFO $pdf ==="
  pdfinfo "$pdf"
  echo "=== SHA256 $pdf ==="
  sha256sum "$pdf"
done

python3 - <<'PY'
import csv, json
from pathlib import Path
p=Path('.')
rows=list(csv.DictReader((p/'ClaimGenome_v23.csv').open()))
assert len(rows)==71, len(rows)
assert len({r['NodeID'] for r in rows})==71
assert sum(r['ChoiceResult']=='global' for r in rows)==7
assert sum(r['ChoiceResult']=='local' for r in rows)==64
for name in ['FunctionalGenome_v23.json','GCAConfiguration_v23.json','GCAReviewInstance_v23.json','GCAExecutionStatus_v23.json']:
    json.load((p/name).open())
print('JSON/CSV structural preflight passed')
PY

if grep -R -nE '_v22|V22|TargetRelativeResidueV22' --exclude='REVISION_NOTES_v23.md' --exclude='AuthorPreflightTranscript_v23.txt' --exclude='run_author_preflight_v23.sh' .; then
  echo 'Stale v22 reference found' >&2
  exit 3
fi

sha256sum "$TRANSCRIPT" > AuthorPreflightTranscript_v23.sha256
