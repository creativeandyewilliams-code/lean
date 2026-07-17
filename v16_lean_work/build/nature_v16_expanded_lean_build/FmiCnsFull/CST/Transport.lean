import Mathlib

namespace FmiCnsFull

/-- A discrete semantic transport step. -/
structure TransportStep (State : Type*) where
  map : State → State

/-- A path is a finite sequence of transport steps. -/
abbrev SemanticPath (State : Type*) := List (TransportStep State)

/-- Path transport, composed in path order. -/
def pathTransport {State : Type*} : SemanticPath State → State → State
  | [], x => x
  | s :: rest, x => pathTransport rest (s.map x)

/-- Two derivation paths are admissibly equivalent when their transport maps
    agree on every semantic state. -/
def PathEquivalent {State : Type*}
    (p q : SemanticPath State) : Prop :=
  ∀ x, pathTransport p x = pathTransport q x

/-- T-HOL-INVARIANCE.  Equivalent paths transport every semantic object to the
    same result. -/
theorem holonomyInvariance
    {State : Type*} {p q : SemanticPath State}
    (h : PathEquivalent p q) :
    ∀ x, pathTransport p x = pathTransport q x :=
  h

/-- A closed loop is semantically trivial when every state returns unchanged. -/
def TrivialHolonomy {State : Type*} (loop : SemanticPath State) : Prop :=
  ∀ x, pathTransport loop x = x

/-- T-HOL-DRIFT.  A registered state changed by a closed derivation loop is a
    constructive semantic-drift witness. -/
theorem holonomyDrift
    {State : Type*} (loop : SemanticPath State) (x : State)
    (h : pathTransport loop x ≠ x) :
    ¬ TrivialHolonomy loop := by
  intro htrivial
  exact h (htrivial x)

/-- Transport respects path concatenation. -/
theorem pathTransport_append
    {State : Type*} (p q : SemanticPath State) (x : State) :
    pathTransport (p ++ q) x = pathTransport q (pathTransport p x) := by
  induction p generalizing x with
  | nil => simp [pathTransport]
  | cons s p ih => simp [pathTransport, ih]

end FmiCnsFull
