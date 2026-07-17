#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv
ap=argparse.ArgumentParser();ap.add_argument('--outputs',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();key=json.loads(Path(a.key).read_text());rows=[];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
for p in sorted(Path(a.outputs).glob('*.json')):
 d=json.loads(p.read_text());rid=d['run_id'];cond=d['condition'];elapsed=float(d.get('elapsed_seconds',0));tx=int(d.get('transmission_bytes',0))
 for ans in d['answers']:
  k=key[ans['task_id']];fields=['verdict','holonomy','closure','drift_detected','semantic_signature'];ok=[ans.get(x)==k[x] for x in fields];rows.append({'run_id':rid,'condition':cond,'task_id':ans['task_id'],'score':sum(ok)/len(ok),'drift_ok':int(ok[3]),'elapsed_seconds':elapsed,'transmission_bytes':tx})
with open(out/'item_scores.csv','w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
g={}
for r in rows:g.setdefault(r['condition'],[]).append(r)
summary={k:{'n':len(v),'mean_score':sum(x['score'] for x in v)/len(v),'drift_accuracy':sum(x['drift_ok'] for x in v)/len(v),'mean_elapsed_seconds':sum(x['elapsed_seconds'] for x in v)/len(v),'mean_transmission_bytes':sum(x['transmission_bytes'] for x in v)/len(v)} for k,v in g.items()};(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
