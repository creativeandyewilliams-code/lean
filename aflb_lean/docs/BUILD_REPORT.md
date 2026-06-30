# BUILD REPORT (v51)

## Toolchain

| Item | Value |
|---|---|
| Lean version | 4.14.0 (x86_64-unknown-linux-gnu, commit 410fab728470, Release) |
| Lake version | 5.0.0-410fab7 (Lean version 4.14.0) |
| Mathlib | **Not used.** Stdlib-only build. Re-verified at the start of v51: `git ls-remote https://github.com/leanprover-community/mathlib4` → HTTP 403; `release.lean-lang.org` → HTTP 403 (proxy scoped only to the four `creativeandyewilliams-code` repos). This matches the v50/v47 finding and is unchanged. |
| `lake-manifest.json` | Zero pinned packages (unchanged). |

## Build

Run via `bash scripts/rebuild.sh` from the package root (auto-`cd`s, so it
can be invoked from anywhere). Six steps, all required to pass:

1. Toolchain check (`lake --version`, `lean --version`).
2. `lake build AflbLean 2>&1 | tee docs/build.log` — explicit headline
   target (bare `lake build` silently no-ops in this project: no default
   target is configured).
3. `bash scripts/check_no_sorry.sh`.
4. `bash scripts/check_no_placeholders.sh`.
5. Regenerate `docs/axioms.txt` via `lake env lean scripts/PrintAxioms.lean`.
6. Headline-axiom-only verification: every one of the 10 Bucket-A
   declarations must show only core axioms (`propext`/`Quot.sound`/
   `Classical.choice`) in `docs/axioms.txt` — mechanically checked by
   grepping for any `AflbLean.(Posits|Physics|Closure|Fiber|SecondOrder|Legacy)`-
   prefixed dependency.

**Result of the captured run: `=== FINAL RESULT: PASS ===`** (all 6 steps
passed). See `docs/build.log` and `docs/axioms.txt` for the full captured
output of this run.

## §5 audit table — required facts

| Fact | Status |
|---|---|
| (1) All 10 Bucket-A theorems depend on core axioms only | **Confirmed.** Per `docs/axioms.txt`: every one of `inverseBranchResponsePositive`, `regularBranchCoefficientPositivity`, `viableAdmSignInvariant`, `signInvariance`, `fiberCriterion`, `classifyCovers`, `classifyExclusive`, `finiteCertificateClosureAscending`, `finiteCertificateClosureComplete`, `viabilityNonReducibility` shows only a subset of `{propext, Quot.sound, Classical.choice}` or no axioms at all. |
| (2) No headline theorem depends on a named physics posit | **Confirmed, and stronger than v50.** v51 declares *no* global `pairResolution`/`physicalOperativity` axioms at all (removed; see `AXIOM_LEDGER.md`). The corresponding hypotheses are bare `Prop` parameters of `secondOrderResult` only, so they cannot appear in any axiom cone by construction. |
| `pairRes`/`physOp` used only where `thm:secondorder` is claimed | **Confirmed.** They are parameters of `AflbLean.secondOrderResult` only; `#print axioms AflbLean.secondOrderResult` shows `[propext, Quot.sound]`, with the hypothesis-dependency visible solely in the theorem's type signature, not its axiom cone. |

Full posit-to-theorem map: see `docs/AXIOM_LEDGER.md`.

## Changes relative to v50 (resolves all nine flagged weaknesses)

1. **Full finite-stabilization theorem.** `Closure.finiteCertificateClosureComplete`
   now proves the complete result (not just the ascending-chain half): given
   a concrete `FiniteWitness` (a hand-rolled, stdlib-only `rank`-based
   structure with `rank_bot`/`rank_mono`/`rank_strict`/`rank_bound` fields,
   substituting for Mathlib's `Fintype`/`PartialOrder`/`OrderBot`/`Monotone`
   machinery, which remains unavailable — see "Downgrade log" below), the
   Kleene sequence stabilizes at some `n ≤ N` at a value `ψ` with `Φψ = ψ`,
   and `ψ` is below every fixed point `≥ bot`. Proved via a genuine
   pigeonhole/rank-growth argument (`rank_ge_of_no_stab`) plus
   `Classical.byContradiction` (the core-Lean substitute for the
   Mathlib-only `by_contra` tactic), not assumed.
2. **`thm:ossv5-endogenous-admissibility` removed.** v50's version proved
   `P ↔ P` via `Iff.rfl` — vacuous. No honest non-vacuous, stdlib-only
   Lean content was found for this claim; it is removed and documented
   (not silently dropped) in `CLAIM_INVENTORY.md` and `FORMALIZATION_SCOPE.md`.
3. **Sign-blind admissibility, formalized semantically.** `Physics.lean` now
   separates `Candidate` (has a `sgn : Bool` field) from `NonSignData` (has
   no `sgn` field by construction) and defines `ViableAdm` only on
   `NonSignData`. `viableAdm_sign_invariant` is a genuine `Iff` between
   `ViableAdm` applied to two different `NonSignData` projections, proved
   via equality of the projected arguments — sign-blindness is a structural,
   type-level guarantee, not a comment.
4. **Sign invariance over the actual typed admissible class.**
   `Physics.signInvariance` is now stated over `Admissible c` (defined as
   `ViableAdm (nonSignData c)`) rather than three raw `Int` premises; its
   positivity conclusion is *derived* by destructuring `Admissible c` and
   feeding the result through `regularBranchCoefficientPositivity` (the
   KEYSTONE) — not assumed as a hypothesis.
