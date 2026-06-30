/-
Root module: imports every sub-module of the AFLB Lean formalization.

Project: Lean 4 formalization of the second-order physics-determination
layer of the gravitation paper (v50).
Toolchain: leanprover/lean4:v4.14.0 (no Mathlib; stdlib only)
See docs/CLAIM_INVENTORY.md, docs/AXIOM_LEDGER.md, docs/BUILD_REPORT.md.
-/

import AflbLean.Posits
import AflbLean.Physics
import AflbLean.Closure
import AflbLean.Fiber
import AflbLean.SecondOrder
import AflbLean.Imported
import AflbLean.Hypotheses
import AflbLean.Conditional

-- Re-export headline theorems at the top level for #print axioms convenience.

/-- Forced inverse-branch response positivity (`eq:inverse-response`). -/
def AflbLean.inverseBranchResponsePositive := @AflbLean.Physics.inverseResponsePositive

/-- Regular-branch admissibility forces coefficient positivity (KEYSTONE, `lem:ossv5-regularity-positivity`). -/
def AflbLean.regularBranchCoefficientPositivity := @AflbLean.Physics.regularBranchCoefficientPositivity

/-- Sign invariance over the surviving functional class (`thm:ossv5-sign-invariance`). -/
def AflbLean.signInvariance := @AflbLean.Physics.signInvariance

/-- Fiber criterion for the inverse branch (`thm:fiber`). -/
def AflbLean.fiberCriterion := @AflbLean.Fiber.fiberCriterion

/-- Finite endogenous certificate closure, ascending-chain half (`thm:ossv5-finite-closure`). -/
def AflbLean.finiteCertificateClosure := @AflbLean.Closure.ascendingKleeneSeq

/-- Necessity of viability-bearing information (`thm:ossv5-nonreducibility`). -/
def AflbLean.viabilityNonReducibility := @AflbLean.Closure.viabilityNonReducibility

/-- Second-order inverse-gravity result (`thm:secondorder`). -/
def AflbLean.secondOrderResult := @AflbLean.SecondOrder.secondOrderResult

/-- Schedule status (`prop:schedule`). -/
def AflbLean.scheduleRealizesInverse := @AflbLean.SecondOrder.scheduleRealizesInverse
