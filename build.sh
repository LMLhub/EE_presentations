#!/usr/bin/env bash
set -euo pipefail

# Usage: ./build.sh presentations/20260326-01-01
PRES_DIR="$(cd "${1:?Usage: ./build.sh <presentation-folder>}" && pwd)"
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -f "$PRES_DIR/main.tex" ]]; then
  echo "Error: $PRES_DIR/main.tex not found" >&2
  exit 1
fi

cd "$PRES_DIR"

# Let pdflatex find shared/ via TEXINPUTS
export TEXINPUTS=".:${REPO_ROOT}/shared//:${TEXINPUTS:-}"

echo "==> Compiling main.tex in $PRES_DIR ..."
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

echo "==> Cleaning up ..."
rm -f "$PRES_DIR/main."{aux,log,nav,out,snm,toc,vrb}

echo "==> Done: $PRES_DIR/main.pdf"
