#!/usr/bin/env python3
"""Myco-Swarm ABM v1: 3-D heterogeneous soil cube with obstacles + bacterial washout.
v0 deltas: 3-D domain, 15% blocked grain cells, advective drift + removal for
bacteria (unattached) while hyphal tips persist (attached network).
Field: analytic 3-D steady state c=sum exp(-r/lam)/(r/lam), obstacles ignored
in field (FLAGGED simplification). Tips: 3-D unit-vector headings, EC50-gated
chemotactic turn, branching (cap 200). Sources deplete on capture (v0 fix kept).
Outputs: results_3d/sweep3d.json, bacteria3d.json, figures/speedup3d.png
"""
import json, os, time
import numpy as np

DX = 5.0
GRID = 40            # 200 um cube (ASSUMED; smaller for 3-D speed)
V_TIP = 24.0         # um/min SOURCED C04
DT = 0.1
T_MAX = 1200.0
CAPTURE_R = 10.0     # um ASSUMED
N_TIPS = 20
N_SRC = 4
P_BRANCH = 0.01      # FLAGGED transfer from C04
OBSTACLE_FRac = 0.15  # ASSUMED grain fraction
V_BACT = 1200.0      # um/min ASSUMED
TUMBLE_P = 0.5       # ASSUMED
N_BACT = 200
WASH_P = 0.002       # per-second removal prob (ASSUMED washout)
ADVECT = np.array([30.0, 0.0, 0.0])  # um/min drift (ASSUMED pore flow)

def build_obstacles(seed, frac=0.15):
    rng = np.random.default_rng(seed)
    return rng.random((GRID, GRID, GRID)) < frac

def make_field(sources, lam):
    z, y, x = np.mgrid[0:GRID, 0:GRID, 0:GRID]
    c = np.zeros((GRID, GRID, GRID))
    for (sx, sy, sz) in sources:
        r = np.sqrt(((x - sx) * DX) ** 2 + ((y - sy) * DX) ** 2 + ((z - sz) * DX) ** 2) + DX
        c += np.exp(-r / lam) / (r / lam)
    c /= c.max()
    gz, gy, gx = np.gradient(c, DX)
    return c, gx, gy, gz

def run_episode(sources, lam, chi, K, seed, inoc="network", ablate="none", dt=0.1, grain=0.15,
                field="analytic"):
    rng = np.random.default_rng(seed)
    obst = build_obstacles(seed, frac=grain)

    def get_field(srcs):
        if field == "solver":
            import transport
            # beacons emit: source cells are always free for the field solve
            o2 = obst.copy()
            for (sx, sy, sz) in srcs:
                o2[int(sz), int(sy), int(sx)] = False
            return transport.solve_field(srcs, lam, GRID, DX, o2)
        return make_field(srcs, lam)

    c, gx, gy, gz = get_field(sources)
    pos = rng.uniform(0, GRID, (N_TIPS, 3)) if inoc == "network" else \
        np.column_stack([rng.uniform(0, GRID, N_TIPS), rng.uniform(0, GRID, N_TIPS),
                         rng.uniform(GRID - 3, GRID, N_TIPS)])
    vec = rng.normal(0, 1, pos.shape)
    vec /= np.linalg.norm(vec, axis=1, keepdims=True)
    captured = np.zeros(len(sources), bool)
    cap_time = np.full(len(sources), np.nan)
    steps = int(T_MAX / dt)
    step_len = V_TIP * dt / DX
    ns = 0.2 * (dt / 0.1) ** 0.5  # SDE-correct noise scaling: variance ∝ time
    for s in range(steps):
        t = (s + 1) * dt
        ix = np.clip(pos[:, 0].astype(int), 0, GRID - 1)
        iy = np.clip(pos[:, 1].astype(int), 0, GRID - 1)
        iz = np.clip(pos[:, 2].astype(int), 0, GRID - 1)
        cc = c[iz, iy, ix]
        g = np.column_stack([gx[iz, iy, ix], gy[iz, iy, ix], gz[iz, iy, ix]])
        gn = np.linalg.norm(g, axis=1, keepdims=True) + 1e-12
        gain = (cc / (cc + K))[:, None]
        if chi > 0:
            w = chi * gain
            vec = (1 - w) * vec + w * (g / gn) + rng.normal(0, ns, vec.shape)
        else:
            vec = vec + rng.normal(0, ns, vec.shape)
        vec /= np.linalg.norm(vec, axis=1, keepdims=True)
        trial = np.clip(pos + vec * step_len, 0, GRID - 1)
        tix = np.clip(trial.astype(int), 0, GRID - 1)
        blocked = obst[tix[:, 2], tix[:, 1], tix[:, 0]]
        pos = np.where(blocked[:, None], pos, trial)  # grains stop tips (C01 confinement)
        if pos.shape[0] < 200 and ablate != "nobranch" and rng.random() < P_BRANCH * (1 + chi):
            k = min(5, pos.shape[0])
            idx = rng.choice(pos.shape[0], k, replace=False)
            pos = np.vstack([pos, pos[idx]])
            vec = np.vstack([vec, vec[idx] + rng.normal(0, 0.3, (k, 3))])
            vec /= np.linalg.norm(vec, axis=1, keepdims=True)
        new_cap = False
        um = pos * DX
        for i, (sx, sy, sz) in enumerate(sources):
            if not captured[i]:
                d = np.sqrt(((um[:, 0] - sx * DX)) ** 2 + ((um[:, 1] - sy * DX)) ** 2
                            + ((um[:, 2] - sz * DX)) ** 2).min()
                if d < CAPTURE_R:
                    captured[i] = True
                    cap_time[i] = t
                    new_cap = True
        if new_cap and ablate != "nodeplete":
            live = [sq for i, sq in enumerate(sources) if not captured[i]]
            if live:
                c, gx, gy, gz = get_field(live)
        if captured.all():
            break
    frac = captured.mean()
    n = int(captured.sum())
    return frac, (float(cap_time[captured].mean()) if n else T_MAX,
                  float(cap_time[captured].min()) if n else T_MAX)

