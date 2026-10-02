# Myco-Swarm P7 — Peptide & GPCR Design Spec (in-silico only)

Provenance rule: each step names its local source file. No affinity/efficacy
claims beyond what those files contain.

## A. Plastic-binding peptide pipeline

1. **Training data**: PepBD-scale sequence→score set (PE/PP/PET + PVC/nylon-6,6)
   + LSTM-SA code — `A02_AI_plastic_binding_peptides_PMC12486148.txt`.
   Retrain per-plastic LSTM regressors (2 layers, hidden 512; R² 0.952–0.977
   reported) then simulated-annealing design (21,525 mutations/run) for
   promiscuous (PET+PE) and PET-selective objectives.
2. **Selectivity filters**: Tyr→Glu aromatic-reduction rule (PS −69–85%,
   PET unchanged) — `A01_PET_selective_peptides_PMC13482935.txt`; LCI
   aromatic-substitution coverage metrics (SPR pmol/cm²) —
   `A04_LCI_PS_binding_PMC12529122.txt`. Reject designs violating these.
3. **Validation bar (computational)**: MM/GBSA + normal-mode entropy +
   steered-MD spot checks per `A02`; QCM-D/fluorescence comparison format
   per `A01`. Experimental testing explicitly required before any binding
   claim — no Kd is claimed here.
4. **Display chassis**: B. subtilis spore anchors SscA (total activity) /
   CotY-C (surface accessibility) + DuraPETase activity format —
   `A05_spore_display_PMC13417171.txt`; vegetative YhcS–LPDTS wall display
   (CALB metrics as expression benchmark) —
   `A06_Bsubtilis_sortase_PMC12671163.txt`. Peptide–anchor fusions are
   constructs to be built, not validated binders.
5. **Stop rule**: no AlphaFold 3 / RFdiffusion PET-binder with measured
   affinity exists in corpus (`A09` review-table mentions only) — such
   designs are labeled *computational candidates*, never *binders*.

## B. Synthetic GPCR–pheromone module (T. reesei target)

1. **Pocket redesign**: Zernike-descriptor + Monte Carlo pipeline against
   PDB 4LDO/7AD3 templates, AutoDock-Vina + Gromacs validation —
   `B02_GPCR_biosensor_design_PMC10220229.txt`. Output: ranked mutant panels
   for a non-natural ligand (activation NOT proven in source — flag carried).
2. **Pre-screen**: YeMaP mating + barcoded Cre-lox multiplex format; potency
   benchmark A4 EC50 0.516 nM vs native 29.2 nM; chemotropism translation
   check at 400 µM plate format —
   `B01_yeast_GPCR_screen_PMC12582325.txt`.
3. **Circuit parts (yeast-proven, T. reesei port = gap)**: sTF
   Gal4DBD–Ste12PRD, PTEF2-GPA1/STE2, Δbar1, PTEF2-SST2 —
   `B04_GPCR_galactose_regulon_PMC10753199.txt`; ratiometric correction
   (SR up to >2) — `B03_ratiometric_GPCR_PMC6818790.txt`.
4. **T. reesei hooks**: CSG1/CSG2 + TMK1/2/3; TMK3 required for glucose
   chemotropism — `B08_Treesei_MAPK_PMC9894936.txt`; CWI-Mgv1 dependency
   pattern (Ste2+Ste3 interdependent) —
   `B05_Ste2_chemotropism_PMC10794396.txt` /
   `B06_Ste3_chemotropism_PMC9769807.txt`; plate CI assay geometries —
   `B07_Trichoderma_chemotropism_assay_frontiers2020.pdf`.
5. **Stop rule**: no designed-GPCR-in-filamentous-fungus and no
   T. reesei–synthetic-ligand chemotropism exist locally — module is a
   *build plan with named parts and assay formats*, not a validated circuit.
