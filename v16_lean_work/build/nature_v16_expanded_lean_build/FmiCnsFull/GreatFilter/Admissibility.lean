import FmiCnsFull.GreatFilter.Necessary

namespace FmiCnsFull

/-- Structural properties of recurrent FMI-CNS failure relevant to GF-2. -/
structure CNSFilterMechanism where
  burdenGeneratedByGrowth : Prop
  substrateGeneral : Prop
  liftReversesCurrentBurden : Prop
  recurrenceRecreatesBurden : Prop
  branchInheritanceOrRecreation : Prop
  outcomePremiseExposed : Prop

/-- Structural admissibility is a conjunction of mechanism-class properties;
    it is not external instantiation. -/
def StructurallyAdmissible (C : CNSFilterMechanism) : Prop :=
  C.burdenGeneratedByGrowth ∧ C.substrateGeneral ∧
  C.liftReversesCurrentBurden ∧ C.recurrenceRecreatesBurden ∧
  C.branchInheritanceOrRecreation ∧ C.outcomePremiseExposed

/-- T-CNS-ADMISSIBILITY. -/
theorem cnsStructuralAdmissibility (C : CNSFilterMechanism)
    (h1 : C.burdenGeneratedByGrowth)
    (h2 : C.substrateGeneral)
    (h3 : C.liftReversesCurrentBurden)
    (h4 : C.recurrenceRecreatesBurden)
    (h5 : C.branchInheritanceOrRecreation)
    (h6 : C.outcomePremiseExposed) :
    StructurallyAdmissible C :=
  ⟨h1, h2, h3, h4, h5, h6⟩

end FmiCnsFull
