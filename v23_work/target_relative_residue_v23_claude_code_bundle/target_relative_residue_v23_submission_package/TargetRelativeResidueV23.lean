/--
TargetRelativeResidueV23.lean

PROVISIONAL Lean 4 / Mathlib source for Version 23 of
"Target-Relative Residue and Sound Choice-Gated Closure for Finite Assessment Systems".

This source is not a build certificate. It becomes a submission warrant only after
compilation in the recorded environment, placeholder and axiom audit, hashing, and
attachment of a completed BuildCertificate_v23.md.

Intended finite control spine:
* target-relative residue, image-relative factorization, evaluator obstruction,
  refinement, canonical target-image factorization, and residual-pair splitting;
* uniformly typed candidate modes with integer projected-fitness ranks;
* finite deterministic best-candidate selection with an always-available safe halt;
* strict local/global emission for explicit finite candidate lists;
* mode independence because parent mode is absent from ChoiceInput;
* target-selection sufficiency, bounded projection-margin stability, and projected Version-23 budget counts (7 global, 64 local);
* finite parent-mode-history erasure, strict successor-mode emission, and a reporting
  gate distinguishing assessed verdicts from not-executed status.

The admissible-completion and full trace-validator theorems remain prose/schema-level
until separately encoded; see TheoremLeanCorrespondence_v23.csv.
-/

import Mathlib.Data.Set.Lattice
import Mathlib.Data.List.Basic
import Mathlib.Logic.Function.Basic
import Mathlib.Tactic

open Set
open Classical

namespace TargetRelativeResidueV23

universe u v w z

/-! ## 1. Target-relative residue -/

def KernelRel {α : Type u} {β : Type v} (f : α → β) : Set (α × α) :=
  {p | f p.1 = f p.2}

def ResiduePair {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy) : Set (α × α) :=
  KernelRel q \ KernelRel δ

def NoResidue {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy) : Prop :=
  ∀ x y, q x = q y → δ x = δ y

theorem noResidue_iff_residuePair_empty
    {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy) :
    NoResidue q δ ↔ ResiduePair q δ = ∅ := by
  constructor
  · intro h
    ext p
    constructor
    · intro hp
      rcases hp with ⟨hq, hnδ⟩
      exact (hnδ (h p.1 p.2 hq)).elim
    · intro hp
      exact False.elim (by simpa using hp)
  · intro h x y hq
    by_contra hn
    have hp : (x, y) ∈ ResiduePair q δ := ⟨hq, hn⟩
    rw [h] at hp
    simpa using hp

theorem factorization_of_noResidue
    {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy)
    (h : NoResidue q δ) :
    ∃! δbar : Set.range q → δTy,
      ∀ x : α, δbar ⟨q x, ⟨x, rfl⟩⟩ = δ x := by
  classical
  let δbar : Set.range q → δTy := fun y => δ (Classical.choose y.property)
  have δbar_spec : ∀ x : α, δbar ⟨q x, ⟨x, rfl⟩⟩ = δ x := by
    intro x
    dsimp [δbar]
    apply h
    exact Classical.choose_spec (show q x ∈ Set.range q from ⟨x, rfl⟩)
  refine ⟨δbar, δbar_spec, ?_⟩
  intro g hg
  funext y
  rcases y.property with ⟨x, rfl⟩
  simpa using hg x

theorem evaluator_obstruction_at_both_states
    {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy)
    {x y : α} (hq : q x = q y) (hδ : δ x ≠ δ y) :
    ¬ ∃ e : β → δTy, e (q x) = δ x ∧ e (q y) = δ y := by
  rintro ⟨e, hx, hy⟩
  apply hδ
  calc
    δ x = e (q x) := hx.symm
    _ = e (q y) := by rw [hq]
    _ = δ y := hy

theorem residue_refinement
    {α : Type u} {β : Type v} {γ : Type w} {δTy : Type z}
    (qFine : α → β) (h : β → γ) (δ : α → δTy) :
    ResiduePair qFine δ ⊆ ResiduePair (h ∘ qFine) δ := by
  intro p hp
  rcases hp with ⟨hq, hnδ⟩
  exact ⟨congrArg h hq, hnδ⟩

