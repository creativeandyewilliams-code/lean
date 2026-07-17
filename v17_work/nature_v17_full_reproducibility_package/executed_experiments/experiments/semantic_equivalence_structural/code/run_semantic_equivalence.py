#!/usr/bin/env python3
"""Bounded structural semantic-equivalence and cognitive-order experiment.

The experiment constructs finite typed metric functional state spaces (FSSs).
A pointed semantic signature is the truth vector of a frozen target language over:
node type, boundary, warrant, continuation, participant role, typed interaction,
and metric-threshold predicates. Admissible transformations preserve all of these
structures. Mutations alter one target-relevant structure while preserving labels.

This is a finite decision experiment over the declared generated class, not a proof
for arbitrary FSSs.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np

PROTOCOL={
 "id":"EXP-SEMANTIC-EQUIVALENCE-STRUCTURAL-V16",
 "seed":2026071701,"worlds":500,"nodes_min":6,"nodes_max":10,
 "admissible_transforms":["rename","rigid_isometry","edge_order","full_iso"],
 "mutations":["metric","edge_type","boundary","warrant","continuation","role"],
 "metric_thresholds":[1.25,2.0,3.0],
 "claim":"bounded invariance/sensitivity within the generated finite FSS class"
}
NODE_TYPES=["concept","process","boundary"]
EDGE_TYPES=["Register","Recall","L","G"]
BOUNDARIES=["open","closed"]
WARRANTS=["definition","theorem","external"]
ROLES=["participant","observer","executor"]

@dataclass
class World:
    ids:list[str]; node_type:list[str]; boundary:list[str]; warrant:list[str]
    continuation:list[int]; role:list[str]; coords:list[list[float]]
    edges:list[tuple[int,int,str]]; effects:list[tuple[int,...]]

def dist(w,i,j):
    a=np.asarray(w.coords[i]); b=np.asarray(w.coords[j]); return float(np.linalg.norm(a-b))

def formulas(w, point, thresholds):
    out=[]
    for x in NODE_TYPES: out.append((f"node_type={x}",w.node_type[point]==x))
    for x in BOUNDARIES: out.append((f"boundary={x}",w.boundary[point]==x))
    for x in WARRANTS: out.append((f"warrant={x}",w.warrant[point]==x))
    for x in [0,1]: out.append((f"continuation={x}",w.continuation[point]==x))
    for x in ROLES: out.append((f"role={x}",w.role[point]==x))
    for et in EDGE_TYPES:
        out.append((f"out_edge_type={et}", any(a==point and t==et for a,b,t in w.edges)))
        out.append((f"in_edge_type={et}", any(b==point and t==et for a,b,t in w.edges)))
    for th in thresholds:
        out.append((f"exists_metric_le={th}", any(j!=point and dist(w,point,j)<=th for j in range(len(w.ids)))))
        out.append((f"exists_same_type_metric_le={th}", any(j!=point and w.node_type[j]==w.node_type[point] and dist(w,point,j)<=th for j in range(len(w.ids)))))
    for et in EDGE_TYPES:
        for th in thresholds:
            out.append((f"typed_neighbor={et}@{th}", any(a==point and t==et and dist(w,a,b)<=th for a,b,t in w.edges)))
    return out

def signature(w, point):
    return tuple(v for _,v in formulas(w,point,PROTOCOL['metric_thresholds']))

def make_world(rng):
    n=int(rng.integers(PROTOCOL['nodes_min'],PROTOCOL['nodes_max']+1))
    ids=[f"n{i}" for i in range(n)]
    nt=list(rng.choice(NODE_TYPES,n)); bd=list(rng.choice(BOUNDARIES,n)); wa=list(rng.choice(WARRANTS,n))
    co=[int(x) for x in rng.integers(0,2,n)]; ro=list(rng.choice(ROLES,n))
    coords=rng.normal(0,1.5,(n,3)).round(8).tolist()
    edges=[]
    for i in range(n):
        for j in range(n):
            if i!=j and rng.random()<0.20:
                edges.append((i,j,str(rng.choice(EDGE_TYPES))))
    if not edges: edges=[(0,1,"L")]
    # finite composition effects over four target bits; duplicates define equivalence classes
    effects=[]
    for _ in range(int(rng.integers(4,10))):
        effects.append(tuple(int(x) for x in rng.integers(0,2,4)))
    return World(ids,nt,bd,wa,co,ro,coords,edges,effects)

def remap_world(w,perm,R=None,shift=None,edge_shuffle=False):
    n=len(w.ids); inv={old:new for new,old in enumerate(perm)}
    coords=np.asarray([w.coords[old] for old in perm],float)
    if R is not None: coords=coords@R.T
    if shift is not None: coords=coords+shift
    edges=[(inv[a],inv[b],t) for a,b,t in w.edges]
    if edge_shuffle: edges=list(reversed(edges))
    return World(["x"+str(i) for i in range(n)], [w.node_type[o] for o in perm], [w.boundary[o] for o in perm],
                 [w.warrant[o] for o in perm], [w.continuation[o] for o in perm], [w.role[o] for o in perm],
                 coords.round(8).tolist(), edges, list(w.effects)), inv

def random_orthogonal(rng):
    q,r=np.linalg.qr(rng.normal(size=(3,3))); q=q@np.diag(np.sign(np.diag(r))); return q

def admissible(w,point,name,rng):
    n=len(w.ids)
    if name=="rename": perm=list(range(n)); return remap_world(w,perm)[0],point
    if name=="rigid_isometry":
        R=random_orthogonal(rng); shift=rng.normal(size=3); nw,inv=remap_world(w,list(range(n)),R,shift); return nw,point
    if name=="edge_order":
        nw,inv=remap_world(w,list(range(n)),edge_shuffle=True); return nw,point
    perm=list(rng.permutation(n)); nw,inv=remap_world(w,perm,random_orthogonal(rng),rng.normal(size=3),True); return nw,inv[point]

def witness_diff(w1,p1,w2,p2):
    a=formulas(w1,p1,PROTOCOL['metric_thresholds']); b=formulas(w2,p2,PROTOCOL['metric_thresholds'])
    for (la,va),(lb,vb) in zip(a,b):
        assert la==lb
        if va!=vb: return la,va,vb
    return None

def mutate(w,point,name,rng):
    # copy
    nw=World(list(w.ids),list(w.node_type),list(w.boundary),list(w.warrant),list(w.continuation),list(w.role),
             [list(x) for x in w.coords],list(w.edges),list(w.effects))
    if name=="boundary": nw.boundary[point]="closed" if nw.boundary[point]=="open" else "open"
    elif name=="warrant": nw.warrant[point]=next(x for x in WARRANTS if x!=nw.warrant[point])
    elif name=="continuation": nw.continuation[point]=1-nw.continuation[point]
    elif name=="role": nw.role[point]=next(x for x in ROLES if x!=nw.role[point])
    elif name=="edge_type":
        # Toggle the presence of an outgoing G edge, guaranteeing a target-language change.
        had=any(a==point and t=="G" for a,b,t in nw.edges)
        nw.edges=[e for e in nw.edges if not (e[0]==point and e[2]=="G")]
        if not had:
            j=(point+1)%len(nw.ids); nw.edges.append((point,j,"G"))
    elif name=="metric":
        # Use a unique outgoing G edge so crossing thresholds is necessarily visible.
        had_close=any(a==point and t=="G" and dist(w,a,b)<=max(PROTOCOL['metric_thresholds']) for a,b,t in w.edges)
        nw.edges=[e for e in nw.edges if not (e[0]==point and e[2]=="G")]
        j=min((j for j in range(len(nw.ids)) if j!=point), key=lambda j:dist(nw,point,j))
        nw.edges.append((point,j,"G"))
        # force the max-threshold G-neighbor predicate to flip.
        if had_close:
            v=np.asarray(nw.coords[j])-np.asarray(nw.coords[point]);
            if np.linalg.norm(v)<1e-8: v=np.array([1.,0.,0.])
            nw.coords[j]=(np.asarray(nw.coords[point])+v/np.linalg.norm(v)*10.0).tolist()
        else:
            nw.coords[j]=(np.asarray(nw.coords[point])+np.array([0.1,0,0])).tolist()
    return nw

def order(w): return len(set(w.effects))

def effect_reencode(w,rng):
    # bijective permutation of target coordinates and ordering of compositions
    p=list(rng.permutation(4)); eff=[tuple(e[i] for i in p) for e in w.effects]; rng.shuffle(eff)
    nw=World(list(w.ids),list(w.node_type),list(w.boundary),list(w.warrant),list(w.continuation),list(w.role),[list(x) for x in w.coords],list(w.edges),eff)
    return nw

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); out=Path(a.out)
    for s in ['raw','derived','reports']: (out/s).mkdir(parents=True,exist_ok=True)
    (out/'protocol.json').write_text(json.dumps(PROTOCOL,indent=2))
    rng=np.random.default_rng(PROTOCOL['seed']); rows=[]; order_rows=[]
    for wid in range(PROTOCOL['worlds']):
        w=make_world(rng); point=int(rng.integers(0,len(w.ids))); sig=signature(w,point)
        for tr in PROTOCOL['admissible_transforms']:
            nw,npnt=admissible(w,point,tr,rng); same=signature(nw,npnt)==sig
            rows.append([wid,'admissible',tr,int(same),''])
        for mut in PROTOCOL['mutations']:
            nw=mutate(w,point,mut,rng); wit=witness_diff(w,point,nw,point); detected=wit is not None
            rows.append([wid,'mutation',mut,int(detected),'' if wit is None else wit[0]])
        ow=order(w); rw=effect_reencode(w,rng); order_rows.append([wid,ow,order(rw),int(ow==order(rw))])
        # noninjective collapse countermodel: replace all effects by first class
        cw=World(**asdict(w)); cw.effects=[w.effects[0] for _ in w.effects]
        order_rows.append([wid,ow,order(cw),int(ow!=order(cw))])
    with open(out/'raw'/'case_results.csv','w',newline='') as f:
        cw=csv.writer(f); cw.writerow(['world','class','operation','passed','shortest_witness']); cw.writerows(rows)
    with open(out/'raw'/'order_results.csv','w',newline='') as f:
        cw=csv.writer(f); cw.writerow(['world','base_order','transformed_order','expected_relation_passed']); cw.writerows(order_rows)
    admiss=[r for r in rows if r[1]=='admissible']; muts=[r for r in rows if r[1]=='mutation']
    byop={}
    for r in rows: byop.setdefault(r[2],[]).append(r[3])
    summary={
      'worlds':PROTOCOL['worlds'],'admissible_cases':len(admiss),'mutation_cases':len(muts),
      'admissible_invariance_rate':sum(r[3] for r in admiss)/len(admiss),
      'mutation_detection_rate':sum(r[3] for r in muts)/len(muts),
      'order_relation_pass_rate':sum(r[3] for r in order_rows)/len(order_rows),
      'operation_rates':{k:sum(v)/len(v) for k,v in sorted(byop.items())},
      'scope':'finite generated FSSs and frozen bounded target language'
    }
    (out/'derived'/'summary.json').write_text(json.dumps(summary,indent=2))
    report=f"""# Structural semantic-equivalence experiment\n\n- Worlds: {PROTOCOL['worlds']}\n- Admissible cases: {len(admiss)}\n- Admissible invariance: {summary['admissible_invariance_rate']:.4f}\n- Target-relevant mutation detection: {summary['mutation_detection_rate']:.4f}\n- Cognitive-order admissible/countermodel relation pass rate: {summary['order_relation_pass_rate']:.4f}\n\nThe experiment evaluates a frozen target language over metric, typed interaction, boundary, warrant, continuation, and participant-role structure. Admissible renamings/isometries/isomorphisms must preserve the complete truth signature. Label-preserving target-relevant mutations must change at least one registered formula and emit a shortest distinguishing witness. The order test counts distinct finite functional-effect classes and verifies preservation under bijective re-encoding while detecting noninjective collapse.\n\nThis is a bounded finite decision result, not universal semantic proof closure.\n"""
    (out/'reports'/'results.md').write_text(report)
    h=hashlib.sha256(); h.update((out/'derived'/'summary.json').read_bytes()); h.update((out/'raw'/'case_results.csv').read_bytes()); h.update((out/'raw'/'order_results.csv').read_bytes())
    (out/'reports'/'derived_fingerprint.txt').write_text(h.hexdigest()+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
