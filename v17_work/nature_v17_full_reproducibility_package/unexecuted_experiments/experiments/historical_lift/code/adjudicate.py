#!/usr/bin/env python3
from pathlib import Path
import argparse,json,collections
ap=argparse.ArgumentParser();ap.add_argument('--outputs',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();votes=collections.defaultdict(list)
for p in Path(a.outputs).glob('*.json'):
 for r in json.loads(p.read_text())['reviews']:votes[r['candidate_id']].append(r['status'])
res={k:{'votes':v,'unanimous':len(set(v))==1,'provisional_status':v[0] if len(set(v))==1 else 'requires_typed_adjudication'} for k,v in votes.items()};Path(a.out).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
