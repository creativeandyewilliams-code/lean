#!/usr/bin/env bash
set -euo pipefail

echo "=== system ==="
id || true
uname -a || true

missing=()
for cmd in python3 pdflatex latexmk pdftotext pdfinfo pdftoppm qpdf git; do
  command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
done
if ((${#missing[@]})); then
  echo "Missing commands: ${missing[*]}"
  if command -v apt-get >/dev/null 2>&1; then
    if [ "$(id -u)" -eq 0 ]; then SUDO=""; elif command -v sudo >/dev/null 2>&1; then SUDO=sudo; else SUDO=""; fi
    if [ "$(id -u)" -eq 0 ] || [ -n "$SUDO" ]; then
      set +e
      $SUDO apt-get update
      $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y qpdf poppler-utils texlive-latex-base texlive-latex-recommended texlive-latex-extra latexmk python3-jsonschema git
      set -e
    fi
  fi
fi

python3 - <<'PY'
try:
    import jsonschema
    print('jsonschema available')
except Exception as e:
    print('jsonschema unavailable:', e)
    raise
PY

for cmd in python3 pdflatex latexmk pdftotext pdfinfo pdftoppm qpdf git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "REQUIRED COMMAND STILL MISSING: $cmd" >&2
    exit 2
  fi
done

if command -v lake >/dev/null 2>&1 && command -v lean >/dev/null 2>&1; then
  lean --version
  lake --version
else
  echo "Lean/Lake missing. Install with elan before running run_lean_checks_v23.sh." >&2
fi
