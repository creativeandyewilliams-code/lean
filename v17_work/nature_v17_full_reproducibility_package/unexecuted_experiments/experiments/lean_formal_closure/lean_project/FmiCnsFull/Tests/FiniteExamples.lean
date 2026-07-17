import FmiCnsFull

namespace FmiCnsFull.Tests

/-- Concrete conflation witness. -/
example : ¬ FactorsThrough (fun _ : Bool => true) (fun b : Bool => b) := by
  exact firstOrderConflation (fun _ : Bool => true) (fun b : Bool => b) rfl (by decide)

/-- A genuine equivalence preserves class cardinality. -/
example : ({0, 1} : Finset (Fin 3)).map (Equiv.refl (Fin 3)).toEmbedding |>.card = 2 := by
  decide

/-- Finite span is executable. -/
def spanExample : FiniteSpanData (Fin 3) where
  required := Finset.univ
  root := 0
  reaches := fun _ _ => true

example : SpansFinite spanExample := by
  decide

/-- A nontrivial holonomy witness. -/
def flipStep : TransportStep Bool := ⟨not⟩

example : ¬ TrivialHolonomy [flipStep] := by
  exact holonomyDrift [flipStep] false (by decide)

end FmiCnsFull.Tests
