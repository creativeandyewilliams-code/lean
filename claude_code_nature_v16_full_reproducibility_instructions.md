# Claude Code Execution Contract for Nature Article and Supplement v16

## Mission

You are operating inside the author's GitHub repository with shell, Python, Git, internet access, Lean execution, document-build tools, and the ability to spawn context-isolated agents.

Your task is **not** to write another plan or merely classify unfinished work. Your task is to execute every gate that can be executed with the repository contents and available tools, update the scientific claims to the exact results obtained, create **Article v16**, **Supplementary Information v16**, and every artifact required for full reproducibility, and bundle the complete release as:

```text
nature_v16_full_reproducibility_package.zip
```

At the end, place the ZIP in a downloadable artifact location and return a direct link to it.

The assignment is incomplete unless that ZIP exists, passes the verification procedure in this document, and contains the final manuscripts, source, data, code, formal proofs, logs, audits, receiver-study artifacts, environment locks, checksums, and build instructions.

---

# 1. Governing execution rules

## 1.1 Execution precedes status reporting

Use this rule throughout:

> **If an item can be executed with available files, tools, public sources, or isolated agents, execute it. Do not substitute a description of the remaining work.**

A report that says “this should be done” is not a deliverable when the environment can do it.

A blocker report is permitted only when the missing input is irreducibly external and cannot be generated, retrieved, measured, or validly approximated in this environment. Before assigning an open status, preserve evidence of the searches and capability checks that establish the blocker.

## 1.2 Do not confuse completion of a status ledger with completion of a gate

These are different:

```text
accurately describing why a task is incomplete
≠
completing the task
```

For each gate, close the underlying procedure wherever possible. Only after execution should you record the result as positive, negative, defeated, bounded, or unresolved.

## 1.3 Positive and negative scientific results are both acceptable

Do not force claims to pass. A gate may close by:

- a kernel-accepted proof;
- a kernel-accepted counterexample;
- a successful conformance audit;
- a failed conformance audit with a precise defect;
- an executed experiment with positive, null, mixed, or defeating results;
- a completed external assessment that narrows or rejects a mapping.

But do not call a gate closed merely because its procedure was never run and its absence was documented.

## 1.4 No silent theorem weakening

When a Lean proof fails:

1. diagnose the actual failure;
2. search for a proof at the frozen statement;
3. try equivalent formal encodings that preserve the statement;
4. construct countermodels;
5. only then change the statement.

Any change to premises, conclusion, domain, equivalence relation, target family, or resource bound must be versioned and propagated to the manuscript and claim ledger.

Allowed dispositions are:

- proof-only repair;
- notation/elaboration repair;
- explicit premise strengthening;
- explicit conclusion weakening;
- domain restriction;
- theorem-to-conjecture or theorem-to-hypothesis demotion;
- removal after a countermodel.

## 1.5 Preserve the projection-level versus carrier-level distinction

Maintain two separate verdicts:

- **formal/global-coherence verdict:** whether the registered formal dependency chain is coherent and kernel-checked within its explicit premises;
- **submission-carrier verdict:** whether code, data, experiments, independent transfer, external evidence, rendering, and repository closure support the manuscript as submitted.

Do not convert a missing carrier into a formal refutation. Do not use formal coherence to promote an unmeasured external premise.

## 1.6 No opposite-claim inversion

State positive claims before scope boundaries. Do not let repeated caveats imply the opposite of the intended mechanism.

For example, preserve the positive claim that typed interactions induce or constrain functional topology through support, schedule, coupling, and admissible transitions. Then state the evidence level of a particular physical mapping.

## 1.7 No new architecture unless execution exposes a typed defeat

Freeze the v16 object inventory after preflight. Do not add new primitive functions, semantic layers, Great Filter properties, action terms, or primary endpoints unless an executed proof, countermodel, audit, or experiment shows the frozen architecture is invalid.

---

# 2. Required source inputs and preflight inventory

## 2.1 Locate the repository inputs

Search the repository, Git history, releases, and attached assets for these items:

```text
nature_v8_full_reproducibility_package*.zip
nature_v8_submission_package/
nature_article_v15.*
nature_supplement_v15.*
nature_v15_revision_experiment_plan*.md
v15_open_gate_closure_note.*
v15_open_gate_closure_package*.zip
independent_llm_lean_gate_closure_instructions*.md
nature_v15_revision*.zip
```

Use `find`, `git ls-files`, `git log --all --name-only`, release assets, and repository search. Do not conclude that an input is absent after checking only the working-tree root.

The v8 package is now expected to be available in the repository. The uploaded reference package had SHA-256:

```text
f21b7ba677c32140710092405a37de460f81a77fe8f6c459a965266eb8842a72
```

If the repository package differs, do not reject it automatically. Preserve both hashes, inspect the contents, and explain whether the difference is a GitHub repackage, a later revision, or a substantive change.

## 2.2 Verify that the v8 lineage is complete

The reference v8 archive contains the artifact classes previously reported missing:

```text
nature_v8_submission_package/
  run_experiment.py
  requirements.txt
  execution_manifest.json
  configs/confirmatory.json
  registry/functions.json
  registry/aliases.json
  registry/obligations.json
  schema/model.schema.json
  schema/event.schema.json
  tests/test_conformance.py
  tests/conformance_results.json
  data/event_log.csv.gz
  data/integrated_trajectories.csv.gz
  data/integrated_summary.csv
  data/key_results.json
  data/regimes.csv
  data/bounded_observation_raw.csv.gz
  data/bounded_observation_summary.csv
  data/model_codewords.csv
  data/model_identification_runs.csv.gz
  data/propagation_surrogate_raw.csv
  data/propagation_surrogate_summary.csv
  figures/*
  manuscript/*.tex
  manuscript/*.pdf
  reports/*
```

