# BUILD REPORT (v50)

## Toolchain

| Item | Value |
|---|---|
| Lean version | 4.14.0 (x86_64-unknown-linux-gnu, commit 410fab728470, Release) |
| Lake version | 5.0.0-410fab7 (Lean version 4.14.0) |
| Mathlib | **Not used.** Stdlib-only build. `lake exe cache get` and `git ls-remote` of `mathlib4` both fail in this sandbox (network/proxy restricted to the four `creativeandyewilliams-code` repos); this matches the v47 build and is unchanged. |
| `lake-manifest.json` | Zero pinned packages (unchanged). |

## Build

- `lake exe cache get || true` — no-op (no Mathlib dependency declared, so nothing to fetch).
- `lake build AflbLean 2>&1 | tee docs/build.log` — exit code 0. See `docs/build.log`.
- `bash scripts/check_no_sorry.sh` — `OK: no sorry in sources or build log.`
- Only cosmetic linter warnings remain (3 unused-argument warnings in `SecondOrder.lean`, of the same kind already present and accepted in the v47 build's `Conditional.lean`).

## §5 audit table — required facts

| Fact | Status |
|---|---|
| (1) Determination theorems (`inverseBranchResponsePositive`, `regularBranchCoefficientPositivity`, `signInvariance`, `fiberCriterion`, `finiteCertificateClosure`, `viabilityNonReducibility`) depend on core axioms only | **Confirmed.** Per `docs/axioms.txt`: all six show only `propext`/`Quot.sound` or no axioms at all. None depends on `Posits.physicalOperativity` or `Posits.pairResolution`. |
| (2) `physicalOperativity` appears in the cone of no Bucket-A theorem | **Confirmed.** `physicalOperativity` appears only in its own `#print axioms` line (self-referential, as expected of any axiom). |
| `pairResolution` used only where branch typing is claimed | **Confirmed.** `pairResolution`/`pairResolution_holds` appear only in `secondOrderResult`'s cone (Bucket B, item 2 of `thm:secondorder`). |

Full posit-to-theorem map: see `docs/AXIOM_LEDGER.md`.

## Downgrade log (relative to the literal v50 mathematics)

1. **No Mathlib ⇒ `Real`/`Rat` unavailable.** Verified empirically: `Rat` is
   an unknown identifier and `positivity`/`linarith`/`nlinarith` are unknown
   tactics in plain Lean 4.14.0 core. All real-valued physics quantities
   (α_e, γ_e, λ_e, r_e) are modeled with `Int`, and every inequality
   involving a denominator (`r_e`, `r_e^3`, `r_e^4`) is stated in its
   denominator-cleared form. Since every concrete denominator appearing in
   the source is provably positive, clearing it never changes a sign
   conclusion; this is a representational downgrade, not a mathematical
   shortcut. Precedent: this mirrors the v47 build's
   `GainBound.finiteTargetGain_real` axiomatization-under-Mathlib-absence
   pattern, generalized to the new physics layer.
2. **`thm:ossv5-finite-closure` stabilization half scoped out.** The
   ascending-chain half of the theorem (`Closure.ascendingKleeneSeq`) is
   proved in full by induction + monotonicity, exactly mirroring the source
   proof. The companion claim — that a strictly ascending chain in a
   *finite* lattice has at most `|V|-1` strict increases, hence
   stabilizes — rests on a `Fintype`/cardinality argument that needs more
   of Mathlib's finite-order machinery than is convenient to hand-roll from
   Lean 4 core alone within this build's scope. It is documented here as an
   open item rather than silently assumed; `Closure.kleeneSeq_le_fixedPoint`
   (least-fixed-point-below-every-fixed-point) is proved separately and
   does not depend on the stabilization claim.
3. **`prop:closure` analytic content axiomatized, not proved.** Both the
   gradient-flow global-existence/uniqueness claim and the algebraic
   descent identity require either real analysis or a calculus of
   `deriv`/`HasDerivAt` on a product manifold, both supplied by Mathlib.
   Declared as `Imported.odeGlobalExistence` ([imported]) and
   `Imported.energyDescentIdentity` ([requires-mathlib]) respectively;
   neither is used by, nor a hypothesis of, any proved theorem in this
   package.
4. **Legacy registration-layer module (`Hypotheses.lean`, `Conditional.lean`)
   retained, not rebuilt.** `prop:shared-basis`, `prop:sync-residue`,
   `def:operation-basis`, `prop:smallest-scale` are unchanged labels in v50
   main; the v47-era axioms/theorems for them are retargeted (headers and
   source-line references updated to v50) but not otherwise altered.
5. **Tautological lemma removed.** `Conditional.secondOrderObservability`
   was re-inspected during retargeting and found to prove `X = X` (`rfl`)
   despite a non-trivial-looking hypothesis list; it has been deleted along
   with the other v47-era vacuous placeholders. See `CLAIM_INVENTORY.md`.
6. **Unrelated v47 modules removed.** `Core.lean`, `NonReducibility.lean`,
   `GhzSupport.lean`, `GainBound.lean`, `Rendering.lean`,
   `StrictSeparation.lean`, and `Assumptions.lean` formalized claims (GHZ
   support cardinality, finite-target gain, 2D/3D rendering dimension,
   four-coordinate witness non-reducibility, shock-wave/Jeans gain) whose
   labels do not appear anywhere in either v50 `.tex` source file (checked
   by direct grep). They are out of scope for this v50 package and have
   been deleted rather than retargeted, since retargeting headers to v50
   while keeping content with no v50 counterpart would misrepresent what
   the certificate covers.

## Module map

| File | v50 content | Bucket |
|---|---|---|
| `Posits.lean` | `pairResolution`, `physicalOperativity` | C (axiom) |
| `Physics.lean` | character facts, attractive/inverse response, KEYSTONE coefficient positivity, sign invariance | A |
| `Closure.lean` | ascending Kleene sequence, least-fixed-point bound, endogenous admissibility, viability non-reducibility | A |
| `Fiber.lean` | fiber criterion for the inverse branch (`thm:fiber`) | A |
| `SecondOrder.lean` | `thm:secondorder`, `prop:schedule` | B |
| `Imported.lean` | `odeGlobalExistence`, `energyDescentIdentity` | D (axiom, ledger only) |
| `Hypotheses.lean`, `Conditional.lean` | legacy registration layer (`prop:shared-basis`, `prop:sync-residue`) | C |
