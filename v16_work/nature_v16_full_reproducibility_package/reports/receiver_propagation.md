# Receiver propagation — bounded same-model isolated study

**Disposition:** closed-bounded. **Claim level:** regenerative propagation across ISOLATED SAME-MODEL receiver instances under the tested conditions; NOT cross-model or human

## Design
6 hidden tasks across 6 families; 2 conditions (formal package vs prose-only control); 2 Receiver A instances per condition; 1 Receiver B regeneration from a Receiver A transmission. Units of inference: receiver instance and claim family.

## Results
| Condition | n | mean verdict accuracy | theorem-identity recovery |
|---|---|---|---|
| formal_package | 2 | 1.00 | 1.00 |
| prose_only | 2 | 1.00 | 0.00 |

- Second-generation success (Receiver B, no original source, no author repair): **True**.
- Author-repair count: **0**.

## Finding
All conditions transferred the six core verdicts (24/24). The registered theorem identity (T-CONFLATE) was recovered by 2/2 formal-package receivers and 0/2 prose-only receivers. A second-generation receiver (Receiver B), given only a Receiver A transmission and no original source, reproduced all six verdicts and the theorem identity with zero author repair.

## Consequence for the manuscript
Report regenerative propagation across isolated same-model receiver instances under the tested conditions. Do not claim cross-model or human propagation. The formal package (typed definitions + registered theorem names) transferred the registered identity that the prose-only control did not, consistent with the CST/registry-improves-propagation hypothesis at bounded scale.