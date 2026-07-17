#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--certificates',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];schema=json.loads((root/'schema/mapping_certificate.schema.json').read_text());errs=[]
for p in Path(a.certificates).glob('*.json'):
 d=json.loads(p.read_text())
 for k in schema['required']:
  if k not in d:errs.append(f'{p.name}: missing {k}')
 if d.get('status') not in schema['status_values']:errs.append(f'{p.name}: invalid status')
 if d.get('status')=='supported_at_registered_scope' and (not d.get('evidence_sources') or not d.get('factorization_witness') or not d.get('schedule_witness')):errs.append(f'{p.name}: unsupported promotion')
print(json.dumps({'pass':not errs,'errors':errs},indent=2));sys.exit(1 if errs else 0)
