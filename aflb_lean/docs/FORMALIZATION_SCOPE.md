# FORMALIZATION SCOPE (v51)

This document lists, explicitly and exhaustively, what is **not** formalized
in this package, and why — so that nobody mistakes the headline build for a
broader certificate than it is.

## Outside formal scope entirely (Bucket D)

- **Continuum/gradient-flow analysis** (`prop:closure`: global existence and
  uniqueness of the gradient flow, the energy-descent identity). This
  requires real analysis (`deriv`/`HasDerivAt`, ODE existence theory) that
  is supplied by Mathlib and not available in this build. Declared as named
  axioms `Legacy.Imported.odeGlobalExistence` / `Legacy.Imported.energyDescentIdentity`,
  retained only as a ledger entry — used by no theorem reachable from the
  headline root.
- **Empirical/falsification claims** (`obl:falsification`). Inherently
  outside the scope of a Lean kernel check.
- **The reconstruction program** (`def:reconstruction`), marked [open] in
  the source. No closed formal statement exists to formalize.

## Removed claims (had a v50 Lean declaration; v51 removes it)

Both of these were judged, on direct inspection, to contain no honest
non-vacuous Lean content — keeping a theorem-shaped placeholder would be
worse than removing it, per this package's non-vacuity discipline ("a
smaller package containing exact, non-vacuous theorems is better than a
larger package containing placeholders, unused axioms, or theorem-shaped
tautologies").

- **`thm:ossv5-endogenous-admissibility`.** v50's
  `Closure.endogenousAdmissibility` proved `P ↔ P` via `Iff.rfl` — a
  tautology of its own statement, not a substantive deduction. No
  non-vacuous, stdlib-only Lean content was found for the underlying claim
  within this build's scope.
- **`prop:schedule`.** v50's `ScheduleReaches`/`InverseBranchMembership`/
  `scheduleRealizesInverse` were effectively `True`, proved by `trivial`.
  No non-vacuous stdlib-only formalization of the schedule-reachability
  claim was found.

If either claim is to be formalized honestly in a future revision, it needs
either (a) a genuinely nontrivial closed-form statement supplied by the
paper authors, or (b) Mathlib's order/lattice-fixed-point or dynamical-
systems machinery, neither of which was available within this build's
constraints.

## Named, undischarged physics posits (Bucket C — by design, never proved)

These are not formalization gaps; they are exactly the claims the source
itself marks [hyp] and never proves. v51 represents them in the most honest
way available: as bare `Prop` parameters threaded into the one theorem that
needs them (`SecondOrder.secondOrderResult`), rather than as global axioms
that would manufacture a proof inhabitant out of an assertion. See
`AXIOM_LEDGER.md`.

- The "this threshold rule is the physically intrinsic one, not
  detector-dependent" half of `hyp:pair-resolution`.
- `hyp:ossv5-physical-operativity`.
- The legacy registration-layer hypotheses `prop:shared-basis`,
  `prop:sync-residue`, `def:operation-basis`/`prop:smallest-scale` (kept as
  named axioms under `AflbLean.Legacy.Hypotheses`, non-headline).

## Mathlib-dependent substitutions (downgrades, not omissions)

Mathlib is confirmed unreachable in this build environment (network/proxy
restricted to the four `creativeandyewilliams-code` repos; verified by
direct `git ls-remote` failures against both `github.com/leanprover-community/mathlib4`
and `release.lean-lang.org`, returning HTTP 403). Two places in the source
mathematics would naturally use Mathlib machinery; both are represented with
honest stdlib-only substitutes rather than skipped or faked:

1. **Real-valued physics quantities** are modeled with `Int` plus
   denominator-cleared inequalities, since `Real`/`Rat` and tactics like
   `positivity`/`linarith`/`nlinarith` are Mathlib-only. Every denominator
   appearing in the source is provably positive at the points considered, so
   clearing it never changes a sign conclusion.
2. **Finite-lattice stabilization** (`thm:ossv5-finite-closure`) is proved
   using a concrete, hand-rolled `rank`-based `FiniteWitness` structure
   instead of Mathlib's `Fintype`/`PartialOrder`/`OrderBot`/`Monotone`
   instances. The caller must supply a concrete witness with the four
   governing properties (`rank_bot`, `rank_mono`, `rank_strict`,
   `rank_bound`); the theorem then derives the same stabilization-at-`n≤N`
   and least-fixed-point conclusions a `Fintype`-based argument would, via a
   genuine pigeonhole/rank-growth proof, not by assumption.

Neither substitution weakens what is *proved* about the structures supplied;
it changes only how the "this structure is finite" / "these are real
numbers" facts are packaged as hypotheses, in a way that is visible in each
theorem's own signature.
