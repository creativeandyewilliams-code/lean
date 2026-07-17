#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv
ap=argparse.ArgumentParser();ap.add_argument('--outputs',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();outs=Path(a.outputs);key=json.loads(Path(a.key).read_text());out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rows=[]
for p in sorted(outs.glob('*.json')):
 d=json.loads(p.read_text());rid=d.get('reviewer_id',p.stem)
 for ans in d['reviews']:
  k=key[ans['item_id']];vok=ans['verdict']==k['verdict'];pred=set(ans.get('mismatch_dimensions',[]));truth=set(k['mismatch_dimensions']);tp=len(pred&truth);prec=tp/len(pred) if pred else (1.0 if not truth else 0.0);rec=tp/len(truth) if truth else (1.0 if not pred else 0.0);rows.append({'reviewer':rid,'item_id':ans['item_id'],'verdict_ok':int(vok),'dimension_precision':prec,'dimension_recall':rec,'false_accept':int(k['verdict']=='mismatched' and ans['verdict']=='matched')})
with open(out/'item_scores.csv','w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'n':len(rows),'verdict_accuracy':sum(x['verdict_ok'] for x in rows)/len(rows),'false_acceptance_rate':sum(x['false_accept'] for x in rows)/sum(1 for x in rows if key[x['item_id']]['verdict']=='mismatched'),'dimension_precision':sum(x['dimension_precision'] for x in rows)/len(rows),'dimension_recall':sum(x['dimension_recall'] for x in rows)/len(rows)};(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