Therefore, **do not retain the prior `FAIL_CLOSED_MISSING_EXECUTABLE_LINEAGE` disposition without rerunning Gate Zero**. The v8 executable lineage is now available and the positive conformance procedure is executable.

## 2.3 Record immutable inputs

Create:

```text
review/original/
review/work/
review/results/
review/logs/
```

Copy every input archive and manuscript source into `review/original/`. Do not edit that directory.

Generate:

```text
review/results/input_manifest.json
review/results/input_hashes.sha256
review/results/git_state.json
review/results/environment_preflight.json
```

`git_state.json` must include:

- repository URL;
- commit hash;
- branch;
- dirty status;
- submodule commits;
- Git LFS status;
- timestamp.

## 2.4 Capability preflight

Before assigning any gate as unavailable, test and record:

```text
Python and virtual environments
Lean, Lake, Elan, and the pinned toolchain
Docker or another clean-container mechanism
LaTeX engines and bibliography tools
PDF rendering and inspection tools
GitHub network access
agent/subagent spawning
fresh-context isolation
filesystem access controls
availability of heterogeneous model providers or CLIs
web research and primary-source retrieval
```

Write the exact commands and outputs to:

```text
review/logs/capability_preflight.log
review/results/capability_matrix.json
```

Do not infer a capability from memory. Test it.

---

# 3. Required v16 repository and release structure

Create or normalize the repository into this structure. Existing equivalent directories may be retained, but the final package must have one obvious entry point and no duplicate contradictory source-of-truth files.

```text
nature_v16_full_reproducibility_package/
  README.md
  LICENSE-or-NO-LICENSE-NOTICE.md
  CITATION.cff
  CHANGELOG_v16.md
  release_metadata.json
  package_manifest.json
  MANIFEST.sha256
  Makefile
  run_all.sh
  verify_package.py
  Dockerfile
  docker-compose.yml                  # only if needed
  requirements.in
  requirements.lock
  environment.yml                    # optional but useful
  pyproject.toml                      # if Python package structure is used
  .github/workflows/reproducibility.yml

  original_inputs/
    nature_v8_full_reproducibility_package.zip
    v15_sources/
    input_manifest.json
    input_hashes.sha256

  registry/
    fmi_cns_cst_registry_v16.json
    fss_semantics_v16.json
    operation_topology_v16.json
    cognitive_order_v16.json
    fragmentation_dynamics_v16.json
    cns_bridge_v16.json
    great_filter_claim_ladder_v16.json
    external_premises_v16.json
    experiment_registry_v16.json
    claim_warrant_ledger_v16.json
    theorem_manifest_v16.json
    manuscript_coverage_v16.json
    version_diff_v15_to_v16.json

  lean/
    lean-toolchain
    lakefile.toml
    lake-manifest.json
    FmiCns.lean
    FmiCns/
      Core/
      FMI/
      Projection/
      Order/
      Fragmentation/
      CNS/
      Governance/
      GreatFilter/
      CST/
      External/
      TopLevel/
      Tests/
    reports/
      build.log
      axiom_report.txt
      dependency_report.json
      theorem_coverage.json
      mutation_results.json
      checker_report.txt
      independent_build_report.md

  experiments/
    gate_zero_v16/
      source_v8/
      rebuilt_v8/
      code/
      data/
      logs/
      reports/
    direct_recurrence/
      protocol.json
      code/
      raw/
      derived/
      figures/
      reports/
    reflective_growth/
    governance/
    semantic_equivalence/
    formalization_fidelity/
    lean_mutation/
    cst_geometry_utility/
    receiver_propagation/
    historical_lift/
    physical_fss_mapping/
    external_traces/
    gf_branch_closure/
    gf_hazard_race/

  receiver/
    administration/
    sealed_ground_truth/
    blinded_packets/
    generation_A/
    transmissions/
    generation_B/
    scoring/
    contamination_audit/
    reports/

  external/
    source_registry.json
    cross_fss_semantics/
    force_operation_mapping/
    current_ai_traces/
    historical_lifts/
    branch_closure/
    hazard_timescale_residue/

  data/
    raw/
    derived/
    manuscript_tables/
    source_data/

  figures/
    source/
    generated/
    article/
    supplement/

  manuscript/
    article/
      nature_article_v16.tex
      nature_article_v16.pdf
      nature_article_v16.docx
      nature_article_v16.md
    supplement/
      nature_supplement_v16.tex
      nature_supplement_v16.pdf
      nature_supplement_v16.docx
      nature_supplement_v16.md
    bibliography/
    generated_tables/
    source_figures/
    journal_checklists/
    cover_letter/

  reports/
    executive_gate_report.md
    final_status_vector.json
    gate_zero_v16.md
    lean_formal_closure.md
    formalization_fidelity.md
    receiver_propagation.md
    external_mapping_dispositions.md
    recurrence_reproduction.md
    manuscript_claim_audit.md
    self_containment_audit.md
    portability_audit.md
    independent_reproduction.md
    release_validation.md

  logs/
```

Do not include font files.

---

# 4. Stage A — Freeze the v16 scientific object inventory

Before implementation, create `registry/version_diff_v15_to_v16.json` and a human-readable `CHANGELOG_v16.md`.

Every v15 load-bearing object must receive one disposition:

```text
retain
clarify
strengthen
split
restrict
prove
countermodel
execute
promote
narrow
demote
remove
```

Freeze:

- canonical FSS and endogenous semantic definitions;
- operation identities;
- local/global support definitions;
- parallel/sequential schedule definitions;
- composition equivalence;
- span;
- cognitive order and finite certificates;
- arrival-service fragmentation dynamics;
- CNS lift and published-CNS bridge statements;
- governance theorem;
- Great Filter target classes and lemma family;
- CST semantic geometry;
- external-premise records;
- primary experimental endpoints.

