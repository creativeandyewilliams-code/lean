# MANIFEST (v51 build)

This package machine-checks the finite/algebraic skeleton of the
second-order gravitation supplement's physics-determination layer
(`antigravity_secondorder_supplement_v50_AFLB.tex`,
`antigravity_secondorder_main_v50_AFLB.tex` — manuscript unchanged from
v50; this is a revision of the Lean package only), Lean 4.14.0, stdlib only
(no Mathlib — confirmed unreachable from this build environment; see
`docs/FORMALIZATION_SCOPE.md`).

**What is kernel-certified (Bucket A, core axioms only — confirmed in
`docs/axioms.txt`, no physics posit in any dependency cone), 10 headline
declarations:**
- `AflbLean.inverseBranchResponsePositive`, `AflbLean.regularBranchCoefficientPositivity`
  — the forced attractive- and inverse-branch radial response signs and the
  coefficient-positivity keystone (`eq:attractive-response`,
  `eq:inverse-response`, `lem:ossv5-regularity-positivity`);
- `AflbLean.viableAdmSignInvariant` — sign-blind admissibility, formalized
  structurally over a type (`NonSignData`) that has no `sgn` field at all
  (`hyp:ossv5-sign-neutrality`);
- `AflbLean.signInvariance` — sign invariance over the actual typed
  admissible class `Admissible`, derived from the keystone rather than
  assumed as a raw premise (`thm:ossv5-sign-invariance`);
- `AflbLean.fiberCriterion` — the fiber criterion for the inverse branch
  (`thm:fiber`);
- `AflbLean.classifyCovers`, `AflbLean.classifyExclusive` — the decidable
  mechanism half of `hyp:pair-resolution`: the threshold classifier always
  returns exactly one branch;
- `AflbLean.finiteCertificateClosureAscending`,
  `AflbLean.finiteCertificateClosureComplete` — the **full** finite
  endogenous certificate closure theorem (not just the ascending-chain
  half): given a concrete rank-based finite witness, the Kleene sequence
  stabilizes at a least fixed point at some `n ≤ N` (`thm:ossv5-finite-closure`);
- `AflbLean.viabilityNonReducibility` — the necessity of viability-bearing
  information (`thm:ossv5-nonreducibility`).

**What is conditional (Bucket B, antecedents never asserted):**
`AflbLean.secondOrderResult` (`thm:secondorder`). Its `pairRes`/`physOp`
dependencies are bare `Prop` hypothesis *parameters* of the theorem, not
global axioms — `docs/axioms.txt` confirms zero axiom footprint for them.

**What is a named, undischarged physics posit (Bucket C):** the
"intrinsicity" half of `hyp:pair-resolution` and
`hyp:ossv5-physical-operativity` — deliberately **not declared** anywhere in
Lean (no `axiom`, no `def` asserted true); they exist only as the `pairRes`/
`physOp` parameters of `secondOrderResult` above. Also the legacy
registration-layer hypotheses `prop:shared-basis`, `prop:sync-residue`,
`def:operation-basis`/`prop:smallest-scale`, retained as named axioms under
`AflbLean.Legacy.Hypotheses`, excluded from the headline build.

**Removed (no honest non-vacuous Lean content found — documented, not
silently dropped):** `thm:ossv5-endogenous-admissibility` (v50's version was
`P ↔ P` via `Iff.rfl`); `prop:schedule` (v50's version was effectively
`True`, proved by `trivial`). See `docs/CLAIM_INVENTORY.md` and
`docs/FORMALIZATION_SCOPE.md`.

**What is out of formal scope (Bucket D, ledger only, never feeds a
headline theorem):** the gradient-flow global-existence/uniqueness claim and
the energy-descent identity (`prop:closure`, under
`AflbLean.Legacy.Imported`); the falsification/reconstruction program
(`obl:falsification`, `def:reconstruction`).

This is not a claim that the physics is correct. It is a claim that the
named deductive steps above are gap-free given the stated axioms. See
`docs/CLAIM_INVENTORY.md`, `docs/AXIOM_LEDGER.md`, `docs/BUILD_REPORT.md`,
`docs/FORMALIZATION_SCOPE.md`, `docs/axioms.txt` for the full accounting.
