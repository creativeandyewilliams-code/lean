import Mathlib

namespace FmiCnsFull

/-- Monotonicity of a consequence operator. -/
def MonotoneConsequence {α : Type*} (Φ : Set α → Set α) : Prop :=
  Monotone Φ

/-- A set is consequence-closed when applying `Φ` adds nothing outside it. -/
def ConsequenceClosed {α : Type*} (Φ : Set α → Set α) (S : Set α) : Prop :=
  Φ S ⊆ S

/-- Least consequence-closed extension of `seed`, defined as the intersection
    of all closed supersets.  This avoids importing an unregistered fixed-point
    axiom. -/
def consequenceClosure {α : Type*} (Φ : Set α → Set α)
    (seed : Set α) : Set α :=
  {x | ∀ S, seed ⊆ S → ConsequenceClosed Φ S → x ∈ S}

/-- The seed embeds into its consequence closure. -/
theorem seed_subset_consequenceClosure
    {α : Type*} (Φ : Set α → Set α) (seed : Set α) :
    seed ⊆ consequenceClosure Φ seed := by
  intro x hx S hseed hclosed
  exact hseed hx

/-- The consequence closure is contained in every closed superset. -/
theorem consequenceClosure_minimal
    {α : Type*} (Φ : Set α → Set α) (seed S : Set α)
    (hseed : seed ⊆ S) (hclosed : ConsequenceClosed Φ S) :
    consequenceClosure Φ seed ⊆ S := by
  intro x hx
  exact hx S hseed hclosed

/-- Under monotonicity, the constructed closure is itself closed. -/
theorem consequenceClosure_closed
    {α : Type*} (Φ : Set α → Set α) (seed : Set α)
    (hmono : MonotoneConsequence Φ) :
    ConsequenceClosed Φ (consequenceClosure Φ seed) := by
  intro x hx
  intro S hseed hclosed
  have hsub : consequenceClosure Φ seed ⊆ S :=
    consequenceClosure_minimal Φ seed S hseed hclosed
  exact hclosed (hmono hsub hx)

/-- Hard admissibility is logically prior to any optional action. -/
def HardAdmissible {α : Type*} (Adm : Set α → Prop)
    (Φ : Set α → Set α) (seed : Set α) : Prop :=
  Adm (consequenceClosure Φ seed)

/-- A numerical action cannot establish hard admissibility when the
    admissibility proposition is false. -/
theorem actionCannotCompensateForInadmissibility
    {α : Type*} (Adm : Set α → Prop) (Φ : Set α → Set α)
    (seed : Set α) (action : Set α → ℝ)
    (hbad : ¬ HardAdmissible Adm Φ seed) :
    ¬ HardAdmissible Adm Φ seed :=
  hbad

end FmiCnsFull