Hash the frozen theorem statement package and experiment protocol package before outcome-bearing execution.

---

# 5. Stage B — Positive v8 Gate Zero rerun

## 5.1 Gate objective

Determine whether every inherited v8 numerical result can be regenerated from the original generator, frozen configuration, registry, source events, schemas, and conformance suite, and determine exactly which v8 objects conform to v16 definitions.

The v8 package is now present. **Do not merely confirm that it exists. Run it.**

## 5.2 Preserve and verify the original v8 archive

1. Copy the archive to `original_inputs/`.
2. Verify `execution_manifest.json` against every listed file.
3. Decompress and hash semantic content where container formats can vary due to timestamps.
4. Record the original model and registry hashes.

Expected reference values include:

```text
model_hash    797b16e309348bbabba0927c4639aae41a7209584d730505e4b451bdaf607bf3
registry_hash b7a6ef0e1d8c5c13f5699cb62142b2965d2391ecda5bd09e2d969eb191ad0385
master_seed   20260715
trajectories  12800
events        102400
witnesses     23
```

## 5.3 Rebuild in a clean environment

Use the exact pinned Python dependency versions in `requirements.txt`:

```text
numpy==2.3.5
pandas==2.2.3
scipy==1.17.0
networkx==3.6.1
matplotlib==3.10.8
scikit-learn==1.7.2
```

Create a clean virtual environment or container. Preserve:

- `pip freeze`;
- Python version;
- platform details;
- command logs;
- runtime;
- stdout/stderr;
- exit codes.

Run from a writable copy, not the immutable original:

```bash
python run_experiment.py
python tests/test_conformance.py
```

Then rebuild the v8 Article and Supplement using their original LaTeX instructions.

## 5.4 Compare regenerated artifacts

Compare all regenerated data with the archived originals.

For CSV and JSON data:

- compare schemas;
- compare row counts;
- compare key uniqueness;
- compare sorted semantic rows;
- compare numerical values at exact precision where deterministic;
- report any floating serialization-only differences separately.

For gzip files, compare decompressed content, not only compressed bytes.

For figures:

- regenerate from source data;
- compare dimensions and normalized pixel content or underlying source data;
- do not require bit-identical PDF metadata.

For manuscripts:

- compare extracted text;
- inspect rendering visually;
- document only nonsemantic timestamp or metadata differences.

## 5.5 Regenerate and verify key results

At minimum, verify these values from regenerated source data rather than copying them from old prose:

```text
full CNS target accuracy                    0.5845588235294118
best matched comparator target accuracy     0.39950980392156865
full CNS certified reach                    0.4349877450980392
best matched comparator certified reach     0.003308823529411765
full CNS recursive reuse                    0.34681372549019607
full CNS Pareto containment                 0.98671875
residual-open/incoherent containment         0.7171875
full CNS harmed fraction                    0.012109375
residual-open/incoherent harmed fraction     0.155712890625
lower-order decoder maximum accuracy        0.4805714285714286
canonical codeword identification accuracy  0.94
correlation-aware held-out log loss          0.258278 approximately
```

Generate manuscript macros and tables directly from regenerated machine-readable outputs.

## 5.6 Audit v8-to-v16 semantic conformance

Do not retroactively claim that v8 implemented semantic fields or theorem objects absent from its code.

For every inherited result, classify:

```text
conformant to v16 definition
partially conformant
nonconformant
undetermined
historical witness only
```

Check:

- one canonical `step` transition;
- no split generator;
- stable model and registry hashes;
- literal versus executed intervention semantics;
- no condition label used as target truth;
- signal-carrier typing;
- stored residuals;
- target-revision separation;
- participant-indexed consequences;
- deterministic replay;
- every metric rebuilt from source events;
- no v16 meaning imputed to an unrepresented v8 variable.

## 5.7 Gate Zero acceptance

Gate Zero becomes **closed-positive** only if:

- the manifest validates;
- the experiment executes cleanly;
- conformance tests pass or all failures are explained and resolved without changing model semantics;
- key data and result tables regenerate;
- the one-generator and event-lineage claims are verified;
- every inherited manuscript claim receives a v16 conformance disposition.

If a discrepancy is found, investigate and either repair an environment/portability issue or narrow the affected claim. Do not stop at “the numbers differ.”

Produce:

```text
reports/gate_zero_v16.md
experiments/gate_zero_v16/reports/gate_zero_v16.json
experiments/gate_zero_v16/reports/result_crosswalk.csv
experiments/gate_zero_v16/reports/reproduction_differences.csv
```

---

# 6. Stage C — Complete the Lean formalization and kernel closure

## 6.1 Scope

The prior bounded Lean core is not sufficient by itself for a claim that the entire v16 formal dependency chain has been checked. Expand it to the complete set of claims actually retained in Article and Supplement v16.

Do not build a second theorem prover. CST and the FSS definitions provide the mathematical object; Lean checks propositions about it.

## 6.2 Pinned project

Use Lean 4.32.0 unless an actual compatibility problem requires a newer pinned version. If the version changes:

- document why;
- preserve the old build attempt;
- pin the new version;
- update all reports.

Pin all imported libraries exactly in `lake-manifest.json`. Prefer a minimal dependency set. If Mathlib is used, pin its commit.

## 6.3 Required formal modules

Implement a coherent module tree covering:

