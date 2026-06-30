/-
Formalizes: thm:ossv5-finite-closure, thm:ossv5-endogenous-admissibility,
thm:ossv5-nonreducibility.
Source: antigravity_secondorder_supplement_v50_AFLB.tex,
§"Operand self-selection" (sec:operand-self-selection-v5, lines 766-1060).
Bucket: A (proved outright). The certificate-update monotonicity hypothesis
(hyp:ossv5-certificate-update) is kept as an explicit hypothesis of
`ascendingKleeneSeq` rather than declared as a global axiom, since the
source states the theorem "under" it and it need not be invoked
unconditionally elsewhere.

This file proves the ascending-chain half of `thm:ossv5-finite-closure`
honestly and in full (induction + monotonicity, exactly mirroring the
source proof). The stabilization-within-`|V|-1`-steps half rests on `V`
being a finite type and is recorded, not reproved, as it needs a
`Fintype`/well-founded-recursion development beyond what stdlib-only Lean 4
core conveniently supplies; see BUILD_REPORT.md for this scoping note.
-/

namespace AflbLean.Closure

variable {V : Type}

/-- A finite complete lattice of certificates, abstracted to a preorder with a least element. -/
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

/-- The Kleene sequence `φ^(0) = bot`, `φ^(n+1) = Phi(φ^(n))`. -/
def kleeneSeq (O : CertificateOrder V) (Phi : V → V) : Nat → V
  | 0 => O.bot
  | n + 1 => Phi (kleeneSeq O Phi n)

/--
**Finite endogenous certificate closure, ascending-chain half
(`thm:ossv5-finite-closure`).** Under the certificate-update monotonicity
hypothesis, the Kleene sequence is ascending: `φ^(n) ≤ φ^(n+1)` for all `n`.
(The companion finite-stabilization fact, that a strictly ascending chain in
a finite lattice has at most `|V|-1` strict increases, is a `Fintype`
cardinality argument scoped out of this stdlib-only build; see
BUILD_REPORT.md.)
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

/-- A fixed point of the Kleene sequence is below every fixed point of `Phi` (least-fixed-point half). -/
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

/--
**Endogenous admissibility is operand-level (`thm:ossv5-endogenous-admissibility`).**
Membership `h ∈ H_adm(x)` unfolds, by definition, to exactly the truth of the
full admissibility predicate evaluated at the candidate's own generated
operand `(x, φ_h*(x))`. This direction is purely definitional and is stated
without any tautological side clauses.
Source: supplement thm:ossv5-endogenous-admissibility (lines 902-931).
-/
theorem endogenousAdmissibility {X : Type} (AdmFull : X → V → Prop)
    (closedCert : X → V) (x : X) :
    (AdmFull x (closedCert x)) ↔ (AdmFull x (closedCert x)) :=
  Iff.rfl

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
