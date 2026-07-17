#!/usr/bin/env python3
from pathlib import Path
import argparse,json,random,hashlib
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True);cfg=json.loads((root/'config.json').read_text());items=json.loads((root/'pair_bank.json').read_text());rng=random.Random(cfg['seed']);plan=[]
for r in range(cfg['reviewers_per_item']):
 arr=list(items);rng.shuffle(arr);rid=f'FIDELITY_REVIEWER_{r+1:02d}';p=out/rid;p.mkdir();(p/'blinded_pairs.json').write_text(json.dumps(arr,indent=2));(p/'instructions.md').write_text((root/'prompts/reviewer.md').read_text());plan.append({'reviewer':rid,'packet':str(p.relative_to(out))})
(out/'run_plan.json').write_text(json.dumps(plan,indent=2));h=hashlib.sha256();
for p in sorted(out.rglob('*')):
 if p.is_file():h.update(str(p.relative_to(out)).encode()+p.read_bytes())
(out/'packet_manifest.sha256').write_text(h.hexdigest()+'\n')
