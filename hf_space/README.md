---
title: Prize Rate Game
emoji: 🎚️
colorFrom: indigo
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: Prize rate k and the future-share motive pick the state.
---

# Prize Rate Game

Team FP4 · COMSCI/ECON 206 · Instructor Luyao Zhang.

A firm **distils** a model or **trains** one, then keeps it **closed** for monopoly profit or **opens** it.
Opening pays a prize of `k` per unit of training compute `E`, but gives up the edge you had — and it buys a
share of the next generation of infrastructure, worth `beta*phi*K*m/(m+m0)`.

Move `k`, switch the future market-share motive on or off, and see which state the market falls into.
No data is collected.

## The four payoffs

```
(1) closed, distill   -C_d + πm
(2) open,   distill   -C_d + k·E_d − L + βφK·m/(m+m0)
(3) closed, train     -C_n + πm
(4) open,   train     -C_n + k·E_n − L + βφK·m/(m+m0)
```

`C_d` cost to distil · `C_n` cost to train · `π` profit while nobody else can use your model ·
`m` your share of compatible applications · `k` prize per unit of training compute · `E` training compute ·
`L` what opening costs you · `β` discount factor · `φ` efficiency of the open-source ecosystem ·
`K` external contributions an open release attracts · `m0` the internal-capacity scale.

## The two lines where the market flips

```
k·E_d > L + πm − βφK·m/(m+m0)     opening beats keeping it closed
k > ΔC / ΔE                        training beats distilling
```

With the motive off this is `k > (π + L)/E_d` (the familiar `k > L` assumed `π = 0`). The innovation
threshold does not move with the motive, because the term is common to both open cells.

## What the two panels show

| Reward rule | (a) no motive | (b) with the motive |
|---|---|---|
| none, k = 0 | .96/.00/.04/.00 — state 1 closed | .28/.68/.01/.03 — **state 2 distill** |
| openness, R = 20 | .11/.85/.00/.04 — state 2 | .01/.95/.00/.04 — state 2 |
| indexed, k = 4 | .35/.00/.01/.64 — **state 3 healthy** | .03/.02/.00/.95 — **state 3 healthy** |
| indexed, capped, k = 12 | .42/.54/.02/.03 — state 2 | .03/.93/.00/.05 — state 2 |

With the motive off, no reward leaves the market closed. With it on, firms open with no reward at all —
but what they open is a copy, so the market settles in state 2. The openness window is `m ∈ (0.101, 1.519)`:
outside it, a firm stays closed. Indexing the reward by training compute reaches state 3 either way, and
capping it returns the market to state 2 either way.

## Sources

Why firms release weights without a reward — the ecosystem and future-share motive:
[Habibi (2025), *Open Sourcing GPTs*](https://arxiv.org/abs/2501.11581) ·
[Xu et al. (2025), *The Economics of AI Foundation Models*](https://arxiv.org/abs/2510.15200) ·
[Lerner & Tirole (2002), *Some Simple Economics of Open Source*](https://doi.org/10.1111/1467-6451.00174).
Prizes beside patents and research contracts: Nalebuff & Stiglitz (1983). Distillation versus training from
scratch under a fixed compute budget:
[ACL 2024 (Insights)](https://aclanthology.org/2024.insights-1.6/).
Model collapse under recursive distillation:
[Shumailov et al. (2024), *Nature*](https://doi.org/10.1038/s41586-024-07566-y).
Compute governance: Sastry et al. (2024), arXiv:2402.08797.

The full list, with DOIs, is in the paper's `references.bib` in the GitHub repository.