```text
Core: typed metric FSS, endogenous semantics, admissible maps, fitness and continuation
FMI: functions, operation typing, support/schedule, Choice, Register/Recall nonreduction
Projection: first-order and reflective projections, conflation, local stability
Order: composition equivalence, span, finite certification, order, invariance
Fragmentation: obligations, arrival-service dynamics, regional fragmentation, reversal, recurrence
CNS: lift, operand expansion, near-singular content, published dynamical CNS, bridge theorems
Governance: projection adequacy, participantwise option monotonicity, propagation
GreatFilter: target classes, necessary-property lemmas, admissibility, conditional corollary
CST: paths, metric-interaction worldsheet, transport, holonomy, consequence closure, optional action
External: explicit theorem parameters for empirical mappings
TopLevel: formal mechanism and conditional Great Filter theorem
Tests: finite examples, countermodels, mutations
```

## 6.4 Required theorem dispositions

Every retained theorem target must be either kernel-proved, kernel-refuted by counterexample, or explicitly relabeled in the manuscript. No theorem placeholder may remain.

Address at least:

1. T-RSUB — reflective-subspace representation.
2. T-SEM-EQUIV — semantic invariance under admissible pointed isomorphism.
3. T-CONFLATE — first-order conflation.
4. COR-LOCAL-STABILITY.
5. T-REFLECTIVE-NECESSITY.
6. T-OP-NONREDUCTION.
7. T-ORDER-INVARIANCE.
8. T-SPAN-DECIDABLE-FINITE.
9. L-ORDER-INCREMENT.
10. T-UFRAG-QUEUE.
11. T-REGIONAL-FRAG, or a precisely restricted regional theorem.
12. T-SEM-FRAG.
13. T-REVERSAL.
14. T-RECURRENCE.
15. T-CNS-LIFT.
16. T-SING-CONTENT, with all comparator and nonfactorization premises explicit.
17. T-OM — participantwise option monotonicity.
18. T-PROJECTION-ADEQUACY.
19. T-REGENERATIVE-THRESHOLD, if a nontrivial theorem is supportable; otherwise retain a definition and empirical hypothesis.
20. L-GF-UPPER-TAIL.
21. L-GF-BRANCH.
22. L-GF-CAUSAL.
23. L-GF-FIRST-MOVER.
24. L-GF-SUBSTRATE.
25. L-GF-ADAPT.
26. L-GF-OUTCOME.
27. T-GF-CONSTRAINT.
28. T-CNS-ADMISSIBILITY.
29. COR-GF-CNS.
30. T-BRIDGE-LIFT-TO-DYN.
31. T-BRIDGE-DYN-TO-LIFT.
32. T-HOL-INVARIANCE.
33. T-HOL-DRIFT.

## 6.5 Separate definitional lemmas from substantive theorems

The cardinality change after adding a new non-equivalent member is a definitional increment lemma. Do not let it carry the scientific burden of the CNS claim.

The substantive CNS result must expose and prove the additional conditions concerning:

- non-equivalence;
- span;
- preservation and reuse;
- operand-domain expansion;
- reversal of the current fragmentation regime;
- target and resource bounds;
- representation invariance under admissible encodings.

## 6.6 Axiom policy

Release theorems must contain no:

```text
sorry
admit
sorryAx
unregistered axiom
hidden oracle-generated proposition
```

External empirical premises must be theorem parameters, not global axioms.

Run a source scan, but do not confuse it with kernel closure.

For every top-level theorem preserve:

```lean
#print axioms theorem_name
```

Classical or quotient axioms imported by Lean must be reported accurately. Do not call an ordinary reported Lean axiom a custom empirical assumption.

## 6.7 Build and independent checking

Execute:

```bash
lake build
lake env lean FmiCns.lean > lean/reports/axiom_report.txt 2>&1
```

Run an independent checker or kernel replay tool such as `lean4checker` where practical. Preserve the exact version and command.

Then perform a second build in a clean container or fresh clone with no build cache. Compare:

- theorem manifest;
- axiom report;
- generated registry links;
- source hashes;
- build result.

Binary build artifacts need not be byte-identical across platforms, but source-generated theorem and dependency reports must agree.

## 6.8 Mutation suite

Freeze expected outcomes before running. Include mutations that:

- substitute Choice depth for cognitive order;
- remove non-equivalence;
- remove span;
- remove reuse;
- collapse Register into L;
- collapse Recall into G;
- swap support/schedule assignments;
- change a theorem parameter into a global axiom;
- promote GF-3 to GF-6;
- remove participant completeness;
- exchange terminal and observability targets;
- remove successor obligations;
- change the semantic metric while preserving labels;
- change an interaction edge while preserving the metric;
- apply a genuine admissible re-encoding.

Each mutation must produce its preregistered class:

```text
type error
failed theorem
proved counterexample
changed dependency/axiom report
status demotion
no change for true equivalence
```

## 6.9 Formalization-fidelity audit with independent agents

Spawn at least three fresh-context reviewer agents that do not see the canonical adjudication key.

Give each agent blinded pairs of:

- manuscript passage;
- Lean declaration;
- registry record.

Include correct pairs and controlled mismatches. Score preservation of:

- identity;
- scope;
- target;
- warrant;
- boundary conditions;
- external-premise status;
- countermodel representability.

Resolve disagreements by typed witnesses, not majority vote alone.

The Lean gate is not fully closed if proofs compile but the fidelity audit shows that the declarations formalize a materially different claim.

## 6.10 Top-level theorem shape

Provide one theorem for the formal mechanism whose conclusion contains the typed dependency chain, and one conditional Great Filter theorem whose external premises are explicit parameters.

Do not use a vague Boolean named `globallyCoherent` as a substitute for the actual structure.

## 6.11 Lean gate acceptance

The Lean gate becomes closed-positive when:

