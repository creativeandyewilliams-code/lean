/-
Formalizes: prop:proper-support-indistinguishability, prop:strict-separation-witness,
            prop:no-local-decider
Source: antigravity_secondorder_supplement_v47_AFLB.tex
Bucket: A (finite combinatorics on Bool³; proved by decidable computation)
-/

import AflbLean.Core
import AflbLean.NonReducibility

namespace AflbLean.StrictSeparation

open AflbLean

def parity (a : Bool × Bool × Bool) : Bool := a.1 ^^ a.2.1 ^^ a.2.2

def evenParityStates : List (Bool × Bool × Bool) :=
  [(false, false, false), (false, true, true), (true, false, true), (true, true, false)]

def oddParityStates : List (Bool × Bool × Bool) :=
  [(false, false, true), (false, true, false), (true, false, false), (true, true, true)]

theorem evenParityStates_correct :
    evenParityStates.all (fun s => parity s == false) = true := rfl

theorem oddParityStates_correct :
    oddParityStates.all (fun s => parity s == true) = true := rfl

def proj1  (a : Bool × Bool × Bool) : Bool        := a.1
def proj2  (a : Bool × Bool × Bool) : Bool        := a.2.1
def proj3  (a : Bool × Bool × Bool) : Bool        := a.2.2
def proj12 (a : Bool × Bool × Bool) : Bool × Bool := (a.1, a.2.1)
def proj13 (a : Bool × Bool × Bool) : Bool × Bool := (a.1, a.2.2)
def proj23 (a : Bool × Bool × Bool) : Bool × Bool := (a.2.1, a.2.2)

/--
**Proper-Support Indistinguishability.**
ρ₀ (even parity) and ρ₁ (odd parity) are identical on all proper-subset marginals.
Source: supplement prop:proper-support-indistinguishability.
-/
theorem properSupportIndistinguishability :
    (∀ v : Bool,
      (evenParityStates.filter (fun s => proj1 s == v)).length =
      (oddParityStates.filter  (fun s => proj1 s == v)).length) ∧
    (∀ v : Bool,
      (evenParityStates.filter (fun s => proj2 s == v)).length =
      (oddParityStates.filter  (fun s => proj2 s == v)).length) ∧
    (∀ v : Bool,
      (evenParityStates.filter (fun s => proj3 s == v)).length =
      (oddParityStates.filter  (fun s => proj3 s == v)).length) ∧
    (∀ v1 v2 : Bool,
      (evenParityStates.filter (fun s => proj12 s == (v1, v2))).length =
      (oddParityStates.filter  (fun s => proj12 s == (v1, v2))).length) ∧
    (∀ v1 v2 : Bool,
      (evenParityStates.filter (fun s => proj13 s == (v1, v2))).length =
      (oddParityStates.filter  (fun s => proj13 s == (v1, v2))).length) ∧
    (∀ v1 v2 : Bool,
      (evenParityStates.filter (fun s => proj23 s == (v1, v2))).length =
      (oddParityStates.filter  (fun s => proj23 s == (v1, v2))).length) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro v; cases v <;> decide
  · intro v; cases v <;> decide
  · intro v; cases v <;> decide
  · intro v1 v2; cases v1 <;> cases v2 <;> decide
  · intro v1 v2; cases v1 <;> cases v2 <;> decide
  · intro v1 v2; cases v1 <;> cases v2 <;> decide

theorem globalParityDistinguishes :
    (evenParityStates.filter (fun s => parity s == false)).length = 4 ∧
    (oddParityStates.filter  (fun s => parity s == true)).length  = 4 ∧
    (evenParityStates.filter (fun s => parity s == true)).length  = 0 ∧
    (oddParityStates.filter  (fun s => parity s == false)).length = 0 := by
  decide

def 𝔠_open    : WitnessCoords := ⟨true,  true, true, true⟩
def 𝔠_blocked : WitnessCoords := ⟨false, true, true, true⟩

/--
**Strict Separation Witness.**
𝔠_open and 𝔠_blocked have different corridor values but are locally
indistinguishable under bridge-erasure.
Source: supplement prop:strict-separation-witness.
-/
theorem strictSeparationWitness :
    corridor 𝔠_open = true ∧
    corridor 𝔠_blocked = false ∧
    NonReducibility.dropBridge 𝔠_open = NonReducibility.dropBridge 𝔠_blocked := by
  simp [𝔠_open, 𝔠_blocked, corridor, NonReducibility.dropBridge]

/--
**No Local Decider.**
Any bridge-erasing procedure cannot be both sound and complete for corridor.
Source: supplement prop:no-local-decider.
-/
theorem noLocalDecider :
    ∀ (decide_corr : Bool × Bool × Bool → Bool),
      ¬ ∀ w : WitnessCoords, decide_corr (NonReducibility.dropBridge w) = corridor w := by
  intro d hd
  have hop := hd 𝔠_open
  have hbl := hd 𝔠_blocked
  have heq : NonReducibility.dropBridge 𝔠_open = NonReducibility.dropBridge 𝔠_blocked := by
    simp [𝔠_open, 𝔠_blocked, NonReducibility.dropBridge]
  rw [heq] at hop
  have hcorr_open    : corridor 𝔠_open    = true  := by simp [𝔠_open, corridor]
  have hcorr_blocked : corridor 𝔠_blocked = false := by simp [𝔠_blocked, corridor]
  rw [hcorr_open] at hop
  rw [hcorr_blocked] at hbl
  rw [hop] at hbl
  exact absurd hbl (by decide)

end AflbLean.StrictSeparation