def run_bacteria(sources, seed):
    rng = np.random.default_rng(seed)
    dt_s, steps = 1.0, int(T_MAX * 60)
    step_len = V_BACT * dt_s / 60.0 / DX
    adv = ADVECT * dt_s / 60.0 / DX
    pos = rng.uniform(0, GRID, (N_BACT, 3))
    vec = rng.normal(0, 1, pos.shape)
    vec /= np.linalg.norm(vec, axis=1, keepdims=True)
    alive = np.ones(N_BACT, bool)
    visits = np.zeros(len(sources))
    um_src = np.array(sources) * DX
    for _ in range(steps):
        if not alive.any():
            break
        tumble = rng.random(N_BACT) < TUMBLE_P
        vec[tumble] = rng.normal(0, 1, (tumble.sum(), 3))
        vec /= np.linalg.norm(vec, axis=1, keepdims=True)
        pos[alive] = np.clip(pos[alive] + vec[alive] * step_len + adv, 0, GRID - 1)
        alive[alive] = rng.random(alive.sum()) > WASH_P  # washout removal
        um = pos[alive] * DX
        if len(um):
            for i in range(len(sources)):
                if np.sqrt(((um - um_src[i]) ** 2).sum(axis=1)).min() < CAPTURE_R:
                    visits[i] += 1
    return visits, 0.0, float(alive.mean())  # visits, sequestered, retention

def main(seed_base=1000, outdir="results_3d"):
    os.makedirs(f"{outdir}/figures", exist_ok=True)
    t0 = time.time()
    LAMBDAS = [100.0, 300.0]
    CHIS = [0.0, 0.6, 1.0]
    KS = [0.01, 0.1]
    REPS = 8
    sources = [(10, 10, 10), (30, 12, 28), (20, 30, 15), (32, 30, 32)]
    sweep = []
    for inoc in ["edge", "network"]:
        for lam in LAMBDAS:
            for chi in CHIS:
                for K in KS:
                    talls, tfirsts, fracs = [], [], []
                    for r in range(REPS):
                        f, (ta, tf) = run_episode(sources, lam, chi, K, seed=seed_base + r, inoc=inoc)
                        fracs.append(f); talls.append(ta); tfirsts.append(tf)
                    sweep.append({"inoc": inoc, "lambda_um": lam, "chi": chi, "K": K,
                                  "mean_frac": float(np.mean(fracs)),
                                  "mean_tall_min": float(np.mean(talls)),
                                  "mean_tfirst_min": float(np.mean(tfirsts)),
                                  "tall_reps": [float(x) for x in talls],
                                  "tfirst_reps": [float(x) for x in tfirsts]})
                    print(f"inoc={inoc} lam={lam} chi={chi} K={K} frac={np.mean(fracs):.2f} "
                          f"tall={np.mean(talls):.1f} tfirst={np.mean(tfirsts):.1f}", flush=True)
    for row in sweep:
        base = next(x for x in sweep if x["inoc"] == row["inoc"] and x["lambda_um"] == row["lambda_um"]
                    and x["K"] == row["K"] and x["chi"] == 0.0)
        row["speedup_tall"] = float(base["mean_tall_min"] / row["mean_tall_min"])
        row["speedup_tfirst"] = float(base["mean_tfirst_min"] / row["mean_tfirst_min"])
    bv = []
    for r in range(REPS):
        v, _s, ret = run_bacteria(sources, seed=seed_base + 1000 + r)
        bv.append((v, ret))
    json.dump({"mean_visits": [float(x) for x in np.array([b[0] for b in bv]).mean(axis=0)],
               "sequestered_frac": 0.0, "mean_retention": float(np.mean([b[1] for b in bv]))},
              open(f"{outdir}/bacteria3d.json", "w"), indent=2)
    json.dump(sweep, open(f"{outdir}/sweep3d.json", "w"), indent=2)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharey=True)
    for r, inoc in enumerate(["edge", "network"]):
        for ax, lam in zip(axes[r], LAMBDAS):
            for K, mk in [(0.01, "o-"), (0.1, "s--")]:
                sub = [x for x in sweep if x["inoc"] == inoc and x["lambda_um"] == lam and x["K"] == K]
                ax.plot([x["chi"] for x in sub], [x["speedup_tall"] for x in sub], mk, label=f"K={K}")
            ax.axhline(1, color="k", ls=":", lw=0.8)
            ax.axhspan(10, 50, color="green", alpha=0.1)
            ax.set_title(f"3-D {inoc}: lambda={lam} um")
            ax.set_xlabel("chi (0=passive)")
    axes[0][0].set_ylabel("speedup vs passive")
    axes[1][0].set_ylabel("speedup vs passive")
    axes[0][1].legend(fontsize=8)
    fig.suptitle("Myco-Swarm ABM v1 (3-D + grains + washout): speedup vs passive")
    fig.tight_layout(); fig.savefig(f"{outdir}/figures/speedup3d.png", dpi=100)
    print(f"DONE in {time.time()-t0:.1f}s", flush=True)

if __name__ == "__main__":
    import sys
    _sb = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    _od = sys.argv[2] if len(sys.argv) > 2 else "results_3d"
    main(seed_base=_sb, outdir=_od)
