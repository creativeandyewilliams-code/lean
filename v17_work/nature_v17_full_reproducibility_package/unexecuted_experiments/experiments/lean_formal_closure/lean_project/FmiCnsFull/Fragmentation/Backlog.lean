import Mathlib

namespace FmiCnsFull

/-- Cumulative unresolved burden. -/
def backlog (D B : ℕ → ℝ) (t : ℕ) : ℝ :=
  max 0 (D t - B t)

/-- T-UFRAG-QUEUE in cumulative form.  If demand minus certified service is
    unbounded above, backlog is unbounded above. -/
theorem backlogUnbounded
    (D B : ℕ → ℝ)
    (h : ∀ M : ℝ, ∃ t, M < D t - B t) :
    ∀ M : ℝ, ∃ t, M < backlog D B t := by
  intro M
  rcases h M with ⟨t, ht⟩
  refine ⟨t, lt_of_lt_of_le ht ?_⟩
  exact le_max_right 0 (D t - B t)

/-- T-REVERSAL.  A bounded cumulative residual gives a bounded backlog over
    the declared interval. -/
theorem boundedResidual
    (D B : ℕ → ℝ) (I : Set ℕ) (ε : ℝ)
    (h : ∀ t ∈ I, D t - B t ≤ ε) :
    ∀ t ∈ I, backlog D B t ≤ max 0 ε := by
  intro t ht
  exact max_le_max (le_refl 0) (h t ht)

/-- One queue step with reflected boundary. -/
def queueStep (u arrival service : ℝ) : ℝ :=
  max 0 (u + arrival - service)

/-- A positive arrival-service gap produces a backlog increment whenever the
    previous backlog is nonnegative. -/
theorem queueGrowthStep
    {u arrival service δ : ℝ}
    (hu : 0 ≤ u) (hgap : δ ≤ arrival - service) :
    u + δ ≤ queueStep u arrival service := by
  unfold queueStep
  calc
    u + δ ≤ u + arrival - service := by linarith
    _ ≤ max 0 (u + arrival - service) := le_max_right _ _

/-- Dynamical backlog growth derived from arrivals and service, rather than
    assumed directly as a property of `U`. -/
theorem queueGrowth
    (U A S : ℕ → ℝ) (δ : ℝ)
    (hU : ∀ t, 0 ≤ U t)
    (hrec : ∀ t, U (t + 1) = queueStep (U t) (A t) (S t))
    (hgap : ∀ t, δ ≤ A t - S t) :
    ∀ n, U 0 + (n : ℝ) * δ ≤ U n := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      have hstep : U n + δ ≤ U (n + 1) := by
        rw [hrec n]
        exact queueGrowthStep (hU n) (hgap n)
      calc
        U 0 + ((n + 1 : ℕ) : ℝ) * δ = (U 0 + (n : ℝ) * δ) + δ := by
          push_cast
          ring
        _ ≤ U n + δ := by linarith
        _ ≤ U (n + 1) := hstep

/-- During a positive service margin, a queue decreases by at least `δ` while
    the reflected boundary is inactive. -/
theorem queueReversalStep
    {u arrival service δ : ℝ}
    (hinside : 0 ≤ u + arrival - service)
    (hmargin : δ ≤ service - arrival) :
    queueStep u arrival service ≤ u - δ := by
  unfold queueStep
  rw [max_eq_right hinside]
  linarith

/-- T-RECURRENCE.  After any post-lift time `T`, a renewed positive gap yields
    linear growth from the then-current backlog. -/
theorem queueRecurrence
    (U A S : ℕ → ℝ) (T : ℕ) (δ : ℝ)
    (hU : ∀ t, 0 ≤ U t)
    (hrec : ∀ t, U (t + 1) = queueStep (U t) (A t) (S t))
    (hgap : ∀ k, δ ≤ A (T + k) - S (T + k)) :
    ∀ n, U T + (n : ℝ) * δ ≤ U (T + n) := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      have hstep : U (T + n) + δ ≤ U (T + (n + 1)) := by
        have hs := queueGrowthStep (hU (T + n)) (hgap n)
        simpa [Nat.add_assoc] using (show
          U (T + n) + δ ≤ queueStep (U (T + n)) (A (T + n)) (S (T + n)) from hs)
      have hrecStep : U (T + n + 1) = queueStep (U (T + n)) (A (T + n)) (S (T + n)) :=
        hrec (T + n)
      rw [← hrecStep] at hstep
      calc
        U T + ((n + 1 : ℕ) : ℝ) * δ = (U T + (n : ℝ) * δ) + δ := by
          push_cast
          ring
        _ ≤ U (T + n) + δ := by linarith
        _ ≤ U (T + (n + 1)) := by simpa [Nat.add_assoc] using hstep

end FmiCnsFull
