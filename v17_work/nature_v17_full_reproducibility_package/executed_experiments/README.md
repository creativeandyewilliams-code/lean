# Nature v16 executed experiments reproducibility package

This archive contains experiments that were implemented and executed in the present environment. It is designed to make every reported number regenerable from code and frozen inputs.

## Executed experiments

1. **EXP-GATE-ZERO-V16-RERUN** — reruns the complete v8 generator and conformance suite and compares the regenerated key results to the frozen v8 record.
2. **EXP-DIRECT-RECURRENCE-V16-RERUN** — reruns the paired common-world queue-and-region recurrence experiment.
3. **EXP-SEMANTIC-EQUIVALENCE-STRUCTURAL-V16** — tests invariance of bounded endogenous metric-interaction semantic signatures under admissible isomorphisms and sensitivity to target-relevant mutations; includes finite cognitive-order invariance.
4. **EXP-GOVERNANCE-OPTION-MONOTONICITY-V16** — verifies the participantwise regret bound in common worlds and exhibits aggregate and residual-open counter-regimes.
5. **EXP-GF-BRANCH-HAZARD-ROBUST-V16** — executes finite analytic/Monte Carlo branch and hazard tests, including held-out generator discrimination and adversarial counter-regimes.
6. **EXP-CST-COMPUTATIONAL-GEOMETRY-V16** — tests transport, holonomy, metric, and consequence-closure invariance/sensitivity on finite typed graph worlds.

These are synthetic or finite-model experiments. They do not establish external physical, historical, AI-system, or civilizational instantiation.

## Rebuild

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./run_all.sh
python verify_package.py
```

`run_all.sh` creates a fresh `rebuild/` directory and does not overwrite the frozen executed results. A full run includes the original v8 generator and may take several minutes. The root requirements reproduce the execution environment used here; the original v8 requirement file is also preserved under `original_inputs/`. The verifier checks the archive manifest and compares canonical fingerprints from the fresh rebuild to the frozen result fingerprints.
