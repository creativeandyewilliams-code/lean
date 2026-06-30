/-
Named axioms for [hyp]-tagged physics posits, v50 target list (Bucket C).
These are NOT proved. They are declared so downstream theorems can be
audited (via `#print axioms`) for exactly which physics posits they use.
Source: antigravity_secondorder_supplement_v50_AFLB.tex
-/

namespace AflbLean.Posits

/--
**Primitive counterposition and intrinsic pair resolution.**
The physical branch of a counterposed pair is decided in P-space by an
intrinsic transport-relative pair-resolution map, not by an observer.
Declared [hyp]; defeater: a branch outcome shown to depend on detector choice.
Source: supplement hyp:pair-resolution (line 231).
-/
axiom pairResolution : Prop
axiom pairResolution_holds : pairResolution

/--
**Physical operativity through endogenous closure.**
A candidate becomes physically/registrationally consequential only if it is
admitted on its own closed viability-bearing operand. An ontic hypothesis of
the proposed second-order theory; not a consequence of the fixed-point
closure theorem.
Declared [hyp, ontic]; defeater: a physically consequential candidate that
fails its own closed admissibility test.
Source: supplement hyp:ossv5-physical-operativity (line 711).
-/
axiom physicalOperativity : Prop
axiom physicalOperativity_holds : physicalOperativity

end AflbLean.Posits
