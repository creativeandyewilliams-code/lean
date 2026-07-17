# Manuscript claim audit (numbers traced to executed source)
- Gate Zero values (0.5845588…, 0.4349877…, 0.98671875, 0.7171875, 0.94,
  0.258278, …) → experiments/gate_zero_v16/reports/result_crosswalk.csv
  (12/12 exact) regenerated from the v8 run.
- Recurrence numbers (fixed final 694 [583,797]; branch 989 [867,1104];
  proportional/regenerative/second-lift recurrence 0.000) →
  experiments/direct_recurrence/derived/summary.json + recurrence_table.csv.
- Receiver claims (24/24 verdicts; formal 1.0 vs prose 0.0 theorem-identity;
  2nd-gen success; 0 author repairs) → receiver/scoring/receiver_scores.json.
- Lean claims (10 core theorems, static audit 0 sorry/axiom, build blocked) →
  lean/reports/{static_audit.txt,theorem_coverage.json,toolchain_block_evidence.txt}.
- GF branch/hazard (non-summable→filter forms; independent branching resists) →
  experiments/gf_branch_closure/reports/branch_hazard_results.json.
No manuscript number is hand-copied without a machine-readable source in-package.
