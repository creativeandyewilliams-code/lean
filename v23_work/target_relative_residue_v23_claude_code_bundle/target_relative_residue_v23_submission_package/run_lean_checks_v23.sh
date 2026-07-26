#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"
TRANSCRIPT=LeanBuildTranscript_v23.txt
CERT=BuildCertificate_v23.md
: > "$TRANSCRIPT"
if ! command -v lean >/dev/null 2>&1 || ! command -v lake >/dev/null 2>&1; then
  echo 'Lean/Lake unavailable; build not executed.' | tee -a "$TRANSCRIPT"
  exit 4
fi
{
  date -u +"UTC=%Y-%m-%dT%H:%M:%SZ"
  uname -a || true
  lean --version
  lake --version
  sha256sum lean-toolchain lakefile.lean TargetRelativeResidueV23.lean
  echo '=== placeholder audit ==='
  grep -nE '\bsorry\b|\badmit\b' TargetRelativeResidueV23.lean || true
  echo '=== lake build ==='
} >> "$TRANSCRIPT" 2>&1
lake build >> "$TRANSCRIPT" 2>&1
rc=$?
python3 - "$rc" <<'PY'
from pathlib import Path
import sys,hashlib,datetime,platform,subprocess
rc=int(sys.argv[1]); t=Path('LeanBuildTranscript_v23.txt'); src=Path('TargetRelativeResidueV23.lean')
text=f"""# Lean Build Certificate - Version 23

- Status: {'successful' if rc==0 else 'failed'}
- UTC timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}
- Platform: {platform.platform()}
- Lean version: {subprocess.run(['lean','--version'],capture_output=True,text=True).stdout.strip()}
- Lake version: {subprocess.run(['lake','--version'],capture_output=True,text=True).stdout.strip()}
- Exact command: `lake build`
- Exit code: {rc}
- Lean source SHA-256: {hashlib.sha256(src.read_bytes()).hexdigest()}
- Transcript: `LeanBuildTranscript_v23.txt`
- Transcript SHA-256: {hashlib.sha256(t.read_bytes()).hexdigest()}
- Scope: only declarations encoded in the Lean source are certified. See `TheoremLeanCorrespondence_v23.csv`.
"""
Path('BuildCertificate_v23.md').write_text(text)
PY
sha256sum "$TRANSCRIPT" > LeanBuildTranscript_v23.sha256
exit "$rc"
