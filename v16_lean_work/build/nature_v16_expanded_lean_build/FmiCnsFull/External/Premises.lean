import Mathlib

namespace FmiCnsFull

/-- External empirical premises are data supplied to theorems, never global
    axioms. -/
structure ExternalPremises where
  physicalFSSMapping : Prop
  currentAIInstantiation : Prop
  historicalOrderLift : Prop
  branchClosureEvidence : Prop
  hazardEvidence : Prop
  timescaleEvidence : Prop
  residueEvidence : Prop

end FmiCnsFull
