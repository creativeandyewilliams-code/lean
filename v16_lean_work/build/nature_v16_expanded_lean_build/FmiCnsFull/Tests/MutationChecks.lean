import FmiCnsFull

namespace FmiCnsFull.Tests

/-- A noninjective relabelling can collapse class identity; this defeats the old
    v16 `List.map` formulation and motivates the `Equiv` hypothesis in
    T-ORDER-INVARIANCE. -/
def collapseClasses : Fin 2 → Fin 1 := fun _ => 0

example : (({0, 1} : Finset (Fin 2)).image collapseClasses).card = 1 := by
  decide

example : ({0, 1} : Finset (Fin 2)).card = 2 := by
  decide

/-- Removing non-equivalence permits a duplicate to masquerade as an increment;
    `Finset.insert` blocks that mutation. -/
example : (Finset.insert 0 ({0} : Finset (Fin 2))).card = 1 := by
  decide

/-- Register cannot be collapsed into an L/G word. -/
example (w : LGWord) : w.eval.erase ≠ Register.erase :=
  registerNotGenerated w

/-- A metric/semantic mutation is detected by an invariant formula rather than
    by labels alone. -/
example (X Y : TypedFSS) (F : AdmissibleIso X Y)
    (a b : X.V) (r : ℝ) :
    Formula.eval (Formula.map F (.distLE a b r)) ↔
    Formula.eval (.distLE a b r) := by
  exact Formula.eval_map_iff F (.distLE a b r)

end FmiCnsFull.Tests
