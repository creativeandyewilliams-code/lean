/-
Bucket D: [imported]/[emp]/[open] claims, ledger only. These axioms are
declared so they can be named and audited; they are never used as a
hypothesis of, nor invoked to prove, any Bucket-A determination theorem.
Source: antigravity_secondorder_supplement_v50_AFLB.tex, prop:closure
(lines 359-383), and §"Observable consequences and falsification route"
(sec:falsification, lines 1169-1199).
-/

namespace AflbLean.Legacy.Imported

/--
**Global existence and uniqueness of the gradient flow [imported, ODE theory].**
The source proof argues this from compactness of K and boundedness of the
energy away from r_e=0 via "standard ODE extension" — genuine analysis
beyond what this stdlib-only (no-Mathlib) build can reproduce. Declared as
an axiom rather than proved.
Defeater: an admissible datum and initial state for which the flow exits
`State_p` or fails to extend to all `t ≥ 0`.
Source: supplement prop:closure (lines 359-372).
-/
axiom odeGlobalExistence : Prop
axiom odeGlobalExistence_holds : odeGlobalExistence

/--
**Energy descent identity [requires-mathlib].**
`d/dt D_p(Flow_p(t,z0)) = -Σ‖grad D_p‖² ≤ 0` is, in the source, the
gradient-flow identity, algebraic given a calculus of `deriv`/`HasDerivAt`
on the manifold `K^V × K^{E^+} × (0,∞)^{E^+}`. Reproducing it requires
Mathlib's analysis library, unavailable in this stdlib-only build; declared
as an axiom rather than faithfully reproved or replaced by a substitute
argument.
Source: supplement eq:descent (line 365).
-/
axiom energyDescentIdentity : Prop
axiom energyDescentIdentity_holds : energyDescentIdentity

end AflbLean.Legacy.Imported
