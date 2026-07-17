# ISGPE v8 computational package

This package implements the finite synthetic experiment reported in **Recursive operand closure and certified spanning generate a cognitive near-singularity**. One function, `step`, is the only state transition used by the integrated benchmark. All tables and figures are read-only queries over its event log.

## Rebuild

```bash
python run_experiment.py
python tests/test_conformance.py
cd manuscript
pdflatex nature_article_v8.tex
bibtex8 nature_article_v8
pdflatex nature_article_v8.tex
pdflatex nature_article_v8.tex
pdflatex nature_supplement_v8.tex
bibtex8 nature_supplement_v8
pdflatex nature_supplement_v8.tex
pdflatex nature_supplement_v8.tex
```

The confirmatory execution uses master seed `20260715`, 128 scrambled Sobol regimes, 32 corner regimes, 8 common-random-number replicates, 10 intervention conditions, 12,800 trajectories, and 102,400 logged transitions. The replicate count was fixed after a runtime-only pilot. The package includes raw compressed trajectories, the complete event log, bounded-observation records, model codewords, held-out variants, and an algorithmic artifact-reconstruction stress test.

## Status boundary

The synthetic mechanism, deterministic witness, event-replay, and model-identification studies were executed. Three external boundaries in the revision plan could not be executed in this environment: an independent receiver study using three external language-model families, collection of externally available reasoning traces from three version-locked model families, and a full historical maximality audit. The Article and Supplement therefore report propagation closure and historical rank as **undetermined**, not as positive findings. The included algorithmic receiver stress test only verifies machine readability of the artifact layers; it is not a substitute for independent semantic reconstruction.

## Directory guide

- `registry/`: canonical functions, aliases, and stored obligations R1/R2.
- `schema/`: canonical state and event schemas.
- `configs/`: frozen synthetic configuration.
- `data/`: raw and summary results.
- `figures/`: PDF and PNG figures.
- `tests/`: conformance and replay checks.
- `manuscript/`: Article and Supplement source and PDFs.
- `reports/`: execution, conformance, preflight, and submission-status reports.
- `CHANGES_v8.md`: substantive differences introduced in v8.
