#!/usr/bin/env python3
import argparse, json, subprocess, datetime, hashlib
from pathlib import Path
p = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--verdict', required=True, choices=['GC_sub', 'GI', 'UB', 'NE'])
ap.add_argument('--root-certificate')
args = ap.parse_args()
root = None
if args.verdict != 'NE':
    if not args.root_certificate:
        raise SystemExit('root certificate required')
    root = json.load(open(args.root_certificate))
    if root.get('derived_verdict') != args.verdict:
        raise SystemExit('requested verdict differs from root certificate')
    trace = p / 'GCAReviewTrace_independent_v23.jsonl'
    if not trace.exists():
        raise SystemExit('independent trace missing')
    subprocess.run([
        'python3', str(p / 'validate_carrier_gca_trace_v23.py'), str(trace),
        '--instance', str(p / 'GCAReviewInstance_v23.json'),
        '--root-certificate', args.root_certificate
    ], check=True, cwd=p)
status = json.load(open(p / 'GCAExecutionStatus_v23.json'))
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
status.update({
    'actual_status': 'executed' if args.verdict != 'NE' else 'NE',
    'actual_overall_verdict': None if args.verdict == 'NE' else args.verdict,
    'reason': 'Recorded from a structurally valid independent carrier-complete assessment.' if args.verdict != 'NE' else 'No valid independent carrier-complete assessment trace.',
    'updated_by': 'apply_gca_result_v23.py',
    'updated_utc': now,
    'frozen_manuscript_modified': False,
    'successor_version_required_for_manuscript_change': args.verdict != 'GC_sub'
})
with open(p / 'GCAExecutionStatus_v23.json', 'w') as f:
    json.dump(status, f, indent=2)
    f.write('\n')
root_hash = hashlib.sha256(Path(args.root_certificate).read_bytes()).hexdigest() if args.root_certificate else 'none'
addendum = "\n".join([
    '# Version 23 Independent GCA Result Addendum', '',
    '- Expected design result: `GC_sub`',
    f'- Actual result: `{args.verdict}`',
    f'- Recorded UTC: {now}',
    f"- Root certificate: `{args.root_certificate or 'none'}`",
    f'- Root certificate SHA-256: `{root_hash}`',
    '- Frozen manuscript PDFs modified after assessment: no',
    f"- Successor version required for manuscript-changing repair: {'yes' if args.verdict != 'GC_sub' else 'no'}",
    '', 'This addendum is an execution output. It is not a premise of the frozen Version-23 assessment instance.', ''
])
(p / 'GCAResultAddendum_v23.md').write_text(addendum)
print('Recorded external actual result:', args.verdict)
