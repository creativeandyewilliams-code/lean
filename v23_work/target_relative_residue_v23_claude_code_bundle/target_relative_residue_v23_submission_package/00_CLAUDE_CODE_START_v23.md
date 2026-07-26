# START HERE - Claude Code independent carrier-complete audit (v23)

The package is written toward an expected result of `GC_sub`, but its actual starting status is `NE`. Your task is to execute a fresh assessment, not to confirm the expectation.

## 1. Environment
Run:
```bash
bash setup_claude_code_environment_v23.sh
```
The script checks for Python, LaTeX, Poppler, qpdf, Git, and Lean/Lake. On Debian/Ubuntu it attempts to install missing qpdf/Poppler/LaTeX utilities when privileges and network permit. Claude Code can run any terminal command available to the host; project `CLAUDE.md` instructions load at session start.

## 2. Mechanical preflight
```bash
bash run_author_preflight_v23.sh
bash run_qpdf_checks_v23.sh
bash run_lean_checks_v23.sh
```
Do not use `qpdf --warning-exit-0`. Exit 0 means qpdf found no errors or warnings; exit 3 means warnings and does not satisfy the registered qpdf condition.

## 3. Freeze after mechanical repair
If Lean debugging, manuscript correction, schema repair, or any other change modifies a frozen input, complete those repairs first, rebuild both PDFs, rerun qpdf, and then execute:
```bash
python3 refreeze_review_instance_v23.py
```
This invalidates every earlier trace. Do not begin semantic assessment until the source, PDFs, Lean file, policy, schemas, validator, and carrier evidence are stable and the new review-instance hash is recorded.

## 4. Semantic carrier assessment
- Read the main paper, supplement, frozen instance, genome, novelty baseline, significance warrant, theorem map, and current journal snapshot.
- Recheck the official journal profile if internet access is available. A changed profile creates a successor instance or non-GC result.
- Verify target adequacy before assessing closure.
- Perform a fresh conventional review. Import every objection that can change the recommendation.
- Execute Choice for every frozen node and every reopened node. Represent all seven actions.
- Produce node-specific projections, fitness comparisons, selected actions, executions, histories, residue, conditions, and budgets.
- Produce a substantive-warrant report and second-order audit.
- Integrate the journal recommendation into the root. Major revision or reject cannot aggregate to GC_sub.

## 5. Required outputs
- `TargetAdequacyCertificate_independent_v23.json`
- `CarrierChallenges_independent_v23.jsonl`
- `GCAReviewTrace_independent_v23.jsonl`
- `IndependentSubstantiveWarrantReport_v23.md`
- `SecondOrderAudit_v23.md`
- `CarrierRootCertificate_independent_v23.json`
- `GCAReviewTraceValidation_independent_v23.txt`
- completed `QPDFCheckCertificate_v23.json` and `BuildCertificate_v23.md`

Validate:
```bash
python3 validate_carrier_gca_trace_v23.py GCAReviewTrace_independent_v23.jsonl \
  --instance GCAReviewInstance_v23.json \
  --root-certificate CarrierRootCertificate_independent_v23.json
```

## 6. Apply actual result
Only after validation:
```bash
python3 apply_gca_result_v23.py --verdict GC_sub --root-certificate CarrierRootCertificate_independent_v23.json
```
Use `GI`, `UB`, or `NE` instead when that is the actual result. Do not recompile the frozen PDFs. If the actual result requires manuscript changes, create a successor version and rerun the complete assessment. Do not preserve the expected GC wording if the actual trace disagrees.
