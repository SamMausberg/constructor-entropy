# Comparison, coherence and the stability of constructor entropy

Read the [final manuscript](constructor_entropy.pdf). This is an unpublished research
manuscript, released with its calculations and supporting material.

## Release and verification

The LaTeX source matches the final manuscript. On October 8, 2026,
`bash build.sh` passed in a fresh directory using Python 3.12.3 and
pdfTeX 1.40.25 (TeX Live 2023/Debian). All 25 rebuilt pages match the
final PDF in extracted text and rendered pixels. The final PDF is preserved
byte for byte; rebuilt PDF metadata may differ.

The final LaTeX pass had no unresolved references, warnings, or overfull or
underfull boxes. Both retained finite checking programs passed. These checks
support the supplied examples and source reproduction; they do not verify
every argument in the final PDF. There are no Lean sources or Lake projects.

See [the current source reproduction record](verification/source-reproduction.json)
and [current build log](verification/source-reproduction-build.log), with the
[final LaTeX log](verification/source-reproduction-latex.log).
The [October 4 validation record](verification/release.json),
[its execution log](verification/build.log), and earlier records in `checks/`
and `verification/checks/` describe the earlier source revision. Their
source/PDF mismatch statements are historical.

Samuel Mausberg, Independent Researcher

Research manuscript in a journal-style layout.

## Scope

The paper proves a bounded-work calibration criterion for entropy-neutral tasks in finite reversible realizations that contain an explicit controlled interchange. It constructs a stationary quantum completion, including entangled states within degenerate total-energy sectors, and checks the repaired thermodynamic clauses. A third theorem excludes nonstationary states from a convex comparison domain containing a pure energy state and the maximally mixed state.

The paper does **not** derive scalar entropy from the repaired operational clauses in every possible subsidiary theory, and it does **not** give a physically complete non-scalar countermodel. The remaining question is whether the stated clauses force uniform work calibration across the vanishing-flag family. The maximal-gate completion has this uniformity; general restricted gate classes are not resolved.

## Build

Run from this folder:

```sh
bash build.sh
```

The script runs both finite checking programs, regenerates the Gibbs data, runs pdfLaTeX three times, and writes `manuscript.pdf`. It stops if the final log has unresolved references, LaTeX/package warnings or overfull/underfull boxes.

Requirements: Python 3.10 or later, pdfLaTeX, and the LaTeX packages used in `main.tex`. A reasonably complete TeX Live installation supplies `amsmath`, `amssymb`, `amsthm`, `mathtools`, `lmodern`, `geometry`, `microtype`, `graphicx`, `xcolor`, `tikz`, `pgfplots`, `fancyhdr`, `enumitem`, `needspace`, `hyperref`, `cleveref` and `caption`. The current manuscript uses the standard article class. The retained Python checks use only the standard library. No network access or shell escape is needed to build.

The source was synchronized from the supplied final revision without changing its rendered content. Expanding the five appendix/bibliography inputs recovers that revision exactly. The plot data and numerical macros are embedded in `main.tex`.

## Source files

`main.tex` contains the main text and the calibration diagram. `axioms.tex` specifies the repaired clauses with locators to arXiv:1608.02625v5. `new_proofs.tex` proves entropy monotonicity, the calibration criterion, its compensation consequences, the memory-size obstruction and the cancellation lemma. `classical_proofs.tex` gives the exact-energy-shell permutation construction, the stationary memory and bounded work calibration. `quantum_checks.tex` gives the quantum reduction, clause-by-clause model checks, the product-return obstruction and the coherence argument. `references.tex` contains the complete bibliography.

The current TikZ/pgfplots figure and its Gibbs data are embedded in `main.tex`. The files in `figures/` are retained supporting material from the earlier source revision and are not inputs to the current manuscript.

## Finite checks

`checks/model_checks.py` exhaustively checks the 1,029-configuration clock permutation, its energy conservation, exact memory stationarity, repeated fresh visits, and six work-swap permutations on 49 configurations each. Stationarity calculations use rational arithmetic. The engine calculation uses ordinary floating-point evaluation of the finite seven-level partition function.

`checks/quantum_checks.py` checks the 98-configuration controlled interchange, the 49-dimensional energy-preserving Hadamard gate, the 98-dimensional controlled phase, exact output and control marginals, and an entanglement witness. Hadamard entries are calculated exactly in Q(sqrt(2)); density matrices and marginal checks use rational arithmetic.

The outputs are `checks/results.json` and `checks/quantum_results.json`. These finite tests support the displayed examples. They are not numerical proofs of the all-accuracy conversion theorem and are not a formal proof-assistant verification. The mathematical arguments, including the scope of imported structural theorems, are in the text and appendices.

## Retained class provenance

`iopjournal.cls` is retained from the earlier source revision and is not used by the current build. It is the IOP Publishing journal class carrying the 2024/01/31 class identifier and the 2025 copyright notice. It is redistributed unmodified under the LaTeX Project Public License 1.3c or later, as permitted by its header. The class file remains unmodified.

The public mirror used to obtain the class was:

https://github.com/alanknguyen/QSOL_CQED/blob/1e32dcf888dc02436ca82b6eabfc8a8a3164eb44/paper/ejp/iopjournal.cls

No font files are included. The header says "Research manuscript" and does not claim publication, acceptance, or assigned journal metadata.

## License and citation

The manuscript and original research material use [CC BY 4.0](LICENSES/CC-BY-4.0.txt).
Original code uses [MIT](LICENSES/MIT.txt). Third-party notices remain in effect.
See [LICENSE](LICENSE) for the scope and [CITATION.cff](CITATION.cff) for citation metadata.
