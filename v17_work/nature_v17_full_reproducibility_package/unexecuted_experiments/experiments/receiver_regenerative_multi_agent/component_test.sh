#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
python "$ROOT/code/generate_packets.py" --out "$TMP/run/packets" >/dev/null
python "$ROOT/code/validate_isolation.py" --run-dir "$TMP/run" >/dev/null
mkdir -p "$TMP/run/outputs"
RA=$(find "$TMP/run/packets/receiver_A" -mindepth 1 -maxdepth 1 -type d | head -1)
python "$ROOT/code/mock_agent.py" --tasks "$RA/hidden_tasks.json" --key "$ROOT/sealed/answer_key.json" --out "$TMP/run/outputs/mock_A.json" --generation A >/dev/null
RB=$(find "$TMP/run/packets/receiver_B" -mindepth 1 -maxdepth 1 -type d | head -1)
python "$ROOT/code/mock_agent.py" --tasks "$RB/hidden_tasks.json" --key "$ROOT/sealed/answer_key.json" --out "$TMP/run/outputs/mock_B.json" --generation B >/dev/null
python "$ROOT/code/score.py" --run-dir "$TMP/run" --key "$ROOT/sealed/answer_key.json" --out "$TMP/score" >/dev/null
python - <<'PY' "$TMP/score/summary.json"
import json,sys
s=json.load(open(sys.argv[1]));assert s['n_items']==28;assert all(v['mean_score']==1 for v in s['groups'].values());print('receiver component plumbing passed')
PY
