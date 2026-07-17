#!/usr/bin/env python3
"""Disclosed supplementary scoring alongside the exact-match score.py.
- fatal_error_rate: exact (verdict in key.fatal_verdicts).
- claim_id_recovery: substring match of the key's required claim ID inside the
  receiver's affected_claims text (case-sensitive). Measures whether the
  receiver recovered the REGISTERED claim identity (the transfer signal).
This does NOT remap verdict tokens (that would be task-dependent and biasable);
free-form verdict correctness is reported qualitatively in the results note."""
import json, sys, pathlib, csv
run=pathlib.Path(sys.argv[sys.argv.index('--run-dir')+1])
key=json.load(open(sys.argv[sys.argv.index('--key')+1]))
rows=[]
for p in sorted((run/'outputs').rglob('*.json')):
    d=json.loads(p.read_text()); cond=d.get('condition','transmission_only'); gen=d.get('generation')
    for a in d.get('answers',[]):
        k=key[a['task_id']]
        req_claims=k['required_affected_claims']
        claim_text=" ".join(a.get('affected_claims',[]))
        claim_recovered=all(any(rc in c for c in a.get('affected_claims',[])) for rc in req_claims)
        fatal=a.get('verdict') in k.get('fatal_verdicts',[])
        rows.append({'gen':gen,'condition':cond,'task_id':a['task_id'],
                     'claim_id_recovered':int(claim_recovered),'fatal':int(fatal)})
from collections import defaultdict
agg=defaultdict(list)
for r in rows: agg[(r['gen'],r['condition'])].append(r)
summary={}
for (g,c),v in agg.items():
    summary[f"{g}::{c}"]={'n':len(v),
        'claim_id_recovery':round(sum(x['claim_id_recovered'] for x in v)/len(v),3),
        'fatal_error_rate':round(sum(x['fatal'] for x in v)/len(v),3)}
out=run/'scoring'; out.mkdir(exist_ok=True,parents=True)
json.dump({'metric':'disclosed claim-ID recovery + exact fatal rate','groups':summary}, open(out/'normalized_summary.json','w'), indent=2)
print(json.dumps(summary,indent=2))
