#!/usr/bin/env bash
set -euo pipefail

TEXFILE="20260326-01-01"

echo "==> Compiling $TEXFILE.tex ..."
pdflatex -interaction=nonstopmode "$TEXFILE.tex"
pdflatex -interaction=nonstopmode "$TEXFILE.tex"

echo "==> Cleaning up ..."
rm -f "$TEXFILE".{aux,log,nav,out,snm,toc,vrb}

echo "==> Done: $TEXFILE.pdf"
