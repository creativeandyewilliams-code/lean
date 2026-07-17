/-
Fragmentation dynamics over the naturals: backlog growth (T-UFRAG-QUEUE, unit
gap form), reversal to bounded residual (T-REVERSAL), and renewed post-lift
growth (T-RECURRENCE, shifted form).
-/
namespace FmiCns

/-- T-UFRAG-QUEUE (unit-gap form). If the backlog rises by at least one unit
    each step, then `U n ≥ U 0 + n`, hence it is unbounded. -/
theorem backlog_growth (U : Nat → Nat)
    (h : ∀ t, U t + 1 ≤ U (t + 1)) : ∀ n, U 0 + n ≤ U n := by
  intro n
  induction n with
  | zero => simpa using Nat.le_refl (U 0)
  | succ k ih =>
    calc U 0 + (k + 1) = (U 0 + k) + 1 := by rw [Nat.add_succ]
      _ ≤ U k + 1 := Nat.succ_le_succ ih
      _ ≤ U (k + 1) := h k

/-- T-REVERSAL (bounded-residual form). If after the lift the backlog is
    nonincreasing and starts bounded by `c`, it stays bounded by `c`. -/
theorem backlog_reversal (U : Nat → Nat) (c : Nat)
    (h : ∀ t, U (t + 1) ≤ U t) (hb : U 0 ≤ c) : ∀ n, U n ≤ c := by
  intro n
  induction n with
  | zero => exact hb
  | succ k ih => exact Nat.le_trans (h k) ih

/-- T-RECURRENCE (shifted form). If, after a post-lift time `T`, the backlog
    again rises by at least one unit each step, it is unbounded above `T`. -/
theorem backlog_recurrence (U : Nat → Nat) (T : Nat)
    (h : ∀ k, U (T + k) + 1 ≤ U (T + (k + 1))) : ∀ n, U T + n ≤ U (T + n) := by
  intro n
  induction n with
  | zero => simpa using Nat.le_refl (U T)
  | succ k ih =>
    calc U T + (k + 1) = (U T + k) + 1 := by rw [Nat.add_succ]
      _ ≤ U (T + k) + 1 := Nat.succ_le_succ ih
      _ ≤ U (T + (k + 1)) := h k

end FmiCns
