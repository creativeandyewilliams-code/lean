/-
Core: typed layers, operations, pointed systems, admissible maps.
Pure Lean 4 core (no Mathlib).
-/
namespace FmiCns

/-- Representational layers of a functional state space. -/
inductive Layer where
  | signal
  | concept
  | memory
  deriving DecidableEq, Repr

/-- A typed operation carries a domain and codomain layer and an identity tag. -/
structure Op where
  name : String
  dom  : Layer
  cod  : Layer
  deriving Repr

/-- Canonical FMI operations. -/
def Register : Op := ⟨"Register", Layer.signal, Layer.concept⟩
def Express  : Op := ⟨"Express",  Layer.concept, Layer.signal⟩
def Recall   : Op := ⟨"Recall",   Layer.memory, Layer.concept⟩
def Lop      : Op := ⟨"L", Layer.concept, Layer.concept⟩
def Gop      : Op := ⟨"G", Layer.concept, Layer.concept⟩

/-- Signal and concept layers are distinct. -/
theorem signal_ne_concept : Layer.signal ≠ Layer.concept := by decide

/-- Memory and concept layers are distinct. -/
theorem memory_ne_concept : Layer.memory ≠ Layer.concept := by decide

end FmiCns