5. **`prop:schedule` trivial formalization removed.** v50's
   `ScheduleReaches`/`InverseBranchMembership`/`scheduleRealizesInverse` were
   effectively `True`, proved by `trivial`. No non-vacuous stdlib-only
   formalization was found; removed and documented in
   `FORMALIZATION_SCOPE.md`.
6. **`Posits.lean` refactored away from the axiom-for-inhabitant pattern.**
   The global `pairResolution`/`physicalOperativity` axioms are deleted.
   The decidable mechanism (coverage + exclusivity of the threshold
   classifier) is now a proved theorem (`classify_covers`,
   `classify_exclusive`); the non-decidable "intrinsicity" claim and
   `physicalOperativity` are not declared in Lean at all and are instead
   passed as bare `Prop` parameters into `secondOrderResult`. See
   `AXIOM_LEDGER.md` for the full rationale.
7. **Root module scoped to the headline determination core.**
   `AflbLean.lean` now imports only `Posits`, `Physics`, `Closure`, `Fiber`,
   `SecondOrder`. The registration-theory layer (`Hypotheses.lean`,
   `Conditional.lean`) and the imported-analytic ledger (`Imported.lean`)
   are moved to `AflbLean/Legacy/` with namespaces renamed to
   `AflbLean.Legacy.*`; independently buildable, excluded from the headline
   root import and from the headline axiom-only check.
8. **`scripts/PrintAxioms.lean` updated** to print axioms for all 10
   Bucket-A declarations, `secondOrderResult`, and the five Legacy axioms
   under their new namespace.
9. **New build-integrity scripts.** `scripts/check_no_placeholders.sh`
   (fails on any `sorry`/`admit`; flags — without failing — any headline
   `axiom`/`opaque`/bare-`True`/bare-`rfl`/bare-`Iff.rfl`/bare-`trivial`
   declaration for manual review) and `scripts/rebuild.sh` (the single
   reproducible end-to-end driver described above) are new in v51.

## Downgrade log (relative to the literal v51 mathematics; carried forward
from v50 where unresolved, updated where resolved)

1. **No Mathlib ⇒ `Real`/`Rat` unavailable.** Unchanged from v50: all
   real-valued physics quantities (α_e, γ_e, λ_e, r_e) are modeled with
   `Int`, and every inequality involving a denominator is stated in its
   denominator-cleared form. Since every concrete denominator appearing in
   the source is provably positive, clearing it never changes a sign
   conclusion; this is a representational downgrade, not a mathematical
   shortcut.
2. **No Mathlib ⇒ `Fintype`/`PartialOrder`/`OrderBot`/`Monotone` unavailable
   for the finite-closure theorem.** Resolved in v51 relative to v50 (item 1
   above): a concrete, hand-rolled `FiniteWitness` structure with an
   explicit `rank : V → Nat` function substitutes for the abstract
   finite-cardinality argument, and the full stabilization-and-least-fixed-
   point result is proved without any Mathlib instance. This is a genuine
   substitute, not a restatement of the conclusion as a hypothesis: the
   `rank` function and its four governing properties (`rank_bot`,
   `rank_mono`, `rank_strict`, `rank_bound`) are exactly the data a
   `Fintype`+`PartialOrder` argument would extract internally; the caller
   must supply a concrete witness satisfying them.
3. **`by_contra`/`push_neg` tactics unavailable (Mathlib-only) — newly
   discovered in v51.** `Classical.byContradiction : (¬p → False) → p`
   (Lean 4 core, `Init/Classical.lean`) is used in its place via
   `apply Classical.byContradiction; intro hcon`, contributing the
   `Classical.choice` axiom to `finiteCertificateClosureComplete`'s cone
   (a standard core axiom, not a physics posit).
4. **`prop:closure` analytic content axiomatized, not proved.** Unchanged
   from v50. Both the gradient-flow global-existence/uniqueness claim and
   the algebraic descent identity require real analysis or a calculus of
   `deriv`/`HasDerivAt`, both supplied by Mathlib. Declared as
   `Legacy.Imported.odeGlobalExistence` ([imported]) and
   `Legacy.Imported.energyDescentIdentity` ([requires-mathlib]); neither is
   used by, nor a hypothesis of, any theorem reachable from the headline
   root.
5. **Legacy registration-layer module retained, not rebuilt.** Moved to
   `AflbLean/Legacy/` and renamespaced; content otherwise unchanged from
   v50/v47.

## Module map

| File | v51 content | Bucket |
|---|---|---|
| `Posits.lean` | `classify`/`classify_covers`/`classify_exclusive` (proved); intrinsicity + physical-operativity claims (undeclared, threaded as `Prop` params) | A (mechanism) / C (undeclared posits) |
| `Physics.lean` | character facts, attractive/inverse response, KEYSTONE coefficient positivity, structural sign-blind admissibility, sign invariance over the typed class | A |
| `Closure.lean` | ascending Kleene sequence, full finite-stabilization + least-fixed-point theorem, viability non-reducibility | A |
| `Fiber.lean` | fiber criterion for the inverse branch (`thm:fiber`) | A |
| `SecondOrder.lean` | `thm:secondorder` (conditional on `pairRes`/`physOp` parameters) | B |
| `Legacy/Imported.lean` | `odeGlobalExistence`, `energyDescentIdentity` | D (axiom, ledger only) |
| `Legacy/Hypotheses.lean`, `Legacy/Conditional.lean` | legacy registration layer (`prop:shared-basis`, `prop:sync-residue`) | C (non-headline) |
