# Independent LLM Reviewer Instructions for Closing the FMI–CNS v15 Open Gates

## Purpose

These instructions are for an **independent LLM reviewer** operating in an environment that can execute Lean, shell commands, and Python. The reviewer’s task is to close every open item identified in `v15_open_gate_closure_note` **where closure is actually possible**, while preserving the paper’s distinction between:

1. formal proof closure;
2. software and computational conformance;
3. independent semantic propagation;
4. external empirical mapping; and
5. manuscript-carrier readiness.

A gate is not closed merely because the reviewer can write plausible prose about it. Closure requires execution of a frozen procedure and preservation of the resulting evidence. A negative or undetermined result is a valid closure disposition when the registered procedure warrants it.

The source note reports the five-gate status as:

```text
Lean kernel build          partially closed
v15 Gate Zero audit        closed-negative
Direct recurrence          closed-positive in the declared synthetic model
Independent receiver study partially closed
External mappings          partially closed
```

The instructions below also address a deeper limitation identified by the note: the supplied Lean package is a **bounded formal core**, not yet the complete Lean formalization required to claim that the entire Article and Supplement have been kernel-checked for conditional global coherence.

---

# 1. Reviewer role, independence, and non-negotiable rules

## 1.1 Reviewer role

Act as an auditor, theorem reviewer, replication investigator, and experimental receiver. Do not act as an advocate whose task is to force every claim to pass.

Your output must distinguish:

- **proved**: a proposition was accepted by the pinned Lean kernel and its axiom dependencies were audited;
- **proved relative to explicit premises**: the proof is valid, but its theorem parameters include external or class assumptions;
- **software-conformant**: code was executed and satisfied the frozen software specification;
- **finite constructive witness**: an example or finite experiment instantiated a formal mechanism;
- **empirically supported mapping**: external evidence supports a mapping at a declared claim level;
- **undetermined**: available evidence or proof budget did not close either the proposition or its negation;
- **defeated**: a typed counterexample, failed proof, failed audit, or contradictory evidence defeats the registered claim as stated.

## 1.2 Independence requirements

Record all of the following before beginning:

```json
{
  "reviewer_model": "<exact model and version>",
  "provider": "<provider>",
  "review_context_created_at_utc": "<timestamp>",
  "tool_environment": "<container/VM identifier>",
  "network_access": true,
  "lean_execution": true,
  "author_interaction_allowed": false,
  "answer_key_access_during_receiver_run": false,
  "prior_exposure_to_hidden_tasks": false
}
```

The reviewer must not:

- ask the author to repair an answer before a primary endpoint is recorded;
- read the receiver-study answer key before completing the blinded receiver run;
- silently weaken theorem statements to make Lean compile;
- convert an external premise into a global Lean axiom merely to obtain a theorem;
- count a static source scan as kernel proof;
- treat successful compilation of a theorem as proof that the theorem statement faithfully represents the manuscript;
- infer empirical truth from a synthetic experiment;
- promote a GF-3 conditional result to GF-4, GF-5, or GF-6 without the required external evidence;
- hide a negative audit result by calling the gate “pending.”

## 1.3 Fail-closed rule

For every gate, use:

```text
absence of a detected problem ≠ closure
formal proof closure ≠ empirical instantiation
successful source parsing ≠ Lean kernel acceptance
agreement with the paper ≠ regenerative understanding
```

When required inputs are missing, report the precise missing inputs and issue a fail-closed or partial disposition. Do not fabricate substitutes.

## 1.4 Statement-preservation rule

Before editing any Lean theorem declaration:

1. save the original declaration;
2. record its SHA-256 hash;
3. record the corresponding manuscript claim;
4. classify the proposed change as one of:
   - proof-only repair;
   - notation/elaboration repair;
   - premise strengthening;
   - conclusion weakening;
   - domain restriction;
   - theorem-to-conjecture demotion;
   - removal after countermodel;
5. generate a claim-impact report.

A proof-only repair may preserve the theorem’s status. Any semantic statement change requires a new theorem version and manuscript status update.

---

# 2. Required inputs

## 2.1 Minimum package

Obtain these files:

```text
v15_open_gate_closure_package.zip
v15_open_gate_closure_note.tex
v15_open_gate_closure_note.pdf
nature_article_v15.md
nature_supplement_v15.md
nature_v15_revision_experiment_plan.md
```

The closure archive should contain at least:

```text
v15_gate_closure/
  README.md
  run_all.sh
  package_manifest.json
  lean/
    lean-toolchain
    lakefile.toml
    FmiCns.lean
    FmiCns/
      Basic.lean
      Semantics.lean
      Projection.lean
      Operations.lean
      Order.lean
      Backlog.lean
      GreatFilter.lean
  code/
    gate_zero_audit.py
    static_lean_audit.py
    direct_recurrence.py
    make_receiver_tasks.py
  data/
  receiver/
  external/
  audit/
  figures/
```

## 2.2 Conditional Gate Zero inputs

A positive Gate Zero rerun additionally requires the original v8 execution lineage:

```text
v8 generator source
raw append-only event log
trajectory table
canonical v8 registry
frozen v8 configuration
v8 conformance suite
v8 environment lock
source figure data
v8 checksums or signed manifest
```

If these are unavailable, a **positive** Gate Zero result cannot be produced. The independent reviewer can still reproduce and confirm the existing closed-negative disposition.

## 2.3 Conditional external-mapping inputs

External mapping closure requires domain-specific evidence. Depending on the mapping, this may include:

- primary physical-theory sources and explicit mathematical witnesses;
- version-locked external AI systems or traces;
- historical source records selected after rubric freeze;
- branch, hazard, timescale, and residue datasets or defensible external models;
- independent domain reviewers.

Lean access alone does not supply these inputs.

---

# 3. Establish an immutable review workspace

## 3.1 Preserve the original archive

```bash
set -euo pipefail
mkdir -p review/original review/work review/results review/logs
cp v15_open_gate_closure_package.zip review/original/
sha256sum review/original/v15_open_gate_closure_package.zip \
  | tee review/results/closure_archive_sha256.txt
unzip -q review/original/v15_open_gate_closure_package.zip -d review/work
```

Do not edit `review/original`.

## 3.2 Normalize the directory layout

The supplied Python scripts contain absolute paths rooted at `/mnt/data`. Use one of these two methods.

### Preferred method: reproduce the expected layout

```bash
sudo mkdir -p /mnt/data
sudo rm -rf /mnt/data/v15_gate_closure
sudo cp -a review/work/v15_gate_closure /mnt/data/v15_gate_closure
sudo cp nature_article_v15.md /mnt/data/
sudo cp nature_supplement_v15.md /mnt/data/
sudo cp nature_v15_revision_experiment_plan.md /mnt/data/
```

### Alternative method: parameterize the scripts

Replace hard-coded roots with command-line arguments or environment variables. Every modification must be recorded in:

```text
review/results/path_portability_patch.diff
review/results/path_portability_patch_sha256.txt
```

A portability patch may change paths only. It may not change audit logic, thresholds, seeds, theorem statements, or expected outcomes.

