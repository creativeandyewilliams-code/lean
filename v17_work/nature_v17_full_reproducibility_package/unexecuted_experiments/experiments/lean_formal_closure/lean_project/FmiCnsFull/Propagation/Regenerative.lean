import Mathlib

namespace FmiCnsFull

/-- Stagewise regenerative propagation. -/
structure RegenerationStages where
  exposure : Prop
  registration : Prop
  reconstruction : Prop
  hiddenExecution : Prop
  retransmission : Prop
  secondReceiverSuccess : Prop

/-- Regeneration requires the entire cascade rather than exposure or agreement
    alone. -/
def Regenerates (S : RegenerationStages) : Prop :=
  S.exposure ∧ S.registration ∧ S.reconstruction ∧ S.hiddenExecution ∧
  S.retransmission ∧ S.secondReceiverSuccess

/-- Deterministic cascade theorem. -/
theorem regenerationOfStages (S : RegenerationStages)
    (h1 : S.exposure) (h2 : S.registration)
    (h3 : S.reconstruction) (h4 : S.hiddenExecution)
    (h5 : S.retransmission) (h6 : S.secondReceiverSuccess) :
    Regenerates S :=
  ⟨h1, h2, h3, h4, h5, h6⟩

/-- T-REGENERATIVE-THRESHOLD, bounded independent-stage form.  If every stage
    succeeds with probability at least `p`, the six-stage chain succeeds with
    probability at least `p^6` under the declared multiplicative model. -/
theorem regenerativeThreshold
    (p exposure registration reconstruction execution retransmission second : ℝ)
    (hp : 0 ≤ p)
    (h1 : p ≤ exposure) (h2 : p ≤ registration)
    (h3 : p ≤ reconstruction) (h4 : p ≤ execution)
    (h5 : p ≤ retransmission) (h6 : p ≤ second) :
    p ^ 6 ≤ exposure * registration * reconstruction * execution * retransmission * second := by
  calc
    p ^ 6 = p * p * p * p * p * p := by ring
    _ ≤ exposure * registration * reconstruction * execution * retransmission * second := by
      gcongr

end FmiCnsFull
