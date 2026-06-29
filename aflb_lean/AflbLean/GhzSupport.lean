/-
Formalizes: prop:ghz-support-recurrence
Source: antigravity_secondorder_supplement_v47_AFLB.tex,
        §"Exact Target-Relative Support Recurrence (GHZ-Tree)"
Bucket: A (proved by Nat induction; physical identification axiomatized)
-/

namespace AflbLean.GhzSupport

/-- Size of the n-th GHZ-tree level: N_n = b^n. -/
def ghzSize (b n : Nat) : Nat := b ^ n

/--
Physical identification axiom: d_Θ(n) = N_n = b^n.
The proof that every proper subsystem is identical for GHZ± requires
quantum-state linear algebra ([imported]).
-/
axiom ghzSupportIsFullSupport (b n : Nat) (hb : 2 ≤ b) :
    ∃ (dTheta : Nat → Nat),
      dTheta n = ghzSize b n ∧
      ∀ k, dTheta k = b ^ k

/-- GHZ support base case: b^0 = 1. -/
theorem ghzSupportBase (b : Nat) : ghzSize b 0 = 1 := by
  simp [ghzSize]

/--
**GHZ support recurrence.**
ghzSize b (n+1) = b · ghzSize b n.
Source: supplement prop:ghz-support-recurrence.
-/
theorem ghzSupportRecurrence (b n : Nat) : ghzSize b (n + 1) = b * ghzSize b n := by
  simp [ghzSize, Nat.pow_succ, Nat.mul_comm]

/-- ghzSize b n = b^n (definitionally). -/
theorem ghzSupportClosedForm (b n : Nat) : ghzSize b n = b ^ n := rfl

/-- GHZ support is strictly increasing for b ≥ 2. -/
theorem ghzSupportStrictMono (b n : Nat) (hb : 2 ≤ b) :
    ghzSize b n < ghzSize b (n + 1) := by
  simp [ghzSize, Nat.pow_succ]
  have hpos : 0 < b ^ n := Nat.pos_pow_of_pos n (by omega)
  have h1 : b ^ n * 1 < b ^ n * b := by
    apply Nat.mul_lt_mul_of_pos_left
    · omega
    · exact hpos
  simp at h1
  exact h1

/-- GHZ support grows at least as fast as 2^n. -/
theorem ghzSupportExponentialGrowth (b n : Nat) (hb : 2 ≤ b) :
    2 ^ n ≤ ghzSize b n := by
  simp [ghzSize]
  exact Nat.pow_le_pow_left hb n

end AflbLean.GhzSupport
