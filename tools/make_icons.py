"""Generates all Android launcher icons from assets-src/icon-source.jpg.
Run:  pip install Pillow numpy && python3 tools/make_icons.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "app", "src", "main", "res")
src = Image.open(os.path.join(ROOT, "assets-src", "icon-source.jpg")).convert("RGB")
W, H = src.size

DENS = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}

def save(img, folder, name):
    d = os.path.join(RES, folder)
    os.makedirs(d, exist_ok=True)
    img.save(os.path.join(d, name), optimize=True)

# ---- legacy icons (rounded square + round) ----
inset = 3
sq = src.crop((inset, inset, W - inset, H - inset)).resize((512, 512), Image.LANCZOS)

def masked(size, shape):
    big = sq.resize((size * 4, size * 4), Image.LANCZOS)
    mask = Image.new("L", big.size, 0)
    dr = ImageDraw.Draw(mask)
    if shape == "round":
        dr.ellipse((0, 0, big.size[0] - 1, big.size[1] - 1), fill=255)
    else:
        r = int(big.size[0] * 0.22)
        dr.rounded_rectangle((0, 0, big.size[0] - 1, big.size[1] - 1), radius=r, fill=255)
    out = big.convert("RGBA")
    out.putalpha(mask)
    return out.resize((size, size), Image.LANCZOS)

for d, s in DENS.items():
    px = int(48 * s)
    save(masked(px, "square"), f"mipmap-{d}", "ic_launcher.png")
    save(masked(px, "round"), f"mipmap-{d}", "ic_launcher_round.png")

# ---- adaptive icon layers ----
# foreground = the full rounded-square artwork filling the 72dp visible area,
# background = flat colour averaged from the artwork's edge (only visible if a launcher
# mask is larger than the artwork's rounded corners).
a = np.array(src).astype(float)
edge = np.concatenate([a[20:40, 60:-60].reshape(-1, 3), a[-40:-20, 60:-60].reshape(-1, 3),
                       a[60:-60, 20:40].reshape(-1, 3), a[60:-60, -40:-20].reshape(-1, 3)])
BG = tuple(int(v) for v in edge.mean(0))

def background(px):
    return Image.new("RGB", (px, px), BG)

def foreground(px):
    vis = int(px * 96 / 108)
    art = masked(vis, "square")
    out = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    off = (px - vis) // 2
    out.paste(art, (off, off), art)
    return out

for d, s in DENS.items():
    px = int(108 * s)
    save(background(px), f"mipmap-{d}", "ic_launcher_background.png")
    save(foreground(px), f"mipmap-{d}", "ic_launcher_foreground.png")

# 512 icon for store / README previews
sq.convert("RGBA").save(os.path.join(ROOT, "assets-src", "icon-512.png"))
print("done")
