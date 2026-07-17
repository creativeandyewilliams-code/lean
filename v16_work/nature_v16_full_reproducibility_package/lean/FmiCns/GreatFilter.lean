/-
GreatFilter: the conditional Great Filter corollary (COR-GF-CNS) with every
external empirical premise carried as an explicit parameter (a `Prop` field),
never as a global axiom.
-/
namespace FmiCns

/-- External empirical premises of the conditional Great Filter claim. Each is
    a `Prop` supplied by the caller; none is asserted globally. -/
structure GFPremises where
  physicalMapping        : Prop
  recurrentBurden        : Prop
  failedLiftOrPropagation : Prop
  branchCorrelation      : Prop
  nonSummableHazard      : Prop
  targetOutcome          : Prop

/-- The modelled filter outcome: the conjunction of the external premises. It
    forms only when all premises hold. -/
def PostIntelligenceFilter (P : GFPremises) : Prop :=
  P.physicalMapping ∧ P.recurrentBurden ∧ P.failedLiftOrPropagation ∧
  P.branchCorrelation ∧ P.nonSummableHazard ∧ P.targetOutcome

/-- COR-GF-CNS. Given proofs of the six external premises, the modelled
    post-intelligence filter outcome follows. This is a GF-3 conditional
    result, not a GF-6 identification: with no premise it proves nothing. -/
theorem conditionalGreatFilter (P : GFPremises)
    (h1 : P.physicalMapping) (h2 : P.recurrentBurden)
    (h3 : P.failedLiftOrPropagation) (h4 : P.branchCorrelation)
    (h5 : P.nonSummableHazard) (h6 : P.targetOutcome) :
    PostIntelligenceFilter P :=
  ⟨h1, h2, h3, h4, h5, h6⟩

end FmiCns
