#!/usr/bin/env python3
"""Structural output gate for a carrier-complete Version-23 GCA trace.

This validator checks identity, frozen-input hashes, target adequacy, typed challenges,
seven-action Choice records, matching executions, budgets, root coverage, and the
mechanical certificates required for GC_sub. It does not replace mathematical or
carrier warrant; those remain the responsibility of the substantive report and audit.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ACTIONS = {'local','global','decompose','acquire_info','revise_model','rollback','halt_UB'}
FIT = {'f0':0,'f1':1,'f2':2,'f3':3,'f4':4}
GLOBAL_ROOTS = {'O00','T00','F00','C00','A00','R00','E00'}
MANDATORY_FAMILIES = {'target_adequacy','formal_correctness','carrier_adequacy','artifact_fidelity','review_closure','editorial_stage'}

def canonical_hash(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_jsonl(path: Path) -> list[dict]:
    records=[]
    for i,line in enumerate(path.read_text().splitlines(),1):
        if not line.strip():
            continue
        try:
            rec=json.loads(line)
        except Exception as e:
            fail(f'{path.name}:{i}: invalid JSON: {e}')
        if not isinstance(rec,dict):
            fail(f'{path.name}:{i}: record is not an object')
        records.append(rec)
    return records

def fail(msg: str) -> None:
    print('INVALID:',msg,file=sys.stderr)
    raise SystemExit(1)

def require_text(rec: dict, key: str, n: int=20) -> None:
    val=rec.get(key)
    if not isinstance(val,str) or len(val.strip())<n or val.strip().upper()=='FILL-IN':
        fail(f"{rec.get('record_id') or rec.get('challenge_id')}: inadequate {key}")

def verify_instance(package: Path, inst: dict) -> None:
    stored=inst.get('review_instance_hash')
    temp=dict(inst); temp.pop('review_instance_hash',None)
    if stored!=canonical_hash(temp):
        fail('review-instance self-hash is invalid')
    files=inst.get('input_corpus_files')
    if not isinstance(files,dict) or not files:
        fail('input corpus file map missing')
    current={}
    for name,expected in files.items():
        path=package/name
        if not path.is_file():
            fail(f'frozen input missing: {name}')
        actual=sha(path)
        current[name]=actual
        if actual!=expected:
            fail(f'frozen input hash mismatch: {name}')
    if canonical_hash(current)!=inst.get('input_corpus_hash'):
        fail('input-corpus aggregate hash mismatch')

def check_target(target: dict, inst: dict) -> None:
    if not target.get('adequate'):
        fail('target adequacy not established')
    if target.get('requested_target_hash')!=inst.get('requested_target_hash'):
        fail('requested target hash mismatch')
    if target.get('frozen_target_hash')!=inst.get('frozen_target_hash'):
        fail('frozen target hash mismatch')
    fam=set(target.get('included_families',[]))
    if not MANDATORY_FAMILIES.issubset(fam):
        fail('carrier-complete target families missing')
    if target.get('residual_pair_challenges'):
        unresolved=[x for x in target['residual_pair_challenges'] if not isinstance(x,dict) or not x.get('resolved')]
        if unresolved:
            fail('unresolved target-selection residual-pair challenge')
    for w in target.get('omission_witnesses',[]):
        if not isinstance(w,dict) or not w.get('root_invariant') or len(str(w.get('rationale','')))<20:
            fail('invalid omission/root-invariance witness')

def check_challenge(ch: dict, node_ids: set[str]) -> None:
    cid=ch.get('challenge_id')
    if ch.get('node_id') not in node_ids:
        fail(f'{cid}: unknown challenged node')
    require_text(ch,'challenged_object')
    require_text(ch,'admissible_variation')
    require_text(ch,'activation_condition')
    require_text(ch,'defeat_condition')
    require_text(ch,'resolution_summary')
    path=ch.get('root_relevance_path')
    if not isinstance(path,list) or len(path)<2 or path[0]!=ch.get('node_id') or path[-1]!='O00':
        fail(f'{cid}: invalid root-relevance path')
    if ch.get('recommendation_effect') not in {'none','minor_non_root','major_revision','reject'}:
        fail(f'{cid}: invalid recommendation effect')
    if ch.get('resolved') and not ch.get('resolution_record_ids'):
        fail(f'{cid}: resolved challenge lacks resolution records')

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('trace')
    ap.add_argument('--instance',required=True)
    ap.add_argument('--root-certificate',required=True)
    args=ap.parse_args()
    trace_path=Path(args.trace).resolve()
    package=Path(args.instance).resolve().parent
    inst=json.load(open(args.instance))
    root=json.load(open(args.root_certificate))
    recs=load_jsonl(trace_path)
    verify_instance(package,inst)
    if not recs or recs[0].get('record_type')!='assessment_identity':
        fail('first trace record must be assessment_identity')
    if any(r.get('template') for r in recs) or root.get('template'):
        fail('template records are non-executable')
    expected_hash=inst['review_instance_hash']; corpus=inst['input_corpus_hash']
    for r in recs+[root]:
        rid=r.get('record_id') or r.get('challenge_id')
        if r.get('review_instance_hash')!=expected_hash:
            fail(f'review-instance mismatch in {rid}')
        if r.get('input_corpus_hash')!=corpus:
            fail(f'input-corpus mismatch in {rid}')
    identities=[r for r in recs if r.get('record_type')=='assessment_identity']
    targets=[r for r in recs if r.get('record_type')=='target_adequacy']
    choices=[r for r in recs if r.get('record_type')=='choice_record']
    execs=[r for r in recs if r.get('record_type')=='execution_record']
    challenges=[r for r in recs if r.get('record_type')=='carrier_challenge']
    if len(identities)!=1 or len(targets)!=1:
        fail('exactly one identity and one target-adequacy record required')
    ident=identities[0]
    if ident.get('trace_kind')!='independent_carrier_complete' or ident.get('genome_version')!='v23':
        fail('assessment identity is not a Version-23 independent carrier-complete trace')
    if ident.get('target_hash')!=inst.get('requested_target_hash') or ident.get('policy_hash')!=inst.get('policy_hash'):
        fail('assessment identity target/policy mismatch')
    check_target(targets[0],inst)
    nodes=list(csv.DictReader((package/'ClaimGenome_v23.csv').open()))
    node_ids={r['NodeID'] for r in nodes}
    if len(node_ids)!=71:
        fail('frozen claim genome is not 71 unique nodes')
    for ch in challenges:
        check_challenge(ch,node_ids)
    if not choices or len(choices)!=len(execs):
        fail('nonempty matching Choice/execution counts required')
    choice_by_id={r.get('record_id'):r for r in choices}
    if None in choice_by_id or len(choice_by_id)!=len(choices):
        fail('Choice record identifiers missing or duplicated')
    choice_counts=Counter(); action_history=defaultdict(list)
    prior_seq=0
    for c in choices:
        require_text(c,'choice_rationale',30)
        seq=c.get('sequence_index')
        if not isinstance(seq,int) or seq<=prior_seq:
            fail('Choice sequence indexes must be strictly increasing')
        prior_seq=seq
        node=c.get('node_id')
        if node not in node_ids:
            fail(f'unknown Choice node: {node}')
        choice_counts[node]+=1
        if choice_counts[node]>1 and not c.get('triggering_challenge_ids'):
            fail(f'reopened node {node} lacks triggering challenge')
        cand=c.get('candidates',[])
        if len(cand)!=7 or {x.get('action_type') for x in cand}!=ACTIONS:
            fail(f'complete seven-action candidate set missing at {node}')
        cand_ids=[x.get('candidate_id') for x in cand]
        if None in cand_ids or len(set(cand_ids))!=7:
            fail(f'duplicate/missing candidate ID at {node}')
        applicable=[]
        for x in cand:
            app=x.get('applicability',{})
            if app.get('status') not in {'applicable','inapplicable'}:
                fail(f'invalid applicability at {node}')
            if app.get('status')=='inapplicable':
                if len(str(app.get('witness','')))<15 or x.get('fitness_class')!='f0':
                    fail(f'inapplicable candidate lacks witness/bottom fitness at {node}')
            else:
                applicable.append(x)
            po=x.get('projected_outcome',{})
            if po.get('node_id')!=node or len(str(po.get('summary','')))<20 or not isinstance(po.get('feature_vector'),dict):
                fail(f'candidate-specific projection missing at {node}')
            if x.get('fitness_class') not in FIT or len(str(x.get('comparison_rationale','')))<20:
                fail(f'fitness/rationale missing at {node}')
            if not isinstance(x.get('evidence_refs'),list):
                fail(f'evidence refs missing at {node}')
        if not applicable:
            fail(f'no applicable candidate at {node}')
        maxfit=max(FIT[x['fitness_class']] for x in applicable)
        best={x['candidate_id'] for x in applicable if FIT[x['fitness_class']]==maxfit}
        if set(c.get('best_candidate_ids',[]))!=best:
            fail(f'best candidate class misreported at {node}')
        if c.get('best_fitness_class')!=f'f{maxfit}':
            fail(f'best fitness class misreported at {node}')
        if c.get('selected_candidate_id') not in best:
            fail(f'selected candidate is not greatest fitness at {node}')
        selected=[x for x in cand if x['candidate_id']==c['selected_candidate_id']]
        if len(selected)!=1 or selected[0]['action_type']!=c.get('selected_action'):
            fail(f'selected action mismatch at {node}')
        action_history[node].append(c.get('selected_action'))
    exec_by_choice={}
    last_exec_seq=0
    budget_prev=None
    for e in execs:
        require_text(e,'execution_result')
        seq=e.get('sequence_index')
        if not isinstance(seq,int) or seq<=last_exec_seq:
            fail('execution sequence indexes must be strictly increasing')
        last_exec_seq=seq
        cid=e.get('choice_record_id'); c=choice_by_id.get(cid)
        if not c or cid in exec_by_choice:
            fail('execution has missing or duplicated Choice link')
        exec_by_choice[cid]=e
        for key in ['node_id','selected_candidate_id','selected_action']:
            if e.get(key)!=c.get(key):
                fail(f'Choice/execution mismatch in {key}')
        if e.get('validation_result')!='valid':
            fail('invalid action executed')
        if e.get('status_after') not in {'conditionally accepted','global coherence assessed'}:
            fail('invalid post-execution status')
        if not isinstance(e.get('unresolved_residue'),list) or not isinstance(e.get('active_conditions'),list):
            fail('execution residue/conditions not typed as arrays')
        if e.get('history_before')==e.get('history_after') or not e.get('history_after'):
            fail('history did not advance')
        before=e.get('budget_before'); after=e.get('budget_after')
        if not isinstance(before,dict) or not isinstance(after,dict):
            fail('budget record missing')
        if budget_prev is not None and before!=budget_prev:
            fail('budget chain discontinuity')
        budget_prev=after
        action=e.get('selected_action')
        key='global' if action=='global' else 'local' if action=='local' else 'meta'
        for k in ['local','global','meta','total_transitions']:
            if not isinstance(before.get(k),int) or not isinstance(after.get(k),int):
                fail('budget coordinate missing/noninteger')
        if after['total_transitions']!=before['total_transitions']-1 or after[key]!=before[key]-1:
            fail('budget debit does not match selected action')
        for k in {'local','global','meta'}-{key}:
            if after[k]!=before[k]:
                fail('unselected budget coordinate changed')
    missing=node_ids-set(choice_counts)
    if missing:
        fail('frozen nodes never assessed: '+','.join(sorted(missing)))
    if root.get('record_type')!='carrier_root_aggregation':
        fail('wrong root record type')
    covered=root.get('covered_nodes',[])
    if len(covered)!=71 or set(covered)!=node_ids:
        fail('root coverage must contain every frozen node exactly once')
    statuses=root.get('final_node_statuses')
    if not isinstance(statuses,dict) or set(statuses)!=node_ids:
        fail('root final-node status map incomplete')
    if any(v not in {'conditionally accepted','global coherence assessed'} for v in statuses.values()):
        fail('invalid final node status')
    verdict=root.get('derived_verdict'); recommendation=root.get('integrated_recommendation')
    if verdict not in {'GC_sub','GI','UB'}:
        fail('invalid derived verdict')
    if root.get('editorial_stage')!='submission' or root.get('future_decision_registered') is not True:
        fail('submission-stage editorial state incorrectly represented')
    if verdict=='GC_sub':
        if recommendation not in {'accept','accept_non_root_edits'}:
            fail('GC_sub blocked by integrated recommendation')
        if root.get('unresolved_root_residue') or root.get('active_root_conditions'):
            fail('GC_sub blocked by root residue/condition')
        if root.get('target_adequacy_record_id')!=targets[0].get('record_id'):
            fail('GC_sub lacks exact target-adequacy link')
        for n in GLOBAL_ROOTS:
            if 'global' not in action_history[n] or statuses.get(n)!='global coherence assessed':
                fail(f'GC_sub lacks global execution/status for {n}')
        unresolved=[ch for ch in challenges if ch.get('recommendation_effect') in {'major_revision','reject'} and not ch.get('resolved')]
        if unresolved:
            fail('unresolved recommendation-changing challenge')
        required_paths={
            'qpdf_certificate':'QPDF certificate',
            'lean_build_certificate':'Lean build certificate',
            'substantive_warrant_report':'substantive warrant report',
            'second_order_audit':'second-order audit'
        }
        resolved_paths={}
        for key,label in required_paths.items():
            val=root.get(key)
            path=(package/val).resolve() if val and not Path(val).is_absolute() else Path(val or '')
            if not path.is_file() or path.stat().st_size<40:
                fail(f'GC_sub missing {label}')
            resolved_paths[key]=path
        q=json.load(resolved_paths['qpdf_certificate'].open())
        if not q.get('all_exit_zero') or q.get('warning_exit_0_used') or q.get('status')!='executed':
            fail('GC_sub lacks valid qpdf exit-zero certificate')
        qfiles={x.get('path'):x for x in q.get('files',[])}
        for pdf in ['target_relative_residue_main_v23.pdf','target_relative_residue_supplement_v23.pdf']:
            item=qfiles.get(pdf)
            if not item or item.get('exit_code')!=0 or item.get('sha256')!=sha(package/pdf):
                fail(f'qpdf certificate is not bound to exact {pdf}')
        lean_text=resolved_paths['lean_build_certificate'].read_text()
        if not re.search(r'(?im)^- Status:\s*successful\s*$',lean_text) or not re.search(r'(?im)^- Exit code:\s*0\s*$',lean_text):
            fail('GC_sub lacks successful Lean certificate')
        lean_hash=sha(package/'TargetRelativeResidueV23.lean')
        if lean_hash not in lean_text:
            fail('Lean certificate is not bound to exact source hash')
        for key in ['substantive_warrant_report','second_order_audit']:
            text=resolved_paths[key].read_text()
            if len(text)<1000 or 'template' in text[:200].lower():
                fail(f'{key} is too short or still a template')
        if root.get('trace_well_formed') is not True or root.get('trace_warranted') is not True or root.get('root_derives') is not True:
            fail('GC_sub root lacks explicit well-formedness, warrant, or derivation attestation')
    print(f'STRUCTURALLY VALID v23 carrier-complete trace. Derived verdict: {verdict}; recommendation: {recommendation}; choices: {len(choices)}; challenges: {len(challenges)}')

if __name__=='__main__':
    main()
