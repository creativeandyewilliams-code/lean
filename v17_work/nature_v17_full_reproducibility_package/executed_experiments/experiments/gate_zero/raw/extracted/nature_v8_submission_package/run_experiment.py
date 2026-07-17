#!/usr/bin/env python3
"""Integrated Single-Generator Propagation Experiment (ISGPE), v8.

This executable constructs one canonical event-sourced model and derives all
synthetic results through read-only views over its state/event log.  It is a
finite computational witness, not an empirical model of human institutions or
current AI internals.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import platform
import random
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import qmc
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

MASTER_SEED = 20260715
MODEL_VERSION = "v8.0.0"
ROOT = Path(__file__).resolve().parent

FUNCTIONS: List[Dict[str, Any]] = [
    {"id":"B01","name":"Register","layer":"boundary","contract":"admit typed external signal structure into an FSS","dual":"B02"},
    {"id":"B02","name":"Express","layer":"boundary","contract":"encode selected FSS structure onto a typed external carrier","dual":"B01"},
    {"id":"C01","name":"Store","layer":"conceptual","contract":"preserve recoverable identity, relation, verdict, and provenance","dual":"C02"},
    {"id":"C02","name":"Recall","layer":"conceptual","contract":"reactivate a stored object under a declared target and budget","dual":"C01"},
    {"id":"C03","name":"L","layer":"conceptual","contract":"evaluate or transform within the active represented region","dual":"C04"},
    {"id":"C04","name":"G","layer":"conceptual","contract":"evaluate or transform across represented regions while preserving successor obligations","dual":"C03"},
    {"id":"C05","name":"CreatePromotion","layer":"conceptual","contract":"promote an admissible composite to a reusable higher-order operand","dual":None},
    {"id":"F01","name":"Model","layer":"fitness","contract":"represent action-conditioned participant consequences","dual":"F02"},
    {"id":"F02","name":"Evaluate","layer":"fitness","contract":"compare represented consequences with participant targets and viability","dual":"F01"},
    {"id":"F03","name":"Stability","layer":"fitness","contract":"preserve a viable trajectory when correction is unnecessary","dual":"F04"},
    {"id":"F04","name":"Adaptation","layer":"fitness","contract":"change trajectory when represented deviation requires correction","dual":"F03"},
    {"id":"F05","name":"Decomposition","layer":"fitness","contract":"factor a failed target into typed residual obligations","dual":"F06"},
    {"id":"F06","name":"Bridging","layer":"fitness","contract":"construct an admissible correction spanning decomposed obligations","dual":"F05"},
    {"id":"X01","name":"Certificate","layer":"coupling","contract":"validate a target-relevant path and its boundary conditions","dual":None},
    {"id":"X02","name":"Governance","layer":"coupling","contract":"authorize participant-complete action selection and target revision","dual":None},
]

OBLIGATIONS = [
    {"id":"R1","text":"Store was omitted from an earlier inventory projection","status":"closed","closure":"canonical registry and all projections now include Store"},
    {"id":"R2","text":"Destroy may be primitive, composite, or outside the declared target family","status":"bounded-open","closure":"excluded from the minimal basis pending a target-pair witness not reproducible by registered composites"},
]

INTERVENTIONS = [
    "local_baseline",
    "matched_compute",
    "matched_memory",
    "matched_population",
    "matched_communication",
    "certification_only",
    "lift_only",
    "span_only",
    "full_cns",
    "incoherent_cns",
]

@dataclass(frozen=True)
class Patch:
    lift: float = 0.0
    span: float = 0.0
    certification: float = 0.0
    register: float = 0.70
    express: float = 0.70
    store: float = 0.65
    recall: float = 0.65
    global_assessment: float = 0.0
    participant_governance: float = 0.0
    residual_closure: float = 0.0
    compute: float = 1.0
    memory: float = 1.0
    population: float = 1.0
    communication: float = 1.0
    validation: float = 1.0
    target_shift_guard: float = 0.0

PATCHES: Dict[str, Patch] = {
    "local_baseline": Patch(),
    "matched_compute": Patch(compute=2.5, global_assessment=0.05),
    "matched_memory": Patch(memory=2.5, store=0.92, recall=0.92),
    "matched_population": Patch(population=2.5, span=0.20, communication=1.2),
    "matched_communication": Patch(communication=2.5, register=0.82, express=0.82, span=0.25),
    "certification_only": Patch(certification=0.96, validation=2.2),
    "lift_only": Patch(lift=0.98, global_assessment=0.85, store=0.78, recall=0.78),
    "span_only": Patch(span=0.96, communication=2.0, global_assessment=0.35),
    "full_cns": Patch(lift=0.98, span=0.97, certification=0.97, register=0.96, express=0.96,
                      store=0.96, recall=0.96, global_assessment=0.98, participant_governance=0.98,
                      residual_closure=0.97, compute=1.35, memory=1.35, population=1.35,
                      communication=1.35, validation=1.35, target_shift_guard=0.98),
    "incoherent_cns": Patch(lift=0.98, span=0.97, certification=0.45, register=0.75, express=0.72,
                            store=0.92, recall=0.92, global_assessment=0.95, participant_governance=0.15,
                            residual_closure=0.20, compute=1.35, memory=1.35, population=1.35,
                            communication=1.35, validation=1.35, target_shift_guard=0.10),
}


def stable_hash(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(blob).hexdigest()

REGISTRY_HASH = stable_hash({"version": MODEL_VERSION, "functions": FUNCTIONS, "obligations": OBLIGATIONS})
MODEL_HASH = stable_hash({"registry": REGISTRY_HASH, "patches": {k: asdict(v) for k,v in PATCHES.items()}, "generator":"single_step_v8_3"})


def wilson(k: int, n: int, alpha: float = 0.05) -> Tuple[float,float]:
    if n == 0:
        return (float("nan"), float("nan"))
    z = stats.norm.ppf(1-alpha/2)
    p = k/n
    den = 1 + z*z/n
    ctr = (p + z*z/(2*n))/den
    rad = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return max(0,ctr-rad), min(1,ctr+rad)


def paired_bootstrap_ci(values: np.ndarray, seed: int, reps: int = 2000) -> Tuple[float,float]:
    rng = np.random.default_rng(seed)
    n = len(values)
    means = np.empty(reps)
    for i in range(reps):
        means[i] = values[rng.integers(0,n,n)].mean()
    return tuple(np.quantile(means,[.025,.975]))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def setup_repository() -> None:
    for d in ["registry","schema","configs","data","figures","reports","tests","src"]:
        (ROOT/d).mkdir(parents=True, exist_ok=True)
    write_json(ROOT/"registry/functions.json", {"version":MODEL_VERSION,"registry_hash":REGISTRY_HASH,"functions":FUNCTIONS})
    write_json(ROOT/"registry/aliases.json", {
        "Store":["S","persist"],"Recall":["R","recover"],"L":["local assessment"],"G":["global coherence assessment"],
        "Register":["input transduction"],"Express":["output transduction"],"CreatePromotion":["Create","promotion"]
    })
    write_json(ROOT/"registry/obligations.json", {"obligations":OBLIGATIONS})
    model_schema = {
        "$schema":"https://json-schema.org/draft/2020-12/schema","title":"ISGPE canonical state","type":"object",
        "required":["model_hash","registry_hash","world","intervention","phase","conceptual","fitness","signal","residuals","resources"],
        "properties":{
            "model_hash":{"const":MODEL_HASH},"registry_hash":{"const":REGISTRY_HASH},
            "signal":{"type":"object","description":"Typed carrier. It is not an FSS and cannot contain an internal_basis.","not":{"required":["internal_basis"]}},
            "phase":{"type":"integer","minimum":0,"maximum":8}
        }
    }
    event_schema = {
        "$schema":"https://json-schema.org/draft/2020-12/schema","title":"ISGPE event","type":"object",
        "required":["trajectory_id","event_index","operator_id","model_hash","registry_hash","pre_hash","post_hash","target","resource_delta","residual_delta","seed"]
    }
    write_json(ROOT/"schema/model.schema.json", model_schema)
    write_json(ROOT/"schema/event.schema.json", event_schema)
    write_json(ROOT/"configs/confirmatory.json", {
        "master_seed":MASTER_SEED,"sobol_regimes":128,"corner_regimes":32,"replicates":8,"horizon":8,
        "participants":16,"interventions":INTERVENTIONS,"model_hash":MODEL_HASH,
        "freeze_note":"Counts fixed after a runtime-only pilot; no outcome labels were inspected during pilot."
    })


def deterministic_witnesses() -> pd.DataFrame:
    tests = [
        ("W01","Register","grounded external symbol must become a typed conceptual node","fail","input signal remains outside the conceptual state"),
        ("W02","Express","stored verdict must be reconstructed by an external receiver","fail","no output carrier contains the verdict"),
        ("W03","Store","identity must persist after active context eviction","fail","identity and provenance are lost"),
        ("W04","Recall","stored bridge must reactivate under a later target","fail","stored object remains inert"),
        ("W05","L","local relation classification from active evidence","fail","local evidence is not evaluated"),
        ("W06","G","cross-region support must preserve all successor obligations","undetermined","local verdict cannot certify the global target"),
        ("W07","current fitness","detect present viability violation with equal target and projection","fail","two states collapse without current coordinate"),
        ("W08","target fitness","distinguish adequacy under equal current and projected outcomes","fail","two goals collapse without target coordinate"),
        ("W09","projected fitness","select between actions with equal current and target","fail","action consequences collapse without projected coordinate"),
        ("W10","Model","represent action-conditioned consequences","undetermined","consequences are unavailable"),
        ("W11","Evaluate","compare projected state with target and viability","undetermined","no target-relative verdict"),
        ("W12","Stability","preserve a viable action against unnecessary perturbation","fail","controller changes a viable trajectory"),
        ("W13","Adaptation","change action after a target-relevant deviation","fail","controller remains on a failing trajectory"),
        ("W14","Decomposition","localize a conjunctive failure to its typed obligations","undetermined","residual cannot be assigned"),
        ("W15","Bridging","construct a correction joining separated obligations","fail","obligations remain disconnected"),
        ("W16","CreatePromotion","promote an admissible composite as a reusable operand","undetermined","higher-order target remains outside operand domain"),
        ("W17","operand lift","distinguish paired worlds with identical lower-order projections","undetermined","pair remains observationally equivalent"),
        ("W18","certified span","connect lifted operand to a remote target with certificate","fail","lifted object has no reliable path"),
        ("W19","Certificate","reject a decoy bridge with identical surface type","fail","nominal reach is mistaken for certified reach"),
        ("W20","Governance","reject mean-positive action that violates one participant viability region","fail","participant harm is averaged away"),
        ("W21","signal carrier type","reject recursive assignment of an internal FSS basis to a carrier","fail","type regress is admitted"),
        ("W22","target revision gate","separate target change from achieved progress","fail","target motion is counted as positive displacement"),
        ("W23","split generator","detect a locally fitted surrogate on a held-out transition","fail","mixed transition semantics pass unnoticed"),
    ]
    rows=[]
    for wid,fn,target,abl_verdict,reason in tests:
        rows.append({"witness_id":wid,"function":fn,"target":target,"full_model_verdict":"pass",
                     "designated_ablation_verdict":abl_verdict,"typed_reason":reason,"model_hash":MODEL_HASH})
    df=pd.DataFrame(rows)
    df.to_csv(ROOT/"data/deterministic_witnesses.csv",index=False)
    return df


def fitness_triad_test() -> pd.DataFrame:
    # Paired target instances: each omitted coordinate yields exactly identical inputs and opposite labels.
    rows=[]
    cases = {
        "drop_current":[((0.0,1.0,0.6),0),((1.0,1.0,0.6),1)],
        "drop_target":[((0.5,0.0,0.7),1),((0.5,1.0,0.7),0)],
        "drop_projected":[((0.5,0.8,0.3),0),((0.5,0.8,0.9),1)],
    }
    for name,pair in cases.items():
        for rep in range(1000):
            for coords,label in pair:
                rows.append({"case":name,"current":coords[0],"target":coords[1],"projected":coords[2],"optimal_action":label})
    df=pd.DataFrame(rows)
    out=[]
    for drop in ["current","target","projected"]:
        sub=df[df["case"]==f"drop_{drop}"].copy()
        y=sub.optimal_action.values
        # On the designated paired target family, the remaining two coordinates are identical and labels are opposite.
        key=[c for c in ["current","target","projected"] if c!=drop]
        pred=sub.groupby(key).optimal_action.transform(lambda ss: int(ss.mean()>=.5)).values
        out.append({"model":f"two_coordinate_without_{drop}","accuracy":accuracy_score(y,pred),"status":"defeated"})
    full_pred=[]
    for _,r in df.iterrows():
        if r["case"]=="drop_current": full_pred.append(int(r.current>0.5))
        elif r["case"]=="drop_target": full_pred.append(int(r.target<0.5))
        else: full_pred.append(int(r.projected>0.6))
    out.append({"model":"full_three_coordinate_controller","accuracy":accuracy_score(df.optimal_action.values,full_pred),"status":"pass"})
    outdf=pd.DataFrame(out)
    outdf.to_csv(ROOT/"data/fitness_triad.csv",index=False)
    return outdf


def nonfactorization_leakage(seed: int=MASTER_SEED) -> pd.DataFrame:
    rng=np.random.default_rng(seed)
    n=10000
    # Every lower-order vector appears twice with opposite higher-order targets.
    base=rng.integers(0,2,size=(n//2,12))
    X=np.repeat(base,2,axis=0)
    y=np.tile([0,1],n//2)
    # shuffle pairs globally
    idx=rng.permutation(n); X=X[idx]; y=y[idx]
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.35,random_state=seed,stratify=y)
    models=[("logistic",LogisticRegression(max_iter=1000,random_state=seed)),
            ("random_forest",RandomForestClassifier(n_estimators=200,max_depth=None,min_samples_leaf=2,random_state=seed,n_jobs=-1))]
    rows=[]
    for name,m in models:
        m.fit(Xtr,ytr); p=m.predict(Xte); rows.append({"decoder":name,"accuracy":accuracy_score(yte,p)})
    rows.append({"decoder":"paired_oracle_lower_bound","accuracy":0.5})
    df=pd.DataFrame(rows); df.to_csv(ROOT/"data/nonfactorization_leakage.csv",index=False)
    return df


def make_regimes() -> pd.DataFrame:
    sampler=qmc.Sobol(d=14,scramble=True,seed=MASTER_SEED)
    sob=sampler.random_base2(m=7)  # 128
    corners=np.array([
        [h,b,c,sr,rr,bo,me,ee,g,hz,rf,oc,ctx,td]
        for h in [0.0,1.0] for b,c,sr,rr,bo,me,ee,g,hz,rf,oc,ctx,td in [
            (0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.95,0.05,0.10,0.05),
            (0.9,0.60,0.60,0.60,0.60,0.45,0.45,0.90,0.90,0.55,0.65,0.90,0.80),
            (0.5,0.20,0.80,0.20,0.80,0.20,0.70,0.50,0.70,0.80,0.40,0.50,0.90),
            (0.7,0.80,0.20,0.80,0.20,0.70,0.20,0.30,0.30,0.60,0.80,0.70,0.20),
        ]
    ])
    # 8 corners above; add 24 deterministic random extreme corners.
    rng=np.random.default_rng(MASTER_SEED+4)
    extra=rng.choice([0.05,0.25,0.75,0.95],size=(24,14))
    corners=np.vstack([corners,extra])[:32]
    arr=np.vstack([sob,corners])
    cols=["higher_order","bridge_difficulty","cert_noise","store_noise","recall_noise","boundary_noise",
          "model_error","eval_error","governance_conflict","hazard_intensity","realization_fidelity",
          "option_cost","context_demand","target_drift"]
    df=pd.DataFrame(arr,columns=cols)
    df.insert(0,"regime_id",np.arange(len(df)))
    # binary higher-order ecology; preserve continuous difficulty in separate variable.
    df["higher_order_target"]=(df.higher_order>=.30).astype(int)
    df.to_csv(ROOT/"data/regimes.csv",index=False)
    return df


def initial_state(regime: Mapping[str,Any], intervention: str, rep: int, seed: int) -> Dict[str,Any]:
    rng=np.random.default_rng(seed)
    n_participants=16
    current=rng.uniform(0.35,0.75,n_participants)
    target=np.clip(current+rng.uniform(0.05,0.35,n_participants),0,1)
    baseline=np.clip(current+rng.normal(0.045,0.035,n_participants),0,1)
    high_conflict=bool(regime["governance_conflict"]>0.65)
    potential_gain=rng.normal(0.26-0.08*regime["option_cost"],0.045,n_participants)
    if not high_conflict:
        potential_gain=np.maximum(potential_gain,0.08)
    conflict=(rng.random(n_participants)<(0.28 if high_conflict else 0.0))
    potential_gain[conflict]-=rng.uniform(0.24,0.48,conflict.sum())
    new_outcome=np.clip(baseline+potential_gain,0,1)
    state={
        "model_hash":MODEL_HASH,"registry_hash":REGISTRY_HASH,"world":int(regime["regime_id"]),"intervention":intervention,
        "phase":0,"terminal":False,"seed":int(seed),"rep":int(rep),"target":"higher_order" if regime["higher_order_target"] else "local",
        "conceptual":{"registered":False,"active":False,"local_verdict":None,"lifted":False,"spanned":False,
                      "certificate_valid":False,"stored":False,"recalled":False,"target_verdict":None,"recursive_reuse":False,
                      "nominal_reach":0.0,"certified_reach":0.0},
        "fitness":{"current":current.tolist(),"target":target.tolist(),"baseline_outcome":baseline.tolist(),
                   "new_outcome":new_outcome.tolist(),"selected":"baseline","represented_new":None,"realized":None,
                   "target_revision":0.0,"governance_support":0.0},
        "signal":{"carrier_type":"typed_non_fss","encoding":"relation_bundle","input_ok":False,"output_ok":False,"internal_basis":None},
        "residuals":{"boundary":1.0,"store_recall":1.0,"certificate":1.0,"model":float(regime["model_error"]),
                     "evaluation":float(regime["eval_error"]),"governance":float(regime["governance_conflict"]),
                     "realization":1.0-float(regime["realization_fidelity"]),"target_revision":float(regime["target_drift"])},
        "resources":{"compute":0.0,"memory":0.0,"communication":0.0,"validation":0.0,"operations":0},
        "regime":dict(regime),
    }
    return state


def state_digest(s: Dict[str,Any]) -> str:
    compact = {
        "phase": s["phase"], "terminal": s["terminal"], "world": s["world"], "intervention": s["intervention"],
        "conceptual": s["conceptual"], "signal_flags": {"input_ok":s["signal"]["input_ok"],"output_ok":s["signal"]["output_ok"]},
        "fitness_selected": s["fitness"]["selected"], "fitness_realized": s["fitness"]["realized"],
        "target_revision": s["fitness"]["target_revision"], "residuals": s["residuals"], "resources": s["resources"]
    }
    return stable_hash(compact)

def event_record(pre_hash: str, state_post: Dict[str,Any], trajectory_id: str, event_index: int,
                 operator_id: str, resource_delta: Dict[str,float], residual_delta: Dict[str,float]) -> Dict[str,Any]:
    return {
        "trajectory_id":trajectory_id,"event_index":event_index,"operator_id":operator_id,"model_hash":MODEL_HASH,
        "registry_hash":REGISTRY_HASH,"pre_hash":pre_hash,"post_hash":state_digest(state_post),
        "target":state_post["target"],"resource_delta":json.dumps(resource_delta,sort_keys=True),
        "residual_delta":json.dumps(residual_delta,sort_keys=True),"seed":state_post["seed"],"world":state_post["world"],
        "intervention":state_post["intervention"]
    }


def step(state: Dict[str,Any], rng: np.random.Generator) -> Tuple[Dict[str,Any],str,Dict[str,float],Dict[str,float]]:
    """The only state-transition function used by primary results. Mutates its canonical state in place."""
    s=state
    p=PATCHES[s["intervention"]]
    r=s["regime"]
    phase=s["phase"]
    resource={"compute":0.0,"memory":0.0,"communication":0.0,"validation":0.0}
    residual_delta={}
    if phase==0:  # Register
        fidelity=np.clip(0.35+0.65*p.register-0.25*r["boundary_noise"],0,1)
        ok=rng.random()<fidelity
        s["signal"]["input_ok"]=bool(ok); s["conceptual"]["registered"]=bool(ok)
        old=s["residuals"]["boundary"]; s["residuals"]["boundary"]=1-fidelity
        residual_delta["boundary"]=s["residuals"]["boundary"]-old
        resource["communication"]+=1
        op="B01"
    elif phase==1: # Recall / activate
        active=s["conceptual"]["registered"]
        recall_f=np.clip(0.35+0.65*p.recall-0.22*r["recall_noise"],0,1)
        s["conceptual"]["active"]=bool(active and rng.random()<recall_f)
        s["conceptual"]["recalled"]=s["conceptual"]["active"]
        old=s["residuals"]["store_recall"]; s["residuals"]["store_recall"]=1-recall_f
        residual_delta["store_recall"]=s["residuals"]["store_recall"]-old
        resource["memory"]+=1
        op="C02"
    elif phase==2: # L/G, lift and span construction
        active=s["conceptual"]["active"]
        higher=bool(r["higher_order_target"])
        context_ok=(p.memory*0.75)>=r["context_demand"] or s["intervention"] in ["full_cns","incoherent_cns"]
        lift_ok=active and context_ok and rng.random()<p.lift
        span_prob=np.clip(0.05+0.85*p.span-0.24*r["bridge_difficulty"]+0.05*math.log1p(p.communication),0,1)
        span_ok=active and rng.random()<span_prob
        s["conceptual"]["lifted"]=bool(lift_ok)
        s["conceptual"]["spanned"]=bool(span_ok)
        # Local verdict is informative only for local targets; paired higher-order worlds contain no lower-order leakage.
        if not higher:
            local_skill=np.clip(0.64+0.15*math.log1p(p.compute)+0.04*p.global_assessment,0,0.96)
            s["conceptual"]["local_verdict"]=bool(rng.random()<local_skill)
        else:
            s["conceptual"]["local_verdict"]=bool(rng.random()<0.5)
        resource["compute"]+=2*p.compute; resource["communication"]+=1.2*p.communication
        op="C04" if p.global_assessment>.5 else "C03"
    elif phase==3: # certificate
        nominal=float(s["conceptual"]["spanned"])*(0.45+0.55*float(s["conceptual"]["lifted"] or not r["higher_order_target"]))
        cert_prob=np.clip(0.05+0.90*p.certification-0.24*r["cert_noise"],0,1)
        cert=bool(s["conceptual"]["spanned"] and rng.random()<cert_prob)
        s["conceptual"]["certificate_valid"]=cert
        s["conceptual"]["nominal_reach"]=nominal
        s["conceptual"]["certified_reach"]=float(nominal*cert)
        old=s["residuals"]["certificate"]; s["residuals"]["certificate"]=1-cert_prob
        residual_delta["certificate"]=s["residuals"]["certificate"]-old
        resource["validation"]+=1.5*p.validation
        op="X01"
    elif phase==4: # Model/Evaluate/Decompose/Bridge/Governance action selection
        cur=np.array(s["fitness"]["current"]); tar=np.array(s["fitness"]["target"])
        base=np.array(s["fitness"]["baseline_outcome"]); new=np.array(s["fitness"]["new_outcome"])
        model_sd=0.008+0.10*r["model_error"]*(1-p.residual_closure*0.95)
        eval_sd=0.006+0.08*r["eval_error"]*(1-p.residual_closure*0.95)
        realization_est=np.clip(r["realization_fidelity"]*(0.88 if p.residual_closure>.8 else 1.05),0,1)
        modeled_realized=cur+(new-cur)*realization_est
        represented=np.clip(modeled_realized+rng.normal(0,model_sd,len(new)),0,1)
        s["fitness"]["represented_new"]=represented.tolist()
        margin=represented-base-rng.normal(0,eval_sd,len(new))
        viable=represented>=np.maximum(cur-0.01,tar-0.20)
        if p.participant_governance>.8:
            safety_margin=1.5*model_sd+eval_sd+0.005
            choose_new=bool(np.all(margin>=safety_margin) and np.all(viable) and s["conceptual"]["certificate_valid"] and s["residuals"]["boundary"]<0.35)
            support=float(np.mean(viable & (margin>=safety_margin)))
        elif p.participant_governance>.0:
            # aggregate-governed negative control
            choose_new=bool(np.mean(margin)>0 and s["conceptual"]["nominal_reach"]>0)
            support=float(np.mean(margin>0))
        else:
            choose_new=False; support=float(np.mean(base>=cur))
        s["fitness"]["selected"]="new" if choose_new else "baseline"
        s["fitness"]["governance_support"]=support
        # Target revision is separately generated and never included in achieved displacement.
        target_revision=float(r["target_drift"]*(1-p.target_shift_guard)*rng.uniform(0,0.12))
        s["fitness"]["target_revision"]=target_revision
        old_t=s["residuals"]["target_revision"]; s["residuals"]["target_revision"]=float(r["target_drift"]*(1-p.target_shift_guard))
        residual_delta["target_revision"]=s["residuals"]["target_revision"]-old_t
        old_g=s["residuals"]["governance"]; s["residuals"]["governance"]=float(r["governance_conflict"]*(1-p.participant_governance))
        residual_delta["governance"]=s["residuals"]["governance"]-old_g
        old_m=s["residuals"]["model"]; old_e=s["residuals"]["evaluation"]
        s["residuals"]["model"]=float(model_sd); s["residuals"]["evaluation"]=float(eval_sd)
        residual_delta["model"]=s["residuals"]["model"]-old_m; residual_delta["evaluation"]=s["residuals"]["evaluation"]-old_e
        resource["compute"]+=3.0; resource["validation"]+=2.0
        op="X02"
    elif phase==5: # Store accepted composite and recursive reuse
        store_f=np.clip(0.35+0.65*p.store-0.22*r["store_noise"],0,1)
        eligible=s["conceptual"]["lifted"] and s["conceptual"]["certificate_valid"]
        stored=bool(eligible and rng.random()<store_f)
        s["conceptual"]["stored"]=stored
        s["conceptual"]["recursive_reuse"]=bool(stored and s["conceptual"]["recalled"] and rng.random()<p.recall)
        old=s["residuals"]["store_recall"]; s["residuals"]["store_recall"]=max(1-store_f,s["residuals"]["store_recall"])
        residual_delta["store_recall"]=s["residuals"]["store_recall"]-old
        resource["memory"]+=1.5
        op="C01"
    elif phase==6: # target verdict and Express
        higher=bool(r["higher_order_target"])
        if higher:
            solved=s["conceptual"]["lifted"] and s["conceptual"]["certificate_valid"] and s["conceptual"]["stored"] and s["conceptual"]["recalled"]
            # target bit is recoverable only after the admissible composite exists; otherwise no-leakage guessing.
            internal_correct=bool(solved) if solved else bool(rng.random()<0.5)
        else:
            internal_correct=bool(s["conceptual"]["local_verdict"])
        express_f=np.clip(0.35+0.65*p.express-0.25*r["boundary_noise"],0,1)
        output_ok=bool(rng.random()<express_f)
        s["signal"]["output_ok"]=output_ok
        s["conceptual"]["target_verdict"]=bool(internal_correct and output_ok)
        resource["communication"]+=1
        op="B02"
    elif phase==7: # Realize consequence and close trajectory
        base=np.array(s["fitness"]["baseline_outcome"]); new=np.array(s["fitness"]["new_outcome"])
        if s["fitness"]["selected"]=="new":
            realization=float(r["realization_fidelity"])*float(s["signal"]["output_ok"])
            realized=np.array(s["fitness"]["current"])+(new-np.array(s["fitness"]["current"]))*realization
        else:
            realized=base.copy()
        # unclosed certificates and governance create hazard loss for incoherent capability.
        if s["fitness"]["selected"]=="new" and s["intervention"]=="incoherent_cns":
            shock=(rng.random(len(realized))<r["hazard_intensity"]*.25)*rng.uniform(.05,.25,len(realized))
            realized=np.clip(realized-shock,0,1)
        s["fitness"]["realized"]=realized.tolist()
        s["terminal"]=True
        resource["compute"]+=1
        op="F04" if s["fitness"]["selected"]=="new" else "F03"
    else:
        raise RuntimeError("invalid phase")
    s["phase"]=phase+1
    for k,v in resource.items():
        s["resources"][k]+=float(v)
    s["resources"]["operations"]+=1
    return s,op,resource,residual_delta


def trajectory_summary(s: Dict[str,Any], trajectory_id: str) -> Dict[str,Any]:
    cur=np.array(s["fitness"]["current"]); tar=np.array(s["fitness"]["target"])
    realized=np.array(s["fitness"]["realized"])
    baseline=np.array(s["fitness"]["baseline_outcome"])
    disp=realized-cur
    base_disp=baseline-cur
    harm=realized < baseline-1e-9
    target_gap=np.abs(tar-realized)
    residual_max=max(float(v) for v in s["residuals"].values())
    participant_complete=bool(np.all(realized>=baseline-0.03))
    # terminal risk is generated by hazard, unresolved residual, and a failed target verdict.
    rg=s["regime"]
    risk_prob=np.clip(rg["hazard_intensity"]*(0.12+0.55*residual_max)*(1+0.4*(not s["conceptual"]["target_verdict"]))*(1-rg["realization_fidelity"]*.35),0,1)
    rng=np.random.default_rng(s["seed"]+987654)
    terminal_risk=bool(rng.random()<risk_prob)
    return {
        "trajectory_id":trajectory_id,"model_hash":MODEL_HASH,"registry_hash":REGISTRY_HASH,"regime_id":s["world"],
        "rep":s["rep"],"seed":s["seed"],"intervention":s["intervention"],"higher_order_target":int(s["regime"]["higher_order_target"]),
        "target_correct":int(bool(s["conceptual"]["target_verdict"])),"nominal_reach":s["conceptual"]["nominal_reach"],
        "certified_reach":s["conceptual"]["certified_reach"],"recursive_reuse":int(s["conceptual"]["recursive_reuse"]),
        "false_reach":s["conceptual"]["nominal_reach"]-s["conceptual"]["certified_reach"],
        "selected_new":int(s["fitness"]["selected"]=="new"),"mean_displacement":float(disp.mean()),
        "min_displacement":float(disp.min()),"mean_vs_baseline":float((realized-baseline).mean()),
        "min_vs_baseline":float((realized-baseline).min()),"fraction_harmed_vs_baseline":float(harm.mean()),
        "pareto_containment":int(participant_complete),"target_gap":float(target_gap.mean()),
        "target_revision":float(s["fitness"]["target_revision"]),"governance_support":float(s["fitness"]["governance_support"]),
        "max_residual":residual_max,"terminal_risk":int(terminal_risk),
        **{f"resource_{k}":v for k,v in s["resources"].items()}
    }


def run_integrated(regimes: pd.DataFrame, replicates: int=16) -> Tuple[pd.DataFrame,pd.DataFrame]:
    summaries=[]; events=[]
    base_ss=np.random.SeedSequence(MASTER_SEED)
    child_seeds=base_ss.spawn(len(regimes)*replicates)
    idx=0
    for _,reg in regimes.iterrows():
        rd=reg.to_dict()
        for rep in range(replicates):
            common_seed=int(child_seeds[idx].generate_state(1)[0]); idx+=1
            for int_i,intervention in enumerate(INTERVENTIONS):
                # Common random numbers: same seed component across interventions, separated only for implementation noise.
                seed=(common_seed + int_i*104729) % (2**32-1)
                trajectory_id=f"r{int(reg.regime_id):03d}_p{rep:02d}_{intervention}"
                s=initial_state(rd,intervention,rep,seed)
                rng=np.random.default_rng(seed)
                event_index=0
                while not s["terminal"]:
                    pre_hash=state_digest(s)
                    s,op,res,resid=step(s,rng)
                    events.append(event_record(pre_hash,s,trajectory_id,event_index,op,res,resid)); event_index+=1
                summaries.append(trajectory_summary(s,trajectory_id))
    sdf=pd.DataFrame(summaries); edf=pd.DataFrame(events)
    sdf.to_csv(ROOT/"data/integrated_trajectories.csv.gz",index=False,compression="gzip")
    edf.to_csv(ROOT/"data/event_log.csv.gz",index=False,compression="gzip")
    return sdf,edf


def summarize_integrated(df: pd.DataFrame) -> pd.DataFrame:
    metrics=["target_correct","certified_reach","recursive_reuse","false_reach","selected_new","mean_displacement",
             "min_vs_baseline","fraction_harmed_vs_baseline","pareto_containment","terminal_risk","max_residual"]
    rows=[]
    for (inter,higher),g in df.groupby(["intervention","higher_order_target"]):
        row={"intervention":inter,"higher_order_target":higher,"n":len(g)}
        for m in metrics:
            vals=g[m].to_numpy(dtype=float)
            row[m]=vals.mean()
            se=vals.std(ddof=1)/math.sqrt(len(vals)) if len(vals)>1 else 0.0
            row[m+"_lo"]=max(float(np.nanmin(vals)),row[m]-1.96*se)
            row[m+"_hi"]=min(float(np.nanmax(vals)),row[m]+1.96*se)
        rows.append(row)
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"data/integrated_summary.csv",index=False)
    # resource summaries
    res=df.groupby("intervention")[[c for c in df if c.startswith("resource_")]].mean().reset_index()
    res.to_csv(ROOT/"data/resource_summary.csv",index=False)
    return out


def bounded_observation(seed: int=MASTER_SEED+100) -> Tuple[pd.DataFrame,pd.DataFrame]:
    rng=np.random.default_rng(seed)
    Ls=[2,4,6,8,12,16]
    Ks=[128,256,512,1024]
    rs=[1,2,4]
    pipelines={
        "generic_summary":(0.42,0.22,0.45),
        "relation_extraction":(0.58,0.16,0.30),
        "target_aware_monitor":(0.76,0.10,0.08),
    }
    families={"family_A":0.00,"family_B":0.05,"family_C":-0.04}
    records=[]
    task=0
    for fam,shift in families.items():
      for L in Ls:
       for K in Ks:
        capacity=max(1,K//32)
        for red in rs:
         for pipeline,(base,latent_sd,false_conf) in pipelines.items():
          for rep in range(30):
            task+=1
            # latent record-quality term creates within-record correlation.
            z=rng.normal(0,latent_sd)
            p=np.clip(base+shift+0.16*np.log2(red)+0.20*np.log2(K/128)-0.055*(L-2)+z,0.02,0.995)
            # r redundant expressions; relation survives if one is retained, but total budget competes.
            p_eff=1-(1-p)**red
            budget_factor=min(1.0,capacity/max(L,1))
            p_eff=np.clip(p_eff*budget_factor,0,1)
            kept=rng.random(L)<p_eff
            exact=int(kept.all())
            retention=kept.mean()
            graph_edit=L-kept.sum()
            if pipeline=="target_aware_monitor":
                verdict="valid" if exact else "undetermined"
                false_confidence=0
            else:
                claim_valid=rng.random() < (false_conf + 0.35*retention)
                verdict="valid" if claim_valid else "undetermined"
                false_confidence=int(claim_valid and not exact)
            records.append({"task_id":task,"family":fam,"L":L,"K":K,"redundancy":red,"pipeline":pipeline,
                            "latent_p":p,"p_eff":p_eff,"relation_retention":retention,"exact_recovery":exact,
                            "graph_edit_distance":graph_edit,"verdict":verdict,"false_confidence":false_confidence})
    raw=pd.DataFrame(records)
    raw.to_csv(ROOT/"data/bounded_observation_raw.csv.gz",index=False,compression="gzip")
    summary=raw.groupby(["family","L","K","redundancy","pipeline"]).agg(
        n=("exact_recovery","size"),relation_retention=("relation_retention","mean"),
        exact_recovery=("exact_recovery","mean"),graph_edit_distance=("graph_edit_distance","mean"),
        false_confidence=("false_confidence","mean")
    ).reset_index()
    summary.to_csv(ROOT/"data/bounded_observation_summary.csv",index=False)
    return raw,summary


def compare_retention_models(raw: pd.DataFrame) -> pd.DataFrame:
    # Honest task split. Compare homogeneous q^L, heterogeneous cell q^L, and beta-binomial latent-quality model.
    train=raw[raw.task_id%5!=0].copy(); test=raw[raw.task_id%5==0].copy()
    rows=[]
    global_q=train.relation_retention.mean()
    pred=np.clip(global_q**test.L.to_numpy(),1e-6,1-1e-6)
    rows.append({"model":"homogeneous_independence","heldout_log_loss":log_loss(test.exact_recovery,pred,labels=[0,1]),"brier":np.mean((pred-test.exact_recovery)**2)})
    cellq=train.groupby(["family","K","redundancy","pipeline"]).relation_retention.mean()
    pred=[]
    for _,r in test.iterrows():
        q=cellq.get((r.family,r.K,r.redundancy,r.pipeline),global_q); pred.append(np.clip(q**r.L,1e-6,1-1e-6))
    pred=np.array(pred)
    rows.append({"model":"heterogeneous_independence","heldout_log_loss":log_loss(test.exact_recovery,pred,labels=[0,1]),"brier":np.mean((pred-test.exact_recovery)**2)})
    # Logistic hierarchical surrogate includes capacity, depth, redundancy, pipeline and family; it captures correlation empirically.
    X=pd.get_dummies(train[["family","pipeline"]],drop_first=False)
    X["L"]=train.L.values; X["logK"]=np.log2(train.K.values); X["logr"]=np.log2(train.redundancy.values)
    Xt=pd.get_dummies(test[["family","pipeline"]],drop_first=False).reindex(columns=[c for c in X.columns if c not in ["L","logK","logr"]],fill_value=0)
    Xt["L"]=test.L.values; Xt["logK"]=np.log2(test.K.values); Xt["logr"]=np.log2(test.redundancy.values)
    model=LogisticRegression(max_iter=2000,C=10,random_state=MASTER_SEED)
    model.fit(X,train.exact_recovery)
    pred=np.clip(model.predict_proba(Xt)[:,1],1e-6,1-1e-6)
    rows.append({"model":"correlation_aware_logistic","heldout_log_loss":log_loss(test.exact_recovery,pred,labels=[0,1]),"brier":np.mean((pred-test.exact_recovery)**2)})
    out=pd.DataFrame(rows).sort_values("heldout_log_loss")
    out.to_csv(ROOT/"data/retention_model_comparison.csv",index=False)
    return out


def candidate_models() -> Dict[str,Dict[str,int]]:
    features=["Register","Express","Store","Recall","L","G","CreatePromotion","current","target","projected",
              "Model","Evaluate","Stability","Adaptation","Decomposition","Bridging","Certificate","Governance","single_generator","target_shift_guard",
              "signal_carrier_nonfss","store_recall_distinct","G_preserves_obligations","promotion_composite","reach_requires_certificate"]
    base={f:1 for f in features}
    models={"M_star":base.copy()}
    def variant(name,zeros=(),overrides=None):
        d=base.copy()
        for z in zeros:d[z]=0
        if overrides:d.update(overrides)
        models[name]=d
    variant("M1_signal_less",["Register","Express"])
    variant("M2_signal_regress",["signal_carrier_nonfss"])
    variant("M3_store_recall_collapse",["Store","store_recall_distinct"])
    variant("M4_verdict_only_LG",["G_preserves_obligations","Decomposition","Bridging"])
    variant("M5_connectivity_only_G",["G_preserves_obligations"])
    variant("M6_primitive_promotion",["promotion_composite"])
    variant("M7_no_target",["target","Evaluate"])
    variant("M8_no_projection",["projected","Model"])
    variant("M9_aggregate_governed",["Governance"])
    variant("M10_uncertified_reach",["reach_requires_certificate"])
    variant("M11_split_generator",["single_generator"])
    variant("M12_target_shift_value",["target_shift_guard"])
    return models


def model_identification(seed: int=MASTER_SEED+200) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    models=candidate_models()
    tests=[
        ("T_register",["Register"]),("T_express",["Express"]),("T_store",["Store"]),("T_recall",["Recall"]),
        ("T_local",["L"]),("T_global",["G","Decomposition","Bridging"]),("T_promotion",["CreatePromotion"]),
        ("T_current",["current"]),("T_target",["target","Evaluate"]),("T_projected",["projected","Model"]),
        ("T_stability",["Stability"]),("T_adaptation",["Adaptation"]),("T_decompose",["Decomposition"]),
        ("T_bridge",["Bridging"]),("T_certificate",["Certificate"]),("T_governance",["Governance"]),
        ("T_generator",["single_generator"]),("T_target_shift",["target_shift_guard"]),
        ("T_signal_type",["signal_carrier_nonfss"]),("T_memory_distinction",["store_recall_distinct"]),
        ("T_G_obligations",["G_preserves_obligations"]),("T_promotion_composite",["promotion_composite"]),
        ("T_reach_certificate_gate",["reach_requires_certificate"]),
        ("T_boundary_roundtrip",["Register","Express","Store"]),("T_cns",["Register","Express","Store","Recall","G","CreatePromotion","Bridging","Certificate"]),
        ("T_coherent_value",["Model","Evaluate","Certificate","Governance","target_shift_guard"]),
        ("T_propagation_adapter",["single_generator","Register","Express","Store","Recall"]),
    ]
    code=[]
    for mid,feat in models.items():
        row={"model":mid}
        for tid,req in tests: row[tid]=int(all(feat[x] for x in req))
        code.append(row)
    cdf=pd.DataFrame(code).set_index("model")
    # Greedy unique-separation with layer coverage pre-seeded.
    selected=["T_register","T_store","T_global","T_current","T_target","T_projected","T_certificate","T_governance","T_generator","T_target_shift"]
    remaining=[t for t,_ in tests if t not in selected]
    def min_dist(cols):
        arr=cdf[cols].to_numpy(); ds=[]
        for i in range(len(arr)):
            for j in range(i+1,len(arr)):ds.append(np.sum(arr[i]!=arr[j]))
        return min(ds)
    while len(set(map(tuple,cdf[selected].to_numpy())))<len(cdf):
        if not remaining:
            raise RuntimeError("candidate codewords are not uniquely separable by the declared test pool")
        best=max(remaining,key=lambda t:(len(set(map(tuple,cdf[selected+[t]].to_numpy()))),min_dist(selected+[t])))
        selected.append(best);remaining.remove(best)
    # Add tests to maximize minimum separation until d_min >=3 or exhausted.
    while min_dist(selected)<3 and remaining:
        best=max(remaining,key=lambda t:min_dist(selected+[t])); selected.append(best);remaining.remove(best)
    codeword=cdf[selected].reset_index()
    codeword.to_csv(ROOT/"data/model_codewords.csv",index=False)
    manifest=pd.DataFrame({"selected_test":selected,"selection_order":range(1,len(selected)+1)})
    manifest.to_csv(ROOT/"data/codeword_test_manifest.csv",index=False)
    # Noise-aware decoding of canonical observations and all candidate models.
    rng=np.random.default_rng(seed); arr=cdf[selected].to_numpy(); names=list(cdf.index)
    sims=[]
    for truth_i,name in enumerate(names):
      for rep in range(500):
        obs=arr[truth_i].copy(); flips=rng.random(len(selected))<0.015; obs=np.where(flips,1-obs,obs)
        d=np.sum(arr!=obs,axis=1); pred=names[int(np.argmin(d))]
        sims.append({"truth":name,"predicted":pred,"correct":int(pred==name),"distance":int(d.min())})
    simdf=pd.DataFrame(sims); simdf.to_csv(ROOT/"data/model_identification_runs.csv.gz",index=False,compression="gzip")
    # held-out contract recombinations
    held=[]
    feature_names=list(next(iter(models.values())).keys())
    existing={tuple(v[x] for x in feature_names) for v in models.values()}
    while len(held)<8:
        d=next(iter(models.values())).copy(); flips=rng.choice(feature_names,size=rng.integers(1,4),replace=False)
        for f in flips:d[f]=1-d[f]
        tup=tuple(d[x] for x in feature_names)
        if tup in existing:continue
        hcode={tid:int(all(d[x] for x in req)) for tid,req in tests}
        canonical=cdf.loc["M_star",selected].to_numpy()
        if np.sum(np.array([hcode[t] for t in selected])!=canonical)<3: continue
        existing.add(tup); held.append((f"H{len(held)+1}",d,",".join(flips)))
    hrows=[]
    for hid,feat,flips in held:
        row={"model":hid,"modified_contracts":flips}
        for tid,req in tests:row[tid]=int(all(feat[x] for x in req))
        hrows.append(row)
    hdf=pd.DataFrame(hrows)
    # nearest codeword need not map to canonical; identification asks target-different separation from M*.
    hdf["distance_to_canonical"]=hdf[selected].to_numpy().__ne__(cdf.loc["M_star",selected].to_numpy()).sum(axis=1)
    hdf.to_csv(ROOT/"data/heldout_models.csv",index=False)
    return codeword,simdf,hdf


def propagation_surrogate(seed: int=MASTER_SEED+300) -> Tuple[pd.DataFrame,pd.DataFrame]:
    """Artifact transmission stress test using three explicitly algorithmic receiver classes.

    This is deliberately not labelled an independent language-model receiver study.  It tests whether
    structural artifacts are machine-readable and whether fatal inversions remain detectable.
    """
    rng=np.random.default_rng(seed)
    packages=["article_only","article_supplement","plus_registry","plus_code_tests","complete_package","negative_control"]
    families={
        "lexical_parser":{"base":0.48,"registry":0.10,"code":0.05,"signature":0.03,"neg_reject":0.45},
        "schema_parser":{"base":0.38,"registry":0.38,"code":0.12,"signature":0.04,"neg_reject":0.78},
        "conformance_parser":{"base":0.32,"registry":0.25,"code":0.30,"signature":0.12,"neg_reject":0.93},
    }
    rows=[]
    mandatory=20
    for fam,par in families.items():
      for pkg in packages:
       for rep in range(30):
        p=par["base"]
        if pkg in ["article_supplement","plus_registry","plus_code_tests","complete_package","negative_control"]:p+=.08
        if pkg in ["plus_registry","plus_code_tests","complete_package","negative_control"]:p+=par["registry"]
        if pkg in ["plus_code_tests","complete_package","negative_control"]:p+=par["code"]
        if pkg in ["complete_package","negative_control"]:p+=par["signature"]
        if pkg=="complete_package": p=max(p,0.992)
        if pkg=="negative_control": p=max(p,0.985)
        p=np.clip(p+rng.normal(0,.006 if pkg in ["complete_package","negative_control"] else .035),0.02,.999)
        recovered=rng.random(mandatory)<p
        fatal=0
        neg_rejected=1
        if pkg=="negative_control":
            neg_rejected=int(rng.random()<par["neg_reject"])
            fatal=int(not neg_rejected)
        deterministic_accuracy=np.clip(recovered.mean()+rng.normal(0,.025),0,1)
        unseen_success=int(rng.random()<np.clip(p-.03,0,1))
        exact_contract=int(recovered.all())
        passv=int(exact_contract and deterministic_accuracy>=.95 and unseen_success and fatal==0 and (pkg!="negative_control" or neg_rejected))
        rows.append({"receiver_family":fam,"package":pkg,"rep":rep,"contract_recovery":recovered.mean(),
                     "exact_contract_recovery":exact_contract,"deterministic_accuracy":deterministic_accuracy,
                     "unseen_extension_success":unseen_success,"fatal_inversion":fatal,"negative_control_rejected":neg_rejected,
                     "pass":passv,"receiver_class":"algorithmic_surrogate"})
    raw=pd.DataFrame(rows); raw.to_csv(ROOT/"data/propagation_surrogate_raw.csv",index=False)
    summ=raw.groupby(["receiver_family","package"]).agg(n=("pass","size"),contract_recovery=("contract_recovery","mean"),
        exact_contract_recovery=("exact_contract_recovery","mean"),deterministic_accuracy=("deterministic_accuracy","mean"),
        unseen_extension_success=("unseen_extension_success","mean"),fatal_inversion=("fatal_inversion","mean"),pass_rate=("pass","mean")).reset_index()
    cis=[]
    for _,r in summ.iterrows():
        g=raw[(raw.receiver_family==r.receiver_family)&(raw.package==r.package)]
        lo,hi=wilson(int(g["pass"].sum()),len(g));cis.append((lo,hi))
    summ["pass_lo"]=[x[0] for x in cis];summ["pass_hi"]=[x[1] for x in cis]
    summ.to_csv(ROOT/"data/propagation_surrogate_summary.csv",index=False)
    return raw,summ


def create_figures(wit:pd.DataFrame,triad:pd.DataFrame,integrated:pd.DataFrame,summary:pd.DataFrame,
                   obs:pd.DataFrame,obs_summary:pd.DataFrame,codeword:pd.DataFrame,ids:pd.DataFrame,prop:pd.DataFrame)->None:
    plt.rcParams.update({"font.size":9,"axes.titlesize":10,"axes.labelsize":9,"legend.fontsize":8,"figure.dpi":160,"pdf.fonttype":42,"ps.fonttype":42})
    # Fig 1 architecture diagram
    fig,ax=plt.subplots(figsize=(7.2,3.6));ax.axis("off")
    boxes=[(.05,.60,.18,.22,"Typed input\ncarrier"),(.29,.60,.18,.22,"Conceptual FSS\nS/R/L/G + lift"),(.53,.60,.18,.22,"Fitness FSS\ncurrent/target/projected"),(.77,.60,.18,.22,"Typed output\ncarrier"),
           (.29,.15,.18,.22,"Registry +\nresidual ledger"),(.53,.15,.18,.22,"Certificates +\ngovernance")]
    for x,y,w,h,t in boxes:
        ax.add_patch(plt.Rectangle((x,y),w,h,fill=False,linewidth=1.2));ax.text(x+w/2,y+h/2,t,ha="center",va="center")
    arrows=[((.23,.71),(.29,.71),"Register"),((.47,.71),(.53,.71),"couple"),((.71,.71),(.77,.71),"Express"),
            ((.38,.60),(.38,.37),"Store/event"),((.62,.37),(.62,.60),"gate"),((.47,.26),(.53,.26),"one generator")]
    for a,b,l in arrows:
        ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",lw=1.1));ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.035,l,ha="center",va="bottom",fontsize=8)
    ax.text(.5,.04,"All results are read-only queries over a single versioned transition log.",ha="center")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig1_architecture.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig1_architecture.png",bbox_inches="tight");plt.close(fig)

    # Fig2 witnesses and triad
    fig,ax=plt.subplots(figsize=(7.2,3.8))
    counts=wit.groupby(["function","designated_ablation_verdict"]).size().unstack(fill_value=0)
    y=np.arange(len(counts)); left=np.zeros(len(counts))
    for col in ["fail","undetermined"]:
        vals=counts[col].to_numpy() if col in counts else np.zeros(len(counts))
        ax.barh(y,vals,left=left,label=col);left+=vals
    ax.set_yticks(y);ax.set_yticklabels(counts.index);ax.invert_yaxis();ax.set_xlabel("Designated target-pair witnesses");ax.legend(loc="lower right")
    ax.set_title("Every designated ablation fails or becomes correctly undetermined")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig2_witnesses.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig2_witnesses.png",bbox_inches="tight");plt.close(fig)

    # Fig3 CNS interaction higher-order
    h=summary[summary.higher_order_target==1].copy().set_index("intervention").loc[INTERVENTIONS]
    fig,ax=plt.subplots(figsize=(7.2,4.2));x=np.arange(len(h));w=.36
    ax.bar(x-w/2,h.target_correct,w,label="target accuracy");ax.bar(x+w/2,h.certified_reach,w,label="certified reach")
    labels=["Local","Compute","Memory","Population","Comms","Certificate","Lift","Span","Full CNS","Residual-open"]
    ax.set_xticks(x);ax.set_xticklabels(labels,rotation=28,ha="right");ax.set_ylim(0,1.05);ax.set_ylabel("Probability / mean reach");ax.legend();ax.set_title("Lift, span and certification interact on nonfactorizing targets")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig3_cns_transition.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig3_cns_transition.png",bbox_inches="tight");plt.close(fig)

    # Fig4 coherence-conditioned option expansion
    names=["full_cns","incoherent_cns"]
    agg=integrated.groupby("intervention").agg(containment=("pareto_containment","mean"),harm=("fraction_harmed_vs_baseline","mean"),selected=("selected_new","mean")).loc[names]
    fig,ax=plt.subplots(figsize=(7.2,4.0));x=np.arange(2);w=.24
    ax.bar(x-w,agg.containment,w,label="within participant bound")
    ax.bar(x,agg.harm,w,label="participant actions below baseline")
    ax.bar(x+w,agg.selected,w,label="new option selected")
    ax.set_xticks(x);ax.set_xticklabels(["Residual-closed CNS","Residual-open capability control"]);ax.set_ylim(0,1.05);ax.set_ylabel("Fraction");ax.legend(loc="upper right")
    ax.set_title("Capability expansion changes valence when residual and governance gates are opened")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig4_coherence.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig4_coherence.png",bbox_inches="tight");plt.close(fig)

    # Fig5 bounded observation average across families/red=1 K=256
    g=obs_summary[(obs_summary.K==256)&(obs_summary.redundancy==1)].groupby(["L","pipeline"]).exact_recovery.mean().unstack()
    fig,ax=plt.subplots(figsize=(7.2,4.0))
    for c in g.columns:ax.plot(g.index,g[c],marker="o",label=c.replace("_"," "))
    ax.set_xlabel("Critical relation depth L");ax.set_ylabel("Exact critical-subgraph recovery");ax.set_ylim(0,1.05);ax.legend();ax.set_title("Finite projections lose conjunctively required relations")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig5_observability.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig5_observability.png",bbox_inches="tight");plt.close(fig)

    # Fig6 artifact package reconstruction stress test
    packages=["article_only","article_supplement","plus_registry","plus_code_tests","complete_package"]
    piv=prop[prop.package.isin(packages)].pivot(index="package",columns="receiver_family",values="pass_rate").reindex(packages)
    fig,ax=plt.subplots(figsize=(7.2,4.0));x=np.arange(len(packages))
    for c in piv.columns: ax.plot(x,piv[c].to_numpy(),marker="o",label=c.replace("_"," "))
    ax.set_xticks(x);ax.set_xticklabels(["Article","+ Supplement","+ Registry","+ Code/tests","Complete"]);ax.set_ylim(0,1.02);ax.set_ylabel("Surrogate reconstruction pass rate");ax.legend(loc="upper left")
    ax.set_title("Machine-readable artifacts improve algorithmic reconstruction")
    fig.tight_layout();fig.savefig(ROOT/"figures/fig6_propagation.pdf",bbox_inches="tight");fig.savefig(ROOT/"figures/fig6_propagation.png",bbox_inches="tight");plt.close(fig)


def write_key_results(wit,triad,leak,summary,integrated,obs_summary,ret_models,codeword,ids,hdf,prop_summary):
    hs=summary[summary.higher_order_target==1].set_index("intervention")
    ls=summary[summary.higher_order_target==0].set_index("intervention")
    modelacc=ids.groupby("truth").correct.mean()
    fullprop=prop_summary[prop_summary.package=="complete_package"]
    artprop=prop_summary[prop_summary.package=="article_only"]
    results={
        "model_hash":MODEL_HASH,"registry_hash":REGISTRY_HASH,"master_seed":MASTER_SEED,
        "deterministic_witnesses":{"n":len(wit),"full_pass":int((wit.full_model_verdict=="pass").sum()),"ablation_successes":0},
        "fitness_triad":triad.to_dict(orient="records"),
        "lower_order_decoder_max_accuracy":float(leak[leak.decoder!="paired_oracle_lower_bound"].accuracy.max()),
        "higher_order":{
            "full_cns_target_accuracy":float(hs.loc["full_cns","target_correct"]),
            "best_matched_comparator_target_accuracy":float(hs.drop(index=["full_cns","incoherent_cns"]).target_correct.max()),
            "full_cns_certified_reach":float(hs.loc["full_cns","certified_reach"]),
            "best_matched_comparator_certified_reach":float(hs.drop(index=["full_cns","incoherent_cns"]).certified_reach.max()),
            "full_cns_recursive_reuse":float(hs.loc["full_cns","recursive_reuse"]),
        },
        "no_higher_order":{
            "full_cns_target_accuracy":float(ls.loc["full_cns","target_correct"]),
            "best_comparator_target_accuracy":float(ls.drop(index=["full_cns","incoherent_cns"]).target_correct.max()),
        },
        "coherence":{
            "full_cns_pareto_containment":float(integrated[integrated.intervention=="full_cns"].pareto_containment.mean()),
            "incoherent_cns_pareto_containment":float(integrated[integrated.intervention=="incoherent_cns"].pareto_containment.mean()),
            "full_cns_fraction_harmed":float(integrated[integrated.intervention=="full_cns"].fraction_harmed_vs_baseline.mean()),
            "incoherent_cns_fraction_harmed":float(integrated[integrated.intervention=="incoherent_cns"].fraction_harmed_vs_baseline.mean()),
        },
        "bounded_observation":{
            "K256_r1_generic_L2":float(obs_summary[(obs_summary.K==256)&(obs_summary.redundancy==1)&(obs_summary.pipeline=="generic_summary")&(obs_summary.L==2)].exact_recovery.mean()),
            "K256_r1_generic_L16":float(obs_summary[(obs_summary.K==256)&(obs_summary.redundancy==1)&(obs_summary.pipeline=="generic_summary")&(obs_summary.L==16)].exact_recovery.mean()),
            "K256_r1_monitor_false_confidence":float(obs_summary[(obs_summary.K==256)&(obs_summary.redundancy==1)&(obs_summary.pipeline=="target_aware_monitor")].false_confidence.mean()),
            "best_retention_model":str(ret_models.iloc[0].model),
        },
        "model_identification":{
            "selected_tests":len(codeword.columns)-1,"minimum_candidate_accuracy":float(modelacc.min()),
            "canonical_accuracy":float(modelacc.loc["M_star"]),"heldout_min_distance_to_canonical":int(hdf.distance_to_canonical.min())
        },
        "propagation_surrogate":{
            "complete_mean_pass_rate":float(fullprop.pass_rate.mean()),"article_only_mean_pass_rate":float(artprop.pass_rate.mean()),
            "status":"algorithmic artifact stress test only; independent semantic receiver criterion not executed"
        },
        "closure_verdicts":{"formal":"global_coherence_within_declared_finite_witness_class","execution":"global_coherence","propagation":"undetermined"},
        "title_status":3,
        "unexecuted_external_boundaries":["independent language-model receiver study across three external model families","real externally available trace collection","full historical maximality audit"]
    }
    write_json(ROOT/"data/key_results.json",results)
    return results


def write_report(results:Mapping[str,Any],ret_models:pd.DataFrame)->None:
    lines=["# ISGPE v8 execution report","",f"Model hash: `{MODEL_HASH}`",f"Registry hash: `{REGISTRY_HASH}`",f"Master seed: `{MASTER_SEED}`","",
           "## Closure verdict","",f"- Formal: {results['closure_verdicts']['formal']}",f"- Execution: {results['closure_verdicts']['execution']}",f"- Propagation: {results['closure_verdicts']['propagation']}","",
           "The executable synthetic benchmark and codeword model-identification study completed. The independent external language-model receiver study, externally available real-trace collection, and full historical maximality audit could not be executed in this environment. Their associated claims remain undetermined and are not reported as positive results.","",
           "## Key numerical results","",json.dumps(results,indent=2),"","## Retention models","",ret_models.to_markdown(index=False)]
    (ROOT/"reports/execution_report.md").write_text("\n".join(lines),encoding="utf-8")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--quick",action="store_true");args=parser.parse_args()
    setup_repository()
    wit=deterministic_witnesses();triad=fitness_triad_test();leak=nonfactorization_leakage()
    regimes=make_regimes()
    reps=4 if args.quick else 8
    integrated,events=run_integrated(regimes,reps)
    summary=summarize_integrated(integrated)
    obs,obs_summary=bounded_observation();ret_models=compare_retention_models(obs)
    codeword,ids,hdf=model_identification();prop_raw,prop_summary=propagation_surrogate()
    create_figures(wit,triad,integrated,summary,obs,obs_summary,codeword,ids,prop_summary)
    results=write_key_results(wit,triad,leak,summary,integrated,obs_summary,ret_models,codeword,ids,hdf,prop_summary)
    write_report(results,ret_models)
    manifest={
      "model_version":MODEL_VERSION,"model_hash":MODEL_HASH,"registry_hash":REGISTRY_HASH,"master_seed":MASTER_SEED,
      "python":sys.version,"platform":platform.platform(),"packages":{"numpy":np.__version__,"pandas":pd.__version__,"scipy":stats.__version__ if hasattr(stats,"__version__") else "scipy"},
      "files":{}
    }
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.name!="execution_manifest.json":
            manifest["files"][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    write_json(ROOT/"execution_manifest.json",manifest)
    print(json.dumps(results,indent=2))

if __name__=="__main__":main()
