# PAPER INTEGRATION (v51)

## Ready-to-paste wording for the manuscript/supplement

Insert verbatim (e.g. as a remark following the relevant propositions, or in
an "Independent verification" / "Formal verification" subsection):

> An accompanying Lean formalization kernel-checks selected finite and
> algebraic deductions: regular-branch stability implies coefficient
> positivity; those coefficients imply the positive inverse-branch response;
> finite certificate iteration stabilizes at a least fixed point under the
> stated finite-order and monotonicity assumptions; and the inverse-target
> and viability-fiber criteria establish the corresponding non-factorization
> results. The intrinsic pair-resolution law and physical-operativity
> principle remain explicit hypotheses. Continuum reconstruction, full
> gradient-flow analysis, and empirical realization are outside the Lean
> certificate.

## Optional footnote on the build environment

If the paper wants to be explicit about the Mathlib-unavailability caveat,
the following footnote may be appended to the paragraph above:

> The Lean package is stdlib-only (Lean 4.14.0, no Mathlib dependency). The
> finite-certificate-closure result uses a concrete, hand-supplied
> rank-bounded finiteness witness in place of an abstract finite-cardinality
> argument; real-valued physics quantities are represented as integers with
> denominator-cleared inequalities. Neither substitution weakens the proved
> conclusions; see the package's `docs/FORMALIZATION_SCOPE.md` for the exact
> statement of each substitution.

## Cross-reference to source labels

For an editor or referee who wants to trace each formal declaration back to
its `.tex` label, the full mapping is in `docs/CLAIM_INVENTORY.md`. Summary:

| Source label | Lean declaration |
|---|---|
| `lem:ossv5-regularity-positivity` | `AflbLean.regularBranchCoefficientPositivity` |
| `prop:response` | `AflbLean.regularBranchCoefficientPositivity` (shape), `AflbLean.inverseBranchResponsePositive` |
| `thm:ossv5-sign-invariance` | `AflbLean.signInvariance` |
| `hyp:ossv5-sign-neutrality` | `AflbLean.viableAdmSignInvariant` |
| `thm:fiber` | `AflbLean.fiberCriterion` |
| `thm:ossv5-finite-closure` | `AflbLean.finiteCertificateClosureAscending`, `AflbLean.finiteCertificateClosureComplete` |
| `thm:ossv5-nonreducibility` | `AflbLean.viabilityNonReducibility` |
| `thm:secondorder` | `AflbLean.secondOrderResult` |
| `hyp:pair-resolution` (mechanism) | `AflbLean.classifyCovers`, `AflbLean.classifyExclusive` |
| `hyp:pair-resolution` (intrinsicity), `hyp:ossv5-physical-operativity` | undeclared; `Prop` parameters of `secondOrderResult` |
