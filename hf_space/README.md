---
title: Prize Rate Game
emoji: 🎚️
colorFrom: indigo
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: How a prize rate k picks the market state.
---

# Prize Rate Game

Team FP4 · COMSCI/ECON 206 · Instructor Luyao Zhang.

Firms choose **imitate or innovate**, then **openness or secrecy**. A prize rate `k`
rewards disclosure, paid per unit of training budget `E`.

Drag `k` and see which market state the economy falls into. No data is collected.

## The two thresholds

`k > L`          → disclosure beats the competition loss
`k > ΔC / ΔE`    → someone still prefers to innovate

`k > max(L, ΔC/ΔE)` → healthy. Below that, the market falls to one end.

## What is not in this page

No calibrated numbers. `L`, `ΔC`, `ΔE` are set by you; units are `E_d = 1`, `C_d = 0`.
The formula is derived in `k_formula.ipynb`.

## Terms

openness / secrecy and the learning-spillover-versus-competition tradeoff:
[Dasaratha, *Innovation and Strategic Network Formation*](https://arxiv.org/abs/1911.06872).
Prize as a disclosure incentive, alongside patents and research contracts:
[Wright (1983)](https://www.merit.unu.edu/publications/rmpdf/1994/rm1994-017.pdf).
Distillation cost versus training from scratch:
[Rethinking LLM distillation under a fixed compute budget](https://aclanthology.org/2024.insights-1.6/).
