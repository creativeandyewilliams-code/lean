# Executive gate report — Nature v16 reproducibility package

**Headline:** the previously fail-closed v8 Gate Zero is now **closed-positive** —
the supplied v8 lineage reproduces bit-for-bit, and every inherited number
regenerates at full precision. The direct recurrence experiment was rebuilt as
one canonical common-latent-world pipeline; a bounded isolated same-model
receiver study, a synthetic Great Filter branch/hazard experiment, and a
model-level mutation suite were executed. A pure-Lean core of the primary
theorems is source-complete and static-audit-clean.

## Gate matrix (see reports/final_status_vector.json for the full vector)
| Gate | Status |
|---|---|
| v8 Gate Zero | **closed-positive** (bit-exact reproduction) |
| Direct recurrence | **closed** (canonical, common latent worlds) |
| Semantic-equivalence mutation | closed-bounded |
| Great Filter branch/hazard | closed-bounded (synthetic) |
| Same-model receiver propagation | closed-bounded (isolated agents) |
| Lean kernel build | partially closed — source-complete, static-audit clean; **toolchain download egress-blocked (HTTP 403)** |
| Cross-model receiver / physical mappings / historical / external AI traces / GF identification | open |
| Journal carrier | partially closed (md/pdf/tex/docx built; .tex not compiled — no LaTeX engine) |

## Irreducible environment blockers (with evidence)
- **Lean toolchain**: `github.com/leanprover/elan/releases` download returns HTTP
  403 under the org egress policy (PyPI allowlisted; GitHub release binaries
  not). Evidence: `lean/reports/toolchain_block_evidence.txt`. Per the proxy
  README, policy denials are not retried. → Lean source is kernel-ready; build
  pending an installable toolchain.
- **LaTeX engine / Docker daemon / external model APIs**: not available; see
  `reports/capability_matrix.json`. These narrow the affected carrier/external
  claims only; they do not block the reproducible package.
