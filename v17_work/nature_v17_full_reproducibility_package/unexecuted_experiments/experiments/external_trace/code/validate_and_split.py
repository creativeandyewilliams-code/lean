#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,random,sys
ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--out',required=True);ap.add_argument('--seed',type=int,default=2026071708);a=ap.parse_args();rows=[json.loads(x) for x in Path(a.input).read_text().splitlines() if x.strip()];required=json.loads((Path(__file__).resolve().parents[1]/'schema/trace_record.schema.json').read_text())['required'];errs=[]
for i,r in enumerate(rows):
 for k in required:
  if k not in r:errs.append(f'row {i} missing {k}')
 if r.get('target_label') in str(r.get('condition')):errs.append(f'row {i} target leakage from condition label')
# exact duplicates and version locks
ids=[r.get('trace_id') for r in rows]
if len(ids)!=len(set(ids)):errs.append('duplicate trace_id')
versions={(r.get('model_provider'),r.get('model_name'),r.get('model_version')) for r in rows}
worlds={}
for r in rows:worlds.setdefault(r['world_id'],set()).add(r['condition'])
paired=[w for w,c in worlds.items() if len(c)>=2]
if not paired:errs.append('no paired worlds across conditions')
if errs:print(json.dumps({'pass':False,'errors':errs},indent=2));sys.exit(1)
rng=random.Random(a.seed);uw=sorted(worlds);rng.shuffle(uw);cut=int(.7*len(uw));train=set(uw[:cut]);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
for name,sel in [('train',train),('test',set(uw)-train)]:
 with open(out/f'{name}.jsonl','w') as f:
  for r in rows:
   if r['world_id'] in sel:f.write(json.dumps(r,sort_keys=True)+'\n')
report={'pass':True,'records':len(rows),'worlds':len(worlds),'paired_worlds':len(paired),'version_locks':[list(x) for x in sorted(versions)],'train_worlds':len(train),'test_worlds':len(set(uw)-train),'input_sha256':hashlib.sha256(Path(a.input).read_bytes()).hexdigest()};(out/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
