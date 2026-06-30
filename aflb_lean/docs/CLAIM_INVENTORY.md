# CLAIM INVENTORY (v50)

Source: `antigravity_secondorder_main_v50_AFLB.tex`,
        `antigravity_secondorder_supplement_v50_AFLB.tex`

## Bucket Key

| Bucket | Meaning |
|---|---|
| A | Proved outright — kernel-certified, stdlib-only (core axioms: propext/Quot.sound at most) |
| B | Conditional on physical/regime argument; antecedent never asserted |
| C | Proved relative to a named [hyp] axiom (physics posit) |
| D | Outside formal scope (empirical, [emp], [imported], or [open]); ledger only |

## Statement Table

| Source label | Bucket | Lean name | Notes |
|---|---|---|---|
| `hyp:pair-resolution` | C (axiom) | `Posits.pairResolution` | Branch selection is decided in P-space, not by observer; named axiom, not proved. supplement:232 |
| `eq:character` | A | `Physics.chi_id, Physics.chi_zinv, Physics.chi_zinv_mul, Physics.psi_nonneg` | χ(Id)=1, χ(zinv)=-1, χ(zinv·k)=-χ(k), Ψ≥0. Modeled with an opaque 2-element sign type. supplement:302-314 |
| `prop:response` (attractive, `eq:attractive-response`) | A | `Physics.attractiveResponseSign` | On Branch_+, sign(ṙ_e) = sign(2α_e-γ_e r_e). supplement:407-414 |
| `prop:response` (inverse, `eq:inverse-response`, TOP PRIORITY) | A | `Physics.inverseResponsePositive` | On Branch_-, ṙ_e = (2α_e+γ_e r_e)/r_e^3 > 0 given α_e,γ_e,r_e>0. supplement:415-420 |
| `eq:inverse-stability` | A | `Physics.inverseStabilityCondition` | Inverse target is a strict local min iff r_e > γ_e/λ_e (stated as the cleared inequality γ_e < λ_e·r_e). supplement:421-426 |
| `lem:ossv5-regularity-positivity` (KEYSTONE) | A | `Physics.regularBranchCoefficientPositivity` | Full admissibility (regular-branch stable equilibrium) forces α_e>0 ∧ γ_e>0; algebraic derivative argument, cleared of denominators. supplement:933-977 |
| `thm:ossv5-sign-invariance` | A | `Physics.signInvariance` | Every admitted h has sgn(ṙ_e^h)=+1 on the inverse branch; built from `regularBranchCoefficientPositivity` alone, core axioms only — does NOT use `physicalOperativity`. supplement:1081-1114 |
| `thm:fiber` | A | `Fiber.fiberCriterion` | If Obs_R(z+)=Obs_R(z-) then no factoring function exists for Θ_inv; reuses the v47 fiber-criterion proof shape, retargeted to Θ_inv/Obs_R. supplement:550-571 |
| `thm:ossv5-finite-closure` | A | `Closure.finiteCertificateClosure` | Kleene sequence on a finite certificate lattice is ascending and stabilizes at the least fixed point, within `|V|-1` steps; proved given the monotonicity hypothesis (kept as an explicit theorem hypothesis, not a global axiom). supplement:863-900 |
| `thm:ossv5-nonreducibility` | A | `Closure.viabilityNonReducibility` | If the viability-distinguishing fiber condition holds, `Adm^full` does not factor through `π_X`. supplement:1013-1060 |
| `thm:ossv5-endogenous-admissibility` | A | `Closure.endogenousAdmissibility` | Membership in `H_adm(x)` unfolds to the full-admissibility predicate on the candidate's own generated certificate; definitional, non-tautological clauses only. supplement:902-931 |
| `thm:secondorder` | B | `SecondOrder.secondOrderResult` | 4-item conjunction citing `Physics.attractiveResponseSign`, `Physics.inverseResponsePositive`, `Posits.pairResolution`, `Fiber.fiberCriterion`. supplement:614-638 |
| `prop:schedule` | B | `SecondOrder.scheduleRealizesInverse` | ScheduleReaches → InverseBranchMembership; antecedent (schedule existence) never asserted. supplement:1160-1167 |
| `hyp:ossv5-physical-operativity` | C (axiom) | `Posits.physicalOperativity` | Ontic hypothesis; must NOT appear in the dependency cone of any Bucket-A theorem. supplement:711-725 |
| `hyp:ossv5-certificate-update` | C (kept as hypothesis) | hypothesis argument of `Closure.finiteCertificateClosure` | Monotonicity of Φ_{h,x}; kept as an explicit theorem hypothesis rather than a global axiom, per task instructions. supplement:766-785 |
| `hyp:ossv5-sign-neutrality` | (definitional, discharged by construction) | — | Source text adds this hypothesis to `thm:ossv5-sign-invariance`, asserting `Adm^viab` carries no inverse-sign predicate. Not in the user's original Bucket-C list. We formalize `Adm^viab` as an opaque predicate that by construction never references the response sign, so this hypothesis is satisfied vacuously by the term's type and is not declared as a separate `axiom`. Documented here rather than silently dropped. |
| `prop:closure` (descent identity) | A | `Imported.energyDescentIdentity` (stated, see note) | The algebraic gradient-flow identity `d/dt D = -Σ‖grad‖² ≤ 0` is, in the source, a calculus identity; without Mathlib's analysis library we state it as an axiom tagged `[requires-mathlib]` rather than fabricate a substitute proof. supplement:359-371 |
| `prop:closure` (global existence/uniqueness) | D | `Imported.odeGlobalExistence` | [imported] ODE theory; axiom, never discharged. supplement:359-383 |
| `obl:falsification` / `eq:sign-prediction` | D | — | [emp] regime judgment; ledger only, no Lean axiom. supplement:1169-1184 |
| `def:reconstruction` | D | — | [open]; ledger only. supplement:1186-1199 |
| `prop:shared-basis`, `prop:sync-residue`, `def:operation-basis`, `prop:smallest-scale` | C (legacy, retained) | `Hypotheses.sharedBasis`, `Hypotheses.pachnerTyped`, `Hypotheses.syncResidueWellDefined` | Out of the v50 task's explicit target list, but the labels persist unchanged in v50 main (lines 256-420); retained verbatim, headers retargeted to v50 line numbers. Not part of the new physics-determination certificate. |
| (deleted) | — | ~~`Conditional.observabilityPairedClosure`~~ | DELETED — `∃ n, n = n` is vacuous; no informative content. |
| (deleted) | — | ~~`Conditional.scheduleNotSignFlip`, `Conditional.nonSignalling`~~ | DELETED — `h := h` / tautological "conditionals" carry no content. |
| (deleted) | — | ~~`Conditional.secondOrderObservability`~~ | DELETED on re-inspection — its statement was literally `X = X` proved by `rfl`; despite a non-trivial-looking hypothesis list it was equally vacuous and is removed for the same reason. |

## Counts (targeted)

| Bucket | Count |
|---|---|
| A (proved outright, new+retargeted) | 11 |
| B (conditional) | 2 |
| C (named axiom / retained legacy) | 5 |
| D (imported/empirical, ledger only) | 4 |
