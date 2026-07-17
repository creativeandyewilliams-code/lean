#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();cs=json.loads((Path(a.packet)/'candidates.json').read_text());reviews=[]
for c in cs:reviews.append({'candidate_id':c['candidate_id'],'status':c.get('fixture_status','undetermined'),'fields':{},'evidence_locators':[],'uncertainty':'fixture'})
Path(a.out).write_text(json.dumps({'reviews':reviews},indent=2))