## 3.3 Validate the internal manifest

Run this from the extracted package root:

```bash
cd /mnt/data/v15_gate_closure
python - <<'PY'
from __future__ import annotations
import hashlib
import json
from pathlib import Path

root = Path('.')
manifest = json.loads((root / 'package_manifest.json').read_text())

# Adapt the key names only if the manifest schema visibly differs.
entries = manifest.get('files', manifest)
errors = []

if isinstance(entries, dict):
    iterable = [dict(path=k, **v) if isinstance(v, dict) else {'path': k, 'sha256': v}
                for k, v in entries.items()]
else:
    iterable = entries

for item in iterable:
    path = Path(item['path'])
    if not path.exists():
        errors.append(f'MISSING {path}')
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = item.get('sha256')
    if expected and actual != expected:
        errors.append(f'HASH_MISMATCH {path} expected={expected} actual={actual}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('PACKAGE_MANIFEST_OK')
PY
```

If the manifest schema differs, inspect it and write a separate validation script. Do not skip validation.

## 3.4 Capture the environment

```bash
{
  date -u +'%Y-%m-%dT%H:%M:%SZ'
  uname -a
  cat /etc/os-release 2>/dev/null || true
  python --version
  git --version
  curl --version | head -1
} | tee review/results/environment_before.txt
```

---

# 4. Install and pin Lean

The project pins:

```text
leanprover/lean4:v4.32.0
```

Lean 4.32.0 is the required first-pass toolchain. Do not upgrade the project before reproducing the pinned build.

## 4.1 Install `elan`

On a fresh Linux environment:

```bash
sudo apt-get update
sudo apt-get install -y git curl build-essential unzip jq python3 python3-pip
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y
source "$HOME/.elan/env"
```

Verify:

```bash
elan --version
```

## 4.2 Install the pinned toolchain

```bash
cd /mnt/data/v15_gate_closure/lean
elan toolchain install leanprover/lean4:v4.32.0
elan show | tee ../../review/results/elan_show.txt
lean --version | tee ../../review/results/lean_version.txt
lake --version | tee ../../review/results/lake_version.txt
cat lean-toolchain | tee ../../review/results/lean_toolchain_pin.txt
```

The versions used by `lean` and `lake` must agree with the project pin.

## 4.3 Do not replace the pin during the first audit

If 4.32.0 cannot be obtained, the build gate remains open. A build under another Lean release is a portability test, not the registered kernel closure.

---

# 5. Close the bounded Lean kernel-build gate

This section closes the gate represented by the **existing seven-module bounded package**. It does not, by itself, justify the broader claim that every v15 theorem has been formalized.

## 5.1 Preserve source hashes

```bash
cd /mnt/data/v15_gate_closure
find lean -type f -print0 | sort -z | xargs -0 sha256sum \
  | tee review/results/lean_source_hashes_before.txt
```

## 5.2 Run the static audit

```bash
python code/static_lean_audit.py \
  2>&1 | tee review/logs/static_lean_audit.log
cp audit/lean_static_audit.json review/results/
```

The static scan is diagnostic only.

## 5.3 Build the project

```bash
cd lean
rm -rf .lake
set -o pipefail
lake build 2>&1 | tee ../review/logs/lake_build.log
```

A nonzero exit status means the kernel gate is not closed.

## 5.4 Repair policy for build failures

For each failure:

1. copy the failing source file to `review/original_lean_failures/`;
2. classify the failure:
   - syntax;
   - missing import;
   - namespace mismatch;
   - elaboration ambiguity;
   - tactic failure;
   - false theorem;
   - theorem too strong;
   - incompatible API change;
3. attempt the smallest proof-preserving repair;
4. run `git diff --no-index` or `diff -u` against the original;
5. write a repair record containing:

```json
{
  "file": "FmiCns/Example.lean",
  "declaration": "FmiCns.example_theorem",
  "failure_class": "tactic_failure",
  "statement_changed": false,
  "proof_changed": true,
  "reason": "<precise reason>",
  "reviewer_assessment": "proof-preserving elaboration repair"
}
```

Forbidden repairs:

- `sorry`;
- `admit`;
- `axiom` used to assert the missing result;
- changing a theorem to `True` or a vacuous proposition;
- introducing an unrestricted `combine` function that merely assumes the conclusion unless the theorem is explicitly labeled as a composition lemma;
- using native computation in a way that introduces unreported trusted axioms;
- deleting a theorem from the release manifest without a status disposition.

## 5.5 Run all `#print axioms` commands

The supplied top-level file prints axioms for seven declarations:

```bash
lake env lean FmiCns.lean \
  2>&1 | tee ../review/results/axiom_report_supplied.txt
```

Acceptable built-in axioms, when present, are ordinarily:

```text
propext
Classical.choice
Quot.sound
```

The following fail the release gate unless explicitly registered and justified:

```text
sorryAx
Lean.trustCompiler
any project-defined axiom
any imported nonstandard axiom not listed in the theorem registry
```

## 5.6 Generate a complete theorem axiom audit

The supplied `FmiCns.lean` does not print every theorem in every module. Generate an audit file covering all theorem declarations.

```bash
cd /mnt/data/v15_gate_closure/lean
python - <<'PY'
from __future__ import annotations
import re
from pathlib import Path

mods = sorted((Path('FmiCns')).glob('*.lean'))
imports = [f'import FmiCns.{p.stem}' for p in mods]
names = []
for p in mods:
    for line in p.read_text().splitlines():
        m = re.match(r'\s*theorem\s+([A-Za-z0-9_]+)', line)
        if m:
            names.append('FmiCns.' + m.group(1))

out = imports + [''] + [f'#print axioms {name}' for name in names] + ['']
Path('AllAxioms.lean').write_text('\n'.join(out))
print('\n'.join(names))
PY

lake env lean AllAxioms.lean \
  2>&1 | tee ../review/results/axiom_report_all_theorems.txt
```

Store the list of declarations in `review/results/bounded_theorem_manifest.txt`.

## 5.7 Replay compiled declarations through `lean4checker`

First inspect available syntax:

```bash
lake env lean4checker --help \
  | tee ../review/results/lean4checker_help.txt
```

Then run a fresh replay. The expected module invocation is:

```bash
lake env lean4checker --fresh FmiCns \
  2>&1 | tee ../review/results/lean4checker_fresh.log
```

If the installed command requires a module path or `.olean` path instead, use the syntax reported by `--help` and record the exact command.

A `lean4checker` failure blocks closure even if `lake build` succeeded.

## 5.8 Scan for bypass mechanisms

```bash
cd /mnt/data/v15_gate_closure/lean
grep -R -n -E \
  'sorry|sorryAx|\badmit\b|\baxiom\b|debug\.skipKernelTC|trustCompiler|native_decide|decide \+native|implemented_by|extern' \
  . | tee ../review/results/lean_bypass_scan.txt || true
```

Every match must be reviewed. Matches in comments still need classification but do not automatically fail.

## 5.9 High-assurance validation for AI-generated proofs

