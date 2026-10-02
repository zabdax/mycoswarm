#!/usr/bin/env python3
"""Myco-Swarm minimal ABM: hyphal-tip foraging for pheromone-emitting plastic sites.
Grounding: C04 growth rates, C06 field form, C08/C03 taxis kernels, C02/C04b
behaviors. ASSUMED params (soil D via lambda, chi, EC50) are swept; see
parameter_ledger.md. 2-D, homogeneous, steady-state field (all flagged).
Outputs: results/sweep.json, results/qlearn.json, results/figures/*.png
"""
import json, os, time
import numpy as np

RNG = np.random.default_rng(7)
DX = 5.0            # um per cell (ASSUMED discretization)
GRID = 60           # 300x300 um domain v0.3 (reachable; ASSUMED size)
V_TIP = 24.0        # um/min SOURCED C04 (0.4 um/s)
DT = 0.1            # min per step
T_MAX = 1200.0      # min cutoff v0.3
CAPTURE_R = 10.0    # um ASSUMED (hyphal-diameter scale, C01)
N_TIPS = 20
N_PLASTICS = 5      # ASSUMED count
P_BRANCH = 0.01     # per-step branching (mapped from C04 gamma; FLAGGED transfer)
# Bacterial passive baseline (proposal_1.md:14 "passive bacterial diffusion")
V_BACT = 1200.0     # um/min = 20 um/s run speed (standard run-tumble scale; ASSUMED)
TUMBLE_P = 0.5      # per-second tumble probability (ASSUMED)
N_BACT = 200

def make_field(sources, lam, c0=1.0):
    ys, xs = np.mgrid[0:GRID, 0:GRID]
    c = np.zeros((GRID, GRID))
    for (sx, sy) in sources:
        r = np.hypot((xs - sx) * DX, (ys - sy) * DX) + DX
        c += c0 * np.exp(-r / lam) / (r / lam)  # C06 heavy-tail-inspired steady state
    c /= c.max()
    gy, gx = np.gradient(c, DX)
    return c, gx, gy

