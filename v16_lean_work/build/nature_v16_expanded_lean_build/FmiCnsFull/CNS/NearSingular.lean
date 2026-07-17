import Mathlib

namespace FmiCnsFull

/-- T-SING-CONTENT, comparator form.  When every non-lift intervention is
    bounded by `B`, the lift is bounded below by `L`, and `B < L`, the lift
    strictly dominates every non-lift intervention in structural magnitude. -/
theorem minimalLiftDominatesNonlift
    {Action : Type*}
    (magnitude : Action → ℝ)
    (nonlift : Set Action)
    (lift : Action) (B L : ℝ)
    (hbound : ∀ a ∈ nonlift, magnitude a ≤ B)
    (hlower : L ≤ magnitude lift)
    (hgap : B < L) :
    ∀ a ∈ nonlift, magnitude a < magnitude lift := by
  intro a ha
  have hab := hbound a ha
  linarith

/-- Near-singular content also requires a target consequence not factorizable
    through the prior-order projection; magnitude alone is insufficient. -/
def NearSingularContent
    {Action W O Y : Type*}
    (magnitude : Action → ℝ) (nonlift : Set Action) (lift : Action)
    (qOld : W → O) (φ : W → Y) : Prop :=
  (∀ a ∈ nonlift, magnitude a < magnitude lift) ∧
  ¬ ∃ d : O → Y, ∀ x, d (qOld x) = φ x

end FmiCnsFull
