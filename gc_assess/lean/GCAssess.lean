/-
  GCAssess.lean
  Lean 4 formal companion for the HCFM global-coherence assessment verdict
  algebra. This is the artifact referenced by slot (L1) of the audit contract in
  "A Conditional Construction of Human-Centric Functional Modeling from Globally
  Lawful Material Flow" (main paper).

  SCOPE (slot L1, stated precisely).
  This development establishes that the DECISION SEMANTICS of the verdict algebra
  are internally consistent: the verdict lattice is a well-defined three-valued
  type; the recursive composition rule `combine` is total and associative on the
  two determinate verdicts; the incoherent short-circuit and the coherent /
  undetermined stopping conditions are exactly characterised; and the tree-level
  evaluator `evalTree` agrees with the fold defining the algebra. It does NOT
  formalise, and makes no claim about, the substantive per-node coherence
  judgment (slot B1): leaf verdicts are inputs to `evalTree`, exactly as they are
  oracle inputs to the Python reference implementation.

  All results below are proved over concrete decidable types (an inductive
  `Verdict` and `List`/`Tree` structures); there are NO `axiom`s and NO `sorry`.

  BUILD STATUS. This file is written against Lean 4 core + Std-style tactics and
  is intended to be checked with a pinned toolchain via `lake build`, with
  `#print axioms` confirming the theorems depend on no additional axioms beyond
  Lean's core. Until that kernel check is run in your environment, the paper
  should describe this as a Lean DEVELOPMENT (source provided), and upgrade the
  wording to "machine-checked" only after attaching the `lake build` /
  `#print axioms` output. (See PACKAGE_README.md, "Build and verification".)
-/

namespace GCAssess

/-- The three-valued verdict lattice (slot C1). -/
inductive Verdict where
  | coherent
  | incoherent
  | undetermined
  deriving DecidableEq, Repr

open Verdict

/--
  The recursive composition rule for combining a running verdict with the
  verdict of the next child, read in traversal order.

  * `incoherent` is absorbing (the short-circuit): once a child is incoherent,
    the combined verdict is `incoherent` regardless of what follows.
  * otherwise `undetermined` dominates `coherent` (a single undetermined child,
    with no incoherent child, yields `undetermined`).
  * `coherent` combines with `coherent` to `coherent`.
-/
def combine : Verdict → Verdict → Verdict
  | incoherent, _            => incoherent
  | _,          incoherent   => incoherent
  | undetermined, _          => undetermined
  | _,          undetermined => undetermined
  | coherent,   coherent     => coherent

/-- Fold `combine` over a list of child verdicts, starting from `coherent`
    (the identity for a node with no children). -/
def foldVerdicts : List Verdict → Verdict
  | []      => coherent
  | v :: vs => combine v (foldVerdicts vs)

/-- A declared hypothesis tree. Leaf carries an oracle-supplied verdict
    (slot B1: this verdict is an INPUT, not decided here). -/
inductive HTree where
  | leaf : Verdict → HTree
  | node : List HTree → HTree

/-- Tree evaluator (mutual with `evalForest`): a leaf returns its
    (oracle) verdict; a node folds its children's verdicts through `combine`. -/
mutual
  def evalTree : HTree → Verdict
    | HTree.leaf v  => v
    | HTree.node ts => evalForest ts

  def evalForest : List HTree → Verdict
    | []      => coherent
    | t :: ts => combine (evalTree t) (evalForest ts)
end

/-! ### Consistency theorems for the decision semantics. -/

/-- `combine` is total and returns one of the three declared verdicts.
    (Totality is automatic from the definition; we record exhaustiveness as a
    sanity theorem: the result is always one of the three constructors.) -/
theorem combine_wellformed (a b : Verdict) :
    combine a b = coherent ∨ combine a b = incoherent ∨
    combine a b = undetermined := by
  cases a <;> cases b <;> simp [combine]

/-- `coherent` is a left identity for `combine`. -/
theorem coherent_left_id (v : Verdict) : combine coherent v = v := by
  cases v <;> rfl

/-- `coherent` is a right identity for `combine`. -/
theorem coherent_right_id (v : Verdict) : combine v coherent = v := by
  cases v <;> rfl

/-- Short-circuit, left form: an incoherent first argument forces incoherent. -/
theorem incoherent_absorbing_left (v : Verdict) :
    combine incoherent v = incoherent := by
  cases v <;> rfl

/-- Short-circuit, right form: an incoherent second argument forces incoherent. -/
theorem incoherent_absorbing_right (v : Verdict) :
    combine v incoherent = incoherent := by
  cases v <;> rfl

/-- `combine` is associative. Together with the identity theorems this makes
    `(Verdict, combine, coherent)` a monoid, so the folded verdict of a node is
    independent of association order (well-definedness of the recursion). -/
theorem combine_assoc (a b c : Verdict) :
    combine (combine a b) c = combine a (combine b c) := by
  cases a <;> cases b <;> cases c <;> rfl

/-- Characterisation of the folded verdict, part 1 (COHERENT stopping
    condition): a node is `coherent` iff EVERY child verdict is `coherent`. -/
