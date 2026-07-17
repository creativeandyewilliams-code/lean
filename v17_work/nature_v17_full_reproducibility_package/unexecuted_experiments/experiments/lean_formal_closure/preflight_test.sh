#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
bash -n "$ROOT/run_lean_experiment.sh"
python -m py_compile "$ROOT/collect_results.py"
python - <<'PY' "$ROOT"
from pathlib import Path
import sys,re
r=Path(sys.argv[1]); files=list((r/'lean_project').rglob('*.lean'))
assert len(files)>=30, len(files)
text='\n'.join(p.read_text() for p in files)
for tok in ['sorry','admit']:
    assert not re.search(r'\b'+tok+r'\b',text),tok
assert (r/'lean_project/lean-toolchain').exists()
assert (r/'lean_project/lakefile.toml').exists()
print('Lean preflight: source files',len(files))
PY
