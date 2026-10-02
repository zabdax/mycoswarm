# Myco-Swarm Parameter Ledger — Sourced vs Assumed

Rule: every number below is tagged. SOURCED = transcribed from a local file in
`manuscripts_raw/` (filename cited). ASSUMED = no local source; swept in the
sensitivity analysis and flagged in all results.

## SOURCED — hyphal growth (surface colonies, no chemotaxis)

| Param | Value | Source file | Original context |
|---|---|---|---|
| Tip extension rate | 0.4 µm/s = 24 µm/min | C04_mycelium_growth_model_arXiv1911_00739.pdf | Lattice hop rate 1/s × ε = 0.4 µm |
| Tip rate range | 20–30 µm/min (Neurospora) | C04 (cited anchor) | Experimental literature cited in C04 |
| Lattice spacing ε | 0.4 µm | C04 | Model definition |
| Entry α | 0.2–0.4 s⁻¹ | C04 (Fig.2–3, calibrations) | Fitted to Rhizopus/Neurospora |
| Loss δ | 0.2–0.3 s⁻¹ | C04 | Same fits |
| Branch parameter γ | 0.9–0.998 | C04 | 0.9 Fig.2; 0.995–0.998 calibrations |
| Retraction rate | 0.4 ± 0.3 µm/min | C04b_AMF_SporeChip_PMC10964749.txt | AMF anastomosis observations |
| Reversal rate | 0.2 ± 0.1 µm/min | C04b | Same |
| Septa spacing | 26.3 ± 11.8 µm | C04b | Same |
| Turning | ~90° at attractant boundary | C02_Aspergillus_chemotropism_PMC11288418.txt | Y-device glucose layers |
| Tip-difference strong/weak/control | 39–40±5–8 / 15±6 / 5±4 | C02 | Glucose/glycerol battery |
| Avoidance magnitude | ~−40 (NH₄Cl) | C02 | Same device |

## SOURCED — gradient field form (agarose yeast, NOT soil)

| Param | Value | Source file | Original context |
|---|---|---|---|
| Field equation | ∂c/∂t = D∇²c + r·ρα·δ(z)·Θ(−x) − Ω·ρA·δ(z)·c | C06_optogenetic_pheromone_PMC11992364.txt | Yeast α-factor, cell-uptake degradation |
| Steady-state heavy tail | c ∝ λα/x; λα ≡ D/(ΩρA) | C06 | Same |
| Fitted λα | ~735 µm | C06 | Same |
| C = 2c(0)/EC50 | 1.45 | C06 | Same |
| Hill n | 1 expression / 3 morphology | C06 | Same |
| Border slope | ~5×10⁻³ EC50/µm | C06 | Same |
| Receptor D (Ste2) | 0.0005 µm²/s | B03_ratiometric_GPCR_PMC6818790.txt | Yeast mating cell (FRAP) |
| Random-orientation floor | 0.5 nM/µm gradient | B03 | Yeast mating |
| Ratiometric gain | SR up to >2 | B03 | Same |

## SOURCED — doses & assay geometry (plate assays, NOT soil)

| Param | Value | Source file |
|---|---|---|
| Pheromone plate dose | 378–400 µM | B01 (400 µM), B06 (378 µM) |
| HRP dose | 4 µM | B05, B06 |
| Glucose (T. reesei) | 1% | B08_Treesei_MAPK_PMC9894936.txt |
| Glucose optimum (T. atroviride) | 1–50 mM, best 10 mM | B07 Frontiers PDF |
| Geometry | 5 mm filters, 50 µL, 14 h, CI formula, n = 100–500 | B05 / B06 / B07 |
| Yeast EC50s (Fusarium system) | A4 0.516 nM, Fo 29.2 nM, Bb 0.245 nM | B01 |

## COMPUTED from model physics (not assumed, not measured)

| Param | Value | How obtained |
|---|---|---|
| Tortuosity Deff/D0 at 15% grains | 0.85 ± 0.03 (n = 5 matrices) | Monte Carlo tracer diffusion in v1 grain matrices (`transport.measure_deff`, tested in `tests/test_transport.py`) |
| FD field solver | Validated: 0.1% on smooth MMS; Yukawa shell r = 0.9985 (lattice-delta limit documented) | `transport.py`, Dirichlet faces (periodic BC shown to trap background mode) |

## ASSUMED — swept, no local source (Critical Research Gaps 7–8)

| Param | Swept range | Rationale |
|---|---|---|
| Soil effective D (pheromone) | Via λα 50–700 µm + tortuosity 0.85 | Free D still unmeasured; Ω unknown so λα stays swept |
| Chemotactic χ (tip bias strength) | 0 (passive) – 1 (strong) | C08 χ dimensionless; C03 σ relative; no physical χ |
| Synthetic EC50 | 0.1–100 nM | B01 yeast EC50s are non-transferable guides |
| λα (soil) | 50–700 µm | C06 735 µm is agarose; soil tortuosity shortens |
| Capture radius | 10 µm | Order of hyphal diameter scale (C01: few µm) |
| Plastic count / domain | v0: 5 sites / 500 µm square; v1: 4 sites / 200 µm cube | Computational convenience; not field density |
| Branching prob/step | from C04 γ mapping | Transferred from surface-colony fits (flagged) |

## Simulation choices (flagged, not sourced)

- 2-D domain (3-D extension = future work; proposal asks 3-D).
- Analytic steady-state field, not explicit diffusion solver.
- Homogeneous matrix, no obstacles/grains (C03 also assumes homogeneity).
- Each tip = agent; colonies not resolved.
- RL = tabular Q-learning on (c-bin, gradient-bin), NOT DQN (no torch in env); C09 DQN used as protocol template only.
