/-
Root module: imports every sub-module of the AFLB Lean formalization.

Project: Lean 4 formalization of the second-order physics of gravitation paper.
Toolchain: leanprover/lean4:v4.14.0 (no Mathlib; stdlib only)
See docs/CLAIM_INVENTORY.md, docs/AXIOM_LEDGER.md, docs/BUILD_REPORT.md.
-/

import AflbLean.Core
import AflbLean.NonReducibility
import AflbLean.GhzSupport
import AflbLean.GainBound
import AflbLean.Rendering
import AflbLean.StrictSeparation
import AflbLean.Hypotheses
import AflbLean.Assumptions
import AflbLean.Conditional

-- Re-export headline theorems at the top level for #print axioms convenience.

/-- Fiber criterion (⇐ direction): non-constant fiber ⇒ no sound/complete decider. -/
def AflbLean.fiberCriterion := @AflbLean.NonReducibility.fiberCriterion

/-- Four-coordinate non-reducibility: every coordinate is indispensable. -/
def AflbLean.nonReducibility := @AflbLean.NonReducibility.nonReducibility

/-- Second-order minimality: no single-coordinate-dropping reduction is adequate. -/
def AflbLean.secondOrderMinimality := AflbLean.NonReducibility.secondOrderMinimality

/-- GHZ support base: ghzSize b 0 = 1. -/
def AflbLean.ghzSupportBase := @AflbLean.GhzSupport.ghzSupportBase

/-- GHZ support recurrence: ghzSize b (n+1) = b · ghzSize b n. -/
def AflbLean.ghzSupportRecurrence := @AflbLean.GhzSupport.ghzSupportRecurrence

/-- Finite-target gain (discrete Nat version): target reached in finite steps. -/
def AflbLean.finiteTargetGain := @AflbLean.GainBound.finiteTargetGain

/-- Minimal rendering dimension: ℝ³ works, ℝ² fails. -/
def AflbLean.minRenderingDim := AflbLean.Rendering.minRenderingDim

/-- Proper-support indistinguishability: ρ₀ and ρ₁ are locally identical. -/
def AflbLean.properSupportIndistinguishability :=
  AflbLean.StrictSeparation.properSupportIndistinguishability

/-- Strict separation witness: open vs blocked have same local projection, different corridor. -/
def AflbLean.strictSeparationWitness := AflbLean.StrictSeparation.strictSeparationWitness

/-- No local decider: bridge-erasing functions cannot decide corridor. -/
def AflbLean.noLocalDecider := AflbLean.StrictSeparation.noLocalDecider

/-- Conditional: second-order observability relative to sharedBasis. -/
def AflbLean.secondOrderObservability := @AflbLean.Conditional.secondOrderObservability

/-- Conditional: shared-basis downstream closure. -/
def AflbLean.observabilityPairedClosure := @AflbLean.Conditional.observabilityPairedClosure
