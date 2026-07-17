# Claude Code execution contract

## Governing rule

Execute every experiment whose prerequisites are present. Do not substitute a status report for execution. A blocker is recorded once and is not counted as a completed experiment.

## Required preflight

1. Run `./run_component_tests.sh` and preserve stdout/stderr.
2. Record model name/version, Claude Code version, OS, shell, Python, Lean, Lake, network policy, and agent-spawning capabilities.
3. Confirm that receiver agents can be started with fresh contexts and restricted file access.
4. Hash the untouched archive and create an immutable working copy.

## Information-isolation roles

Create distinct agents or contexts:

- `ADMIN`: randomizes and distributes packets; must not solve tasks.
- `KEY_CUSTODIAN`: alone can read sealed answer keys before scoring.
- `RECEIVER_A_*`: can read only assigned condition and hidden packet.
- `RECEIVER_B_*`: can read only one Receiver A transmission and its own hidden packet.
- `FIDELITY_REVIEWER_*`: can read only blinded fidelity pairs.
- `SCORER`: receives frozen outputs only after all receiver contexts are closed.
- `CONTAMINATION_AUDITOR`: reviews prompts, paths, access logs, hashes, and temporal order.
- `LEAN_BUILDER_1` and `LEAN_BUILDER_2`: use separate clean worktrees/environments.

Agents of the same model are independent **instances**, not heterogeneous receiver families. Report this exactly.

## Mandatory evidence

For every agent run preserve:

- full system/developer/user prompt;
- model and tool version;
- context/run identifier;
- start/end timestamps;
- files made visible to the agent;
- filesystem/tool access log where available;
- raw output before normalization;
- normalized JSON output;
- exit/error status;
- SHA-256 hashes.

## Order of execution

1. Lean formal closure and first build.
2. Lean mutations and axiom report.
3. Second clean independent build and hash comparison.
4. Formalization-fidelity review.
5. Receiver A runs across all six conditions.
6. Freeze Receiver A outputs and transmissions; terminate their contexts.
7. Receiver B runs with transmission-only access.
8. CST utility receiver experiment.
9. External trace, historical, and physical mappings only when their required external inputs exist.
10. Unseal keys, score, audit contamination, and generate final reports.

## Prohibitions

- Do not let an agent generate a task and then count its own solution as independent.
- Do not expose answer keys, expected mutation outcomes, or task-generation rationale to receivers.
- Do not silently weaken Lean theorem statements to make them compile.
- Do not call same-model agents different receiver families.
- Do not promote a synthetic or formal mapping to external evidence.
- Do not report completion without raw logs and generated result files.

Each experiment directory contains a dedicated execution document and exact commands.
