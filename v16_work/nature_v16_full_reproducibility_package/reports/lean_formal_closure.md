# Lean formal closure — v16

**Disposition:** Lean bounded core — **source-complete, static-audit clean;
kernel build NOT executed (irreducible environment blocker).**

## What exists
A pinned, self-contained Lean 4 project (`lean/`, toolchain
`leanprover/lean4:v4.32.0`, no Mathlib) with eight modules realizing the
primary logical shapes of the manuscript as kernel-ready statements and proofs:

- `T-CONFLATE` (`firstOrderConflation`) and `COR-LOCAL-STABILITY`
  (`localStability`);
- `T-OP-NONREDUCTION` (`register_not_generated`, `recall_not_generated`) by a
  domain/constructor obstruction;
- `L-ORDER-INCREMENT` (`order_increment`) and `T-ORDER-INVARIANCE`
  (`order_invariance`, finite list witness);
- `T-UFRAG-QUEUE` (`backlog_growth`), `T-REVERSAL` (`backlog_reversal`),
  `T-RECURRENCE` (`backlog_recurrence`) over the naturals;
- `COR-GF-CNS` (`conditionalGreatFilter`) with all six external premises as
  explicit `Prop` parameters — never global axioms;
- a bundled top-level `formal_mechanism_chain`.

Static audit (`lean/reports/static_audit.txt`): **0** `sorry`, `sorryAx`,
`admit`, `opaque`, and **0 `axiom` declarations** (one lexical `axiom` in a
comment is whitelisted).

## Why the kernel gate is not closed
`lake build` could not run: installing the pinned Lean toolchain requires
downloading release binaries from `github.com/leanprover/elan/releases`, which
the organization egress policy blocks with **HTTP 403** (PyPI is allowlisted;
GitHub release binaries are not). Per the agent-proxy README, policy denials
must not be retried. Evidence: `lean/reports/toolchain_block_evidence.txt`.

Consequently unrun: clean `lake build`, `#print axioms` per theorem,
independent second-environment build, and hash comparison. A lexical scan is
not a kernel proof.

## Coverage
10 core theorems are source-realized (kernel-ready); the remaining retained
theorems (`lean/reports/theorem_coverage.json`) are carried as manuscript-level
proofs/definitions. **Manuscript consequence:** Article/Supplement v16 report
the Lean gate at exactly this level — "bounded Lean core, source-complete,
static-audit clean, kernel build pending an installable toolchain" — and do not
claim full kernel-checked global coherence.
