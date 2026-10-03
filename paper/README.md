# COMSCI/ECON 206 PS2 — Team FP4

Upload this ZIP to Overleaf and compile `main.tex` with pdfLaTeX.

Authors: Zhengjun He (zhengjun.he@dukekunshan.edu.cn), Yichen Shen (yichen.shen@dukekunshan.edu.cn).
A third author slot is left blank in `main.tex` as a comment; add `\author{}`, `\affiliation{}`, `\email{}` when known. Symposium session is blank.

## Files

- `main.tex` — clean submission driver.
- `sections/proposal.tex` — Sections 1–5 (Q1 economics, Q2 computation, Q3 behavior, roadmap).
- `appendices/supporting.tex` — Author Notes, references, Appendices A–F (A AI disclosure, B cumulative
  intellectual development, C open-source record and three lenses, D review response and revision record,
  E structured author notes, F PS2 extension record).
- `figures/ps2_teaser.tex` — three-panel teaser figure.
- `references.bib` — 34 verified entries (all DOIs/arXiv IDs resolved live on 2026-10-03).
- `code/distill_sim.py`, `code/fresh_run_output.txt` — simulation and its fresh run (seed 206).
- `annotated.tex`, `annotations/` — instructor's guidance rail; not the submission driver.
- `main.pdf` — compiled result at packaging time (7 pages: 2 main + 5 appendix pages).

## Artifact links (verified 200 OK)

GitHub: https://github.com/dku-comsci-econ206-Autumn2026/PS2-FP4-CapabilityTransfer
  — holds `k_formula.ipynb` (sympy derivation of the two thresholds on k), `verify_k.py`,
  and `hf_space/`.

Hugging Face Space "Prize Rate Game": https://huggingface.co/spaces/dku-comsci-econ206-2026/FP4_PS2

The A0 poster (`PS2-FP04-A0-Poster.pptx` / `.pdf`) ships in `poster/` and quotes the same fresh run (seed 206).

## Verify locally

```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
python code/distill_sim.py
```
