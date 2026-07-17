# Formalization-fidelity multi-agent execution

Generate packets, then spawn each reviewer in a fresh context with only one packet. Reviewers must not see the answer key, other outputs, or pair-generation code. Freeze all reviews before scoring. Use at least three reviewer instances; heterogeneous models or humans should be reported separately when available. After scoring, adjudicate disagreements by typed witness rather than majority alone. Any declaration repaired after the review invalidates the affected item and requires a fresh blinded rerun.

```bash
python code/generate_packets.py --out run/packets
# spawn isolated reviewers and save run/outputs/*.json
python code/score.py --outputs run/outputs --key sealed/answer_key.json --out run/scoring
```