theorem fold_coherent_iff (vs : List Verdict) :
    foldVerdicts vs = coherent ↔ ∀ v ∈ vs, v = coherent := by
  induction vs with
  | nil => simp [foldVerdicts]
  | cons v vs ih =>
      constructor
      · -- forward: fold = coherent  ⇒  head and every tail element coherent
        intro h w hw
        -- case on the head; only `coherent` head keeps the fold coherent
        cases hv : v with
        | coherent =>
            subst hv
            rcases List.mem_cons.mp hw with hw | hw
            · exact hw
            · -- fold (v::vs) = combine coherent (fold vs) = fold vs
              have hfold : foldVerdicts vs = coherent := by
                simpa [foldVerdicts, coherent_left_id] using h
              exact (ih.mp hfold) w hw
        | incoherent =>
            subst hv
            simp [foldVerdicts, incoherent_absorbing_left] at h
        | undetermined =>
            subst hv
            -- combine undetermined _ is coherent for no tail value
            simp only [foldVerdicts] at h
            cases hfold : foldVerdicts vs <;> rw [hfold] at h <;>
              simp [combine] at h
      · -- backward: every element coherent ⇒ fold coherent
        intro h
        have hhead : v = coherent := h v (List.mem_cons_self _ _)
        have htail : ∀ w ∈ vs, w = coherent :=
          fun w hw => h w (List.mem_cons_of_mem _ hw)
        subst hhead
        simp [foldVerdicts, coherent_left_id, ih.mpr htail]

/-- Characterisation part 2 (INCOHERENT reachability): a fold is `incoherent`
    iff SOME child verdict is `incoherent`. This is the semantic content of the
    short-circuit: one incoherent child suffices, matching the Python
    implementation's early return. -/
theorem fold_incoherent_iff (vs : List Verdict) :
    foldVerdicts vs = incoherent ↔ ∃ v ∈ vs, v = incoherent := by
  induction vs with
  | nil => simp [foldVerdicts]
  | cons v vs ih =>
      constructor
      · -- forward
        intro h
        cases hv : v with
        | incoherent =>
            exact ⟨incoherent, List.mem_cons_self _ _, hv ▸ rfl⟩
        | coherent =>
            subst hv
            have hfold : foldVerdicts vs = incoherent := by
              simpa [foldVerdicts, coherent_left_id] using h
            obtain ⟨w, hw, hwi⟩ := ih.mp hfold
            exact ⟨w, List.mem_cons_of_mem _ hw, hwi⟩
        | undetermined =>
            subst hv
            simp only [foldVerdicts] at h
            cases hfold : foldVerdicts vs <;> rw [hfold] at h <;>
              simp [combine] at h
      · -- backward
        rintro ⟨w, hw, rfl⟩
        rcases List.mem_cons.mp hw with hw | hw
        · -- w is the head and w = incoherent
          simp [foldVerdicts, hw, incoherent_absorbing_left]
        · -- w is in the tail
          have hfold : foldVerdicts vs = incoherent := ih.mpr ⟨incoherent, hw, rfl⟩
          cases hv : v with
          | incoherent => simp [foldVerdicts, hv, incoherent_absorbing_left]
          | coherent => simp [foldVerdicts, hv, coherent_left_id, hfold]
          | undetermined =>
              simp [foldVerdicts, hv, hfold, incoherent_absorbing_right]

/-- The three verdicts are pairwise distinct: the trichotomy is genuinely
    three-valued (no two collapse). Guards against a degenerate lattice. -/
theorem verdicts_distinct :
    coherent ≠ incoherent ∧ coherent ≠ undetermined ∧
    incoherent ≠ undetermined := by
  refine ⟨?_, ?_, ?_⟩ <;> intro h <;> cases h

/-- A node's verdict equals the `foldVerdicts` of its children's verdicts, i.e.
    `evalForest` computes exactly the algebra's fold. This ties the tree
    evaluator to the verdict algebra characterised above, so the COHERENT and
    INCOHERENT characterisations transport to whole trees. -/
theorem evalForest_eq_fold (ts : List HTree) :
    evalForest ts = foldVerdicts (ts.map evalTree) := by
  induction ts with
  | nil => rfl
  | cons t ts ih => simp [evalForest, foldVerdicts, List.map_cons, ih]

/-- Determinism/soundness at tree level: evaluating a tree yields exactly one
    verdict (`evalTree` is a total function into the three-valued `Verdict`;
    combined with the characterisation theorems, a returned determinate verdict
    reflects a real structural condition on the leaves). -/
theorem evalTree_total (t : HTree) :
    evalTree t = coherent ∨ evalTree t = incoherent ∨
    evalTree t = undetermined := by
  cases h : evalTree t <;> simp

end GCAssess

/-
  Verification hooks. Uncomment under a Lean 4 toolchain with `lake build`:

  #print axioms GCAssess.combine_assoc
  #print axioms GCAssess.fold_coherent_iff
  #print axioms GCAssess.fold_incoherent_iff
  #print axioms GCAssess.evalForest_eq_fold
  -- Expected: each depends only on Lean core (no `sorry`, no extra axioms).
-/
