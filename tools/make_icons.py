"""インクメモのアイコン（PNG）を作る。index.html の splatPath と同じ考え方でインクの形を描く。

使い方: python tools/make_icons.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "icons"
BG = (22, 17, 43)
YELLOW = (232, 255, 58)
PURPLE = (123, 75, 255)
PINK = (255, 62, 165)
SCALE = 4  # 大きく描いて縮小し、ふちをなめらかにする


def rng(seed):
    s = seed & 0xFFFFFFFF

    def nxt():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        return s / 4294967296

    return nxt


def splat(draw, seed, cx, cy, r, color):
    rand = rng(seed)
    n = 18
    pts = []
    for i in range(n):
        a = i / n * math.tau + rand() * 0.15
        rr = r * (0.6 + rand() * 0.15) if i % 2 else r * (0.92 + rand() * 0.38)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    # Catmull-Rom で輪郭をなめらかにつなぐ
    poly = []
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for t in [j / 16 for j in range(16)]:
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            poly.append((x, y))
    draw.polygon(poly, fill=color)
    for _ in range(5):
        a = rand() * math.tau
        dist = r * (1.25 + rand() * 0.45)
        rr = r * (0.06 + rand() * 0.14)
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist
        draw.ellipse((x - rr, y - rr, x + rr, y + rr), fill=color)


def font(size):
    for name in ("C:/Windows/Fonts/meiryob.ttc", "C:/Windows/Fonts/YuGothB.ttc", "C:/Windows/Fonts/msgothic.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def icon(size, safe=1.0, rounded=False):
    s = size * SCALE
    img = Image.new("RGBA", (s, s), BG + (255,))
    d = ImageDraw.Draw(img)
    c = s / 2
    k = s * safe
    splat(d, 21, c - k * 0.27, c + k * 0.28, k * 0.13, PINK)
    splat(d, 3, c + k * 0.28, c - k * 0.27, k * 0.12, PURPLE)
    splat(d, 7, c, c + k * 0.01, k * 0.3, YELLOW)
    f = font(int(k * 0.2))
    d.text((c, c + k * 0.02), "W-L", font=f, fill=BG, anchor="mm")
    img = img.resize((size, size), Image.LANCZOS)
    if rounded:
        mask = Image.new("L", (size * SCALE, size * SCALE), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * SCALE - 1, size * SCALE - 1), radius=size * SCALE * 0.22, fill=255)
        img.putalpha(mask.resize((size, size), Image.LANCZOS))
    return img


def main():
    OUT.mkdir(exist_ok=True)
    icon(192).save(OUT / "icon-192.png")
    icon(512).save(OUT / "icon-512.png")
    icon(512, safe=0.78).save(OUT / "icon-maskable-512.png")
    icon(180).convert("RGB").save(OUT / "apple-touch-icon.png")
    print("ok:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
