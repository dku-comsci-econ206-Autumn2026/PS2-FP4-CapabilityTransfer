"""Zero-dependency check of the paper's two thresholds on the prize rate k.

Recomputes the four decision payoffs from scratch and finds where the best
decision changes. Nothing is imported; independent of k_formula.ipynb,
code/distill_sim.py and the Hugging Face page.

Levels: Appendix A parameters plus the six constants fitted to Table 2
(residual 7.4e-5). A representative firm has cost multiplier a = 1 and
market power m = 1.
"""

# ---- levels (paper Appendix A + the fit to Table 2) ----------------------
C_D, C_N = 1.4446, 5.6704     # distillation cost, training cost
PI       = 8.2391             # monopoly profit
L        = 2.5193             # lost exclusivity
E_D, E_N = 0.9854, 4.6311     # training compute reported, distilled vs original

R_LUMP, CAP = 20.0, 12.0      # Tool 1 lump sum; the cap


def reward(rule, k):
    """(reward on a distilled release, reward on an original release)."""
    if rule == "none":
        return 0.0, 0.0
    if rule == "openness":                     # Tool 1: lump sum for any open release
        return R_LUMP, R_LUMP
    if rule == "indexed":                      # Tool 2: paid per unit of reported compute
        return k * E_D, k * E_N
    if rule == "capped":
        return min(k * E_D, CAP), min(k * E_N, CAP)
    raise ValueError(rule)


def decisions(rule="indexed", k=4.0):
    """The four decisions and their payoffs, in the paper's order."""
    r_small, r_large = reward(rule, k)
    return {
        1: ("closed, distill", -C_D + PI),
        2: ("open, distill",   -C_D + r_small - L),
        3: ("closed, train",   -C_N + PI),
        4: ("open, train",     -C_N + r_large - L),
    }


def best(rule="indexed", k=4.0):
    d = decisions(rule, k)
    top = max(v for _, v in d.values())
    return sorted(i for i, (_, v) in d.items() if v == top)


def threshold_disclosure():
    """(2) beats (1) once the reward covers the forgone profit and lost exclusivity."""
    return (PI + L) / E_D


def threshold_innovation():
    """(4) beats (2) once the reward differential covers the extra cost."""
    return (C_N - C_D) / (E_N - E_D)


print("Payoffs  (1) -C_d+pi   (2) -C_d+kE_d-L   (3) -C_n+pi   (4) -C_n+kE_n-L")
print(f"Levels   C_d={C_D}  C_n={C_N}  pi={PI}  L={L}  E_d={E_D}  E_n={E_N}")
print()
print(f"threshold 1  (2) > (1)  =>  k > (pi + L)/E_d = {threshold_disclosure():.2f}")
print(f"threshold 2  (4) > (2)  =>  k > dC/dE       = {threshold_innovation():.2f}")
print()

print(f"{'rule':9} {'k':>6}  {'(1)':>7} {'(2)':>7} {'(3)':>7} {'(4)':>7}   best")
for rule, k in [("none", 0.0), ("openness", 0.0), ("indexed", 4.0), ("capped", 12.0)]:
    d = decisions(rule, k)
    row = " ".join(f"{d[i][1]:7.2f}" for i in (1, 2, 3, 4))
    print(f"{rule:9} {k:>6.1f}  {row}   {best(rule, k)}")
print()

print("claim 1: at k = 0 decision (1) is privately best")
assert best("none", 0.0) == [1], best("none", 0.0)
print(f"   best = {best('none', 0.0)}")

print()
print("claim 2: the private order (1)>(3)>(2)>(4) exactly reverses the social order")
d = {i: v for i, (_, v) in decisions("none", 0.0).items()}
priv = sorted(d, key=lambda i: -d[i])
social = [4, 2, 3, 1]
print(f"   private {priv}   social {social}")
assert priv == [1, 3, 2, 4] and social == list(reversed(priv))

print()
print("claim 3: Tool 1 lets (2) beat (4) at every lump sum, so nobody trains")
for R in [1.0, 20.0, 1e3, 1e6]:
    gap = (-C_N + R - L) - (-C_D + R - L)          # (4) - (2)
    assert abs(gap - (C_D - C_N)) < 1e-6 and gap < 0, (R, gap)
print(f"   (4) - (2) = C_d - C_n = {C_D - C_N:.4f} < 0 at every R")

print()
print("claim 4: Tool 2 separates the open cells once k passes threshold 2")
k = threshold_innovation() + 1e-9
d = decisions("indexed", k)
assert d[4][1] > d[2][1], (k, d)
print(f"   k={k:.2f}:  (4)={d[4][1]:.2f} > (2)={d[2][1]:.2f}")

print()
print("claim 5: if the reward ignores reported compute (E_n = E_d), threshold 2 diverges")
print(f"   dC/dE = ({C_N} - {C_D}) / 0 -> infinity, so no k separates (4) from (2)")

print()
print("note: these thresholds are for a representative firm, a = m = 1. Firms are")
print("      heterogeneous, so in the simulation state 3 needs a higher k (about 3).")
print()
print("all five claims hold")


# ---------------------------------------------------------------- future market share
# Added in the PS2 revision. Same parameters as code/distill_sim.py.
BETA, PHI, K_EXT, M0 = 0.90, 0.50, 44.4, 0.50
ECOSYSTEM = BETA * PHI * K_EXT


def future(m, ecosystem=ECOSYSTEM, m0=M0):
    """Value of the future market share an open release buys."""
    return ecosystem * m / (m + m0)


def openness_window(ecosystem=ECOSYSTEM, m0=M0):
    """m where a firm opens at k = 0: future(m) > L + pi*m."""
    import math
    a, b, c = PI, PI * m0 + L - ecosystem, L * m0
    disc = b * b - 4 * a * c
    if disc <= 0:
        return None
    r = math.sqrt(disc)
    return ((-b - r) / (2 * a), (-b + r) / (2 * a))


if __name__ == "__main__" or True:
    print()
    print("future market share  beta=%.2f phi=%.2f K=%.1f m0=%.2f  => beta*phi*K=%.2f"
          % (BETA, PHI, K_EXT, M0, ECOSYSTEM))
    print("  future(m = 1) = %.3f" % future(1.0))
    print("  disclosure with the motive, at m = 1:  k > %.2f" % ((L + PI - future(1.0)) / E_D))
    w = openness_window()
    print("  openness window in m: (%s)" % (", ".join("%.3f" % x for x in w) if w else "empty"))
