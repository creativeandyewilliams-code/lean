#!/usr/bin/env python3
from pathlib import Path
import argparse,json,collections,random
ap=argparse.ArgumentParser();ap.add_argument('--test',required=True);ap.add_argument('--out',required=True);ap.add_argument('--bootstrap',type=int,default=2000);a=ap.parse_args();rows=[json.loads(x) for x in Path(a.test).read_text().splitlines() if x.strip()]
# Requires externally scored fields: correct, false_promotion, missing_premise_recovered.
for r in rows:
 for k in ['correct','false_promotion','missing_premise_recovered']:
  if k not in r:raise SystemExit(f'missing scored field {k}')
g=collections.defaultdict(list)
for r in rows:g[r['condition']].append(r)
summary={c:{'n':len(v),'accuracy':sum(x['correct'] for x in v)/len(v),'false_promotion_rate':sum(x['false_promotion'] for x in v)/len(v),'missing_premise_rate':sum(x['missing_premise_recovered'] for x in v)/len(v)} for c,v in g.items()}
out=Path(a.out);out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
