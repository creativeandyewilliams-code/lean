/-
Order: the definitional increment lemma (L-ORDER-INCREMENT) and a
representation-invariance witness for the order count (T-ORDER-INVARIANCE,
finite list model). Cognitive order is modelled as the count of registered,
reusable, nonredundant, spanning composition classes.
-/
namespace FmiCns

/-- Registered spanning composition classes as a finite list; `Ord` is its
    length. -/
def Ord {α : Type} (S : List α) : Nat := S.length

/-- L-ORDER-INCREMENT. Adding one new qualifying class not already present
    increases the order by exactly one. -/
theorem order_increment {α : Type} (S : List α) (g : α) (_ : g ∉ S) :
    Ord (g :: S) = Ord S + 1 := by
  simp [Ord]

/-- T-ORDER-INVARIANCE (finite witness). An admissible relabelling `f` of the
    spanning classes preserves the order count. -/
theorem order_invariance {α β : Type} (S : List α) (f : α → β) :
    Ord (S.map f) = Ord S := by
  simp [Ord]

end FmiCns
