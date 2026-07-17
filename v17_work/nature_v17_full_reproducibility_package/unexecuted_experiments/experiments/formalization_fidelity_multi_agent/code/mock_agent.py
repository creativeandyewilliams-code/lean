#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True);ap.add_argument('--key',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();items=json.loads((Path(a.packet)/'blinded_pairs.json').read_text());key=json.loads(Path(a.key).read_text());reviews=[{'item_id':x['item_id'],'verdict':key[x['item_id']]['verdict'],'mismatch_dimensions':key[x['item_id']]['mismatch_dimensions'],'counterexample':'mock','confidence':1} for x in items];Path(a.out).write_text(json.dumps({'reviewer_id':'MOCK','reviews':reviews},indent=2))
