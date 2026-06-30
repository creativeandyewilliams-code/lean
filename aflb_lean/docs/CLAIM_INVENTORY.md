# CLAIM INVENTORY (v51)

Source: `antigravity_secondorder_main_v50_AFLB.tex`,
`antigravity_secondorder_supplement_v50_AFLB.tex` (manuscript unchanged
from v50; this is a revision of the Lean package only).

## Bucket key

| Bucket | Meaning |
|---|---|
| A | Proved outright — kernel-certified, stdlib-only (core axioms: `propext`/`Quot.sound`/`Classical.choice` at most, never a named physics posit) |
| B | Conditional on a physical/regime hypothesis; antecedent never asserted |
| C | A named physics posit ([hyp]), now carried as an explicit `Prop` hypothesis parameter rather than a global axiom (see `Posits.lean`) |
| Legacy | Retained registration-theory layer (`AflbLean/Legacy/`), not part of the headline build/audit |
| D | Outside formal scope (empirical/[emp], [imported], or [open]); ledger only |
| — | Removed; no honest non-vacuous Lean content found (documented, not silently dropped) |

Headline kernel-checked theorems are exactly the Bucket-A rows below. None
is a definitional unfolding wrapper, conjunction restatement, or
placeholder.

## Statement table

| Source label | Bucket | Lean declaration | Formal statement (informal) | Assumptions | Axiom-audit result | Source |
|---|---|---|---|---|---|---|
| `eq:character` | A | `Physics.chi_id`, `Physics.chi_zinv`, `Physics.chi_zinv_mul` | χ(Id)=1, χ(zinv)=-1, χ(zinv·k)=-χ(k) on the 2-element sign carrier `Chi := Int` | none | core axioms only | supplement:302-314 |
| `prop:response` (`eq:attractive-response`) | A | `Physics.attractiveResponseSign` | On Branch₊: `2α-γr<0` for `r>r*`; `2α-γr>0` for `0<r<r*`, given `γ>0`, `γr*=2α` | `γ>0`, equilibrium identity | `propext, Quot.sound` | supplement:407-414 |
| `prop:response` (`eq:inverse-response`) | A | `Physics.inverseResponsePositive` | `2α+γr>0` given `α>0, γ>0, r>0` (denominator-cleared `ṙ_e=(2α_e+γ_e r_e)/r_e³>0`) | `α>0, γ>0, r>0` | `propext, Quot.sound` | supplement:415-420 |
| `lem:ossv5-regularity-positivity` (KEYSTONE) | A | `Physics.regularBranchCoefficientPositivity` | Regular-branch equilibrium witness (`r*>0`, `γr*=2α`, cleared derivative `-6α+2γr*<0`) forces `α>0 ∧ γ>0` | the three witness conditions | `propext, Quot.sound` | supplement:933-977 |
| `hyp:ossv5-sign-neutrality` | A | `Physics.viableAdm_sign_invariant` | `ViableAdm` (the regularity witness predicate) is invariant under changing a candidate's independent `sgn` annotation while `(alpha,gamma,rstar)` are unchanged — proved semantically via the predicate's type, not asserted by comment | candidates agree on `alpha,gamma,rstar` | `propext` | supplement:1062-1079 |
| `thm:ossv5-sign-invariance` | A | `Physics.signInvariance` | `∀ c, Admissible c → ∀ r>0, 2·c.alpha+c.gamma·r>0`, where `Admissible` is the typed surviving class (`ViableAdm` on `nonSignData c`); positivity is *derived* from class membership via the KEYSTONE, not assumed as a raw premise | `Admissible c`, `r>0` | `propext, Quot.sound` | supplement:1081-1114 |
| `thm:fiber` | A | `Fiber.fiberCriterion` | If `Obs_R(z+)=Obs_R(z-)` and `Theta_inv` differs on `z+,z-`, no `Θbar` factors `Theta_inv` through `Obs_R` | co-registration + differing target values | none | supplement:550-571 |
| `hyp:pair-resolution` (mechanism only) | A | `Posits.classify_covers`, `Posits.classify_exclusive` | The threshold classifier `classify(τ,θ)` always returns exactly one of `Branch.plus`/`Branch.minus` (coverage + exclusivity, proved by case analysis) | none | `propext` (exclusivity); none (coverage) | supplement:231 — mechanism only; see Bucket-C row below for the unproved "this rule is physically intrinsic" claim |
| `thm:ossv5-finite-closure` (ascending half) | A | `Closure.ascendingKleeneSeq` | Kleene sequence `φ^(n)` is `≤`-ascending under monotone `Φ` | `Φ` monotone (explicit hypothesis) | none | supplement:863-900 |
| `thm:ossv5-finite-closure` (complete) | A | `Closure.finiteCertificateClosureComplete` | Given a concrete `rank`-based finite witness bounded by `N`, the Kleene sequence stabilizes at some `n≤N` at a value `ψ` with `Φψ=ψ`, and `ψ ≤` every fixed point `≥ bot` | `FiniteWitness` (rank monotone/strict/bounded), `Φ` monotone | `propext, Classical.choice, Quot.sound` | supplement:863-900 |
| `thm:ossv5-nonreducibility` | A | `Closure.viabilityNonReducibility` | If `AdmFull x` distinguishes two certificates, it does not factor through a fitness-erasing projection onto `x` alone | `AdmFull x φ0 ≠ AdmFull x φ1` | `propext` | supplement:1013-1060 |
| `thm:secondorder` | B | `SecondOrder.secondOrderResult` | 4-item conjunction citing the attractive/inverse response shapes, `pairRes`, `physOp` (bare `Prop` hypothesis parameters), and the fiber non-factorization fact | `pairRes`, `physOp`, response/equilibrium hypotheses, co-registration | `propext, Quot.sound` (no dependency on `pairRes`/`physOp` as axioms — they are hypothesis parameters, visible in the signature) | supplement:614-638 |
| `hyp:pair-resolution` (intrinsicity claim) | C | none declared (see `Posits.lean`) | "This threshold rule is the physically intrinsic one, not detector-dependent" | n/a | supplied as a `Prop` argument to `secondOrderResult`; never asserted true by an axiom | supplement:231 |
| `hyp:ossv5-physical-operativity` | C | none declared (see `Posits.lean`) | A candidate is physically consequential only if admitted on its own closed operand | n/a | supplied as a `Prop` argument to `secondOrderResult`; never asserted true by an axiom; confirmed absent from every Bucket-A cone in `docs/axioms.txt` | supplement:711-725 |
| `hyp:ossv5-certificate-update` | A (kept as hypothesis) | `mono` field of `Closure.CertificateUpdate` | Monotonicity of `Φ` | explicit theorem hypothesis, not a global axiom | n/a | supplement:766-785 |
| `thm:ossv5-endogenous-admissibility` | — (removed) | — | v50's `Closure.endogenousAdmissibility` proved `P ↔ P` via `Iff.rfl` — vacuous. No non-vacuous, non-Mathlib-dependent Lean content found; removed rather than retained as a fake result. | — | — | supplement:902-931 |
| `prop:schedule` | — (removed) | — | v50's `SecondOrder.ScheduleReaches`/`InverseBranchMembership`/`scheduleRealizesInverse` were effectively `True`, proved by `trivial`. No non-vacuous stdlib-only formalization found; removed rather than retained as a fake result. See `FORMALIZATION_SCOPE.md`. | — | — | supplement:1140-1167 |
| `prop:closure` (descent identity, global existence) | D | `Legacy.Imported.energyDescentIdentity`, `Legacy.Imported.odeGlobalExistence` | Gradient-flow analytic claims; axioms, ledger only, used by no theorem in this package | — | self-referential only | supplement:359-383 |
| `obl:falsification`, `def:reconstruction` | D | — | [emp]/[open]; ledger only, no Lean declaration | — | — | supplement:1169-1199 |
| `prop:shared-basis`, `prop:sync-residue`, `def:operation-basis`, `prop:smallest-scale` | Legacy | `Legacy.Hypotheses.sharedBasis`, `.pachnerTyped`, `.syncResidueWellDefined`, `Legacy.Conditional.*` | Registration-theory layer, retained unchanged from v50/v47, moved out of the headline root import | — | self-referential axioms | main:256-420 |

