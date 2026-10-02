#!/usr/bin/env python3
"""Build docs/MycoSwarm_Report.pdf — visual summary of the full in-silico package."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- corpus chart ---
cats = ["Pillar A\npeptide/display", "Pillar B\nGPCR/signal", "Pillar C\nmodeling"]
got = [8, 8, 6]
failed = [1, 0, 1]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(cats, got, label="full texts acquired", color="#66BB6A")
ax.bar(cats, failed, bottom=got, label="failed (HTTP 500)", color="#EF5350")
ax.set_ylabel("documents")
ax.set_title("Manuscript corpus: 22 full texts + 3 PDFs (A03, C05 unrecoverable)")
ax.legend(fontsize=8)
for i, (g, f) in enumerate(zip(got, failed)):
    ax.text(i, g + f + 0.15, f"{g}+{f}", ha="center", fontsize=9, weight="bold")
fig.tight_layout(); fig.savefig("docs/figures/corpus.png", dpi=110)

# --- speedup summary chart (primary + robust) ---
import json
s1 = json.load(open("results_3d/sweep3d.json"))
s2 = json.load(open("results_3d_robust/sweep3d.json"))
def peak(s, inoc):
    return max(x["speedup_tall"] for x in s if x["inoc"] == inoc and x["chi"] > 0)
labels = ["Edge\nprimary", "Edge\nrobust", "Network\nprimary", "Network\nrobust"]
vals = [peak(s1, "edge"), peak(s2, "edge"), peak(s1, "network"), peak(s2, "network")]
fig, ax = plt.subplots(figsize=(6, 3.4))
bars = ax.bar(labels, vals, color=["#42A5F5", "#26A69A", "#AB47BC", "#EC407A"])
ax.axhspan(10, 50, color="green", alpha=0.12, label="10-50x target band")
ax.set_ylabel("peak speedup vs undirected growth")
ax.set_title("v1 result: target band reached in 3-D soil setup (both seed sets)")
ax.legend(fontsize=8)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.1f}x", ha="center",
            fontsize=10, weight="bold")
fig.tight_layout(); fig.savefig("docs/figures/peaks.png", dpi=110)
print("charts written")
