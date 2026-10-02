# Myco-Swarm: An In-Silico Proof of Concept for Synthetic Bacterial–Fungal Symbiosis in Microplastic Sequestration

## Abstract

**Background.** Bacteria cannot physically aggregate scattered microplastics in
situ, forcing reliance on ex-situ bioreactors. We propose and computationally
validate Myco-Swarm: engineered microplastic-binding bacteria ("scouts") emit a
synthetic pheromone that guides an engineered fungal network ("harvesters") to
envelop and sequester the plastics.
**Methods.** From 25 open-access full texts we extracted validated parameter
values (hyphal tip rate 24 µm/min; pheromone field equations; chemotaxis assay
geometries) and built a 3-D agent-based model (200 µm cube, 15% grain
obstacles, bacterial washout) with all assumed parameters swept, not fixed.
Pre-registered contrasts: engineered (χ = 0.6/1.0) vs passive (χ = 0) capture
times, n = 12 episodes each, Mann–Whitney U with Holm correction, Cliff's δ,
bootstrap 95% CIs for speedup ratios, plus branching/depletion ablations and a
time-step convergence check.
**Results.** All 16 contrasts were significant after Holm correction (U = 0,
p ≤ .0006, Cliff's δ = −1.00, complete separation). Speedup 95% CIs lay fully
inside the 10–50x target band (edge colony: 10.0–19.4x; distributed network:
19.0–41.9x) with 100% capture completeness. Ablation showed chemotaxis without
branching matches full performance (3.4 vs 3.5 min) while removing source
depletion halves it (7.3 min). Passive bacteria visited sources ~30,000 times
but sequestered 0% and were fully washed out. Absolute times were
time-step-sensitive (dt = 0.1 vs 0.05, p = .012); the speedup ratio at matched
dt held at 10.6x (p < .0001). An independent seed set reproduced the band
(edge ~17x, network ~23x).
**Conclusions.** Within stated assumptions, a chemotactic fungal swarm
sequesters scattered microplastics an order of magnitude faster than undirected
growth and completes what passive bacteria structurally cannot. No molecular
affinity (Kd) or soil transport (D) data exist in the reviewed corpus; these are
specified as the mandatory next measurements.

## 1. Introduction

Microplastics pervade agricultural soils as vectors for heavy metals and
pathogens, yet remediation stalls at collection: bacteria are too small to
filter an environment and wash away, mandating ex-situ bioreactors. Recent
co-culture upcycling systems (e.g., iGEM Heidelberg 2023) inherit this
constraint. The gap is in-situ physical sequestration. Myco-Swarm reframes the
problem as ecosystem-level behavioral symbiosis: scouts convert invisible,
scattered targets into diffusing chemical beacons, and a macroscopic
harvester network performs the physical collection. Because cross-kingdom
signaling construction is a multi-year wet-lab program, this study is
aggressively narrowed to a computational proof-of-concept with a single
falsifiable criterion: the simulated swarm must aggregate sources 10–50x
faster than passive bacterial diffusion.

## 2. Methods

### 2.1 Systematic corpus

We queried Europe PMC (open-access subset) and OpenAlex across three pillars
(plastic-binding peptides/display; synthetic GPCR/fungal signaling; spatial
modeling of diffusion and mycelial chemotaxis), screened ~30 candidates, and
retained 22 full texts plus 3 preprints/OA PDFs in a local repository with a
provenance manifest. Two targets were unrecoverable (publisher-withheld
redistribution) and recorded as gaps. No paywalls were bypassed. Every
parameter below cites its source file; values without a source were swept.

### 2.2 Model

Hyphal tips are agents on a 200 µm cube (5 µm voxels) extending at 24 µm/min
(C04 lattice-gas calibration) with EC50-gated chemotactic turning
(Keller–Segel form, C08), stochastic branching, and grain blocking (15%
blocked voxels; confinement per C01). Four pheromone-emitting sources follow a
C06-form steady-state field (heavy tail c ∝ λα/x); enveloped sources go silent
(source depletion). Bacteria are run-tumble walkers (20 µm/s) subject to
advection and per-second washout removal; they can visit but never sequester.
Swept (assumed) parameters: λα ∈ {100, 300} µm, χ ∈ {0, 0.6, 1.0},
EC50 gate K ∈ {0.01, 0.1}, inoculation {edge colony, distributed network}.
Outcomes: fraction captured, mean/all-source capture time (tall), first-capture
time. Twelve episodes per condition (seeds 11000+); independent replication at
seeds 1000+ and 5000+. Transport physics (finite-difference steady-state
solver, Monte Carlo effective-diffusion measurement) was built test-first
(tests/test_transport.py, 4/4 passing): solver verified to 0.1% against a
manufactured smooth solution with absorbing boundaries (periodic boundaries
were shown to trap a corrupting background mode); tracer diffusion recovers
free D within 10% in empty domains. A Morris screening (r = 8 trajectories,
k = 4: λα, χ, K, grain fraction) ranked assumed-parameter influence with
range-normalized effects.

### 2.3 Statistical plan (fixed before analysis)

Mann–Whitney U (two-sided) for each engineered-vs-passive tall contrast (16
tests), Holm family-wise correction, Cliff's δ, and bootstrap (5,000
resamples) 95% CIs for the speedup ratio (mean-passive/mean-engineered).
Ablations (branching off; depletion off) and a dt = 0.1 vs 0.05 convergence
check were pre-declared; a same-dt speedup verification was added after the
convergence check failed. Environment: Python 3.12, NumPy 2.2.6, SciPy 1.15.3.

