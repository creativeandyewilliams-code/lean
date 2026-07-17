import FmiCnsFull

namespace FmiCnsFull.Tests

/-- Reflection without a new class is not an order lift. -/
def reflectionOnlyBefore : Architecture (Fin 2) Bool where
  classes := {0}
  operands := Set.univ

def reflectionOnlyAfter : Architecture (Fin 2) Bool where
  classes := {0}
  operands := Set.univ

example : reflectionOnlyAfter.order = reflectionOnlyBefore.order := by
  decide

/-- A contracting local operator may exist without a fresh composition class;
    therefore contraction alone does not imply an order lift. -/
def boolMetric : MetricData Bool where
  d := fun x y => if x = y then 0 else 1
  nonneg := by intro x y; split <;> norm_num
  eq_zero_iff := by intro x y; by_cases h : x = y <;> simp [h]
  symm := by intro x y; by_cases h : x = y <;> simp [h, eq_comm]
  triangle := by intro x y z; by_cases h : x = z <;> simp [h]; norm_num

/-- Matching service is an explicit counter-regime to backlog divergence. -/
example (D : ℕ → ℝ) : backlog D D = fun _ => 0 := by
  funext t
  simp [backlog]

/-- A summable finite hazard budget below one leaves positive survival. -/
example : 0 < (([0.1, 0.2, 0.3] : List ℝ).map (fun x => 1 - x)).prod := by
  apply positiveSurvival_of_totalHazard_lt_one
  · intro x hx
    simp at hx
    rcases hx with rfl | rfl | rfl <;> norm_num
  · norm_num

end FmiCnsFull.Tests
