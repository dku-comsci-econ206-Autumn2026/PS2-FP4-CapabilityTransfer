# Pay for Training, Not for Openness — Team FP4

COMSCI/ECON 206 · Autumn 2026 · Instructor Luyao Zhang · **Zhengjun He, Yichen Shen**

Paper: *Pay for Training, Not for Openness: Reward Design for Original and Distilled AI Models.*

A firm **distils** or **trains**, then keeps the model **closed** for monopoly profit `pi` or **opens**
it for a reward `kE` while losing exclusivity `L`. An open release also buys a share of the next
generation of infrastructure, worth `beta*phi*K * m / (m + m0)`.

| | closed | open |
|---|---|---|
| **distil** | (1) free rider | (2) passer-on |
| **train** | (3) monopolist | (4) source |

The private ranking `(1) > (3) > (2) > (4)` reverses the social ranking `(4) > (2) > (3) > (1)` while the
future-share motive is weak.

**Live page:** <https://huggingface.co/spaces/dku-comsci-econ206-2026/FP4_PS2>

## What this revision changed

1. **A future market-share motive on the two open cells** (Han Zhang's comment). Notation follows the
   published economics of open source: `beta` discount factor, `phi` ecosystem efficiency, `K` external
   contributions, `m` the firm's share of compatible applications, `m0` the internal-capacity scale. The
   term is `beta*phi*K * m/(m+m0)`, increasing and concave in `m`.
2. **The earlier table is the special case `beta*phi*K = 0`.** Table 2 now has two panels, and the
   simulation prints both.
3. **Corrected thresholds.** Disclosure needs `k*E_d > L + pi*m - beta*phi*K`; with the motive off this is
   `k > (L + pi)/E_d` (the familiar `k > L` assumed `pi = 0`). Innovation needs `k > dC/dE`, which the
   motive does not affect because the term is common to both open cells.
4. **An eight-family evidence table** (`EVIDENCE_TABLE.md`) on whether weights are downloadable, under
   which licence, whether training compute is disclosed, and whether distillation is documented.

## Contents

| File | What |
|---|---|
| `code/distill_sim.py` | the fresh run; reproduces both panels of Table 2 and the compute account |
| `outputs/fresh_run_output.txt` | its saved output log |
| `k_formula.ipynb` | derives the two thresholds with sympy, then runs the two panels (outputs saved) |
| `verify_k.py` | recomputes the four payoffs from scratch, no dependencies |
| `hf_space/` | the interactive page (static Hugging Face Space) |
| `hf_space/test.js` | logic tests for the page, including the new motive |
| `paper/` | the manuscript source and the compiled PDF |
| `EVIDENCE_TABLE.md` | open-weight evidence across eight model families, dated and sourced |
| `CHANGE_MAP.md` | reviewer point to change made, kept in sync with the paper's Appendix D |

## Run

```bash
pip install -r requirements.txt
python code/distill_sim.py          # both panels of Table 2 and the compute account
python verify_k.py                  # the four payoffs, from scratch
jupyter notebook k_formula.ipynb    # the thresholds, symbolically and numerically
node hf_space/test.js               # page logic, including the future-share motive
```

Page: open `hf_space/index.html`.

## Parameters

`N = 20000`, `seed 206`, `sigma_a = sigma_m = 0.6`, `lambda = 1`, `delta = 0.95`, `c_d = 1`,
100 firms, 5 rounds, `B = 100`, `T0 = 25`, `rho = 0.01`, `v = 1`, `c_e = 0.02`, cap `12`, `R = 20`.

Level constants, calibrated so the run reproduces panel (a) (residual `7.4e-5`):
`C_d = 1.4446`, `C_n = 5.6704`, `pi = 8.2391`, `L = 2.5193`, `E_d = 0.9854`, `E_n = 4.6311`.

Future market-share motive: `beta = 0.90`, `phi = 0.50`, `K = 44.4`, `m0 = 0.50`, so `beta*phi*K = 19.98`.

## Result

```
disclosure                       motive off: k > 10.92     motive on: k > -2.60   (at m = 1)
innovation                       k > dC/dE = 1.1591, either way

panel (a) no future-share motive        panel (b) with the motive
none, k = 0      0.96/0.00/0.04/0.00  1 none, k = 0      0.28/0.68/0.01/0.03  2
openness, R = 20 0.11/0.85/0.00/0.04  2 openness, R = 20 0.01/0.95/0.00/0.04  2
indexed, k = 4   0.35/0.00/0.01/0.64  3 indexed, k = 4   0.03/0.02/0.00/0.95  3
indexed, cap = 12 0.42/0.54/0.02/0.03 2 indexed, cap = 12 0.03/0.93/0.00/0.05 2
```

With the motive off, no reward leaves the market closed. With it on, firms open with no reward at all —
but what they open is a copy, so the market settles in state 2. The openness window in `m` is
`(0.101, 1.519)`. Indexing the reward by training compute reaches state 3 either way, and capping it
returns the market to state 2 either way.

## Sources

- all-pay auction and over-dissipation — Baye, Kovenock & de Vries (1996, 1999)
- knowledge distillation — Hinton, Vinyals & Dean (2015)
- why firms open source — Lerner & Tirole (2002); von Hippel & von Krogh (2003); Fosfuri et al. (2008);
  Habibi (2025, arXiv:2501.11581); Xu et al. (2025, arXiv:2510.15200)
- openness regulation and compute governance — Qiu et al. (2025); Sastry et al. (2024); Epoch AI
- model collapse under recursive distillation — Shumailov et al. (2024), *Nature*
- industrial-scale distillation advisory — NSA/CISA/FBI AA26-251A (2026)

Full list with DOIs: `paper/references.bib`.

## Tested release

Course-organization repository:
<https://github.com/dku-comsci-econ206-Autumn2026/PS2-FP4-CapabilityTransfer>

Tested commit: **`8be3f02`** (release merge in the course organization, 2026-10-04). It carries the tested
revision `4c3b928`; both trees are `cb1e48d5628c`, so `git checkout 8be3f02` and `git checkout 4c3b928`
give byte-identical working copies. The paper, this README and `k_formula.ipynb` cite the same commit.
What was run at that commit, from a clean clone:

```
pip install -r requirements.txt
python code/distill_sim.py      # reproduces code/fresh_run_output.txt byte for byte
python verify_k.py              # "all five claims hold"
node hf_space/test.js           # "all tests passed"
```

The paper's Table 2 two-panel numbers are the output of the first command; `outputs/fresh_run_output.txt`
is the same file as `code/fresh_run_output.txt`. Nothing in `code/`, `verify_k.py`, `hf_space/`, the
notebook logic or the result files has changed since `8be3f02`, so the tested release stays reproducible at
that commit; all later edits are documentation and the paper copy.

## License

MIT. See `LICENSE`.
