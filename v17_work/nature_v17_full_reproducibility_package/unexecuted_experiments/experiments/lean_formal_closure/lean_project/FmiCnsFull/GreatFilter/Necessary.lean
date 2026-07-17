import Mathlib

namespace FmiCnsFull

/-- A declared Great-Filter target over lineages. -/
structure FilterModel (Lineage : Type*) where
  consequential : Lineage → Prop
  outcome : Lineage → Prop

/-- Sufficiency means every consequential lineage reaches the declared
    terminal or observability outcome. -/
def SufficientFilter {Lineage : Type*} (M : FilterModel Lineage) : Prop :=
  ∀ l, M.consequential l → M.outcome l

/-- Individually inspectable necessary-property flags. -/
structure GFConstraintFlags where
  upperTailSuppression : Prop
  branchClosure : Prop
  causalSelfInstantiation : Prop
  firstMoverConsistency : Prop
  substrateInvariance : Prop
  adaptiveNonEscapability : Prop
  outcomeTimescaleResidue : Prop

/-- Scientific bridge assumptions saying that failure of each named property
    supplies a consequential lineage that escapes the declared outcome.  These
    assumptions are explicit and can be challenged independently. -/
structure GFDefeatWitnesses
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags) where
  upperTail : ¬ F.upperTailSuppression →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  branch : ¬ F.branchClosure →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  causal : ¬ F.causalSelfInstantiation →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  firstMover : ¬ F.firstMoverConsistency →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  substrate : ¬ F.substrateInvariance →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  adaptation : ¬ F.adaptiveNonEscapability →
    ∃ l, M.consequential l ∧ ¬ M.outcome l
  outcome : ¬ F.outcomeTimescaleResidue →
    ∃ l, M.consequential l ∧ ¬ M.outcome l

private theorem propertyNecessary
    {Lineage : Type*} (M : FilterModel Lineage)
    (hsuff : SufficientFilter M) (P : Prop)
    (hw : ¬ P → ∃ l, M.consequential l ∧ ¬ M.outcome l) : P := by
  by_contra hP
  rcases hw hP with ⟨l, hc, hno⟩
  exact hno (hsuff l hc)

/-- L-GF-UPPER-TAIL. -/
theorem upperTailNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.upperTailSuppression :=
  propertyNecessary M hsuff F.upperTailSuppression W.upperTail

/-- L-GF-BRANCH. -/
theorem branchClosureNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.branchClosure :=
  propertyNecessary M hsuff F.branchClosure W.branch

/-- L-GF-CAUSAL. -/
theorem causalSelfInstantiationNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.causalSelfInstantiation :=
  propertyNecessary M hsuff F.causalSelfInstantiation W.causal

/-- L-GF-FIRST-MOVER. -/
theorem firstMoverNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.firstMoverConsistency :=
  propertyNecessary M hsuff F.firstMoverConsistency W.firstMover

/-- L-GF-SUBSTRATE. -/
theorem substrateInvarianceNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.substrateInvariance :=
  propertyNecessary M hsuff F.substrateInvariance W.substrate

/-- L-GF-ADAPT. -/
theorem adaptiveNonEscapabilityNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.adaptiveNonEscapability :=
  propertyNecessary M hsuff F.adaptiveNonEscapability W.adaptation

/-- L-GF-OUTCOME. -/
theorem outcomeTimescaleResidueNecessary
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.outcomeTimescaleResidue :=
  propertyNecessary M hsuff F.outcomeTimescaleResidue W.outcome

/-- T-GF-CONSTRAINT.  Sufficiency entails all seven properties whenever each
    failure has the registered escape witness. -/
