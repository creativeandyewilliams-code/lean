import Mathlib

namespace FmiCnsFull

/-- A finite registered family of canonical functional-equivalence-class IDs.
    Each member is separately certified as registered, reusable, nonredundant,
    and spanning by `qualifies`. -/
structure OrderCertificate (ClassId : Type*) [DecidableEq ClassId] where
  classes : Finset ClassId
  qualifies : ClassId → Prop
  all_qualify : ∀ c ∈ classes, qualifies c

/-- Canonical cognitive order represented by a complete class certificate. -/
def CognitiveOrder {ClassId : Type*} [DecidableEq ClassId]
    (C : OrderCertificate ClassId) : ℕ :=
  C.classes.card

/-- Transport a class certificate through a genuine equivalence.  Unlike the
    v16 list-map witness, the map is injective and therefore represents a
    bijection on functional-equivalence classes. -/
def OrderCertificate.transport
    {A B : Type*} [DecidableEq A] [DecidableEq B]
    (e : A ≃ B) (C : OrderCertificate A)
    (qualifiesB : B → Prop)
    (hqual : ∀ a, C.qualifies a ↔ qualifiesB (e a)) :
    OrderCertificate B where
  classes := C.classes.map e.toEmbedding
  qualifies := qualifiesB
  all_qualify := by
    intro b hb
    rcases Finset.mem_map.mp hb with ⟨a, ha, rfl⟩
    exact (hqual a).mp (C.all_qualify a ha)

/-- T-ORDER-INVARIANCE.  Admissible relabelling by an equivalence preserves
    the cardinality of qualifying composition classes. -/
theorem orderInvariance
    {A B : Type*} [DecidableEq A] [DecidableEq B]
    (e : A ≃ B) (C : OrderCertificate A)
    (qualifiesB : B → Prop)
    (hqual : ∀ a, C.qualifies a ↔ qualifiesB (e a)) :
    CognitiveOrder (C.transport e qualifiesB hqual) = CognitiveOrder C := by
  simp [CognitiveOrder, OrderCertificate.transport]

/-- L-ORDER-INCREMENT.  Adding a fresh qualifying class increments the order
    by one.  This lemma is explicitly definitional and is not the complete CNS
    theorem. -/
theorem orderIncrement
    {A : Type*} [DecidableEq A]
    (C : OrderCertificate A) (g : A) (hg : g ∉ C.classes)
    (hgqual : C.qualifies g) :
    (Finset.insert g C.classes).card = CognitiveOrder C + 1 := by
  simpa [CognitiveOrder, Finset.card_insert_of_not_mem hg, Nat.add_comm]

/-- Observable equivalence of two compositions on a finite admissible domain. -/
def functionallyEquivalentB
    {X Y Z : Type*} [DecidableEq Z]
    (domain : Finset X) (obs : Y → Z) (f g : X → Y) : Bool :=
  domain.all (fun x => decide (obs (f x) = obs (g x)))

/-- Propositional wrapper for the executable finite equivalence test. -/
def FunctionallyEquivalentFinite
    {X Y Z : Type*} [DecidableEq Z]
    (domain : Finset X) (obs : Y → Z) (f g : X → Y) : Prop :=
  functionallyEquivalentB domain obs f g = true

instance functionallyEquivalentFiniteDecidable
    {X Y Z : Type*} [DecidableEq Z]
    (domain : Finset X) (obs : Y → Z) (f g : X → Y) :
    Decidable (FunctionallyEquivalentFinite domain obs f g) :=
  inferInstance

end FmiCnsFull
