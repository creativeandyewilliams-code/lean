#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--packets',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
for p in Path(a.packets).glob('PROPONENT__*'):
 m=json.loads((p/'candidate.json').read_text());d={**m,'scale_regime':'fixture','support_definition':'fixture support','factorization_witness':'fixture witness','schedule_witness':'fixture schedule','topological_consequence':'fixture topology','cross_fss_invariant':'fixture invariant','defeaters':['fixture defeater'],'evidence_sources':['fixture source'],'status':'undetermined'};(out/f"{m['mapping_id']}.json").write_text(json.dumps(d,indent=2))
