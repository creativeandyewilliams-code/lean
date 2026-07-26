# Independent Substantive-Warrant Report — Version 23

**Executor:** Claude Code independent carrier-complete audit
**Instance:** THETA-J-SUB-V23 (submission stage), review-instance hash `f1bac795…`
**Actual derived verdict:** `UB` (bounded traversal with unresolved root-relevant residue)
**Integrated recommendation:** major revision
**Expected design result (`GC_sub`) is a hypothesis only and is NOT confirmed.**

## 1. What was mechanically established
- **LaTeX build:** both `target_relative_residue_main_v23.tex` and `…_supplement_v23.tex` compile cleanly with `latexmk` (author preflight exit 0). Recompilation changed the PDF bytes (embedded timestamps), so the review instance was refrozen; the new frozen PDF hashes are `d86426f8…` (main) and `5cddd793…` (supplement).
- **qpdf:** `qpdf --check` returns exit code 0 for both final PDFs, without `--warning-exit-0`. `QPDFCheckCertificate_v23.json` records `status=executed`, `all_exit_zero=true`, `warning_exit_0_used=false`. The **artifact-fidelity qpdf sub-condition closes.**
- **Structural preflight:** the 71-node claim genome parses with exactly 7 `global` and 64 `local` `ChoiceResult` values; no stale `v22` references remain.

## 2. What did NOT close (root-relevant residue)
### 2.1 Formal correctness — central theorems are prose-only
`TheoremLeanCorrespondence_v23.csv` maps the paper's **central results** — *sound bounded closure*, *relative completeness*, and *carrier root* — to `none` / **not encoded**. The Lean source `TargetRelativeResidueV23.lean` (hash `54af4779…`) encodes only the *elementary* spine (§1–5: residue/factorization, evaluator obstruction, refinement monotonicity, canonical observation, splitting, finite scalar Choice, parent-mode noninterference, target-selection sufficiency, integer projection-margin, budget counts). A static audit found **no `sorry`/`admit`/`native_decide`** and no explicit `axiom` declarations (the file uses `open Classical`, i.e. the standard classical-choice axiom). These encoded lemmas read as correct, but they are elementary and are *not* the paper's headline contribution.

### 2.2 Artifact fidelity — machine Lean build not obtained
The mandatory mechanical condition *"successful actual Lean build with exact theorem coverage"* could **not be satisfied in this environment**. The Lean toolchain host `release.lean-lang.org`, the Lake registry `reservoir.lean-lang.org`, and the compiled-Mathlib cache hosts (`mathlib4.blob.core.windows.net`, `lakecache.blob.core.windows.net`) are all denied (HTTP 403) by the session egress policy. The toolchain itself was obtained from the GitHub release mirror and all Mathlib sources/dependencies were materialized from GitHub, but `lake exe cache get` failed on all 8232 modules and a from-source Mathlib build (4 cores) could not complete within the session. This is an **environmental execution gap**, not a demonstrated source defect — the file may well build in a permissive environment — but the required successful-build certificate is absent, so the condition does not close here.

### 2.3 Carrier adequacy — novelty and significance below the journal bar
Assessed against the current Studia Logica profile (original, significant results on formal systems; ≤25 printed pages): the residue/factorization core is an elementary restatement of the standard fact that *a map factors uniquely through its image iff it is constant on the fibres of the observation* (equivalently, a kernel-inclusion / quotient universal property). The genuinely ambitious claims (sound Choice-gated bounded closure; relative completeness; strict global/local separation) are the ones left **unverified**. Theorem-level novelty (`C03`) and capability-level significance (`C04`) are therefore not warranted at accept level.

## 3. Imported recommendation-changing challenges
Five typed carrier challenges were imported and executed through Choice; all remain **unresolved** in this instance:
`CH-NOVELTY` (C03), `CH-SIGNIFICANCE` (C04), `CH-FORMALGAP` (A09/C02), `CH-LEANBUILD` (A07), `CH-RECOMMENDATION` (C14). Each carries `recommendation_effect = major_revision` with a root-relevance path terminating at `O00`.

## 4. Integration and verdict
All 71 nodes were assessed exactly once (7 global family/root aggregations, 64 local leaves); every node reached `conditionally accepted` or `global coherence assessed`. The traversal is a **complete bounded traversal**, so the result is not `NE`. However, it terminates with unresolved root-relevant residue (§2) and an active major-revision condition (§2.3), which by the registered root rule (`major_revision_blocks_GC_sub`, `active_root_residue_blocks_GC_sub`) **blocks `GC_sub`**. The correct actual result is therefore **`UB`**: a bounded traversal leaving root-relevant residue. A successor manuscript version (verified central theorems, strengthened novelty/significance) and a machine Lean build in a permissive environment would be required before `GC_sub` could be reconsidered.
