"""Zero-dependency check of the k formula.

Recomputes the four cells from scratch and finds where the best cell changes.
Nothing is imported; this is independent of k_formula.ipynb and of model.js.

Units: E_d = 1, C_d = 0  (so C_n = dC and E_n = 1 + dE)
"""

# ---- the four cells, written out directly -------------------------------
def cells(k, L, dC, dE):
    En = 1 + dE
    return {
        "imitate/secrecy":    0.0,
        "imitate/openness":   k * 1 - L,
        "innovate/secrecy":  -dC,
        "innovate/openness": -dC + k * En - L,
    }


def best(k, L, dC, dE):
    c = cells(k, L, dC, dE)
    top = max(c.values())
    return sorted([n for n, v in c.items() if v == top])


def state(k, L, dC, dE):
    if k <= L:
        return "secrecy"
    if k <= dC / dE:
        return "imitation"
    return "healthy"


# ---- pick any numbers you like ------------------------------------------
L, dC, dE = 1.0, 2.0, 1.0

b1 = L            # openness vs secrecy
b2 = dC / dE      # innovate vs imitate
print(f"L={L}  dC={dC}  dE={dE}")
print(f"threshold 1 (k > L)        = {b1}")
print(f"threshold 2 (k > dC/dE)    = {b2}")
print(f"lower bound = max(...)     = {max(b1, b2)}")
print()

# scan across the bound and watch the winning cell flip
print(f"{'k':>6}  {'best cell':<20} {'state':<10}  cells")
for k in [0.5, 1.0, 1.5, 1.9, 2.0, 2.1, 3.0]:
    c = cells(k, L, dC, dE)
    shown = "  ".join(f"{n.split('/')[0][:4]}/{n.split('/')[1][:4]}={v:+.2f}" for n, v in c.items())
    print(f"{k:>6}  {','.join(best(k,L,dC,dE)):<20} {state(k,L,dC,dE):<10}  {shown}")

print()
# ---- the three claims worth checking ------------------------------------
print("claim 1: the flip from imitation to healthy happens exactly at k = dC/dE")
for k in [b2 - 1e-9, b2 + 1e-9]:
    print(f"   k={k:.6f} -> {state(k, L, dC, dE)}")
assert state(b2 - 1e-9, L, dC, dE) == "imitation"
assert state(b2 + 1e-9, L, dC, dE) == "healthy"

print()
print("claim 2: if the prize is flat (dE = 0), innovate can never win")
for k in [1e3, 1e6, 1e9]:
    c = cells(k, L, dC, dE=0.0)
    print(f"   k={k:>10.0f} -> best {best(k, L, dC, 0.0)}")
    assert "innovate/openness" not in best(k, L, dC, 0.0)

print()
print("claim 3: with dE > 0, a large enough k always makes innovate win")
k_big = (dC - 0 + L) / dE + 10          # comfortably past both bounds
assert "innovate/openness" in best(k_big, L, dC, dE)
print(f"   k={k_big:.1f} -> best {best(k_big, L, dC, dE)}")

print()
print("all three claims hold")
