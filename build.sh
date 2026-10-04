#!/usr/bin/env bash
# Rebuild the finite checks, plot data and manuscript from the source directory.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
command -v python3 >/dev/null || { echo 'Python 3.10+ is required.' >&2; exit 1; }
command -v pdflatex >/dev/null || { echo 'pdfLaTeX and the packages listed in README.md are required.' >&2; exit 1; }
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ is required"'
mkdir -p build
python3 checks/model_checks.py > build/model-checks.stdout
python3 checks/quantum_checks.py > build/quantum-checks.stdout
for pass in 1 2 3; do
    if ! pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
        -output-directory=build main.tex > "build/latex-pass-${pass}.stdout" 2>&1; then
        tail -n 65 "build/latex-pass-${pass}.stdout" >&2
        exit 1
    fi
done
if grep -nE '(^!|LaTeX Warning|Package .* Warning|Class .* Warning|Overfull|Underfull|undefined)' build/main.log; then
    echo 'The final LaTeX log contains a diagnostic; inspect build/main.log.' >&2
    exit 1
fi
cp build/main.pdf manuscript.pdf
printf '%s\n' 'Build passed. Output: manuscript.pdf; finite checks: checks/*results.json.'
