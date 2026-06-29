# BUILD REPORT

## Toolchain

| Item | Value |
|---|---|
| Lean version | 4.14.0 (x86_64-unknown-linux-gnu, commit 410fab728470, Release) |
| Lake version | 5.0.0-410fab7 (Lean version 4.14.0) |
| Mathlib | **Not used.** Stdlib-only build. |
| Mathlib cache | Not applicable. |
| Installation | Downloaded from github.com/leanprover/lean4/releases/download/v4.14.0/lean-4.14.0-linux.tar.zst |

**Why no Mathlib:** The network proxy policy in this environment blocks `release.lean-lang.org` (the elan manifest server).  GitHub releases are allowed, so we downloaded Lean 4.14.0 directly.  Mathlib's current master targets lean 4.32.0-rc1; finding and building a compatible older Mathlib commit from source within the time budget was not feasible.  All Lean 4 stdlib-available tactics (`omega`, `simp`, `decide`, `rfl`, `by_cases`, induction) and types (`Nat`, `Bool`, `List`, `Float`) were sufficient for all Bucket-A results.  The two items that would genuinely benefit from Mathlib (`finiteTargetGain_real` needing real logarithms, and `existsRendering3D` needing Euclidean geometry) are declared as named axioms with full ledger entries.

## Build Status

| Item | Status |
|---|---|
| `lake build AflbLean` exit code | **0 (success)** |
| Compiled modules | 10 `.olean` files |
| `check_no_sorry.sh` | **OK: no sorry in sources or build log** |
| Compiler sorry warnings | None |
| Compiler errors | None |
| Compiler warnings | 2 (unused variables in `Conditional.lean`; cosmetic only) |

## Per-Module Build Results

| Module | Status | Notes |
|---|---|---|
| `AflbLean.Core` | ✔ Built | Definitions only; no theorems |
| `AflbLean.NonReducibility` | ✔ Built | All theorems proved |
| `AflbLean.GhzSupport` | ✔ Built | Recurrence proved; identification axiomatized |
| `AflbLean.GainBound` | ✔ Built | Discrete version proved; real version axiomatized |
| `AflbLean.Rendering` | ✔ Built | 2D impossibility proved; 3D existence axiomatized |
| `AflbLean.StrictSeparation` | ✔ Built | All theorems proved by decide |
| `AflbLean.Hypotheses` | ✔ Built | Named axioms declared |
| `AflbLean.Assumptions` | ✔ Built | Documented axioms declared |
| `AflbLean.Conditional` | ✔ Built (⚠ lint warnings) | All theorems proved relative to hypotheses |
| `AflbLean` | ✔ Built | Root module |

## Per-Headline-Theorem Axiom Dependencies

| Theorem | Bucket | File:loc | Axioms beyond Lean core |
|---|---|---|---|
| `fiberCriterion` | A | `NonReducibility.lean` | **none** |
| `nonReducibility` | A | `NonReducibility.lean` | `propext` (Lean core) only |
| `secondOrderMinimality` | A | `NonReducibility.lean` | `propext` (Lean core) only |
| `ghzSupportBase` | A | `GhzSupport.lean` | `propext` (Lean core) only |
| `ghzSupportRecurrence` | A | `GhzSupport.lean` | `propext` (Lean core) only |
| `finiteTargetGain` | A | `GainBound.lean` | `propext`, `Quot.sound` (Lean core) only |
| `noUniversalRendering2D` | A | `Rendering.lean` | `propext` (Lean core) only |
| `minRenderingDim` | A | `Rendering.lean` | `existsRendering3D`, `allGraphsRenderIn3D` (documented geometry axioms) |
| `properSupportIndistinguishability` | A | `StrictSeparation.lean` | **none** |
| `strictSeparationWitness` | A | `StrictSeparation.lean` | `propext` (Lean core) only |
| `noLocalDecider` | A | `StrictSeparation.lean` | `propext` (Lean core) only |
| `secondOrderObservability` | C | `Conditional.lean` | `sharedBasis` (project axiom, [hyp]) |
| `observabilityPairedClosure` | C | `Conditional.lean` | `sharedBasis` (project axiom, [hyp]) |

## Bucket-A Downgrade Log

| Source label | Action | Reason |
|---|---|---|
| `prop:ghz-support-recurrence` (identification part) | Split: recurrence proved, identification axiomatized as `ghzSupportIsFullSupport` | Proving that every proper subsystem of |GHZ±_n⟩ is identical requires quantum-state linear algebra (not in Lean 4 stdlib). |
| `thm:finite-target-gain` (real/continuous version) | Axiomatized as `finiteTargetGain_real` | Requires `Real.log` and `Real.ceil` from Mathlib.  Integer-discrete version fully proved. |
| `prop:minimal-rendering-dim` (3D existence) | Axiomatized as `existsRendering3D` + `allGraphsRenderIn3D` | Formal proof requires Euclidean-space geometry (Mathlib.Analysis.InnerProductSpace). 2D insufficiency proved outright via Euler. |

## Reproducibility

To reproduce the build:
```bash
# Install Lean 4.14.0
mkdir -p /opt/lean4
curl -fL https://github.com/leanprover/lean4/releases/download/v4.14.0/lean-4.14.0-linux.tar.zst | tar --use-compress-program=zstd -xC /opt/lean4
export PATH="/opt/lean4/lean-4.14.0-linux/bin:$PATH"

# Build
cd aflb_lean
lake build AflbLean
bash scripts/check_no_sorry.sh
lake env lean scripts/PrintAxioms.lean > docs/axioms.txt
```

No network access is required after the Lean tarball is downloaded (no Mathlib).
