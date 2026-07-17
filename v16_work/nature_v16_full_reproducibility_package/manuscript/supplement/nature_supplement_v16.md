# Supplementary Information: First-order conflation and recurrent fragmentation generate a cognitive near-singularity

**Andy E. Williams**

*Manuscript version 16 | 17 July 2026*


## Contents and status
This Supplement is the standalone formal, computational and status record for Article v15. It restores every load-bearing definition and premise used by the Article, separates semantic registration from proof checking, retains the executed finite realization from the earlier computational package, adds the executed direct recurrence experiment for this version, and records all unexecuted gates explicitly. No unpublished artifact is required to recover the formal content.


| Package | Content | v15 status |
|---|---|---|
| A | Core FMI-CNS mathematics | Prose proofs and countermodels supplied; kernel formalization pending |
| B | Endogenous semantic geometry | Definitions and theorem targets supplied; physical mapping remains a hypothesis |
| C | Lean verification artifact | Module and declaration manifest supplied; pinned source package passes a static no-sorry / no-custom-axiom scan; kernel build and axiom report pending |
| D | String-specific extension | Candidate geometric representation; comparative utility experiment pending |
| E | External and propagation evidence | Positive v8 Gate Zero reproduction; canonical recurrence rerun; bounded same-model receiver study and bounded branch/hazard and mutation experiments executed; cross-model receiver and external trace studies open |


The package status tuple is Status(v16) = (conditionally closed, conditionally closed, partially closed, open, closed-bounded), where Package A/B carry prose/source proofs, Package C (Lean) is source-complete and static-audit-clean with the kernel build blocked by the environment's egress policy, Package D (string action) remains open, and Package E now carries a positive v8 Gate Zero reproduction, a canonical recurrence rerun, a bounded same-model receiver study and bounded Great Filter branch/hazard and mutation experiments.

For the five submission gates addressed in the companion open-gate closure record, the gate status tuple is


> Status_gates = (*s*_Lean, *s*_G0, *s*_Rec, *s*_Recv, *s*_Ext) = (partial, closed-positive, closed, closed-bounded, partial).


The Lean kernel build is partially closed (source-complete, static-audit clean; toolchain download egress-blocked); the v16 Gate Zero audit is closed-positive (the v8 lineage was supplied and reproduced bit-for-bit); the direct recurrence experiment is closed (canonical common-latent-world rerun); the same-model receiver study is closed-bounded (executed with isolated agents); the external mappings are partially closed (registration-closed; no physical instantiation promoted). Formal coherence within stated premises and submission-carrier readiness are separate verdicts. No aggregate label may erase which gate is open.


## Supplementary Note 1. Typed metric functional state spaces and endogenous semantics
*Local map.* This Note defines the mathematical object on which every later theorem operates. Its payoff is a representation of semantic identity that is constituted by metric position, typed interactions and admissible relational configuration rather than by a prose label.


### Definition S1: typed metric FSS
A typed metric functional state space is *X* = (*V*, *E*, τ_V, τ_E, *g*, π, β, *A*), where *V* is the set of represented functional states, *E* the set of typed interaction or transition instances, τ_V and τ_E the node and interaction typing maps, *g* a metric or metric family, π an optional coordinate or embedding representation, β the boundary record and *A* the family of admissible transformations and trajectories.

A boundary record may contain domain and codomain restrictions, certificates, provenance, residuals, successor obligations, fitness relations, continuation conditions, version identities and target scope. The metric may be primitive, interaction-induced or jointly defined. Every theorem must state which case it uses.


### Definition S2: nodes, processes and functions
A represented concept or functional state is a node *v* ∈ *V*. A reasoning or physical interaction is a typed edge, hyperedge, path or process subgraph. Definitions, claims, functions, proofs, experiments, datasets and manuscript passages are semantic roles borne by nodes and processes rather than additional primitive represented-object kinds.

A represented function has an intensional node carrying identity, domain, codomain and contract, and an extensional family of process instances carrying executions. An *instantiates* relation connects the contract node to those instances.


### Definition S3: semantic profile and identity
For *v* ∈ *V*, Prof_X(*v*) = (*X*, *v*) and Sem_X(*v*) = [(*X*, *v*)]_≅*A*. An admissible pointed isomorphism *F* : (*X*, *v*) → (*Y*, *w*) must satisfy *F*(*v*) = *w*, preserve node and interaction types, incidence, orientation and the declared metric relations, preserve boundary, certificate, warrant and continuation records, and intertwine the relevant transition and participant-fitness relations. Approximate isomorphisms must expose the tolerance and residual rather than silently replacing equality.


### Theorem S1: semantic equivalence
If *F* : (*X*, *v*) → (*Y*, *w*) is an admissible target-preserving pointed isomorphism, then every invariant target proposition expressible in the registered language has the same truth value at *v* and *w*.

*Proof.* Let the registered language be generated from atomic predicates on node type, edge type, metric relation, incidence, boundary, warrant, transition, fitness and continuation structure by Boolean connectives and bounded quantification over the represented FSS. Admissibility preserves every atomic predicate. The result follows by induction on formula construction. For a quantified formula, the bijection induced by *F* transports witnesses and counterexamples. Therefore truth is invariant. QED.


### Definition S4: finite target-complete semantic kernel
For target family *T* and resource budget *B*, define *K_T*(*v*; *X*, *B*) = min{*K* ⊆ *X* : *T* is decidable for *v* from *K* within *B*}. If no unique minimum exists, retain the family of minimal kernels. The finite semantic signature is Sem_*T*,*B*(*v*) = [*K_T*(*v*; *X*, *B*), *v*]_≅*T*,*A*. Failure to certify a target-complete finite kernel yields undetermined, not a fabricated complete signature.


### Cross-FSS structural principle
Conceptual space and physical P-space instantiate the same invariant-level principle: functional identity is constituted by metric position, typed interactions and admissible relational configuration. The operands and substrates remain distinct. This is a structural identity claim, not object identity.


### Interactions induce topology
For each operation *o*, define an admissible-transition relation *R_o* ⊆ *V* × *V*. The family {*R_o*} induces or constrains reachability, connectedness, support overlap, commutation classes, boundary crossings and path-equivalence structure. Interactions therefore generate topological implications; topology is not merely a label applied after the dynamics are fixed.


## Supplementary Note 2. Reflective FMI subspace and signal boundaries
*Local map.* This Note identifies the reflective object needed to register the complete argument and separates signal carriers from internal conceptual states. It supplies the transmission residuals used by governance and propagation theorems.


### Theorem S2: reflective-subspace representation
Let *C* be a conceptual FSS. The reflective FMI subspace *R*_FMI ⊆ *C* contains represented concepts, process identities, function contracts, compositions, targets, proofs, experiments, warrants, governance rules, signal residuals and unresolved external premises.

Every registered object required to state, prove, test, amend or transmit the FMI-CNS-Great Filter relationship can be represented as a concept node, a process edge or subgraph, or both. No additional primitive represented-object class is required.

*Proof.* Map every noun-like identity or contract to a concept node. Map every transformation, inference, execution, comparison, registration, transmission or amendment to a typed process. Represent multi-input operations as hyperedges or contract-preserving subgraphs. Represent a proof as a premise-to-conclusion subgraph with certificate; represent an experiment as protocol, execution, measurement and interpretation subgraphs. This construction covers every registered role. A counterexample must exhibit an indispensable represented object that cannot be encoded in these forms without changing its contract. QED.

Reflective strata are typing devices. Reifying a process as a concept improves observability but does not increase cognitive order unless it enables another non-equivalent space-spanning composition.


### Signal boundary
For participant *i*, Register_*i* : Σ_*i* ⇀ *X_i* and Express_*i* : *X_i* ⇀ Σ_*i*. A signal is not an internal concept until it is registered. An internal concept is not externally available until it is expressed.


