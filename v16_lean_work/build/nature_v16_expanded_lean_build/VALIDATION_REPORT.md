# Validation report — nature_v16_expanded_lean

Independent validation performed by a second LLM (Claude) on the candidate
package. **No Lean source statement was modified or weakened.** All checks below
are static/structural — a kernel build could not be run here (see
`BUILD_CERTIFICATE.txt` and `egress_block_evidence.txt`).

## 1. Integrity
- Input zip SHA-256 `75c3c704679aa6d17b0920759e5164cdef813df74745fe3b7be900615bb89121`.
- `sha256sum -c MANIFEST.sha256`: **all files OK** (exit 0).

## 2. Static audit (independently reproduced)
| Metric | Claimed | Reproduced |
|---|---|---|
| Lean source files | 32 | 32 |
| `sorry` | 0 | 0 |
| `sorryAx` | 0 | 0 |
| `admit` | 0 | 0 |
| custom `axiom` declarations | 0 | 0 |
| registered targets | 33 | 33 |

## 3. Theorem-manifest coverage
- All **33 registered targets** in `THEOREM_MANIFEST.json` resolve to a
  `theorem`/`lemma`/`def`/`structure` declaration **present in the named file**
  (the two compound entries — `collapsedPairLoss / collapsedPairWeightedLoss`
  and `boundedResidual / queueReversalStep` — both resolve; verified in
  `Fragmentation/SemanticLoss.lean` and `Fragmentation/Backlog.lean`).
- Both top-level theorems present: `formalFmiCnsCoherence`
  (`TopLevel/FormalCoherence.lean`) and `formalConditionalGreatFilter`
  (`TopLevel/ConditionalFilter.lean`).
- 67 `theorem`/`lemma` declarations across the project.

## 4. Import closure and dependency pins
- Intra-project imports: **0 unresolved** (every non-Mathlib import resolves to
  a file in the package).
- External dependency: a single `import Mathlib`.
- **Toolchain/Mathlib pins are mutually consistent**: the package pins
  `leanprover/lean4:v4.32.0`, and mathlib4's own `lean-toolchain` at tag
  `v4.32.0` is **exactly** `leanprover/lean4:v4.32.0`.
- Mathlib `v4.32.0` resolves to commit
  `81a5d257c8e410db227a6665ed08f64fea08e997`; a fully pinned
  `lake-manifest.json` (Mathlib + its 8 transitive dependencies at exact
  commits, mirrored from mathlib4's manifest) is included for deterministic
  resolution. See `PINNED_DEPENDENCIES.json`.

## 5. Source-quality review (spot check of substantive theorems)
The proofs use genuine Lean 4 / Mathlib idioms and standard arguments; they are
plausibly correct and are not skeletons:
- `Fragmentation/Backlog.lean` — `queueStep`/`queueGrowth`/`queueRecurrence`
  with real induction, `linarith`, `push_cast`, `le_max_right`, `max_le_max`.
- `Governance/Options.lean` — the `2ε+δ` bound via `abs_le.mp` + `linarith`.
- `CNS/Dynamic.lean` — contraction ⇒ unique fixed point (`κ<1`, `d≥0` ⟹ `d=0`).
- `Order/Span.lean` — decidable finite span via `Finset.all_eq_true` + `inferInstance`.
- `Core/Semantics.lean` — an inductive registered-formula language with
  higher-order quantifier constructors, `eval`, `map`, and `eval_map_iff` by
  structural induction (T-SEM-EQUIV).
- `TopLevel/FormalCoherence.lean` — a typed conclusion bundling semantic
  invariance with the substantive CNS-lift output (not a Boolean label).

## 6. Concurred elaboration-risk areas (from `KNOWN_DEBUG_RISKS.md`)
I independently concur these are the most likely repair sites (API/elaboration,
not statement weakening):
- higher-order `Formula.existsNode`/`forallNode` induction cases in
  `Core/Semantics.lean` (the `Equiv.symm_apply_apply` simp steps under `simpa`);
- exact names/simp behaviour for `Finset.all_eq_true`,
  `Finset.card_insert_of_not_mem`, `Relation.ReflTransGen.single`;
- arithmetic normalization in `queueRecurrence` (`simpa [Nat.add_assoc]`);
- list product/sum simplification in the finite hazard theorem;
- `gcongr` nonnegativity discharge in `regenerativeThreshold`;
- the concrete `Bool` metric triangle example.

## Verdict
The package is **static-validated and internally consistent**: audit reproduced,
manifest verified, all 33 targets declared, imports closed, pins mutually
consistent and fully resolved. It is **build-ready** but **not kernel-checked
here** — the Lean toolchain binary is blocked by the environment's egress policy.
