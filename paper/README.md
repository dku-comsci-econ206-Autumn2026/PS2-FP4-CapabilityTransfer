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

## To finish before submission (grep for `TODO` and `[FINAL-COMMIT]`)

1. Record the Rogerson email in Appendix G (sent date + the specific contribution thanked + the one question asked).
2. Replace `[FINAL-COMMIT]` with the real commit hash after the final push (main.tex and Appendix G).
3. Commit `poster/final-poster.png` and `poster/final-poster.pdf`, and add the embed + PDF link to the repository **root** README.

## Verify locally

```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
python code/distill_sim.py
```
