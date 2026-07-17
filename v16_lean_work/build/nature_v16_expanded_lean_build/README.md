# FMI-CNS v16 Expanded Lean Formalization Candidate

This package replaces the bounded seven-module Lean core in the v16 reproducibility archive with a substantially expanded, Mathlib-based formalization of the manuscript's load-bearing claims.

It is designed for a second LLM or human formalizer with Lean execution to build, debug, strengthen, and independently audit. **This package has not been kernel-built in the present environment.** No claim of Lean closure should be made until the commands below succeed and the generated axiom report is inspected.

## What this package fixes

The earlier v16 core proved several elementary logical shapes but did not formalize the principal scientific burden. In particular, its order-invariance theorem only proved that `List.map` preserves list length, and its conditional Great Filter theorem merely introduced a conjunction of premises.

This replacement adds:

- a typed metric FSS with metric, interaction, boundary, warrant, continuation, and participant-fitness structure;
- a registered semantic language with Boolean connectives and bounded node/edge quantification;
- a structural-induction proof of semantic invariance under an admissible metric-interaction isomorphism;
- projection factorization and first-order conflation;
- reflective necessity;
- typed Register/Recall nonreduction;
- canonical local/global support and parallel/sequential schedule definitions;
- cognitive-order invariance under an actual equivalence of qualifying composition classes;
- executable finite span and finite functional-equivalence certificates;
- arrival-service queue theorems derived from the queue recursion;
- a restricted regional-fragmentation theorem that separates local certification from unresolved cross-region burden;
- a finite semantic-loss lower bound for collapsed target-different pairs;
- a substantive CNS-lift theorem combining order increment, operand expansion, reversal, and nonfactorization;
- a comparator theorem for near-singular content;
- a conditional bridge to a contracting, closed, invariant dynamical CNS and a uniqueness theorem for its fixed normal form;
- participantwise option monotonicity;
- a regenerative propagation threshold;
- seven separately inspectable Great Filter necessary-property lemmas;
- a finite hazard survival lower bound;
- a conditional Great Filter theorem whose conclusion is the universal filter target, not a restatement of a premise conjunction;
- discrete semantic transport, holonomy invariance, and holonomy drift;
- a least consequence-closed operand construction with hard admissibility prior to any optional action;
- a top-level formal FMI-CNS theorem carrying semantic invariance and the substantive CNS-lift conclusion;
- finite examples, independence countermodels, and mutation checks.

## Toolchain

The project pins:

```text
Lean 4.32.0
Mathlib v4.32.0
```

The matched release tags are used so that Lake can generate a locked `lake-manifest.json` in the debugging environment.

## Build

```bash
lake update
lake build
lake env lean AxiomReport.lean | tee axiom-report.txt
bash scripts/audit.sh
```

Then perform a second build from a clean clone or container:

```bash
rm -rf .lake
lake update
lake build 2>&1 | tee clean-build.log
lake env lean AxiomReport.lean > clean-axiom-report.txt 2>&1
```

Do not claim kernel closure unless both builds succeed and the reports are retained.

## Expected debugging policy

1. Repair syntax, elaboration, or library-API errors without silently weakening a theorem.
2. When a theorem needs stronger premises, expose those premises and update `THEOREM_MANIFEST.json` and `MANUSCRIPT_INTEGRATION.md`.
3. When a theorem is false, preserve a kernel-checked countermodel and relabel the manuscript claim.
4. Do not insert `sorry`, `admit`, `sorryAx`, or custom axioms.
5. External physical, historical, AI, branch, hazard, timescale, and residue premises must remain theorem parameters.
6. Preserve the distinction between:
   - definitional order increment;
   - substantive order-lift CNS;
   - dynamical CNS;
   - conditional Great Filter formation;
   - external instantiation.

## Package status

- Source coverage: expanded candidate for all 33 registered theorem targets.
- Static forbidden-token scan in the generating environment: zero matches.
- Kernel build: **not executed here**.
- Intended next step: run `DEBUG_PROMPT_FOR_LEAN_LLM.md` in a Lean-enabled environment.
