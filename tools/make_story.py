#!/usr/bin/env python3
"""Myco-Swarm story film: 4 scenes, scrited narrative, pixel-field aesthetic.
S1 field+washout | S2 scout binding + plume | S3 harvester chemotaxis + envelop
| S4 mat harvest + stats card. Writes assets/mycoswarm_story.gif.
Run from repo root: py tools/make_story.py
"""
import os
import shutil
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Ellipse
from PIL import Image as PILImage

rng = np.random.default_rng(5)
FRAMEDIR = "C:\\Windows\\Temp\\opencode\\story_frames"
shutil.rmtree(FRAMEDIR, ignore_errors=True)
os.makedirs(FRAMEDIR, exist_ok=True)
os.makedirs("assets", exist_ok=True)

SOIL, SOIL2 = "#2b1d0e", "#3a2712"
CYAN, YELLOW = "#19c2dc", "#ffd94d"
AMBER = ["#5a2f08", "#8a4a0c", "#c06a12", "#f0901c", "#ffc44d"]
GREEN, MATC, WHITE = "#37e85a", "#5a7038", "white"

# shared cast
plastics = np.array([[12, 30], [30, 14], [44, 34], [22, 46], [48, 48]])
drift = rng.uniform(-1, 1, (14, 2))

def base(ax, title, sub):
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    ax.axis("off")
    ax.add_patch(Rectangle((2, 6), 56, 44, fc=SOIL, ec="#6b4a22", lw=2))
    ax.text(30, 54.5, title, color="#ffd54f", fontsize=13, family="monospace",
            weight="bold", ha="center")
    ax.text(30, 2.5, sub, color="#a1887f", fontsize=7.5, family="monospace",
            ha="center")

def soil_tex(ax):
    for _ in range(90):
        x, y = rng.uniform(3, 57), rng.uniform(7, 49)
        ax.add_patch(Circle((x, y), rng.uniform(0.3, 0.9), fc=SOIL2, ec="none",
                            alpha=0.7))

# ---- S1: the field (frames 0-39): scattered plastics, bacteria drift + wash out
S1 = 40
for f in range(S1):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0a0805")
    base(ax, "SCENE 1 · THE FIELD", "wind and rain scatter microplastics · bacteria wash away")
    soil_tex(ax)
    for p in plastics:
        ax.add_patch(Rectangle((p[0] - 1, p[1] - 1), 2, 2, fc=CYAN, ec="none"))
    for i in range(14):
        pos = np.array([8.0, 40.0]) + drift[i] * (f * 0.5)
        alpha = max(0.05, 1.0 - f / 38.0)  # washout fade
        ax.add_patch(Circle(pos, 0.8, fc=YELLOW, ec="none", alpha=alpha))
    if f > 20:
        ax.annotate("", xy=(52, 44), xytext=(44, 44),
                    arrowprops=dict(arrowstyle="->", color="#ef5350", lw=2))
        ax.text(48, 46, "washed out", color="#ef5350", fontsize=8,
                family="monospace", ha="center")
    fig.savefig(f"{FRAMEDIR}\\s1_{f:03d}.png", dpi=90, facecolor=fig.get_facecolor())
    plt.close(fig)