Treat unreviewed AI-generated proof code as potentially adversarial. At minimum:

1. build in a sandboxed disposable environment;
2. run `lean4checker --fresh`;
3. preserve the trusted theorem statements separately from proof bodies;
4. where available, use Lean’s `comparator` workflow or an independent external checker such as `nanoda`;
5. do not allow the proof package to modify the trusted challenge statements during validation.

If `comparator` is installed:

```bash
lake env comparator --help \
  | tee ../review/results/comparator_help.txt
```

Follow the pinned Lean documentation for creating a trusted challenge file and comparing the submitted proof. Preserve the full command line and logs. If comparator is unavailable, state this explicitly; do not claim gold-standard malicious-proof resistance.

## 5.10 Rebuild in a second clean environment

Use a fresh container or VM with no `.lake` directory and no copied Lean build cache.

```bash
# In clean environment 2
unzip -q v15_open_gate_closure_package.zip
cd v15_gate_closure/lean
source "$HOME/.elan/env"
elan toolchain install leanprover/lean4:v4.32.0
rm -rf .lake
lake build 2>&1 | tee build_environment_2.log
lake env lean AllAxioms.lean 2>&1 | tee axiom_environment_2.log
lake env lean4checker --fresh FmiCns 2>&1 | tee checker_environment_2.log
find . -type f \( -name '*.lean' -o -name '*.olean' \) -print0 \
  | sort -z | xargs -0 sha256sum > build_environment_2_hashes.txt
```

Compare:

```bash
diff -u environment_1_source_hashes.txt environment_2_source_hashes.txt
```

`.olean` hashes may contain environment-sensitive differences; if they differ, document them and compare declaration and axiom reports. Source hashes must match exactly.

## 5.11 Bounded Lean gate acceptance criteria

Mark the bounded Lean kernel gate **closed-positive** only if:

- the pinned Lean 4.32.0 build succeeds;
- every theorem body is kernel-accepted;
- all release theorems are covered by an axiom report;
- no theorem depends on `sorryAx` or an unregistered custom axiom;
- `lean4checker --fresh` succeeds;
- a second clean environment reproduces the build and reports;
- every source modification is classified and preserved;
- theorem statements have not been silently weakened.

If the build fails because a theorem is false or too strong, issue a **closed-negative theorem disposition** for that declaration and update the manuscript claim. Do not leave it vaguely open.

---

# 6. Do not confuse the bounded build with full v15 formal closure

The current package explicitly omits several load-bearing objects. A successful build proves only that the supplied bounded theorem shapes compile. To claim **Lean-checked conditional coherence of Article and Supplement v15**, complete the full theorem and definition package below.

## 6.1 Required canonical definitions

Create standalone Lean definitions for:

```text
D-FSS                     typed metric functional state space
D-ADMISSIBLE-ISO          target-relevant pointed FSS isomorphism
D-SEMANTIC-IDENTITY       semantic identity under admissible isomorphism
D-TARGET-KERNEL           minimum target-complete support / finite signature
D-SIGNAL-BOUNDARY         signal, Register, Express, and four residuals
D-FMI-FUNCTIONS           canonical external, conceptual, and internal functions
D-SUPPORT                 minimal support, local factorization, global nonfactorization
D-SCHEDULE                parallel commutation and sequential precedence
D-COMPOSITION-EQUIVALENCE functional equivalence over domain and target language
D-SPAN                    intrinsic span and finite span certificate
D-COGNITIVE-ORDER         canonical order and finite lower-bound certificate
D-OBLIGATION-DYNAMICS     arrivals, service, backlog, regional graph, semantic burden
D-ADM-SUB                 admissible operand family and order-lift expansion
D-IMPORTANCE              structural displacement, consequence field, magnitude, valence
D-REGENERATE              reconstruction, hidden execution, retransmission
D-GF-TARGETS              terminal and observability filter classes
D-CST-WORLDSHEET          typed path family in conceptual-fitness FSS
D-CONSEQUENCE-CLOSURE     monotone consequence operator, least fixed point, admissibility
D-LEAN-STATUS             external reporting map to gc/gi/u
```

`D-LEAN-STATUS` belongs outside the proof kernel. It must report proof status; it must not manufacture proofs.

## 6.2 Recommended full module tree

```text
lean/
  lean-toolchain
  lakefile.toml
  lake-manifest.json
  FmiCns/
    Core/
      Types.lean
      FSS.lean
      Semantics.lean
      Signal.lean
      Fitness.lean
    FMI/
      Functions.lean
      Operations.lean
      Choice.lean
      Topology.lean
      NonReduction.lean
    Projection/
      FirstOrder.lean
      Reflective.lean
      Conflation.lean
    Order/
      Composition.lean
      Span.lean
      CognitiveOrder.lean
      Invariance.lean
    Fragmentation/
      Obligations.lean
      QueueTheorems.lean
      RegionalFragmentation.lean
      Reversal.lean
      Recurrence.lean
    CNS/
      Lift.lean
      NearSingularContent.lean
      PublishedDynamic.lean
      Bridge.lean
    Governance/
      ProjectionAdequacy.lean
      OptionMonotonicity.lean
      Propagation.lean
    GreatFilter/
      Targets.lean
      Assumptions.lean
      NecessaryProperties.lean
      Admissibility.lean
      ConditionalCorollary.lean
    CST/
      Paths.lean
      Worldsheet.lean
      Transport.lean
      Holonomy.lean
      Closure.lean
      OptionalAction.lean
    External/
      Premises.lean
    TopLevel/
      FormalCoherence.lean
      ConditionalFilter.lean
    Tests/
      Mutations.lean
      FiniteExamples.lean
      Countermodels.lean
```

This tree may be simplified, but every load-bearing declaration must have a stable name and theorem-manifest entry.

## 6.3 Required theorem package

Each theorem below must receive one of five final statuses:

```text
proved
proved under exposed premises
restricted and proved
conjecture/open hypothesis
refuted/removed with countermodel
```

The required IDs are:

```text
1.  T-RSUB
2.  T-SEM-EQUIV
3.  T-CONFLATE
4.  COR-LOCAL-STABILITY
5.  T-REFLECTIVE-NECESSITY
6.  T-OP-NONREDUCTION
7.  T-ORDER-INVARIANCE
8.  T-SPAN-DECIDABLE-FINITE
9.  L-ORDER-INCREMENT
10. T-UFRAG-QUEUE
11. T-REGIONAL-FRAG
12. T-SEM-FRAG
13. T-REVERSAL
14. T-RECURRENCE
15. T-CNS-LIFT
16. T-SING-CONTENT
17. T-OM
18. T-PROJECTION-ADEQUACY
19. T-REGENERATIVE-THRESHOLD, only if nontrivial
20. L-GF-UPPER-TAIL
21. L-GF-BRANCH
22. L-GF-CAUSAL
23. L-GF-FIRST-MOVER
24. L-GF-SUBSTRATE
25. L-GF-ADAPT
26. L-GF-OUTCOME
27. T-GF-CONSTRAINT
28. T-CNS-ADMISSIBILITY
29. COR-GF-CNS
30. T-BRIDGE-LIFT-TO-DYN
31. T-BRIDGE-DYN-TO-LIFT
32. T-HOL-INVARIANCE
33. T-HOL-DRIFT
```