## Counts (headline build only)

| Bucket | Count |
|---|---|
| A (kernel-checked, headline) | 10 distinct claims |
| B (conditional) | 1 (`secondOrderResult`) |
| C (hypothesis parameters, no global axiom) | 2 (`pairRes`, `physOp`) |
| Removed (no honest non-vacuous content) | 2 (`thm:ossv5-endogenous-admissibility`, `prop:schedule`) |
| Legacy (non-headline) | 3 named axioms + 2 conditional theorems |
| D (ledger only) | 2 named axioms + 2 unformalized claims |

## Non-vacuity audit

Every Bucket-A row above has a conclusion that is not a syntactic
tautology of its own hypotheses:

- `chi_id`, `chi_zinv`: `rfl` on a `def`-level equation — labeled
  definitional, not advertised as a substantive inference; included only
  because the source treats them as named facts.
- `chi_zinv_mul`, `attractiveResponseSign`, `inverseResponsePositive`,
  `regularBranchCoefficientPositivity`, `signInvariance`: each conclusion
  is a numeric inequality/conjunction not implied by its hypotheses by
  unfolding alone; each requires the `omega`/`Int.mul_*` arithmetic steps
  shown in `Physics.lean`.
- `viableAdm_sign_invariant`: the conclusion is an `Iff` between two
  applications of `ViableAdm` to *different* arguments
  (`nonSignData c1`, `nonSignData c2`); proved via equality of those
  arguments, not reflexivity of the predicate on one fixed argument.
- `fiberCriterion`: proved by deriving `false = true` from the factoring
  hypothesis — a genuine contradiction extraction, not unfolding.
- `classify_covers`, `classify_exclusive`: require case-splitting on the
  defining `if`; not provable by `rfl` on the bare statement.
- `ascendingKleeneSeq`, `finiteCertificateClosureComplete`,
  `viabilityNonReducibility`: each is proved by induction or by
  contradiction-from-injectivity; none unfolds to its own hypothesis.
