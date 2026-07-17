import FmiCnsFull.Core.Types

namespace FmiCnsFull

universe u₁ v₁ u₂ v₂

/-- An admissible FSS isomorphism preserves exactly the target-relevant
    metric-interaction-position structure used by the manuscript. -/
structure AdmissibleIso (X : TypedFSS.{u₁, v₁}) (Y : TypedFSS.{u₂, v₂}) where
  nodeEquiv : X.V ≃ Y.V
  edgeEquiv : X.E ≃ Y.E
  nodeKind_preserved : ∀ x, Y.nodeKind (nodeEquiv x) = X.nodeKind x
  edgeKind_preserved : ∀ e, Y.edgeKind (edgeEquiv e) = X.edgeKind e
  src_preserved : ∀ e, Y.src (edgeEquiv e) = nodeEquiv (X.src e)
  dst_preserved : ∀ e, Y.dst (edgeEquiv e) = nodeEquiv (X.dst e)
  dist_preserved : ∀ x y, Y.dist (nodeEquiv x) (nodeEquiv y) = X.dist x y
  admissible_preserved : ∀ x,
    Y.boundary.admissible (nodeEquiv x) ↔ X.boundary.admissible x
  certified_preserved : ∀ x,
    Y.boundary.certified (nodeEquiv x) ↔ X.boundary.certified x
  warranted_preserved : ∀ x,
    Y.boundary.warranted (nodeEquiv x) ↔ X.boundary.warranted x
  continues_preserved : ∀ x,
    Y.boundary.continues (nodeEquiv x) ↔ X.boundary.continues x
  fitness_preserved : ∀ x,
    Y.boundary.fitness (nodeEquiv x) = X.boundary.fitness x

/-- A pointed admissible isomorphism also preserves the designated node. -/
structure AdmissiblePointedIso (P : PointedFSS) (Q : PointedFSS) where
  iso : AdmissibleIso P.space Q.space
  point_preserved : iso.nodeEquiv P.point = Q.point

/-- Registered target language.  It contains the manuscript's primitive
    semantic predicates, Boolean connectives, and bounded quantification over
    represented nodes and interactions. -/
inductive Formula (X : TypedFSS) where
  | nodeKindEq (x : X.V) (k : NodeKind)
  | edgeKindEq (e : X.E) (k : EdgeKind)
  | incident (e : X.E) (a b : X.V)
  | distLE (a b : X.V) (r : ℝ)
  | admissible (x : X.V)
  | certified (x : X.V)
  | warranted (x : X.V)
  | continues (x : X.V)
  | fitnessLE (a b : X.V)
  | neg (φ : Formula X)
  | conj (φ ψ : Formula X)
  | disj (φ ψ : Formula X)
  | existsNode (φ : X.V → Formula X)
  | forallNode (φ : X.V → Formula X)
  | existsEdge (φ : X.E → Formula X)
  | forallEdge (φ : X.E → Formula X)

namespace Formula

/-- Truth of a registered formula in its FSS. -/
def eval {X : TypedFSS} : Formula X → Prop
  | nodeKindEq x k => X.nodeKind x = k
  | edgeKindEq e k => X.edgeKind e = k
  | incident e a b => X.src e = a ∧ X.dst e = b
  | distLE a b r => X.dist a b ≤ r
  | admissible x => X.boundary.admissible x
  | certified x => X.boundary.certified x
  | warranted x => X.boundary.warranted x
  | continues x => X.boundary.continues x
  | fitnessLE a b => X.boundary.fitness a ≤ X.boundary.fitness b
  | neg φ => ¬ eval φ
  | conj φ ψ => eval φ ∧ eval ψ
  | disj φ ψ => eval φ ∨ eval ψ
  | existsNode φ => ∃ x, eval (φ x)
  | forallNode φ => ∀ x, eval (φ x)
  | existsEdge φ => ∃ e, eval (φ e)
  | forallEdge φ => ∀ e, eval (φ e)