def targetImageObservation
    {α : Type u} {δTy : Type v} (δ : α → δTy) : α → Set.range δ :=
  fun x => ⟨δ x, ⟨x, rfl⟩⟩

theorem canonical_targetImage_factorization
    {α : Type u} {β : Type v} {δTy : Type w}
    (q : α → β) (δ : α → δTy)
    (h : NoResidue q δ) :
    ∃! φ : Set.range q → Set.range δ,
      ∀ x : α, φ ⟨q x, ⟨x, rfl⟩⟩ = targetImageObservation δ x := by
  apply factorization_of_noResidue q (targetImageObservation δ)
  intro x y hq
  exact Subtype.ext (h x y hq)

theorem sufficientObservation_splits_residue
    {α : Type u} {β : Type v} {γ : Type w} {δTy : Type z}
    (q : α → β) (δ : α → δTy) (s : α → γ)
    (hs : NoResidue s δ)
    {x y : α} (hxy : (x, y) ∈ ResiduePair q δ) :
    s x ≠ s y := by
  intro hsame
  exact hxy.2 (hs x y hsame)

/-! ## 2. Finite target-relative Choice -/

inductive Mode
  | local | global | decompose | acquireInfo
  | reviseModel | rollback | haltUndetermined
  deriving DecidableEq, Repr

structure Candidate where
  id : String
  mode : Mode
  contextId : String
  score : Int
  deriving DecidableEq, Repr

/-- The candidate with greater score is fitter. Equal scores use list order as the
    declared deterministic tie rule. -/
def prefer (current next : Candidate) : Candidate :=
  if current.score < next.score then next else current

/-- Safe halt is included as the initial candidate, so selection is always defined. -/
def chooseBest (safeHalt : Candidate) (candidates : List Candidate) : Candidate :=
  candidates.foldl prefer safeHalt

@[simp] theorem chooseBest_nil (safeHalt : Candidate) :
    chooseBest safeHalt [] = safeHalt := by
  rfl

@[simp] theorem chooseBest_singleton (safeHalt a : Candidate) :
    chooseBest safeHalt [a] = prefer safeHalt a := by
  rfl

theorem prefer_right_of_strict (a b : Candidate) (h : a.score < b.score) :
    prefer a b = b := by
  simp [prefer, h]

theorem prefer_left_of_not_strict (a b : Candidate) (h : ¬ a.score < b.score) :
    prefer a b = a := by
  simp [prefer, h]

/-- Two-candidate strict local emission under the scalar total order. -/
theorem strict_local_emission
    (halt local global : Candidate)
    (hh : halt.score < local.score)
    (hg : global.score < local.score) :
    chooseBest halt [global, local] = local := by
  simp [chooseBest, prefer, hh, hg]

/-- Two-candidate strict global emission under the scalar total order. -/
theorem strict_global_emission
    (halt local global : Candidate)
    (hh : halt.score < local.score)
    (hlg : local.score < global.score) :
    chooseBest halt [local, global] = global := by
  simp [chooseBest, prefer, hh, hlg]

structure ChoiceInput where
  targetHash : String
  policyHash : String
  safeHalt : Candidate
  candidates : List Candidate
  deriving Repr

def choose (i : ChoiceInput) : Candidate :=
  chooseBest i.safeHalt i.candidates

/-- Parent mode is not a field of ChoiceInput, so equal successor inputs choose equally. -/
theorem mode_independence (i₁ i₂ : ChoiceInput) (h : i₁ = i₂) :
    choose i₁ = choose i₂ := by
  simpa [h]


/-! ## 3. Finite parent-mode-history erasure and report gate -/

structure RawReviewState where
  input : ChoiceInput
  parentMode : Option Mode
  modeHistory : List Mode
  nonModeHistoryHash : String
  deriving Repr

structure ErasedReviewState where
  input : ChoiceInput
  nonModeHistoryHash : String
  deriving Repr

