# FSS Gravity Sector v12 — Build Package

Claim-status routing skeleton (Lean 4) for observer-relative order-N P-space,
conceptual-to-physical projection, inverse global-shape operators, and safe
gravity-intervention boundary routing.

## Contents
- `FssGravitySector/RoutingSkeleton.lean` — the v12 source (library module).
- `lakefile.lean` — Lake build config (pure Lean, no Mathlib).
- `lean-toolchain` — pinned compiler (`leanprover/lean4:v4.12.0`).
- `build.sh` — runs the structural pre-check then `lake build`.
- `verify_structure.py` — kernel-independent structural verifier.
- `BUILD_CERTIFICATE.txt` — what was verified, hashes, reproduction steps.

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
empirical gravitational fact (GR, QFT, bigravity, GW170817, quantum gravity,
dark matter/energy, inverse gravity, safe-experiment, journal acceptance).
