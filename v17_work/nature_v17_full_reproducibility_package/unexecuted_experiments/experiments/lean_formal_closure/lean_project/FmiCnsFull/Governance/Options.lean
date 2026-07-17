import Mathlib

namespace FmiCnsFull

/-- T-OM, pointwise form.  If governance selects an option whose represented
    value is within `δ` of a baseline option, and both represented values are
    within `ε` of realized value, the selected realized value is no worse than
    the baseline by more than `2ε + δ`. -/
theorem optionMonotonicityPointwise
    {Option : Type*}
    (realized represented : Option → ℝ)
    (selected baseline : Option)
    (ε δ : ℝ)
    (hselectedErr : |represented selected - realized selected| ≤ ε)
    (hbaselineErr : |represented baseline - realized baseline| ≤ ε)
    (hselection : represented baseline - δ ≤ represented selected) :
    realized baseline - (2 * ε + δ) ≤ realized selected := by
  have hs := (abs_le.mp hselectedErr).1
  have hb := (abs_le.mp hbaselineErr).2
  linarith

/-- Best-baseline corollary when a maximizing baseline witness is supplied. -/
theorem optionMonotonicityBestBaseline
    {Option : Type*}
    (realized represented : Option → ℝ)
    (selected best : Option)
    (baseline : Set Option)
    (ε δ : ℝ)
    (hbest : best ∈ baseline)
    (hmax : ∀ b ∈ baseline, realized b ≤ realized best)
    (hselectedErr : |represented selected - realized selected| ≤ ε)
    (hbestErr : |represented best - realized best| ≤ ε)
    (hselection : represented best - δ ≤ represented selected) :
    ∀ b ∈ baseline, realized b - (2 * ε + δ) ≤ realized selected := by
  intro b hb
  have hpoint := optionMonotonicityPointwise realized represented selected best
    ε δ hselectedErr hbestErr hselection
  have hle := hmax b hb
  linarith

end FmiCnsFull
