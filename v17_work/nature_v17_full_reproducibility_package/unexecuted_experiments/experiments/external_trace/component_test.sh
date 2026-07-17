#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python "$R/code/validate_and_split.py" --input "$R/fixtures/traces.jsonl" --out "$T/split" >/dev/null
python "$R/code/analyze.py" --test "$T/split/test.jsonl" --out "$T/results" >/dev/null
test -s "$T/results/summary.json";echo 'external trace component plumbing passed'
