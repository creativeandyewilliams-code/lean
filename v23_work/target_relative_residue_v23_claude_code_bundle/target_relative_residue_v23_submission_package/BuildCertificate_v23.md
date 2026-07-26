# Lean Build Certificate - Version 23

- Status: not_successful (machine build not obtained in this environment)
- UTC timestamp: 2026-07-26T23:43:37Z
- Platform: Linux-6.18.5-x86_64-with-glibc2.39
- Lean version: Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)
- Lake version: Lake version 5.0.0-src+98dc76e (Lean version 4.29.0)
- Exact command attempted: `lake build` (after `lake update`)
- Exit code: non-zero (dependency materialization / from-source mathlib build not completed)
- Lean source SHA-256: 54af477951daa15744b3974d3b61de3ab08e100069a5c2ec74438dc6a594594a
- Toolchain SHA source: leanprover/lean4:v4.29.0 obtained from the GitHub release mirror (github.com allowed); the Lean FRO host release.lean-lang.org is denied by this session's egress policy.

## Why the machine build was not obtained (environmental, not a source defect)
The session egress policy returns HTTP 403 at the gateway for the Lean First-Order infrastructure hosts required to build Mathlib:
- `release.lean-lang.org` (toolchain) — worked around via the GitHub release asset.
- `reservoir.lean-lang.org` (Lake package registry lookup) — blocked; no allowed mirror.
- `mathlib4.blob.core.windows.net` and `lakecache.blob.core.windows.net` (compiled Mathlib cache) — blocked; `lake exe cache get` failed on all 8232 modules.
Mathlib source and its transitive dependencies were successfully materialized from github.com, but a full from-source Mathlib compilation (8232 modules on 4 cores) could not complete within this session. Therefore a successful, machine-checked build certificate cannot be issued here.

## Static audit performed on the exact frozen source (54af477951daa15744b3974d3b61de3ab08e100069a5c2ec74438dc6a594594a)
- `sorry` / `admit` / `native_decide`: none present.
- Explicit `axiom` declarations: none. The file uses `open Classical`, so proofs relying on `Classical.choose`/choice depend on the standard classical-choice axiom (expected, non-defective for a Mathlib development).
- The encoded declarations (§1-5: residue/factorization, evaluator obstruction, refinement monotonicity, canonical observation, splitting, finite scalar Choice, parent-mode noninterference, target-selection sufficiency, integer projection-margin, budget counts) correspond to elementary, plausibly-correct statements on inspection.
- Per TheoremLeanCorrespondence_v23.csv, the paper's CENTRAL results — "Sound bounded closure", "Relative completeness", and "Carrier root" — map to `none` and are explicitly NOT encoded in Lean. A machine build, even if completed, would not certify the central theorems.

## Scope
This certificate records a not-obtained machine build plus a static audit. It does not attest a successful compilation. Only declarations encoded in the Lean source are in scope; see TheoremLeanCorrespondence_v23.csv.
