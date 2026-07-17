import FmiCnsFull.Projection.Conflation

namespace FmiCnsFull

/-- Centralized uncheckability: a center using a target distinction that does
    not factor through the participant signal cannot be universally checked by
    a participant restricted to that signal. -/
theorem centralizedUncheckability
    {World Signal Verdict : Type*}
    (q : World → Signal) (φ : World → Verdict)
    {x y : World} (hcollapsed : q x = q y)
    (hseparated : φ x ≠ φ y) :
    ¬ FactorsThrough q φ := by
  exact firstOrderConflation q φ hcollapsed hseparated

end FmiCnsFull
