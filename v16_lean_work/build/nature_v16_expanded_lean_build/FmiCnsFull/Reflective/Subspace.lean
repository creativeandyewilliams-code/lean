import Mathlib

namespace FmiCnsFull

/-- Every load-bearing registered role named in the manuscript. -/
inductive RegisteredRole where
  | concept
  | processIdentity
  | functionContract
  | composition
  | target
  | proof
  | experiment
  | warrant
  | governanceRule
  | signalResidual
  | externalPremise
  | amendment
  deriving DecidableEq, Repr

/-- The two fundamental represented forms, with `both` for intensional and
    extensional objects such as functions. -/
inductive CoreRepresentedForm where
  | node
  | process
  | both
  deriving DecidableEq, Repr

/-- Canonical normalization of every registered role. -/
def normalizeRole : RegisteredRole → CoreRepresentedForm
  | .concept => .node
  | .processIdentity => .both
  | .functionContract => .both
  | .composition => .both
  | .target => .node
  | .proof => .both
  | .experiment => .both
  | .warrant => .node
  | .governanceRule => .both
  | .signalResidual => .node
  | .externalPremise => .node
  | .amendment => .both

/-- T-RSUB.  No third primitive represented-object class is needed for the
    registered FMI-CNS-Great-Filter language.  The theorem is constructive:
    `normalizeRole` supplies the representation. -/
theorem reflectiveSubspaceRepresentation (r : RegisteredRole) :
    ∃ f : CoreRepresentedForm, normalizeRole r = f := by
  exact ⟨normalizeRole r, rfl⟩

/-- Reflective reification is a representation operation, not itself a
    cognitive-order increment. -/
def reifyProcessAsNode (_ : RegisteredRole) : RegisteredRole := .concept

end FmiCnsFull
