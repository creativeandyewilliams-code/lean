#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"
FILES=(target_relative_residue_main_v23.pdf target_relative_residue_supplement_v23.pdf)
TRANSCRIPT=QPDFCheckTranscript_v23.txt
CERT=QPDFCheckCertificate_v23.json
: > "$TRANSCRIPT"

if ! command -v qpdf >/dev/null 2>&1; then
  echo 'qpdf unavailable; no qpdf result can be claimed.' | tee -a "$TRANSCRIPT"
  python3 - <<'PY'
import json
json.dump({
  'certificate_type':'qpdf-check','version':'v23','status':'not_executed',
  'reason':'qpdf executable unavailable','all_exit_zero':False,
  'warning_exit_0_used':False,'files':[]
},open('QPDFCheckCertificate_v23.json','w'),indent=2)
open('QPDFCheckCertificate_v23.json','a').write('\n')
PY
  exit 4
fi

{
  echo '=== ENVIRONMENT ==='
  date -u +"UTC=%Y-%m-%dT%H:%M:%SZ"
  uname -a || true
  echo '=== QPDF IDENTITY ==='
  command -v qpdf
  qpdf --version
  sha256sum "$(command -v qpdf)" 2>/dev/null || true
  echo '=== INPUT HASHES ==='
  sha256sum "${FILES[@]}"
} >> "$TRANSCRIPT" 2>&1

overall=0
results=()
for file in "${FILES[@]}"; do
  echo "=== CHECK $file ===" >> "$TRANSCRIPT"
  echo "COMMAND=qpdf --check $file" >> "$TRANSCRIPT"
  qpdf --check "$file" >> "$TRANSCRIPT" 2>&1
  rc=$?
  echo "EXIT_CODE=$rc" >> "$TRANSCRIPT"
  [ "$rc" -eq 0 ] || overall=1
  results+=("$file:$rc:$(sha256sum "$file" | awk '{print $1}')")
done

python3 - "$TRANSCRIPT" "${results[@]}" <<'PY'
import json,sys,subprocess,platform,datetime,hashlib
transcript=sys.argv[1]
items=[]
for raw in sys.argv[2:]:
    path,rc,h=raw.rsplit(':',2)
    items.append({'path':path,'sha256':h,'exit_code':int(rc)})
try:
    version=subprocess.check_output(['qpdf','--version'],text=True).strip()
except Exception as e:
    version=f'error: {e}'
b=open(transcript,'rb').read()
cert={
 'certificate_type':'qpdf-check','version':'v23','status':'executed',
 'utc_timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'platform':platform.platform(),'qpdf_version':version,
 'command_template':'qpdf --check <file>','warning_exit_0_used':False,
 'files':items,'all_exit_zero':all(x['exit_code']==0 for x in items),
 'transcript':transcript,'transcript_sha256':hashlib.sha256(b).hexdigest(),
 'scope_note':'Exit zero means qpdf found no errors or warnings; it is not a proof that every possible PDF defect is absent.'
}
json.dump(cert,open('QPDFCheckCertificate_v23.json','w'),indent=2)
open('QPDFCheckCertificate_v23.json','a').write('\n')
PY
sha256sum "$TRANSCRIPT" > QPDFCheckTranscript_v23.sha256
exit "$overall"
