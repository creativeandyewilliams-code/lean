# Pause Paper v82 — Build Package

Claim-status routing skeleton (Lean 4) for the pre-validation admission
boundary in risk analysis: status non-entailments, the non-decomposability /
assessment-regress boundary, and the propagation-difficulty / fixed-point
gate, as typed distinctions.

This is v82 of the package: it builds on the uploaded
`pause_paper_v81_routing_skeleton_full.lean` with two fixes applied after a
real `lake build` failure and a simulated peer review (see
`BUILD_CERTIFICATE.txt` Section 0 for the exact diff and rationale):

1. **Proof fix** (no theorem statement changed) — `fixed_point_requires_type_preservation`
   and `fixed_point_requires_independence` did not type-check as originally
   written (`cases a` desynced `h` from the simplified goal). Rewritten to
   `simp [fixedPointGate, h]` without `cases a`.
2. **Semantic fix** — `wordingObjectionStatus` previously routed gated wording
   objections straight to `projectionDefeat`, contradicting the paper's own
   "object preservation before objection evaluation" principle. It now routes
   to a new `RoutedStatus.riskShapeReview` status instead, with a new theorem
   confirming this never collapses into `projectionDefeat`.

The originally uploaded v81 file is left unmodified in the repository; only
the copy inside this package was changed.

## Contents
- `ClaimStatusRouting/RoutingSkeleton.lean` — the v82 source (library module).
- `lakefile.lean` — Lake build config (pure Lean, no Mathlib).
- `lean-toolchain` — pinned compiler (`leanprover/lean4:v4.12.0`).
- `build.sh` — runs the structural pre-check then `lake build`.
- `verify_structure.py` — kernel-independent structural verifier.
- `BUILD_CERTIFICATE.txt` — what was verified, hashes, full build log,
  including the failed-then-fixed build transcript.

## Build
```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
source "$HOME/.elan/env"
./build.sh
```
A clean `lake build` (exit 0, no diagnostics) is the kernel-level certificate:
every theorem type-checks with no `sorry`, `admit`, or added `axiom`.

## Scope
Formalizes routing distinctions and explicit non-entailment only. Proves no
empirical risk fact, policy efficacy, reviewer behavior, propagation
efficacy, AI-risk claim, Great Filter claim, journal acceptance, or
governance feasibility.
