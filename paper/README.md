# COMSCI/ECON 206 Final Project — Team FP4

Upload this folder to Overleaf (or use it to update the Canvas-shared project) and compile `main.tex` with pdfLaTeX / `latexmk -pdf main.tex`. The clean main text is two A4 pages; Author Notes, references, and Appendices A–G follow.

Authors: Zhengjun He (zhengjun.he@dukekunshan.edu.cn), Yichen Shen (yichen.shen@dukekunshan.edu.cn). Team FP4, symposium session D.

## Files

- `main.tex` — clean final submission driver.
- `sections/proposal.tex` — the eight named parts (Background … Practical Impacts) plus Future Research Roadmap, Evolving 2056 Statement, Open Science/SDG, and Final Submission.
- `appendices/supporting.tex` — Author Notes, full references, and Appendices A–G (technical details + AI disclosure, cumulative development, three lenses, feedback record, structured abstract, retained PS2 auction record, final-week evidence and release audit).
- `figures/ps2_teaser.tex` — the three-panel economics / computer science / behavioral science teaser.
- `references.bib` — full references with DOI or direct URL.
- `code/distill_sim.py`, `code/fresh_run_output.txt` — simulation and its fresh run (seed 206).

## Release status

- Rogerson email recorded in Appendix G (sent October 18, 2026).
- Tested commit `a38a684` recorded in `main.tex` and Appendix G.
- `poster/final-poster.png` and `poster/final-poster.pdf` committed; embedded in the root README.

## Verify locally

```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
python code/distill_sim.py
```
