#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python "$R/code/generate_packets.py" --out "$T/packets";mkdir "$T/outputs"
for cond in prose_only registry_only direct_graph_plus_lean cst_plus_lean cst_optional_action cst_ablation; do
  p="$T/packets/CST__${cond}__01"
  python "$R/code/mock_agent.py" --packet "$p" --key "$R/sealed/answer_key.json" --out "$T/outputs/$(basename "$p").json"
done
python "$R/code/score.py" --outputs "$T/outputs" --key "$R/sealed/answer_key.json" --out "$T/score" >/dev/null
python - <<'PY' "$T/score/summary.json"
import json,sys;s=json.load(open(sys.argv[1]));assert len(s)==6;assert all(x['mean_score']==1 for x in s.values());print('CST utility component plumbing passed')
PY
