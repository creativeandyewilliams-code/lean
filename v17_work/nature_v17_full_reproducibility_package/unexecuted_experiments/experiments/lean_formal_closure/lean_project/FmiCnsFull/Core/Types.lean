import Mathlib

namespace FmiCnsFull

universe u v

/-- Canonical node roles.  A represented object may carry more than one role,
    but these tags are sufficient for the registered language used below. -/
inductive NodeKind where
  | concept
  | functionContract
  | claim
  | premise
  | target
  | certificate
  | observation
  | dataset
  | protocol
  | manuscriptPassage
  deriving DecidableEq, Repr

/-- Canonical process and interaction roles. -/
inductive EdgeKind where
  | define
  | infer
  | execute
  | register
  | express
  | store
  | recall
  | localTransform
  | globalTransform
  | certify
  | govern
  | transmit
  | amend
  deriving DecidableEq, Repr

/-- Boundary, warrant, continuation, and participant-fitness data carried by an
    FSS.  These predicates are intentionally mathematical fields rather than
    global axioms. -/
structure BoundaryRecord (V : Type u) where
  admissible : V → Prop
  certified : V → Prop
  warranted : V → Prop
  continues : V → Prop
  fitness : V → ℝ

/-- A typed metric functional state space.  The metric axioms are included
    explicitly so that semantic equivalence can preserve the actual relational
    object rather than merely labels. -/
structure TypedFSS where
  V : Type u
  E : Type v
  nodeKind : V → NodeKind
  edgeKind : E → EdgeKind
  src : E → V
  dst : E → V
  dist : V → V → ℝ
  dist_nonneg : ∀ x y, 0 ≤ dist x y
  dist_self : ∀ x, dist x x = 0
  dist_symm : ∀ x y, dist x y = dist y x
  dist_triangle : ∀ x y z, dist x z ≤ dist x y + dist y z
  boundary : BoundaryRecord V

/-- A pointed FSS is the semantic profile of one represented state. -/
structure PointedFSS where
  space : TypedFSS
  point : space.V

/-- A target is any proposition evaluated on a pointed FSS.  The registered
    language in `Semantics.lean` supplies a syntactic subclass for which
    invariance is proved by structural induction. -/
abbrev Target (P : PointedFSS) := Prop

/-- Structural equality of participant-indexed consequences is part of
    semantic preservation whenever fitness is target-relevant. -/
def FitnessEquivalent {X Y : TypedFSS} (f : X.V → Y.V) : Prop :=
  ∀ x, Y.boundary.fitness (f x) = X.boundary.fitness x

end FmiCnsFull
