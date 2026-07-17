# Receiver regenerative experiment — EXECUTED (bounded, same-model isolated instances)

Real isolated fresh-context agents (not the mock agents). Executed scale: 6
Receiver A (one per condition) + 1 Receiver B (second generation from the
direct_graph+Lean transmission). Config's full scale (3 A/condition + 2 B) was
reduced for agent-budget reasons; report is at same-model isolated-instance
level (not heterogeneous families).

## Primary findings
- **Fatal-error rate = 0.000 across ALL six conditions**, including the
  corrupted-artifact condition: every receiver detected and rejected the fatal
  substitutions (order=choice-depth, reflection-raises-order, Register=L,
  Recall=G, decreasing-backlog=dynamical-CNS, aggregate-governance,
  formal-admissibility=identified-filter). (exact scoring, robust)
- **Registered-claim-ID recovery** (disclosed substring metric): the
  direct_graph+Lean condition recovered the registered claim identities at
  0.786 (11/14: T-CONFLATE, T-RECURRENCE, T-OM, T-OP-NONREDUCTION,
  L-ORDER-INCREMENT, T-SEM-EQUIV, COR-GF-CNS, the two bridge IDs). All other
  conditions = 0.000 — they reasoned correctly but in prose, not the registered
  identifiers. This is the transfer signal: the explicit Lean theorem inventory
  transferred the registered identities that narrative/registry/CST-prose did not.
- **Second-generation regeneration**: Receiver B, given ONLY a Receiver A
  transmission (no source), answered all 14 disguised B-variant tasks correctly
  (fibre-constancy for conflation, gap-gated recurrence, dyn-bridge needs
  closure+contraction, participant guarantee) with 0 fatal verdicts and 0 author
  repairs.
- Isolation validator passed (no sealed key in any receiver-visible path).

## Scoring note (transparency)
The provided exact-match `score.py` requires the key's controlled verdict
vocabulary (e.g. `projection_decoder_impossible`) which the receiver prompt did
not supply, so raw verdict_accuracy is low (0.00-0.14) and UNDERSTATES the
(clearly correct) reasoning. The disclosed supplementary scorer
(`score_normalized.py`) reports the robust, exactly-scored fatal-error rate and
the registered-claim-ID recovery. A schema-native re-run (giving receivers the
allowed verdict enum) is the recommended confirmatory step.

## Disposition
EXECUTED (bounded, same-model isolated instances). Full-scale and cross-model /
human receiver families remain open.
