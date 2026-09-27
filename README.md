# Capability-Transfer Openness — Team FP4

COMSCI/ECON 206 · Autumn 2026 · Instructor Luyao Zhang · **Zhengjun He, Yichen Shen**

Firms choose **imitate or innovate**, then **openness or secrecy**. A prize rate `k`
rewards disclosure, paid per unit of training budget `E`. This repository derives the
range of `k` that keeps the market healthy.

**Live page:** <https://huggingface.co/spaces/dku-comsci-econ206-2026/FP4_PS2>

## Contents

| File | What |
|---|---|
| `k_formula.ipynb` | derives the two thresholds on `k`, with sympy |
| `hf_space/` | the interactive page (static Hugging Face Space) |

## Run

```bash
pip install sympy jupyter
jupyter notebook k_formula.ipynb
```

Game: open `hf_space/index.html` in a browser.
Logic check: `cd hf_space && node test.js`.

## Result

```
k > L             disclosure beats the competition loss
k > ΔC / ΔE       someone still prefers to innovate
=> healthy range: k > max(L, ΔC/ΔE)
```

Below the bound, nobody discloses: all secrecy. Between the two lines, everyone
discloses but nobody innovates: all imitation. If the prize is paid flat instead of per
unit of `E`, the second line vanishes and no `k` can sustain innovation.

## Terms and sources

- openness / secrecy, learning spillover vs competition — [Dasaratha, *Innovation and Strategic Network Formation*](https://arxiv.org/abs/1911.06872)
- prize as a disclosure incentive, beside patents and research contracts — [Wright (1983)](https://www.merit.unu.edu/publications/rmpdf/1994/rm1994-017.pdf)
- distillation cost vs training from scratch — [Rethinking LLM distillation under a fixed compute budget](https://aclanthology.org/2024.insights-1.6/)

No calibrated numbers. `L`, `ΔC`, `ΔE` are inputs the reader sets, not estimates.

## License

MIT. See `LICENSE`.
