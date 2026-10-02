#!/usr/bin/env python3
"""Publication-grade analysis: per-rep sweep + ablation + time-step convergence
+ inferential stats (Mann-Whitney U, Cliff's delta, bootstrap speedup CI, Holm).
Writes results_pub/{sweep_pub.json,ablation.json,convergence.json,stats.json}
+ figures/ci_speedup.png. Imports the model (no code duplication).
"""
import json, os, time
import numpy as np
from scipy import stats as sstats
import mycoswarm_abm_3d as sim

OUT = "results_pub"
os.makedirs(f"{OUT}/figures", exist_ok=True)
t0 = time.time()
REPS = 12
SOURCES = [(10, 10, 10), (30, 12, 28), (20, 30, 15), (32, 30, 32)]

def run_many(sources, lam, chi, K, seeds, inoc="network", ablate="none", dt=0.1):
    talls, tfirsts, fracs = [], [], []
    for sd in seeds:
        f, (ta, tf) = sim.run_episode(sources, lam, chi, K, seed=sd, inoc=inoc,
                                      ablate=ablate, dt=dt)
        fracs.append(f); talls.append(ta); tfirsts.append(tf)
    return {"frac": fracs, "tall": talls, "tfirst": tfirsts}

def cliffs_delta(a, b):
    a, b = np.asarray(a), np.asarray(b)
    wins = sum(1 for x in a for y in b if x > y) + 0.5 * sum(1 for x in a for y in b if x == y)
    return (2 * wins) / (len(a) * len(b)) - 1  # positive => a tends larger

def boot_speedup_ci(pass_reps, eng_reps, n_boot=5000, seed=42):
    rng = np.random.default_rng(seed)
    p, e = np.asarray(pass_reps), np.asarray(eng_reps)
    boots = [rng.choice(p, len(p), replace=True).mean() / rng.choice(e, len(e), replace=True).mean()
             for _ in range(n_boot)]
    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))

# ---- 1. primary sweep with per-rep storage (reproduces results_3d, new seeds) ----
sweep = []
for inoc in ["edge", "network"]:
    for lam in [100.0, 300.0]:
        for chi in [0.0, 0.6, 1.0]:
            for K in [0.01, 0.1]:
                r = run_many(SOURCES, lam, chi, K, seeds=list(range(11000, 11000 + REPS)), inoc=inoc)
                sweep.append({"inoc": inoc, "lambda_um": lam, "chi": chi, "K": K,
                              "mean_frac": float(np.mean(r["frac"])),
                              "mean_tall_min": float(np.mean(r["tall"])),
                              "tall_reps": [float(x) for x in r["tall"]],
                              "tfirst_reps": [float(x) for x in r["tfirst"]]})
                print(f"sweep {inoc} lam={lam} chi={chi} K={K} tall={np.mean(r['tall']):.1f}", flush=True)
json.dump(sweep, open(f"{OUT}/sweep_pub.json", "w"), indent=2)

# ---- 2. ablation (network, lam=200, K=0.1) ----
abl = {}
for chi in [0.0, 1.0]:
    for ab in ["none", "nobranch", "nodeplete"]:
        abl[f"chi{chi}_{ab}"] = run_many(SOURCES, 200.0, chi, 0.1,
                                         seeds=list(range(12000, 12000 + REPS)),
                                         inoc="network", ablate=ab)
        m = np.mean(abl[f"chi{chi}_{ab}"]["tall"])
        print(f"ablation chi={chi} {ab}: tall={m:.1f}", flush=True)
json.dump({k: {"mean_tall": float(np.mean(v["tall"])),
               "tall_reps": [float(x) for x in v["tall"]]} for k, v in abl.items()},
          open(f"{OUT}/ablation.json", "w"), indent=2)

# ---- 3. time-step convergence (network, lam=200, chi=1, K=0.1) ----
conv = {}
for dt in [0.1, 0.05]:
    conv[f"dt{dt}"] = run_many(SOURCES, 200.0, 1.0, 0.1,
                               seeds=list(range(13000, 13000 + REPS)),
                               inoc="network", dt=dt)
    print(f"convergence dt={dt}: tall={np.mean(conv[f'dt{dt}']['tall']):.2f}", flush=True)
