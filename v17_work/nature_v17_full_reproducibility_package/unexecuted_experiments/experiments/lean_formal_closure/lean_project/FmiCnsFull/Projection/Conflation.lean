import Mathlib

namespace FmiCnsFull

/-- A target factors through a projection when a decoder on the projected
    state reproduces the target on every latent state. -/
def FactorsThrough {W O Y : Type*} (q : W → O) (φ : W → Y) : Prop :=
  ∃ d : O → Y, ∀ x, d (q x) = φ x

/-- Projection adequacy is constancy of the target on projection fibres. -/
def TargetAdequate {W O Y : Type*} (q : W → O) (φ : W → Y) : Prop :=
  ∀ ⦃x y⦄, q x = q y → φ x = φ y

/-- Factorization always implies fibre constancy. -/
theorem factorsThrough_targetAdequate {W O Y : Type*}
    (q : W → O) (φ : W → Y) :
    FactorsThrough q φ → TargetAdequate q φ := by
  rintro ⟨d, hd⟩ x y hxy
  calc
    φ x = d (q x) := (hd x).symm
    _ = d (q y) := congrArg d hxy
    _ = φ y := hd y

/-- T-PROJECTION-ADEQUACY.  For a surjective projection, fibre constancy is
    also sufficient for factorization. -/
theorem targetAdequate_iff_factorsThrough_of_surjective
    {W O Y : Type*} (q : W → O) (φ : W → Y)
    (hq : Function.Surjective q) :
    TargetAdequate q φ ↔ FactorsThrough q φ := by
  constructor
  · intro h
    classical
    choose section hsection using hq
    refine ⟨fun o => φ (section o), ?_⟩
    intro x
    apply h
    exact (hsection (q x)).symm
  · exact factorsThrough_targetAdequate q φ

/-- T-CONFLATE.  A target-different collapsed pair defeats every decoder over
    the first-order projection. -/
theorem firstOrderConflation
    {W O Y : Type*} (q : W → O) (φ : W → Y)
    {x y : W} (hq : q x = q y) (hφ : φ x ≠ φ y) :
    ¬ FactorsThrough q φ := by
  intro hfactor
  have had := factorsThrough_targetAdequate q φ hfactor
  exact hφ (had hq)

/-- COR-LOCAL-STABILITY.  Equal projected states remain equal under every
    finite iterate of a deterministic first-order-local map. -/
theorem localStability {O : Type*} (L : O → O) {o₁ o₂ : O}
    (h : o₁ = o₂) : ∀ n : ℕ, (L^[n]) o₁ = (L^[n]) o₂ := by
  intro n
  simpa [h]

/-- T-REFLECTIVE-NECESSITY.  When a reflective witness is collapsed by the
    first-order map and the target separates it, first-order factorization is
    impossible.  The extra reflective projection records the location of the
    separating witness but is not assumed to be an order lift. -/
theorem reflectiveNecessity
    {W OFO OR Y : Type*}
    (qFO : W → OFO) (qR : W → OR) (h : OR → OFO) (φ : W → Y)
    (hrefine : ∀ z, qFO z = h (qR z))
    {x y : W} (hR : qR x ≠ qR y) (hFO : qFO x = qFO y)
    (hφ : φ x ≠ φ y) :
    ¬ FactorsThrough qFO φ := by
  exact firstOrderConflation qFO φ hFO hφ

end FmiCnsFull