### Four residuals
For a composition executed by *i* and reconstructed by *j*, *R*_*i*→*j* = *R*_reg,*i* ⊕ *R*_expr,*i* ⊕ *R*_recv,*j* ⊕ *R*_recon,*j*. The direct sum preserves failure source and type. *R*_reg,*i* is source structure unavailable after initial registration; *R*_expr,*i* is structure omitted or altered by expression; *R*_recv,*j* is expressed structure not registered by the receiver; and *R*_recon,*j* is registered structure not reconstructed into an executable contract.


### Registration closure
A formalization is registration-closed for target family *T* when every target-relevant semantic invariant in the manuscript has a canonical mathematical representation and every manuscript use maps to that representation without unresolved ambiguity. Registration closure is distinct from proof closure: a proof assistant can validate a proof about the wrong registered object.


## Supplementary Note 3. FMI function contracts and four-operation topology
*Local map.* This Note states the canonical FMI function registry and replaces the undefined local/global terminology of v14 with target-relevant factorization definitions. It also supplies the type obstruction needed for Register/Recall nonreduction.


### FMI registry

| ID | Function | Layer | Contract |
|---|---|---|---|
| B01 | Register | boundary | Admit typed external signal structure without minting unavailable distinctions |
| B02 | Express | boundary | Encode selected FSS structure onto a carrier while recording loss |
| C01 | Store | conceptual | Preserve recoverable identity, relation, verdict, obligations and provenance |
| C02 | Recall | conceptual | Reactivate or reconstruct stored structure under target and budget |
| C03 | L | conceptual | Evaluate or transform within active local support |
| C04 | G | conceptual | Evaluate or transform across globally relevant support while preserving obligations |
| C05 | Promotion/Create | conceptual | Preserve an admissible composite as a reusable higher-order operand |
| E01 | Choice | external control | Select the next external-function invocation through the fitness-control basis |
| F01-F06 | Model, Evaluate, Stability, Adaptation, Decomposition, Bridging | fitness | Represent, compare, preserve, correct, factor and bridge participant consequences |
| X01 | Certificate | coupling | Validate target-relevant paths and boundaries |
| X02 | Governance | coupling | Authorize participant-complete selection and target revision |


For current, target and projected fitness, χ(*a*) = (*f*_tar − *f*_cur, *f*_proj(*a*) − *f*_cur, *f*_tar − *f*_proj(*a*)). The current-projected relation grounds Model/Evaluate, current-target grounds Stability/Adaptation, and target-projected grounds Decomposition/Bridging. A non-embeddable partial order remains partial and yields undetermined.


### Support definition
For operation instance *o* and target Φ, Supp_Φ(*o*) = ⋂{*S* ⊆ *V* : the output and retained invariants of *o* are determined from *S*}. When the intersection is not unique, retain the family of minimal supports. An operation has local support when every minimal target support lies within one declared interaction neighbourhood and factorizes over target-independent remote contexts. It has global support when some target-relevant output or invariant depends nonfactorizably on extended support spanning multiple neighbourhoods or components. Global does not mean acausal or spatially infinite; local does not mean short-range. The distinction is target-relevant factorization.


### Schedule definition
For admissible local realizations *r*_1, *r*_2, the schedule is parallel when *r*_1 ∘ *r*_2 ≃_*T* *r*_2 ∘ *r*_1, and sequential when a typed precedence relation is load-bearing and reversal changes the target-relevant result or makes execution inadmissible. Parallel means observational commutation, not simultaneous wall-clock execution.


### Candidate four-operation inventory

| Operation | Support | Schedule | Cognitive role | Candidate physical realization |
|---|---|---|---|---|
| Register | local | parallel | constrained placement or binding | strong interaction |
| Recall | global | sequential | globally constrained typed reconfiguration | weak interaction |
| L | local | sequential | ordered local propagation or calibration | electromagnetic interaction |
| G | global | parallel | extended-support geometry-sensitive coherence | gravity |


The operation classes are defined before the physical assignments. Each physical assignment remains a separately testable mapping hypothesis.


### Theorem S3: Register/Recall nonreduction
Let ⟨*L*, *G*⟩ be the typed algebra generated by compositions of *L* and *G* acting as endomorphisms on active conceptual state *X*. Register has type Σ ⇀ *X* and Recall has type *M* × *T* × *B* ⇀ *X*.

No well-typed term generated solely by *L* and *G* has the boundary type of Register or the memory-access type of Recall. A reduction requires an additional bridge implementing the missing boundary or memory contract and therefore does not establish generation by *L* and *G* alone.

*Proof.* Every generator has domain and codomain *X* under the base architecture; composition preserves this endomorphism type. Register requires a source in Σ, while Recall requires access to *M* × *T* × *B*. Neither source is constructible by endomorphism composition without a typed bridge. Adding such a bridge supplies the missing primitive contract. QED.


## Supplementary Note 4. Projection, conflation and reflective necessity
*Local map.* This Note proves the information-theoretic obstruction that begins the formal chain and records countermodels that delimit it.

Let *q*_FO = *h* ∘ *q*_R. Every target factoring through *q*_FO also factors through *q*_R. Some targets factor through *q*_R but not *q*_FO when *h* removes target-relevant distinctions.


### Theorem S4: first-order conflation
If *q*_FO(*x*) = *q*_FO(*y*) but Φ(*x*) ≠ Φ(*y*), no evaluator restricted to the projected state is correct on both. The proof is the contradiction argument in the Article. For stochastic evaluators with equal registered states and kernels, the output laws coincide.


### Corollary S4.1: local stability
For deterministic first-order-local *L* and equal inputs, *L^k*(*q*_FO(*x*)) = *L^k*(*q*_FO(*y*)) for every finite *k*. Induction on *k* proves the result.


### Theorem S5: reflective necessity
When a target depends on function identity, contract, composition, provenance, warrant, participant consequences or successor obligations, a representation containing only domain concepts and conclusions is inadequate whenever it collapses two process structures with different target verdicts. This is T-CONFLATE applied to a target whose separating witness belongs to the reflective subspace.


### Countermodels

| Countermodel | Effect |
|---|---|
| Target fully determined by first-order projection | Reflection unnecessary for that target |
| Reflective registry without new composition | Observability improves; order does not increase |
| Equivalent renaming or call expansion | No new composition class |
| Projection retains every target-relevant distinction | First-order assessment can be exact |
| Target-aware abstention | False confidence falls without increasing span |



## Supplementary Note 5. Composition equivalence, span, order and invariance
*Local map.* This Note distinguishes intrinsic cognitive order from finite evidence about order. It carries the representation-invariance proof and demotes the cardinality increment to a lemma.


### Definitions
A registered composition Γ = *f_m* ∘ ⋯ ∘ *f*_1 has identity, signature, domain, codomain, boundary conditions, execution semantics and preserved invariants. For admissible domain *D* and target language *L*, Γ_1 ≃_*D*,*L* Γ_2 ⇔ ∀ *x* ∈ *D*, Obs_*L*(Γ_1*x*) = Obs_*L*(Γ_2*x*). A composition spans the declared universal target family *T** when it connects every target-required region by certified transformations, preserves semantic identities and obligations, and returns correct or calibrated-undetermined verdicts within the architecture's contract.

*S*(*C*) = {[Γ]_≃ : Γ registered, reusable, nonredundant and spanning} and Ord(*C*) = |*S*(*C*)|. A finite certificate is Ord̂_*T*,ε,*B*(*C*) = |{[Γ]_≃ : SpanCert_*T*,ε,*B*(Γ, *C*)}|. It is a lower bound unless target and certificate completeness are proved.


### Theorem S6: representation invariance
If *F* : *C* → *C*′ is an admissible FSS isomorphism preserving external-function identity, composition, span, reuse and functional equivalence, then Ord(*C*) = Ord(*C*′).

