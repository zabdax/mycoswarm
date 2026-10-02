#!/usr/bin/env python3
"""Repo banner: dark soil-green, title + tagline + three stat chips."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 420
img = Image.new("RGB", (W, H), (12, 20, 12))
d = ImageDraw.Draw(img)
# soil gradient bands
for i in range(H):
    t = i / H
    d.line([(0, i), (W, i)], fill=(int(12 + 30 * t), int(20 + 26 * t), int(12 + 14 * t)))
# amber glow blob (pheromone) + green network strokes
for r, a in [(150, 40), (110, 70), (70, 110)]:
    d.ellipse([W - 260 - r, H // 2 - r, W - 260 + r, H // 2 + r],
              outline=(200 + a // 4, 140, 40), width=3)
d.line([(60, 350), (300, 280), (520, 320), (700, 210)], fill=(55, 200, 90), width=6)
d.line([(300, 280), (420, 170)], fill=(55, 200, 90), width=5)
for x, y in [(700, 210), (420, 170), (1020 - 260 + 150, H // 2)]:
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(25, 194, 220))
try:
    f_big = ImageFont.truetype("arial.ttf", 92)
    f_mid = ImageFont.truetype("arial.ttf", 34)
    f_sm = ImageFont.truetype("arial.ttf", 26)
except OSError:
    f_big = f_mid = f_sm = ImageFont.load_default()
d.text((70, 60), "MYCO-SWARM", font=f_big, fill=(255, 213, 79))
d.text((72, 170), "Synthetic bacterial–fungal symbiosis for in-situ", font=f_mid, fill=(230, 230, 220))
d.text((72, 212), "microplastic sequestration — proven in silico.", font=f_mid, fill=(230, 230, 220))
chips = [("11–33x", "faster capture"), ("100%", "completeness"), ("0%", "bacteria retain")]
x = 72
for val, lbl in chips:
    d.rounded_rectangle([x, 280, x + 200, 360], radius=14, outline=(255, 213, 79), width=2)
    d.text((x + 100, 296), val, font=f_mid, fill=(255, 213, 79), anchor="mm")
    d.text((x + 100, 332), lbl, font=f_sm, fill=(200, 200, 190), anchor="mm")
    x += 224
img.save("assets/banner.png")
print("banner written")
