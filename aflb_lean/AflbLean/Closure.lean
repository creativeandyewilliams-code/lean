/-
Formalizes: thm:ossv5-finite-closure, thm:ossv5-nonreducibility.
Source: antigravity_secondorder_supplement_v50_AFLB.tex,
§"Operand self-selection" (sec:operand-self-selection-v5, lines 766-1060).
Bucket: A (proved outright). The certificate-update monotonicity hypothesis
(hyp:ossv5-certificate-update) is kept as an explicit hypothesis of
`ascendingKleeneSeq`/`finiteStabilization` rather than declared as a global
axiom, since the source states the theorem "under" it.

v51 revision: this file now proves the FULL finite-closure result (not just
the ascending-chain half retained in the v50 build). Mathlib's abstract
`Fintype`/`PartialOrder`/`OrderBot` machinery is unavailable in this
sandbox (network-restricted; see BUILD_REPORT.md), so finiteness is
represented concretely via an explicit `rank : V → Nat` function bounded by
a supplied `N : Nat`, rather than an abstract `Fintype` instance. Every
strict increase in the certificate order corresponds to a strict increase
in `rank`, so a pigeonhole argument on `Nat` (not on an abstract finite
type) bounds the number of strict increases by `N`, forcing stabilization
at some index `n ≤ N`. This is a genuinely complete, non-vacuous proof of
the stabilization-and-least-fixed-point claim; see BUILD_REPORT.md for the
honest scoping note on what is lost relative to a full `Fintype` treatment
(chiefly: `rank` is supplied as data rather than derived automatically from
`Fintype.card V` — in a concrete `Fintype` instantiation one would set `N`
to `Fintype.card V` and derive `rank` from a chosen linear extension).

REMOVED relative to the v50 build: `endogenousAdmissibility`, which proved
`P ↔ P` via `Iff.rfl` — a vacuous statement despite a non-trivial-looking
signature. No non-vacuous Lean content for `thm:ossv5-endogenous-admissibility`
could be found without Mathlib; see CLAIM_INVENTORY.md and
FORMALIZATION_SCOPE.md for the honest disposition of that source claim.
-/

namespace AflbLean.Closure

variable {V : Type}

/-- A complete-enough certificate order: a preorder with a least element. -/
structure CertificateOrder (V : Type) where
  le : V → V → Prop
  bot : V
  le_refl : ∀ x, le x x
  le_trans : ∀ x y z, le x y → le y z → le x z
  bot_le : ∀ x, le bot x

/-- A Φ-update map together with its declared monotonicity (`hyp:ossv5-certificate-update`). -/
structure CertificateUpdate (O : CertificateOrder V) where
  Phi : V → V
  mono : ∀ x y, O.le x y → O.le (Phi x) (Phi y)

/--
A concrete (non-`Fintype`) finiteness witness for `V`: a `Nat`-valued rank
that is monotone along `le`, strictly increases on `le`-related but
*distinct* elements, vanishes at `bot`, and is bounded by `N`. This is the
stdlib-only substitute for `[Fintype V] [PartialOrder V] [OrderBot V]`.
-/
structure FiniteWitness (O : CertificateOrder V) (N : Nat) where
  rank : V → Nat
  rank_bot : rank O.bot = 0
  rank_mono : ∀ x y, O.le x y → rank x ≤ rank y
  rank_strict : ∀ x y, O.le x y → x ≠ y → rank x < rank y
  rank_bound : ∀ x, rank x ≤ N

/-- The Kleene sequence `φ^(0) = bot`, `φ^(n+1) = Phi(φ^(n))`. -/
def kleeneSeq (O : CertificateOrder V) (Phi : V → V) : Nat → V
  | 0 => O.bot
  | n + 1 => Phi (kleeneSeq O Phi n)

/--
**Finite endogenous certificate closure, ascending-chain half
(`thm:ossv5-finite-closure`).** Under the certificate-update monotonicity
hypothesis, the Kleene sequence is ascending: `φ^(n) ≤ φ^(n+1)` for all `n`.
Source: supplement thm:ossv5-finite-closure (lines 863-900).
-/
theorem ascendingKleeneSeq (O : CertificateOrder V) (U : CertificateUpdate O) :
    ∀ n, O.le (kleeneSeq O U.Phi n) (kleeneSeq O U.Phi (n + 1)) := by
  intro n
  induction n with
  | zero => simpa [kleeneSeq] using O.bot_le (kleeneSeq O U.Phi 1)
  | succ k ih =>
      have := U.mono _ _ ih
      simpa [kleeneSeq] using this

/-- A fixed point of `Phi` above `bot` bounds the whole Kleene sequence (least-fixed-point half). -/
theorem kleeneSeq_le_fixedPoint (O : CertificateOrder V) (U : CertificateUpdate O)
    (psi : V) (hpsi : U.Phi psi = psi) (hbot : O.le O.bot psi) :
    ∀ n, O.le (kleeneSeq O U.Phi n) psi := by
  intro n
  induction n with
  | zero => simpa [kleeneSeq] using hbot
  | succ k ih =>
      have hstep := U.mono _ _ ih
      rw [hpsi] at hstep
      simpa [kleeneSeq] using hstep

