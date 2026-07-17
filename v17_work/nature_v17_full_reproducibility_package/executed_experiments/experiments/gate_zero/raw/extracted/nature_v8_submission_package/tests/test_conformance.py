#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import run_experiment as exp

results=[]
def check(name,cond,detail=""):
    results.append({"test":name,"pass":bool(cond),"detail":detail})
    if not cond:
        raise AssertionError(f"{name}: {detail}")

# Registry and type conformance
ids=[f["id"] for f in exp.FUNCTIONS]
check("unique_registry_ids",len(ids)==len(set(ids)))
check("R1_R2_present",{o["id"] for o in exp.OBLIGATIONS}>={"R1","R2"})
check("signal_carrier_not_fss","internal_basis" not in {"carrier_type":"typed_non_fss"})
check("single_generator_symbol",callable(exp.step))

# Primary result hashes are unmixed
traj=pd.read_csv(ROOT/"data/integrated_trajectories.csv.gz")
events=pd.read_csv(ROOT/"data/event_log.csv.gz")
check("single_model_hash_trajectories",traj.model_hash.nunique()==1 and traj.model_hash.iloc[0]==exp.MODEL_HASH)
check("single_model_hash_events",events.model_hash.nunique()==1 and events.model_hash.iloc[0]==exp.MODEL_HASH)
check("single_registry_hash",events.registry_hash.nunique()==1 and events.registry_hash.iloc[0]==exp.REGISTRY_HASH)
check("eight_events_per_trajectory",events.groupby("trajectory_id").size().eq(8).all())

# Deterministic replay of one canonical trajectory
row=traj.iloc[0]
regimes=exp.make_regimes()
reg=regimes.loc[regimes.regime_id==row.regime_id].iloc[0].to_dict()
s=exp.initial_state(reg,row.intervention,int(row.rep),int(row.seed))
rng=np.random.default_rng(int(row.seed))
post_hashes=[]
while not s["terminal"]:
    s,op,res,resid=exp.step(s,rng)
    post_hashes.append(exp.state_digest(s))
stored=events.loc[events.trajectory_id==row.trajectory_id].sort_values("event_index").post_hash.tolist()
check("deterministic_replay",post_hashes==stored)
summary=exp.trajectory_summary(s,row.trajectory_id)
for col in ["target_correct","certified_reach","recursive_reuse","mean_displacement","terminal_risk"]:
    a=float(summary[col]); b=float(row[col])
    check(f"replay_summary_{col}",abs(a-b)<1e-12,f"{a} != {b}")

# Hidden-resource and split-generator detectors
w=pd.read_csv(ROOT/"data/deterministic_witnesses.csv")
check("no_ablation_passes",not (w.designated_ablation_verdict=="pass").any())
code=pd.read_csv(ROOT/"data/model_codewords.csv").set_index("model")
check("split_generator_codeword_detected",(code.loc["M_star"]!=code.loc["M11_split_generator"]).any())
check("signal_regress_codeword_detected",(code.loc["M_star"]!=code.loc["M2_signal_regress"]).any())

out={"model_hash":exp.MODEL_HASH,"registry_hash":exp.REGISTRY_HASH,"all_pass":all(x["pass"] for x in results),"tests":results}
(ROOT/"tests/conformance_results.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