- all retained release modules build;
- all retained theorem targets have a determinate disposition;
- release proofs contain no `sorry` or unregistered custom axioms;
- axiom reports match the registry;
- mutation tests behave as preregistered;
- formalization fidelity passes or all failed mappings are repaired/narrowed;
- a second clean build succeeds;
- manuscript claims are no stronger than the Lean conclusions.

---

# 7. Stage D — Rebuild the direct recurrence experiment as one canonical execution

## 7.1 Correct the prior reproducibility defect

Do not copy recurrence numbers from an earlier note while shipping a different plotting script.

Create one canonical recurrence program that generates, in one execution:

- protocol JSON;
- every random draw or reconstructible seed stream;
- per-replicate metrics;
- time-series summaries;
- recurrence proportions;
- reversal proportions;
- recurrence times and intervals;
- final backlog values and intervals;
- regional fragmentation counts;
- manuscript table CSV/LaTeX;
- both manuscript figures;
- analysis report.

## 7.2 Frozen design

Retain or explicitly version the registered design:

```text
master seed                20260716
replicates per regime      1000
regions                    12
horizon                    300
lift time                  80
operand expansion time     120
second-lift time           215
regional threshold         12
recurrence window          30
persistent slope threshold 1.0
final backlog threshold    150
```

Regimes:

1. fixed post-lift service;
2. proportional same-order service;
3. regenerative distribution;
4. second order lift;
5. branch heterogeneity.

## 7.3 Use genuine common-world pairing

Pre-generate common latent arrival, service-noise, and branch draws for each replicate. Apply regime-specific policy transformations to the same latent world.

Do not use one RNG sequentially across regimes and describe the result as paired.

Preserve the common-world IDs and seeds in raw data.

## 7.4 Report the actual canonical rerun

If canonical rerun values differ from v15, update Article and Supplement v16 to the rerun. Do not force the old table.

Use paired regime-level contrasts and appropriate hierarchical or exact finite analysis. Do not treat every time step as independent evidence.

## 7.5 Sensitivity and counter-regimes

Run preregistered sensitivity analyses for:

- arrival growth rate;
- service scaling;
- lift magnitude;
- branch heterogeneity and correlation;
- fragmentation threshold;
- recurrence slope/window thresholds;
- second-lift timing;
- regenerative spread rate.

Report regions in which recurrence is present, absent, delayed, or ambiguous.

## 7.6 Recurrence gate acceptance

The recurrence gate closes when the theorem, protocol, raw outputs, analysis, table, and figures are generated by a single reproducible pipeline and a second clean run reproduces the registered outputs.

---

# 8. Stage E — Execute the independent receiver study using isolated agents

## 8.1 Use the environment's multi-agent capability

Do not leave the receiver gate unexecuted merely because one top-level Claude Code session is orchestrating the study.

Independence is created by information isolation, fresh contexts, restricted inputs, and preserved logs—not by requiring multiple physical computers.

## 8.2 Required roles

Create separate agents or sessions for:

```text
ADMINISTRATOR
TASK_GENERATOR
KEY_CUSTODIAN
RECEIVER_A_01 ... RECEIVER_A_n
TRANSMISSION_AUDITOR
RECEIVER_B_01 ... RECEIVER_B_n
SCORER
CONTAMINATION_AUDITOR
STATISTICAL_REVIEWER
```

No receiver may have access to:

- the answer key;
- task-generation rationale;
- another receiver's output;
- author repair;
- hidden source files outside its condition.

The scorer must not alter scoring rules after seeing condition labels.

## 8.3 Isolation implementation

Use the strongest controls available:

- fresh context for every receiver;
- separate working directories or Git worktrees;
- read-only condition packets;
- sealed answer-key directory;
- OS permissions or container isolation where available;
- complete prompts and file-access logs;
- no shared hidden memory;
- deterministic packet hashes.

If same-process subagents cannot be filesystem-isolated, use separate Claude Code invocations or containers. Document residual contamination risk.

## 8.4 Experimental conditions

At minimum compare:

1. Article and Supplement only.
2. Article, Supplement, and registry.
3. Article, Supplement, registry, and direct graph Lean artifact.
4. Article, Supplement, CST semantic geometry, and Lean artifact.
5. Deliberately corrupted formal artifact.
6. Semantically equivalent re-encoding.

Use common hidden claim families across conditions while preventing task leakage.

## 8.5 Receiver sample

Minimum same-model execution:

- at least three fresh Receiver A instances per condition;
- at least one Receiver B instance for each Receiver A retransmission package;
- preferably three Receiver B instances per condition.

If the environment can invoke genuinely different model providers or versions, add at least three receiver families and report family separately from instance.

Do not label multiple instances of one model as multiple model families.

## 8.6 Hidden tasks and primary endpoints

Use the frozen 14 hidden families / 28 randomized tasks if available. Otherwise regenerate them from the frozen protocol before any receiver runs and seal the key.

Families must cover:

- first-order conflation;
- reflection without lift;
- Register type substitution;
- Recall type substitution;
- order, span, novelty, and reuse;
- recurrence and scaled-service countermodels;
- both CNS-bridge directions;
- participant completeness;
- terminal versus observability target;
- GF-3 versus GF-6 promotion;
- benign admissible isomorphism;
- metric or interaction mutation;
- formal theorem versus external premise.

Primary tasks:

1. recover the theorem dependency chain;
2. classify definitions, theorems, finite witnesses, and external premises;
3. execute a novel hidden claim family;
4. identify the minimum missing premise;
5. reject a fatal inversion;
6. predict downstream effects of a definition mutation;
7. create a retransmission package from which Receiver B succeeds.

Primary endpoints:

- novel-target accuracy;
- theorem-status accuracy;
- false proof promotion;
- missing-premise recovery;
- mutation-impact accuracy;
- first-to-second receiver loss;
- second-generation success;
- author-repair count;
- time/cost;
- stage-specific semantic residual.

