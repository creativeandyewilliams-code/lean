# Gate Zero v16 — v8 positive reproduction audit

**Audit ID:** EXP-GATE-ZERO-V16-EXECUTED-REPRODUCTION
**Disposition:** **closed-positive**
**Supersedes:** v15 `FAIL_CLOSED_MISSING_EXECUTABLE_LINEAGE`

## Inputs
- `nature_v8_full_reproducibility_package.zip`
  SHA-256 `f21b7ba677c32140710092405a37de460f81a77fe8f6c459a965266eb8842a72`
  — **matches the reference hash exactly** (no repackage/revision difference).
- Pinned environment rebuilt in a clean venv: numpy 2.3.5, pandas 2.2.3,
  scipy 1.17.0, networkx 3.6.1, matplotlib 3.10.8, scikit-learn 1.7.2.
  `tabulate` (an unpinned optional pandas dependency used only by the report
  writer) was additionally installed; this is a packaging fix, not a change to
  model semantics.

## Procedure
1. Verified the v8 zip hash against the reference.
2. Validated `execution_manifest.json`: **58 files listed, 0 hash mismatches**.
3. Ran `python run_experiment.py` from a writable copy (not the immutable
   original). Exit 0, ~17 s.
4. Ran `python tests/test_conformance.py`. Exit 0 (all conformance checks pass).
5. Compared every regenerated data file against the archived original,
   decompressing `.gz` files and hashing content.

## Results
- `model_hash` = `797b16e3…607bf3` — **matches** the manifest and reference.
- `registry_hash` = `b7a6ef0e…ad0385` — **matches**.
- `master_seed` = 20260715; 12,800 trajectories; 102,400 events; 23 witnesses,
  all pass, 0 ablation successes.
- **All 18 data files are semantically identical** after gzip decompression,
  including the 45 MB `event_log.csv.gz` and `integrated_trajectories.csv.gz` —
  a bit-exact deterministic reproduction.
- Key-value crosswalk: **12 / 12 reference values reproduced at full
  precision** (see `experiments/gate_zero_v16/reports/result_crosswalk.csv`),
  including full-CNS accuracy 0.5845588235294118, best matched comparator
  0.39950980392156865, full-CNS certified reach 0.4349877450980392, best
  comparator certified reach 0.003308823529411765, reuse 0.34681372549019607,
  Pareto containment 0.98671875, incoherent containment 0.7171875, harmed
  fractions 0.012109375 / 0.155712890625, lower-order decoder max accuracy
  0.4805714285714286, canonical codeword identification 0.94, and
  correlation-aware held-out log loss 0.258278.
- `reproduction_differences.csv` is **empty** (no differences).

## v8-to-v16 semantic conformance
The v8 generator uses one canonical `step` transition (single generator; no
split), stable model/registry hashes, event-sourced state, and rebuilds every
reported metric from the source event log. Inherited numbers are therefore
promoted from "historical constructive witness (unverifiable lineage)" to
**"conformant — reproduced from source events under the single generator"**.
Claims that depend on unrepresented v8 variables remain out of scope; no v16
meaning is imputed to variables the v8 code does not represent.

## Consequence for the manuscripts
The v15 fail-closed disposition is removed. Article/Supplement v16 report these
values as a reproduced finite constructive witness (synthetic; not a
measurement of real AI systems or civilizations).
