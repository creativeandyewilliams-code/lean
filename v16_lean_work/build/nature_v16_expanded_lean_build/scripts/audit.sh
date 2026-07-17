#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[audit] forbidden release tokens"
if grep -R -n -E '\bsorry\b|sorryAx|\badmit\b|^[[:space:]]*axiom[[:space:]]' \
    --include='*.lean' FmiCnsFull FmiCnsFull.lean AxiomReport.lean; then
  echo "Forbidden token found" >&2
  exit 1
else
  echo "No forbidden tokens found"
fi

echo "[audit] import targets"
python3 - <<'PY'
import pathlib,re,sys
root=pathlib.Path('.')
missing=[]
for p in root.rglob('*.lean'):
    for line in p.read_text().splitlines():
        m=re.match(r'import\s+(FmiCnsFull(?:\.[A-Za-z0-9_]+)*)', line)
        if m:
            target=root/(m.group(1).replace('.','/')+'.lean')
            if not target.exists(): missing.append((str(p),m.group(1)))
if missing:
    print(missing)
    sys.exit(1)
print('All project imports resolve to source files')
PY

echo "[audit] theorem manifest count"
python3 - <<'PY'
import json
m=json.load(open('THEOREM_MANIFEST.json'))
assert len(m['theorems']) == 33, len(m['theorems'])
print('33 registered theorem targets present')
PY
