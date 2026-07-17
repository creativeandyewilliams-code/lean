import Mathlib

namespace FmiCnsFull

/-- Finite span certificate: every required region must be reached from the
    declared root by the registered decision procedure. -/
structure FiniteSpanData (Region : Type*) [DecidableEq Region] where
  required : Finset Region
  root : Region
  reaches : Region → Region → Bool

/-- Executable span decision. -/
def spansB {Region : Type*} [DecidableEq Region]
    (S : FiniteSpanData Region) : Bool :=
  S.required.all (fun r => S.reaches S.root r)

/-- Propositional statement corresponding to `spansB`. -/
def SpansFinite {Region : Type*} [DecidableEq Region]
    (S : FiniteSpanData Region) : Prop :=
  spansB S = true

/-- T-SPAN-DECIDABLE-FINITE. -/
theorem spanDecidableFinite {Region : Type*} [DecidableEq Region]
    (S : FiniteSpanData Region) : Decidable (SpansFinite S) :=
  inferInstance

/-- A positive finite certificate exposes the certified reachability of each
    required region. -/
theorem spansFinite_iff
    {Region : Type*} [DecidableEq Region]
    (S : FiniteSpanData Region) :
    SpansFinite S ↔ ∀ r ∈ S.required, S.reaches S.root r = true := by
  simp [SpansFinite, spansB, Finset.all_eq_true]

end FmiCnsFull
