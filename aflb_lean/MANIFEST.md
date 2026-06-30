# MANIFEST (v50 build)

This package machine-checks the finite/algebraic skeleton of the
second-order gravitation supplement's physics-determination layer
(`antigravity_secondorder_supplement_v50_AFLB.tex`,
`antigravity_secondorder_main_v50_AFLB.tex`), Lean 4.14.0, stdlib only
(no Mathlib).

**What is kernel-certified (Bucket A, core axioms only — confirmed in
`docs/axioms.txt`, no physics posit in any dependency cone):**
- the forced attractive- and inverse-branch radial response signs
  (`eq:attractive-response`, `eq:inverse-response`);
- the coefficient-positivity keystone, `lem:ossv5-regularity-positivity`;
- sign invariance over the surviving functional class,
  `thm:ossv5-sign-invariance`;
- the fiber criterion for the inverse branch, `thm:fiber`;
- the ascending-chain half of finite endogenous certificate closure,
  `thm:ossv5-finite-closure`;
- the necessity of viability-bearing information,
  `thm:ossv5-nonreducibility`.

**What is conditional (Bucket B, antecedents never asserted):**
`thm:secondorder`, `prop:schedule`.

**What is a named, undischarged physics posit (Bucket C):**
`hyp:pair-resolution`, `hyp:ossv5-physical-operativity`, plus the legacy
registration-layer hypotheses `prop:shared-basis`, `prop:sync-residue`,
`def:operation-basis`/`prop:smallest-scale`.

**What is out of formal scope (Bucket D, ledger only, never feeds a
theorem):** the gradient-flow global-existence/uniqueness claim and the
energy-descent identity (`prop:closure`); the falsification/reconstruction
program (`obl:falsification`, `def:reconstruction`).

This is not a claim that the physics is correct. It is a claim that the
named deductive steps above are gap-free given the stated axioms. See
`docs/CLAIM_INVENTORY.md`, `docs/AXIOM_LEDGER.md`, `docs/BUILD_REPORT.md`,
`docs/axioms.txt` for the full accounting.