## 6.4 Per-theorem closure record

Create `registry/theorem_manifest_v15.json`. Every theorem record must contain:

```json
{
  "id": "T-ORDER-INVARIANCE",
  "lean_declaration": "FmiCns.Order.order_invariance",
  "statement_sha256": "...",
  "informal_statement": "...",
  "formal_statement": "...",
  "status": "proved",
  "premises": [],
  "external_premises": [],
  "direct_dependencies": [],
  "transitive_axioms": [],
  "countermodels": [],
  "manuscript_passages": [],
  "warrant": "theorem",
  "reviewer_notes": "..."
}
```

## 6.5 Theorem construction discipline

For every theorem:

1. freeze the statement before proof construction;
2. create at least one expected countermodel for a missing premise;
3. prove the theorem or obtain a precise failure;
4. run the axiom audit;
5. map the theorem to manuscript passages;
6. test at least one finite example;
7. if the statement changes, increment its version and rerun the claim-impact audit.

If a theorem cannot be proved at its stated generality, do one of:

- expose stronger premises;
- weaken the conclusion;
- restrict the domain to a finite, compact, or otherwise defensible class;
- relabel as conjecture or empirical hypothesis;
- remove it and preserve a countermodel.

Do not leave a theorem-shaped placeholder in the paper.

## 6.6 Critical formal gaps to close

### A. Endogenous semantic structure

The existing `PointedSystem` contains only a node type, point, and invariant predicate. Replace or supplement it with a typed metric-interaction FSS containing at least:

```lean
structure FSS where
  Node : Type u
  Edge : Type v
  nodeType : Node → NodeType
  edgeType : Edge → EdgeType
  src : Edge → Node
  dst : Edge → Node
  dist : Node → Node → ℝ
  boundary : BoundaryData Node Edge
  admissible : Transformation FSS → Prop
```

Use a mathematically appropriate metric type and assumptions. Do not claim metric axioms unless encoded as fields or typeclasses.

Define admissible pointed equivalence to preserve all target-relevant:

- node and edge typing;
- incidence and orientation;
- metric relations;
- boundary and certificate data;
- continuation and successor obligations;
- participant-indexed fitness structure where relevant;
- target interpretation.

Then prove `T-SEM-EQUIV` for targets registered as invariant under that equivalence.

### B. Support and schedule

Define rather than label:

- local support by factorization through a declared bounded or component support family;
- global support by target-relevant nonfactorization through every allowed local decomposition;
- parallel schedule by commutation or retained-observation equivalence under admissible reorderings;
- sequential schedule by required typed precedence.

The operation-cell assignments must be hypotheses or proved certificates. Do not encode their truth merely as enumeration labels.

### C. Register/Recall nonreduction

The bounded theorem proves a domain/codomain obstruction for an algebra containing only conceptual endomorphisms. Preserve that theorem, but state its exact scope:

```text
Register and Recall are not definable by the declared L/G word algebra without an additional typed bridge.
```

Do not infer absolute nondefinability in every richer algebra.

### D. Order and finite certification

Separate:

- intrinsic cognitive order;
- a finite certified lower bound;
- a resource-relative assessment certificate.

Prove representation invariance only for admissible maps that preserve the certified composition family, functional non-equivalence, span, and reuse. If full invariance fails, report the restricted invariance theorem rather than treating it as system-intrinsic without qualification.

### E. Fragmentation

The existing backlog theorem is a one-unit arithmetic lower bound. Add:

- arrival-service dynamics;
- a theorem for positive cumulative gap;
- a reversal theorem;
- a recurrence theorem after renewed gap;
- a regional fragmentation theorem requiring explicit locality and cross-region bridge assumptions;
- semantic fragmentation connecting collapsed target-relevant distinctions to certified-reach loss.

Do not infer “locally coherent regions” from scalar backlog divergence without regional assumptions.

### F. CNS lift and published dynamical CNS bridge

Separate:

- the definitional order-increment lemma;
- a substantive lift theorem establishing span, operand-domain expansion, reuse, and reversal;
- the published dynamical CNS properties of contraction, closure, and invariance;
- two conditional bridge directions.

Required bridge shapes:

```text
order lift + expanded domain + globally contracting closed invariant operator
    ⇒ dynamical CNS on the expanded domain

new dynamical CNS operator + implementation requires prior-unavailable
non-equivalent spanning composition
    ⇒ order lift
```

If either bridge fails, treat the two CNS notions as distinct transition types. Do not force equivalence.

### G. Governance and option monotonicity

Formalize participantwise baseline-option preservation, representation error, realization error, and selection error. Prove the bound with its exact constants. Include a countermodel where aggregate mean improves while one participant is harmed.

### H. Great Filter constraints

Do not use a theorem like the bounded package’s `conditional_great_filter` as the full scientific proof if its `combine` argument already assumes the entire implication. It may remain a transparent application lemma, but the scientific work must be in separate proved lemmas:

```text
L-GF-UPPER-TAIL
L-GF-BRANCH
L-GF-CAUSAL
L-GF-FIRST-MOVER
L-GF-SUBSTRATE
L-GF-ADAPT
L-GF-OUTCOME
```

Then construct `T-GF-CONSTRAINT` from those lemmas, `T-CNS-ADMISSIBILITY` from the FMI–CNS mechanism, and `COR-GF-CNS` with all external premises as theorem parameters.

### I. CST transport, closure, and holonomy

Formalize:

- typed reasoning paths;
- admissible path deformations;
- transport of identity, contract, warrant, boundary, and continuation data;
- closed-loop invariance;
- a proved drift witness for nontrivial target-relevant holonomy;
- consequence closure as a monotone operator with a least fixed point under stated lattice assumptions;
- hard admissibility as a proposition prior to any optional action score.

The optional Polyakov-style action must not be used to compensate for a type or warrant failure.

## 6.7 Top-level formal theorem

Construct a theorem whose conclusion is a non-vacuous structure containing the formal dependency chain:

```lean
theorem formal_fmi_cns_coherence
    (M : Model)
    (hOntology : ValidOntology M)
    (hProjection : ProjectionPremises M)
    (hGrowth : GrowthPremises M)
    (hLift : LiftPremises M) :
    FormalMechanism M := by
  ...
```

`FormalMechanism M` must not be a structure containing arbitrary propositions with no proof fields. It should package proved consequences such as:

- the projection obstruction under its premises;
- the backlog or fragmentation result under growth premises;
- reversal under lift premises;
- recurrence under renewed growth;
- explicit status of unresolved external mappings.

## 6.8 Top-level conditional Great Filter theorem

```lean
theorem conditional_great_filter
    (M : Model)
    (hFormal : FormalMechanism M)
    (hPhysical : PhysicalMapping M)
    (hBranch : BranchClosure M)
    (hHazard : NonSummableHazard M)
    (hTimescale : TimescaleSufficiency M)
    (hOutcome : TargetOutcome M) :
    PostIntelligenceFilter M := by
  ...
```

