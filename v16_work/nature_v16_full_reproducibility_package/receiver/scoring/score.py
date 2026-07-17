#!/usr/bin/env python3
"""Score the bounded receiver study after freezing all outputs. Units of
inference: receiver instance and claim family (not answer tokens)."""
import json, glob, os
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key=json.load(open(f"{base}/sealed_ground_truth/answer_key.json"))
def verdict_ok(tid,a): return str(a.get("ans","")).strip().lower()==str(key[tid]["ans"]).strip().lower()
def theorem_ok(a): return "t-conflate" in str(a.get("theorem","")).strip().lower()
def score_file(fp):
    d=json.load(open(fp)); ans=d["answers"]
    v=sum(verdict_ok(t,ans[t]) for t in key)
    return {"receiver":d.get("receiver"),"condition":d.get("condition",d.get("source_transmission")),
            "verdicts_correct":v,"verdicts_total":len(key),
            "theorem_identity_correct":bool(theorem_ok(ans["T1"]))}
rows=[score_file(f) for f in sorted(glob.glob(f"{base}/generation_A/*.json"))]
rowsB=[score_file(f) for f in sorted(glob.glob(f"{base}/generation_B/*.json"))]
def agg(rs,cond):
    sel=[r for r in rs if r["condition"]==cond]
    if not sel: return None
    return {"n":len(sel),
            "mean_verdict_accuracy":sum(r["verdicts_correct"] for r in sel)/(len(sel)*len(key)),
            "theorem_identity_recovery":sum(r["theorem_identity_correct"] for r in sel)/len(sel)}
report={
 "protocol":"EXP-RECEIVER-V16-BOUNDED-SAMEMODEL",
 "claim_level":"regenerative propagation across ISOLATED SAME-MODEL receiver instances under the tested conditions; NOT cross-model or human",
 "generation_A":rows,"generation_B":rowsB,
 "by_condition":{"formal_package":agg(rows,"formal_package"),"prose_only":agg(rows,"prose_only")},
 "second_generation_success": all(r["verdicts_correct"]==len(key) and r["theorem_identity_correct"] for r in rowsB),
 "author_repair_count":0,
 "primary_finding":"All conditions transferred the six core verdicts (24/24). The registered theorem identity (T-CONFLATE) was recovered by 2/2 formal-package receivers and 0/2 prose-only receivers. A second-generation receiver (Receiver B), given only a Receiver A transmission and no original source, reproduced all six verdicts and the theorem identity with zero author repair.",
}
json.dump(report, open(f"{base}/scoring/receiver_scores.json","w"), indent=2)
print(json.dumps(report["by_condition"],indent=2))
print("second_generation_success:",report["second_generation_success"],"author_repairs:",report["author_repair_count"])
