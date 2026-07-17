import FmiCnsFull.GreatFilter.Conditional

namespace FmiCnsFull

/-- Top-level conditional filter theorem, exported under a manuscript-facing
    name. -/
theorem formalConditionalGreatFilter
    {Lineage : Type*} (M : FilterModel Lineage)
    (C : CNSFilterMechanism) (hC : StructurallyAdmissible C)
    (B : CNSExternalBridge Lineage M)
    (hPhysical : B.physicalMapping)
    (hBranch : B.branchCorrelation)
    (hHazard : B.nonSummableHazard)
    (hTime : B.timescaleSufficient)
    (hResidue : B.residueOutcomeSufficient) :
    SufficientFilter M := by
  exact conditionalGreatFilter M C hC B hPhysical hBranch hHazard hTime hResidue

end FmiCnsFull
