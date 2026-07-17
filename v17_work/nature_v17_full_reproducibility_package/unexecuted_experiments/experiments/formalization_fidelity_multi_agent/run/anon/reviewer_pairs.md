### ITEM-01
- passage: Semantic identity depends on metric, interactions, position, boundaries, warrant, fitness, and continuation.
- candidate Lean declaration: def SemEq (x y : Node) := x.label = y.label
- candidate registry warrant: definition

### ITEM-02
- passage: Regional fragmentation requires locality and unresolved cross-region obligations.
- candidate Lean declaration: theorem regional_fragmentation (h : backlog_unbounded U) : exists_regions U
- candidate registry warrant: theorem

### ITEM-03
- passage: If two latent states share first-order projection but require different target values, no projection-only decoder is correct on both.
- candidate Lean declaration: theorem conflation (hq : q x = q y) (hφ : φ x ≠ φ y) : ¬ ∃ d, d (q x)=φ x ∧ d (q y)=φ y
- candidate registry warrant: theorem

### ITEM-04
- passage: Under bounded evaluation error and residual budget, participantwise selected options are within the registered regret bound for every participant.
- candidate Lean declaration: theorem option_bound (i : Participant) : regret i selected ≤ 2*ε+δ
- candidate registry warrant: theorem

### ITEM-05
- passage: Cognitive order is preserved by a bijection on qualifying functional-equivalence classes induced by an admissible representation.
- candidate Lean declaration: theorem order_invariant (e : QualClass X ≃ QualClass Y) : Fintype.card (QualClass X)=Fintype.card (QualClass Y)
- candidate registry warrant: theorem

### ITEM-06
- passage: Without external evidence the strongest result is GF-3 conditional structural admissibility.
- candidate Lean declaration: theorem actual_great_filter_identified : ObservedCosmicFilter = FMICNS
- candidate registry warrant: theorem

### ITEM-07
- passage: Admissible pointed FSS isomorphisms preserve every formula in the registered metric-interaction target language.
- candidate Lean declaration: theorem semantic_invariance (e : AdmissibleIso X Y) (φ : Formula) : Eval X v φ ↔ Eval Y (e.toFun v) φ
- candidate registry warrant: theorem

### ITEM-08
- passage: Metric is constitutive and target-relevant changes can alter semantic identity.
- candidate Lean declaration: structure FSS where nodes : Type; edges : Node → Node → Prop
- candidate registry warrant: definition

### ITEM-09
- passage: Physical mappings remain external premises.
- candidate Lean declaration: axiom gravity_is_G : PhysicalMapping Gravity G
- candidate registry warrant: axiom

### ITEM-10
- passage: After a valid reversal, a persistent positive post-lift arrival-service gap makes backlog unbounded.
- candidate Lean declaration: theorem recurrence (hgap : ∀ t≥T, δ ≤ A t - S t) : ∀ M, ∃ t, M ≤ U t
- candidate registry warrant: theorem

### ITEM-11
- passage: The lift-to-dynamical bridge needs contraction, closure, and invariance.
- candidate Lean declaration: theorem lift_to_dyn (h : CNSLift M c) : DynamicCNS f D
- candidate registry warrant: theorem

### ITEM-12
- passage: Admissible isomorphism and gauge transformation preserve semantic holonomy around corresponding closed paths.
- candidate Lean declaration: theorem holonomy_invariant (e : AdmissibleIso X Y) (g : Gauge) : holonomy (transportPath e g p) = holonomy p
- candidate registry warrant: theorem

### ITEM-13
- passage: Terminal and observability targets are distinct.
- candidate Lean declaration: def TerminalFilter := ObservabilityLoss
- candidate registry warrant: definition

### ITEM-14
- passage: The mechanism yields a conditional structural filter only when branch, hazard, timescale, outcome, and residue premises are supplied.
- candidate Lean declaration: theorem conditional_filter (hbranch : BranchClosure M) (hhazard : NonSummableHazard M) (htime : Timescale M) (hout : TargetOutcome M) (hres : ResidueSuppression M) : StructuralFilter M
- candidate registry warrant: corollary

### ITEM-15
- passage: Cognitive order is the number of non-equivalent reusable spanning compositions.
- candidate Lean declaration: def CognitiveOrder (m : Model) := m.choiceDepth
- candidate registry warrant: definition

### ITEM-16
- passage: Reflection exposes residual but does not by itself raise cognitive order.
- candidate Lean declaration: theorem reflection_increments_order : Ord (reflect M) = Ord M + 1
- candidate registry warrant: theorem

### ITEM-17
- passage: Register and Recall are not equal to words generated solely by conceptual L/G endomorphisms without typed bridges.
- candidate Lean declaration: theorem register_not_word (w : LGWord) : Register ≠ w.eval
- candidate registry warrant: theorem

### ITEM-18
- passage: A valid lift adds a prior-unavailable non-equivalent spanning composition, expands the operand domain, and reverses the current residual.
- candidate Lean declaration: theorem cns_lift (hnew : NewComposition M c) (hspan : Spans c) (hexpand : StrictOperandExpansion M c) (hrev : ReversesResidual M c) : CNSLift M c
- candidate registry warrant: theorem

### ITEM-19
- passage: An order lift enters the dynamical CNS regime only with contraction, closure, and invariance premises.
- candidate Lean declaration: theorem lift_to_dyn (hL : CNSLift M c) (hc : Contractive f) (hcl : ClosedOn f D) (hi : Invariant target f) : DynamicCNS f D
- candidate registry warrant: theorem

### ITEM-20
- passage: Governance is participantwise and cannot be reduced to aggregate mean improvement.
- candidate Lean declaration: theorem governance_ok (h : meanUtility after ≥ meanUtility before) : GoodGovernance after
- candidate registry warrant: theorem