# Known debugging risks

The source was written against common Lean 4/Mathlib idioms but was not elaborated in the generating environment. The most likely repair locations are:

- induction hypotheses for higher-order `Formula.existsNode` / `forallNode` constructors;
- exact names or simp behavior for `Finset.all_eq_true`, `Finset.card_insert_of_not_mem`, and `Relation.ReflTransGen.single`;
- arithmetic normalization in `queueRecurrence`;
- list product and sum simplification in the finite hazard theorem;
- `gcongr` discharge of nonnegativity in `regenerativeThreshold`;
- the concrete `Bool` metric triangle example.

These are expected API/elaboration repairs, not invitations to weaken the statements. Any required mathematical change must be recorded under the theorem-strength rule in `BUILD_AND_DEBUG.md`.