## 3. Results

### 3.1 Primary outcome

All 16 contrasts were significant after Holm correction (U = 0 in every case,
p_holm ≤ .0006) with Cliff's δ = −1.00 — complete separation: every engineered
replicate was faster than every passive replicate. Bootstrap speedup 95% CIs:
edge colony 10.0–19.4x; distributed network 19.0–41.9x — all fully inside the
pre-registered 10–50x band, with 100% capture completeness in all 72
sweep episodes. A tabular Q-learning proxy failed to converge and was replaced
by a real DQN (isolated torch 2.14.1 env, C09 protocol: 20-dim frame history,
3 turn actions, Δc reward + capture bonus): after 2,000 episodes the learned
controller captures in 7.36 min mean (median 7.30, worst seed 8.0) vs greedy
8.84 min — beating the hand-designed baseline on all 10 eval seeds.

### 3.2 Mechanism (ablation; network, λ = 200 µm, K = 0.1)

Disabling branching left engineered performance unchanged (3.4 vs 3.5 min)
but tripled passive times (157.0 vs 67.9 min): branching is the passive
search's exploration engine and redundant under guidance. Disabling source
depletion halved engineered performance (7.3 vs 3.5 min): consumed beacons
must go silent or agents orbit them — a design constraint for the genetic
circuit (signal shutoff on envelopment).

### 3.3 Bacteria and robustness

Passive bacteria visited each source ~30,000 times yet sequestered 0% with 0%
retention (full washout): encounter is not the bottleneck, retention is —
the premise of the symbiosis. Independent seed sets reproduced the band (edge
~17x, network ~23x); engineered times were stable while passive baselines
varied, i.e., guidance de-risks as well as accelerates capture.

### 3.4 Computed physics and sensitivity

Tracer diffusion measured inside the v1 grain matrices gives tortuosity
Deff/D0 = 0.85 ± 0.03 (n = 5 matrices): grains obstruct modestly, so the
swept λα range already spans the realistic correction — absolute free D of
the actual pheromone remains the unmeasured quantity. Morris screening
(range-normalized effects: χ 33.0 > grain 16.3 > K 2.9 > λα 2.0) shows
chemotaxis strength and soil structure dominate capture time while the field
range is negligible at this domain scale and the EC50 gate is minor. The
measurement priority for wet-lab follow-up is therefore: (1) tip χ
dose–response, (2) soil porosity/tortuosity, (3) pheromone free D; λα
precision buys almost nothing. High σ relative to μ* throughout indicates
substantial parameter interaction (non-additive effects).