# ---- S2: the scouts (frames 40-79): rods attach, plume blooms
S2 = 40
cx, cy = 30, 28
for k in range(S2):
    f = 40 + k
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0a0805")
    base(ax, "SCENE 2 · THE SCOUTS", "B. subtilis binds plastic · pheromone beacon switches on")
    soil_tex(ax)
    ax.add_patch(Rectangle((cx - 3, cy - 3), 6, 6, fc=CYAN, ec="none"))
    nb = min(8, 1 + k // 5)
    for i in range(nb):
        ang = 2 * np.pi * i / 8 + 0.4
        rr = 4.2 + 0.3 * np.sin(k / 3 + i)
        ax.add_patch(Ellipse((cx + rr * np.cos(ang), cy + rr * np.sin(ang)),
                             2.2, 1.1, angle=np.degrees(ang), fc=YELLOW, ec="none"))
    glow_r = min(20, k * 0.55)
    for lvl in range(4, 0, -1):
        ax.add_patch(Circle((cx, cy), glow_r * lvl / 4, fc=AMBER[lvl], ec="none",
                            alpha=0.28))
    if k > 28:
        ax.text(cx, cy - 8, "SIGNAL ON", color="#ffc44d", fontsize=10,
                family="monospace", weight="bold", ha="center")
    fig.savefig(f"{FRAMEDIR}\\s2_{k:03d}.png", dpi=90, facecolor=fig.get_facecolor())
    plt.close(fig)

# ---- S3: the harvesters (frames 80-129): network grows up-gradient, envelops
S3, NBR = 50, 26
tips = [{"p": np.array([6.0 + i * 2.2, 8.0]), "trail": []} for i in range(5)]
center = np.array([cx, cy])
traj = []
for _ in range(S3):
    for tip in list(tips):
        for _ in range(2):
            d = center - tip["p"]
            n = float(np.hypot(*d)) + 1e-9
            step = d / n * 0.8 + rng.normal(0, 0.45, 2)
            tip["p"] = np.clip(tip["p"] + step, 3, 57)
            tip["trail"].append(tuple(tip["p"]))
        if rng.random() < 0.06 and len(tips) < NBR:
            tips.append({"p": tip["p"].copy(), "trail": []})
    traj.append([(tuple(t["trail"])) for t in tips])
for k in range(S3):
    f = 80 + k
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0a0805")
    base(ax, "SCENE 3 · THE HARVESTERS", "fungal network climbs the gradient · envelops the plastic")
    soil_tex(ax)
    for lvl in range(4, 0, -1):
        ax.add_patch(Circle((cx, cy), 20 * lvl / 4, fc=AMBER[lvl], ec="none", alpha=0.22))
    ax.add_patch(Rectangle((cx - 3, cy - 3), 6, 6, fc=CYAN, ec="none"))
    show = traj[k]
    for tr in show:
        if len(tr) > 1:
            xs, ys = zip(*tr[::2])
            ax.plot(xs, ys, color=GREEN, lw=2.2, solid_capstyle="round")
    if k > S3 - 12:
        ax.add_patch(Circle((cx, cy), 5.5, fc="white", ec="none", alpha=0.75))
        ax.text(cx, cy + 9, "ENVELOPED", color="white", fontsize=10,
                family="monospace", weight="bold", ha="center")
    fig.savefig(f"{FRAMEDIR}\\s3_{k:03d}.png", dpi=90, facecolor=fig.get_facecolor())
    plt.close(fig)

# ---- S4: the harvest (frames 130-169): mat lifts, stats card
S4 = 40
for k in range(S4):
    f = 130 + k
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0a0805")
    base(ax, "SCENE 4 · THE HARVEST", "biological net pulled out · plastic gone from soil")
    soil_tex(ax)
    lift = min(14, k * 0.5)
    ax.add_patch(Rectangle((22, 20 + lift), 16, 10, fc=MATC, ec="#8a9a5b", lw=2))
    for gx in range(24, 38, 3):
        ax.plot([gx, gx], [20 + lift, 30 + lift], color=GREEN, lw=1.2, alpha=0.8)
    for idx, line in enumerate(["SEQUESTERED: 100%", "SPEEDUP: 11-33x",
                                "BACTERIA SEQUESTER: 0%", "STATUS: PRE-WET-LAB READY"]):
        a = min(1.0, max(0.0, (k - 6 - idx * 5) / 6.0))
        ax.text(30, 15 - idx * 2.6, line, color="#ffd54f", fontsize=8.5,
                family="monospace", weight="bold", ha="center", alpha=a)
    fig.savefig(f"{FRAMEDIR}\\s4_{k:03d}.png", dpi=90, facecolor=fig.get_facecolor())
    plt.close(fig)

import glob
paths = sorted(glob.glob(f"{FRAMEDIR}\\s*.png"))
ims = [PILImage.open(p).convert("RGB") for p in paths]
print("frames:", len(ims))
ims[0].save("assets/mycoswarm_story.gif", save_all=True, append_images=ims[1:],
            duration=110, loop=0)
print("story written, n_frames:",
      PILImage.open("assets/mycoswarm_story.gif").n_frames)
