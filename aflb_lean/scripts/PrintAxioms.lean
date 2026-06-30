/-
Axiom audit driver (v50).
Run: lake env lean scripts/PrintAxioms.lean > docs/axioms.txt 2>&1

Bucket-A determination results must show core axioms only (propext,
Quot.sound, or none) — in particular none of them may depend on
Posits.physicalOperativity or Posits.pairResolution. See BUILD_REPORT.md
facts (1) and (2).
-/

import AflbLean

-- Bucket A: the physics-determination theorems (core axioms only)
#print axioms AflbLean.inverseBranchResponsePositive
#print axioms AflbLean.regularBranchCoefficientPositivity
#print axioms AflbLean.signInvariance
#print axioms AflbLean.fiberCriterion
#print axioms AflbLean.finiteCertificateClosure
#print axioms AflbLean.viabilityNonReducibility

-- Bucket B: conditional results (cite pairResolution via secondOrderResult)
#print axioms AflbLean.secondOrderResult
#print axioms AflbLean.scheduleRealizesInverse

-- Legacy registration-layer conditionals (Bucket C, relative to sharedBasis)
#print axioms AflbLean.Conditional.syncResidueBlindSpot
#print axioms AflbLean.Conditional.topologicalClosureTwoSpaces

-- Named axiom inventory (never expected to be "no axioms")
#print axioms AflbLean.Posits.pairResolution
#print axioms AflbLean.Posits.physicalOperativity
#print axioms AflbLean.Hypotheses.sharedBasis
#print axioms AflbLean.Hypotheses.pachnerTyped
#print axioms AflbLean.Hypotheses.syncResidueWellDefined
#print axioms AflbLean.Imported.odeGlobalExistence
#print axioms AflbLean.Imported.energyDescentIdentity
