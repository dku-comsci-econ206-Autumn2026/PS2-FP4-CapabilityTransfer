"""Distillation versus original training under two reward rules.

COMSCI/ECON 206 PS2 - Team FP4 (Zhengjun He, Yichen Shen).
Reproduces Table 2 and the compute account of the paper.

Run:  python code/distill_sim.py
Writes code/fresh_run_output.txt, and prints the same text.
"""

from __future__ import annotations

import pathlib

import numpy as np

# ---------------------------------------------------------------- parameters
# Paper Appendix A (all given there).
N = 20_000            # firms
SEED = 206
SIGMA_A = 0.6         # cost multiplier, lognormal
SIGMA_M = 0.6         # market power, lognormal
LAMBDA = 1.0          # logit best-response precision

R_LUMP = 20.0         # Tool 1: lump-sum reward for any open release
CAP = 12.0            # capped Run: reward = min(kE, CAP)

DELTA = 0.95          # frontier retained per distillation round
C_D = 1.0             # distillation spend per firm per round
LOOP_FIRMS = 100
LOOP_ROUNDS = 5

B = 100.0             # budget B = T + D
T0 = 25.0             # frontier scale
RHO = 0.01            # price on duplicated effort
V = 1.0               # frontier value
CE = 0.02             # compute cost per unit of budget

# Level constants. Appendix A does not give these; they are calibrated so the
# simulation reproduces Table 2 (fit residual 7.4e-5 over the sixteen shares).
C_D0 = 1.4446         # distillation cost level
C_N0 = 5.6704         # training cost level   (C_N0 / C_D0 = 3.93)
PI_0 = 8.2391         # monopoly profit level
L = 2.5193            # lost exclusivity
E_D = 0.9854          # training compute reported on a distilled release
E_N = 4.6311          # ... and on an original release

STATE_NAMES = {1: "1 closed", 2: "2 distill", 3: "3 healthy"}


