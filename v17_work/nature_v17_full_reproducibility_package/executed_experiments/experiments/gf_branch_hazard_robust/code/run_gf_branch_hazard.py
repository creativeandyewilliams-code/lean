#!/usr/bin/env python3
"""Robust finite branch/hazard experiment.

Three registered components:
A. finite analytic and Monte Carlo checks for summable versus non-summable hazard classes;
B. branch-correlation resilience at matched branch marginal hazard;
C. held-out discrimination among independent, correlated, regenerative, and mixed synthetic generators.

The conclusions are bounded to these generators and are not extinction-probability estimates.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path
import numpy as np

PROTOCOL={"id":"EXP-GF-BRANCH-HAZARD-ROBUST-V16","seed":2026071703,
 "hazard_horizon":5000,"hazard_c":0.12,"hazard_exponents":[0.7,1.0,1.3,1.8],
 "branch_horizon":160,"branch_replicates":12000,"branches":[1,2,4,8,16],"correlations":[0.0,0.25,0.5,0.75,1.0],
 "discrimination_worlds_per_class":100,"discrimination_replicates":180,"discrimination_branches":8,"discrimination_horizon":120,
 "claim":"finite model-regime tests and held-out generator identifiability; no external extinction estimate"}

def survival_product(h): return float(np.exp(np.log1p(-np.asarray(h)).sum()))

def simulate_branch_system(rng,h,K,rho,nrep):
    alive=np.ones((nrep,K),dtype=bool)
    for ht in h:
        common=rng.random(nrep)<rho*ht
        denom=max(1e-12,1-rho*ht); pid=(ht-rho*ht)/denom
        idio=rng.random((nrep,K))<pid
        fail=common[:,None]|idio
        alive &= ~fail
    return float(alive.any(axis=1).mean()),float(alive.mean())

def generator_events(rng,kind,reps,K,H):
    # event tensors represent per-time failures among still-active test branches; features use raw hazard indicators.
    t=np.arange(H); base=rng.uniform(0.015,0.045); trend=rng.uniform(-0.005,0.012)
    h=np.clip(base+trend*t/H,0.002,0.12)
    rho=0.0; regen=0.0
    if kind=='correlated': rho=rng.uniform(0.45,0.85)
    elif kind=='regenerative': regen=rng.uniform(1.2,2.5)
    elif kind=='mixed': rho=rng.uniform(0.25,0.55); regen=rng.uniform(0.6,1.3)
    h=np.clip(h*np.exp(-regen*np.maximum(0,t-H//3)/H),0.0002,0.25)
    ev=np.zeros((reps,K,H),dtype=np.int8)
    for j,ht in enumerate(h):
        common=rng.random(reps)<rho*ht
        pid=(ht-rho*ht)/max(1e-12,1-rho*ht)
        ev[:,:,j]=(common[:,None]|(rng.random((reps,K))<pid))
    return ev

def features(ev):
    reps,K,H=ev.shape; half=H//2; e=ev[:,:,:half]
    mean=float(e.mean()); first=float(e[:,:,:half//2].mean()); second=float(e[:,:,half//2:].mean()); trend=second-first
    # Mean pairwise branch event correlation across replicate-time observations.
    x=e.transpose(1,0,2).reshape(K,-1)
    c=np.corrcoef(x); vals=c[np.triu_indices(K,1)]; corr=float(np.nanmean(np.nan_to_num(vals)))
    dispersion=float(e.mean(axis=(0,2)).std())
    late=float(ev[:,:,half:].mean())
    return np.array([mean,trend,corr,dispersion,late],float)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); out=Path(a.out)
 for s in ['raw','derived','figures','reports']:(out/s).mkdir(parents=True,exist_ok=True)
 (out/'protocol.json').write_text(json.dumps(PROTOCOL,indent=2)); rng=np.random.default_rng(PROTOCOL['seed'])
 # A: hazard classes
 H=PROTOCOL['hazard_horizon']; c=PROTOCOL['hazard_c']; hazard_rows=[]
 for alpha in PROTOCOL['hazard_exponents']:
  t=np.arange(1,H+1); h=np.minimum(0.45,c/(t**alpha)); q=survival_product(h)
  prefix=[survival_product(h[:n]) for n in [100,500,1000,5000]]
  hazard_rows.append({'alpha':alpha,'summability_class':'non-summable' if alpha<=1 else 'summable','survival_H':q,'survival_prefix':prefix,'cumulative_hazard':float(h.sum())})
 # B: branch correlation, matched marginal hazard
 Hb=PROTOCOL['branch_horizon']; t=np.arange(1,Hb+1); h=np.minimum(.2,0.025+0.012*np.sin(t/17)**2)
 branch_rows=[]
 for K in PROTOCOL['branches']:
  for rho in PROTOCOL['correlations']:
   sys_s,branch_s=simulate_branch_system(rng,h,K,rho,PROTOCOL['branch_replicates'])
   q=survival_product(h); independent_formula=1-(1-q)**K
   branch_rows.append({'K':K,'rho':rho,'system_survival_mc':sys_s,'branch_survival_mc':branch_s,'branch_survival_formula':q,'independent_system_formula':independent_formula})
 # C: hidden generator discrimination, nearest-centroid on standardized features
 kinds=['independent','correlated','regenerative','mixed']; X=[]; y=[]; ids=[]
 for kind in kinds:
  for i in range(PROTOCOL['discrimination_worlds_per_class']):
   ev=generator_events(rng,kind,PROTOCOL['discrimination_replicates'],PROTOCOL['discrimination_branches'],PROTOCOL['discrimination_horizon'])
   X.append(features(ev)); y.append(kind); ids.append(f'{kind}_{i:03d}')
 X=np.vstack(X); y=np.array(y); idx=rng.permutation(len(y)); split=int(.7*len(y)); tr=idx[:split]; te=idx[split:]
 mu=X[tr].mean(0); sd=X[tr].std(0)+1e-12; Z=(X-mu)/sd
 cent={k:Z[tr][y[tr]==k].mean(0) for k in kinds}
 pred=[]
 for z in Z[te]: pred.append(min(kinds,key=lambda k:float(((z-cent[k])**2).sum())))
 pred=np.array(pred); acc=float((pred==y[te]).mean())
 conf={k:{j:int(((y[te]==k)&(pred==j)).sum()) for j in kinds} for k in kinds}
 # sensitivity endpoints
 corr_monotone=[]
 for K in PROTOCOL['branches']:
  vals=[next(r['system_survival_mc'] for r in branch_rows if r['K']==K and r['rho']==rho) for rho in PROTOCOL['correlations']]
  corr_monotone.append(all(vals[i]>=vals[i+1]-0.02 for i in range(len(vals)-1))) # Monte Carlo tolerance
 summary={
  'hazard_classes':hazard_rows,
  'branch_correlation':branch_rows,
  'heldout_discrimination':{'accuracy':acc,'n_train':len(tr),'n_test':len(te),'confusion':conf,'features':['early_mean','early_trend','pairwise_correlation','branch_dispersion','late_mean']},
  'registered_checks':{
    'summable_survival_exceeds_non_summable_at_H':min(r['survival_H'] for r in hazard_rows if r['summability_class']=='summable')>max(r['survival_H'] for r in hazard_rows if r['summability_class']=='non-summable'),
    'correlation_nonincreasing_system_survival_with_tolerance':all(corr_monotone),
    'heldout_generator_accuracy_above_chance':acc>0.25
  },
  'scope':PROTOCOL['claim']}
 (out/'derived'/'summary.json').write_text(json.dumps(summary,indent=2))
 with open(out/'raw'/'hazard_classes.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['alpha','summability_class','survival_H','cumulative_hazard','survival_prefix']);w.writeheader();w.writerows(hazard_rows)
 with open(out/'raw'/'branch_correlation.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=branch_rows[0].keys());w.writeheader();w.writerows(branch_rows)
 with open(out/'raw'/'generator_features.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','class','split','early_mean','early_trend','pairwise_correlation','branch_dispersion','late_mean'])
  tes=set(te.tolist())
  for i,(id_,cl,xx) in enumerate(zip(ids,y,X)):w.writerow([id_,cl,'test' if i in tes else 'train',*xx])
 # figures
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(6.8,4.0))
 for r in hazard_rows: ax.plot([100,500,1000,5000],r['survival_prefix'],marker='o',label=f"alpha={r['alpha']} ({r['summability_class']})")
 ax.set_xscale('log');ax.set_xlabel('horizon');ax.set_ylabel('survival product');ax.legend(fontsize=8,frameon=False);fig.tight_layout();fig.savefig(out/'figures'/'hazard_classes.png',dpi=180)
 fig,ax=plt.subplots(figsize=(6.8,4.0))
 K=8
 for rho in PROTOCOL['correlations']:
  r=next(x for x in branch_rows if x['K']==K and x['rho']==rho);ax.scatter(rho,r['system_survival_mc'])
 ax.plot(PROTOCOL['correlations'],[next(x['system_survival_mc'] for x in branch_rows if x['K']==K and x['rho']==r) for r in PROTOCOL['correlations']])
 ax.set_xlabel('common-shock fraction rho');ax.set_ylabel('system survival, K=8');fig.tight_layout();fig.savefig(out/'figures'/'branch_correlation.png',dpi=180)
 report=f"""# Great Filter branch/hazard finite experiment\n\n- Hazard horizon: {H}\n- Branch Monte Carlo replicates per cell: {PROTOCOL['branch_replicates']}\n- Held-out generator discrimination accuracy: {acc:.3f} (chance 0.25)\n- Summable/non-summable registered separation: {summary['registered_checks']['summable_survival_exceeds_non_summable_at_H']}\n- Correlation monotonicity within Monte Carlo tolerance: {summary['registered_checks']['correlation_nonincreasing_system_survival_with_tolerance']}\n\nThe branch experiment keeps each branch's marginal hazard fixed while varying a common-shock fraction. The hazard experiment compares frozen summability classes. The held-out task tests whether branch correlation and regeneration leave identifiable signatures rather than simply reading generator labels. These are finite synthetic model-regime results and do not estimate real extinction or observability-filter probability.\n"""
 (out/'reports'/'results.md').write_text(report)
 hh=hashlib.sha256();hh.update((out/'derived'/'summary.json').read_bytes());hh.update((out/'raw'/'generator_features.csv').read_bytes());(out/'reports'/'derived_fingerprint.txt').write_text(hh.hexdigest()+'\n')
 print(json.dumps({'accuracy':acc,'checks':summary['registered_checks']},indent=2))
if __name__=='__main__':main()
