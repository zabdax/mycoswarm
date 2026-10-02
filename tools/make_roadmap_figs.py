#!/usr/bin/env python3
"""Roadmap figures: architecture schematic + phase timeline. matplotlib only."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- Architecture ---
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis("off")
boxes = [
    (0.3, 2.8, 2.0, 1.4, "SCOUT\nB. subtilis\n+ PET/PE peptide", "#BBDEFB"),
    (2.9, 2.8, 2.0, 1.4, "SIGNAL\nsynthetic\npheromone", "#FFE0B2"),
    (5.5, 2.8, 2.0, 1.4, "FIELD\nC06 diffusion\nλa sweep", "#C8E6C9"),
    (8.1, 2.8, 2.0, 1.4, "HARVESTER\nT. reesei + GPCR\nchemotaxis", "#E1BEE7"),
    (3.2, 0.5, 4.6, 1.2, "SIMULATION STACK: C04 growth + C08/C03 kernels\n+ C02/C04b behavior + Q-learn eval", "#F5F5F5"),
]
for x, y, w, h, t, c in boxes:
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                 fc=c, ec="black", lw=1.2))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=9, weight="bold")
for (x1, x2, y) in [(2.3, 2.9, 3.5), (4.9, 5.5, 3.5), (7.5, 8.1, 3.5)]:
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="->", lw=1.8))
ax.annotate("", xy=(2.0, 4.2), xytext=(8.5, 4.2),
            arrowprops=dict(arrowstyle="->", lw=1.2, ls="dashed", color="green"))
ax.text(5.3, 4.4, "mycelial mat sequesters plastic (harvest)", fontsize=9,
        color="green", ha="center", style="italic")
ax.text(5.5, 0.15, "Ledger: sourced (filename-cited) vs assumed (swept) — parameter_ledger.md",
        fontsize=8, ha="center", style="italic")
ax.set_title("Myco-Swarm System Architecture (in-silico scope)", fontsize=12, weight="bold")
fig.tight_layout(); fig.savefig("docs/figures/architecture.png", dpi=110)

# --- Timeline ---
phases = [
    ("P0 Env+skills", 0, 1, "done"),
    ("P1 Corpus", 1, 2, "done"),
    ("P2 Review", 2, 3, "done"),
    ("P3 Ledger", 3, 4, "done"),
    ("P4 ABM v0", 4, 5, "running"),
    ("P5 Verdict", 5, 6, "next"),
    ("P6 ABM v1 3-D", 6, 7.5, "planned"),
    ("P7 Design spec", 7.5, 9, "planned"),
    ("P8 Final report", 9, 10, "planned"),
]
colors = {"done": "#66BB6A", "running": "#FFA726", "next": "#29B6F6", "planned": "#BDBDBD"}
fig, ax = plt.subplots(figsize=(11, 3.2))
for i, (name, s, e, st) in enumerate(phases):
    ax.barh(0, e - s, left=s, height=0.55, color=colors[st], edgecolor="black")
    ax.text((s + e) / 2, 0, name, ha="center", va="center", fontsize=8, weight="bold",
            color="white" if st == "done" else "black")
ax.set_xlim(0, 10); ax.set_ylim(-0.7, 0.7); ax.set_yticks([])
ax.set_xlabel("execution order")
for k, c in colors.items():
    ax.bar(0, 0, color=c, label=k)
ax.legend(loc="upper right", fontsize=8, ncol=4)
ax.set_title("Myco-Swarm Execution Timeline", fontsize=12, weight="bold")
fig.tight_layout(); fig.savefig("docs/figures/timeline.png", dpi=110)
print("figures written")
