#!/usr/bin/env python3
from pathlib import Path
import argparse,json,random,hashlib,math
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True);cfg=json.loads((root/'config.json').read_text());rng=random.Random(cfg['seed'])
worlds=[];key={}
for wid in range(cfg['worlds']):
 n=6; coords=[[round(rng.uniform(-2,2),3),round(rng.uniform(-2,2),3)] for _ in range(n)];edges=[]
 for i in range(n):edges.append([i,(i+1)%n,rng.choice(['Register','Recall','L','G']),rng.randrange(11)])
 # one chord
 edges.append([0,3,'G',rng.randrange(11)]); boundary=[rng.choice(['open','closed']) for _ in range(n)];warrant=[rng.choice(['definition','theorem','external']) for _ in range(n)];seeds=[0]
 cycle=list(range(n))+[0]; em={(u,v):(t,z) for u,v,t,z in edges};hol=sum(em[(u,v)][1] for u,v in zip(cycle[:-1],cycle[1:]))%11
 closure=set(seeds);changed=True
 while changed:
  changed=False
  for u,v,t,z in edges:
   if u in closure and v not in closure:closure.add(v);changed=True
 # mutation alternates metric, transport, boundary, edge type
 mtype=['metric','transport','boundary','edge_type'][wid%4]
 drift=True
 task_id=f'CST-W{wid:02d}'
 worlds.append({'task_id':task_id,'coords':coords,'edges':edges,'boundary':boundary,'warrant':warrant,'seeds':seeds,'cycle':cycle,'mutation':mtype})
 key[task_id]={'verdict':'mutation_changes_semantics','holonomy':hol,'closure':sorted(closure),'drift_detected':drift,'semantic_signature':[boundary[0],warrant[0],em[(0,1)][0]]}
(root/'sealed/answer_key.json').write_text(json.dumps(key,indent=2))
plan=[]
for cond in cfg['conditions']:
 for i in range(cfg['receiver_instances_per_condition']):
  rid=f'CST__{cond}__{i+1:02d}';p=out/rid;p.mkdir(parents=True)
  packet=[]
  for w in worlds:
   base={'task_id':w['task_id'],'question':'Compute the declared semantic signature, cycle holonomy mod 11, consequence closure, and decide whether the registered mutation changes semantics.','mutation':w['mutation']}
   if cond=='prose_only':base['representation']=f"Six nodes form a directed cycle. Coordinates={w['coords']}; typed edges={w['edges']}; boundaries={w['boundary']}; warrants={w['warrant']}; seed node=0."
   elif cond=='registry_only':base['representation']={'nodes':list(range(6)),'boundary':w['boundary'],'warrant':w['warrant'],'metric_coords':w['coords'],'typed_edges':w['edges'],'closure_seed':w['seeds']}
   elif cond=='direct_graph_plus_lean':base['representation']={'typed_graph':w,'rules':['transport sums mod 11','closure is least directed reachability fixed point','metric/interaction/boundary mutations are target relevant']}
   elif cond in ('cst_plus_lean','cst_optional_action'):
    em={(u,v):(t,z) for u,v,t,z in w['edges']};base['representation']={'worldsheet_path':w['cycle'],'path_types':[em[(u,v)][0] for u,v in zip(w['cycle'][:-1],w['cycle'][1:])],'transport':[em[(u,v)][1] for u,v in zip(w['cycle'][:-1],w['cycle'][1:])],'metric_coords':w['coords'],'boundary':w['boundary'],'warrant':w['warrant'],'closure_edges':w['edges'],'optional_action':('rank by length after hard admissibility' if cond=='cst_optional_action' else None)}
   else:base['representation']={'worldsheet_path':w['cycle'],'path_types':[e[2] for e in w['edges'][:6]],'ablation':rng.choice(['no_metric','no_transport','no_closure','no_boundary'])}
   packet.append(base)
  (p/'tasks.json').write_text(json.dumps(packet,indent=2));(p/'instructions.md').write_text((root/'prompts/receiver.md').read_text());plan.append({'run_id':rid,'condition':cond,'packet':str(p.relative_to(out))})
(out/'run_plan.json').write_text(json.dumps(plan,indent=2));h=hashlib.sha256();
for p in sorted(out.rglob('*')):
 if p.is_file():h.update(str(p.relative_to(out)).encode()+p.read_bytes())
(out/'packet_manifest.sha256').write_text(h.hexdigest()+'\n')
