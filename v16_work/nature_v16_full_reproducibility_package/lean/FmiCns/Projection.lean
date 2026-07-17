/-
Projection: first-order conflation (T-CONFLATE) and the local-stability
corollary (COR-LOCAL-STABILITY).
-/
namespace FmiCns

/-- T-CONFLATE. If a first-order projection `q` identifies two latent states
    that a target `phi` must separate, then no decoder over the projected state
    is correct on both. -/
theorem firstOrderConflation
    {W O Y : Type} (q : W → O) (phi : W → Y)
    {x y : W} (hq : q x = q y) (hphi : phi x ≠ phi y) :
    ¬ ∃ d : O → Y, d (q x) = phi x ∧ d (q y) = phi y := by
  rintro ⟨d, h1, h2⟩
  apply hphi
  have : d (q x) = d (q y) := by rw [hq]
  rw [h1, h2] at this
  exact this

/-- COR-LOCAL-STABILITY. If two latent states share the same first-order
    registration, every finite iterate of a first-order-local map `L` agrees
    on them. -/
theorem localStability
    {O : Type} (L : O → O) {o1 o2 : O} (h : o1 = o2) :
    ∀ k : Nat, (Nat.iterate L k) o1 = (Nat.iterate L k) o2 := by
  intro k
  rw [h]

end FmiCns