### 3.5 Numerical fidelity

Absolute times differed between dt = 0.1 (2.18 min) and dt = 0.05 (7.96 min),
Mann–Whitney p = .012: the scheme has no clean continuum limit (per-step
heading blending is not time-scaled), so absolute minutes are not claimed.
The ratio at matched dt held at 10.6x (passive 84.1 vs engineered 8.0 min,
p < .0001) — the band claim rests on ratios, explicitly not on absolutes.

## 4. Discussion

This study meets its falsifiable criterion in 3-D heterogeneous conditions (it
failed it in 2-D homogeneous conditions, peak 7.7x — reported). The result is
conditional on swept, not measured, soil transport and sensing parameters, and
on a field solve that ignores grains. Five critical evidence gaps bound the
work: no soil pheromone D, no hyphal χ, no synthetic-ligand EC50, no
peptide–plastic Kd, and no designed GPCR validated in a filamentous fungus —
each mapped to a named next measurement in the design spec. The in-silico
package (corpus, ledger, code, seeds, replication sets) is complete and is the
mandatory groundwork for wet-lab construction, not a substitute for it.

## References

1. Keller EF, Segel LA. Initiation of slime mold aggregation viewed as an
   instability. J Theor Biol. 1970;26:399-415.
2. Keller EF, Segel LA. Model for chemotaxis. J Theor Biol. 1971;30:225-234.
3. A01 — PET-selective peptide engineering via MD/umbrella sampling
   (PMC13482935). 4. A02 — LSTM-SA plastic-binding peptide design
   (PMC12486148). 5. A04 — LCI aromatic substitutions, SPR coverage
   (PMC12529122). 6. A05 — B. subtilis spore display survey (PMC13417171).
7. A06 — B. subtilis sortase vegetative display (PMC12671163).
8. A08 — PHL7 directed evolution, PDB 7NEI (PMC12371127).
9. B01 — Yeast mating platform for fungal GPCR–ligand screening
   (PMC12582325). 10. B02 — Computational Ste2 pocket redesign (PMC10220229).
11. B03 — Ratiometric GPCR directional sensing (PMC6818790).
12. B04 — GPCR-to-galactose regulon rewiring (PMC10753199).
13. B05/B06 — Fusarium Ste2/Ste3 peroxidase chemotropism
   (PMC10794396/PMC9769807). 14. B07 — Trichoderma chemotropism assays
   (Frontiers 2020, 10.3389/fmicb.2020.601251).
15. B08 — T. reesei MAPK chemotropism/cellulase (PMC9894936).
16. C01 — Hyphal navigation hierarchy (PMC12109565).
17. C02 — Aspergillus chemotropism device (PMC11288418).
18. C03 — Agent-based microbial movement, R code (PMC13564397).
19. C04 — Driven lattice-gas mycelium model (arXiv:1911.00739).
20. C06 — Optogenetic pheromone gradients, analytical field (PMC11992364).
21. C07 — Particle-based polarity, Smoldyn (PMC10569529).
22. C08 — Phenotypic heterogeneity in Keller–Segel aggregation (PMC9626439).
23. C09 — Deep RL chemotaxis, sperm model (arXiv:2209.07407).
24. Harris CR, et al. Array programming with NumPy. Nature. 2020;585:357-362.
25. Virtanen P, et al. SciPy 1.0. Nat Methods. 2020;17:261-272.
26. Hunter JD. Matplotlib. Comput Sci Eng. 2007;9:90-95.
27. Kassis T, et al. Scientific Agent Skills. arXiv:2609.00065 (2026).

## Data and code availability

Corpus: manuscripts_raw/ with manifest. Code: src/mycoswarm_abm.py,
src/mycoswarm_abm_3d.py, src/analysis_publication.py (seeds fixed; NumPy 2.2.6/SciPy
1.15.3). Results: results/, results_3d/, results_3d_robust/, results_pub/.
AI assistance used for coding/analysis under human direction; all outputs
verified by execution.
