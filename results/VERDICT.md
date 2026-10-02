# Myco-Swarm ABM v0.4 — Verdict (P5)

Source: `results/sweep.json` (72 conditions × 10 reps), `results/bacteria.json`,
`results/qlearn.json`. Code: `myocoswarm_abm.py`. Params: `parameter_ledger.md`.

## Result: 10x–50x NOT reached in 2-D homogeneous geometry. Peak 7.7x.

| Setup | Passive (χ=0) tall | Best engineered tall | Max speedup |
|---|---|---|---|
| Edge colony | 14.9 min | 5.8 min (χ=1, K=0.01) | **2.6x** |
| Network | 7.6 min | 1.0 min (χ=1, K=0.01) | **7.7x** |

Completeness 100% in all 72 conditions. First-capture speedup ~1.5–3x.
Bacteria: ~30,000 visits/source, sequestered **0%** (no envelopment mechanism).

## Honest interpretation

1. Against the proposal's literal baseline (passive bacterial diffusion), the
   comparison is sequestration, not speed: swarm 100% vs bacteria 0% at T_MAX.
   A 10–50x *rate* ratio is undefined (division by zero) — the band in the
   figure is the wrong metric shape for that baseline.
2. Against undirected hyphal growth, chemotaxis gives 2.6–7.7x in 2-D
   homogeneous matrix. Below the 10x band, but the geometry favors the
   baseline (small domain, no obstacles, no washout — all conditions where
   random search does well).
3. Q-learning proxy failed to converge (test: random 453 / greedy 8.8 /
   qlearn 1200 min). Greedy gradient-climbing is the working policy.
   DQN needs a torch environment (roadmap P6).

## What earns the 10x (P6 requirements)

- 3-D heterogeneous soil: obstacles + advection/washout penalize random
  search and bacteria far more than gradient-guided hyphae.
- Larger domains where guidance compounds over distance.
- Measured (not swept) soil D, χ, EC50 to replace the assumed block.

Artifacts found and fixed during v0–v0.4: orbit-trapping without source
depletion; timeout-penalty contaminating means; 80%-stop saturating
completeness; indent bug collapsing the K sweep (rerun clean).
