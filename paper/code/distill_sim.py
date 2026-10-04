"""Distillation versus original training under two reward rules.

COMSCI/ECON 206 PS2 - Team FP4 (Zhengjun He, Yichen Shen).
Reproduces Table 2 and the compute account of the paper.

Revision (PS2 v2).  The four decisions now carry a **future market-share** payoff on
the two open cells, so that the model can explain why firms release weights without
any reward at all.  Notation follows the published economics of open source:

  beta   time discount factor                       (Habibi 2025, Table 6)
  phi    efficiency of the open source ecosystem    (Habibi 2025, Table 6)
  K      external contributions an open release attracts (Habibi 2025, Eq. 5, K_{-A})
  m      the firm's share of compatible applications (Habibi 2025, "their mass m")
  m0     internal-capacity scale: beyond it, external contributions stop mattering
         relative to the firm's own development (Habibi 2025: "when the firm becomes
         too large, the benefits of external contributions ... diminish in comparison
         to internal contributions")

  future(m) = beta * phi * K * m / (m + m0)         (saturating, increasing, concave)

Setting ECOSYSTEM = beta * phi * K = 0 switches the motive off and reproduces the
paper's earlier table exactly, so the earlier result is the special case of no
ecosystem motive.

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

# Level constants. Calibrated so the simulation reproduces the paper's Table 2
# when the ecosystem motive is switched off (fit residual 7.4e-5 over sixteen shares).
C_D0 = 1.4446         # distillation cost level
C_N0 = 5.6704         # training cost level   (C_N0 / C_D0 = 3.93)
PI_0 = 8.2391         # monopoly profit level
L = 2.5193            # lost exclusivity
E_D = 0.9854          # training compute reported on a distilled release
E_N = 4.6311          # ... and on an original release

# --- future market-share (ecosystem) motive -------------------------------------
BETA = 0.90           # time discount factor
PHI = 0.50            # efficiency of the open source ecosystem
K_EXT = 44.4          # external contributions an open release attracts
M0 = 0.50             # internal-capacity scale
ECOSYSTEM = BETA * PHI * K_EXT      # beta * phi * K = 19.98

STATE_NAMES = {1: "1 closed", 2: "2 distill", 3: "3 healthy"}


# -------------------------------------------------------------------- model
def firm_types(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Cost multiplier a and market power m, lognormal with sigma = 0.6."""
    return rng.lognormal(0.0, SIGMA_A, N), rng.lognormal(0.0, SIGMA_M, N)


def future_share_payoff(m: np.ndarray | float, ecosystem: float = ECOSYSTEM, m0: float = M0):
    """Value of the future market share an open release buys, beta*phi*K*m/(m+m0)."""
    return ecosystem * np.asarray(m, dtype=float) / (np.asarray(m, dtype=float) + m0)


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


def decision_shares(a: np.ndarray, m: np.ndarray, rule: str, k: float,
                    ecosystem: float = ECOSYSTEM) -> np.ndarray:
    """Shares of firms choosing (1) closed+distill (2) open+distill
    (3) closed+train (4) open+train, under a logit best response."""
    c_d, c_n, pi = a * C_D0, a * C_N0, m * PI_0
    r_small, r_large = rewards(rule, k)
    future = future_share_payoff(m, ecosystem)

    u1 = -c_d + pi                     # (1) closed, distill
    u2 = -c_d + r_small - L + future   # (2) open,   distill  + future share
    u3 = -c_n + pi                     # (3) closed, train
    u4 = -c_n + r_large - L + future   # (4) open,   train    + future share

    u = np.stack([u1, u2, u3, u4], axis=1) * LAMBDA
    u -= u.max(axis=1, keepdims=True)
    p = np.exp(u)
    p /= p.sum(axis=1, keepdims=True)
    return p.mean(axis=0)