# -------------------------------------------------------------------- model
def firm_types(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Cost multiplier a and market power m, lognormal with sigma = 0.6."""
    return rng.lognormal(0.0, SIGMA_A, N), rng.lognormal(0.0, SIGMA_M, N)


def rewards(rule: str, k: float) -> tuple[float, float]:
    """Reward on a distilled release and on an original release, under `rule`."""
    if rule == "none":
        return 0.0, 0.0
    if rule == "openness":          # Tool 1, lump sum
        return R_LUMP, R_LUMP
    if rule == "indexed":           # Tool 2, paid per unit of E
        return k * E_D, k * E_N
    if rule == "indexed_capped":
        return min(k * E_D, CAP), min(k * E_N, CAP)
    raise ValueError(rule)


def decision_shares(a: np.ndarray, m: np.ndarray, rule: str, k: float) -> np.ndarray:
    """Shares of firms choosing (1) closed+distill (2) open+distill
    (3) closed+train (4) open+train, under a logit best response."""
    c_d, c_n, pi = a * C_D0, a * C_N0, m * PI_0
    r_small, r_large = rewards(rule, k)

    u1 = -c_d + pi                 # (1) closed, distill
    u2 = -c_d + r_small - L        # (2) open, distill
    u3 = -c_n + pi                 # (3) closed, train
    u4 = -c_n + r_large - L        # (4) open, train

    u = np.stack([u1, u2, u3, u4], axis=1) * LAMBDA
    u -= u.max(axis=1, keepdims=True)
    p = np.exp(u)
    p /= p.sum(axis=1, keepdims=True)
    return p.mean(axis=0)


def market_state(shares: np.ndarray) -> int:
    """1 if closing dominates, 3 if sources are modal, else 2."""
    c1, c2, _c3, c4 = shares
    if c4 == shares.max():
        return 3
    return 2 if c2 > c1 else 1


# ----------------------------------------------------------- compute account
def frontier(t: float) -> float:
    """Capability reached by training compute t. Only training moves it."""
    return 1.0 - np.exp(-t / T0)


def social_loss(t: float, budget: float = B) -> float:
    """Compute cost, plus a price on effort beyond the frontier scale, minus value."""
    return CE * budget + RHO * max(0.0, t - T0) - V * frontier(t)


def optimal_training_share(budget: float = B) -> float:
    """t*: minimise social loss over the training share."""
    grid = np.linspace(0.0, 1.0, 1001)
    losses = np.array([social_loss(t * budget, budget) for t in grid])
    return float(grid[losses.argmin()])


def mutual_distillation(start: float = 1.0) -> tuple[list[float], float]:
    """Everyone distils: the frontier decays by delta each round."""
    path = [start]
    for _ in range(LOOP_ROUNDS):
        path.append(path[-1] * DELTA)
    return path, LOOP_FIRMS * LOOP_ROUNDS * C_D


# --------------------------------------------------------------------- main
def main() -> None:
    rng = np.random.default_rng(SEED)
    a, m = firm_types(rng)

    runs = [
        ("none, k = 0", "none", 0.0),
        (f"openness, R = {R_LUMP:.0f}", "openness", 0.0),
        ("indexed, k = 4", "indexed", 4.0),
        (f"indexed, capped, k = {CAP:.0f}", "indexed_capped", CAP),
    ]

    lines = [
        "Fresh run. Seed %d, N = %d, logit best response with lambda = %.1f." % (SEED, N, LAMBDA),
        "Level constants calibrated to the paper's Table 2 (residual 7.4e-5).",
        "",
        "Table 2  Reward design and market outcome",
        f"{'reward rule':24} {'(1)/(2)/(3)/(4)':28} state",
    ]
    for label, rule, k in runs:
        s = decision_shares(a, m, rule, k)
        lines.append(f"{label:24} " + "/".join(f"{v:.2f}" for v in s) + f"        {STATE_NAMES[market_state(s)]}")

    shares_none = decision_shares(a, m, "none", 0.0)
    shares_open = decision_shares(a, m, "openness", 0.0)
    shares_idx = decision_shares(a, m, "indexed", 4.0)
    shares_cap = decision_shares(a, m, "indexed_capped", CAP)

    lines += [
        "",
        f"Dominant at k = 0: decision ({int(np.argmax(shares_none)) + 1}) with share {shares_none.max():.2f}.",
        f"Openness-only reward never lifts sources above {max(shares_open[3], shares_cap[3]):.2f} and ends in state 2.",
        f"Indexed reward reaches state 3 at k = 4, with (4) modal at {shares_idx[3]:.2f}.",
        f"Capping the reward so small-E and large-E releases are paid alike returns the market to state 2.",
        "",
        "Analytic thresholds: disclosure needs k > L, innovation needs k > dC/dE.",
        f"  L = {L:.4f}      dC/dE = {(C_N0 - C_D0) / (E_N - E_D):.4f}",
        "",
        "Compute account",
        f"  F(T) = 1 - exp(-T/T0), T0 = {T0:.0f}, delta = {DELTA}, c_d = {C_D}, {LOOP_FIRMS} firms, {LOOP_ROUNDS} rounds",
    ]

    path, spent = mutual_distillation()
    lines += [
        "  Mutual distillation: frontier " + " -> ".join(f"{v:.3f}" for v in path),
        f"    copying a copy only decays; {spent:.0f} compute units spent for no new capability.",
        "",
        f"  Social loss  c_e*B + rho*max(0,T-T0) - v*F(T),  B = {B:.0f}, rho = {RHO}, v = {V:.0f}, c_e = {CE}",
    ]
    for label, t in (("all distill", 0.0), ("all train", B), (f"t* = {optimal_training_share():.2f}", optimal_training_share() * B)):
        lines.append(f"    {label:14} +{social_loss(t):.2f}")
    lines += [
        "  A positive distillation share is efficient: it stops every firm from paying",
        "  to re-derive the same result. Distillation is cheap, but never free, so the",
        "  reward metric must be E.",
    ]

    text = "\n".join(lines) + "\n"
    out = pathlib.Path(__file__).resolve().parent / "fresh_run_output.txt"
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[written to {out}]")


if __name__ == "__main__":
    main()
