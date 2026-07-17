#!/usr/bin/env python3
from pathlib import Path
import argparse,json,random
ap=argparse.ArgumentParser();ap.add_argument('--candidates',required=True);ap.add_argument('--out',required=True);ap.add_argument('--reviewers',type=int,default=3);a=ap.parse_args();root=Path(__file__).resolve().parents[1];c=json.loads(Path(a.candidates).read_text());out=Path(a.out);out.mkdir(parents=True,exist_ok=True);rng=random.Random(2026071709)
for i in range(a.reviewers):
 arr=list(c);rng.shuffle(arr);p=out/f'HIST_REVIEWER_{i+1:02d}';p.mkdir();(p/'candidates.json').write_text(json.dumps(arr,indent=2));(p/'rubric.json').write_text((root/'rubric.json').read_text());(p/'instructions.md').write_text((root/'prompts/reviewer.md').read_text())
