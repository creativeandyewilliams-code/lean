# Lean closure and independent-build execution

1. Run `./preflight_test.sh`.
2. Create two clean worktrees or containers, `builder_1` and `builder_2`, with no shared `.lake` cache unless the exact cache hash is recorded.
3. In each environment run:

```bash
./run_lean_experiment.sh run_builder_1
./run_lean_experiment.sh run_builder_2
```

4. Repair source only in a separate repair branch. For every repair, record the failing declaration, compiler message, exact diff, and why the theorem statement was not weakened. Re-freeze hashes before final builds.
5. Compare the two build outputs and source hashes. Environment-specific compiled-object hashes may differ; source, declaration inventory, axiom report, and theorem status must agree.
6. Run `#print axioms` for every declaration in `THEOREM_MANIFEST.json`. Extend `AxiomReport.lean` if any are absent.
7. No release theorem may depend on `sorryAx` or an unregistered custom axiom. Imported foundational axioms must be reported exactly rather than hidden.
8. Return the complete build directories, repaired source tree, statement-impact audit, and final status per theorem target.

A build of only a bounded subtheorem must not be reported as closure of the corresponding stronger manuscript theorem.
