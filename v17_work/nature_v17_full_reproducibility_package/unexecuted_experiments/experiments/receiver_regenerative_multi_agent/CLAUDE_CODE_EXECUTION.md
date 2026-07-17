# Execute the regenerative receiver experiment

1. Run `python code/generate_packets.py --out run/packets`.
2. Move `sealed/answer_key.json` outside every receiver-visible directory. Only `KEY_CUSTODIAN` and the post-freeze `SCORER` may read it.
3. For every entry in `run/packets/run_plan.json`, spawn a fresh Receiver A context. Expose exactly its packet and any condition-referenced artifact. Preserve the raw prompt, visible-file list, timestamps, model/version, and output.
4. Require Receiver A to produce `answer.json` and `transmission.md`. The administrator copies only `transmission.md` into the linked Receiver B packets.
5. Terminate/detach all Receiver A contexts before launching Receiver B.
6. Spawn each Receiver B in a fresh context with only its instructions, alternate hidden tasks, and one transmission. It must not see the source condition or Receiver A answer JSON.
7. Put normalized outputs under `run/outputs/` with `generation`, `condition`, `run_id`, and `answers` fields.
8. Run `python code/validate_isolation.py --run-dir run` before scoring.
9. After all outputs are frozen, expose the sealed key to `SCORER` and run:

```bash
python code/score.py --run-dir run --key sealed/answer_key.json --out run/scoring
```

10. Report results by receiver instance, condition, generation, and hidden family. Primary comparisons are formal package minus prose, CST+Lean minus direct graph+Lean, corrupted minus valid, equivalent re-encoding minus canonical, and Receiver A to Receiver B loss.
11. Same-model runs are receiver instances. Do not describe them as heterogeneous families.
