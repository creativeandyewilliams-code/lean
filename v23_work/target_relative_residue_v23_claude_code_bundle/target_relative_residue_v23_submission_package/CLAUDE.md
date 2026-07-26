# Version 23 carrier-complete audit instructions

@00_CLAUDE_CODE_START_v23.md
@CLAUDE_CODE_PROMPT_v23.txt

## Non-negotiable controls
- Treat `expected_overall_verdict=GC_sub` as an untrusted design hypothesis, never as evidence.
- Do not reuse an author verdict or invent an execution.
- Do not return overall GC if the integrated recommendation is major revision or reject.
- Import every recommendation-changing conventional objection as a typed carrier challenge.
- Preserve theorem statements while debugging Lean; revise prose and theorem maps if a correction is mathematically required.
- A missing or invalid trace is NE, not UB.
- Run all mechanical checks and record exact commands, versions, hashes, stdout/stderr, and exit codes.
- Update manuscript status only through `apply_gca_result_v23.py` after the root certificate validates.

- If any frozen input changes during Lean or carrier repair, run `refreeze_review_instance_v23.py` before generating a trace; all prior traces are invalid.
