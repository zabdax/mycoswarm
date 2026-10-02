#!/usr/bin/env python3
"""Pixel-art animation of the Myco-Swarm process on a real model field.
Scouts bind plastics -> pheromone beacons expand -> hyphal tips chemotax ->
envelop -> mat. Schematic (scripted tips on a true C06-style field).
Writes assets/mycoswarm_pixel.gif (chunky pixels, limited palette)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np

import mycoswarm_abm as sim2d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation

N = sim2d.GRID  # match model grid (60); canvas is the field itself
rng = np.random.default_rng(11)
SOURCES = [(16, 16), (48, 24), (34, 50)]  # grid coords
c, gx, gy = sim2d.make_field(SOURCES, 200.0)

# quantized glow levels, gamma-widened so beacons read on screen (pixel aesthetic)
glow_full = np.clip(((c / c.max()) ** 0.35 * 4.99).astype(int), 0, 4)

# scripted tip growth: few tips, slow branching, visible travel over the film
tips = [{"p": np.array([rng.uniform(0, N), N - 2.0]), "trail": []} for _ in range(4)]
enveloped = [False] * len(SOURCES)
events = []  # (frame, source)
MAXF = 150
for f in range(MAXF):
    for tip in list(tips):
        p = tip["p"]
        ix, iy = int(np.clip(p[0], 0, N - 1)), int(np.clip(p[1], 0, N - 1))
        g = np.array([gx[iy, ix], gy[iy, ix]])
        n = float(np.hypot(*g)) + 1e-12
        step = g / n * 0.55 + rng.normal(0, 0.30, 2)
        p = np.clip(p + step, 0, N - 1)
        tip["p"] = p
        tip["trail"].append(tuple(p.astype(int)))
        for i, s in enumerate(SOURCES):
            if not enveloped[i] and np.hypot(p[0] - s[0], p[1] - s[1]) < 2.5:
                enveloped[i] = True
                events.append((f, i))
        if rng.random() < 0.008 and len(tips) < 24:
            tips.append({"p": tip["p"].copy(), "trail": []})

PAL = {  # soil, glow x4, plastic, scout, hypha, mat, flash
    "soil": (0.16, 0.11, 0.07), "g1": (0.30, 0.16, 0.05), "g2": (0.48, 0.24, 0.06),
    "g3": (0.66, 0.36, 0.08), "g4": (0.85, 0.52, 0.12),
    "plastic": (0.10, 0.75, 0.85), "scout": (1.0, 0.9, 0.2),
    "hypha": (0.25, 0.95, 0.35), "mat": (0.35, 0.5, 0.2), "flash": (1, 1, 1)}
CAPTIONS = [(0, "1 SCOUTS BIND MICROPLASTICS"), (25, "2 PHEROMONE BEACONS"),
            (50, "3 HARVESTER CHEMOTAXIS"), (90, "4 ENVELOP + SEQUESTER"),
            (120, "5 MYCELIAL MAT HARVEST x11-33")]
os.makedirs("assets", exist_ok=True)
fig, ax = plt.subplots(figsize=(6, 6.8))
fig.patch.set_facecolor("#0a0805")
ax.set_facecolor("#0a0805")

def draw(f):
    ax.clear()
    ax.set_xlim(-1, N)
    ax.set_ylim(N, -1)
    ax.axis("off")
    img = np.zeros((N, N, 3))
    img[:, :] = PAL["soil"]
    gl = np.clip(glow_full * min(1.0, max(0.0, (f - 20) / 40.0)), 0, 4).astype(int)
    gpal = [PAL["soil"], PAL["g1"], PAL["g2"], PAL["g3"], PAL["g4"]]
    for lvl in range(1, 5):
        img[gl == lvl] = gpal[lvl]
    cap = CAPTIONS[0][1]
    for t0, txt in CAPTIONS:
        if f >= t0:
            cap = txt
    for i, s in enumerate(SOURCES):
        ev = next((ff for ff, ss in events if ss == i), None)
        if ev is not None and ev <= f:
            r = min(8, 2 + (f - ev) // 8)
            x0, y0 = max(0, s[0] - r), max(0, s[1] - r)
            img[y0:s[1] + r, x0:s[0] + r] = PAL["mat"]
        if f >= 8:  # scouts attached (2px for visibility)
            img[s[1]:s[1] + 2, s[0]:s[0] + 2] = PAL["scout"]
        if not enveloped[i]:
            img[s[1] - 1:s[1] + 1, s[0] - 1:s[0] + 1] = PAL["plastic"]
    for tip in tips:
        for (tx, ty) in tip["trail"][: max(0, f - 2)]:
            if 0 <= tx < N and 0 <= ty < N:
                img[ty, tx] = PAL["hypha"]
    for ff, ss in events:
        if 0 <= f - ff <= 4:
            img[SOURCES[ss][1] - 2:SOURCES[ss][1] + 2,
                SOURCES[ss][0] - 2:SOURCES[ss][0] + 2] = PAL["flash"]
    ax.imshow(img, interpolation="nearest")
    ax.text(N / 2, N + 1.5, f"MYCO-SWARM  |  {cap}", color="#ffd54f", fontsize=11,
            family="monospace", weight="bold", ha="center")
    ax.text(N / 2, -2.2, "scouts bind plastic - pheromone guides fungus - mat sequesters",
            color="#a1887f", fontsize=7, family="monospace", ha="center")

import shutil
from PIL import Image as PILImage

FRAMEDIR = "C:\\Windows\\Temp\\opencode\\myco_frames"
shutil.rmtree(FRAMEDIR, ignore_errors=True)
os.makedirs(FRAMEDIR, exist_ok=True)
for f in range(MAXF):
    draw(f)
    fig.savefig(f"{FRAMEDIR}\\f{f:03d}.png", dpi=100,
                facecolor=fig.get_facecolor())
frames = [PILImage.open(f"{FRAMEDIR}\\f{f:03d}.png").convert("RGB")
          for f in range(MAXF)]
frames[0].save("assets/mycoswarm_pixel.gif", save_all=True,
               append_images=frames[1:], duration=90, loop=0)
print("assets/mycoswarm_pixel.gif written",
      PILImage.open("assets/mycoswarm_pixel.gif").n_frames, "frames")