Diagnostic conformance tasks may be included but must not replace transfer endpoints.

## 8.7 Regenerative protocol

Receiver B receives only:

- Receiver A's retransmission artifact;
- Receiver B instructions;
- Receiver B hidden task packet.

Receiver B must not receive the original Article, Supplement, registry, Lean project, or Receiver A private scratch work unless Receiver A deliberately includes those items in its transmission package.

This tests actual regenerative transfer.

## 8.8 Scoring and contamination audit

Freeze all outputs before unsealing the key. Then score using a preregistered schema.

Audit:

- file accesses;
- prompts;
- context creation times;
- answer-key permissions;
- cross-agent leakage;
- author interaction;
- duplicated task exposure.

Treat agent and claim family as inferential units. Do not treat individual answer tokens as independent observations.

## 8.9 Receiver gate claim level

If only isolated instances of one Claude model are used, the warranted result is:

> regenerative propagation across isolated same-model receiver instances under the tested conditions.

Do not claim cross-model or human propagation.

If heterogeneous model families are validly executed, report the broader result with family-level uncertainty.

The receiver gate closes at the exact level actually executed. It must not remain protocol-only if isolated agents are available.

---

# 9. Stage F — Execute all external and mapping work that is actually available

## 9.1 General rule

For each external mapping, distinguish:

- formal definability;
- source-supported mathematical certificate;
- bounded experiment;
- measured external instantiation;
- universal or civilizational claim.

Execute all available lower levels. Do not leave an item untouched merely because its highest possible claim level cannot be established.

## 9.2 Cross-FSS semantic principle

Formalize and, where possible, prove the invariant-level correspondence:

> functional identity is constituted by metric position, typed interactions, and admissible relational configuration across different FSS operands.

Do not assert object or substrate identity.

This can be closed formally if the definitions and admissible maps are complete.

## 9.3 Physical force-operation mapping

For each proposed assignment:

```text
strong interaction ↔ Register
weak interaction   ↔ Recall
electromagnetism   ↔ L
gravity             ↔ G
```

create a falsification-first certificate containing:

- canonical operational definition of support;
- minimal support family;
- factorization or nonfactorization witness;
- parallel-commutation or sequential-precedence witness;
- physical regime and scale;
- induced topological consequence;
- exact cross-FSS invariant;
- primary-source citations;
- strongest counterargument;
- explicit defeaters;
- reviewer verdict.

Spawn independent physics-review agents to challenge each certificate. Use primary sources and standard mathematical physics references, not blogs or popularity summaries.

A failed assignment narrows the mapping and CST alphabet; it does not defeat the conceptual CNS theorem unless the theorem explicitly depends on that assignment.

## 9.4 External AI traces

If version-locked external model APIs or CLIs are available:

- freeze models and prompts;
- construct genuinely target-different collapsed pairs;
- collect traces without label leakage;
- apply the target-aware three-valued monitor;
- preserve raw responses and metadata;
- use model family as an inference level.

If only Claude instances are available, execute a bounded Claude-family trace study and label it accordingly. Do not call it a three-family external study.

## 9.5 Historical lift classification

Execute a bounded, preregistered historical audit rather than leaving it as a protocol.

Before reading candidate-specific outcomes:

- freeze the candidate set;
- freeze the rubric;
- freeze evidence rules;
- include positive candidates, negative controls, and ambiguous cases.

Have independent agents classify:

- prior-order representability;
- pre-existing compositions;
- new non-equivalent composition;
- span;
- reuse;
- operand expansion;
- adoptability;
- comparator closure;
- participant consequences;
- uncertainty.

Report agreement and typed disagreement. Do not tune the rubric per candidate.

## 9.6 Branch and hazard experiments

Execute the model-regime studies that are possible:

- heterogeneous branching;
- shared versus independent vulnerability;
- subcritical and supercritical regenerative propagation;
- correction versus hazard race;
- summable versus non-summable hazards;
- residue-preserving terminal outcomes;
- observability loss without extinction.

These can close synthetic/mechanistic experiment gates. They cannot establish real civilization-level extinction probabilities.

## 9.7 External mapping disposition

For every mapping, publish one of:

```text
formal certificate closed
bounded external experiment closed
supported at claim level GF-n
narrowed
refuted for the tested definition
empirically unresolved
not executable because of a precisely documented external input
```

An “empirically unresolved” result is permitted only after all accessible formal, source, synthetic, and multi-agent work has been executed.

---

# 10. Stage G — CST semantic geometry and comparative utility

## 10.1 Preserve endogenous semantics

The CST representation must encode semantic identity through:

- the FSS metric or metric family;
- typed interactions;
- relative position;
- boundary and admissibility conditions;
- fitness and continuation conditions;
- admissible transport and deformation.

Do not treat semantics as an external prose label attached after formalization.

## 10.2 Separate constitutive metric from optional action

The metric and interaction topology may be load-bearing. A weighted Polyakov-like action is not automatically load-bearing.

Represent fatal identity, type, contract, warrant, or boundary defects as ill-typed constructions or unprovable propositions. Do not allow a low finite action to compensate for logical invalidity.

## 10.3 Holonomy

Formalize semantic transport around loops and prove:

- invariance for admissible closed transport;
- detection of registered drift for a known nontrivial loop.

## 10.4 Comparative utility experiment

Compare:

```text
prose only
registry only
direct typed graph + Lean
CST worldsheet + Lean
CST + optional action
CST ablations
```

Measure:

- representation size;
- proof effort;
- receiver reconstruction time;
- equivalent-encoding stability;
- novel-target execution;
- semantic-drift detection;
- regenerative retransmission;
- registration cost.

