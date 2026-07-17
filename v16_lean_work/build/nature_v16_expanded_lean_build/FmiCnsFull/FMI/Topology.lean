import Mathlib

namespace FmiCnsFull

/-- Two contexts agree on a declared support. -/
def AgreeOn {V State : Type*} (S : Set V)
    (c₁ c₂ : V → State) : Prop :=
  ∀ v ∈ S, c₁ v = c₂ v

/-- The output of an operation is determined by support `S`. -/
def DeterminedBy {V State Out : Type*} (S : Set V)
    (op : (V → State) → Out) : Prop :=
  ∀ c₁ c₂, AgreeOn S c₁ c₂ → op c₁ = op c₂

/-- Local support means that one declared interaction neighbourhood determines
    the target-relevant output. -/
def LocalSupport {V State Out : Type*} (neighbourhoods : Set (Set V))
    (op : (V → State) → Out) : Prop :=
  ∃ S, S ∈ neighbourhoods ∧ DeterminedBy S op

/-- Global support means that every declared local neighbourhood admits a
    target-relevant remote-context witness changing the output. -/
def GlobalSupport {V State Out : Type*} (neighbourhoods : Set (Set V))
    (op : (V → State) → Out) : Prop :=
  ∀ S, S ∈ neighbourhoods → ¬ DeterminedBy S op

/-- Local and global support are incompatible relative to the same target and
    neighbourhood family. -/
theorem globalSupport_not_local {V State Out : Type*}
    (N : Set (Set V)) (op : (V → State) → Out) :
    GlobalSupport N op → ¬ LocalSupport N op := by
  intro hg hl
  rcases hl with ⟨S, hSN, hdet⟩
  exact hg S hSN hdet

/-- Parallel schedule is target-equivalence commutation. -/
def ParallelSchedule {X : Type*} (f g : X → X) : Prop :=
  Function.Commute f g

/-- Sequential schedule records a load-bearing failure of commutation. -/
def SequentialSchedule {X : Type*} (f g : X → X) : Prop :=
  ¬ Function.Commute f g

/-- The operation relation generates reachability by reflexive-transitive
    closure; topology is therefore induced by admissible transitions. -/
def OperationReachable {V : Type*} (R : V → V → Prop) : V → V → Prop :=
  Relation.ReflTransGen R

/-- Every primitive transition is reachable in the induced topology. -/
theorem transition_is_reachable {V : Type*} (R : V → V → Prop)
    {x y : V} (h : R x y) : OperationReachable R x y := by
  exact Relation.ReflTransGen.single h

end FmiCnsFull
