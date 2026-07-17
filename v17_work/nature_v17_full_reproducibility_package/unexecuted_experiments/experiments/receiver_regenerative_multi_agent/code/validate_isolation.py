#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--run-dir',required=True);a=ap.parse_args();r=Path(a.run_dir);bad=[]
for p in (r/'packets').rglob('*'):
 if p.is_file() and ('answer_key' in p.name or 'sealed' in p.parts):bad.append(str(p))
plan=json.loads((r/'packets/run_plan.json').read_text());
for x in plan['runs']:
 if not (r/'packets'/x['receiver_A_packet']).exists():bad.append(x['receiver_A_packet'])
print(json.dumps({'bad_paths':bad,'pass':not bad},indent=2));sys.exit(1 if bad else 0)
