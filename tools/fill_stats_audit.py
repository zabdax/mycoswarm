#!/usr/bin/env python3
"""Fill the peer-review statistics-reproducibility template with honest statuses."""
import json

tpl = json.load(open("skills/scientific-agent-skills/skills/peer-review/assets/"
                      "statistical_reproducibility_template.json"))
tpl["checklist_id"] = "MYCOSWARM-v1-2026-10-02"
tpl["study_design"] = "simulation_experiment"

notes = {
 "question.estimand_alignment": ("verified_present", "Estimand (speedup ratio of capture times, engineered vs passive) fixed before analysis; band 10-50x pre-registered from proposal."),
 "design.unit_and_independence": ("verified_present", "Unit = one episode (fixed seeds, independent RNG streams). Limitation: source positions fixed across reps; obstacles vary by seed."),
 "design.sample_size_precision": ("verified_present", "n=12 episodes/group; precision via 5000-resample bootstrap 95% CIs."),
 "design.allocation_randomization": ("verified_present", "Pre-declared seed blocks (11000s sweep, 12000s ablation, 13000s convergence). No allocation beyond RNG."),
 "design.blinding": ("not_applicable", "Simulation with scripted outcomes; no human observers."),
 "data.inclusion_exclusion": ("verified_present", "All episodes included; no exclusions. T_MAX=1200 never bound v1 runs (100% capture)."),
 "data.missing_data": ("verified_present", "No missing episodes. Corpus-level: 2/27 target docs unrecoverable (recorded, not imputed)."),
 "data.outliers_transformations": ("verified_present", "No outlier removal performed; no transformations. Raw per-rep values archived."),
 "analysis.prespecification": ("partly_documented", "16 contrasts + ablation + convergence pre-declared. Same-dt verification added POST HOC after convergence failure — disclosed in manuscript 3.4."),
 "analysis.method_design_alignment": ("verified_present", "Capture times are skewed/floor-bounded; Mann-Whitney U appropriate. Test selected during analysis, not pre-registered — disclosed."),
 "analysis.assumptions_diagnostics": ("verified_present", "Shapiro-Wilk run on all 24 groups (results_pub/normality.json): 2/24 non-normal, confirming the non-parametric route. Mann-Whitney requires independence (independent RNG streams, satisfied), not normality. No outlier removal; no transformations."),
 "analysis.multiplicity": ("verified_present", "Holm correction over all 16 contrasts; exact Holm p reported."),
 "analysis.clustering_repeated_measures": ("verified_present", "Episodes independent; shared fixed source geometry noted under unit_and_independence."),
 "results.effect_sizes_uncertainty": ("verified_present", "Cliff's delta + bootstrap 95% CI for every contrast; CIs plotted."),
 "results.denominators_flow": ("verified_present", "All reps, all conditions reported including negatives (v0, Q-learn, convergence)."),
 "results.complete_outcomes_harms": ("verified_present", "Negative/null findings reported (v0 7.7x; Q-learn timeout; dt-sensitivity). No harms applicable."),
 "reproducibility.data_materials_access": ("verified_present", "Corpus + manifest + per-rep JSONs + seeds archived in-repo."),
 "reproducibility.code_environment_parameters": ("verified_present", "Python 3.12, NumPy 2.2.6, SciPy 1.15.3; scripts + argv seeds; matplotlib 3.10.9 figures."),
 "reproducibility.provenance_versions": ("verified_present", "Primary/robust/pub seed blocks; file manifest; ledger versions."),
 "ethics.approval_consent_governance": ("verified_present", "No human/animal subjects. Engineered-organism designs remain computational with explicit stop rules; dual-use review deferred to wet-lab stage and flagged."),
 "interpretation.claim_evidence_causality": ("partly_documented", "Causal language scoped to within-model effects; no real-world efficacy claimed. CLAIM-003 mechanisticflagged for expert review."),
 "integrity.deviations_selective_reporting": ("verified_present", "Deviation (post-hoc same-dt) disclosed; all conditions and failures reported; no cherry-picking."),
}
by_id = {it["id"]: it for it in tpl["items"]}
for iid, (st, note) in notes.items():
    by_id[iid]["status"] = st
    by_id[iid]["note"] = note
    if st in ("verified_present", "partly_documented"):
        by_id[iid]["evidence_locations"] = ["docs/manuscript.md", "results_pub/"]
by_id["design.blinding"]["applicability"] = "not_applicable"
tpl["specialist_review"] = {"needed": "yes",
                            "areas": ["mechanistic_claim_review", "assumption_diagnostics"],
                            "requested": True}
json.dump(tpl, open("docs/stats_reproducibility.json", "w"), indent=2)
print("wrote docs/stats_reproducibility.json")