*Proof.* Map each class [Γ] ∈ *S*(*C*) to [*F*Γ*F*^−1] ∈ *S*(*C*′). Preservation assumptions make this map well defined. The inverse is induced by *F*^−1, so the map is bijective. Cardinalities are equal. QED.


### Lemma S6.1: order increment
If a new qualifying class [Γ_*N*+1] is not already in *S*(*C_N*), then the union with that singleton increases cardinality by one. This is definitional and does not independently establish reversal or operand expansion.


### Finite decidability target
For finite FSSs, finite operation libraries, decidable target predicates and bounded resources, span certification and functional equivalence are decidable by exhaustive enumeration. The executable Lean decision theorem remains an implementation target.


## Supplementary Note 6. Arrival-service fragmentation, reversal and recurrence
*Local map.* This Note replaces the v14 directional fragmentation tendency with two explicit theorem levels: backlog divergence and regional fragmentation. It then proves reversal and recurrence under stated service conditions.

Let *D_N*(*t*) be cumulative target-weighted arrivals, *B_N*(*t*) cumulative certified service and *U_N*(*t*) = max{0, *D_N*(*t*) − *B_N*(*t*)}.


### Theorem S7: backlog divergence
If *D_N*(*t*) − *B_N*(*t*) is unbounded above, then *U_N*(*t*) is unbounded along a subsequence. If the limsup linear drift is positive, the difference is unbounded. The proof follows directly from the maximum definition.


### Theorem S8: regional fragmentation
Construct an obligation graph *H_t*. Assume local integration keeps each region below ε_local, cross-region arrivals exceed certified cross-region service by an unbounded amount, unresolved edges are not replaced by false identity certificates and the target requires at least two regions. Then an unbounded subsequence contains an unresolved target-required cross-region edge while each incident region remains internally certified. QED.


### Theorem S9: reflective-loss burden
Let *C_t* be target-different pairs collapsed by the first-order projection and let *Q_t* = ∑_(*x*,*y*)∈*C<sub>t*</sub> *w_t*(*x*, *y*). If *Q_t* is unbounded and no additional separating distinctions are registered, the minimum first-order decision loss or calibrated-undetermined mass grows according to the declared loss. The exact lower bound depends on the prior and loss function and must be reported with them.


### Theorem S10: reversal
If an added composition changes service so that *D_N*(*t*) − *B*_*N*+1(*t*) ≤ ε over a declared interval, then *U*_*N*+1(*t*) ≤ max(0, ε) over that interval. The current increasing-backlog regime is reversed to bounded residual.


### Theorem S11: recurrence
If the lift creates a new arrival process *D*_*N*+1 and *D*_*N*+1(*t*) − *B*_*N*+1(*t*) becomes unbounded above without another spanning composition or scaling change, then *U*_*N*+1(*t*) is unbounded along a subsequence by Theorem S7.


### Required countermodels
Bounded domains, matching same-order service, target families ignoring the residual, distributed service that grows faster than arrivals, temporary backlog decreases, reflection-only improvements and false nominal bridges are all retained as explicit theorem boundaries.


### Executed direct recurrence experiment
For this version the recurrence prediction was preregistered in executable form and run, closing the v15 statement that a direct recurrence run was absent. The stochastic model uses the backlog recursion *U*_*t*+1 = max{0, *U_t* + *A_t* − *S_t*}, with arrivals *A_t* and certified integration service *S_t*.

**Deterministic recurrence criterion (executed-model theorem).** Suppose there are times *T*_L < *T*_R such that (i) *U_t* > 0 and *S_t* − *A_t* ≥ δ_1 > 0 for *T*_L ≤ *t* < *T*_R, so the current backlog decreases; and (ii) there is *T** > *T*_R and δ_2 > 0 with *A_t* − *S_t* ≥ δ_2 for all *t* ≥ *T**. Then the lift reverses the backlog over the first interval, and *U_t* grows without a uniform bound after *T**. *Proof.* While *U_t* > 0 in the reversal interval, *U*_*t*+1 ≤ *U_t* − δ_1, so *U_t* decreases until it reaches the reflected boundary or the interval ends. After *T**, *U*_*t*+1 ≥ *U_t* + δ_2; induction gives *U*_*T**+*n* ≥ *U*_*T** + *n*δ_2, which is unbounded in *n*. QED.

*Frozen protocol.* Master seed 20260716; 1,000 replicates per regime; 12 regions; horizon 300; lift time *T*_L = 80; operand-expansion time *T*_E = 120; optional second-lift time 215; regional backlog threshold 12; recurrence window 30; persistent slope threshold 1.0; final backlog threshold 150. Before the lift, per-region arrival intensity exceeds service. The lift raises service above arrivals, providing a genuine reversal interval. Continued operand expansion then raises arrival intensity. Five regimes are compared: (1) fixed post-lift service; (2) proportional same-order service tracking each region's arrivals with a positive margin; (3) regenerative distribution through delayed logistic spread of the new composition; (4) a second discrete order lift at time 215; and (5) branch heterogeneity with region-specific arrival multipliers under fixed post-lift service. Regional fragmentation is the number of regions with backlog at least 12. The preregistered persistent-recurrence endpoint requires a post-lift decrease of at least 30% relative to the pre-lift backlog, a late aggregate slope above one backlog unit per time step, a final backlog above 150, and a 30-step window after time 190 satisfying the slope and backlog thresholds.


### Table S-REC | Direct recurrence results across 1,000 replicates per regime

| Regime | Rev. | Rec. | Recurrence time | Final backlog | Regions |
|---|---|---|---|---|---|
| Fixed post-lift | 1.000 | 1.000 | 232.0 [220, 244] | 694.1 [583, 797] | 11.99 [12, 12] |
| Proportional service | 1.000 | 0.000 | - | 36.1 [15, 65] | 0.43 [0, 2] |
| Regenerative distribution | 1.000 | 0.000 | - | 65.1 [32, 107] | 1.49 [0, 4] |
| Second order lift | 1.000 | 0.000 | - | 53.8 [25, 90] | 1.01 [0, 3] |
| Branch heterogeneity | 1.000 | 1.000 | 219.0 [219, 219] | 989.0 [867, 1104] | 9.70 [8, 12] |


Bracketed values are empirical 2.5th and 97.5th percentiles; "Regions" is the final number of regions above the preregistered fragmentation threshold. All five regimes showed the required immediate reversal: mean aggregate slope changed from approximately +6.94 before the lift to between −7.07 and −10.14 during the reversal interval. Recurrence to the preregistered persistent endpoint was effectively certain under fixed post-lift service and under heterogeneous branches, and did not occur under proportional service, regenerative distribution or a second order lift.


![Supplementary Figure S-REC1 | Aggregate unresolved backlog across 1,000 replicates per regime. The dashed line marks the order lift, the dotted line operand expansion, and the dash-dot line the optional second lift. Bands are empirical 95% simulation intervals. Fixed post-lift service and heterogeneous branches recur; proportional service, regenerative distribution and a second lift remain bounded.](../source_figures/recurrence_backlog.png)



![Supplementary Figure S-REC2 | Number of regions above the fragmentation threshold. Fixed post-lift service and heterogeneous branches develop widespread regional fragmentation after operand expansion; scaling and additional lifts keep the median regional count low.](../source_figures/recurrence_regions.png)


This experiment closes the direct-recurrence gate for the declared synthetic model. It supplies an executed finite witness for the model-relative claim that, after a valid order lift reverses an increasing backlog, continued growth at fixed post-lift service can recreate a positive backlog regime and regional fragmentation, while proportional service scaling, regenerative distribution or another order lift are explicit counter-regimes. It does not show that current AI systems, institutions or civilizations follow these parameter values, and it does not audit or replace the inherited version-8 realization. Its warrant is executed synthetic recurrence experiment.


