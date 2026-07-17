#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python "$R/code/generate_packets.py" --candidates "$R/fixtures/candidates.json" --out "$T/p";mkdir "$T/o"
for p in "$T"/p/HIST_*;do python "$R/code/mock_review.py" --packet "$p" --out "$T/o/$(basename "$p").json";done
python "$R/code/adjudicate.py" --outputs "$T/o" --out "$T/result.json" >/dev/null
python - <<'PY' "$T/result.json"
import json,sys;x=json.load(open(sys.argv[1]));assert all(v['unanimous'] for v in x.values());print('historical component plumbing passed')
PY