def eraseParentModeHistory (s : RawReviewState) : ErasedReviewState :=
  { input := s.input, nonModeHistoryHash := s.nonModeHistoryHash }

def chooseFromRawState (s : RawReviewState) : Candidate :=
  choose (eraseParentModeHistory s).input

theorem parentModeHistory_noninterference
    (s₁ s₂ : RawReviewState)
    (h : eraseParentModeHistory s₁ = eraseParentModeHistory s₂) :
    chooseFromRawState s₁ = chooseFromRawState s₂ := by
  simp [chooseFromRawState, h]

/-- A strictly fitter successor global action is emitted independently of parent mode
    in the explicit two-assessment finite model. -/
theorem strict_successor_global_switch
    (halt local global : Candidate)
    (hh : halt.score < local.score)
    (hlg : local.score < global.score)
    (pm₁ pm₂ : Option Mode) :
    chooseFromRawState
      { input := { targetHash := "t", policyHash := "p", safeHalt := halt,
                   candidates := [local, global] },
        parentMode := pm₁, modeHistory := [], nonModeHistoryHash := "h" } = global ∧
    chooseFromRawState
      { input := { targetHash := "t", policyHash := "p", safeHalt := halt,
                   candidates := [local, global] },
        parentMode := pm₂, modeHistory := [], nonModeHistoryHash := "h" } = global := by
  constructor <;> simpa [chooseFromRawState, choose, eraseParentModeHistory] using
    strict_global_emission halt local global hh hlg

inductive ReviewVerdict
  | gc | gi | ub
  deriving DecidableEq, Repr

inductive ReviewOutput
  | notExecuted
  | assessed (v : ReviewVerdict)
  deriving DecidableEq, Repr

def reportGate (traceValid : Bool) (v : ReviewVerdict) : ReviewOutput :=
  if traceValid then .assessed v else .notExecuted

@[simp] theorem noVerdictWithoutValidTrace (v : ReviewVerdict) :
    reportGate false v = .notExecuted := by
  rfl

@[simp] theorem verdictWithValidTrace (v : ReviewVerdict) :
    reportGate true v = .assessed v := by
  rfl

/-! ## 4. Target selection and projected-fitness stability -/

theorem targetSelectionSufficiency
    {α : Type u} {β : Type v} {δTy : Type w}
    (frozen : α → β) (requested : α → δTy) :
    NoResidue frozen requested ↔
      ∃! eval : Set.range frozen → δTy,
        ∀ x : α, eval ⟨frozen x, ⟨x, rfl⟩⟩ = requested x := by
  constructor
  · intro h
    exact factorization_of_noResidue frozen requested h
  · rintro ⟨eval, hEval, _⟩ x y hxy
    calc
      requested x = eval ⟨frozen x, ⟨x, rfl⟩⟩ := (hEval x).symm
      _ = eval ⟨frozen y, ⟨y, rfl⟩⟩ := by cases hxy; rfl
      _ = requested y := hEval y

/-- Integer version of the projection-margin argument. -/
theorem projected_choice_stable
    (projectedBest projectedOther onticBest onticOther ε m : Int)
    (hmargin : projectedOther + m ≤ projectedBest)
    (hm : 2 * ε < m)
    (hbestLo : projectedBest - ε ≤ onticBest)
    (hotherHi : onticOther ≤ projectedOther + ε) :
    onticOther < onticBest := by
  omega

/-! ## 5. Projected Version-23 budget counts -/

inductive PlannedMode
  | local | global | meta
  deriving DecidableEq, Repr

def plannedModesV23 : List PlannedMode :=
  List.replicate 7 .global ++ List.replicate 64 .local

def countMode (m : PlannedMode) : Nat :=
  (plannedModesV23.filter (fun x => x == m)).length

example : countMode .global = 7 := by decide
example : countMode .local = 64 := by decide
example : countMode .meta = 0 := by decide
example : plannedModesV23.length = 71 := by decide

end TargetRelativeResidueV23