External premises must be theorem parameters or fields of a supplied evidence structure. Do not declare them as global axioms.

## 6.9 Full Lean closure criteria

The full Lean package is closed only when:

- all 33 theorem IDs have a final status;
- every theorem labeled proved builds under the pinned kernel;
- no release theorem uses `sorryAx` or an unregistered axiom;
- all theorem dependencies match the registry;
- all manuscript claims map bidirectionally to Lean declarations or explicit open statuses;
- required mutation tests behave as preregistered;
- a second environment reproduces the build;
- formalization-fidelity review does not find an unclosed load-bearing registration error.

---

# 7. Build and run the Lean mutation suite

## 7.1 Purpose

The mutation suite must show that target-relevant conceptual corruptions change proof status in the expected way, while benign equivalent encodings preserve it.

## 7.2 Required mutation classes

Implement at least:

```text
replace cognitive order with Choice depth
remove non-equivalence from the lift
remove span
remove reuse
collapse Register into L
collapse Recall into G
swap support/schedule certificates
turn theorem parameter into global axiom
promote GF-3 to GF-6
remove participant completeness
replace terminal target with observability target
remove successor obligation
alter metric while preserving labels
alter interaction edge while preserving metric
apply admissible equivalent re-encoding
```

## 7.3 Expected outcomes

Each mutation must preregister one of:

```text
expected type error
expected proof failure
expected proved counterexample
expected changed axiom dependency
expected demotion to unresolved
expected no change for true equivalence
```

## 7.4 Keep expected-failure mutants outside the release import closure

Suggested layout:

```text
Tests/Mutations/ExpectedFail/*.lean
Tests/Mutations/ExpectedPass/*.lean
```

A shell harness should assert the expected return code:

```bash
#!/usr/bin/env bash
set -euo pipefail

pass=0
fail=0
for f in Tests/Mutations/ExpectedFail/*.lean; do
  if lake env lean "$f" >"$f.log" 2>&1; then
    echo "UNEXPECTED_PASS $f"
    fail=$((fail+1))
  else
    echo "EXPECTED_FAIL $f"
    pass=$((pass+1))
  fi
done

for f in Tests/Mutations/ExpectedPass/*.lean; do
  if lake env lean "$f" >"$f.log" 2>&1; then
    echo "EXPECTED_PASS $f"
    pass=$((pass+1))
  else
    echo "UNEXPECTED_FAIL $f"
    fail=$((fail+1))
  fi
done

printf 'pass=%s fail=%s\n' "$pass" "$fail"
test "$fail" -eq 0
```

## 7.5 Mutation output schema

Create `review/results/mutation_results.csv`:

```text
mutation_id,file,expected_class,observed_class,pass,affected_theorems,notes
```

A superficial schema error is not sufficient when the expected failure is semantic. For example, removing participant completeness should either invalidate the participantwise theorem or permit a proved countermodel, not merely break JSON parsing.

---

# 8. Conduct the formalization-fidelity audit

Lean verifies formal consequences, not whether the formal declaration is the intended scientific claim. This audit is a separate gate.

## 8.1 Freeze the canonical source

Before review, hash:

```text
Article v15
Supplement v15
v15 revision plan
canonical registry
Lean theorem statements
```

The proof author may not change these during blinded review without versioning the change.

## 8.2 Build blinded passage–declaration pairs

Each item should contain:

- one manuscript passage;
- one Lean declaration;
- one registry record;
- one warrant label;
- optionally one deliberately mismatched declaration.

Do not tell the reviewer whether the pair is matched.

## 8.3 Review dimensions

For every pair, score:

```text
identity preserved?                 yes/no/undetermined
scope preserved?                    yes/no/undetermined
target preserved?                   yes/no/undetermined
premises complete?                  yes/no/undetermined
warrant preserved?                  yes/no/undetermined
external status preserved?          yes/no/undetermined
countermodel representable in Lean? yes/no/undetermined
load-bearing omission?              description
```

## 8.4 Required adversarial pairs

Include:

- cognitive order replaced by reflective depth;
- reflection called an order lift without a new composition;
- Register or Recall collapsed into L/G;
- span deleted;
- participantwise rule replaced by aggregate mean;
- terminal and observability targets exchanged;
- GF-3 conditional theorem represented as GF-6 explanation;
- label-preserving metric mutation;
- metric-preserving edge mutation;
- an admissible renaming/isometry that should remain equivalent.

## 8.5 Decision rule

A load-bearing mismatch blocks the claim that Lean checks the intended paper, even if the proof compiles. Repair the registration mapping, rerun the affected proofs, rerun mutations, and repeat the fidelity audit.

Do not determine ground truth by reviewer majority alone. Use the frozen canonical specification plus an explicit typed witness or counterexample.

---

# 9. Independently reproduce the direct recurrence result

The direct recurrence gate is already closed-positive in the note’s declared synthetic model. The independent reviewer should reproduce it because the final carrier requires independent build and figure regeneration.

## 9.1 Run the frozen experiment

```bash
cd /mnt/data/v15_gate_closure
python code/direct_recurrence.py \
  2>&1 | tee review/logs/direct_recurrence_rerun.log
```

## 9.2 Verify protocol constants

Confirm:

```text
master seed              20260716
replicates per regime    1000
regions                  12
horizon                  300
lift time                80
operand expansion time   120
second lift time         215
regional threshold       12
recurrence window        30
late slope threshold     1.0
final backlog threshold  150
```

## 9.3 Compare outputs

```bash
sha256sum data/direct_recurrence_* figures/direct_recurrence_* \
  | tee review/results/direct_recurrence_hashes_rerun.txt
```

Compare the regenerated summary with the note:

```text
Fixed post-lift recurrence        approximately 1.000
Proportional service recurrence   0.000
Regenerative distribution        0.000
Second lift                       0.000
Branch heterogeneity              approximately 0.999
```

If deterministic outputs differ:

1. compare Python and dependency versions;
2. compare the protocol JSON and code hashes;
3. verify random-number generator behavior;
4. rerun in the pinned original environment if available;
5. report the discrepancy instead of averaging it away.

## 9.4 Scope statement

The reproduced experiment closes only this model-relative statement:

```text
After a valid lift reverses an increasing backlog, continued growth under
fixed post-lift service can recreate backlog and regional fragmentation;
service scaling, regenerative distribution, and another lift are explicit
counter-regimes in the declared model.
```

Do not describe it as evidence that civilizations actually follow these parameters.

---

# 10. Reproduce or reopen the v15 Gate Zero audit

## 10.1 First reproduce the existing closed-negative result

```bash
cd /mnt/data/v15_gate_closure
python code/gate_zero_audit.py \
  2>&1 | tee review/logs/gate_zero_documentary_rerun.log
cat audit/gate_zero_report.json | jq . \
  | tee review/results/gate_zero_documentary_rerun.json
```

Expected result when the v8 lineage is absent:

