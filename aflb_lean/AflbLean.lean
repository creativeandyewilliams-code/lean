/-
Root module (v51): imports ONLY the headline physics-determination core.

Project: Lean 4 formalization of the second-order physics-determination
layer of the gravitation paper (v50 manuscript; this is the v51 Lean
package revision).
Toolchain: leanprover/lean4:v4.14.0 (no Mathlib; stdlib only — see
docs/BUILD_REPORT.md for why, and exactly which Mathlib-dependent features
this implies are absent).
See docs/CLAIM_INVENTORY.md, docs/AXIOM_LEDGER.md, docs/BUILD_REPORT.md,
docs/FORMALIZATION_SCOPE.md.

The legacy registration-theory layer (`AflbLean.Legacy.Hypotheses`,
`AflbLean.Legacy.Conditional`) and the unformalized-claim ledger
(`AflbLean.Legacy.Imported`) are deliberately NOT imported here. They still
build (`lake build AflbLean.Legacy.Hypotheses` etc.) but are excluded from
this headline target and from the headline axiom audit; see MANIFEST.md.
-/

import AflbLean.Posits
import AflbLean.Physics
import AflbLean.Closure
import AflbLean.Fiber
import AflbLean.SecondOrder

-- Re-export headline theorems at the top level for #print axioms convenience.

/-- Forced inverse-branch response positivity (`eq:inverse-response`). -/
def AflbLean.inverseBranchResponsePositive := @AflbLean.Physics.inverseResponsePositive

/-- Regular-branch admissibility forces coefficient positivity (KEYSTONE, `lem:ossv5-regularity-positivity`). -/
def AflbLean.regularBranchCoefficientPositivity := @AflbLean.Physics.regularBranchCoefficientPositivity

/-- Sign-blind admissibility invariance (semantic form of `hyp:ossv5-sign-neutrality`). -/
def AflbLean.viableAdmSignInvariant := @AflbLean.Physics.viableAdm_sign_invariant

/-- Sign invariance over the surviving (typed, admissible) functional class (`thm:ossv5-sign-invariance`). -/
def AflbLean.signInvariance := @AflbLean.Physics.signInvariance

/-- Fiber criterion for the inverse branch (`thm:fiber`). -/
def AflbLean.fiberCriterion := @AflbLean.Fiber.fiberCriterion

/-- Pair-resolution classifier coverage (mechanism underlying `hyp:pair-resolution`). -/
def AflbLean.classifyCovers := @AflbLean.Posits.classify_covers

/-- Pair-resolution classifier exclusivity (mechanism underlying `hyp:pair-resolution`). -/
def AflbLean.classifyExclusive := @AflbLean.Posits.classify_exclusive

/-- Finite endogenous certificate closure, ascending-chain half (`thm:ossv5-finite-closure`). -/
def AflbLean.finiteCertificateClosureAscending := @AflbLean.Closure.ascendingKleeneSeq

/-- Finite endogenous certificate closure, full statement: stabilization + least fixed point (`thm:ossv5-finite-closure`). -/
def AflbLean.finiteCertificateClosureComplete := @AflbLean.Closure.finiteCertificateClosureComplete

/-- Necessity of viability-bearing information (`thm:ossv5-nonreducibility`). -/
def AflbLean.viabilityNonReducibility := @AflbLean.Closure.viabilityNonReducibility

/-- Second-order inverse-gravity result (`thm:secondorder`). -/
def AflbLean.secondOrderResult := @AflbLean.SecondOrder.secondOrderResult