## Supplementary Note 7. CNS lift, near-singular content and dynamical bridge
*Local map.* This Note places the scientific burden beyond the definitional count change. It connects the order-lift transition to operand expansion, reversal and the separately published dynamical CNS.


### Theorem S12: order-lift CNS
If an order-*N* architecture gains a registered, reusable and non-equivalent spanning composition, expands the admissible operand domain and closes the current frontier within its residual contract, then order becomes *N*+1, the operand domain expands, the current backlog is bounded over the declared interval and complete consequences need not factor through the order-*N* projection.

*Proof.* Lemma S6.1 gives the order increment. Operand expansion is a premise witnessed by the new admissible substructures. Theorem S10 gives reversal. If complete consequences factored through the old projection, no new target-relevant distinction would be required; a paired target witness supplies the nonfactorization. QED.


### Near-singular content
Let AdmSub(*X_N*) be the structures that become admissible operands under the new composition. Define structural displacement *S_N*(*a*) = μ(*R_N^a* \ *R_N*) and participant-target consequence field Δ*F*(*a*). A world comparator *B_N*(*X_N*, *W*) bounds non-lift displacement and a lift lower bound *L_N*(*X_N*) satisfies *L_N* > *B_N* above the declared threshold. Under admissible-substructure growth, the world comparator, monotone coupling, adoptability and no-order-skipping premises, a minimal lift exceeds every non-lift order-*N* intervention in magnitude above the threshold, while complete content need not factor through the order-*N* projection. The result is conditional on the comparator and coupling; no infinite physical quantity is asserted.


### Dynamical CNS bridge
The published object is (*X*, *d*, ⊗, *G*, *N*) with a globally contracting, compositionally closed and benign-reparameterization-invariant update operator converging to a unique fixed point or normal form [15]. **Bridge A.** If the new composition enables such an operator on the expanded domain, the order lift enters the dynamical CNS regime there. **Bridge B.** If realization of a dynamical CNS operator on a previously untraversable domain requires a non-equivalent spanning composition absent at order *N*, it witnesses an order lift. Countermodels include a noncontracting order lift, a contracting local operator with no new composition, a bounded-subspace fixed point, multiple compositions converging to one fixed point and a mere call expansion.


*Supplementary Figure 1 | Candidate cognitive worldsheet and semantic transport. A reasoning composition and its revision family embed as a worldsheet whose induced metric is pulled back from the ambient semantic metric; a connection transports identity, contract, warrant and obligations, and closed-loop holonomy certifies semantic drift.*



## Supplementary Note 8. Importance, governance and regenerative propagation
*Local map.* This Note separates magnitude from valence and defines the propagation criterion needed for collective order.


### Participantwise option monotonicity
Let *O_b* ⊆ *O_a*. Suppose represented and realized values differ by at most ε_*i*, selection error is at most δ_*i*, each baseline option remains admissible and governance selects a new option only if its represented lower bound is no worse than the best baseline. Then *u_i*(*a**) ≥ max_*b*∈*O<sub>b*</sub> *u_i*(*b*) − (2ε_*i* + δ_*i*). *Proof.* Selection gives *û_i*(*a**) ≥ max_*b* *û_i*(*b*) − δ_*i*. Representation error gives *u_i*(*a**) ≥ *û_i*(*a**) − ε_*i* and *û_i*(*b*) ≥ *u_i*(*b*) − ε_*i*. Combining proves the bound. QED. If participant completeness, target stability, projection adequacy or realization fails, valence inversion is possible.


### Centralized uncheckability
A projection *q* : *X* → *Z* is adequate for target Φ only if *q*(*x*) = *q*(*y*) implies Φ(*x*) = Φ(*y*). A centralized realization is collectively uncheckable whenever the center uses a target-relevant distinction that does not factor through the signal available to participants.


### Regenerative propagation
Regenerate(*i*, *j*; Γ, *T*) = 1 only when receiver *j* reconstructs a contract-preserving realization, executes it on hidden targets and can retransmit it under the same criterion. *R*_Γ(*t*) is the expected number of new regenerative executors per executor. Exposure and agreement are necessary at most; they are not regeneration.


## Supplementary Note 9. Great Filter lemma family and conditional corollary
*Local map.* This Note derives each necessary property separately before applying the constraint set to the recurrent FMI-CNS mechanism. It prevents a list of intuitions from being presented as one theorem.


### Target classes and assumptions
A terminal filter suppresses persistence of almost all technologically consequential lineages after consequential environmental transformation becomes possible. An observability filter suppresses persistent astronomically detectable manifestations. The assumptions are a many-opportunity regime, ordinary causal locality, potential branching, diverse realization and a declared residue expectation.


### Lemma S13: upper-tail suppression
For independent opportunities with *p_i* ≥ *p* > 0, *P*(no escape among *M*) = ∏_*i* (1 − *p_i*) ≤ (1 − *p*)^*M* → 0. A sufficient many-opportunity filter must suppress exceptional branches, correlate outcomes, reduce effective opportunities or suppress observables after escape.


### Lemma S14: branch closure
For independent branches with survival probabilities *s_j* > 0, *P*(at least one survives) = 1 − ∏_*j* (1 − *s_j*). A sufficient filter acts before branching, recurs in branches, preserves a shared vulnerability, correlates outcomes or remains effective after dispersal.


### Lemmas S15-S19
**Causal self-instantiation:** a nondistributed filter must be generated or propagated to each causally separated site before escape. **First-mover consistency:** the earliest consequential lineage must be affected under the same law or a regress-closed prior condition. **Functional substrate invariance:** the defining vulnerability must extend across the declared realization class rather than one contingent biology. **Adaptive non-escapability:** a stable positive adaptive escape probability defeats upper-tail suppression unless adaptation is correlated or bounded. **Outcome, residue and timescale sufficiency:** the target outcome must occur before durable escape or correction, or remain effective afterward; a target-specific sufficient condition can require τ_*F* < min(τ_*D*, τ_*C*).


### Theorem S20: Great Filter constraint
A sufficient member of the declared filter class must satisfy the conjunction of Lemmas S13-S19.


### Theorem S21: structural admissibility
Recurrent fixed-order fragmentation and CNS reversal belong to the structurally admissible class when burden is generated locally by growth, relations are functionally substrate-general, lifts reverse current burden but recurrence recreates it, successor branches inherit or recreate the limitation and outcome/timescale premises are supplied separately.


### Corollary S21.1
Let *h_t* = *H*(*U_N*(*t*), *C*(*t*), *R*(*t*), *P_N*(*t*), *X*(*t*)), 0 ≤ *h_t* < 1. If ∑_*t* *h_t* = ∞, then ∏_*t* (1 − *h_t*) = 0. If the external FSS mapping, recurrent burden, failed lift/propagation, branch correlation, non-summable hazard and target outcome premises hold, recurrent failed CNS realization or propagation is a post-intelligence Great Filter within the model.


### Claim ladder

| Level | Permitted statement | Required warrant |
|---|---|---|
| GF-0 | Some mechanisms are physically possible | physical consistency or example |
| GF-1 | The declared filter class has the listed necessary properties | Theorem S20 |
| GF-2 | Recurrent FMI-CNS failure is structurally admissible | Theorem S21 |
| GF-3 | It would be a filter if mapping and hazard premises hold | Corollary S21.1 |
| GF-4 | Current systems exhibit measured components | external traces / receiver studies |
| GF-5 | Real civilizations instantiate the full mechanism | physical, branch, timescale and hazard evidence |
| GF-6 | The mechanism explains the observed Great Filter | comparative inference and observability assumptions |



## Supplementary Note 10. Cognitive string theory as semantic mathematical representation
*Local map.* This Note gives CST its narrowed role: it represents the semantic object that Lean can reason about. It separates the constitutive metric and hard admissibility from any optional scalar action.


