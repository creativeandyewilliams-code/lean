#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,random,shutil
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
config=json.loads((root/'config.json').read_text());tasks=json.loads((root/'task_bank.json').read_text());A=[t for t in tasks if t['variant']=='A'];B={t['family']:t for t in tasks if t['variant']=='B'}
rng=random.Random(config['seed']);plan={'experiment_id':config['experiment_id'],'runs':[]}
for cond in config['conditions']:
 mat=root/'materials'/'conditions'/next(p.name for p in (root/'materials'/'conditions').iterdir() if p.stem==cond)
 for i in range(config['receiver_A_instances_per_condition']):
  rid=f'RA__{cond}__{i+1:02d}'; packet=out/'receiver_A'/rid;packet.mkdir(parents=True,exist_ok=True)
  shuffled=list(A);rng.shuffle(shuffled)
  (packet/('condition'+mat.suffix)).write_bytes(mat.read_bytes());(packet/'hidden_tasks.json').write_text(json.dumps(shuffled,indent=2));(packet/'instructions.md').write_text((root/'prompts/receiver_A.md').read_text())
  allowed=[p.name for p in packet.iterdir()]
  rbs=[]
  for j in range(config['receiver_B_instances_per_transmission']):
   bid=f'RB__{rid}__{j+1:02d}'; bp=out/'receiver_B'/bid;bp.mkdir(parents=True,exist_ok=True)
   btask=[B[t['family']] for t in shuffled];rng.shuffle(btask)
   (bp/'hidden_tasks.json').write_text(json.dumps(btask,indent=2));(bp/'instructions.md').write_text((root/'prompts/receiver_B.md').read_text());rbs.append(bid)
  plan['runs'].append({'receiver_A':rid,'condition':cond,'receiver_A_packet':str(packet.relative_to(out)),'receiver_B':rbs,'allowed_files':allowed})
(out/'run_plan.json').write_text(json.dumps(plan,indent=2))
h=hashlib.sha256()
for p in sorted(out.rglob('*')):
 if p.is_file():h.update(str(p.relative_to(out)).encode()+b'\0'+p.read_bytes())
(out/'packet_manifest.sha256').write_text(h.hexdigest()+'\n');print(json.dumps({'receiver_A_runs':len(plan['runs']),'receiver_B_runs':sum(len(x['receiver_B']) for x in plan['runs'])},indent=2))
