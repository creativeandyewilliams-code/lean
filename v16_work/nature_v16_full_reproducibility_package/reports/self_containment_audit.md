# Self-containment audit
The package rebuilds its computational artifacts from included inputs:
- v8 lineage under original_inputs/ (+ run_experiment.py inside the zip) → Gate Zero.
- experiments/*/code + protocol/seed → recurrence, mutation, branch/hazard.
- receiver/ contains tasks, sealed key, generation A/B outputs, scorer.
- lean/ is a self-contained pure-Lean project (no external libraries).
Not self-buildable HERE (documented environment blockers, not package defects):
- Lean kernel build (toolchain download egress-blocked, HTTP 403).
- LaTeX PDF compile (no engine; PDFs rendered by included tool; .tex provided).
