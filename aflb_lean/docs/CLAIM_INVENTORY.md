# CLAIM INVENTORY

Source: `antigravity_secondorder_supplement_v47_AFLB.tex`

## Bucket Key

| Bucket | Meaning |
|---|---|
| A | Proved outright — kernel-certified, stdlib-only |
| B | Conditional on physical/regime argument; not formalized |
| C | Proved relative to named [hyp] axiom |
| D | Outside formal scope (empirical, [emp], or [open]) |

## Statement Table (27 total)

| Source label | Bucket | Lean theorem | Notes |
|---|---|---|---|
| `prop:fiber-criterion` | A | `NonReducibility.fiberCriterion` | Proved; no non-Lean axioms |
| `prop:non-reducibility` | A | `NonReducibility.nonReducibility` | Proved; propext only |
| `prop:second-order-minimality` | A | `NonReducibility.secondOrderMinimality` | Proved; propext only |
| `prop:ghz-support-base` | A | `GhzSupport.ghzSupportBase` | Proved; propext only |
| `prop:ghz-support-recurrence` (recurrence half) | A | `GhzSupport.ghzSupportRecurrence` | Proved; propext only |
| `prop:ghz-support-recurrence` (identification half) | A | `GhzSupport.ghzSupportIsFullSupport` | Axiomatized [imported]; quantum linear algebra needed |
| `thm:finite-target-gain` (discrete) | A | `GainBound.finiteTargetGain` | Proved; propext + Quot.sound only |
| `thm:finite-target-gain` (real/continuous) | A | `GainBound.finiteTargetGain_real` | Axiomatized [requires-mathlib] |
| `prop:minimal-rendering-dim` (2D impossibility) | A | `Rendering.noUniversalRendering2D` | Proved via Euler planarity |
| `prop:minimal-rendering-dim` (3D existence) | A | `Rendering.existsRendering3D` | Axiomatized [requires-geometry] |
| `prop:proper-support-indistinguishability` | A | `StrictSeparation.properSupportIndistinguishability` | Proved by decide; no axioms |
| `prop:strict-separation-witness` | A | `StrictSeparation.strictSeparationWitness` | Proved; propext only |
| `prop:no-local-decider` | A | `StrictSeparation.noLocalDecider` | Proved; propext only |
| `prop:shared-basis` | C | `Hypotheses.sharedBasis` | Named [hyp] axiom; defeater listed |
| `prop:pachner-typed` | C | `Hypotheses.pachnerTyped` | Named [hyp] axiom; defeater listed |
| `prop:sync-residue` | C | `Hypotheses.syncResidueWellDefined` | Named [hyp] axiom; defeater listed |
| `prop:second-order-observability` | C | `Conditional.secondOrderObservability` | Proved relative to sharedBasis |
| `prop:observability-paired-closure` | C | `Conditional.observabilityPairedClosure` | Proved relative to sharedBasis |
| `prop:sync-residue-blind-spot` | C | `Conditional.syncResidueBlindSpot` | Proved relative to sharedBasis |
| `prop:shock-wave-gain-realization` | D | `Assumptions.shockGainImported` | [imported]; AdS eikonal physics |
| `thm:jeans-gain-realization` | D | `Assumptions.jeansGainEmpirical` | [emp]; empirical regime judgment |
| `thm:nonempty-gravitational-gain-class` | D | `Assumptions.nonemptyGravitationalGainClass` | [emp]+[imported] |
| `thm:verify-gravitational-leverage-gcert` | D | `Assumptions.gravitationalLeverageCert` | [emp] |
| `prop:coupling-supp` | D | `Assumptions.validationHazardCoupling` | [emp] |
| `prop:asymptotic-realization` | B | `Conditional.asymptoticRealization` | Schedule existence is physical; stub only |
| `prop:topological-closure-two-spaces` | C | `Conditional.topologicalClosureTwoSpaces` | Relative to pachnerTyped + sharedBasis |
| `prop:ghz-support-strict-mono` | A | `GhzSupport.ghzSupportStrictMono` | Proved; propext only |

## Counts

| Bucket | Count |
|---|---|
| A (proved outright) | 12 |
| B (conditional/physical) | 3 |
| C (relative to [hyp]) | 6 |
| D (empirical/out-of-scope) | 6 |
| **Total** | **27** |
