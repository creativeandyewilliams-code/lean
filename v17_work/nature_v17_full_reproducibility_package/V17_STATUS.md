# Nature v17 — master status vector

Assembled from two inputs on `main`:
`nature_v16_executed_experiments_reproducibility_package.zip` and
`nature_v16_unexecuted_experiments.zip`.

## A. Validation of the EXECUTED experiments — ALL PASS (deterministic)
`executed_experiments/run_all.sh` was re-run in a clean venv (numpy 2.3.5,
pandas 2.2.3, scipy 1.17.0, networkx 3.6.1, matplotlib 3.10.8,
scikit-learn 1.8.0). Every experiment's canonical fingerprint **matched** the
frozen result (see `executed_experiments/VALIDATION_fingerprint_match.log`):

| Experiment | Fingerprint | Match |
|---|---|---|
| Gate Zero (v8 lineage) | 60aececb566a8ab2 | ✅ |
| Direct recurrence | 7b8f8c0002633c9f | ✅ |
| Semantic equivalence (structural) | 06afccc2f7e0172d | ✅ |
| Governance option monotonicity | b4993f44e09f1bc4 | ✅ |
| GF branch/hazard (robust) | 346448509b350ca8 | ✅ |
| CST computational geometry | 18bb20e0171e9e00 | ✅ |

`verify_package.py` also passed (nothing missing). The six executed experiments
are correct and reproducible in their declared finite/synthetic classes.

## B. Execution of the UNEXECUTED experiments (7)
| Experiment | Disposition (v17) |
|---|---|
| EXP-RECEIVER-REGENERATIVE-MULTIAGENT | **EXECUTED (bounded, same-model isolated agents)**: 6 Receiver A (1/condition) + 1 Receiver B. Fatal-error rate 0.000 across all 6 conditions incl. corrupted; registered-claim-ID recovery 0.786 for direct_graph+Lean vs 0.000 for all other conditions; second-generation regeneration succeeded from a transmission alone with 0 author repairs. See `unexecuted_experiments/experiments/receiver_regenerative_multi_agent/run/RESULTS.md`. |
| EXP-EXTERNAL-TRACE | **Pipeline validated on fixtures** (20 records/10 paired worlds; version_lock="mock"). Decisive execution **BLOCKED**: requires genuinely external, version-locked traces (not available). |
| EXP-FORMALIZATION-FIDELITY-MULTIAGENT | **Packets generated + anonymized** (blinding flaw fixed: neutral ITEM-NN ids). Decisive reviewer-agent execution **INCOMPLETE — session agent/API limit reached mid-run.** Re-runnable per its execution doc. |
| EXP-CST-GEOMETRY-UTILITY-MULTIAGENT | Not agent-executed (session limit). Corroborated by the EXECUTED `cst_computational_geometry` (invariance/sensitivity = 1.000 across 600 worlds). |
| EXP-HISTORICAL-LIFT | Not agent-executed (session limit). Candidate dossiers + rubric present; re-runnable. |
| EXP-PHYSICAL-FSS-MAPPING | Not agent-executed (session limit). Falsification-first certificates present; **primary physical evidence is an external blocker for promotion** regardless. |
| EXP-LEAN-FORMAL-CLOSURE | **BLOCKED**: the Lean 4.32.0 toolchain binary is blocked by the org egress policy (HTTP 403 on GitHub release assets; Mathlib source reachable but no compiler). A separately delivered build-ready package (`nature_v16_expanded_lean_build_package`) is static-validated (32 files, 0 sorry/axiom, 33 targets declared, pins consistent) and runs on any CI with GitHub access. |

## Honest summary
Validation of the executed science is complete and passing. Of the 7 unexecuted
experiments, the flagship multi-agent receiver study was genuinely executed at
bounded scale with real isolated agents; the external-trace pipeline was
validated on fixtures; the remaining agent-driven experiments (fidelity, CST,
historical, physical) could not be completed because the session reached its
agent/API limit mid-run, and Lean remains egress-blocked. Nothing synthetic or
mock is promoted to external evidence; no receiver families beyond same-model
instances are claimed.
