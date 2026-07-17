#!/usr/bin/env python3
"""Finite CST computational geometry experiment.

Tests discrete semantic transport and holonomy under node relabelling, Euclidean
isometry, and gauge transformation; detects transport, metric, and interaction
mutations; and verifies least consequence closure by fixed-point iteration.
"""
from __future__ import annotations
import argparse,csv,hashlib,heapq,json
from pathlib import Path
import numpy as np
PROTOCOL={"id":"EXP-CST-COMPUTATIONAL-GEOMETRY-V16","seed":2026071704,"worlds":600,"nodes_min":7,"nodes_max":13,"transport_modulus":17,"claim":"finite computational invariance/sensitivity"}
EDGE_TYPES=['Register','Recall','L','G']

def make_world(rng):
 n=int(rng.integers(PROTOCOL['nodes_min'],PROTOCOL['nodes_max']+1)); coords=rng.normal(size=(n,3))
 edges=[]
 # directed ring guarantees a cycle
 for i in range(n): edges.append([i,(i+1)%n,str(rng.choice(EDGE_TYPES)),int(rng.integers(0,17))])
 used={(e[0],e[1]) for e in edges}
 for i in range(n):
  for j in range(n):
   if i!=j and (i,j) not in used and rng.random()<.12:
    edges.append([i,j,str(rng.choice(EDGE_TYPES)),int(rng.integers(0,17))]); used.add((i,j))
 seeds=set(int(x) for x in rng.choice(n,size=max(1,n//4),replace=False))
 return {'n':n,'coords':coords,'edges':edges,'seeds':seeds,'cycle':list(range(n))+[0]}

def edge_map(w): return {(a,b):(typ,tr) for a,b,typ,tr in w['edges']}
def cycle_holonomy(w,cyc):
 em=edge_map(w); return sum(em[(a,b)][1] for a,b in zip(cyc[:-1],cyc[1:]))%PROTOCOL['transport_modulus']
def typed_cycle(w,cyc):
 em=edge_map(w); return tuple(em[(a,b)][0] for a,b in zip(cyc[:-1],cyc[1:]))
def closure(w):
 # Monotone consequence operator: a node enters when reachable by a directed edge from closure.
 cur=set(w['seeds']); changed=True
 while changed:
  changed=False
  for a,b,t,tr in w['edges']:
   if a in cur and b not in cur: cur.add(b);changed=True
 return cur

def dijkstra(w,src):
 n=w['n']; adj=[[] for _ in range(n)]
 for a,b,t,tr in w['edges']:
  d=float(np.linalg.norm(w['coords'][a]-w['coords'][b]));adj[a].append((b,d))
 dist=[float('inf')]*n;dist[src]=0;heap=[(0,src)]
 while heap:
  d,u=heapq.heappop(heap)
  if d!=dist[u]:continue
  for v,c in adj[u]:
   nd=d+c
   if nd<dist[v]:dist[v]=nd;heapq.heappush(heap,(nd,v))
 return dist

def transform(w,rng):
 n=w['n'];perm=list(rng.permutation(n));inv={old:new for new,old in enumerate(perm)}
 q,_=np.linalg.qr(rng.normal(size=(3,3)));shift=rng.normal(size=3);phi=rng.integers(0,17,n)
 coords=np.asarray([w['coords'][o] for o in perm])@q.T+shift
 edges=[]
 for a,b,t,tr in w['edges']:
  # gauge transformation preserves cycle holonomy
  edges.append([inv[a],inv[b],t,int((tr+phi[b]-phi[a])%17)])
 cyc=[inv[x] for x in w['cycle']]
 return {'n':n,'coords':coords,'edges':edges,'seeds':{inv[x] for x in w['seeds']},'cycle':cyc},inv

def mutate_transport(w):
 nw={'n':w['n'],'coords':w['coords'].copy(),'edges':[list(e) for e in w['edges']],'seeds':set(w['seeds']),'cycle':list(w['cycle'])};nw['edges'][0][3]=(nw['edges'][0][3]+1)%17;return nw

def mutate_type(w):
 nw={'n':w['n'],'coords':w['coords'].copy(),'edges':[list(e) for e in w['edges']],'seeds':set(w['seeds']),'cycle':list(w['cycle'])};old=nw['edges'][0][2];nw['edges'][0][2]=next(x for x in EDGE_TYPES if x!=old);return nw

def mutate_metric(w):
 nw={'n':w['n'],'coords':w['coords'].copy(),'edges':[list(e) for e in w['edges']],'seeds':set(w['seeds']),'cycle':list(w['cycle'])};nw['coords'][1]=nw['coords'][1]+np.array([20.,0,0]);return nw

def direct_json(w):
 return json.dumps({'coords':np.asarray(w['coords']).round(8).tolist(),'edges':w['edges'],'seeds':sorted(w['seeds'])},sort_keys=True)
def worldsheet_json(w):
 # Explicit cycle path plus transport/type sequence and metric edge lengths.
 em=edge_map(w);cyc=w['cycle'];return json.dumps({'path':cyc,'types':[em[(a,b)][0] for a,b in zip(cyc[:-1],cyc[1:])],'transport':[em[(a,b)][1] for a,b in zip(cyc[:-1],cyc[1:])],'lengths':[round(float(np.linalg.norm(w['coords'][a]-w['coords'][b])),8) for a,b in zip(cyc[:-1],cyc[1:])]},sort_keys=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out)
 for s in ['raw','derived','reports']:(out/s).mkdir(parents=True,exist_ok=True)
 (out/'protocol.json').write_text(json.dumps(PROTOCOL,indent=2));rng=np.random.default_rng(PROTOCOL['seed']);rows=[]
 for wid in range(PROTOCOL['worlds']):
  w=make_world(rng);tw,inv=transform(w,rng)
  hol=cycle_holonomy(w,w['cycle']);thol=cycle_holonomy(tw,tw['cycle'])
  typ=typed_cycle(w,w['cycle']);ttyp=typed_cycle(tw,tw['cycle'])
  clo=closure(w);tclo=closure(tw)
  closure_ok={inv[x] for x in clo}==tclo
  # path reassociation in an abelian transport is equality of grouped sums
  transports=[edge_map(w)[(a,b)][1] for a,b in zip(w['cycle'][:-1],w['cycle'][1:])]
  mid=len(transports)//2;assoc_ok=(sum(transports)%17)==((sum(transports[:mid])+sum(transports[mid:]))%17)
  mt=mutate_transport(w);me=mutate_type(w);mm=mutate_metric(w)
  d0=dijkstra(w,0);dm=dijkstra(mm,0);metric_detect=any((np.isfinite(x) and np.isfinite(y) and abs(x-y)>1e-8) for x,y in zip(d0,dm))
  rows.append([wid,int(hol==thol),int(typ==ttyp),int(closure_ok),int(assoc_ok),int(cycle_holonomy(mt,mt['cycle'])!=hol),int(typed_cycle(me,me['cycle'])!=typ),int(metric_detect),len(direct_json(w).encode()),len(worldsheet_json(w).encode())])
 with open(out/'raw'/'case_results.csv','w',newline='') as f:
  cw=csv.writer(f);cw.writerow(['world','holonomy_iso_gauge','typed_cycle_iso','closure_iso','path_association','transport_mutation_detected','edge_type_mutation_detected','metric_mutation_detected','direct_graph_bytes','worldsheet_cycle_bytes']);cw.writerows(rows)
 arr=np.asarray([r[1:8] for r in rows],float);summary={'worlds':len(rows),'rates':{k:float(arr[:,i].mean()) for i,k in enumerate(['holonomy_iso_gauge','typed_cycle_iso','closure_iso','path_association','transport_mutation_detected','edge_type_mutation_detected','metric_mutation_detected'])},'representation_bytes':{'direct_graph_mean':float(np.mean([r[8] for r in rows])),'worldsheet_cycle_mean':float(np.mean([r[9] for r in rows]))},'scope':PROTOCOL['claim']}
 (out/'derived'/'summary.json').write_text(json.dumps(summary,indent=2))
 (out/'reports'/'results.md').write_text(f"""# CST computational geometry experiment\n\n- Worlds: {len(rows)}\n- Holonomy invariance under isomorphism plus gauge: {summary['rates']['holonomy_iso_gauge']:.4f}\n- Typed-cycle invariance: {summary['rates']['typed_cycle_iso']:.4f}\n- Least consequence-closure invariance: {summary['rates']['closure_iso']:.4f}\n- Transport mutation detection: {summary['rates']['transport_mutation_detected']:.4f}\n- Metric mutation detection: {summary['rates']['metric_mutation_detected']:.4f}\n\nThe experiment checks finite discrete transport and closure properties. It does not measure human or model receiver utility of CST; that remains a separate multi-agent experiment.\n""")
 h=hashlib.sha256();h.update((out/'derived'/'summary.json').read_bytes());h.update((out/'raw'/'case_results.csv').read_bytes());(out/'reports'/'derived_fingerprint.txt').write_text(h.hexdigest()+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