def run_episode(sources, lam, chi, K, seed, policy=None, qtab=None, inoc="edge"):
    rng = np.random.default_rng(seed)
    c, gx, gy = make_field(sources, lam)
    pos = np.zeros((N_TIPS, 2))  # grid coords (float)
    if inoc == "network":
        # distributed mycelial network inoculation (biologically realistic)
        pos[:, 0] = rng.uniform(0, GRID, N_TIPS)
        pos[:, 1] = rng.uniform(0, GRID, N_TIPS)
    else:
        pos[:, 0] = rng.uniform(0, GRID, N_TIPS)
        pos[:, 1] = rng.uniform(GRID - 5, GRID, N_TIPS)  # edge colony
    head = rng.uniform(-np.pi, np.pi, N_TIPS)
    captured = np.zeros(len(sources), bool)
    cap_time = np.full(len(sources), np.nan)
    steps = int(T_MAX / DT)
    step_len = V_TIP * DT / DX  # grid units
    eps = 1e-9
    c, gx, gy = make_field([s for i, s in enumerate(sources) if not captured[i]] or sources, lam)
    for s in range(steps):
        t = (s + 1) * DT
        ix = np.clip(pos[:, 0].astype(int), 0, GRID - 1)
        iy = np.clip(pos[:, 1].astype(int), 0, GRID - 1)
        cc = c[iy, ix]
        gx_ = gx[iy, ix]; gy_ = gy[iy, ix]
        gmag = np.hypot(gx_, gy_)
        gain = cc / (cc + K)  # EC50-gated sensing (K swept, ASSUMED)
        gdir = np.arctan2(-gy_, gx_)  # note y-axis orientation; consistent for all policies
        if policy == "qlearn":
            cb = np.clip((cc * 4).astype(int), 0, 3)
            gb = np.clip((np.log10(gmag + 1e-12) + 6).astype(int) // 2, 0, 3)
            acts = qtab[cb, gb].argmax(axis=1)
            head = head + (acts - 1) * (np.pi / 6)
        elif chi > 0:
            w = chi * gain
            # turn toward gradient with strength w + noise (C02 ~90deg turns at boundary)
            dh = (gdir - head + np.pi) % (2 * np.pi) - np.pi
            head = head + w * dh + rng.normal(0, 0.35, pos.shape[0])
        else:
            head = head + rng.normal(0, 0.35, pos.shape[0])  # passive random walk
        pos[:, 0] += np.cos(head) * step_len
        pos[:, 1] += -np.sin(head) * step_len
        pos = np.clip(pos, 0, GRID - 1)
        # branching: add daughter heading (capped population for speed)
        if chi >= 0 and pos.shape[0] < 400 and rng.random() < P_BRANCH * (1 + chi):
            k = min(5, pos.shape[0])
            idx = rng.choice(pos.shape[0], k, replace=False)
            pos = np.vstack([pos, pos[idx]])
            head = np.concatenate([head, head[idx] + rng.normal(0, 0.5, k)])
        # capture check + source depletion: enveloped plastic stops emitting
        # (mycelial mat sequestration premise, proposal_1.md:5)
        new_capture = False
        um = pos * DX
        for i, (sx, sy) in enumerate(sources):
            if not captured[i]:
                d = np.hypot(um[:, 0] - sx * DX, um[:, 1] - sy * DX).min()
                if d < CAPTURE_R:
                    captured[i] = True
                    cap_time[i] = t
                    new_capture = True
        if new_capture:
            live = [s_ for i, s_ in enumerate(sources) if not captured[i]]
            if live:
                c, gx, gy = make_field(live, lam)
        if captured.sum() >= len(sources):
            break
    frac = captured.mean()
    # honest metrics: mean over CAPTURED sources + completeness reported separately
    n_cap = int(captured.sum())
    tall = float(cap_time[captured].mean()) if n_cap else T_MAX
    t_first = float(cap_time[captured].min()) if n_cap else T_MAX
    return frac, tall, t_first


def run_bacteria(sources, seed):
    """Passive bacterial baseline: run-tumble walkers can VISIT but never
    sequester (no envelopment mechanism — the proposal's core premise,
    proposal_1.md:3-5). Returns visits per source and sequestered fraction (0)."""
    rng = np.random.default_rng(seed)
    dt_s = 1.0  # 1-s steps
    steps = int(T_MAX * 60 / dt_s)
    step_len = V_BACT * dt_s / 60.0 / DX
    pos = rng.uniform(0, GRID, (N_BACT, 2))
    head = rng.uniform(-np.pi, np.pi, N_BACT)
    visits = np.zeros(len(sources))
    um_src = np.array(sources) * DX
    for _ in range(steps):
        tumble = rng.random(N_BACT) < TUMBLE_P
        head[tumble] = rng.uniform(-np.pi, np.pi, tumble.sum())
        pos[:, 0] = np.clip(pos[:, 0] + np.cos(head) * step_len, 0, GRID - 1)
        pos[:, 1] = np.clip(pos[:, 1] + np.sin(head) * step_len, 0, GRID - 1)
        um = pos * DX
        for i in range(len(sources)):
            if np.hypot(um[:, 0] - um_src[i, 0], um[:, 1] - um_src[i, 1]).min() < CAPTURE_R:
                visits[i] += 1
    return visits, 0.0  # sequestered fraction: bacteria cannot envelop

def main():
    os.makedirs("results/figures", exist_ok=True)
    t0 = time.time()
    LAMBDAS = [50.0, 200.0, 700.0]   # um, ASSUMED sweep (C06 agarose 735 upper anchor)
    CHIS = [0.0, 0.3, 0.6, 1.0]      # 0 = passive baseline
    KS = [0.01, 0.1, 1.0]            # normalized EC50 gate, ASSUMED
    REPS = 10
    base_sources = [(12, 12), (42, 18), (27, 33), (15, 48), (48, 45)]  # reachable in 300 um domain
    sweep = []
    for inoc in ["edge", "network"]:
        for lam in LAMBDAS:
            for chi in CHIS:
                for K in KS:
                    talls, tfirsts, fracs = [], [], []
                    for r in range(REPS):
                        f, ta, tf = run_episode(base_sources, lam, chi, K, seed=1000 + r, inoc=inoc)
                        fracs.append(f); talls.append(ta); tfirsts.append(tf)
                    sweep.append({"inoc": inoc, "lambda_um": lam, "chi": chi, "K": K,
                                  "mean_frac": float(np.mean(fracs)),
                                  "mean_tall_min": float(np.mean(talls)),
                                  "mean_tfirst_min": float(np.mean(tfirsts))})
                    print(f"inoc={inoc} lam={lam} chi={chi} K={K} frac={np.mean(fracs):.2f} "
                          f"tall={np.mean(talls):.1f} tfirst={np.mean(tfirsts):.1f}", flush=True)
    # speedup vs passive per (inoc, lam, K), on both metrics
    for row in sweep:
        base = next(x for x in sweep if x["inoc"] == row["inoc"]
                    and x["lambda_um"] == row["lambda_um"]
                    and x["K"] == row["K"] and x["chi"] == 0.0)
        row["speedup_tall"] = float(base["mean_tall_min"] / row["mean_tall_min"]) if row["mean_tall_min"] > 0 else 0.0
        row["speedup_tfirst"] = float(base["mean_tfirst_min"] / row["mean_tfirst_min"]) if row["mean_tfirst_min"] > 0 else 0.0
    # bacterial baseline (run-tumble; visits only, sequestration = 0)
    bact_visits = []
    for r in range(REPS):
        v, _seq = run_bacteria(base_sources, seed=2000 + r)
        bact_visits.append(v)
    bact_visits = np.array(bact_visits)
    json.dump({"mean_visits_per_source": [float(x) for x in bact_visits.mean(axis=0)],
               "sequestered_frac": 0.0,
               "note": "run-tumble walkers visit but cannot envelop (proposal_1.md:3-5)"},
              open("results/bacteria.json", "w"), indent=2)
    print(f"bacteria mean visits/source: {bact_visits.mean(axis=0).round(1)} sequestered=0.0", flush=True)
    json.dump(sweep, open("results/sweep.json", "w"), indent=2)

    # Q-learning proxy (tabular; DQN/C09 = protocol template only, no torch in env)
    NCB, NGB, NA = 4, 4, 3
    qtab = np.zeros((NCB, NGB, NA))
    alpha, gamma, eps = 0.15, 0.9, 0.2
    qsrc = [(30, 30)]
    lam_q, K_q = 200.0, 0.1
    cF, gxF, gyF = make_field(qsrc, lam_q)
    train_hist = []
    for ep in range(200):
        rng = np.random.default_rng(5000 + ep)
        p = np.array([[rng.uniform(0, GRID), GRID - 5.0]])
        h = rng.uniform(-np.pi, np.pi)
        prev_c = 0.0
        tot_r = 0.0
        for s in range(600):
            ix, iy = int(np.clip(p[0, 0], 0, GRID - 1)), int(np.clip(p[0, 1], 0, GRID - 1))
            cc = cF[iy, ix]; gm = float(np.hypot(gxF[iy, ix], gyF[iy, ix]))
            cb = min(3, int(cc * 4)); gb = min(3, max(0, int((np.log10(gm + 1e-12) + 6) // 2)))
            a = rng.integers(0, NA) if rng.random() < eps else qtab[cb, gb].argmax()
            h = h + (a - 1) * (np.pi / 6)
            p[0, 0] = np.clip(p[0, 0] + np.cos(h) * V_TIP * DT / DX, 0, GRID - 1)
            p[0, 1] = np.clip(p[0, 1] - np.sin(h) * V_TIP * DT / DX, 0, GRID - 1)
            r = cc - prev_c; prev_c = cc; tot_r += r
            ix2, iy2 = int(p[0, 0]), int(p[0, 1])
            cc2 = cF[iy2, ix2]; gm2 = float(np.hypot(gxF[iy2, ix2], gyF[iy2, ix2]))
            cb2 = min(3, int(cc2 * 4)); gb2 = min(3, max(0, int((np.log10(gm2 + 1e-12) + 6) // 2)))
            qtab[cb, gb, a] += alpha * (r + gamma * qtab[cb2, gb2].max() - qtab[cb, gb, a])
        train_hist.append(tot_r)
    # test: single tip capture time, greedy(chi=1) vs qlearn vs random
    def single(policy, seed):
        rng = np.random.default_rng(seed)
        p = np.array([5.0, 55.0]); h = -np.pi / 2
        for s in range(3000):
            ix, iy = int(np.clip(p[0], 0, GRID - 1)), int(np.clip(p[1], 0, GRID - 1))
            cc = cF[iy, ix]
            if policy == "qlearn":
                cb = min(3, int(cc * 4))
                gm = float(np.hypot(gxF[iy, ix], gyF[iy, ix]))
                gb = min(3, max(0, int((np.log10(gm + 1e-12) + 6) // 2)))
                h = h + (int(qtab[cb, gb].argmax()) - 1) * (np.pi / 6)
            elif policy == "greedy":
                gdir = np.arctan2(-gyF[iy, ix], gxF[iy, ix])
                dh = (gdir - h + np.pi) % (2 * np.pi) - np.pi
                h = h + 0.8 * dh * (cc / (cc + K_q)) + rng.normal(0, 0.2)
            else:
                h = h + rng.normal(0, 0.35)
            p[0] = np.clip(p[0] + np.cos(h) * V_TIP * DT / DX, 0, GRID - 1)
            p[1] = np.clip(p[1] - np.sin(h) * V_TIP * DT / DX, 0, GRID - 1)
            if np.hypot(p[0] * DX - 30 * DX, p[1] * DX - 30 * DX) < CAPTURE_R:
                return (s + 1) * DT
        return T_MAX
    comp = {pol: [single(pol, 9000 + i) for i in range(10)] for pol in ["random", "greedy", "qlearn"]}
    qres = {"train_final_mean_reward": float(np.mean(train_hist[-20:])),
            "test_capture_min": {k: float(np.mean(v)) for k, v in comp.items()}}
    json.dump(qres, open("results/qlearn.json", "w"), indent=2)

    # figures
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharey=True)
    for r, inoc in enumerate(["edge", "network"]):
        for ax, lam in zip(axes[r], LAMBDAS):
            sub = [x for x in sweep if x["inoc"] == inoc and x["lambda_um"] == lam and x["K"] == 0.1]
            ax.plot([x["chi"] for x in sub], [x["speedup_tfirst"] for x in sub], "o-", label="first capture")
            ax.plot([x["chi"] for x in sub], [x["speedup_tall"] for x in sub], "s--", label="all-source mean")
            ax.axhline(1, color="k", ls="--", lw=0.8)
            ax.axhspan(10, 50, color="green", alpha=0.1)
            ax.set_title(f"{inoc}: lambda={lam} um, K=0.1")
            ax.set_xlabel("chi (0=passive)")
    axes[0][0].set_ylabel("speedup vs passive")
    axes[1][0].set_ylabel("speedup vs passive")
    axes[0][2].legend(fontsize=8)
    fig.suptitle("Myco-Swarm ABM: speedup vs passive (green band = 10-50x target)")
    fig.tight_layout(); fig.savefig("results/figures/speedup.png", dpi=100)
    plt.figure(figsize=(6, 4))
    plt.plot(train_hist); plt.xlabel("episode"); plt.ylabel("total Δc reward")
    plt.title("Tabular Q-learning training (proxy; C09 DQN = template only)")
    plt.tight_layout(); plt.savefig("results/figures/qlearn.png", dpi=100)
    print(f"DONE in {time.time()-t0:.1f}s. Q-learn test means: {qres['test_capture_min']}", flush=True)

if __name__ == "__main__":
    main()
