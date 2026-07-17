import Mathlib

namespace FmiCnsFull

/-- Participant-indexed current, target, and projected fitness. -/
structure FitnessTriple (Action : Type*) where
  current : ℝ
  target : ℝ
  projected : Action → ℝ

/-- The three pairwise differences used by the FMI internal control basis. -/
def fitnessDifferences {Action : Type*} (F : FitnessTriple Action)
    (a : Action) : ℝ × ℝ × ℝ :=
  (F.target - F.current,
   F.projected a - F.current,
   F.target - F.projected a)

/-- Choice selects among external-function invocations.  Choice depth is kept
    as a separate control-complexity quantity and is not identified with
    cognitive order. -/
structure ChoicePolicy (State Action : Type*) where
  choose : State → List Action → Option Action
  depth : ℕ

end FmiCnsFull