json.dump({k: {"mean_tall": float(np.mean(v["tall"])),
               "tall_reps": [float(x) for x in v["tall"]]} for k, v in conv.items()},
          open(f"{OUT}/convergence.json", "w"), indent=2)

# ---- 4. inferential stats ----
tests = []
pvals = []
def add_test(name, a_pass, a_eng):
    u, p = sstats.mannwhitneyu(a_eng, a_pass, alternative="two-sided")
    d = cliffs_delta(np.asarray(a_eng), np.asarray(a_pass))  # negative => eng faster
    lo, hi = boot_speedup_ci(a_pass, a_eng)
    tests.append({"contrast": name, "U": float(u), "p_raw": float(p),
                  "cliffs_delta": float(d),
                  "speedup_boot_ci95": [lo, hi],
                  "n_per_group": len(a_pass)})
    pvals.append(p)

_lookup = {(x["inoc"], x["lambda_um"], x["K"]): x for x in sweep if x["chi"] == 0.0}
for (inoc, lam, K), base in _lookup.items():
    for chi in [0.6, 1.0]:
        eng = next(x for x in sweep if x["inoc"] == inoc and x["lambda_um"] == lam
                   and x["K"] == K and x["chi"] == chi)
        add_test(f"{inoc}/lam{lam}/K{K}/chi{chi}-vs-passive",
                 base["tall_reps"], eng["tall_reps"])
# convergence check: dt=0.1 vs dt=0.05 (same seeds) — non-significance required,
# else the scheme is dt-sensitive (reported as limitation either way)
_t01 = np.asarray(conv["dt0.1"]["tall"])
_t005 = np.asarray(conv["dt0.05"]["tall"])
u_c, p_c = sstats.mannwhitneyu(_t005, _t01, alternative="two-sided")
conv_test = {"contrast": "convergence dt0.05-vs-dt0.1", "U": float(u_c), "p_raw": float(p_c),
             "mean_dt01": float(_t01.mean()),
             "mean_dt005": float(_t005.mean()),
             "n_per_group": REPS}
json.dump(conv_test, open(f"{OUT}/convergence_test.json", "w"), indent=2)
print(f"convergence: dt0.1={conv_test['mean_dt01']:.2f} dt0.05={conv_test['mean_dt005']:.2f} p={p_c:.3f}", flush=True)
# Holm correction over the family
order = np.argsort(pvals)
m = len(pvals)
holm = [None] * m
for rank, idx in enumerate(order):
    holm[idx] = min(1.0, pvals[idx] * (m - rank))
for t, h in zip(tests, holm):
    t["p_holm"] = float(h)
json.dump(tests, open(f"{OUT}/stats.json", "w"), indent=2)
print(f"DONE in {time.time()-t0:.1f}s; {sum(1 for t in tests if t['p_holm']<0.05)}/{len(tests)} Holm-significant", flush=True)

# ---- 5. CI figure ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 4.5))
xs, ys, lo, hi, lbl = [], [], [], [], []
for i, t in enumerate(tests):
    xs.append(i)
    md = (t["speedup_boot_ci95"][0] + t["speedup_boot_ci95"][1]) / 2
    ys.append(md); lo.append(md - t["speedup_boot_ci95"][0]); hi.append(t["speedup_boot_ci95"][1] - md)
    lbl.append(t["contrast"])
ax.errorbar(xs, ys, yerr=[lo, hi], fmt="o", capsize=4)
ax.axhspan(10, 50, color="green", alpha=0.1, label="10-50x band")
ax.axhline(1, color="k", ls=":", lw=0.8)
ax.set_xticks(xs); ax.set_xticklabels(lbl, rotation=45, ha="right", fontsize=7)
ax.set_ylabel("speedup vs passive (bootstrap 95% CI)")
ax.set_title("Engineered-vs-passive speedup with uncertainty (Mann-Whitney + Holm)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{OUT}/figures/ci_speedup.png", dpi=100)
