# AFLB Lean Formalization (v51)

A stdlib-only Lean 4 package that kernel-checks the finite/algebraic
deductive skeleton of the second-order antigravity-leverage/branching (AFLB)
gravitation supplement (`antigravity_secondorder_supplement_v50_AFLB.tex`,
`antigravity_secondorder_main_v50_AFLB.tex`). The manuscript is unchanged
from v50; this is a revision of the Lean package only.

## What this is (and isn't)

This package proves, with the Lean 4 kernel, that a specific set of
algebraic/finite deductions in the paper are gap-free given their stated
hypotheses. It does **not** claim the underlying physics is correct, and it
clearly separates:

- **Bucket A** — kernel-checked theorems, core axioms only (`propext`,
  `Quot.sound`, `Classical.choice` at most — never a named physics posit).
- **Bucket B** — conditional results (antecedents never asserted true).
- **Bucket C** — named physics posits, carried as explicit hypothesis
  parameters, never asserted by axiom.
- **Bucket D** — outside formal scope (ledger only).

See `docs/CLAIM_INVENTORY.md` for the full theorem-by-theorem accounting
and `MANIFEST.md` for a quick summary.

## Quick start

```sh
export PATH=/opt/lean4/lean-4.14.0-linux/bin:$PATH   # if using the pinned toolchain
lake build AflbLean
bash scripts/rebuild.sh
```

See `REPRODUCE.md` for full step-by-step instructions.

## Layout

```
AflbLean.lean              -- headline root module (imports only the determination core)
AflbLean/
  Posits.lean               -- threshold classifier mechanism; undeclared physics-posit doc
  Physics.lean               -- character facts, response signs, KEYSTONE, sign invariance
  Closure.lean               -- finite endogenous certificate closure (full theorem)
  Fiber.lean                 -- inverse-target fiber criterion
  SecondOrder.lean            -- conditional combined theorem (Bucket B)
  Legacy/                     -- registration-theory layer + imported analytic ledger (non-headline)
    Hypotheses.lean
    Conditional.lean
    Imported.lean
scripts/
  rebuild.sh                  -- single reproducible build+audit driver
  check_no_sorry.sh
  check_no_placeholders.sh
  PrintAxioms.lean
docs/
  CLAIM_INVENTORY.md          -- per-claim Lean declaration, bucket, axiom-audit result
  AXIOM_LEDGER.md              -- every axiom in the package, headline vs legacy
  BUILD_REPORT.md              -- toolchain, build steps, downgrade log (Mathlib unavailability)
  FORMALIZATION_SCOPE.md       -- everything intentionally not formalized, and why
  PAPER_INTEGRATION.md         -- ready-to-paste manuscript wording
  BUILD_CERTIFICATE.md         -- reproducibility record of the captured PASS build
  axioms.txt, build.log        -- regenerated artifacts (see scripts/rebuild.sh)
```

## Why no Mathlib

This environment cannot reach `mathlib4` or `release.lean-lang.org` (network
policy scopes outbound access to four specific GitHub repos only). The
package is therefore stdlib-only. Two places that would naturally use
Mathlib (real-number arithmetic, finite-lattice cardinality) use honest,
documented stdlib-only substitutes instead — see
`docs/FORMALIZATION_SCOPE.md` for exactly what each substitution does and
does not weaken.

## License

MIT — see `LICENSE`.
