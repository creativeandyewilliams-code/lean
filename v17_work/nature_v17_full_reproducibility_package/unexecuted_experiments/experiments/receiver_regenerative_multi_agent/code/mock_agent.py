#!/usr/bin/env python3
# Plumbing test only. Reads the key and therefore must never be used as scientific evidence.
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--tasks',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);ap.add_argument('--run-id',default='MOCK');ap.add_argument('--generation',default='A');ap.add_argument('--condition',default='mock');a=ap.parse_args();tasks=json.loads(Path(a.tasks).read_text());key=json.loads(Path(a.key).read_text());ans=[]
for t in tasks:
 k=key[t['task_id']];ans.append({'task_id':t['task_id'],'verdict':k['verdict'],'missing_premises':k['required_missing_premises'],'affected_claims':k['required_affected_claims'],'rationale':'mock plumbing answer','confidence':1.0})
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps({'run_id':a.run_id,'generation':a.generation,'condition':a.condition,'answers':ans},indent=2))
