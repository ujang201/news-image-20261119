#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday 19 November 2026.

A single 1024x1024 newspaper front page summing up the day's world news.
Rendered with Pillow only: no network, no downloaded assets, fully
deterministic — the same script always writes the same PNG bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (18, 18, 18)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, text, size=17):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 4


def headline(draw, x, y, text, size, width, leading=1.08):
    fnt = font(SERIF, size)
    return draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=leading)


def body(draw, x, y, text, size, width, leading=1.3):
    fnt = font(SERIF_REG, size)
    return draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=leading)


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def sunset_panel(draw, x, y, w, h):
    """A Vice City sunset: gradient sky, sun, skyline and palm silhouettes."""
    # sky gradient: deep orange -> pink -> purple
    top = (255, 122, 26)
    mid = (233, 84, 120)
    bot = (88, 48, 130)
    for yy in range(h):
        t = yy / max(h - 1, 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(top[i] + (mid[i] - top[i]) * u) for i in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * u) for i in range(3))
        draw.line([(x, y + yy), (x + w, y + yy)], fill=c)
    # sun
    cx, cy, r = x + int(w * 0.62), y + int(h * 0.42), 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 120))
    # skyline silhouettes, deterministic heights
    base = y + h
    heights = [0.42, 0.58, 0.34, 0.66, 0.48, 0.72, 0.38, 0.55, 0.62, 0.44]
    bw = w / len(heights)
    for i, frac in enumerate(heights):
        bx = x + int(i * bw)
        bh = int(h * frac)
        draw.rectangle([bx, base - bh, bx + int(bw) - 2, base], fill=(30, 16, 44))
        # tiny lit windows
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in (bx + 4, bx + 12):
                if (wx + wy) % 29 < 9:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
    # palm silhouettes
    for px, ph in ((x + 26, 74), (x + w - 52, 88)):
        draw.line([(px, base), (px + 8, base - ph)], fill=(24, 12, 36), width=5)
        for dx, dy in ((-26, -14), (-18, -26), (0, -30), (18, -26), (28, -14)):
            draw.line([(px + 8, base - ph), (px + 8 + dx, base - ph + dy)],
                      fill=(24, 12, 36), width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30  # side margin

    # --- masthead -------------------------------------------------------
    d.text((mx, 26), "MAKE.FUN  ·  NEWS-IMAGE", font=font(SANS_B, 15), fill=GREY)
    d.text((W - mx - 150, 26), "THURSDAY EDITION", font=font(SANS_B, 15), fill=GREY)
    rule(d, mx, 48, W - mx, 3)
    d.text((mx, 56), "THE WORLD TODAY", font=font(SERIF, 96), fill=INK)
    d.text((mx, 158), "T H U R S D A Y ,  1 9  N O V E M B E R  2 0 2 6",
           font=font(SANS_B, 24), fill=RED)
    rule(d, mx, 198, W - mx, 3)
    rule(d, mx, 204, W - mx, 1)

    # --- lead story: GTA VI --------------------------------------------
    ly = 222
    sunset_panel(d, 600, ly, 394, 238)
    d.text((600, ly + 244), "Vice City at dusk: Rockstar's sequel opens worldwide.",
           font=font(SERIF_IT, 15), fill=GREY)
    y = ly
    y = kicker(d, mx, y, "GAMES  ·  VICE CITY", 17)
    y = headline(d, mx, y, "Grand Theft Auto VI opens its doors", 44, 548)
    y += 6
    y = body(d, mx, y,
             "Rockstar's long-awaited sequel begins its global rollout, "
             "launching first in Australia at midnight with a 99 on "
             "Metacritic — the biggest entertainment launch of the year.",
             18, 548)
    rule(d, mx, 490, W - mx, 2)

    # --- middle: two columns --------------------------------------------
    col_y = 508
    col_w = 464
    # left column
    y = col_y
    y = kicker(d, mx, y, "THE GULF", 16)
    y = headline(d, mx, y, "U.S. and Iran trade fire as the war widens", 27, col_w)
    y += 4
    y = body(d, mx, y,
             "American jets hit a missile site on Iran's Qeshm Island after "
             "Tehran struck a U.S. radar base in Bahrain. Iran then attacked "
             "a U.S. base in Kuwait, and three U.S. carriers are now in the region.",
             16, col_w)
    y += 12
    rule(d, mx, y, mx + col_w, 1)
    y += 12
    y = kicker(d, mx, y, "BRUSSELS", 16)
    y = headline(d, mx, y, "EU plans a €45bn loan for Ukraine", 27, col_w)
    y += 4
    y = body(d, mx, y,
             "The Commission proposes borrowing on the markets to cover "
             "Kyiv's 2026 budget gap, repaid only once Russia agrees to pay "
             "war reparations.",
             16, col_w)

    # vertical divider
    d.line([(512, col_y), (512, 800)], fill=RULE, width=1)

    # right column
    x2 = 530
    y = col_y
    y = kicker(d, x2, y, "SHENZHEN  ·  APEC", 16)
    y = headline(d, x2, y, "Trump, Xi and Putin to meet three-way", 27, col_w)
    y += 4
    y = body(d, x2, y,
             "The three leaders hold trilateral talks today at the APEC "
             "summit in Shenzhen, with nuclear arms control and the Iran "
             "crisis at the top of the agenda.",
             16, col_w)
    y += 12
    rule(d, x2, y, x2 + col_w, 1)
    y += 12
    y = kicker(d, x2, y, "CHIPS", 16)
    y = headline(d, x2, y, "Nvidia's founder steps down; China chip sales halt", 27, col_w)
    y += 4
    y = body(d, x2, y,
             "Jensen Huang resigns as Nvidia's chief; acting CEO Colette "
             "Kress promises earlier pay rises. The firm also stops "
             "shipping H-series chips to mainland China.",
             16, col_w)

    rule(d, mx, 812, W - mx, 2)

    # --- lower pair ------------------------------------------------------
    y = 830
    y = kicker(d, mx, y, "THE HAGUE", 16)
    y = headline(d, mx, y, "World court to rule on Myanmar genocide case", 24, col_w)
    y += 4
    y = body(d, mx, y,
             "The International Court of Justice delivers its judgment "
             "today in The Gambia v. Myanmar, over the treatment of the "
             "Rohingya in Rakhine State.",
             15, col_w)

    y2 = 830
    y2 = kicker(d, x2, y2, "DEEP SPACE", 16)
    y2 = headline(d, x2, y2, "Voyager 1 reaches a light-day from Earth", 24, col_w)
    y2 += 4
    y2 = body(d, x2, y2,
              "After nearly 50 years in space, NASA's Voyager 1 probe is "
              "believed to have passed one light-day — about 26 billion "
              "kilometres — from home.",
              15, col_w)

    # --- ticker ----------------------------------------------------------
    ty = 946
    d.rectangle([mx, ty, W - mx, ty + 40], fill=INK)
    d.text((mx + 10, ty + 10),
           "ALSO TODAY:  Cyclone Akvan nears India's east coast  ·  Fed minutes signal more rate hikes  ·  Canada rethinks China ties",
           font=font(SANS_B, 15), fill=(251, 247, 238))
    d.text((mx, 996), "THE WORLD TODAY  ·  THURSDAY, 19 NOVEMBER 2026  ·  make.fun/news-image-20261119",
           font=font(SANS, 13), fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
