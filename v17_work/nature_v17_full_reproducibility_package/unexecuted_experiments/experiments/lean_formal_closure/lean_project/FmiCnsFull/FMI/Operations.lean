import Mathlib

namespace FmiCnsFull

/-- Boundary and internal layers. -/
inductive Layer where
  | signal
  | concept
  | memory
  deriving DecidableEq, Repr

/-- A typed operation. -/
structure TypedOp (dom cod : Layer) where
  name : String
  deriving Repr

/-- Canonical typed operations. -/
def Register : TypedOp .signal .concept := ⟨"Register"⟩
def Express : TypedOp .concept .signal := ⟨"Express"⟩
def Recall : TypedOp .memory .concept := ⟨"Recall"⟩
def L : TypedOp .concept .concept := ⟨"L"⟩
def G : TypedOp .concept .concept := ⟨"G"⟩

/-- Erasure exposes type indices for an extensional nonreduction theorem. -/
structure ErasedOp where
  name : String
  dom : Layer
  cod : Layer
  deriving DecidableEq, Repr

/-- Erase a typed operation while retaining its domain and codomain. -/
def TypedOp.erase {a b : Layer} (o : TypedOp a b) : ErasedOp :=
  ⟨o.name, a, b⟩

/-- Words generated only by L and G. -/
inductive LGWord where
  | l
  | g
  | comp (left right : LGWord)
  deriving DecidableEq, Repr

/-- Every L/G word denotes a conceptual endomorphism. -/
def LGWord.eval : LGWord → TypedOp .concept .concept
  | .l => L
  | .g => G
  | .comp _ _ => ⟨"L/G composition"⟩

/-- T-OP-NONREDUCTION for Register. -/
theorem registerNotGenerated (w : LGWord) :
    w.eval.erase ≠ Register.erase := by
  intro h
  have hdom := congrArg ErasedOp.dom h
  simpa [TypedOp.erase, LGWord.eval, Register] using hdom

/-- T-OP-NONREDUCTION for Recall. -/
theorem recallNotGenerated (w : LGWord) :
    w.eval.erase ≠ Recall.erase := by
  intro h
  have hdom := congrArg ErasedOp.dom h
  simpa [TypedOp.erase, LGWord.eval, Recall] using hdom

end FmiCnsFull