Promote string-specific machinery only if it adds measurable value beyond direct typed graph formalization. If it does not, retain the semantic FSS and Lean core and demote the string-specific extension without weakening the central result.

---

# 11. Stage H — Create Article v16 and Supplement v16

## 11.1 Draft only from frozen executed results

Do not begin final manuscript projection until:

- Gate Zero has a rerun disposition;
- Lean theorem statuses are frozen;
- recurrence outputs are canonical;
- receiver outputs are scored;
- external mapping dispositions are frozen;
- claim-warrant ledger is current.

## 11.2 Article v16 requirements

Article v16 must:

- remain self-contained at the Article's declared level;
- state endogenous metric-interaction semantics positively;
- distinguish reflection, cognitive order, and dynamical convergence;
- separate the order-increment lemma from substantive CNS results;
- report Gate Zero using the actual v8 rerun;
- report the canonical recurrence rerun;
- report Lean kernel closure at the exact theorem coverage achieved;
- report the executed multi-agent receiver result at the exact family/instance level;
- keep external mappings at their measured claim-ladder level;
- state Great Filter claims through the necessary-properties-first funnel;
- avoid scope language that creates an opposite-claim attractor;
- contain no placeholders, invented DOI, or unavailable repository link.

## 11.3 Supplement v16 requirements

Supplement v16 must be the complete formal, computational, experimental, and status record. It should include:

1. complete typed metric FSS definitions;
2. endogenous semantic identity and admissible isomorphism;
3. reflective subspace and signal residuals;
4. projection and conflation proofs;
5. FMI function contracts;
6. support/schedule definitions and certificates;
7. Register/Recall nonreduction;
8. composition equivalence, span, order, finite certification, and invariance;
9. arrival-service and regional fragmentation mathematics;
10. reversal and recurrence theorem and experiment;
11. CNS lift and near-singular content;
12. published dynamical-CNS bridge;
13. governance and regenerative propagation;
14. decomposed Great Filter lemma family, theorem, corollary, ladder, and countermodels;
15. CST metric, paths, transport, holonomy, closure, and optional action;
16. Lean module and theorem manifest;
17. axiom and dependency report;
18. Gate Zero v16 audit and v8 rerun;
19. formalization-fidelity and mutation studies;
20. receiver propagation experiment, including second generation;
21. CST utility results;
22. external trace, historical, physical, branch, and hazard studies actually executed;
23. registry and claim ledger;
24. standalone-completeness audit;
25. repository and reproduction instructions.

Each Supplementary Note should begin with a concise local purpose/role/payoff map.

## 11.4 Canonical numerical source

Every table and numerical sentence must be generated from machine-readable source data or macros. Do not hand-copy results from an earlier note.

## 11.5 Required manuscript formats

Produce:

```text
nature_article_v16.tex
nature_article_v16.pdf
nature_article_v16.docx
nature_article_v16.md
nature_supplement_v16.tex
nature_supplement_v16.pdf
nature_supplement_v16.docx
nature_supplement_v16.md
```

The LaTeX sources are canonical. DOCX and Markdown are projections and must not silently change definitions.

## 11.6 Figures and tables

Generate all figures from source code and source data. Number figures in order. Ensure labels are legible at publication scale.

Produce a source-data file for each figure and table.

## 11.7 References

Verify every citation against the cited source. Use primary sources for technical claims. Do not retain references that do not support the nearby sentence.

## 11.8 Availability and AI statements

Data and code availability statements must describe the files actually in the ZIP. Do not claim the package contains a Lean project, task bank, raw data, or audit code unless it does.

State AI assistance accurately, including multi-agent receiver roles and the distinction between authoring agents and blinded receiver agents.

---

# 12. Stage I — Full reproducibility engineering

## 12.1 One-command rebuild

`run_all.sh` and `make all` must:

1. validate original inputs;
2. install or check environments;
3. rerun Gate Zero or verify its frozen rerun outputs;
4. build Lean;
5. run axiom and mutation audits;
6. run canonical recurrence;
7. run all noninteractive experiments;
8. regenerate tables and figures;
9. build Article and Supplement;
10. run PDF/text/figure preflight;
11. regenerate reports and manifests;
12. verify the final package.

Interactive or costly receiver/external API runs may have separate commands, but their frozen raw outputs and exact replay/analysis scripts must be included.

## 12.2 Environment locks

Include:

- exact Python dependency lock;
- Lean toolchain and Lake manifest;
- TeX engine/package report;
- Dockerfile or equivalent clean environment;
- external model/version metadata;
- operating system and architecture.

## 12.3 Portability

No source file may contain an execution-critical absolute path such as:

```text
/home/user/...
/mnt/data/...
/Users/name/...
```

Resolve paths relative to repository root or source-file location.

Run a portability scan and preserve the result.

## 12.4 Artifact truth audit

Programmatically compare the README and manuscript availability statements to the actual archive contents.

Fail the build if a claimed file class is absent.

## 12.5 Placeholder and bypass scans

Scan for:

```text
TODO
TBD
REPOSITORY DOI
PRIVATE REVIEWER LINK
INSERT
PLACEHOLDER
sorry
sorryAx
admit
unregistered axiom
```

Allow literal mentions inside audit documentation only when explicitly whitelisted.

## 12.6 PDF and DOCX validation

For both manuscripts:

- rebuild from extracted ZIP in a fresh directory;
- verify page count;
- render every PDF page;
- inspect for clipping, overlaps, missing glyphs, unreadable figures, and incorrect numbering;
- extract text and compare with canonical source;
- open DOCX and check headings, equations, figures, tables, and references.

## 12.7 Independent reproduction

Spawn an independent build agent in a clean context. Give it only the final candidate ZIP and the README.

It must:

