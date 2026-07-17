#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python "$R/code/generate_packets.py" --out "$T/p";python "$R/code/mock_certificates.py" --packets "$T/p" --out "$T/c";python "$R/code/validate_certificates.py" --certificates "$T/c" >/dev/null;echo 'physical mapping component plumbing passed'
