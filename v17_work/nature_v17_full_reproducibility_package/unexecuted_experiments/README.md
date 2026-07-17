# Nature v16 implemented but not fully executed experiments

This archive contains experiments whose decisive execution requires a Lean toolchain, isolated multi-agent receivers, heterogeneous external data, or independent reviewers. The experiment implementations, task banks, sealed keys, scoring programs, schemas, mock fixtures, and component tests are included.

## Included experiments

- **Lean formal closure, mutation, axiom audit, and independent build** — expanded 33-target Lean package plus build/collection harness.
- **Formalization fidelity** — blinded manuscript/Lean/registry pair review with deliberate typed mismatches.
- **Regenerative receiver propagation** — six conditions, 14 hidden families, 28 tasks, first- and second-generation receiver chains.
- **CST geometry utility** — direct graph versus CST-plus-Lean conditions, ablations, hidden execution, and retransmission.
- **External AI trace study** — version-locked trace ingestion, leakage/pseudoreplication gates, paired analysis.
- **Historical order-lift classification** — frozen rubric, blinded dual review, adjudication, and uncertainty reporting.
- **Physical FSS mapping** — support/schedule/topology certificate workflow with independent proponent and adversarial reviewer agents.

## Component tests

```bash
./run_component_tests.sh
```

The tests validate packet generation, schemas, sealed-key separation, scorer behavior, and negative controls. They do not simulate scientific independence and are not study results.

## Execution

Read `CLAUDE_CODE_EXECUTION_INSTRUCTIONS.md`. Claude Code must use fresh context-isolated agents, preserve full prompts and outputs, prevent receiver access to sealed keys, and return all raw agent logs. A protocol-only report is not completion.
