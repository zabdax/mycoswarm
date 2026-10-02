#!/usr/bin/env python3
"""Strength upgrades: (1) measured Deff in v1 grain matrices (replaces part of
the assumed block with computed physics); (2) Morris screening of assumed
parameters (lam, chi, K, grain) on capture time + speedup.
Writes results_pub/{deff.json, morris.json} + figures/morris.png.
"""
import json, os, time
import numpy as np
import mycoswarm_abm_3d as sim
from transport import measure_deff

OUT = "results_pub"
t0 = time.time()
SOURCES = [(10, 10, 10), (30, 12, 28), (20, 30, 15), (32, 30, 32)]

# ---- 1. Deff over v1-like grain matrices ----
recs = []
for sd in [1000, 2000, 3000, 4000, 5000]:
    obst = sim.build_obstacles(sd, frac=0.15)
    deff, d0 = measure_deff(obst, dx=5.0, d0=500.0, n_walkers=1500, steps=1500, seed=sd)
    recs.append(deff / d0)
    print(f"matrix {sd}: tortuosity Deff/D0 = {deff/d0:.3f}", flush=True)
deff = {"frac": 0.15, "Deff_D0_mean": float(np.mean(recs)),
        "Deff_D0_sd": float(np.std(recs)), "seeds": [1000, 2000, 3000, 4000, 5000]}
json.dump(deff, open(f"{OUT}/deff.json", "w"), indent=2)

# ---- 2. Morris screening (r=8 trajectories, p=4 levels, k=4 params) ----
bounds = {"lam": (50.0, 700.0), "chi": (0.0, 1.0), "K": (0.01, 1.0), "grain": (0.0, 0.30)}
keys = ["lam", "chi", "K", "grain"]
p, r, REPS = 4, 8, 6
delta = p / (2 * (p - 1))
rng = np.random.default_rng(77)

def evaluate(pt, rep0):
    vals = []
    for rr in range(REPS):
        f, (ta, tf) = sim.run_episode(SOURCES, pt["lam"], pt["chi"], pt["K"],
                                      seed=rep0 + rr, inoc="network",
                                      grain=pt["grain"])
        vals.append(ta)
    return float(np.mean(vals))

def scale(u):
    return {k: bounds[k][0] + u[i] * (bounds[k][1] - bounds[k][0]) for i, k in enumerate(keys)}

EE = {k: [] for k in keys}
for t in range(r):
    base = rng.integers(0, p - 1, size=len(keys)) / (p - 1)  # stay clear of top edge
    order = rng.permutation(len(keys))
    cur = base.copy()
    y_prev = evaluate(scale(cur), rep0=20000 + t * 100)
    step_taken = np.zeros(len(keys), bool)
    for j in order:
        lo, hi = bounds[keys[j]]
        nxt = cur.copy()
        nxt[j] = min(1.0, cur[j] + delta)
        step = (nxt[j] - cur[j]) * (hi - lo)
        y_new = evaluate(scale(nxt), rep0=20000 + t * 100)
        EE[keys[j]].append((y_new - y_prev) / step if step > 0 else 0.0)
        cur, y_prev = nxt, y_new
    print(f"trajectory {t + 1}/{r} done", flush=True)

morris = {k: {"mu_star": float(np.mean(np.abs(v))), "sigma": float(np.std(v)),
              "mean": float(np.mean(v))} for k, v in EE.items()}
json.dump(morris, open(f"{OUT}/morris.json", "w"), indent=2)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4.5))
for k in keys:
    ax.scatter(morris[k]["mu_star"], morris[k]["sigma"], s=90, label=k)
    ax.annotate(k, (morris[k]["mu_star"], morris[k]["sigma"]), fontsize=10,
                xytext=(6, 6), textcoords="offset points", weight="bold")
ax.set_xlabel("mu* (overall influence on capture time)")
ax.set_ylabel("sigma (nonlinearity / interactions)")
ax.set_title("Morris screening: which assumed parameter matters most")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{OUT}/figures/morris.png", dpi=100)
print(f"DONE in {time.time()-t0:.1f}s", flush=True)
print("Morris ranking:", sorted(morris, key=lambda k: -morris[k]["mu_star"]))