```text
FAIL_CLOSED_MISSING_EXECUTABLE_LINEAGE
```

If this result reproduces, the audit remains **closed-negative**, not open.

## 10.2 If the v8 lineage is supplied, preserve it immutably

```bash
mkdir -p review/v8_original review/v8_work
cp -a <supplied_v8_artifacts>/. review/v8_original/
find review/v8_original -type f -print0 | sort -z | xargs -0 sha256sum \
  > review/results/v8_supplied_hashes.txt
cp -a review/v8_original/. review/v8_work/
```

## 10.3 Required positive audit sequence

### A. Build the frozen environment

Use only the supplied environment lock. Record all deviations.

### B. Verify one-generator semantics

Confirm that all conditions are patches to one transition function. Search for:

- multiple condition-specific transition implementations;
- label-dependent truth branches;
- hidden data generation differences;
- target values derived from intervention names.

### C. Regenerate raw events

The regenerated event log must preserve:

```text
trajectory ID
event ID
operator
model hash
registry hash
seed
target
resource deltas
residual deltas
pre-state hash
post-state hash
```

### D. Verify state correspondence

Map every v8 state variable to a v15 object. Use these dispositions:

```text
conformant
partially conformant
nonconformant
undetermined
```

Do not retroactively declare that an old variable implemented a v15 semantic distinction when the code did not represent it.

### E. Verify residual handling

Check all four signal residual stages where applicable:

```text
registration
expression
receiver registration
receiver reconstruction
```

### F. Verify target revision separation

A change to the target must not be counted as progress toward the original target.

### G. Regenerate every inherited result

At minimum:

```text
12,800 trajectories
102,400 events
23 target-pair witnesses
full-CNS accuracy 0.585
matched comparator accuracy 0.400
full-CNS certified reach 0.435
best non-CNS certified reach 0.0033 or its exact unrounded value
reuse 0.347
participant containment 0.987
residual-open containment 0.717
master seed 20260715
```

Regenerate all tables and figures from raw events, not from printed manuscript values.

### H. Compare hashes and outputs

Create:

```text
audit/v8_regeneration_report.json
audit/v8_metric_crosswalk.csv
audit/v8_state_correspondence.csv
audit/v8_hash_comparison.csv
audit/v8_conformance_summary.md
```

## 10.4 Positive Gate Zero acceptance criteria

Positive closure requires:

- every critical artifact class is present;
- the frozen environment builds;
- raw events regenerate deterministically or within a preregistered stochastic identity rule;
- no condition label sets ground truth;
- no split generator is used;
- reported metrics are regenerated from events;
- source figures regenerate;
- every v8 claim has a v15 conformance disposition;
- discrepancies are reported rather than normalized away.

If any critical item fails, keep Gate Zero closed-negative or partially conformant. The inherited numbers may remain historical constructive-witness results or should be removed from prominence.

---

# 11. Execute the independent receiver study without contaminating it

## 11.1 Important limitation

A single LLM reviewer can complete one blinded receiver run. It cannot alone satisfy a study requiring three independent receiver families and second-generation retransmission unless the environment can instantiate genuinely separate model families or human receivers with isolated contexts.

Do not call repeated prompts to the same context “independent receiver families.”

## 11.2 Protect the answer key

The package contains:

```text
receiver/hidden_tasks.json
receiver/answer_key.json
receiver/receiver_scoring_schema.json
receiver/receiver_protocol.md
```

The receiver must not have filesystem or tool access to `answer_key.json` during its run.

Use an external orchestrator to:

1. hash the hidden tasks and answer key;
2. move the answer key into a directory inaccessible to the receiver;
3. provide only the assigned artifacts and task prompts;
4. collect receiver outputs;
5. score after all primary runs are locked.

Example:

```bash
sha256sum receiver/hidden_tasks.json receiver/answer_key.json \
  > review/results/receiver_freeze_hashes.txt
chmod 000 receiver/answer_key.json
```

Filesystem permissions alone are insufficient if the same privileged process can reverse them. Use process or account isolation.

## 11.3 Expand the task bank before recruitment if using the planned minimum

The current package contains 14 hidden claim families instantiated as 28 tasks. The protocol states that a defensible first study should use at least 20 hidden claim families per condition.

An independent task-setter—not a study receiver—must therefore:

1. create at least six additional claim families;
2. create base, mutation, and where appropriate equivalent-reencoding instances;
3. generate the answer key;
4. freeze all hashes before receiver recruitment;
5. never act as a receiver in the same study.

Possible additional families:

```text
HF-SPAN-FINITE
HF-SEM-FRAG
HF-OPTION-BOUND
HF-GF-BRANCH
HF-GF-HAZARD
HF-HOLONOMY
HF-CONSEQUENCE-CLOSURE
HF-ORDER-INVARIANCE
```

## 11.4 Conditions

Randomize receivers to or within these conditions:

```text
1. Article and Supplement only
2. Article, Supplement, and registry
3. Article, Supplement, registry, and direct typed-graph Lean package
4. Article, Supplement, CST geometry, and Lean package
5. Corrupted formal artifact
6. Benign equivalent re-encoding
```

Do not provide the answer key or corruption label.

## 11.5 Primary tasks

Each receiver must:

1. recover the theorem dependency chain;
2. classify statements as definition, assumption, theorem, finite witness, external premise, or open claim;
3. apply the formalism to a hidden claim family;
4. identify the minimum missing premise for an unresolved conclusion;
5. reject a fatal inversion;
6. predict downstream failures after a definition mutation;
7. produce a retransmission package for a second receiver.

## 11.6 Receiver output schema

Require machine-readable output:

```json
{
  "receiver_id": "...",
  "model_family": "...",
  "condition": "...",
  "task_token": "...",
  "status": "...",
  "statement_type": "...",
  "minimum_missing_premise": "...",
  "downstream_failures": [],
  "confidence": 0.0,
  "elapsed_seconds": 0,
  "author_repairs": 0,
  "registration_residual": "...",
  "expression_residual": "...",
  "reconstruction_summary": "..."
}
```

## 11.7 Second-generation retransmission

Receiver 1 creates a package containing only what it believes Receiver 2 needs. Receiver 2 receives:

- Receiver 1’s retransmission package;
- a new hidden task from the same claim family;
- no Article, Supplement, registry, answer key, or author repair unless the condition explicitly includes them.

Record:

```text
contract recovered?
hidden target executed correctly?
fatal inversion rejected?
minimum premise recovered?
new retransmission package generated?
author repair count?
```

`Regenerate = 1` only if Receiver 2 succeeds without author repair.

## 11.8 Primary endpoints

Analyze separately:

```text
novel-target execution accuracy
theorem-status accuracy
false proof-promotion rate
minimum-missing-premise recovery
second-receiver regenerative success
author-repair count
elapsed time and token/cost burden
registration, expression, reception, and reconstruction residuals
```

Do not collapse these into a single accuracy number.

## 11.9 Preregister the statistical decision rule

Before scoring labeled outcomes, freeze:

