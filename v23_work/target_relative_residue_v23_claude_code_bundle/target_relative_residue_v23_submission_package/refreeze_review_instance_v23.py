#!/usr/bin/env python3
"""Regenerate the Version-23 frozen input manifest and review-instance hash.

Run only before an independent trace. Any manuscript, Lean, policy, schema, validator,
or carrier-evidence change invalidates prior trace outputs and requires this refreeze.
"""
from pathlib import Path
import hashlib, json, datetime

p = Path(__file__).resolve().parent
FROZEN = [
    'target_relative_residue_main_v23.tex',
    'target_relative_residue_main_v23.pdf',
    'target_relative_residue_supplement_v23.tex',
    'target_relative_residue_supplement_v23.pdf',
    'TargetRelativeResidueV23.lean', 'lean-toolchain', 'lakefile.lean',
    'TheoremLeanCorrespondence_v23.csv',
    'ClaimGenome_v23.csv', 'FunctionalGenome_v23.json',
    'ChoiceProposalManifest_v23.csv', 'ClaimCoverage_v23.csv',
    'EvidenceRegistry_v23.csv', 'GCAConfiguration_v23.json',
    'JournalProfileSnapshot_v23.json', 'JournalProfileSnapshot_v23.md',
    'NoveltyBaseline_v23.csv', 'SignificanceWarrant_v23.md',
    'TheoremCarrierMap_v23.csv', 'CarrierRepairClosureMatrix_v23.csv',
    'ExpectedGCDesignAssumptions_v23.md',
    'AssessmentIdentitySchema_v23.json',
    'TargetAdequacyCertificateSchema_v23.json',
    'CarrierChallengeSchema_v23.json', 'ChoiceRecordSchema_v23.json',
    'ExecutionRecordSchema_v23.json', 'CarrierRootCertificateSchema_v23.json',
    'validate_carrier_gca_trace_v23.py', 'refreeze_review_instance_v23.py',
    'setup_claude_code_environment_v23.sh', 'run_author_preflight_v23.sh',
    'run_qpdf_checks_v23.sh', 'run_lean_checks_v23.sh', 'apply_gca_result_v23.py',
    '00_CLAUDE_CODE_START_v23.md', 'CLAUDE_CODE_PROMPT_v23.txt', 'CLAUDE.md',
    'README_v23.md', 'REVISION_NOTES_v23.md', 'SubmissionChecklist_v23.md',
    'CoverLetter_v23.md', 'PDF_QA_REPORT_v23.md',
    'BuildCertificateTemplate_v23.md', 'README_Lean_v23.md', 'LEAN_STATIC_AUDIT_v23.md',
    'GCAReviewTraceTemplate_v23.jsonl', 'CarrierChallengesTemplate_v23.jsonl',
    'TargetAdequacyCertificateTemplate_v23.json', 'CarrierRootCertificateTemplate_v23.json',
    'QPDFCheckCertificateTemplate_v23.json',
    'IndependentSubstantiveWarrantReportTemplate_v23.md',
    'SecondOrderAuditTemplate_v23.md', 'ConventionalReviewStatus_v23.md'
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

missing = [name for name in FROZEN if not (p / name).is_file()]
if missing:
    raise SystemExit('Missing frozen inputs: ' + ', '.join(missing))
entries = {name: sha(p / name) for name in FROZEN}
corpus_hash = hashlib.sha256(
    json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
).hexdigest()
inst_path = p / 'GCAReviewInstance_v23.json'
inst = json.load(inst_path.open())
inst['input_corpus_files'] = entries
inst['input_corpus_hash'] = corpus_hash
inst['instance_status'] = 'frozen_inputs_pending_independent_execution'
inst['actual_status'] = 'NE'
inst['frozen_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
inst.pop('review_instance_hash', None)
inst_hash = hashlib.sha256(
    json.dumps(inst, sort_keys=True, separators=(',', ':')).encode()
).hexdigest()
inst['review_instance_hash'] = inst_hash
with inst_path.open('w') as f:
    json.dump(inst, f, indent=2)
    f.write('\n')
manifest = {
    'version': 'v23', 'record_type': 'frozen_input_manifest',
    'frozen_utc': inst['frozen_utc'], 'files': entries,
    'input_corpus_hash': corpus_hash, 'review_instance_hash': inst_hash,
    'excluded_execution_outputs': [
        'GCAExecutionStatus_v23.json', 'GCAResultAddendum_v23.md',
        'QPDFCheckCertificate_v23.json', 'QPDFCheckTranscript_v23.txt',
        'BuildCertificate_v23.md', 'LeanBuildTranscript_v23.txt',
        'TargetAdequacyCertificate_independent_v23.json',
        'CarrierChallenges_independent_v23.jsonl',
        'GCAReviewTrace_independent_v23.jsonl',
        'IndependentSubstantiveWarrantReport_v23.md', 'SecondOrderAudit_v23.md',
        'CarrierRootCertificate_independent_v23.json',
        'GCAReviewTraceValidation_independent_v23.txt'
    ]
}
with (p / 'FrozenInputManifest_v23.json').open('w') as f:
    json.dump(manifest, f, indent=2)
    f.write('\n')
status = json.load((p / 'GCAExecutionStatus_v23.json').open())
status.update({
    'actual_status': 'NE', 'actual_overall_verdict': None,
    'reason': 'Frozen inputs were regenerated; no independent trace for this instance has executed.',
    'review_instance_hash': inst_hash,
    'input_corpus_hash': corpus_hash,
    'expected_result_is_evidence': False,
    'updated_by': 'refreeze_review_instance_v23.py',
    'updated_utc': inst['frozen_utc']
})
with (p / 'GCAExecutionStatus_v23.json').open('w') as f:
    json.dump(status, f, indent=2)
    f.write('\n')
print('Frozen input corpus:', corpus_hash)
print('Review instance:', inst_hash)