theorem greatFilterConstraint
    {Lineage : Type*} (M : FilterModel Lineage) (F : GFConstraintFlags)
    (W : GFDefeatWitnesses M F) (hsuff : SufficientFilter M) :
    F.upperTailSuppression ∧ F.branchClosure ∧
    F.causalSelfInstantiation ∧ F.firstMoverConsistency ∧
    F.substrateInvariance ∧ F.adaptiveNonEscapability ∧
    F.outcomeTimescaleResidue := by
  exact ⟨upperTailNecessary M F W hsuff,
    branchClosureNecessary M F W hsuff,
    causalSelfInstantiationNecessary M F W hsuff,
    firstMoverNecessary M F W hsuff,
    substrateInvarianceNecessary M F W hsuff,
    adaptiveNonEscapabilityNecessary M F W hsuff,
    outcomeTimescaleResidueNecessary M F W hsuff⟩

/-- Independent opportunities with a fixed nonzero escape probability retain a
    positive finite-horizon no-escape probability, while each additional
    opportunity strictly reduces it. -/
def noEscapeProbability (p : ℝ) (n : ℕ) : ℝ :=
  (1 - p) ^ n

theorem noEscapeProbability_positive
    {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p < 1) (n : ℕ) :
    0 < noEscapeProbability p n := by
  unfold noEscapeProbability
  positivity

theorem noEscapeProbability_strictlyDecreases
    {p : ℝ} (hp : 0 < p) (hp1 : p < 1) (n : ℕ) :
    noEscapeProbability p (n + 1) < noEscapeProbability p n := by
  unfold noEscapeProbability
  rw [pow_succ]
  have hbase0 : 0 < 1 - p := by linarith
  have hbase1 : 1 - p < 1 := by linarith
  have hpow : 0 < (1 - p) ^ n := pow_pos hbase0 n
  nlinarith

private theorem listSum_nonneg
    (xs : List ℝ) (h : ∀ x ∈ xs, 0 ≤ x) : 0 ≤ xs.sum := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      have ha : 0 ≤ a := h a (by simp)
      have htail : ∀ x ∈ xs, 0 ≤ x := by
        intro x hx
        exact h x (by simp [hx])
      simp [ha, ih htail]

private theorem listProdOneSub_nonneg
    (xs : List ℝ) (h : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1) :
    0 ≤ (xs.map (fun x => 1 - x)).prod := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      have ha := h a (by simp)
      have htail : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1 := by
        intro x hx
        exact h x (by simp [hx])
      have hnonneg : 0 ≤ 1 - a := by linarith
      have hi := ih htail
      simpa using mul_nonneg hnonneg hi

/-- Finite survival lower bound: the product of one-minus-hazard terms is at
    least one minus the total hazard.  Hence a total finite hazard below one
    leaves strictly positive survival. -/
theorem oneSubSum_le_prodOneSub
    (xs : List ℝ) (h : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1) :
    1 - xs.sum ≤ (xs.map (fun x => 1 - x)).prod := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      have ha := h a (by simp)
      have htail : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1 := by
        intro x hx
        exact h x (by simp [hx])
      have hsum : 0 ≤ xs.sum :=
        listSum_nonneg xs (fun x hx => (htail x hx).1)
      have hleft : 1 - (a + xs.sum) ≤ (1 - a) * (1 - xs.sum) := by
        nlinarith
      have hmul := mul_le_mul_of_nonneg_left (ih htail) (by linarith [ha.2])
      calc
        1 - (a :: xs).sum = 1 - (a + xs.sum) := by simp
        _ ≤ (1 - a) * (1 - xs.sum) := hleft
        _ ≤ (1 - a) * (xs.map (fun x => 1 - x)).prod := hmul
        _ = ((a :: xs).map (fun x => 1 - x)).prod := by simp

/-- A finite hazard budget below one cannot produce certain failure. -/
theorem positiveSurvival_of_totalHazard_lt_one
    (xs : List ℝ) (h : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1)
    (hsum : xs.sum < 1) :
    0 < (xs.map (fun x => 1 - x)).prod := by
  have hbound := oneSubSum_le_prodOneSub xs h
  have hpositive : 0 < 1 - xs.sum := by linarith
  exact lt_of_lt_of_le hpositive hbound

end FmiCnsFull
