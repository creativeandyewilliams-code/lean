import Mathlib

namespace FmiCnsFull

/-- Four typed transmission residuals. -/
structure TransmissionResidual (Rreg Rexpr Rrecv Rrecon : Type*) where
  registration : Rreg
  expression : Rexpr
  reception : Rrecv
  reconstruction : Rrecon

/-- The residual is a product, not a scalar sum, so failure source and type are
    retained. -/
abbrev ResidualProduct (Rreg Rexpr Rrecv Rrecon : Type*) :=
  Rreg × Rexpr × Rrecv × Rrecon

/-- Register and Express are boundary maps and may be partial. -/
structure SignalBoundary (Signal Concept : Type*) where
  register : Signal → Option Concept
  express : Concept → Option Signal

end FmiCnsFull
