/-
Axiom audit driver.
Run: lake env lean scripts/PrintAxioms.lean > docs/axioms.txt 2>&1

Bucket-A results should show only Lean core axioms (propext, Quot.sound or none).
Bucket-B/C results will additionally show project axioms.
-/

import AflbLean

-- Bucket A: fully kernel-certified
#print axioms AflbLean.fiberCriterion
#print axioms AflbLean.nonReducibility
#print axioms AflbLean.secondOrderMinimality
#print axioms AflbLean.ghzSupportBase
#print axioms AflbLean.ghzSupportRecurrence
#print axioms AflbLean.finiteTargetGain
#print axioms AflbLean.minRenderingDim
#print axioms AflbLean.properSupportIndistinguishability
#print axioms AflbLean.strictSeparationWitness
#print axioms AflbLean.noLocalDecider

-- Bucket B/C: hypothesis-gated
#print axioms AflbLean.secondOrderObservability
#print axioms AflbLean.observabilityPairedClosure

-- Project axiom inventory
#print axioms AflbLean.GhzSupport.ghzSupportIsFullSupport
#print axioms AflbLean.GainBound.finiteTargetGain_real
#print axioms AflbLean.Rendering.existsRendering3D
#print axioms AflbLean.Hypotheses.sharedBasis
#print axioms AflbLean.Hypotheses.pachnerTyped
#print axioms AflbLean.Hypotheses.syncResidueWellDefined
#print axioms AflbLean.Assumptions.shockGainImported
#print axioms AflbLean.Assumptions.jeansGainEmpirical
#print axioms AflbLean.Assumptions.nonemptyGravitationalGainClass
#print axioms AflbLean.Assumptions.gravitationalLeverageCert
#print axioms AflbLean.Assumptions.validationHazardCoupling
