#!/usr/bin/env python3
"""Render the news-summary image for 21 November 2026.

Draws a 1024x1024 newspaper-style front page with the day's six biggest
stories plus an in-brief strip, and writes it to entry.png beside this file.
Deterministic: no network, no clock, no randomness -- the same input always
produces the same bytes. Run: python3 render.py

Stories (all reported on Saturday 21 November 2026):
  1. Russia's largest attack of the year on Ukraine; missiles land in Poland
  2. ICJ finds Myanmar responsible for genocide against the Rohingya
  3. AI sell-off pushes the S&P 500 and Nasdaq into correction
  4. COP31 climate talks run past deadline, deadlocked over fossil fuels
  5. UK and EU sign their biggest post-Brexit agreements
  6. Magnitude 6.8 earthquake shakes Peru's Andes
In brief: "El Chapo Isidro" captured in Mexico; pancreatic-cancer pill trial;
Houthi missiles at Riyadh intercepted a third night running.
Sources: BBC, CNN, France 24, FT, Al Jazeera, El Pais, Reuters.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (185, 28, 28)
MUTED = (90, 86, 76)
CARD = (255, 255, 255)
LINE = (210, 204, 190)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "..."
    return lines


def draw_card(draw, x, y, w, h, tag, tag_color, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=LINE, width=2)
    pad = 16
    tx = x + pad
    ty = y + 14
    draw.text((tx, ty), tag, font=font(BOLD, 16), fill=tag_color)
    ty += 26
    hl = fit_lines(draw, headline, font(BOLD, 24), w - 2 * pad, 3)
    for ln in hl:
        draw.text((tx, ty), ln, font=font(BOLD, 24), fill=INK)
        ty += 29
    ty += 2
    bl = fit_lines(draw, body, font(REG, 18), w - 2 * pad, 4)
    for ln in bl:
        draw.text((tx, ty), ln, font=font(REG, 18), fill=MUTED)
        ty += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((28, 16), "THE WORLD IN ONE IMAGE",
           font=font(BOLD, 52), fill=(255, 255, 255))
    d.text((28, 78), "SATURDAY 21 NOVEMBER 2026  ·  SIX STORIES, ONE DAY",
           font=font(BOLD, 20), fill=(197, 205, 224))
    d.rectangle([0, 118, W, 122], fill=RED)

    # --- Lead story ---
    lx, ly, lw, lh = 28, 138, 968, 196
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly + 10, lx + 10, ly + lh - 10], fill=RED)
    tx = lx + 28
    ty = ly + 16
    d.text((tx, ty), "CONFLICT  ·  UKRAINE / POLAND", font=font(BOLD, 19),
           fill=RED)
    ty += 30
    lead_head = ("Russia's biggest attack of the year: 400+ drones and "
                 "110 missiles hit Ukraine")
    for ln in fit_lines(d, lead_head, font(BOLD, 33), lw - 56, 2):
        d.text((tx, ty), ln, font=font(BOLD, 33), fill=INK)
        ty += 40
    ty += 4
    lead_body = ("Two missiles and a suspected drone came down in Poland. "
                 "At least eight people were killed in Kyiv, and Warsaw "
                 "called the incursion a deliberate provocation.")
    for ln in fit_lines(d, lead_body, font(REG, 21), lw - 56, 2):
        d.text((tx, ty), ln, font=font(REG, 21), fill=MUTED)
        ty += 27

    # --- Story grid: 2 rows x 3 cards ---
    cards = [
        ("JUSTICE", (109, 40, 217),
         "ICJ: Myanmar guilty of Rohingya genocide",
         "The World Court finds Myanmar responsible for genocide "
         "against the Rohingya in a landmark ruling."),
        ("MARKETS", (22, 101, 52),
         "AI sell-off drags S&P 500 into correction",
         "US stocks plunge as AI shares slide; the Nasdaq wipes out "
         "all of its 2026 gains in tech's worst week since Covid."),
        ("CLIMATE", (15, 118, 110),
         "COP31 deadlocked over fossil fuels",
         "Climate talks in Antalya run past deadline as nearly 200 "
         "nations fail to agree; the summit is extended."),
        ("POLITICS", (29, 78, 216),
         "UK and EU sign biggest post-Brexit deal",
         "Three pacts on food trade, carbon markets and youth "
         "mobility; 100,000 young Britons gain EU access."),
        ("DISASTER", (194, 65, 12),
         "Magnitude 6.8 quake shakes Peru's Andes",
         "The tremor is felt in Lima, sending residents into the "
         "streets; no casualties reported."),
        ("CRIME", (124, 45, 18),
         "\u201cEl Chapo Isidro\u201d captured in Mexico",
         "FBI most-wanted cartel boss Fausto Isidro Meza Flores is "
         "reportedly seized in Sinaloa after gunfights."),
    ]
    cw, ch, gap = 313, 214, 14
    gx, gy = 28, 350
    for i, (tag, color, head, body) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, tag, color, head, body)

    # --- In brief strip ---
    by = 806
    d.rounded_rectangle([28, by, 996, by + 118], radius=10,
                        fill=NAVY, outline=NAVY)
    d.text((48, by + 12), "IN BRIEF", font=font(BOLD, 18),
           fill=(252, 211, 77))
    briefs = [
        ("Cancer hope: ", "a trial pill makes tumours undetectable "
         "in 1 in 12 pancreatic-cancer patients."),
        ("Riyadh: ", "Houthi missiles intercepted for a third "
         "straight night by the Saudi-led coalition."),
        ("Cyber: ", "the FBI and the US Department of Agriculture "
         "are hit by cyberattacks amid US outages."),
    ]
    bw = (968 - 40) // 3
    for i, (lead, rest) in enumerate(briefs):
        bx = 48 + i * bw
        lines = fit_lines(d, lead + rest, font(REG, 17), bw - 24, 4)
        ty = by + 40
        for j, ln in enumerate(lines):
            fnt = font(BOLD, 17) if j == 0 else font(REG, 17)
            d.text((bx, ty), ln, font=fnt, fill=(255, 255, 255))
            ty += 22

    # --- Footer: sources ---
    footer = ("Sources: BBC  ·  CNN  ·  France 24  ·  FT  ·  Al Jazeera  ·  "
              "El Pa\u00eds  ·  Reuters   —   21 November 2026")
    fw = d.textlength(footer, font=font(REG, 15))
    d.text(((W - fw) / 2, 946), footer, font=font(REG, 15), fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
