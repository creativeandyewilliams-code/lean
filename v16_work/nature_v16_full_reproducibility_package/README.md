# Nature v16 full reproducibility package

FMI–CNS–Great Filter: "First-order conflation and recurrent fragmentation
generate a cognitive near-singularity in reflective conceptual systems"
(Article v16 + Supplementary Information v16), with the complete source, data,
formal core, experiments, receiver-study artifacts, logs, audits, and build
tooling.

## Headline result
The previously fail-closed **v8 Gate Zero is now closed-positive**: the supplied
`nature_v8_full_reproducibility_package.zip` (SHA-256 `f21b7ba6…`) reproduces
**bit-for-bit** (model hash `797b16e3…`, registry hash `b7a6ef0e…`, all 18 data
files identical after decompression), and the twelve key inherited values
regenerate at full precision.

## Layout
- `original_inputs/` — the v8 package, the v16 instructions, v15 sources, hashes.
- `registry/` — frozen v16 source-of-truth records and version diff.
- `lean/` — pinned pure-Lean 4 core (10 primary theorems), static audit, reports.
- `experiments/` — gate_zero_v16, direct_recurrence, semantic_equivalence,
  gf_branch_closure (each with code, data, reports).
- `receiver/` — bounded isolated same-model receiver study (tasks, sealed key,
  generation A/B outputs, scoring, contamination audit).
- `manuscript/` — Article & Supplement v16 in `.md`, `.tex`, `.pdf`, `.docx`.
- `reports/` — executive gate report, final status vector, per-gate reports.
- `tools/` — manuscript renderer + markdown converter.

## Rebuild
```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.in
./run_all.sh        # or: make all
python3 verify_package.py
```

## Environment blockers (documented, with evidence)
- **Lean kernel build**: the Lean toolchain binary download from GitHub releases
  is blocked by the environment's egress policy (HTTP 403; see
  `lean/reports/toolchain_block_evidence.txt`). The Lean source is
  kernel-ready and static-audit-clean; run `lake build` where the pinned
  toolchain is installable.
- **LaTeX engine**: none available here; PDFs are produced by the included
  renderer and the `.tex` files (pandoc-generated) are provided for a LaTeX
  build elsewhere. **Docker daemon / external model APIs**: unavailable.
  See `reports/capability_matrix.json`.

## Data & code availability
All numerical data are synthetic and contained in this package. The v8 lineage
is under `original_inputs/` and was reproduced by the Gate Zero rerun; the
recurrence, mutation, branch/hazard and receiver artifacts (code + raw outputs +
scoring) are under `experiments/` and `receiver/`.

## AI-assistance statement
Manuscript drafting, code generation, and orchestration used AI assistance. The
bounded receiver study used isolated fresh-context agent instances as blinded
receivers (distinct from the authoring/orchestration role); it warrants
same-model isolated-instance regenerative propagation only, not cross-model or
human transfer.
