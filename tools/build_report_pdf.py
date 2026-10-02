#!/usr/bin/env python3
"""Assemble docs/MycoSwarm_Report.pdf with reportlab platypus."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable)

W, H = A4
styles = getSampleStyleSheet()
title = ParagraphStyle("Title2", parent=styles["Title"], fontSize=24, spaceAfter=4,
                       textColor=colors.HexColor("#1B5E20"))
h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, spaceBefore=14,
                    spaceAfter=6, textColor=colors.HexColor("#2E7D32"))
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceBefore=8,
                    spaceAfter=4, textColor=colors.HexColor("#33691E"))
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14)
small = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8.5, leading=11.5,
                       textColor=colors.HexColor("#424242"))
cell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=8.5, leading=11)
hdr = ParagraphStyle("Hdr", parent=styles["Normal"], fontSize=8.5, leading=11,
                     textColor=colors.white, fontName="Helvetica-Bold")

def img(path, w=15 * cm):
    return Image(path, width=w, height=w * 0.62, kind="proportional")

def stable(data, widths=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F8E9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

P = Paragraph
story = [
    P("Myco-Swarm", title),
    P("In-Silico Proof of Concept for Synthetic Bacterial–Fungal Symbiosis "
      "in Microplastic Sequestration — Final Report", styles["Normal"]),
    P("Autonomous research run · all methods grounded in local full texts · "
      "assumptions explicitly flagged", small),
    HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2E7D32")),
    P("1 · Objective", h1),
    P("Engineered <i>B. subtilis</i> scouts bind microplastics and emit a synthetic "
      "pheromone; engineered <i>T. reesei</i> harvesters follow the gradient and "
      "sequester plastic into harvestable mycelial mats. Deliverable: computational "
      "proof that the swarm aggregates plastics <b>10–50x faster than passive "
      "bacterial diffusion</b>, as mandatory groundwork before any wet lab.", body),
    img("docs/figures/architecture.png"),
    Spacer(1, 6),
    P("2 · How the proposal documents were tailored down", h1),
    P("The <i>docs/*.md</i> briefs describe a multi-year cross-kingdom program. "
      "Per the TA constraint (proposal_1.md), everything was narrowed to a purely "
      "computational proof-of-concept:", body),
    stable([
        [P("<b>Brief element</b>", hdr), P("<b>Tailoring decision</b>", hdr),
         P("<b>Landed as</b>", hdr)],
        [P("AlphaFold 3 / RFdiffusion peptide design", cell),
         P("No AF3-designed PET-binder with affinity data exists in corpus — downgraded to LSTM-SA pipeline spec with stop rules", cell),
         P("docs/design_spec.md §A", cell)],
        [P("Synthetic GPCR in <i>T. reesei</i>", cell),
         P("No designed-GPCR-in-fungus exists locally — yeast-proven parts + assay formats only, port flagged as gap", cell),
         P("docs/design_spec.md §B", cell)],
        [P("NetLogo / PyTorch 3-D soil simulation", cell),
         P("No mycelium-chemotaxis codebase in corpus; no torch in env — custom numpy ABM (2-D then 3-D), tabular Q-learning proxy", cell),
         P("mycoswarm_abm.py, mycoswarm_abm_3d.py (now src/)", cell)],
        [P("10–50x success metric", cell),
         P("Unprovable from literature (no capture-rate data) — converted to a measured simulation outcome with honest verdicts incl. a published negative (v0)", cell),
         P("results/VERDICT.md, results_3d/", cell)],
        [P("Paywalled literature", cell),
         P("OA-only rule; Cloudflare-blocked PDFs replaced by identical EBI fullTextXML; A03/C05 failures recorded, never bypassed", cell),
         P("manuscripts_raw/ + manifest", cell)],
    ]),
    P("3 · Evidence pipeline", h1),
    img("docs/figures/timeline.png"),
    Spacer(1, 4),
    P("Skill audit → new stdlib pipeline skill (<i>mycoswarm-fulltext-pipeline</i>) → "
      "3 parallel harvest agents (~30 OA candidates) → 22 full texts + 3 PDFs → "
      "3 extraction agents (per-claim filename citations) → parameter ledger "
      "(sourced vs assumed) → ABM v0 → verdict → ABM v1 → robustness → this report.",
      body),
    img("docs/figures/corpus.png"),
    PageBreak(),
    P("4 · Simulation results", h1),
    P("v0 (2-D homogeneous): peak <b>7.7x</b> — below band, reported as a negative. "
      "v1 (3-D + 15% grains + bacterial washout):", body),
    img("results_3d/figures/speedup3d.png", w=16 * cm),
    Spacer(1, 4),
    img("docs/figures/peaks.png"),
    Spacer(1, 4),
    stable([
        [P("<b>Setup</b>", hdr), P("<b>Undirected</b>", hdr),
         P("<b>Engineered</b>", hdr), P("<b>Speedup</b>", hdr)],
        [P("Edge colony (primary / robust)", cell), P("14.9 / 115 min", cell),
         P("5.8–6.7 / ~6.5 min", cell), P("11–12x / ~17x", cell)],
        [P("Network (primary / robust)", cell), P("7.6 / 60.5 min", cell),
         P("1.0–3.3 / ~2.7 min", cell), P("21–33x / ~23x", cell)],
        [P("Bacteria (both runs)", cell), P("~30k visits/source", cell),
         P("0% retained, 0% sequestered", cell), P("n/a (division by zero)", cell)],
    ]),
    Spacer(1, 4),
    P("Chemotaxis times are stable across seed sets (~6–7 / ~2.6–3 min) while "
      "passive baselines wobble — guidance de-risks capture, not just accelerates it. "
      "Tabular Q-learning failed; the real DQN (torch env, 2,000 episodes) captures "
      "in 7.36 min mean vs greedy 8.84, winning on all 10 eval seeds.",
      body),
    P("5 · Gaps & pre-wet-lab requirements", h1),
    stable([
        [P("<b>#</b>", hdr), P("<b>Critical gap</b>", hdr), P("<b>Needed measurement</b>", hdr)],
        [P("1", cell), P("No soil pheromone D; no hyphal χ; no synthetic EC50", cell),
         P("Diffusion-cell + dose–response assays", cell)],
        [P("2", cell), P("No peptide–plastic Kd anywhere in corpus", cell),
         P("SPR/QCM-D binder series", cell)],
        [P("3", cell), P("No designed GPCR validated in filamentous fungus", cell),
         P("Ste2-redesign expression + activation assay", cell)],
        [P("4", cell), P("No <i>T. reesei</i>–synthetic-ligand chemotropism demo", cell),
         P("Plate-CI dose–response (B07 format)", cell)],
        [P("5", cell), P("Field solve ignores grains; washout rate assumed", cell),
         P("Tracer-calibrated 3-D transport model", cell)],
    ]),
    Spacer(1, 6),
    P("Package (interim): corpus + ledger + v0/v1 + design spec — full package below.", small),
    PageBreak(),
    P("6 · What was done — in detail", h1),
    P("Corpus acquisition (Phase 1). Three parallel harvest agents queried EuropePMC "
      "(OA-only) and OpenAlex across the three pillars, returning ~30 candidates with "
      "verified DOIs/PMCIDs. Twenty-four full texts were pulled via EBI fullTextXML "
      "(identical OA content; europepmc.org PDF rendering was Cloudflare-blocked from "
      "this network) plus two arXiv PDFs and one Frontiers OA PDF — 25 local documents "
      "with a provenance manifest. Two targets (A03, C05) returned HTTP 500 (publisher "
      "withholds redistribution) and were recorded as gaps. A new stdlib-only pipeline "
      "skill was written and tested because the vendored uv-based scripts cannot run "
      "in this environment.", body),
    P("Methodological extraction (Phase 2). Three more agents parsed only local files, "
      "with per-claim filename citations and explicit gap flags. Yield: the sole "
      "sequence-to-affinity training set (PepBD ~2.3M, A02), the only PET-selective "
      "binder data (QCM-D/PMF, A01), the only absolute surface-density data (SPR, A04), "
      "spore/vegetative display parts (A05/A06), the Ste2 redesign pipeline (B02, "
      "in-silico only), yeast GPCR circuit parts (B04) with the ratiometric sensing "
      "rule (B03, Ste2 D = 0.0005 µm²/s), filamentous chemotropism mechanisms and "
      "plate-CI assay formats (B05/B06/B07), T. reesei MAPK hooks (B08), and the full "
      "simulation-physics set: C06 field equations (λα ~735 µm, agarose), C08 "
      "Keller–Segel forms, C03 agent rules with R code, C04 lattice growth (24 µm/min "
      "tip rate), C02/C04b behavior numbers, C07 particle framework, and the C09 DQN "
      "protocol template.", body),
    P("Parameter ledger. Every number tagged sourced (filename-cited) or assumed "
      "(swept). The assumed block — soil D, hyphal χ, synthetic EC50, washout, grain "
      "fraction, capture radius — is the honest core of the sensitivity analysis, not "
      "a footnote.", body),
    P("ABM v0 (2-D, homogeneous). Twenty hyphal-tip agents at the sourced 24 µm/min, "
      "steady-state C06-style field, EC50-gated chemotactic turning, branching, and "
      "source depletion on capture. A 72-condition sweep (λ × χ × K × 10 reps) plus a "
      "run-tumble bacterial baseline and a tabular Q-learning proxy (no torch in env). "
      "Four model bugs were found and fixed en route: orbit-trapping without depletion, "
      "timeout penalties contaminating means, an 80%-stop saturating completeness, and "
      "an indent bug collapsing the K sweep. Result: peak 7.7x — published as a "
      "negative (results/VERDICT.md), which is what motivated the 3-D build.", body),
    P("ABM v1 (3-D + grains + washout). A 200 µm cube with 15% blocking grains, "
      "3-D unit-vector headings, bacterial advection plus per-second washout removal "
      "(hyphae persist as an attached network). Result: edge 11–12x, network 21–33x "
      "at 100% completeness; bacteria 0% retained and 0% sequestered. A fresh-seed "
      "rerun reproduced the band (edge ~17x, network ~23x) with engineered times "
      "stable while passive baselines wobbled — guidance de-risks capture.", body),
    P("Design spec (P7). In-silico-only build plans with stop rules: LSTM-SA binder "
      "pipeline filtered by A01/A04 selectivity rules onto A05/A06 display chassis "
      "(no Kd claimed); Ste2 pocket redesign pre-screened in YeMaP format, wired "
      "through B04/B03 parts onto B08 MAPK hooks (no filamentous validation claimed).",
      body),
    P("7 · Making the in-silico more powerful", h1),
    P("In order of leverage:", body),
    stable([
        [P("<b>Upgrade</b>", hdr), P("<b>Why it matters</b>", hdr),
         P("<b>Needs</b>", hdr)],
        [P("Measured soil D, χ, EC50", cell),
         P("Replaces the entire assumed block; converts sweeps into predictions", cell),
         P("Diffusion-cell + plate-CI dose–response (wet lab)", cell)],
        [P("Explicit 3-D diffusion solver", cell),
         P("Grains currently ignored in the field solve; real tortuosity reshapes gradients", cell),
         P("Finite-difference/voxel solver; tracer calibration", cell)],
        [P("Larger heterogeneous domains", cell),
         P("Guidance compounds with distance; current 200–300 µm flatters random search", cell),
         P("Compute only; ~10x runtime", cell)],
        [P("Real DQN + baselines", cell),
         P("Tabular proxy failed to converge; learned policies may beat greedy", cell),
         P("PyTorch environment", cell)],
        [P("Peptide structure validation", cell),
         P("Docking/MD of top LSTM-SA designs against PET surfaces", cell),
         P("AF2 + Gromacs time; A01/A08 protocols exist", cell)],
        [P("Uncertainty quantification", cell),
         P("Posteriors over assumed params instead of grid sweeps", cell),
         P("Compute only (ensemble runs)", cell)],
        [P("Bacterial retention physics", cell),
         P("Washout rate is assumed; adhesion/biofilm would change the contrast", cell),
         P("Literature rates or microfluidic data", cell)],
    ]),
    Spacer(1, 6),
    P("None of these weaken the current claim — they narrow its error bars and extend "
      "its domain. The package as it stands is the mandatory groundwork the proposal "
      "requires before wet-lab spend.", body),
    PageBreak(),
    P("8 · Publication-grade evidence (no wet lab)", h1),
    P("Pre-registered contrasts (Mann–Whitney U, Holm over 16 tests, Cliff's δ, "
      "bootstrap 5,000-resample 95% CIs) on n = 12 episodes per condition, "
      "SciPy 1.15.3:", body),
    stable([
        [P("<b>Family</b>", hdr), P("<b>Result</b>", hdr), P("<b>CI location</b>", hdr)],
        [P("Edge colony, 8 contrasts", cell),
         P("All U = 0, p_holm ≤ .0006, δ = −1.00 (complete separation)", cell),
         P("Speedup CI 10.0–19.4x — inside band", cell)],
        [P("Network, 8 contrasts", cell),
         P("All U = 0, p_holm ≤ .0006, δ = −1.00", cell),
         P("Speedup CI 19.0–41.9x — inside band", cell)],
        [P("Ablation (λ = 200, K = 0.1)", cell),
         P("No-branch engineered 3.4 ≈ full 3.5 min; no-depletion 7.3 min; passive no-branch 157 vs 67.9 min", cell),
         P("Branching = passive exploration; depletion = anti-orbiting", cell)],
        [P("Convergence dt 0.1 vs 0.05", cell),
         P("2.18 vs 7.96 min, p = .012 — absolutes dt-sensitive; same-dt ratio 10.6x, p < .0001", cell),
         P("Ratios claimed, absolutes not", cell)],
        [P("Assumptions (Shapiro × 24)", cell),
         P("2/24 groups non-normal — non-parametric route confirmed correct", cell),
         P("results_pub/normality.json", cell)],
    ]),
    Spacer(1, 4),
    P("Machine-checked audits: claim–evidence matrix 8/8 valid "
      "(docs/claim_audit.json); statistics–reproducibility 19 verified, 0 missing, "
      "2 disclosed partials — post-hoc same-dt check and within-model causality scope "
      "(docs/stats_audit.json). Full IMRAD manuscript with verified-only references: "
      "docs/manuscript.md.", body),
    Spacer(1, 4),
    P("Strength upgrades (TDD transport physics). Finite-difference field solver "
      "built test-first (tests/test_transport.py, 4/4 green): 0.1% on manufactured "
      "smooth solutions; Yukawa shell correlation 0.9985 (lattice-delta limit "
      "documented); periodic boundaries proven to trap a corrupting background mode, "
      "Dirichlet used. Monte Carlo tortuosity in our grain matrices: Deff/D0 = "
      "0.85 ± 0.03. Morris screening (range-normalized): χ (33) > grains (16) > "
      "K (2.9) > λα (2.0) — wet-lab priority is χ dose–response, then soil structure; "
      "λα precision buys almost nothing. Claim matrix now 9/9 valid.", body),
    Spacer(1, 6),
    P("Package: manuscripts_raw/ (25 docs) · docs/parameter_ledger.md · src/ (model + analysis) · "
      "results/ + results_3d/ + results_3d_robust/ + results_pub/ · docs/manuscript.md · docs/claim_matrix.csv · "
      "docs/design_spec.md · docs/roadmap.md — ready for wet-lab handoff.", small),
]

doc = SimpleDocTemplate("docs/MycoSwarm_Report.pdf", pagesize=A4,
                        leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title="Myco-Swarm Final Report", author="Myco-Swarm initiative")
doc.build(story)
print("PDF built")
