# BUILD CERTIFICATE (v51)

This is a **reproducibility/build record**, not a cryptographic proof
certificate. It records the exact environment and commands used to produce
a verified-clean build, so a third party can reproduce the same result.
Trust in the Lean kernel's type-checking is what actually certifies the
theorems; this document only certifies that the recorded build happened as
described.

## Environment

| Item | Value |
|---|---|
| Lean version | 4.14.0 |
| Lean commit | 410fab728470 |
| Build type | Release |
| Platform | x86_64-unknown-linux-gnu |
| Lake version | 5.0.0-410fab7 |
| Mathlib | none (stdlib-only build; confirmed unreachable, see `docs/FORMALIZATION_SCOPE.md`) |
| `lake-manifest.json` | zero pinned packages |

## Rebuild command

```sh
export PATH=/opt/lean4/lean-4.14.0-linux/bin:$PATH
bash scripts/rebuild.sh
```

This single script performs the toolchain check, the explicit-target
headline build (`lake build AflbLean`), the no-sorry audit, the
no-placeholder audit, axiom-ledger regeneration, and the headline-axiom-only
verification, in that order, and exits nonzero if any step fails.

## Result of the captured run

```
=== FINAL RESULT: PASS ===
```

All six steps passed:
1. Toolchain check — PASS.
2. `lake build AflbLean` — PASS (exit 0). Output: `docs/build.log`.
3. No-sorry audit (`scripts/check_no_sorry.sh`) — PASS: no `sorry`/`admit`
   anywhere in `AflbLean.lean` or `AflbLean/` (headline or legacy).
4. No-placeholder audit (`scripts/check_no_placeholders.sh`) — PASS: no
   `sorry`/`admit`; manual-review flags (if any) reported separately and do
   not fail the build.
5. Axiom-audit regeneration (`lake env lean scripts/PrintAxioms.lean`) —
   PASS. Output: `docs/axioms.txt`.
6. Headline-axiom-only verification — PASS: none of the 10 Bucket-A
   declarations depends on a named physics-posit axiom.

## What this certificate does and does not claim

- **Does claim:** the Lean kernel accepted every declaration in
  `AflbLean.lean`/`AflbLean/` (headline and legacy) with no `sorry`, and the
  10 headline theorems' axiom dependencies are exactly the recorded core-axiom
  subsets in `docs/axioms.txt`.
- **Does not claim:** that the underlying physics is correct, that the
  formalized statements are the *only* possible formalization of the source
  propositions, or that anything outside the headline build (Legacy,
  Bucket C/D items) has been independently verified beyond what is stated in
  `docs/AXIOM_LEDGER.md`.

## Reproducing independently

See `REPRODUCE.md` for step-by-step instructions usable without prior
context on this package.
