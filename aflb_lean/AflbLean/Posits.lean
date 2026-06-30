/-
v51 revision of the Bucket-C physics posits, refactored away from
"global axiom used merely to manufacture a proof inhabitant"
(v50's `axiom pairResolution : Prop` + `axiom pairResolution_holds : pairResolution`,
and `axiom physicalOperativity : Prop` + `axiom physicalOperativity_holds : physicalOperativity`).

Two changes relative to v50:

1. `pairResolution` (hyp:pair-resolution): the *decidable mechanism* — a
   threshold-based branch classifier on a transport-relative quantity — is
   now formalized directly, with real (non-axiomatic) exclusivity and
   coverage theorems proved about it. Only the claim that this particular
   threshold is the *physically intrinsic* one (as opposed to some other,
   detector-dependent, rule) remains a named hypothesis, and it is now
   carried as an explicit parameter to whichever downstream theorem needs
   it (see `SecondOrder.secondOrderResult`), not a global axiom asserted
   true by a companion `_holds` axiom.

2. `physicalOperativity` (hyp:ossv5-physical-operativity) is no longer a
   global axiom. It is represented as an ordinary `Prop`-valued hypothesis
   that a conditional theorem may take as an explicit argument. No
   Bucket-A (kernel-checked) theorem in this package takes it as a
   hypothesis or otherwise depends on it.

Source: antigravity_secondorder_supplement_v50_AFLB.tex.
-/

namespace AflbLean.Posits

/-- The two physical branches a counterposed gravitational pair can resolve to. -/
inductive Branch where
  | plus
  | minus
deriving DecidableEq, Repr

/--
**Threshold-based pair-resolution classifier.**
Given a transport-relative quantity `tau` and a threshold `theta`, classify
the pair into `Branch.minus` (inverse branch) when `tau < theta`, and
`Branch.plus` otherwise. This is the decidable *mechanism* cited by
`hyp:pair-resolution`; it is a definition, not an axiom.
Source: supplement hyp:pair-resolution (line 231).
-/
def classify (tau theta : Int) : Branch :=
  if tau < theta then Branch.minus else Branch.plus

/--
**Coverage: every input is classified.**
`classify` always returns `Branch.plus` or `Branch.minus` — there is no
third outcome and no case where the classifier is undefined.
-/
theorem classify_covers (tau theta : Int) :
    classify tau theta = Branch.plus ∨ classify tau theta = Branch.minus := by
  unfold classify
  split <;> simp

/--
**Exclusivity: classification is single-valued.**
No input is classified as both `Branch.plus` and `Branch.minus`
simultaneously — i.e. the classifier never produces a contradictory
verdict. Proved by case-splitting on the defining `if`, not by `decide`
applied to the bare goal (the goal is universally quantified over all
`Int` inputs, so this is genuine, non-vacuous case analysis).
-/
theorem classify_exclusive (tau theta : Int) :
    ¬ (classify tau theta = Branch.plus ∧ classify tau theta = Branch.minus) := by
  unfold classify
  split <;> simp

/-- `classify` agrees with the order relation on `tau`, `theta` it is defined from. -/
theorem classify_minus_iff (tau theta : Int) :
    classify tau theta = Branch.minus ↔ tau < theta := by
  unfold classify
  split
  · constructor
    · intro _; assumption
    · intro _; rfl
  · rename_i h
    constructor
    · intro hcontra; cases hcontra
    · intro hlt; exact absurd hlt h

/-
**Intrinsic pair-resolution hypothesis (`hyp:pair-resolution`).**
The claim that `classify` (for the source's specific physical `tau`,
`theta`) is the *physically intrinsic* resolution rule — decided in
P-space by an intrinsic transport-relative map, not by an observer's
detector choice or budget — is deliberately **not** declared as a
definition or axiom in this file. There is no honest non-trivial Lean
content to assign it (any closed `Prop` we could write here would either
be vacuously true by construction or smuggle in the desired conclusion).
Instead, downstream theorems that need this hypothesis (see
`SecondOrder.secondOrderResult`) take it as a bare universally-quantified
`Prop` *parameter*, so the dependency is visible in the theorem's own
signature and `#print axioms` output, rather than hidden behind a global
axiom with a companion `_holds` axiom asserting it true.
Declared [hyp]; defeater: a branch outcome shown empirically to depend on
detector choice/budget.
Source: supplement hyp:pair-resolution (line 231).
-/

/--
**Physical operativity hypothesis (`hyp:ossv5-physical-operativity`).**
A candidate energy functional is physically/registrationally consequential
only if it is admitted on its own closed viability-bearing operand. This is
an ontic hypothesis of the broader programme, represented here as an
ordinary `Prop` so it can be threaded as an explicit hypothesis into a
conditional (Bucket-B) theorem. No axiom in this file asserts it true, and
no Bucket-A theorem in this package takes it as a hypothesis.
Declared [hyp, ontic]; defeater: a physically consequential candidate shown
to fail its own closed admissibility test.
Source: supplement hyp:ossv5-physical-operativity (line 711).
-/
def PhysicalOperativity (admits : Prop) : Prop := admits

end AflbLean.Posits
