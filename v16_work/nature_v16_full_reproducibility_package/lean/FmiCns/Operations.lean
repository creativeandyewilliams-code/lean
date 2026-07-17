/-
Operations: typed L/G word algebra and Register/Recall nonreduction
(T-OP-NONREDUCTION) by a domain (constructor) obstruction.
-/
import FmiCns.Core
namespace FmiCns

/-- Words generated solely by the conceptual endomorphisms L and G. -/
inductive LGWord where
  | lop
  | gop
  | comp (a b : LGWord)
  deriving Repr

/-- Every L/G word is a conceptual endomorphism (domain = concept). -/
def LGWord.dom : LGWord → Layer := fun _ => Layer.concept

/-- Every L/G word is a conceptual endomorphism (codomain = concept). -/
def LGWord.cod : LGWord → Layer := fun _ => Layer.concept

/-- The typed operation induced by an L/G word. -/
def LGWord.toOp (w : LGWord) : Op := ⟨"LGword", w.dom, w.cod⟩

theorem lgword_dom_concept (w : LGWord) : (w.toOp).dom = Layer.concept := rfl

/-- T-OP-NONREDUCTION (Register). No L/G word has the boundary (signal) domain
    of Register. -/
theorem register_not_generated (w : LGWord) : w.toOp ≠ Register := fun h =>
  absurd (congrArg Op.dom h) (by decide)

/-- T-OP-NONREDUCTION (Recall). No L/G word has the memory-access domain of
    Recall. -/
theorem recall_not_generated (w : LGWord) : w.toOp ≠ Recall := fun h =>
  absurd (congrArg Op.dom h) (by decide)

end FmiCns
