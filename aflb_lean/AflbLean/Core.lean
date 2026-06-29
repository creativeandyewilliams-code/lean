/-
Formalizes: shared definitions used across all modules
Source: antigravity_secondorder_supplement_v47_AFLB.tex, §"Four-Coordinate Witness Family"
Bucket: A (definitions only; used by NonReducibility, StrictSeparation, etc.)
-/

namespace AflbLean

/-!
## Corridor Witness Coordinates

A witness record 𝔠_{brhs} is characterised by four binary coordinates:
  b — bridge legality (1 = typed bridge licensed, 0 = unlicensed substitution)
  r — regime validity  (1 = inside declared regime, 0 = regime left)
  h — history/ordering (1 = ordered path with retention, 0 = unordered ledger)
  s — support/global invariant (1 = full support attained, 0 = proper-support proxy)

Source: supplement §"Four-Coordinate Witness Family", eq. Corr(𝔠_{brhs}) = b ∧ r ∧ h ∧ s
-/

structure WitnessCoords where
  bridge  : Bool
  regime  : Bool
  history : Bool
  support : Bool
  deriving DecidableEq, Repr

/-- The corridor predicate: open iff all four coordinates are true. -/
def corridor (w : WitnessCoords) : Bool :=
  w.bridge && w.regime && w.history && w.support

/-- Full open corridor: all four coordinates satisfied. -/
def 𝔠_1111 : WitnessCoords := ⟨true,  true,  true,  true⟩
/-- Bridge blocked, rest satisfied. -/
def 𝔠_0111 : WitnessCoords := ⟨false, true,  true,  true⟩
/-- Regime invalid, rest satisfied. -/
def 𝔠_1011 : WitnessCoords := ⟨true,  false, true,  true⟩
/-- History/ordering broken, rest satisfied. -/
def 𝔠_1101 : WitnessCoords := ⟨true,  true,  false, true⟩
/-- Support incomplete, rest satisfied. -/
def 𝔠_1110 : WitnessCoords := ⟨true,  true,  true,  false⟩

/-- Computed corridor values (verified by the kernel at elaboration time). -/
theorem corridor_1111 : corridor 𝔠_1111 = true  := rfl
theorem corridor_0111 : corridor 𝔠_0111 = false := rfl
theorem corridor_1011 : corridor 𝔠_1011 = false := rfl
theorem corridor_1101 : corridor 𝔠_1101 = false := rfl
theorem corridor_1110 : corridor 𝔠_1110 = false := rfl

/-- The fiber of q over z. -/
def fiber {Q : Type} [DecidableEq Q] (q : WitnessCoords → Q) (z : Q) : List WitnessCoords :=
  [𝔠_1111, 𝔠_0111, 𝔠_1011, 𝔠_1101, 𝔠_1110].filter (fun w => q w == z)

/-- c and d are locally equivalent under q iff q maps them to the same value. -/
def locallyEquivalent {Q : Type} (q : WitnessCoords → Q) (c d : WitnessCoords) : Prop :=
  q c = q d

end AflbLean