- smallest transfer effect worth detecting;
- family-level and receiver-level sample size;
- primary contrasts;
- exclusions;
- handling of fatal errors;
- confidence interval or Bayesian decision rule;
- multiplicity handling.

Primary contrasts:

```text
Lean artifact minus prose only
Lean artifact minus registry only
CST plus Lean minus direct graph plus Lean
corrupted artifact minus valid artifact
equivalent encoding minus canonical encoding
Receiver 2 minus Receiver 1 transmission loss
```

Treat receiver family and claim family as inferential units. Individual prompt repetitions are not independent units.

## 11.10 Receiver gate closure criteria

The receiver gate may be marked closed when:

- at least three independent receiver families complete the study;
- hidden claim families meet the preregistered sample requirement;
- task and answer-key hashes were frozen before recruitment;
- answer keys were inaccessible during runs;
- second-generation retransmission was executed;
- author interventions were logged;
- primary transfer endpoints were analyzed before diagnostic tasks;
- results and failures were reported regardless of direction.

A single independent LLM run is a valid pilot or one receiver-family observation, not full closure.

---

# 12. Evaluate external mappings without promoting them by formal convenience

## 12.1 General certificate schema

For every mapping, create:

```json
{
  "mapping_id": "...",
  "formal_source_object": "...",
  "external_target_object": "...",
  "regime": "...",
  "target_family": "...",
  "invariants_claimed": [],
  "minimum_evidence": [],
  "evidence_supplied": [],
  "defeaters": [],
  "independent_reviewers": [],
  "status": "open",
  "strongest_permitted_claim": "...",
  "claim_ladder_level": "..."
}
```

## 12.2 Cross-FSS semantic principle

This item can be formally closed if the claim is:

```text
The same class of metric-interaction-position invariants can constitute
functional identity in distinct FSSs under an explicit invariant-preserving map.
```

Required work:

1. formalize source and target FSSs;
2. define the admissible map;
3. specify the target-relevant invariants;
4. prove preservation;
5. preserve the distinction between invariant-level identity and object/substrate identity.

This does not prove that a particular physical force realizes a particular cognitive operation.

## 12.3 Physical interaction mappings

Candidate mappings:

```text
strong interaction ↔ Register
weak interaction   ↔ Recall
electromagnetism   ↔ L
gravity            ↔ G
```

For each mapping, freeze the functional definitions before inspecting confirming evidence.

Required certificate fields:

```text
operational support definition
local factorization or global nonfactorization witness
parallel commutation or sequential precedence witness
scale and physical regime
topological implication
cross-FSS invariant
known counter-regimes
defeating observation or theorem
```

Do not infer local/global support from ordinary spatial range. The registered support claim is target-relative and functional.

A mapping is not closed merely by finding an analogy. Closure requires a mathematical or experimentally grounded witness and independent domain review.

Possible dispositions:

```text
supported in declared regime
partially supported
undetermined
refuted in declared regime
ill-posed under current definition
```

A failed force mapping narrows that cross-FSS hypothesis. It does not defeat the conceptual FMI–CNS theorem unless the theorem explicitly depends on it.

## 12.4 Current-AI trace mapping

Required design:

1. freeze version-locked external systems;
2. create paired latent worlds with identical first-order projection and target-different reflective structure;
3. use hidden targets;
4. prevent answer leakage and intervention-label truth;
5. collect genuinely external traces or outputs;
6. apply a target-aware three-valued monitor;
7. distinguish failure, correct abstention, and false confidence;
8. analyze at model-family and task-family levels.

This mapping can close to GF-4-like measured-component evidence only for the measured systems and tasks. It cannot establish civilizational instantiation.

## 12.5 Historical order-lift mapping

Before choosing examples, freeze a uniform rubric:

```text
prior-order representability
pre-existing compositions
new non-equivalent composition
span
reuse
operand-domain expansion
adoptability
world comparator
participant consequences
uncertainty
```

Then:

1. select candidates using a preregistered rule;
2. collect independent primary and scholarly sources;
3. classify each candidate by at least two independent reviewers;
4. permit `undetermined`;
5. rerun every classification if the rubric changes.

Historical examples support the framework only at the classified level. They do not prove universality.

## 12.6 Great Filter branch closure

Separate:

- formal branch-closure lemma;
- synthetic branch experiment;
- external evidence that real successor branches inherit or recreate the vulnerability.

The synthetic experiment can close a model-regime claim. External branch closure remains open without evidence about real or defensibly modeled lineages.

## 12.7 Hazard non-summability

A finite time series cannot by itself prove that an infinite hazard sequence is non-summable. Permitted outcomes are:

```text
non-summability assumed in a model
finite evidence consistent with a non-summable class
finite evidence inconsistent with specified non-summable models
undetermined extrapolation
```

Do not promote model non-summability to a fact about civilizations.

## 12.8 Timescale and residue suppression

A terminal or observability-filter claim requires:

- explicit target class;
- correction, dispersal, and hazard timescales;
- outcome-specific residue model;
- evidence that the relevant residue is suppressed within the declared observation window.

Terminal collapse with durable observable residue does not satisfy an observability-filter target. Low observability does not by itself establish terminal extinction.

## 12.9 External mapping closure rule

Mark an individual external mapping closed only when:

- the formal mapping object is frozen;
- required evidence is supplied;
- explicit defeaters are tested;
- at least one independent domain reviewer signs the certificate;
- the strongest permitted claim is no stronger than the evidence;
- the claim-ladder level is recorded.

The external package as a whole need not be uniformly closed. Publish a vector of per-mapping statuses.

---

# 13. Great Filter claim-ladder enforcement

Use this ladder:

```text
GF-0 physically possible candidate
GF-1 necessary properties of the declared filter class proved
GF-2 FMI–CNS mechanism structurally admissible
GF-3 mechanism is a filter if explicit external premises hold
GF-4 measured components exist in current systems
GF-5 real civilizations instantiate the full mechanism
GF-6 mechanism explains the observed Great Filter
```

The Lean theorem package can close GF-1 and conditional GF-3 shapes and may support GF-2 if structural admissibility is proved. It cannot by itself close GF-4 through GF-6.

Any output that promotes GF-3 to GF-6 is a fatal warrant error.

---

# 14. Independent build, repository, and manuscript coverage

## 14.1 Required generated reports

Produce:

```text
reports/theorem_manifest.md
reports/theorem_dependency_report.md
reports/axiom_audit.md
reports/lean4checker_report.md
reports/manuscript_to_lean_coverage.csv
reports/lean_to_manuscript_coverage.csv
reports/formalization_fidelity.md
reports/mutation_results.csv
reports/gate_zero_v15.md
reports/direct_recurrence_reproduction.md
reports/receiver_study.md
reports/external_mapping_status.md
reports/self_containment_audit.md
reports/independent_build.md
```

## 14.2 Bidirectional coverage

For every positive manuscript claim, record:

```text
claim ID
exact passage
warrant
Lean declaration or experiment
proof/experiment status
external premises
countermodels
```

For every release Lean theorem, record the manuscript claim it supports. Orphan theorems are allowed but must be identified; unsupported manuscript claims are not.

