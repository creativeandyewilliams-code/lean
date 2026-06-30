/-
Formalizes: thm:fiber (fiber criterion for the inverse branch).
Source: antigravity_secondorder_supplement_v50_AFLB.tex, §"Registration,
bridge, and the inverse target" (lines 550-571).
Bucket: A (proved outright; no axioms beyond the Lean kernel).

The argument is purely combinatorial: if a target function Θ_inv takes
different values on two states z+, z- that the observation map Obs_R cannot
distinguish, no factorization of Θ_inv through Obs_R can exist. This is the
same fiber-non-factorization shape as the v47 `NonReducibility.fiberCriterion`,
retargeted to the v50 inverse-branch target Θ_inv and observation map Obs_R.
-/

namespace AflbLean.Fiber

/--
**Fiber criterion for the inverse branch (`thm:fiber`).**
If there are states `z+ ∈ Branch_+` and `z- ∈ Branch_-` with
`Obs_R(z+) = Obs_R(z-)`, then no function `Θbar` factoring
`Theta_inv = Θbar ∘ Obs_R` exists. Consequently the material record available
through `Obs_R` cannot decide inverse-branch membership.
Source: supplement thm:fiber (lines 550-571).
-/
theorem fiberCriterion {State R : Type} (Obs_R : State → R) (Theta_inv : State → Bool)
    (z_plus z_minus : State)
    (hcoreg : Obs_R z_plus = Obs_R z_minus)
    (hplus : Theta_inv z_plus = false)
    (hminus : Theta_inv z_minus = true) :
    ∀ Θbar : R → Bool, ¬ (∀ z : State, Theta_inv z = Θbar (Obs_R z)) := by
  intro Θbar hfact
  have h1 := hfact z_plus
  have h2 := hfact z_minus
  rw [hcoreg, hplus] at h1
  rw [hminus] at h2
  exact absurd (h1.trans h2.symm) (by decide)

end AflbLean.Fiber
