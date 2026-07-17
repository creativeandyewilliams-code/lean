#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True);maps=json.loads((root/'candidate_mappings.json').read_text())
for m in maps:
 for role in ['proponent','adversary']:
  p=out/f"{role.upper()}__{m['mapping_id']}";p.mkdir();(p/'candidate.json').write_text(json.dumps(m,indent=2));(p/'schema.json').write_text((root/'schema/mapping_certificate.schema.json').read_text());(p/'instructions.md').write_text((root/f'prompts/{role}.md').read_text())
