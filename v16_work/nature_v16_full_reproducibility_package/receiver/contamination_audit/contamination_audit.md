# Receiver study contamination audit

- Isolation: each Receiver A ran in a fresh, separate agent context (no shared
  memory), seeing ONLY its condition packet + the task list in its prompt. No
  receiver saw the answer key, task-generation rationale, another receiver's
  output, or sources beyond its packet.
- Answer key: stored under sealed_ground_truth/ and read by the scorer ONLY
  after all receiver outputs were frozen. SHA-256 in answer_key.sha256.
- Receiver B: received ONLY a Receiver A transmission artifact plus the task
  list — not the original packet, registry, or Lean project.
- Scorer: preregistered schema (verdict match; theorem-identity recovery =
  literal "T-CONFLATE"); rules not altered after seeing labels.
- Residual risk (disclosed): all receivers are instances of the same model
  family spawned by one orchestrating session; same-process subagents were
  isolated by prompt scoping, not OS containers. Warranted claim is therefore
  SAME-MODEL isolated-instance regenerative propagation only (per §8.9).
