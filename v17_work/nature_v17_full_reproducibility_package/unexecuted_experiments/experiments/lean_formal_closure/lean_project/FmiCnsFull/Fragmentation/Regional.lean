import FmiCnsFull.Fragmentation.Backlog

namespace FmiCnsFull

/-- Regional obligation system.  Local burdens and cross-region demand/service
    are kept distinct so regional fragmentation is not inferred from backlog
    growth alone. -/
structure RegionalSystem (Region Edge : Type*) where
  src : Edge → Region
  dst : Edge → Region
  requiredCross : Edge → Prop
  localBurden : Region → ℕ → ℝ
  crossDemand : Edge → ℕ → ℝ
  crossService : Edge → ℕ → ℝ

/-- Every region remains internally certified below `ε`. -/
def InternallyCertifiedAt {Region Edge : Type*}
    (R : RegionalSystem Region Edge) (ε : ℝ) (t : ℕ) : Prop :=
  ∀ r, R.localBurden r t ≤ ε

/-- At least one target-required cross-region edge remains unresolved. -/
def HasUnresolvedCrossAt {Region Edge : Type*}
    (R : RegionalSystem Region Edge) (t : ℕ) : Prop :=
  ∃ e, R.requiredCross e ∧
    0 < backlog (R.crossDemand e) (R.crossService e) t

/-- Regional fragmentation is internal certification together with an
    unresolved required cross-region bridge. -/
def RegionallyFragmentedAt {Region Edge : Type*}
    (R : RegionalSystem Region Edge) (ε : ℝ) (t : ℕ) : Prop :=
  InternallyCertifiedAt R ε t ∧ HasUnresolvedCrossAt R t

/-- T-REGIONAL-FRAG, restricted and substantive.  If local certification is
    maintained while one required cross-edge demand-service difference is
    unbounded, then arbitrarily large unresolved cross burden occurs at times
    when the incident regions remain internally certified. -/
theorem regionalFragmentation
    {Region Edge : Type*}
    (R : RegionalSystem Region Edge) (ε : ℝ) (e : Edge)
    (hreq : R.requiredCross e)
    (hlocal : ∀ t, InternallyCertifiedAt R ε t)
    (hcross : ∀ M : ℝ, ∃ t,
      M < R.crossDemand e t - R.crossService e t) :
    ∀ M : ℝ, 0 ≤ M → ∃ t,
      RegionallyFragmentedAt R ε t ∧
      M < backlog (R.crossDemand e) (R.crossService e) t := by
  intro M hM
  rcases backlogUnbounded (R.crossDemand e) (R.crossService e) hcross M with
    ⟨t, ht⟩
  refine ⟨t, ?_, ht⟩
  refine ⟨hlocal t, ?_⟩
  refine ⟨e, hreq, ?_⟩
  linarith

end FmiCnsFull
