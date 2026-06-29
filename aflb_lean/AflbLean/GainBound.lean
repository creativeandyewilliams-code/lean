/-
Formalizes: thm:finite-target-gain
Source: antigravity_secondorder_supplement_v47_AFLB.tex, §"Finite-Target Gain Theorem"
Bucket: A (proved outright for the Nat-discrete version)
-/

namespace AflbLean.GainBound

/-- For b ≥ 2 and n ≥ 1: b^n ≥ n. -/
theorem pow_ge_self (b n : Nat) (hb : 2 ≤ b) (hn : 1 ≤ n) : n ≤ b ^ n := by
  induction n with
  | zero => omega
  | succ k ih =>
    rw [Nat.pow_succ]
    by_cases hk : k = 0
    · subst hk; simp; omega
    · have hk1 : 1 ≤ k := by omega
      have ihk : k ≤ b ^ k := ih hk1
      have hbk : 0 < b ^ k := Nat.pos_pow_of_pos k (by omega)
      have h2 : 2 * b ^ k ≤ b ^ k * b := by
        rw [Nat.mul_comm]
        exact Nat.mul_le_mul_left _ hb
      omega

/--
**Finite-Target Gain Theorem (discrete integer version).**
Given lam ≥ 2, q₀ ≥ 1, q₀ ≤ q_star: ∃ N, q_star ≤ lam^N · q₀.
Source: supplement thm:finite-target-gain (integer-discrete specialization).
-/
theorem finiteTargetGain
    (lam q₀ q_star : Nat)
    (hlam : 2 ≤ lam)
    (hq₀  : 1 ≤ q₀)
    (hqs  : q₀ ≤ q_star) :
    ∃ N : Nat, q_star ≤ lam ^ N * q₀ := by
  refine ⟨q_star, ?_⟩
  by_cases h : q_star = 0
  · subst h; simp
  · have hn : 1 ≤ q_star := by omega
    have hpow : q_star ≤ lam ^ q_star := pow_ge_self lam q_star hlam hn
    have hmul : lam ^ q_star ≤ lam ^ q_star * q₀ :=
      Nat.le_mul_of_pos_right _ (by omega)
    omega

theorem finiteTargetGain_tight
    (lam q₀ q_star : Nat)
    (hlam : 2 ≤ lam) (hq₀ : 1 ≤ q₀) (hqs : q₀ ≤ q_star) :
    ∃ N : Nat, N ≤ q_star ∧ q_star ≤ lam ^ N * q₀ := by
  by_cases h : q_star = 0
  · subst h; exact ⟨0, Nat.le_refl _, by simp⟩
  · have hn : 1 ≤ q_star := by omega
    have hpow : q_star ≤ lam ^ q_star := pow_ge_self lam q_star hlam hn
    have hmul : lam ^ q_star ≤ lam ^ q_star * q₀ :=
      Nat.le_mul_of_pos_right _ (by omega)
    exact ⟨q_star, Nat.le_refl _, by omega⟩

/--
Real-logarithm version of finite-target gain.
Requires real analysis; declared as axiom.
See AXIOM_LEDGER.md.
-/
axiom finiteTargetGain_real
    (lam_rho q₀ q_star : Float)
    (hlam : 1 < lam_rho) (hq₀ : 0 < q₀) (hqs : q₀ ≤ q_star) :
    ∃ steps : Float, q₀ * Float.pow lam_rho steps ≥ q_star

end AflbLean.GainBound
