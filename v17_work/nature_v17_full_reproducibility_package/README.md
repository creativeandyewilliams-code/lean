# nature_v17_full_reproducibility_package

Combines the validated executed v16 experiments with the executed portion of the
previously-unexecuted experiments. Read `V17_STATUS.md` first — it is the master
status vector. `EXECUTIVE_SUMMARY.md` is a one-screen overview.

- `executed_experiments/` — 6 finite/synthetic experiments, INDEPENDENTLY
  RE-RUN and fingerprint-matched here (Gate Zero, direct recurrence, structural
  semantic equivalence, governance option monotonicity, GF branch/hazard, CST
  geometry). Rebuild: `cd executed_experiments && ./run_all.sh`.
- `unexecuted_experiments/` — the 7 decisive experiments. The receiver study was
  EXECUTED here with real isolated agents (see
  `.../receiver_regenerative_multi_agent/run/RESULTS.md`); the external-trace
  pipeline was validated on fixtures. Fidelity/CST/historical/physical and the
  Lean kernel build remain open for the reasons in `V17_STATUS.md`.

No mock-agent output is a scientific result; no synthetic/formal mapping is
promoted to external evidence; receiver claims are same-model isolated-instance
only.
