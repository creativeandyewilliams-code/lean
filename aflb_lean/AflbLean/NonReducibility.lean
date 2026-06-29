/-
Formalizes: prop:fiber-criterion, prop:second-order-nonreducibility, prop:second-order-minimality
Source: antigravity_secondorder_supplement_v47_AFLB.tex,
        §"Fiber Criterion", §"Second-Order Non-Reducibility"
Bucket: A (finite/combinatorial; proved outright by logic and computation)
-/

import AflbLean.Core

namespace AflbLean.NonReducibility

open AflbLean

/--
**Fiber Criterion (⇐ direction):**
If corridor is NOT constant on some fiber of q, then no function on Q
can be both sound and complete for corridor.
-/
theorem fiberCriterion_bwd {Q : Type}
    (q : WitnessCoords → Q)
    (c d : WitnessCoords)
    (hfiber : q c = q d)
    (hdiff  : corridor c ≠ corridor d) :
    ∀ (decide_corr : Q → Bool),
      ¬ (∀ w : WitnessCoords, decide_corr (q w) = corridor w) := by
  intro decide_corr hall
  have hc := hall c
  have hd := hall d
  rw [hfiber] at hc
  exact hdiff (hc.symm.trans hd)

/--
**Fiber Criterion (main statement):**
corridor is q-measurable only if corridor is constant on every fiber of q.
Source: supplement prop:fiber-criterion.
-/
theorem fiberCriterion {Q : Type}
    (q : WitnessCoords → Q)
    (decide_corr : Q → Bool)
    (hsound_complete : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    ∀ c d : WitnessCoords, q c = q d → corridor c = corridor d := by
  intro c d hfiber
  have hc := hsound_complete c
  have hd := hsound_complete d
  rw [hfiber] at hc
  exact hc.symm.trans hd

theorem bridge_indispensable {Q : Type}
    (q : WitnessCoords → Q) (decide_corr : Q → Bool)
    (hsc : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    q 𝔠_1111 ≠ q 𝔠_0111 := by
  intro heq
  have := fiberCriterion q decide_corr hsc 𝔠_1111 𝔠_0111 heq
  simp [corridor, 𝔠_1111, 𝔠_0111] at this

theorem regime_indispensable {Q : Type}
    (q : WitnessCoords → Q) (decide_corr : Q → Bool)
    (hsc : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    q 𝔠_1111 ≠ q 𝔠_1011 := by
  intro heq
  have := fiberCriterion q decide_corr hsc 𝔠_1111 𝔠_1011 heq
  simp [corridor, 𝔠_1111, 𝔠_1011] at this

theorem history_indispensable {Q : Type}
    (q : WitnessCoords → Q) (decide_corr : Q → Bool)
    (hsc : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    q 𝔠_1111 ≠ q 𝔠_1101 := by
  intro heq
  have := fiberCriterion q decide_corr hsc 𝔠_1111 𝔠_1101 heq
  simp [corridor, 𝔠_1111, 𝔠_1101] at this

theorem support_indispensable {Q : Type}
    (q : WitnessCoords → Q) (decide_corr : Q → Bool)
    (hsc : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    q 𝔠_1111 ≠ q 𝔠_1110 := by
  intro heq
  have := fiberCriterion q decide_corr hsc 𝔠_1111 𝔠_1110 heq
  simp [corridor, 𝔠_1111, 𝔠_1110] at this

/--
**Second-Order Non-Reducibility (Four-Coordinate Theorem).**
Any adequate reduction must distinguish all four witness pairs simultaneously.
Source: supplement prop:second-order-nonreducibility.
-/
theorem nonReducibility {Q : Type}
    (q : WitnessCoords → Q) (decide_corr : Q → Bool)
    (hsc : ∀ w : WitnessCoords, decide_corr (q w) = corridor w) :
    q 𝔠_1111 ≠ q 𝔠_0111 ∧
    q 𝔠_1111 ≠ q 𝔠_1011 ∧
    q 𝔠_1111 ≠ q 𝔠_1101 ∧
    q 𝔠_1111 ≠ q 𝔠_1110 :=
  ⟨bridge_indispensable q decide_corr hsc,
   regime_indispensable q decide_corr hsc,
   history_indispensable q decide_corr hsc,
   support_indispensable q decide_corr hsc⟩

def dropBridge (w : WitnessCoords) : Bool × Bool × Bool := (w.regime, w.history, w.support)
def dropRegime (w : WitnessCoords) : Bool × Bool × Bool := (w.bridge, w.history, w.support)
def dropHistory (w : WitnessCoords) : Bool × Bool × Bool := (w.bridge, w.regime, w.support)
def dropSupport (w : WitnessCoords) : Bool × Bool × Bool := (w.bridge, w.regime, w.history)

/--
**Second-Order Minimality.**
Each single-coordinate-dropping reduction is corridor-inadequate.
Source: supplement prop:second-order-minimality.
-/
theorem secondOrderMinimality :
    (∀ (decide_corr : Bool × Bool × Bool → Bool),
      ¬ ∀ w, decide_corr (dropBridge w) = corridor w) ∧
    (∀ (decide_corr : Bool × Bool × Bool → Bool),
      ¬ ∀ w, decide_corr (dropRegime w) = corridor w) ∧
    (∀ (decide_corr : Bool × Bool × Bool → Bool),
      ¬ ∀ w, decide_corr (dropHistory w) = corridor w) ∧
    (∀ (decide_corr : Bool × Bool × Bool → Bool),
      ¬ ∀ w, decide_corr (dropSupport w) = corridor w) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro d hd
    have h1 : dropBridge 𝔠_1111 = dropBridge 𝔠_0111 := rfl
    have heq := fiberCriterion dropBridge d hd 𝔠_1111 𝔠_0111 h1
    simp [corridor, 𝔠_1111, 𝔠_0111] at heq
  · intro d hd
    have h1 : dropRegime 𝔠_1111 = dropRegime 𝔠_1011 := rfl
    have heq := fiberCriterion dropRegime d hd 𝔠_1111 𝔠_1011 h1
    simp [corridor, 𝔠_1111, 𝔠_1011] at heq
  · intro d hd
    have h1 : dropHistory 𝔠_1111 = dropHistory 𝔠_1101 := rfl
    have heq := fiberCriterion dropHistory d hd 𝔠_1111 𝔠_1101 h1
    simp [corridor, 𝔠_1111, 𝔠_1101] at heq
  · intro d hd
    have h1 : dropSupport 𝔠_1111 = dropSupport 𝔠_1110 := rfl
    have heq := fiberCriterion dropSupport d hd 𝔠_1111 𝔠_1110 h1
    simp [corridor, 𝔠_1111, 𝔠_1110] at heq

end AflbLean.NonReducibility