/-- Transport a formula along an admissible FSS isomorphism. -/
def map {X : TypedFSS} {Y : TypedFSS} (F : AdmissibleIso X Y) : Formula X → Formula Y
  | nodeKindEq x k => nodeKindEq (F.nodeEquiv x) k
  | edgeKindEq e k => edgeKindEq (F.edgeEquiv e) k
  | incident e a b => incident (F.edgeEquiv e) (F.nodeEquiv a) (F.nodeEquiv b)
  | distLE a b r => distLE (F.nodeEquiv a) (F.nodeEquiv b) r
  | admissible x => admissible (F.nodeEquiv x)
  | certified x => certified (F.nodeEquiv x)
  | warranted x => warranted (F.nodeEquiv x)
  | continues x => continues (F.nodeEquiv x)
  | fitnessLE a b => fitnessLE (F.nodeEquiv a) (F.nodeEquiv b)
  | neg φ => neg (map F φ)
  | conj φ ψ => conj (map F φ) (map F ψ)
  | disj φ ψ => disj (map F φ) (map F ψ)
  | existsNode φ => existsNode (fun y => map F (φ (F.nodeEquiv.symm y)))
  | forallNode φ => forallNode (fun y => map F (φ (F.nodeEquiv.symm y)))
  | existsEdge φ => existsEdge (fun e => map F (φ (F.edgeEquiv.symm e)))
  | forallEdge φ => forallEdge (fun e => map F (φ (F.edgeEquiv.symm e)))

/-- T-SEM-EQUIV.  Every registered target formula is invariant under an
    admissible metric-interaction isomorphism. -/
theorem eval_map_iff {X : TypedFSS} {Y : TypedFSS}
    (F : AdmissibleIso X Y) : ∀ φ : Formula X, eval (map F φ) ↔ eval φ := by
  intro φ
  induction φ with
  | nodeKindEq x k => simp [map, eval, F.nodeKind_preserved]
  | edgeKindEq e k => simp [map, eval, F.edgeKind_preserved]
  | incident e a b =>
      simp [map, eval, F.src_preserved, F.dst_preserved]
  | distLE a b r => simp [map, eval, F.dist_preserved]
  | admissible x => simpa [map, eval] using F.admissible_preserved x
  | certified x => simpa [map, eval] using F.certified_preserved x
  | warranted x => simpa [map, eval] using F.warranted_preserved x
  | continues x => simpa [map, eval] using F.continues_preserved x
  | fitnessLE a b => simp [map, eval, F.fitness_preserved]
  | neg φ ih => simp [map, eval, ih]
  | conj φ ψ ihφ ihψ => simp [map, eval, ihφ, ihψ]
  | disj φ ψ ihφ ihψ => simp [map, eval, ihφ, ihψ]
  | existsNode φ ih =>
      constructor
      · rintro ⟨y, hy⟩
        refine ⟨F.nodeEquiv.symm y, ?_⟩
        exact (ih (F.nodeEquiv.symm y)).mp hy
      · rintro ⟨x, hx⟩
        refine ⟨F.nodeEquiv x, ?_⟩
        simpa using (ih x).mpr hx
  | forallNode φ ih =>
      constructor
      · intro h x
        have hx := h (F.nodeEquiv x)
        simpa using (ih x).mp hx
      · intro h y
        have hy := (ih (F.nodeEquiv.symm y)).mpr (h (F.nodeEquiv.symm y))
        simpa using hy
  | existsEdge φ ih =>
      constructor
      · rintro ⟨e, he⟩
        refine ⟨F.edgeEquiv.symm e, ?_⟩
        exact (ih (F.edgeEquiv.symm e)).mp he
      · rintro ⟨e, he⟩
        refine ⟨F.edgeEquiv e, ?_⟩
        simpa using (ih e).mpr he
  | forallEdge φ ih =>
      constructor
      · intro h e
        have he := h (F.edgeEquiv e)
        simpa using (ih e).mp he
      · intro h e
        have he := (ih (F.edgeEquiv.symm e)).mpr (h (F.edgeEquiv.symm e))
        simpa using he

end Formula

/-- Semantic identity is represented extensionally by the existence of an
    admissible pointed isomorphism.  Quotienting by this relation can be added
    after the kernel confirms equivalence-law proofs. -/
def SemanticallyEquivalent (P Q : PointedFSS) : Prop :=
  Nonempty (AdmissiblePointedIso P Q)

end FmiCnsFull
