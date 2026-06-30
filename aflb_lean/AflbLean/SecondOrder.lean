/-
Formalizes: thm:secondorder (Bucket B, conditional).
Source: antigravity_secondorder_supplement_v50_AFLB.tex, §"The second-order
theory object" (lines 593-638).
Bucket: B. This theorem never asserts its antecedents; it only shows what
follows once stated conditions (branch membership, intrinsic pair
resolution, physical operativity) hold.

REMOVED relative to the v50 build: the schedule material
(`ScheduleType`/`ScheduleReaches`/`InverseBranchMembership`/
`scheduleRealizesInverse`, formalizing `prop:schedule`). The v50 versions
were `∃ _ : Unit, True` / `True` / proved by `trivial` — effectively
vacuous despite a non-trivial-looking signature. No non-vacuous,
non-Mathlib-dependent Lean content for `prop:schedule` could be built
within this build's scope; it is recorded as an open/unformalized item in
docs/FORMALIZATION_SCOPE.md instead of being encoded as a trivial theorem.
-/

import AflbLean.Physics
import AflbLean.Fiber
import AflbLean.Posits

namespace AflbLean.SecondOrder

open AflbLean.Posits

/--
**Second-order inverse-gravity result (`thm:secondorder`).**
A four-item conjunction citing: (1) the attractive/inverse response shapes
(`Physics.attractiveResponseSign`, `Physics.inverseResponsePositive`);
(2) that the branch condition is physically typed by the intrinsic
pair-resolution law — taken here as an explicit `Prop` hypothesis
`pairRes`, supplied by the caller, rather than a global axiom (see
`Posits.lean`); (3) the physical-operativity ontic hypothesis, likewise
taken as an explicit `Prop` hypothesis `physOp`, not a global axiom; (4)
the registration-side factorization/fiber facts (`Fiber.fiberCriterion`).
The conjunction itself proves nothing new beyond restating these cited
facts together, mirroring the source's proof, which is itself "each
inference uses a named object ... or an explicit bridge" with no further
derivation. Both `pairRes` and `physOp` appear explicitly in this
theorem's signature, so `#print axioms` and direct inspection both show
that this Bucket-B theorem — and only this theorem — depends on them; no
Bucket-A theorem in this package takes either as a hypothesis.
Source: supplement thm:secondorder (lines 614-638).
-/
theorem secondOrderResult
    (α γ r rstar : Int) (hγ : γ > 0) (heqAttr : γ * rstar = 2 * α)
    (hα : α > 0) (hr : r > 0)
    (pairRes physOp : Prop) (_hpairRes : pairRes) (_hphysOp : physOp)
    {State R : Type} (Obs_R : State → R) (Theta_inv : State → Bool)
    (z_plus z_minus : State)
    (hcoreg : Obs_R z_plus = Obs_R z_minus)
    (hplus : Theta_inv z_plus = false) (hminus : Theta_inv z_minus = true) :
    ((r > rstar → 2 * α - γ * r < 0) ∧ (0 < r → r < rstar → 2 * α - γ * r > 0)) ∧
    (2 * α + γ * r > 0) ∧
    pairRes ∧ physOp ∧
    (∀ Θbar : R → Bool, ¬ (∀ z : State, Theta_inv z = Θbar (Obs_R z))) :=
  ⟨AflbLean.Physics.attractiveResponseSign α γ r rstar hγ heqAttr,
   AflbLean.Physics.inverseResponsePositive α γ r hα hγ hr,
   _hpairRes, _hphysOp,
   AflbLean.Fiber.fiberCriterion Obs_R Theta_inv z_plus z_minus hcoreg hplus hminus⟩

end AflbLean.SecondOrder
