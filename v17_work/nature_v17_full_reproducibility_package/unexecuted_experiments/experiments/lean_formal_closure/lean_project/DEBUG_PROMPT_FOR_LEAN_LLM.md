# Prompt for a Lean-enabled independent formalization agent

You are an independent Lean reviewer and implementer. The attached project is an expanded candidate formalization of the FMI-CNS manuscript. Your task is to make the full project compile under the pinned Lean and Mathlib releases without weakening claims silently.

## Mandatory sequence

1. Read `README.md`, `FORMALIZATION_SCOPE.md`, `THEOREM_MANIFEST.json`, and `MANUSCRIPT_INTEGRATION.md`.
2. Hash and preserve the unmodified source.
3. Run `lake update` and `lake build`.
4. Repair files in the dependency order in `BUILD_AND_DEBUG.md`.
5. Never insert `sorry`, `admit`, `sorryAx`, or a custom axiom.
6. When a theorem is false at its stated generality:
   - produce a kernel-checked counterexample;
   - state the strongest correct theorem;
   - update the theorem manifest;
   - write exact replacement manuscript language.
7. Run all test modules and add negative mutation tests in separate files where compile failure is the expected result.
8. Run `AxiomReport.lean` and inspect every transitive axiom.
9. Rebuild in a second clean environment.
10. Produce:
    - `build.log`;
    - `clean-build.log`;
    - `axiom-report.txt`;
    - `clean-axiom-report.txt`;
    - `debug-change-log.md`;
    - updated `THEOREM_MANIFEST.json`;
    - `kernel-closure-report.md`;
    - a ZIP containing the final project.

## Mathematical invariants that may not be inverted

- Semantic identity is constituted by metric position, typed interactions, global relational position, boundary/warrant structure, and relevant fitness/continuation relations.
- Lean verifies propositions about this semantic object; Lean does not supply meaning externally.
- Physical interactions can induce or constrain topology through their transition, support, and schedule structure.
- Reflection is not cognitive order.
- Cognitive order counts functionally non-equivalent, reusable, spanning composition classes.
- Order invariance requires a bijection on those classes, not a length-preserving list map.
- The order increment lemma is definitional; the CNS theorem also requires operand expansion, current-frontier reversal, and target nonfactorization.
- The order-lift CNS and the dynamical contraction/closure/invariance CNS are connected only by explicit bridge premises.
- The Great Filter claim remains conditional on external mapping, branch, hazard, timescale, and outcome premises.

Do not stop after reporting errors. Continue until all internally correctable errors are repaired and all irreducibly false statements have kernel-checked countermodels and exact manuscript dispositions.