- extract the archive;
- follow documented commands;
- rebuild Lean;
- reproduce generated reports;
- rebuild manuscripts;
- run `verify_package.py`;
- report discrepancies without author repair.

Repair the package and repeat until the independent build passes.

## 12.8 Package verification script

`verify_package.py` must check at least:

- ZIP/tree completeness;
- manifest and SHA-256 hashes;
- absence of broken symlinks;
- no absolute-path dependencies;
- required gate reports;
- Lean build evidence;
- axiom report presence;
- recurrence raw/derived/table consistency;
- Gate Zero result crosswalk;
- receiver raw outputs and scoring;
- manuscript-to-registry coverage;
- figure/table source data;
- no unapproved placeholders;
- Article and Supplement rebuild success;
- availability statements match contents.

Return nonzero on any failure.

---

# 13. Final gate matrix and manuscript consequence rules

Publish `reports/final_status_vector.json` with separate fields for:

```text
v8 Gate Zero
Lean bounded-core build
Lean full retained-theorem coverage
formalization fidelity
semantic-equivalence mutation
order/fragmentation mathematics
direct recurrence
same-model multi-agent receiver propagation
cross-family receiver propagation
CST comparative utility
physical force mapping
external AI traces
historical classification
Great Filter branch experiment
Great Filter hazard/timescale/residue mapping
repository rebuild
journal carrier
```

Allowed statuses:

```text
closed-positive
closed-negative
closed-bounded
partially closed
empirically unresolved
defeated
not retained
```

For every non-positive status, state the exact manuscript consequence. Examples:

- order invariance fails → report representation-relative certification;
- Register/Recall nonreduction fails → revise operation inventory;
- regional fragmentation theorem fails → retain backlog theorem, remove regional claim;
- dynamical bridge fails → treat the two CNS notions as distinct;
- CST adds no utility → demote string-specific layer;
- receiver succeeds only within Claude → claim same-model transfer only;
- physical mapping fails → narrow mapping, preserve conceptual theorem;
- v8 rerun fails → remove or relabel affected inherited numbers.

Do not use one aggregate “complete” label to erase component statuses.

---

# 14. Final release construction

## 14.1 Build the release directory

The root directory inside the ZIP must be exactly:

```text
nature_v16_full_reproducibility_package/
```

The ZIP filename must be exactly:

```text
nature_v16_full_reproducibility_package.zip
```

## 14.2 Generate final hashes

After all files are frozen:

```bash
find nature_v16_full_reproducibility_package -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > nature_v16_full_reproducibility_package/MANIFEST.sha256
```

Generate `package_manifest.json` with path, size, SHA-256, MIME type, source/generated status, and producing command.

## 14.3 Verify from a fresh extraction

Before delivery:

```bash
rm -rf /tmp/nature_v16_verify
mkdir -p /tmp/nature_v16_verify
unzip -q nature_v16_full_reproducibility_package.zip -d /tmp/nature_v16_verify
cd /tmp/nature_v16_verify/nature_v16_full_reproducibility_package
python verify_package.py
make all
```

Also run:

```bash
unzip -t nature_v16_full_reproducibility_package.zip
```

Do not deliver until all required checks pass.

## 14.4 Final independent sign-off

Have a fresh reviewer agent inspect only the final ZIP and produce:

```text
reports/final_independent_signoff.md
```

The sign-off must state:

- what was rebuilt;
- what matched;
- what did not;
- whether the ZIP is internally truthful;
- exact open external claims;
- whether Article and Supplement match the evidence.

## 14.5 Deliver the artifact

Copy the verified ZIP to the environment's downloadable artifact directory. In the final response provide:

```markdown
[Download nature_v16_full_reproducibility_package.zip](<actual-downloadable-artifact-URL>)
```

Also summarize the final gate statuses in no more than a short paragraph. Do not replace the link with a repository path that the user cannot download.

---

# 15. Non-negotiable failure conditions

The assignment is not complete if any of the following is true:

- the final ZIP does not exist;
- the v8 package is present but Gate Zero was not rerun;
- Lean is available but `lake build` was not executed;
- theorem failures were hidden by weakening claims without a change report;
- multiple agents were available but the receiver study remained protocol-only;
- recurrence numbers were copied from an older note rather than generated by included code;
- recurrence conditions were described as paired without common latent worlds;
- Supplement or Article cannot rebuild from the extracted ZIP;
- any required image path is absolute;
- availability statements claim absent files;
- the ZIP omits raw data, logs, or scoring outputs needed to reproduce a reported result;
- Article and Supplement disagree on a canonical definition;
- external premises were promoted to Lean axioms;
- a synthetic Great Filter model was described as a real extinction estimate;
- a same-model receiver experiment was described as cross-family evidence;
- the final response provides no downloadable link.

---

# 16. Recommended execution order

Execute in this order and do not stop after writing plans:

```text
1. immutable input and capability preflight
2. v16 object inventory and freeze
3. v8 manifest validation and positive Gate Zero rerun
4. Lean statement freeze, proof completion, axiom audit, mutation suite
5. formalization-fidelity agent audit
6. canonical paired recurrence rerun
7. semantic-equivalence and CST utility experiments
8. isolated Receiver A and Receiver B study
9. physical, historical, AI-trace, branch, and hazard tracks that are executable
10. freeze all results and claim statuses
11. write Article v16 and Supplement v16
12. generate all tables and figures from source data
13. build complete reproducibility tree
14. independent clean rebuild
15. package verification
16. create exact ZIP and provide download link
```

Do not return a response after steps 1–10 saying what remains to be done. Continue through step 16 unless an irreducible external blocker affects only a bounded external claim. Such a blocker must narrow the manuscript; it must not prevent creation of the fully reproducible v16 package for everything actually executed.
