#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();p=Path(a.packet);tasks=json.loads((p/'tasks.json').read_text());key=json.loads(Path(a.key).read_text());answers=[]
for t in tasks:
 k=key[t['task_id']];answers.append({'task_id':t['task_id'],**k,'rationale':'mock','confidence':1})
Path(a.out).write_text(json.dumps({'run_id':p.name,'condition':p.name.split('__')[1],'elapsed_seconds':1,'transmission_bytes':100,'answers':answers},indent=2))