## 14.3 Data and code placeholders

Before submission, replace every placeholder with actual reviewer-access locations. Include:

- source repository;
- archive DOI or immutable snapshot;
- code and data license;
- environment lock;
- toolchain pin;
- source figures;
- checksum manifest;
- independent build report.

## 14.4 Final status vector

Publish at least:

```text
bounded Lean kernel
full v15 Lean theorem coverage
formalization fidelity
Gate Zero
recurrence reproduction
receiver propagation
cross-FSS semantic principle
four physical mappings
current-AI mapping
historical mapping
branch closure
hazard non-summability
timescale/residue
repository reproduction
```

Each receives:

```text
closed-positive
closed-negative
partially closed
open
not applicable
```

---

# 15. Required final reviewer report

Use this structure.

## 15.1 Executive disposition

```text
What was closed positively?
What was closed negatively?
What remains partial?
What could not be attempted because inputs were absent?
Which manuscript claims must change?
```

## 15.2 Lean report

Include:

- exact toolchain;
- source hashes;
- build command and exit code;
- all theorem declarations;
- all axiom reports;
- `lean4checker` result;
- comparator/external-checker result if used;
- source modifications and statement diffs;
- bounded versus full coverage distinction.

## 15.3 Gate Zero report

Include:

- artifact inventory;
- hash verification;
- one-generator audit;
- event regeneration;
- metric regeneration;
- per-result conformance;
- final positive or negative disposition.

## 15.4 Recurrence report

Include:

- protocol hash;
- environment;
- reproduced results;
- discrepancies;
- exact model-relative scope.

## 15.5 Receiver report

Include:

- receiver families;
- blinding and answer-key controls;
- conditions;
- hidden family count;
- primary endpoints;
- second-generation results;
- author repairs;
- fatal errors;
- inferential unit and statistical model.

## 15.6 External mapping report

For every mapping, include:

- formal object;
- evidence;
- defeaters;
- independent reviewer;
- claim level;
- strongest permitted statement;
- open residuals.

## 15.7 Manuscript consequences

State exact changes required in Article and Supplement. Do not rewrite a negative result as a rhetorical qualification. Update claim status directly.

---

# 16. Suggested execution order

Execute in this order:

```text
1. preserve and verify package
2. install pinned Lean
3. build existing bounded package
4. repair proof-only errors without statement drift
5. run complete axiom audit
6. run lean4checker and second clean build
7. reproduce recurrence
8. reproduce documentary Gate Zero
9. inventory any supplied v8 lineage
10. freeze complete v15 theorem statements
11. expand Lean package to full theorem coverage
12. run mutation and countermodel suites
13. run formalization-fidelity audit
14. conduct blinded receiver study
15. execute only feasible external mapping tracks
16. generate bidirectional manuscript coverage
17. issue final status vector and manuscript changes
18. deposit immutable repository and independent report
```

Stop and issue a negative disposition rather than proceeding when:

- a theorem is false at stated generality;
- a build requires a prohibited axiom;
- formalization fidelity fails on a load-bearing object;
- receiver blinding is compromised;
- Gate Zero lacks the executable lineage;
- external evidence does not satisfy the registered certificate.

---

# 17. Minimum closure outcomes possible in different environments

## 17.1 Lean execution only; no v8 lineage; no external receivers

Possible:

- close bounded Lean kernel gate;
- expand and close full formal theorem package if proofs can be constructed;
- close or defeat individual theorem claims;
- reproduce recurrence;
- confirm Gate Zero closed-negative;
- run mutation tests;
- conduct one independent formalization-fidelity review;
- complete mapping registration.

Not possible:

- positive Gate Zero;
- full independent receiver gate;
- empirical physical, AI, historical, branch, hazard, or residue closure.

## 17.2 Lean plus original v8 lineage

Additionally possible:

- positive or negative Gate Zero regeneration;
- exact disposition of inherited numerical claims.

## 17.3 Lean plus multiple independent model/human receivers

Additionally possible:

- full transfer-first receiver study;
- second-generation regenerative endpoint;
- minimum independent submission anchor.

## 17.4 Lean plus external data and domain reviewers

Additionally possible:

- per-mapping physical, AI, historical, branch, hazard, and residue dispositions;
- claim promotion only to the supported ladder level.

---

# 18. Final acceptance conditions for “all closable open items closed”

The independent reviewer may state that all currently closable items have been closed only when:

1. the pinned Lean package has a successful build, full axiom report, `lean4checker` replay, and independent second build;
2. the distinction between the bounded package and full v15 theorem coverage is explicit;
3. every required theorem has a final proved, restricted, open, or defeated disposition;
4. all theorem statement changes are versioned and mapped back to the manuscripts;
5. recurrence reproduces or a discrepancy is closed with a precise explanation;
6. Gate Zero is either positively regenerated from the complete v8 lineage or remains explicitly closed-negative due to missing/nonconformant lineage;
7. the receiver protocol has either been fully executed with independent families or is explicitly partial, with no contaminated pseudo-run substituted;
8. every external mapping has a registered certificate and an evidence-based status;
9. no external claim is promoted beyond its evidence;
10. the final repository is immutable, hashed, independently buildable, and available to reviewers.

The reviewer must not use the phrase “all gates closed” when some gates are only registration-closed, model-relative, or empirically unexecuted. Report the vector.

---

# 19. Official Lean validation references

Use the documentation for the pinned Lean release whenever command behavior differs from these instructions.

- [Lean installation](https://lean-lang.org/install/)
- [Manual installation and `elan`](https://lean-lang.org/install/manual/)
- [Lean Language Reference, version 4.32.0](https://lean-lang.org/doc/reference/latest/)
- [Validating a Lean proof](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
- [Lean 4.32.0 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.32.0/)

The official proof-validation guidance distinguishes theorem-statement meaning from proof validity, recommends `#print axioms`, describes `lean4checker --fresh`, and gives a stronger comparator/external-checker workflow for potentially malicious or unreviewed AI-generated proofs. Apply that higher-assurance workflow where the environment permits it.

---

# 20. Final reviewer sign-off template

```markdown
# Independent v15 Gate-Closure Report

## Reviewer identity and environment
- Model:
- Provider:
- Context isolation:
- Lean version:
- OS/container:
- Review date:

## Immutable input hashes
...

## Status vector
| Gate/package | Disposition | Evidence | Blocking residual |
|---|---|---|---|

## Lean bounded build
...

## Full theorem coverage
...

## Axiom and kernel replay
...

## Formalization fidelity
...

## Mutation suite
...

## Gate Zero
...

## Direct recurrence reproduction
...

## Receiver propagation
...

## External mappings
...

## Required manuscript changes
...

## Typed defeating objections
...

## Final projection/global-coherence verdict
...

## Final journal-carrier verdict
...

## Reviewer declaration
I did not access the receiver answer key before completing the blinded run.
I did not use author repair before recording primary endpoints.
I did not silently weaken theorem statements.
I have reported every missing input, negative result, and custom assumption.
```
