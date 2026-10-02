# Myco-Swarm — Final In-Silico Report (P8)

## Claim

A chemotactic fungal network sequesters scattered microplastic sources
**11–33x faster than undirected hyphal growth** in 3-D heterogeneous matrix,
and completes what passive bacteria structurally cannot (0% sequestered,
fully washed out). Traceability: `results_3d/sweep3d.json`,
`results_3d/bacteria3d.json`, `results_3d/figures/speedup3d.png`;
code `src/mycoswarm_abm_3d.py`; params `docs/parameter_ledger.md`.

## Evidence chain

- **Corpus**: 22 OA full texts + 3 PDFs in `manuscripts_raw/` (A03/C05
  unrecoverable, recorded). Phase-2 review extracted all datasets, equations,
  and parameter values used; 9 Critical Research Gaps flagged, none bridged.
- **Sourced physics**: C04 tip rate 24 µm/min + lattice calibration;
  C06 reaction-diffusion field form (λα fitted 735 µm, agarose);
  C08/C03 taxis kernels; C02/C04b behavior rules; B03 gradient-sensing design
  rule; B01/B05/B06 assay geometries and EC50-scale anchors.
- **Assumed block (swept)**: soil D via λα {100, 300} µm, χ {0–1},
  EC50 gate K, washout/advection rates, grain fraction 15%, capture radius.
- **v0 (2-D homogeneous)**: peak 7.7x — below band. Correct negative,
  published in `results/VERDICT.md` with four fixed model bugs.
- **v1 (3-D + grains + washout)**: edge 11–12x, network 21–33x, 100%
  completeness in all 24 conditions; bacteria 0% retained, 0% sequestered.
- **Robustness (fresh seeds 5000+, `results_3d_robust/`)**: edge ~17x,
  network ~20–24x (peak 23.7x) — band reproduces; passive baseline varies
  across seed sets while engineered times stay stable (~6–7 / ~2.6–3 min).
- **Publication layer (`results_pub/`, `docs/manuscript.md`)**: 16/16 contrasts
  Holm-significant (U = 0, p ≤ .0006, Cliff's δ = −1.00); bootstrap CIs edge
  10.0–19.4x, network 19.0–41.9x; ablation + convergence + Shapiro checks;
  claim matrix 9/9 valid; stats audit 19 verified / 0 missing. Absolute times
  are dt-sensitive (p = .012) — ratios only are claimed (same-dt 10.6x,
  p < .0001).
- **Grain-aware field (`results_pub/grainfield.json`, fixed no-flux solver +
  source carve)**: network solver-field 3.8 vs analytic 2.2 min (~15x vs
  passive) — band holds; edge 9.5 vs 5.8 (~8.6x, borderline). Grains cost
  ~1.6–1.7x. First attempt with absorbing grains + a NaN event was discarded
  as flawed, fixed, and rerun clean.
- **DQN controller (`src/dqn_chemotaxis.py`, isolated torch 2.14.1 env, 2,000
  episodes)**: learned policy captures in 7.36 min mean (median 7.30, worst
  seed 8.0) vs greedy 8.84 — wins on all 10 eval seeds (`results_dqn/`).
  Supersedes the failed tabular proxy. Multi-source 3-D policy
  (`src/dqn3d_chemotaxis.py`): 21.0 vs greedy 24.9, wins all 10 seeds.

## What the numbers do and do not prove

- Prove: under stated assumptions, gradient-guided branching networks
  aggregate scattered sources an order of magnitude faster than undirected
  growth, and persistence (attachment) beats washout-prone planktonic cells.
- Do not prove: real-soil rates (D/χ/EC50 assumed), molecular feasibility
  (no Kd for any synthetic binder/receptor pair exists in corpus), or
  3-D field accuracy (obstacles ignored in field solve — flagged).

## Pre-wet-lab package (P7, `docs/design_spec.md`)

Peptide pipeline (PepBD/LSTM-SA → A01/A04 filters → A05/A06 chassis) and
GPCR module (B02 redesign → B01 pre-screen → B04/B03 parts → B08 hooks),
each with stop rules marking unvalidated steps. Next physical measurements
required: soil pheromone D, tip χ dose–response, binder Kd series.
