/-
Formalizes the physics-determination layer: forced branch responses,
the coefficient-positivity keystone, and sign invariance.
Source: antigravity_secondorder_supplement_v50_AFLB.tex, §"One energy, two
gravitational response branches" and §"Operand self-selection" (sec:operand-self-selection-v5).
Bucket: A (proved outright; core axioms only — no physics posit is used).

Real-valued quantities (α_e, γ_e, λ_e, r_e) are modeled with `Int` because
this stdlib-only build has no Mathlib (no `Real`/`Rat`/ordered-field
tactics available; verified empirically). All inequalities below are the
denominator-cleared forms of the source equations: since every concrete
r_e, r_e^3, r_e^4 appearing as a denominator in the source is strictly
positive, clearing it does not change any sign conclusion. This is recorded
as a downgrade in BUILD_REPORT.md.
-/

import AflbLean.Posits

namespace AflbLean.Physics

/-- Character χ as a {+1,-1}-valued sign, per `eq:character`. -/
abbrev Chi := Int

def chiId : Chi := 1
def chiZinv : Chi := -1

/-- χ(Id) = 1. Source eq:character (line 310). -/
theorem chi_id : chiId = 1 := rfl

/-- χ(zinv) = -1. Source eq:character (line 310). -/
theorem chi_zinv : chiZinv = -1 := rfl

/-- χ(zinv·k) = -χ(k), for the two-element {Id,zinv} carrier. Source eq:character. -/
theorem chi_zinv_mul (k : Chi) (hk : k = chiId ∨ k = chiZinv) :
    (if k = chiId then chiZinv else chiId) = -k := by
  rcases hk with hk | hk <;> simp [hk, chiId, chiZinv]

/--
**Forced attractive response (`eq:attractive-response`).**
On the attractive branch, the cleared numerator `2α_e - γ_e r_e` changes sign
exactly at the equilibrium `r_e* = 2α_e/γ_e` (encoded via `γ_e·r_e* = 2α_e`
to avoid division): negative for `r_e > r_e*`, positive for `0 < r_e < r_e*`.
Source: supplement prop:response, eq:attractive-response (lines 407-414).
-/
theorem attractiveResponseSign (α γ r rstar : Int) (hγ : γ > 0)
    (heq : γ * rstar = 2 * α) :
    (r > rstar → 2 * α - γ * r < 0) ∧ (0 < r → r < rstar → 2 * α - γ * r > 0) := by
  constructor
  · intro hr
    have h1 : 2 * α - γ * r = γ * (rstar - r) := by
      rw [Int.mul_sub, heq]
    rw [h1]
    have : rstar - r < 0 := by omega
    exact Int.mul_neg_of_pos_of_neg hγ this
  · intro _ hr
    have h1 : 2 * α - γ * r = γ * (rstar - r) := by
      rw [Int.mul_sub, heq]
    rw [h1]
    have : rstar - r > 0 := by omega
    exact Int.mul_pos hγ this

/--
**Forced inverse response, positivity (`eq:inverse-response`, TOP PRIORITY).**
On the inverse branch, the cleared numerator `2α_e + γ_e r_e` is strictly
positive whenever the carrier coefficients and separation are positive.
Source: supplement prop:response, eq:inverse-response (lines 415-420).
-/
theorem inverseResponsePositive (α γ r : Int) (hα : α > 0) (hγ : γ > 0) (hr : r > 0) :
    2 * α + γ * r > 0 := by
  have h1 : 2 * α > 0 := by omega
  have h2 : γ * r > 0 := Int.mul_pos hγ hr
  omega

/--
**Inverse local-energy strict-minimum condition (`eq:inverse-stability`),
denominator-cleared.** The inverse mismatch target is a strict local minimum
exactly when `λ_e · r_e > γ_e`.
Source: supplement eq:inverse-stability (line 425).
-/
def inverseStable (γ lam r : Int) : Prop := lam * r > γ

/--
**Regular-branch admissibility forces coefficient positivity (KEYSTONE,
`lem:ossv5-regularity-positivity`).**
Hypotheses are the denominator-cleared forms of the source's two conditions
on the regular-branch equilibrium r*: `f(r*) = 0` becomes `γ·r* = 2α`, and
`f'(r*) < 0` becomes `-6α + 2γr* < 0` (multiplying by `r*^4 > 0` preserves
sign). The proof is the same algebraic substitution as the source proof.
Source: supplement lem:ossv5-regularity-positivity (lines 933-977).
-/
theorem regularBranchCoefficientPositivity (α γ rstar : Int)
    (hrstar : rstar > 0) (heq : γ * rstar = 2 * α)
    (hderiv : -6 * α + 2 * (γ * rstar) < 0) :
    α > 0 ∧ γ > 0 := by
  have hα : α > 0 := by
    rw [heq] at hderiv
    omega
  have hγ : γ > 0 := by
    by_cases hpos : 0 < γ
    · exact hpos
    · have hle : γ ≤ 0 := Int.not_lt.mp hpos
      have : γ * rstar ≤ 0 := Int.mul_nonpos_of_nonpos_of_nonneg hle (Int.le_of_lt hrstar)
      omega
  exact ⟨hα, hγ⟩

/--
**Sign invariance over the surviving functional class (`thm:ossv5-sign-invariance`).**
Every admitted candidate (i.e. one satisfying the regular-branch
coefficient-positivity conclusion) has positive inverse-branch response.
This theorem is built only from `regularBranchCoefficientPositivity` and
elementary arithmetic: it does **not** take `Posits.physicalOperativity` as
a hypothesis and does not use it. `Hypothesis hyp:ossv5-sign-neutrality` is
discharged by construction: the hypotheses below never reference a response
sign, so no extra axiom for sign-blindness is declared.
Source: supplement thm:ossv5-sign-invariance (lines 1081-1114).
-/
theorem signInvariance (α γ rstar r : Int)
    (hrstar : rstar > 0) (heq : γ * rstar = 2 * α)
    (hderiv : -6 * α + 2 * (γ * rstar) < 0) (hr : r > 0) :
    2 * α + γ * r > 0 := by
  obtain ⟨hα, hγ⟩ := regularBranchCoefficientPositivity α γ rstar hrstar heq hderiv
  exact inverseResponsePositive α γ r hα hγ hr

end AflbLean.Physics
