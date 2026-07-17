/-
TopLevel: the formal mechanism chain. Bundles the kernel-checkable
statements of the retained core theorems into one conclusion (no vague
`globallyCoherent` Boolean placeholder).
-/
import FmiCns.Core
import FmiCns.Projection
import FmiCns.Operations
import FmiCns.Backlog
import FmiCns.Order
import FmiCns.GreatFilter
namespace FmiCns

/-- The formal mechanism chain: first-order conflation impossibility, typed
    Register/Recall nonreduction, unit-gap backlog growth, reversal to bounded
    residual, renewed post-lift growth, and the definitional order increment.
    Each conjunct is one of the retained core theorems. -/
theorem formal_mechanism_chain :
    (∀ {W O Y : Type} (q : W → O) (phi : W → Y) {x y : W},
        q x = q y → phi x ≠ phi y →
        ¬ ∃ d : O → Y, d (q x) = phi x ∧ d (q y) = phi y) ∧
    (∀ w : LGWord, w.toOp ≠ Register) ∧
    (∀ w : LGWord, w.toOp ≠ Recall) ∧
    (∀ U : Nat → Nat, (∀ t, U t + 1 ≤ U (t + 1)) → ∀ n, U 0 + n ≤ U n) ∧
    (∀ (U : Nat → Nat) (c : Nat), (∀ t, U (t + 1) ≤ U t) → U 0 ≤ c →
        ∀ n, U n ≤ c) ∧
    (∀ (U : Nat → Nat) (T : Nat), (∀ k, U (T + k) + 1 ≤ U (T + (k + 1))) →
        ∀ n, U T + n ≤ U (T + n)) ∧
    (∀ {α : Type} (S : List α) (g : α), g ∉ S → Ord (g :: S) = Ord S + 1) := by
  refine ⟨?_, register_not_generated, recall_not_generated, backlog_growth,
          backlog_reversal, backlog_recurrence, ?_⟩
  · intro W O Y q phi x y hq hphi
    exact firstOrderConflation q phi hq hphi
  · intro α S g hg
    exact order_increment S g hg

end FmiCns