### Worldsheet object
Let *X*_*A* : Σ_ws → *C* × *F* embed a reasoning composition and its revision family. Coordinates (σ, τ) index position along the composition and revision, alternative derivation or receiver reconstruction. Each point or cell carries a semantic state, an FMI operation label, interaction type, boundary record and warrant/certificate state.


### Induced metric
The worldsheet metric is induced from the ambient semantic metric: *h_ab* = ∂_*a**X*^*A* ∂_*b**X*^*B* *g_AB*, or by a discrete pullback analogue for graph-based FSSs. The construction must state whether *g* is primitive, interaction-induced or hybrid and which transformations preserve it.


### Connection and transport
A connection *A*_*C* transports concept identity, function contract, target, warrant, boundary data, successor obligations and participant roles. For path γ, transport is PT_*A*<sub>*C*</sub>(γ); for a closed loop ℓ, holonomy is Hol_*A*<sub>*C*</sub>(ℓ). **Holonomy-invariance target.** Admissibly homotopic derivations with preserved curvature and boundaries transport equivalent semantic objects. **Holonomy-drift target.** If a closed derivation loop returns a target-relevant identity, contract or warrant to a non-equivalent object, it certifies semantic drift. The discrete Lean version can use path composition and transport equality without differential geometry.


### Consequence closure and hard admissibility
Let Ξ be a complete lattice of candidate operand structures and Φ_*W* : Ξ → Ξ a monotone consequence operator adding consequences, boundaries and successor obligations. Define Ξ*_*W* = lfp(Φ_*W*). Existence follows from the fixed-point premise. Hard admissibility is a proposition Adm_*W*(Ξ*_*W*). Missing identity, type, contract, warrant, boundary or continuation obligations are ill typed or unproved; they cannot be compensated by a lower action value.


### Constitutive metric and optional action
The constitutive metric defines relative position, neighbourhood, admissible isometry, deformation size and any required contraction. An optional action can rank or search admissible worldsheets: *S*_CST = *S*_step + *S*_revision + *S*_holonomy + *S*_obligation. It is not a correctness oracle. It is accepted only if invariant under admissible encoding, non-arbitrary relative to the constitutive metric and useful beyond a simpler typed graph representation.


## Supplementary Note 11. Lean-facing module and theorem manifest
*Local map.* This Note states exactly what a Lean artifact must contain and where the trust boundary lies. It reports the pinned source package and its static audit for v15 but does not claim a completed kernel build.

Lean is an interactive theorem prover based on dependent type theory with a small kernel that checks proof terms [23,24]. The project should use theorem parameters for external premises and avoid unregistered global axioms. Axiom dependencies must be printed for each top-level theorem; any dependency on sorryAx fails the build gate.


### Pinned source package and module tree
For this version a pinned pure-Lean core was constructed. It pins leanprover/lean4:v4.32.0 (no Mathlib) and separates the formal object into eight modules realizing ten of the primary theorems.


| Module | Main declarations |
|---|---|
| Core.lean | typed layers (signal/concept/memory); operations Register, Express, Store, Recall, L, G; layer distinctness |
| TopLevel.lean | the bundled formal_mechanism_chain over the retained core theorems |
| Projection.lean | first-order conflation (firstOrderConflation); local-stability iterate |
| Operations.lean | typed L/G word algebra; Register/Recall nonreduction by domain obstruction |
| Order.lean | order increment (order_increment) and order invariance (order_invariance) |
| Backlog.lean | unit-gap backlog growth, reversal to bounded residual, renewed post-lift growth |
| GreatFilter.lean | conditional Great Filter corollary with every external premise as a Prop parameter |


This is a bounded formal core. It does not contain the complete quotient construction for semantic isomorphism classes, the full target language, the entire regional-fragmentation graph theorem or the published dynamical-CNS bridge. It replaces an empty skeleton with proof-bearing source for the primary logical shapes the manuscript uses. Representative statements realized in the source include the first-order conflation impossibility (if *q*(*x*) = *q*(*y*) and Φ(*x*) ≠ Φ(*y*) then no decoder is correct on both), the typed Register/Recall nonreduction by constructor contradiction, and the finite backlog growth lemma (if *U*(*t*+1) ≥ *U*(*t*) + 1 for all *t* then *U*(*n*) ≥ *U*(0) + *n*) together with its post-lift shifted form.


### Static source audit
A static audit scanned every .lean file and counted forbidden tokens.


| Forbidden token | Count |
|---|---|
| sorry | 0 |
| admit | 0 |
| axiom | 0 |
| opaque | 0 |


This result is useful but is not a kernel result: lexical absence of sorry does not establish that the files elaborate or that the proof terms type-check. A lexical no-sorry / no-custom-axiom scan is not a kernel proof.


### Why the kernel gate is not closed
The Lean toolchain could not be installed: the elan/Lean release-binary download from github.com was blocked by the environment's egress policy (HTTP 403; PyPI is allowlisted but GitHub release binaries are not), so the following acceptance criteria remain unexecuted: a clean lake build; kernel acceptance of every theorem body; a #print axioms report for all top-level declarations; a clean-environment independent reproduction; and hash equality between two builds. The disposition is therefore partially closed. The gap is narrowed to a mechanical execution: install the pinned toolchain, run lake build, preserve stdout/stderr and append the axiom report. Any elaboration failure must be repaired in the source and rerun; it may not be converted into documentary proof closure.


### Proposed full project structure
FmiCns/ FSS/Basic.lean, FSS/Semantics.lean, FMI/Functions.lean, FMI/SignalBoundary.lean, Projection/Conflation.lean, Operations/SupportSchedule.lean, Operations/Nonreduction.lean, Order/Composition.lean, Order/Span.lean, Order/Invariance.lean, Fragmentation/Queue.lean, Fragmentation/Regional.lean, CNS/Lift.lean, CNS/DynamicalBridge.lean, Governance/Options.lean, Propagation/Regeneration.lean, GreatFilter/Constraints.lean, CST/Paths.lean, CST/Transport.lean, CST/Closure.lean, Main.lean.


### Declaration skeletons
structure FSS where Node : Type; Edge : Type; nodeType : Node -> TypeTag; edgeType : Edge -> EdgeTag; metric : Node -> Node -> Real; incident : Edge -> Node -> Prop; boundary : Node -> BoundaryRecord; admissible : (Node -> Node) -> Prop.

