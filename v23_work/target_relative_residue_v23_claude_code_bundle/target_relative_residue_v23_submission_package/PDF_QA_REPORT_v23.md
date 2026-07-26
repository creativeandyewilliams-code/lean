# PDF QA Report — Version 23

Authoring-environment checks completed on 2026-07-26:

- Main manuscript: 9410 source-counted words; 19 A4 pages; SHA-256 `7492e74578fae496e3609ef7170156e11cdcafe83ea62aa287a269a4405dd63d`.
- Formal supplement: 9 A4 pages; SHA-256 `3015eff286f8ae6de38de4145ef5563631edfbbf3773a3dfbcf7456b0b037cee`.
- LaTeX: both files compiled with `latexmk -pdf -interaction=nonstopmode -halt-on-error`.
- Logs: no overfull boxes, undefined references, or LaTeX warnings after the final build.
- Fonts: main PDF reports 34 font records and supplement reports 22; non-embedded font records: main 0, supplement 0.
- Poppler: `pdfinfo`, `pdftotext`, and full-page rendering succeeded for both PDFs.
- Visual inspection: every rendered page was inspected; no clipping, missing glyphs, broken figures, or unreadable tables were observed.
- qpdf: not executed in the authoring environment because the executable is unavailable. No qpdf result is claimed. `run_qpdf_checks_v23.sh` requires a fresh exact-hash check in Claude Code or another controlled environment before `GC_sub` can validate.

The qpdf and Lean checks are independent execution outputs and must be bound to the exact frozen input hashes recorded by `refreeze_review_instance_v23.py`.
