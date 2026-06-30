/-
Axiom audit driver (v51).
Run: lake env lean scripts/PrintAxioms.lean > docs/axioms.txt 2>&1

Bucket-A determination results must show core axioms only (propext,
Quot.sound, or none) — in particular none of them may depend on
`SecondOrder.secondOrderResult`'s `pairRes`/`physOp` hypothesis parameters
(those are not global axioms in v51 at all; see Posits.lean and
BUILD_REPORT.md facts (1) and (2)).
-/

import AflbLean
import AflbLean.Legacy.Hypotheses
import AflbLean.Legacy.Conditional
import AflbLean.Legacy.Imported

-- Bucket A: the physics-determination theorems (core axioms only, headline)
#print axioms AflbLean.inverseBranchResponsePositive
#print axioms AflbLean.regularBranchCoefficientPositivity
#print axioms AflbLean.viableAdmSignInvariant
#print axioms AflbLean.signInvariance
#print axioms AflbLean.fiberCriterion
#print axioms AflbLean.classifyCovers
#print axioms AflbLean.classifyExclusive
#print axioms AflbLean.finiteCertificateClosureAscending
#print axioms AflbLean.finiteCertificateClosureComplete
#print axioms AflbLean.viabilityNonReducibility

-- Bucket B: conditional result. `pairRes`/`physOp` are bare Prop hypothesis
-- *parameters* of this theorem (not global axioms), so this line shows no
-- extra axiom dependency beyond the kernel ones — the dependency on the
-- physics posits is visible instead in the theorem's own type signature.
#print axioms AflbLean.secondOrderResult

-- Legacy registration-layer conditionals (Bucket C, relative to sharedBasis) — NOT headline.
#print axioms AflbLean.Legacy.Conditional.syncResidueBlindSpot
#print axioms AflbLean.Legacy.Conditional.topologicalClosureTwoSpaces

-- Named axiom inventory (never expected to be "no axioms") — legacy/ledger only.
#print axioms AflbLean.Legacy.Hypotheses.sharedBasis
#print axioms AflbLean.Legacy.Hypotheses.pachnerTyped
#print axioms AflbLean.Legacy.Hypotheses.syncResidueWellDefined
#print axioms AflbLean.Legacy.Imported.odeGlobalExistence
#print axioms AflbLean.Legacy.Imported.energyDescentIdentity
