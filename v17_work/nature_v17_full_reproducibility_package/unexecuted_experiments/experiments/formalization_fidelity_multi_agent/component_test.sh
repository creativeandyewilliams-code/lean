#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python "$R/code/generate_packets.py" --out "$T/packets"
mkdir "$T/outputs";for p in "$T"/packets/FIDELITY_REVIEWER_*;do python "$R/code/mock_agent.py" --packet "$p" --key "$R/sealed/answer_key.json" --out "$T/outputs/$(basename "$p").json";done
python "$R/code/score.py" --outputs "$T/outputs" --key "$R/sealed/answer_key.json" --out "$T/score" >/dev/null
python - <<'PY' "$T/score/summary.json"
import json,sys;s=json.load(open(sys.argv[1]));assert s['verdict_accuracy']==1;assert s['false_acceptance_rate']==0;print('fidelity component plumbing passed')
PY
