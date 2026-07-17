import FmiCnsFull.Core.Semantics
import FmiCnsFull.CNS.Lift

namespace FmiCnsFull

/-- A concrete formalization instance for the core semantic-to-CNS dependency
    chain. -/
structure FormalInstance
    (ClassId Operand W O Y : Type*) [DecidableEq ClassId]
    (P Q : PointedFSS) where
  semanticIso : AdmissiblePointedIso P Q
  targetFormula : Formula P.space
  before : Architecture ClassId Operand
  after : Architecture ClassId Operand
  lift : OrderLift before after
  demand : ℕ → ℝ
  service : ℕ → ℝ
  interval : Set ℕ
  epsilon : ℝ
  residualContract : ∀ t ∈ interval, demand t - service t ≤ epsilon
  oldProjection : W → O
  target : W → Y
  left : W
  right : W
  collapsed : oldProjection left = oldProjection right
  separated : target left ≠ target right

/-- Typed output of the formal mechanism. -/
structure FormalConclusion
    {ClassId Operand W O Y : Type*} [DecidableEq ClassId]
    {P Q : PointedFSS}
    (I : FormalInstance ClassId Operand W O Y P Q) : Prop where
  semantic_invariance :
    Formula.eval (Formula.map I.semanticIso.iso I.targetFormula) ↔
    Formula.eval I.targetFormula
  cns_lift : CNSLiftConclusion I.before I.after I.demand I.service
    I.interval I.epsilon I.oldProjection I.target

/-- Top-level formal FMI-CNS coherence theorem.  Its conclusion contains the
    actual semantic invariance and substantive CNS-lift outputs, not a vague
    Boolean label. -/
theorem formalFmiCnsCoherence
    {ClassId Operand W O Y : Type*} [DecidableEq ClassId]
    {P Q : PointedFSS}
    (I : FormalInstance ClassId Operand W O Y P Q) :
    FormalConclusion I := by
  refine ⟨Formula.eval_map_iff I.semanticIso.iso I.targetFormula, ?_⟩
  exact cnsLift I.lift I.demand I.service I.interval I.epsilon
    I.residualContract I.oldProjection I.target I.collapsed I.separated

end FmiCnsFull