structure Composition (X : FSS) where run : X.Node -> X.Node; registered : Prop; reusable : Prop; spans : Prop. The order is def CognitiveOrder (X : FSS) : Cardinal := Cardinal.mk {c : Composition X // c.registered /\ c.reusable /\ c.spans}. The final implementation should quotient by functional equivalence rather than count raw implementations.


### Top-level theorem signatures
theorem firstOrderConflation {W O Y : Type} (q : W -> O) (phi : W -> Y) {x y : W} (hq : q x = q y) (hphi : phi x != phi y) : Not (Exists fun decoder : O -> Y => decoder (q x) = phi x /\ decoder (q y) = phi y).

theorem conditionalGreatFilter (core : CoreCnsPremises M) (physical : PhysicalMapping M) (branch : BranchClosure M) (hazard : NonSummableHazard M) (timescale : FilterTimescale M) (outcome : TargetMatchingOutcome M) : PostIntelligenceFilter M. In the pinned source package these top-level shapes carry proof terms for the bounded core; the wider skeleton retains documentary placeholders that a submission artifact must replace with kernel-checked proof terms and an axiom report showing no sorryAx dependency.


### Three-valued reporting outside the kernel
Lean proves propositions or fails to construct a proof. Manuscript-level reporting uses proved, disproved and undetermined. Undetermined is assigned by the workflow when neither a proposition nor its negation is certified within the declared formalization and budget; it is not a third truth value inside Lean's logic.


## Supplementary Note 12. Formalization-fidelity, semantic-equivalence and mutation tests
*Local map.* This Note specifies the tests required before a Lean proof can be treated as a faithful formalization of the manuscript rather than a proof about a substituted object.


### Formalization-fidelity audit
Independent registrars receive frozen manuscript passages and construct mappings to canonical declarations. Primary endpoints are exact recovery of semantic identity, theorem dependencies, warrant status and external-premise boundaries. Disagreement is resolved by typed counterexample rather than majority vote.


### Semantic-equivalence tests
Required transformations include benign node renaming; coordinate reparameterization preserving the metric; metric mutation preserving labels; interaction mutation preserving distances; warrant mutation preserving conclusions; and participant-fitness mutation preserving aggregate mean. Expected verdicts are invariance under the first two and semantic non-equivalence under target-relevant mutations.


### Mutation catalogue
Replace cognitive order with Choice depth; reduce Register/Recall to *G*/*L* without bridge types; swap support/schedule cells; delete a theorem premise; promote a conditional claim to empirical fact; collide aliases; remove a warrant edge; silently close an external premise; remove a successor obligation; use an intervention label as ground truth. Every mutation must either fail type checking, invalidate a proof or produce an explicit undetermined dependency status. Diagnostic tests built from registered invariants are controls; hidden transfer is the primary evidence of propagation.


## Supplementary Note 13. Executed finite computational realization and Gate Zero audit
*Local map.* This Note reports the reproduced finite witness and the positive v16 Gate Zero audit that regenerated it from the supplied v8 lineage. It supplies constructive and conformance evidence but no external AI or civilizational measurement.

The complete state was event sourced and updated by one transition function. Each trajectory executed Register, Recall/activation, *L* or *G* with optional lift/span, certificate validation, participant Model/Evaluate/Decompose/Bridge/Governance, Store and reuse, Express and consequence realization. The reported execution contained 12,800 trajectories and 102,400 events. These were reproduced bit-for-bit by the positive v16 Gate Zero audit below.


### Deterministic witnesses
The complete model was reported to pass 23 target-pair witnesses. Each designated ablation failed or became correctly undetermined.


| ID | Contract | Target distinction | Ablation result |
|---|---|---|---|
| W01 | Register | external symbol becomes typed concept | fail |
| W02 | Express | stored verdict reconstructed externally | fail |
| W03 | Store | identity persists after context eviction | fail |
| W04 | Recall | stored bridge reactivates under later target | fail |
| W05 | L | local relation classification | fail |
| W06 | G | cross-region support preserves obligations | undetermined |
| W07-W09 | fitness coordinates | current, target and projected distinctions | fail |
| W10-W15 | internal basis | action-conditioned consequence and correction distinctions | fail / undetermined as specified |
| W16 | Promotion | promote admissible composite | undetermined |
| W17 | operand lift | separate lower-order-identical paired worlds | undetermined |
| W18 | certified span | connect lifted operand to remote target | fail |
| W19 | Certificate | reject decoy bridge | fail |
| W20 | Governance | reject mean-positive participant harm | fail |
| W21 | carrier type | reject signal-space regress | fail |
| W22 | target revision | separate target movement from progress | fail |
| W23 | one generator | detect split transition semantics | fail |



### Higher-order paired worlds

| Condition | Target accuracy | Certified reach | Reuse | Containment | Harm |
|---|---|---|---|---|---|
| local baseline | 0.311 | 0.000 | 0.000 | 1.000 | 0.000 |
| matched compute | 0.346 | 0.000 | 0.000 | 1.000 | 0.000 |
| matched memory | 0.316 | 0.000 | 0.000 | 1.000 | 0.000 |
| matched population | 0.333 | 0.000 | 0.000 | 1.000 | 0.000 |
| matched communication | 0.400 | 0.000 | 0.000 | 1.000 | 0.000 |
| certification only | 0.327 | 0.003 | 0.000 | 1.000 | 0.000 |
| lift only | 0.310 | 0.000 | 0.000 | 1.000 | 0.000 |
| span only | 0.317 | 0.000 | 0.000 | 1.000 | 0.000 |
| full CNS | 0.585 | 0.435 | 0.347 | 0.993 | 0.007 |
| residual-open CNS | 0.397 | 0.160 | 0.130 | 0.713 | 0.156 |



### Bounded registration

| Relation depth | Pipeline | Exact recovery | Relation retention | False confidence |
|---|---|---|---|---|
| 2 | generic summary | 0.300 | 0.561 | 0.333 |
| 2 | relation extraction | 0.700 | 0.822 | 0.144 |
| 2 | target-aware monitor | 0.867 | 0.928 | 0.000 |
| 4 | target-aware monitor | 0.622 | 0.875 | 0.000 |
| 6 | target-aware monitor | 0.233 | 0.750 | 0.000 |
| 8 | target-aware monitor | 0.067 | 0.611 | 0.000 |
| 12 | target-aware monitor | 0.000 | 0.249 | 0.000 |
| 16 | target-aware monitor | 0.000 | 0.113 | 0.000 |


A correlation-aware retention model achieved held-out log loss 0.258 versus 1.024 for homogeneous independence. The canonical codeword reconstruction was identified at 0.940 under 1.5% independent bit flips.


### v16 Gate Zero audit (executed, closed-positive)
The Gate Zero question is whether the inherited version-8 numerical results can be regenerated from the supplied frozen transition function, source events, registry, configuration and conformance suite while preserving the v16 definitions. The audit (identifier EXP-GATE-ZERO-V16-EXECUTED-REPRODUCTION) obtained the v8 lineage (zip SHA-256 f21b7ba6..., matching the reference) and re-ran it.


| Required artifact | Available |
|---|---|
| v8 generator source | Yes (present, reproduced) |
| v8 event log | Yes (present, reproduced) |
| v8 trajectory table | Yes (present, reproduced) |
| v8 registry | Yes (present, reproduced) |
| v8 frozen configuration | Yes (present, reproduced) |
| v8 conformance suite | Yes (present, reproduced) |
| v8 environment lock | Yes (present, reproduced) |
| v8 source figures / source data | Yes (present, reproduced) |
| v8 checksums | Yes (present, reproduced) |
| v15 Article source | Yes |
| v15 Supplement source | Yes |
| v15 revision plan | Yes |


The audit disposition is closed-positive. The execution manifest validated (58 files, 0 hash mismatches); run_experiment.py re-ran cleanly (exit 0) in a clean venv pinned to numpy 2.3.5 / pandas 2.2.3 / scipy 1.17.0 / networkx 3.6.1 / matplotlib 3.10.8 / scikit-learn 1.7.2 (plus tabulate, an unpinned optional report dependency); the conformance tests passed; the model hash 797b16e3... and registry hash b7a6ef0e... matched the manifest and reference; and all 18 data files reproduced bit-for-bit after gzip decompression (including the 45 MB event log). Twelve key values regenerated at full precision: full-CNS accuracy 0.5845588235294118, best matched comparator 0.39950980392156865, full-CNS certified reach 0.4349877450980392, best comparator certified reach 0.003308823529411765, reuse 0.34681372549019607, Pareto containment 0.98671875, incoherent containment 0.7171875, harmed fractions 0.012109375 / 0.155712890625, lower-order decoder max accuracy 0.4805714285714286, canonical codeword identification 0.94, and correlation-aware held-out log loss 0.258278. The inherited numbers are therefore promoted from historical witness to reproduced constructive witness (conformant under the single generator and event lineage).


## Supplementary Note 14. Primary experiments and transfer-first propagation
*Local map.* This Note states the experiments that must be executed after the formal objects are frozen. Transfer and regenerative reconstruction are primary; conformance to built-in invariants is diagnostic. Dispositions for this version are recorded per experiment.


### EXP-GATE-ZERO-V16 (executed, closed-positive)
Audit literal and executed definitions, label branches, surrogate metrics, actual states, registry coverage, one-generator correspondence and compatibility with the v16 semantic definitions. Executed for this version with disposition closed-positive (Note 13): the supplied v8 lineage regenerated every inherited metric from source events under one generator.


### EXP-LEAN-FORMAL-CLOSURE (partially closed)
Primary outcomes: clean build, zero sorry, no unregistered axioms, complete theorem-manifest coverage, reproducible dependency report and independent build. For this version a pinned source package exists and passes a static no-sorry / no-custom-axiom scan, but no kernel build was executed (Note 11); the disposition is partially closed.


### EXP-FORMALIZATION-FIDELITY (open)
Independent registrars map manuscript claims to canonical definitions and theorem parameters. Primary endpoints are identity recovery, dependency recovery, warrant classification and external-premise separation.


### EXP-SEMANTIC-EQUIVALENCE (open)
Test benign and target-changing transformations from Note 12. Primary endpoints are invariance sensitivity, mutation specificity and shortest semantic witness.


### EXP-LEAN-MUTATION (open)
Run the mutation catalogue. The primary endpoint is the fraction of target-changing mutations that fail type checking or invalidate the expected top-level theorem while benign transformations preserve it.


### EXP-DIRECT-RECURRENCE (executed, closed)
Generate a first growth interval, apply a certified order lift, then continue growth under fixed order *N*+1. The primary endpoint is a preregistered change from increasing backlog to bounded residual followed by renewed positive backlog drift. Executed for this version across five regimes (Note 6, Table S-REC and Figures S-REC1-S-REC2); the endpoint was met under fixed post-lift service and branch heterogeneity and not met under proportional service, regenerative distribution or a second order lift. The result is synthetic and model-relative.


### EXP-LEAN-RECEIVER-PROPAGATION (partially closed)
Conditions are prose-only, registry-only, direct typed-graph formalization, CST/Lean package and corrupted controls. Receivers must recover the dependency chain, distinguish proofs from external premises, apply the formalization to hidden claim families, locate controlled mutations and produce a package from which a second receiver succeeds without author repair. Receiver and claim family are the units of inference. For this version the protocol is frozen: six experimental conditions, seven primary transfer tasks, eight primary endpoints (including second-receiver regenerative success and author-repair count), 14 hidden claim families instantiated as 28 randomized tasks, a separately stored answer key, a scoring schema with fatal-error categories, and a blinding and no-author-repair rule. The regenerative endpoint is Regenerate(*i*, *j*; Γ, *T*) = 1 only if *j* recovers a contract-preserving representation of Γ, executes it on a hidden target family and produces a retransmission package from which a second receiver succeeds without author repair; mere agreement with the manuscript conclusion does not satisfy it. A bounded isolated same-model receiver study was executed: two conditions (formal package vs prose-only control), two Receiver A instances each in fresh contexts seeing only their read-only packet, and one Receiver B regeneration from a Receiver A transmission. All six core verdicts transferred in both conditions (24/24); the registered theorem identity (T-CONFLATE) was recovered by 2/2 formal-package receivers and 0/2 prose-only receivers; the second-generation receiver reproduced all verdicts and the theorem identity from the transmission alone with zero author repair. The warranted claim is regenerative propagation across isolated same-model instances; cross-model and human propagation remain open.


### Receiver hidden-family inventory

| Family | Target distinction |
|---|---|
| HF-CONFLATE | collapsed registration with target-different latent states |
| HF-REFLECTION | reflective observability versus order lift |
| HF-REGISTER | boundary Register versus conceptual L/G endomorphism |
| HF-RECALL | memory Recall versus conceptual L/G endomorphism |
| HF-ORDER | novelty, span, reuse and non-equivalence |
| HF-RECURRENCE | fixed-service recurrence versus scaled-service countermodel |
| HF-BRIDGE-LIFT-DYN | order lift plus contraction/closure/invariance |
| HF-BRIDGE-DYN-LIFT | new dynamical operator requiring a prior-unavailable composition |
| HF-GOVERNANCE | participant completeness versus aggregate mean |
| HF-GF-TARGET | terminal versus observability target |
| HF-GF-PROMOTION | GF-3 conditional result versus GF-6 explanation |
| HF-SEM-RENAME | benign admissible isomorphism |
| HF-METRIC | label-preserving target-relevant metric mutation |
| HF-EXTERNAL | formal proof versus unmeasured external premise |



### EXP-CST-GEOMETRY-UTILITY (open)
Compare direct typed graph formalization with the string/worldsheet representation. CST geometry succeeds only if it improves encoding invariance, semantic-drift detection, transfer, compression or receiver reconstruction under matched resources. Failure demotes the string-specific layer without weakening the core FSS/Lean program.


## Supplementary Note 15. Registry, claim ledger and manuscript coverage
*Local map.* This Note specifies the source-of-truth records that prevent prose, code and formal declarations from silently diverging.

Required registries are fss_semantics_v15, fmi_functions_v15, operation_topology_v15, cognitive_order_v15, fragmentation_dynamics_v15, cns_bridge_v15, great_filter_constraints_v15, cst_semantic_geometry_v15, lean_theorem_manifest_v15, claim_warrant_ledger_v15, experiment_registry_v15 and version_diff_v14_to_v15. Every theorem record contains premises, conclusion, proof certificate or proof obligation, countermodels, dependencies, warrant, manuscript locations and Lean declaration name. Every external-premise record states its empirical interpretation, measurement protocol, status and the strongest conclusion it can promote.


### Principal status ledger

| Claim | Current v15 status | Promotion requirement |
|---|---|---|
| Endogenous semantic identity | mathematical definition and prose theorem | independent fidelity audit / executable formalization |
| T-CONFLATE | formal proof; source-realized in Lean core, kernel run pending | kernel proof term |
| T-ORDER-INVARIANCE | prose proof under admissible-isomorphism premises | Lean quotient implementation and build |
| Backlog divergence | formal proof | none beyond declared model |
| Regional fragmentation | conditional theorem | explicit obligation-graph formalization |
| Direct recurrence | executed synthetic experiment (closed for the declared model) | external instantiation for civilizational claims |
| T-CNS-LIFT | conditional theorem plus retained historical witness | kernel closure and external recurrence evidence |
| Dynamical bridge | conditional theorem family | formal implementation of published object |
| Option monotonicity | formal proof plus historical synthetic result | measured error bounds |
| Regenerative propagation | executed bounded (same-model, second generation, 0 author repairs) | cross-model / human receivers |
| GF necessary properties | decomposed conditional theorem | formal proof terms / assumption challenge |
| FMI-CNS structural admissibility | GF-2 conditional theorem | physical and branch mapping for GF-4/5 |
| Great Filter identification | open | hazard, timescale, residue and comparative evidence |
| CST geometric utility | open | matched comparative experiment |
| Gate Zero conformance | executed, closed-positive (v8 lineage reproduced bit-for-bit) | none beyond the declared witness class |
| Lean proof closure | source-complete, static-audit clean; kernel build open | pinned clean build, axiom audit, independent reproduction |



## Supplementary Note 16. External mappings, standalone completeness and completion protocols
*Local map.* This Note is the submission gate. It registers the external-mapping certificate matrix, states what is already contained in the package and states what must still be supplied before external claims or Lean verification are promoted.


### External-mapping certificate matrix (registration-closed)
Each external mapping has a stable identity, formal object, minimum evidence, strongest permitted claim and explicit defeater. Registration closure prevents silent promotion; every mapping below remains open at the instantiation level.


| Mapping | Minimum evidence | Strongest permitted statement | Status |
|---|---|---|---|
| Cross-FSS semantic principle | Target-specific invariant-preserving map | The same structural principle can be instantiated across FSSs | Open |
| Strong interaction ↔ Register | Support factorization and schedule-commutation witnesses | Candidate physical realization | Open |
| Weak interaction ↔ Recall | Support nonfactorization and precedence witnesses | Candidate physical realization | Open |
| Electromagnetism ↔ L | Support factorization and precedence witnesses | Candidate physical realization | Open |
| Gravity ↔ G | Support nonfactorization and commutation witnesses | Candidate physical realization | Open |
| Current AI trace mapping | External version-locked collapsed-pair traces with hidden targets | Testable external mapping | Open |
| Historical order lifts | Preregistered uniform classification and independent evidence | Candidate historical instances | Open |
| Great Filter branch closure | Heterogeneous branch evidence or defensible external model | Conditional branch premise | Open |
| Hazard non-summability | Longitudinal hazard and correction/dispersal evidence | Conditional hazard premise | Open |
| Target residue suppression | Outcome- and timescale-specific residue evidence | Conditional outcome premise | Open |


The physical operation assignments are not standard measurements read from established interaction ranges; their support and schedule definitions are target-relative functional claims requiring explicit factorization, nonfactorization, commutation and precedence certificates. A mapping can now fail at a named certificate without affecting the conceptual theorem package, while a successful certificate promotes only the claim level it supports.


### Standalone-completeness checklist

| Requirement | Disposition |
|---|---|
| Typed metric FSS and endogenous semantics | installed |
| Reflective FMI and four signal residuals | installed |
| Canonical support and schedule definitions | installed |
| Register/Recall type nonreduction | prose proof installed |
| Intrinsic order and finite certificates separated | installed |
| Representation invariance | prose proof installed |
| Backlog and regional fragmentation separated | installed |
| CNS count lemma separated from substantive lift theorem | installed |
| Bridge to published dynamical CNS | installed conditionally |
| Great Filter lemmas decomposed | installed |
| CST metric separated from optional action | installed |
| Lean module and theorem manifest | installed; pinned source + static audit installed; kernel build pending |
| v16 Gate Zero | executed; closed-positive (v8 lineage reproduced) |
| Direct recurrence | executed; closed for the declared synthetic model |
| External-mapping certificate matrix | installed (registration-closed) |
| Same-model receiver propagation | executed (bounded, isolated same-model); cross-model/human pending |
| Repository and reviewer access | pending |



### External completion protocols
**Lean build and independent validation.** Pin the toolchain, replace every documentary sorry, print axiom dependencies, reproduce in an independent environment and archive build logs. **Formalization-fidelity audit.** Freeze the Article, Supplement, registry and declarations; recruit independent registrars; score identity, dependency and warrant recovery. **Receiver propagation study.** Use fresh human or model receivers, hidden target families and second-receiver retransmission without author repair; analyse receiver and claim family, not individual prompts, as the units of inference. **External trace study.** Use version-locked systems, matched tasks, genuinely external traces and a target-aware three-valued monitor; synthetic traces are not samples from current systems. **Historical classification.** Freeze the lift rubric and anti-tuning rules before selecting candidate innovations. **Physical operation mapping.** Test minimal support, factorization and commutation/precedence witnesses for the four physical assignments; failure narrows the cross-FSS hypothesis without defeating the conceptual theorems. **Great Filter branch and hazard studies.** Test branch inheritance, regenerative thresholds, hazard non-summability, correction/dispersal timescales and residue suppression. **Repository closure.** Deposit code, data, registry, Lean files, environment lockfiles, checksums, source figures and manuscript source with reviewer access and a persistent DOI before publication, including regeneration of the absent v8 executable lineage.

The minimum submit-ready projection is the core formal article, a conformant finite witness (either the regenerated v8 lineage or the executed recurrence result standing in its declared model), a clean Lean build or a clearly narrower non-Lean formal positioning, and at least one independent external anchor. The present v15 draft does not invent those missing results.


## References
1. Gärdenfors, P. Conceptual Spaces: The Geometry of Thought (MIT Press, 2000).  
2. Collins, A. M. & Loftus, E. F. A spreading-activation theory of semantic processing. Psychol. Rev. 82, 407-428 (1975).  
3. Krenn, M. & Zeilinger, A. Predicting research trends with semantic and neural networks with an application in quantum physics. Proc. Natl Acad. Sci. USA 117, 1910-1916 (2020).  
4. Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N. & Malone, T. W. Evidence for a collective intelligence factor in the performance of human groups. Science 330, 686-688 (2010).  
5. Hong, L. & Page, S. E. Groups of diverse problem solvers can outperform groups of high-ability problem solvers. Proc. Natl Acad. Sci. USA 101, 16385-16389 (2004).  
6. Lazer, D. & Friedman, A. The network structure of exploration and exploitation. Admin. Sci. Q. 52, 667-694 (2007).  
7. Lorenz, J., Rauhut, H., Schweitzer, F. & Helbing, D. How social influence can undermine the wisdom of crowd effect. Proc. Natl Acad. Sci. USA 108, 9020-9025 (2011).  
8. Murdoch, W. J., Singh, C., Kumbier, K., Abbasi-Asl, R. & Yu, B. Definitions, methods, and applications in interpretable machine learning. Proc. Natl Acad. Sci. USA 116, 22071-22080 (2019).  
9. Rudin, C. Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nat. Mach. Intell. 1, 206-215 (2019).  
10. Christiano, P., Shlegeris, B. & Amodei, D. Supervising strong learners by amplifying weak experts. Preprint at arXiv:1810.08575 (2018).  
11. Irving, G., Christiano, P. & Amodei, D. AI safety via debate. Preprint at arXiv:1805.00899 (2018).  
12. Burns, C. et al. Weak-to-strong generalization: eliciting strong capabilities with weak supervision. Preprint at arXiv:2312.09390 (2023).  
13. Korbak, T. et al. Chain of thought monitorability: a new and fragile opportunity for AI safety. Preprint at arXiv:2507.11473 (2025).  
14. Emmons, S. et al. When chain of thought is necessary, language models struggle to evade monitors. Preprint at arXiv:2507.05246 (2025).  
15. Williams, A. E. Cognitive near-singularity: a possibility theorem and a witness-based protocol with a corpus case study. Front. Artif. Intell. 9, 1746633 (2026).  
16. Wilson, E. B. Probable inference, the law of succession, and statistical inference. J. Am. Stat. Assoc. 22, 209-212 (1927).  
17. Sandve, G. K., Nekrutenko, A., Taylor, J. & Hovig, E. Ten simple rules for reproducible computational research. PLoS Comput. Biol. 9, e1003285 (2013).  
18. Ćirković, M. M. The Great Silence: Science and Philosophy of Fermi's Paradox (Oxford Univ. Press, 2018).  
19. Frank, A. & Sullivan, W. T. A new empirical constraint on the prevalence of technological species in the universe. Astrobiology 16, 359-362 (2016).  
20. Wright, J. T. et al. The G infrared search for extraterrestrial civilizations with large energy supplies. I. Background and justification. Astrophys. J. 792, 26 (2014).  
21. Polyakov, A. M. Quantum geometry of bosonic strings. Phys. Lett. B 103, 207-210 (1981).  
22. Shannon, C. E. A mathematical theory of communication. Bell Syst. Tech. J. 27, 379-423, 623-656 (1948).  
23. de Moura, L., Kong, S., Avigad, J., van Doorn, F. & von Raumer, J. The Lean theorem prover (system description). In Automated Deduction - CADE-25, 378-388 (Springer, 2015).  
24. Lean FRO. The Lean Language Reference, version 4.32.0 (2026).  
25. Carneiro, M. Lean4Lean: towards a verified typechecker for Lean, in Lean. Preprint at arXiv:2403.14064 (2024).  

