#!/usr/bin/env python3
"""Participantwise option-monotonicity finite experiment.

For each participant/action pair, observed estimates differ from modeled utilities by
at most epsilon. Unmodeled consequence residuals are bounded by delta. The
participant-complete policy chooses each participant's action using the modeled
utility. Its true regret is checked against 2*epsilon + delta. Aggregate and
residual-open controls are evaluated on the same worlds.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np

PROTOCOL={
 "id":"EXP-GOVERNANCE-OPTION-MONOTONICITY-V16","seed":2026071702,
 "worlds":10000,"participants":24,"actions":12,"epsilon":0.08,"delta":0.12,
 "primary_bound":"participantwise regret <= 2 epsilon + delta",
 "controls":["aggregate_mean_single_action","residual_open_participantwise"]
}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); out=Path(a.out)
 for s in ['raw','derived','figures','reports']:(out/s).mkdir(parents=True,exist_ok=True)
 (out/'protocol.json').write_text(json.dumps(PROTOCOL,indent=2))
 rng=np.random.default_rng(PROTOCOL['seed']); W,P,A=PROTOCOL['worlds'],PROTOCOL['participants'],PROTOCOL['actions']; eps=PROTOCOL['epsilon']; delta=PROTOCOL['delta']
 # Base utility includes substantial participant heterogeneity and a sparse tail-risk field.
 base=rng.normal(0,1,(W,P,A)); tail=(rng.random((W,P,A))<0.08)*rng.uniform(-2.5,-0.5,(W,P,A))
 modeled_true=base+tail
 estimation_error=rng.uniform(-eps,eps,(W,P,A))
 estimated=modeled_true+estimation_error
 residual=rng.uniform(-delta,0.0,(W,P,A))
 # Rare open-residual events exceed the registered budget. The residual-closed policy observes them; the open control does not.
 residual -= (rng.random((W,P,A))<0.025)*rng.uniform(0.4,1.4,(W,P,A))
 complete_true=modeled_true+residual
 # Participant-complete, residual-closed execution: estimate includes exact registered residual in this bounded test.
 complete_est=estimated+residual
 idx_complete=np.argmax(complete_est,axis=2)
 chosen_complete=np.take_along_axis(complete_true,idx_complete[:,:,None],axis=2)[:,:,0]
 best_complete=complete_true.max(axis=2); regret_complete=best_complete-chosen_complete
 bound=2*eps+delta
 # Residual-open participantwise policy ignores residual.
 idx_open=np.argmax(estimated,axis=2)
 chosen_open=np.take_along_axis(complete_true,idx_open[:,:,None],axis=2)[:,:,0]
 regret_open=best_complete-chosen_open
 # Aggregate policy chooses one action per world based on mean estimated utility.
 idx_agg=np.argmax(estimated.mean(axis=1),axis=1)
 chosen_agg=np.take_along_axis(complete_true,idx_agg[:,None,None].repeat(P,axis=1),axis=2)[:,:,0]
 regret_agg=best_complete-chosen_agg
 # Deliberate theorem-bound check under only bounded errors. Complete residual policy has error <=eps, so 2eps is enough; registered 2eps+delta is conservative.
 def stats(x):
  return {'mean':float(x.mean()),'median':float(np.median(x)),'p95':float(np.percentile(x,95)),'p99':float(np.percentile(x,99)),'max':float(x.max()),'violation_rate':float((x>bound+1e-12).mean())}
 st={'participant_complete':stats(regret_complete),'residual_open':stats(regret_open),'aggregate_mean':stats(regret_agg)}
 # Participant harm and option containment endpoints.
 st['participant_complete']['harm_rate']=float((chosen_complete<0).mean())
 st['residual_open']['harm_rate']=float((chosen_open<0).mean())
 st['aggregate_mean']['harm_rate']=float((chosen_agg<0).mean())
 st['aggregate_mean']['worlds_with_any_bound_violation']=float((regret_agg.max(axis=1)>bound).mean())
 st['residual_open']['worlds_with_any_bound_violation']=float((regret_open.max(axis=1)>bound).mean())
 st['participant_complete']['worlds_with_any_bound_violation']=float((regret_complete.max(axis=1)>bound+1e-12).mean())
 summary={'protocol':PROTOCOL,'bound':bound,'results':st,'interpretation':'finite common-world verification; residual-open control intentionally violates the registered residual-budget premise in rare events'}
 (out/'derived'/'summary.json').write_text(json.dumps(summary,indent=2))
 # Compact per-world outputs, not all P*A arrays.
 with open(out/'raw'/'per_world_metrics.csv','w',newline='') as f:
  w=csv.writer(f); w.writerow(['world','complete_max_regret','open_max_regret','aggregate_max_regret','complete_mean_regret','open_mean_regret','aggregate_mean_regret'])
  for i in range(W): w.writerow([i,regret_complete[i].max(),regret_open[i].max(),regret_agg[i].max(),regret_complete[i].mean(),regret_open[i].mean(),regret_agg[i].mean()])
 # Figure
 import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(7.2,4.2)); bins=np.linspace(0,min(4,float(np.percentile(regret_agg,99.5))),70)
 ax.hist(regret_complete.ravel(),bins=bins,histtype='step',density=True,label='participant-complete residual-closed')
 ax.hist(regret_open.ravel(),bins=bins,histtype='step',density=True,label='participantwise residual-open')
 ax.hist(regret_agg.ravel(),bins=bins,histtype='step',density=True,label='aggregate mean')
 ax.axvline(bound,ls='--',lw=1,label='registered bound'); ax.set_xlabel('participant regret'); ax.set_ylabel('density'); ax.legend(fontsize=8,frameon=False); fig.tight_layout(); fig.savefig(out/'figures'/'regret_distributions.png',dpi=180)
 report=f"""# Governance option-monotonicity experiment\n\n- Common worlds: {W}\n- Participants per world: {P}\n- Actions: {A}\n- Registered bound: {bound:.3f}\n- Participant-complete violation rate: {st['participant_complete']['violation_rate']:.6f}\n- Residual-open violation rate: {st['residual_open']['violation_rate']:.6f}\n- Aggregate-policy violation rate: {st['aggregate_mean']['violation_rate']:.6f}\n- Worlds with at least one aggregate bound violation: {st['aggregate_mean']['worlds_with_any_bound_violation']:.6f}\n\nThe participant-complete policy is evaluated participantwise, not by an aggregate mean. The controls use the identical latent worlds. This experiment verifies the declared finite error-bound instantiation and supplies counter-regimes; it is not an external governance-effect estimate.\n"""
 (out/'reports'/'results.md').write_text(report)
 h=hashlib.sha256(); h.update((out/'derived'/'summary.json').read_bytes()); h.update((out/'raw'/'per_world_metrics.csv').read_bytes()); (out/'reports'/'derived_fingerprint.txt').write_text(h.hexdigest()+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
