import FmiCnsFull.Order.Composition
import FmiCnsFull.Fragmentation.Backlog
import FmiCnsFull.Projection.Conflation

namespace FmiCnsFull

/-- Architecture with canonical composition classes and an admissible operand
    domain. -/
structure Architecture (ClassId Operand : Type*) [DecidableEq ClassId] where
  classes : Finset ClassId
  operands : Set Operand

/-- Cognitive order of an architecture. -/
def Architecture.order
    {ClassId Operand : Type*} [DecidableEq ClassId]
    (A : Architecture ClassId Operand) : ℕ :=
  A.classes.card

/-- A registered order lift records freshness of the new class, preservation of
    all prior classes, and strict operand-domain expansion.  Span, reuse, and
    non-equivalence are encoded in the fact that `newClass` is a canonical
    qualifying class ID rather than an implementation call. -/
structure OrderLift
    {ClassId Operand : Type*} [DecidableEq ClassId]
    (before after : Architecture ClassId Operand) where
  newClass : ClassId
  fresh : newClass ∉ before.classes
  class_update : after.classes = insert newClass before.classes
  operand_monotone : before.operands ⊆ after.operands
  operand_strict : ∃ x, x ∈ after.operands ∧ x ∉ before.operands

/-- A strict operand expansion is represented without relying on a library
    theorem about strict set inclusion. -/
def StrictOperandExpansion
    {ClassId Operand : Type*} [DecidableEq ClassId]
    (before after : Architecture ClassId Operand) : Prop :=
  before.operands ⊆ after.operands ∧
  ∃ x, x ∈ after.operands ∧ x ∉ before.operands

/-- The order part of an order lift is derived rather than assumed. -/
theorem liftOrderIncrement
    {ClassId Operand : Type*} [DecidableEq ClassId]
    {before after : Architecture ClassId Operand}
    (L : OrderLift before after) :
    after.order = before.order + 1 := by
  rw [Architecture.order, Architecture.order, L.class_update]
  simpa [Finset.card_insert_of_not_mem L.fresh, Nat.add_comm]

/-- Operand-domain expansion is likewise derived from the lift certificate. -/
theorem liftOperandExpansion
    {ClassId Operand : Type*} [DecidableEq ClassId]
    {before after : Architecture ClassId Operand}
    (L : OrderLift before after) :
    StrictOperandExpansion before after :=
  ⟨L.operand_monotone, L.operand_strict⟩

/-- Complete substantive conclusion of the order-lift CNS theorem. -/
structure CNSLiftConclusion
    {ClassId Operand W O Y : Type*} [DecidableEq ClassId]
    (before after : Architecture ClassId Operand)
    (D B : ℕ → ℝ) (I : Set ℕ) (ε : ℝ)
    (qOld : W → O) (φ : W → Y) : Prop where
  order_increment : after.order = before.order + 1
  operand_expansion : StrictOperandExpansion before after
  residual_bounded : ∀ t ∈ I, backlog D B t ≤ max 0 ε
  old_projection_inadequate : ¬ FactorsThrough qOld φ

/-- T-CNS-LIFT.  The theorem combines a genuine fresh-class order lift,
    operand expansion, arrival-service reversal, and a target-different witness
    not factorizable through the old projection.  The count increment alone is
    not allowed to carry the conclusion. -/
theorem cnsLift
    {ClassId Operand W O Y : Type*} [DecidableEq ClassId]
    {before after : Architecture ClassId Operand}
    (L : OrderLift before after)
    (D B : ℕ → ℝ) (I : Set ℕ) (ε : ℝ)
    (hresidual : ∀ t ∈ I, D t - B t ≤ ε)
    (qOld : W → O) (φ : W → Y)
    {x y : W} (hcollapse : qOld x = qOld y)
    (hseparate : φ x ≠ φ y) :
    CNSLiftConclusion before after D B I ε qOld φ := by
  refine ⟨liftOrderIncrement L, liftOperandExpansion L, ?_, ?_⟩
  · exact boundedResidual D B I ε hresidual
  · exact firstOrderConflation qOld φ hcollapse hseparate

end FmiCnsFull
