#!/usr/bin/env bash
set -euo pipefail

FAIL=0

if grep -rnw --include='*.lean' 'sorry' AflbLean.lean AflbLean/ ; then
  echo "FAIL: residual 'sorry' found in sources." >&2
  FAIL=1
fi

if [ -f docs/build.log ] && grep -q "uses 'sorry'" docs/build.log ; then
  echo "FAIL: compiler reports a declaration uses sorry." >&2
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  echo "OK: no sorry in sources or build log."
fi

exit $FAIL
