#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv
ap=argparse.ArgumentParser();ap.add_argument('--run-dir',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();run=Path(a.run_dir);key=json.loads(Path(a.key).read_text());out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
rows=[]
for p in sorted((run/'outputs').rglob('*.json')):
 d=json.loads(p.read_text());gen=d.get('generation');cond=d.get('condition','transmission_only');rid=d.get('run_id',p.stem)
 for ans in d.get('answers',[]):
  k=key[ans['task_id']];missing=set(ans.get('missing_premises',[]));claims=set(ans.get('affected_claims',[]));verdict_ok=ans.get('verdict')==k['verdict'];missing_ok=set(k['required_missing_premises']).issubset(missing);claims_ok=set(k['required_affected_claims']).issubset(claims);fatal=ans.get('verdict') in k.get('fatal_verdicts',[]);score=(verdict_ok+missing_ok+claims_ok)/3
  rows.append({'run_id':rid,'generation':gen,'condition':cond,'task_id':ans['task_id'],'family':ans['task_id'].rsplit('-',1)[0],'score':score,'verdict_ok':int(verdict_ok),'missing_ok':int(missing_ok),'claims_ok':int(claims_ok),'fatal':int(fatal)})
with open(out/'item_scores.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={}
for r in rows:
 k=f"{r['generation']}::{r['condition']}";summary.setdefault(k,[]).append(r)
agg={k:{'n':len(v),'mean_score':sum(x['score'] for x in v)/len(v),'verdict_accuracy':sum(x['verdict_ok'] for x in v)/len(v),'fatal_error_rate':sum(x['fatal'] for x in v)/len(v)} for k,v in summary.items()}
(out/'summary.json').write_text(json.dumps({'groups':agg,'n_items':len(rows)},indent=2));print(json.dumps({'groups':agg,'n_items':len(rows)},indent=2))
