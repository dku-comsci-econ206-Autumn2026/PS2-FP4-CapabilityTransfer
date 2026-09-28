# Pay for Training, Not for Openness — Team FP4

COMSCI/ECON 206 · Autumn 2026 · Instructor Luyao Zhang · **Zhengjun He, Yichen Shen**

Paper: *Pay for Training, Not for Openness: Reward Design for Original and Distilled AI Models.*

A firm **distils** or **trains**, then keeps the model **closed** for monopoly profit `pi`
or **opens** it for a reward `kE` while losing exclusivity `L`. Four decisions:

| | closed | open |
|---|---|---|
| **distil** | (1) free rider | (2) passer-on |
| **train** | (3) monopolist | (4) source |

The private ranking `(1) > (3) > (2) > (4)` exactly reverses the social ranking
`(4) > (2) > (3) > (1)`, so without policy the market stops at (1).

**Live page:** <https://huggingface.co/spaces/dku-comsci-econ206-2026/FP4_PS2>

## Contents

| File | What |
|---|---|
| `code/distill_sim.py` | fresh run; reproduces Table 2 and the compute account |
| `code/fresh_run_output.txt` | its output log |
| `k_formula.ipynb` | derives the two thresholds on `k` with sympy |
| `verify_k.py` | recomputes the four payoffs from scratch, no dependencies |
| `hf_space/` | the interactive page (static Hugging Face Space) |

## Run

```bash
python code/distill_sim.py          # Table 2 and the compute account
python verify_k.py                  # the four payoffs, from scratch
pip install sympy jupyter
jupyter notebook k_formula.ipynb    # the thresholds, symbolically
```

Page: open `hf_space/index.html`. Logic check: `cd hf_space && node test.js`.

## Result

```
k > (pi + L) / E_d    disclosure beats closing   (Tool 1 gets this far)
k > dC / dE           training beats distilling  (only Tool 2 gets here)
```

**Tool 1** pays a lump sum for any open release, so (2) and (4) receive the same amount
and (2) wins at every level: nobody trains, sources run out, state 2.
**Tool 2** pays per unit of reported training compute, so (4) collects the largest reward
and (2) the smallest, which is the only reason a second threshold exists.

Table 2 (seed 206, N = 20000), shares per decision:

| Reward rule | (1)/(2)/(3)/(4) | State |
|---|---|---|
| none, k = 0 | .96 / .00 / .04 / .00 | 1 closed |
| openness, R = 20 | .11 / .85 / .00 / .04 | 2 distill |
| indexed, k = 4 | .35 / .00 / .01 / .64 | 3 healthy |
| indexed, capped, k = 12 | .42 / .54 / .02 / .03 | 2 distill |

Capping so that small-`E` and large-`E` releases are paid alike removes the differential
and returns the market to state 2.

## Parameters

Appendix A gives `N = 20000`, `seed 206`, `sigma = 0.6`, `lambda = 1`, `delta = 0.95`,
`T0 = 25`, `B = 100`, `rho = 0.01`, `v = 1`, `c_e = 0.02`, cap `12`, `R = 20`.
The six level constants (`C_d`, `C_n`, `pi`, `L`, `E_d`, `E_n`) are fitted so the
simulation reproduces Table 2, residual `7.4e-5`. They are listed at the top of
`code/distill_sim.py`.

## Sources

- all-pay auction, over-dissipation — Baye, Kovenock & de Vries (1996), *Economic Theory* 8(2) 291–305
- knowledge distillation — Hinton, Vinyals & Dean (2015), arXiv:1503.02531
- optimal auction design — Myerson (1981); counterspeculation — Vickrey (1961)
- equilibrium points — Nash (1950)

## License

MIT. See `LICENSE`.