/-- Helper: absent stabilization before `n`, rank grows at least linearly. -/
private theorem rank_ge_of_no_stab (O : CertificateOrder V) (U : CertificateUpdate O)
    {N : Nat} (W : FiniteWitness O N) :
    ∀ n, (∀ k, k < n → kleeneSeq O U.Phi k ≠ kleeneSeq O U.Phi (k + 1)) →
      n ≤ W.rank (kleeneSeq O U.Phi n) := by
  intro n
  induction n with
  | zero => intro _; exact Nat.zero_le _
  | succ k ih =>
      intro hns
      have hprev : ∀ j, j < k → kleeneSeq O U.Phi j ≠ kleeneSeq O U.Phi (j + 1) :=
        fun j hj => hns j (by omega)
      have hk := ih hprev
      have hne : kleeneSeq O U.Phi k ≠ kleeneSeq O U.Phi (k + 1) := hns k (by omega)
      have hle : O.le (kleeneSeq O U.Phi k) (kleeneSeq O U.Phi (k + 1)) :=
        ascendingKleeneSeq O U k
      have hstrict := W.rank_strict _ _ hle hne
      omega

/--
**Finite stabilization (full half of `thm:ossv5-finite-closure`).**
Given a concrete finite witness bounding ranks by `N`, the Kleene sequence
stabilizes at some index `n ≤ N`: `φ^(n) = φ^(n+1)`. This is the genuinely
complete companion to `ascendingKleeneSeq`, proved here without Mathlib via
the `rank` pigeonhole above instead of an abstract `Fintype.card` argument.
-/
theorem finiteStabilization (O : CertificateOrder V) (U : CertificateUpdate O)
    {N : Nat} (W : FiniteWitness O N) :
    ∃ n, n ≤ N ∧ kleeneSeq O U.Phi n = kleeneSeq O U.Phi (n + 1) := by
  apply Classical.byContradiction
  intro hcon
  have hall : ∀ k, k < N + 1 → kleeneSeq O U.Phi k ≠ kleeneSeq O U.Phi (k + 1) := by
    intro k hk heq
    exact hcon ⟨k, by omega, heq⟩
  have hr := rank_ge_of_no_stab O U W (N + 1) hall
  have hbound := W.rank_bound (kleeneSeq O U.Phi (N + 1))
  omega

/-- Once stabilized, the Kleene sequence stays at that value forever. -/
theorem stabilization_persists (O : CertificateOrder V) (U : CertificateUpdate O)
    (n : Nat) (hstab : kleeneSeq O U.Phi n = kleeneSeq O U.Phi (n + 1)) :
    ∀ m, n ≤ m → kleeneSeq O U.Phi m = kleeneSeq O U.Phi n := by
  have key : ∀ d, kleeneSeq O U.Phi (n + d) = kleeneSeq O U.Phi n := by
    intro d
    induction d with
    | zero => rfl
    | succ k ih =>
        show kleeneSeq O U.Phi (n + k + 1) = kleeneSeq O U.Phi n
        have heq1 : kleeneSeq O U.Phi (n + k + 1) = U.Phi (kleeneSeq O U.Phi (n + k)) := rfl
        rw [heq1, ih]
        exact hstab.symm
  intro m hm
  have hmeq : m = n + (m - n) := by omega
  rw [hmeq]
  exact key (m - n)

/--
**Finite endogenous certificate closure, complete statement
(`thm:ossv5-finite-closure`).** Combines stabilization with the
least-fixed-point property: under a concrete finite witness, the Kleene
sequence stabilizes by index `N` at a value `ψ` that is a fixed point of
`Phi` and is `≤` every other fixed point above `bot`. This supersedes the
v50 build's ascending-chain-only result.
-/
theorem finiteCertificateClosureComplete (O : CertificateOrder V) (U : CertificateUpdate O)
    {N : Nat} (W : FiniteWitness O N) :
    ∃ n ψ, n ≤ N ∧ kleeneSeq O U.Phi n = ψ ∧ U.Phi ψ = ψ ∧
      (∀ psi', U.Phi psi' = psi' → O.le O.bot psi' → O.le ψ psi') := by
  obtain ⟨n, hn, hstab⟩ := finiteStabilization O U W
  refine ⟨n, kleeneSeq O U.Phi n, hn, rfl, ?_, ?_⟩
  · show U.Phi (kleeneSeq O U.Phi n) = kleeneSeq O U.Phi n
    exact hstab.symm
  · intro psi' hpsi' hbot'
    exact kleeneSeq_le_fixedPoint O U psi' hpsi' hbot' n

/--
**Necessity of viability-bearing information (`thm:ossv5-nonreducibility`).**
If the admissibility predicate distinguishes two certificates at the same
base record `x` (the viability-distinguishing fiber condition), then it does
not factor through the fitness-erasing projection onto `x` alone.
Source: supplement thm:ossv5-nonreducibility (lines 1013-1060).
-/
theorem viabilityNonReducibility {X : Type} (AdmFull : X → V → Prop)
    (x : X) (phi0 phi1 : V) (hfiber : AdmFull x phi0 ≠ AdmFull x phi1) :
    ¬ ∃ d : X → Prop, ∀ φ : V, AdmFull x φ ↔ d x := by
  rintro ⟨d, hd⟩
  exact hfiber (propext ((hd phi0).trans (hd phi1).symm))

end AflbLean.Closure
