#!/usr/bin/env python3
"""Confirm: analytic field vs grain-aware FD-solver field in the ABM loop.
Focused: inoc {edge, network}, lam=200, K=0.1, chi {0,1}, 8 reps.
Writes results_pub/grainfield.json."""
import json, time
import numpy as np
import mycoswarm_abm_3d as sim

SOURCES = [(10, 10, 10), (30, 12, 28), (20, 30, 15), (32, 30, 32)]
out = []
t0 = time.time()
for inoc in ["edge", "network"]:
    for field in ["analytic", "solver"]:
        for chi in [0.0, 1.0]:
            talls = []
            for r in range(8):
                f, (ta, tf) = sim.run_episode(SOURCES, 200.0, chi, 0.1,
                                              seed=30000 + r, inoc=inoc, field=field)
                talls.append(ta)
            row = {"inoc": inoc, "field": field, "chi": chi,
                   "mean_tall": float(np.mean(talls)), "frac": 1.0}
            out.append(row)
            print(f"{inoc} {field} chi={chi}: tall={np.mean(talls):.1f}", flush=True)
json.dump(out, open("results_pub/grainfield.json", "w"), indent=2)
print(f"DONE in {time.time()-t0:.1f}s", flush=True)
