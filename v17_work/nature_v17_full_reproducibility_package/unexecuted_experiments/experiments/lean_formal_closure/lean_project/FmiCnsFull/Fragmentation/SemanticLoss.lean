import FmiCnsFull.Projection.Conflation

namespace FmiCnsFull

/-- Zero-one decision loss. -/
def zeroOneLoss {Y : Type*} [DecidableEq Y] (prediction truth : Y) : ℝ :=
  if prediction = truth then 0 else 1

/-- A collapsed target-different pair forces at least one unit of total
    zero-one loss across the two states. -/
theorem collapsedPairLoss
    {W O Y : Type*} [DecidableEq Y]
    (q : W → O) (φ : W → Y) (d : O → Y)
    {x y : W} (hq : q x = q y) (hφ : φ x ≠ φ y) :
    1 ≤ zeroOneLoss (d (q x)) (φ x) +
        zeroOneLoss (d (q y)) (φ y) := by
  have hd : d (q x) = d (q y) := congrArg d hq
  by_cases hx : d (q x) = φ x
  · have hy : d (q y) ≠ φ y := by
      intro hy
      apply hφ
      calc
        φ x = d (q x) := hx.symm
        _ = d (q y) := hd
        _ = φ y := hy
    simp [zeroOneLoss, hx, hy]
  · by_cases hy : d (q y) = φ y
    · simp [zeroOneLoss, hx, hy]
    · simp [zeroOneLoss, hx, hy]

/-- Weighted pair lower bound. -/
theorem collapsedPairWeightedLoss
    {W O Y : Type*} [DecidableEq Y]
    (q : W → O) (φ : W → Y) (d : O → Y)
    {x y : W} (hq : q x = q y) (hφ : φ x ≠ φ y)
    (w : ℝ) (hw : 0 ≤ w) :
    w ≤ w * zeroOneLoss (d (q x)) (φ x) +
        w * zeroOneLoss (d (q y)) (φ y) := by
  have h := collapsedPairLoss q φ d hq hφ
  have hm := mul_le_mul_of_nonneg_left h hw
  nlinarith

/-- T-SEM-FRAG in finite witness form: every registered collapsed pair
    contributes its nonnegative weight to the aggregate lower bound. -/
structure CollapsedPairWitness (W O Y : Type*) [DecidableEq Y]
    (q : W → O) (φ : W → Y) where
  left : W
  right : W
  collapsed : q left = q right
  separated : φ left ≠ φ right
  weight : ℝ
  weight_nonneg : 0 ≤ weight

end FmiCnsFull
