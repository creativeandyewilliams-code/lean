# Claude Code bundle quick start — Version 23

This outer README is transport guidance only. The frozen submission and assessment instance are inside `target_relative_residue_v23_submission_package/`.

1. Extract this ZIP.
2. Open `target_relative_residue_v23_submission_package/` as the Claude Code project directory so its `CLAUDE.md` is loaded.
3. Read `00_CLAUDE_CODE_START_v23.md` before changing or assessing anything.
4. Run, in order:
   ```bash
   bash setup_claude_code_environment_v23.sh
   bash run_author_preflight_v23.sh
   bash run_qpdf_checks_v23.sh
   bash run_lean_checks_v23.sh
   ```
5. Repair Lean or any other load-bearing defect without weakening theorem statements. Rebuild the PDFs and rerun all checks after every load-bearing change.
6. After the files are stable, refreeze the review instance:
   ```bash
   python3 refreeze_review_instance_v23.py
   ```
   Refreezing invalidates all earlier traces.
7. Perform a fresh carrier-complete global-coherence assessment. Do not reuse the expected verdict. Include formal correctness, artifact fidelity, novelty, significance, journal fit, peer-review objections, integrated recommendation, and submission-stage editorial status in the same root target.
8. Produce all outputs listed in `00_CLAUDE_CODE_START_v23.md`, then validate the trace with `validate_carrier_gca_trace_v23.py`.
9. Apply only the actual validated result with `apply_gca_result_v23.py`. `GC_sub` is permitted only if the integrated carrier recommendation is accept-level and every required certificate closes. Otherwise record `GI`, `UB`, or `NE` as warranted.
10. Do not recompile or mutate the frozen PDFs after the final assessment. Any required manuscript change creates a successor version and requires a new freeze and trace.
