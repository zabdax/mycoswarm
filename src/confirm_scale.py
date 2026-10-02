#!/usr/bin/env python3
"""Scale test: 400 um domain (GRID=80 via module patch, same physics).
inoc {edge, network}, lam=200, K=0.1, chi {0,1}, 8 reps.
Writes results_pub/scale80.json. Coarser relative resolution flagged."""
import json, time
import numpy as np
import mycoswarm_abm_3d as sim

sim.GRID = 80  # 400 um cube; all model code reads GRID/DX dynamically
SOURCES = [(20, 20, 20), (62, 25, 60), (40, 58, 30), (64, 62, 62)]
out = []
t0 = time.time()
for inoc in ["edge", "network"]:
    for chi in [0.0, 1.0]:
        talls, fracs = [], []
        for r in range(8):
            f, (ta, tf) = sim.run_episode(SOURCES, 200.0, chi, 0.1,
                                          seed=31000 + r, inoc=inoc)
            talls.append(ta)
            fracs.append(f)
        row = {"inoc": inoc, "chi": chi, "mean_tall": float(np.mean(talls)),
               "mean_frac": float(np.mean(fracs))}
        out.append(row)
        print(f"{inoc} chi={chi}: tall={np.mean(talls):.1f} frac={np.mean(fracs):.2f}", flush=True)
    base = next(x for x in out if x["inoc"] == inoc and x["chi"] == 0.0)["mean_tall"]
    for row in [x for x in out if x["inoc"] == inoc and x["chi"] > 0]:
        row["speedup"] = float(base / row["mean_tall"])
json.dump(out, open("results_pub/scale80.json", "w"), indent=2)
print(f"DONE in {time.time()-t0:.1f}s", flush=True)