def openness_window(ecosystem: float = ECOSYSTEM, m0: float = M0) -> tuple[float, float]:
    """Range of m where a firm opens at k = 0: future(m) > L + PI_0*m.

    Solves PI_0*m^2 + (PI_0*m0 + L - ecosystem)*m + L*m0 = 0.
    """
    qa = PI_0
    qb = PI_0 * m0 + L - ecosystem
    qc = L * m0
    disc = qb * qb - 4 * qa * qc
    if disc <= 0:
        return (float("nan"), float("nan"))
    r = np.sqrt(disc)
    return ((-qb - r) / (2 * qa), (-qb + r) / (2 * qa))


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


def state3_threshold(ecosystem: float = ECOSYSTEM) -> float:
    """Smallest k at which an E-indexed reward makes original sources modal."""
    rng = np.random.default_rng(SEED)
    a, m = firm_types(rng)
    lo, hi = 0.0, 50.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if market_state(decision_shares(a, m, "indexed", mid, ecosystem)) == 3:
            hi = mid
        else:
            lo = mid
    return hi


# ---------------------------------------------------------- auction account
def auction_account(rule: str, k: float, ecosystem: float = ECOSYSTEM) -> dict:
    """Auction reading of one reward rule, in expected values over the firm draws.

    The bid is the training compute E of a release: a distilled release bids E_d,
    an original release bids E_n, and a closed firm does not bid. Under the all-pay
    reading every bidder pays its own bid, because the training cost is sunk whether
    or not the release wins. Allocation in our rule is proportional (each release is
    paid kE), not winner-take-all; the winner-take-all reading is reported separately.
    """
    rng = np.random.default_rng(SEED)
    a, m = firm_types(rng)
    c_d, c_n, pi = a * C_D0, a * C_N0, m * PI_0
    future = future_share_payoff(m, ecosystem)
    r_small, r_large = rewards(rule, k)
    u = np.stack([-c_d + pi, -c_d + r_small - L + future,
                  -c_n + pi, -c_n + r_large - L + future], axis=1)
    z = u * LAMBDA
    z -= z.max(axis=1, keepdims=True)
    p = np.exp(z)
    p /= p.sum(axis=1, keepdims=True)
    p2, p4 = p[:, 1], p[:, 3]
    sources = float(p4.sum())
    opens = float(p2.sum() + p4.sum())
    prize = float((p2 * r_small + p4 * r_large).sum())
    bid = float((p2 * E_D + p4 * E_N).sum())
    return {
        "opens": opens,
        "sources": sources,
        "source_share": sources / opens if opens else float("nan"),
        "prize": prize,
        "bid_compute": bid,
        "spend_per_source": prize / sources if sources else float("nan"),
        "rent_over_prize": bid / prize if prize else float("nan"),
        "utility": float((p * u).mean()),
    }


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
        "Level constants calibrated so that beta*phi*K = 0 reproduces the paper's earlier table.",
        "",
    ]

    def table(title: str, ecosystem: float) -> None:
        lines.append(title)
        lines.append(f"{'reward rule':24} {'(1)/(2)/(3)/(4)':28} state")
        for label, rule, k in runs:
            s = decision_shares(a, m, rule, k, ecosystem)
            lines.append(f"{label:24} " + "/".join(f"{v:.2f}" for v in s)
                         + f"        {STATE_NAMES[market_state(s)]}")
        lines.append("")

    table("Table A  no ecosystem motive  (beta*phi*K = 0)", 0.0)
    table(f"Table B  with the future market-share motive  (beta*phi*K = {ECOSYSTEM:.2f}, m0 = {M0})",
          ECOSYSTEM)

    lo, hi = openness_window()
    inside = float(((m > lo) & (m < hi)).mean())
    shares_none = decision_shares(a, m, "none", 0.0)
    shares_idx = decision_shares(a, m, "indexed", 4.0)
    shares_cap = decision_shares(a, m, "indexed_capped", CAP)

    lines += [
        "Future market-share motive",
        f"  future(m) = beta*phi*K*m/(m+m0),  beta = {BETA}, phi = {PHI}, K = {K_EXT}, m0 = {M0}",
        f"  a firm opens at k = 0 iff future(m) > L + PI_0*m, i.e. m in ({lo:.3f}, {hi:.3f})",
        f"  share of firms inside that window: {inside:.2f}",
        f"  at k = 0 the modal decision is ({int(np.argmax(shares_none)) + 1}) with share {shares_none.max():.2f}"
        f" -> {STATE_NAMES[market_state(shares_none)]}",
        f"  with the motive off, at k = 0 the modal decision is "
        f"({int(np.argmax(decision_shares(a, m, 'none', 0.0, 0.0))) + 1}) with share "
        f"{decision_shares(a, m, 'none', 0.0, 0.0).max():.2f} -> "
        f"{STATE_NAMES[market_state(decision_shares(a, m, 'none', 0.0, 0.0))]}",
        "",
        "Thresholds",
        "  disclosure needs  k*E_d > L + PI_0*m - beta*phi*K*m/(m+m0)",
        f"    at m = 1, motive on:   k > {(L + PI_0 - ECOSYSTEM / (1 + M0)) / E_D:.2f}",
        f"    at m = 1, motive off:  k > (L + PI_0)/E_d = {(L + PI_0) / E_D:.2f}"
        f"   (the familiar k > L/E_d = {L / E_D:.2f} holds only if pi = 0)",
        f"  sources are modal from  k = {state3_threshold(0.0):.2f} (motive off)"
        f"  and  k = {state3_threshold(ECOSYSTEM):.2f} (motive on)",
        f"  innovation needs  k > (C_n - C_d)/(E_n - E_d) = {(C_N0 - C_D0) / (E_N - E_D):.4f}",
        f"  sources stay modal under indexed k = 4 with the motive on: share(4) = {shares_idx[3]:.2f}",
        f"  capping pays small-E and large-E releases alike, share(4) = {shares_cap[3]:.2f}",
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
    for label, t in (("all distill", 0.0), ("all train", B),
                     (f"t* = {optimal_training_share():.2f}", optimal_training_share() * B)):
        lines.append(f"    {label:14} +{social_loss(t):.2f}")
    lines += [
        "  A positive distillation share is efficient: it stops every firm from paying",
        "  to re-derive the same result. Distillation is cheap, but never free, so the",
        "  reward metric must be E.",
        "",
        "Auction account (expected over the 20000 firms; the bid is training compute, not money)",
        f"  {'reward rule':22}{'opens':>7}{'sources':>9}{'source share':>14}"
        f"{'prize spend':>13}{'spend/source':>14}{'utility':>10}{'compute/source':>16}",
    ]
    for label, rule, k in runs:
        acc = auction_account(rule, k)
        per_source = acc['bid_compute'] / acc['sources'] if acc['sources'] else float('nan')
        lines.append(
            f"  {label:22}{acc['opens']:>7.0f}{acc['sources']:>9.0f}{acc['source_share']:>14.2f}"
            f"{acc['prize']:>13.0f}{acc['spend_per_source']:>14.2f}"
            f"{acc['utility']:>10.2f}{per_source:>16.2f}")
    lines += [
        "  read as an all-pay auction: every bidder pays its own bid, so compute/source is the",
        "  rent a rule dissipates per original release, prize spend is public spending, and",
        "  source share is the share of releases that are original. Winner-take-all would hand",
        "  the prize to the highest verified E, always an original release whenever any firm",
        "  trains; our rule pays proportionally instead, so what separates the rules is the",
        "  index, not the level or the allocation form.",
    ]

    text = "\n".join(lines) + "\n"
    out = pathlib.Path(__file__).resolve().parent / "fresh_run_output.txt"
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[written to {out}]")


if __name__ == "__main__":
    main()
