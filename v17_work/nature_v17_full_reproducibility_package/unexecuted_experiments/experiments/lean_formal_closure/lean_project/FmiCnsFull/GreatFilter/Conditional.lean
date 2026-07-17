import FmiCnsFull.GreatFilter.Admissibility

namespace FmiCnsFull

/-- External bridge for the GF-3 claim.  Each premise remains a theorem
    parameter and can be supported, rejected, or left open independently. -/
structure CNSExternalBridge (Lineage : Type*) (M : FilterModel Lineage) where
  cnsFailure : Lineage → Prop
  physicalMapping : Prop
  branchCorrelation : Prop
  nonSummableHazard : Prop
  timescaleSufficient : Prop
  residueOutcomeSufficient : Prop
  everyConsequentialFails : ∀ l, M.consequential l → cnsFailure l
  failureProducesOutcome : ∀ l, cnsFailure l → M.outcome l

/-- COR-GF-CNS.  Unlike the v16 conjunction-introduction theorem, the
    conclusion is the universal filter target.  The proof composes the external
    coverage and outcome implications while retaining every empirical premise
    as a visible parameter. -/
theorem conditionalGreatFilter
    {Lineage : Type*} (M : FilterModel Lineage)
    (C : CNSFilterMechanism) (hC : StructurallyAdmissible C)
    (B : CNSExternalBridge Lineage M)
    (hPhysical : B.physicalMapping)
    (hBranch : B.branchCorrelation)
    (hHazard : B.nonSummableHazard)
    (hTime : B.timescaleSufficient)
    (hResidue : B.residueOutcomeSufficient) :
    SufficientFilter M := by
  intro l hconsequential
  exact B.failureProducesOutcome l (B.everyConsequentialFails l hconsequential)

end FmiCnsFull
