# news-image-20261123 entry — "THE MONDAY WORLD" broadsheet, 1024x1024.
# Draws the front page for Monday 23 November 2026 from code (Pillow + system
# fonts) and writes entry.png beside this file. Deterministic: no clock, no
# randomness, no network — the same bytes every run.
# 35 verified stories (every one happened or was first reported on 23 Nov 2026),
# 7 regions, 3 drawn hero panels, a dotted world map, a DATE CHECK box.

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (247, 243, 232)
INK = (20, 20, 20)
SOFT_INK = (70, 70, 70)
RULE = (160, 150, 130)
RED = (178, 34, 34)
GREEN = (34, 120, 60)

# One accent colour per region band, in band order.
REGIONS = [
    ("EUROPE", (31, 78, 121)),
    ("MIDDLE EAST", (179, 84, 30)),
    ("ASIA-PACIFIC", (46, 125, 50)),
    ("AFRICA", (160, 110, 0)),
    ("AMERICAS", (106, 27, 154)),
    ("MARKETS & TECH", (0, 105, 92)),
    ("SCIENCE, SPORT & CULTURE", (173, 20, 87)),
]

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_check(d, text, f, max_w, tag):
    """Warn (stdout) when a one-line story is too wide for its column."""
    w = d.textlength(text, font=f)
    if w > max_w:
        print("OVERFLOW %s: %.0fpx > %.0fpx :: %s" % (tag, w, max_w, text))
    return w <= max_w


# ---------------------------------------------------------------- icons
# Tiny 12x12 pictograms, drawn in the band colour. Each story gets one.

def _star(d, x, y, c):
    d.polygon([(x + 6, y), (x + 8, y + 4), (x + 12, y + 6), (x + 8, y + 8),
               (x + 6, y + 12), (x + 4, y + 8), (x, y + 6), (x + 4, y + 4)],
              fill=c)


def _bank(d, x, y, c):
    d.polygon([(x, y + 4), (x + 6, y), (x + 12, y + 4)], fill=c)
    for i in range(3):
        d.rectangle([x + 1 + i * 4, y + 5, x + 3 + i * 4, y + 10], fill=c)
    d.rectangle([x, y + 11, x + 12, y + 12], fill=c)


def _plane(d, x, y, c):
    d.polygon([(x + 1, y + 7), (x + 6, y + 2), (x + 8, y + 6), (x + 12, y + 7),
               (x + 8, y + 8), (x + 6, y + 11), (x + 4, y + 8)], fill=c)


def _flame(d, x, y, c):
    d.polygon([(x + 6, y), (x + 9, y + 4), (x + 11, y + 8), (x + 8, y + 12),
               (x + 4, y + 12), (x + 1, y + 8), (x + 3, y + 4)], fill=c)


def _cross(d, x, y, c):
    d.rectangle([x + 5, y, x + 7, y + 12], fill=c)
    d.rectangle([x, y + 4, x + 12, y + 6], fill=c)


def _person(d, x, y, c):
    d.ellipse([x + 4, y, x + 8, y + 4], fill=c)
    d.polygon([(x + 6, y + 5), (x + 11, y + 12), (x + 1, y + 12)], fill=c)


def _ship(d, x, y, c):
    d.polygon([(x, y + 6), (x + 12, y + 6), (x + 10, y + 11), (x + 2, y + 11)],
              fill=c)
    d.rectangle([x + 5, y + 1, x + 7, y + 6], fill=c)


def _rocket(d, x, y, c):
    d.polygon([(x + 6, y), (x + 9, y + 5), (x + 8, y + 9), (x + 4, y + 9),
               (x + 3, y + 5)], fill=c)
    d.polygon([(x + 4, y + 9), (x + 6, y + 12), (x + 8, y + 9)], fill=c)


def _drop(d, x, y, c):
    d.polygon([(x + 6, y), (x + 11, y + 7), (x + 6, y + 12), (x + 1, y + 7)],
              fill=c)


def _chip(d, x, y, c):
    d.rectangle([x + 2, y + 2, x + 10, y + 10], outline=c, width=2)
    for i in range(3):
        d.line([x + 3 + i * 3, y, x + 3 + i * 3, y + 2], fill=c, width=1)
        d.line([x + 3 + i * 3, y + 10, x + 3 + i * 3, y + 12], fill=c, width=1)
    d.rectangle([x + 5, y + 5, x + 7, y + 7], fill=c)


def _chart(d, x, y, c):
    d.line([x, y + 10, x + 4, y + 7, x + 7, y + 8, x + 12, y + 2], fill=c,
           width=2)
    d.polygon([(x + 12, y + 2), (x + 9, y + 2), (x + 12, y + 5)], fill=c)


def _ball(d, x, y, c):
    d.ellipse([x + 1, y + 1, x + 11, y + 11], outline=c, width=2)
    d.line([x + 6, y + 1, x + 6, y + 11], fill=c, width=1)
    d.line([x + 1, y + 6, x + 11, y + 6], fill=c, width=1)


def _paw(d, x, y, c):
    d.ellipse([x + 4, y + 6, x + 8, y + 10], fill=c)
    for dx, dy in [(1, 1), (5, 0), (9, 1)]:
        d.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=c)


def _shield(d, x, y, c):
    d.polygon([(x + 1, y + 1), (x + 11, y + 1), (x + 11, y + 7),
               (x + 6, y + 12), (x + 1, y + 7)], outline=c, width=2)


def _bolt(d, x, y, c):
    d.polygon([(x + 7, y), (x + 3, y + 7), (x + 6, y + 7), (x + 5, y + 12),
               (x + 9, y + 5), (x + 6, y + 5)], fill=c)


def _globe(d, x, y, c):
    d.ellipse([x + 1, y + 1, x + 11, y + 11], outline=c, width=1)
    d.line([x + 6, y + 1, x + 6, y + 11], fill=c, width=1)
    d.line([x + 1, y + 6, x + 11, y + 6], fill=c, width=1)


ICONS = {
    "star": _star, "bank": _bank, "plane": _plane, "flame": _flame,
    "cross": _cross, "person": _person, "ship": _ship, "rocket": _rocket,
    "drop": _drop, "chip": _chip, "chart": _chart, "ball": _ball,
    "paw": _paw, "shield": _shield, "bolt": _bolt, "globe": _globe,
}


def draw_icon(d, kind, x, y, colour):
    fn = ICONS.get(kind, _star)
    fn(d, x, y, colour)


# ------------------------------------------------------- hero illustrations
# Each hero panel gets one bold vector scene drawn from primitives.

def hero_cop31(d, x, y, w, h):
    """Gavel + empty conference chairs + globe: a summit that agreed nothing."""
    # globe, upper left
    cx, cy, r = x + 52, y + 48, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=INK,
          width=2)
    # three empty chairs in profile (vertical back, seat, two legs), right
    for cx2 in (x + w - 122, x + w - 82, x + w - 42):
        d.rectangle([cx2, y + 26, cx2 + 5, y + 62], fill=INK)
        d.rectangle([cx2, y + 62, cx2 + 28, y + 68], fill=INK)
        d.rectangle([cx2 + 2, y + 68, cx2 + 6, y + 96], fill=INK)
        d.rectangle([cx2 + 22, y + 68, cx2 + 26, y + 96], fill=INK)
    # gavel striking its block, centre bottom
    d.polygon([(x + 96, y + 88), (x + 156, y + 68), (x + 166, y + 84),
               (x + 106, y + 104)], fill=RED)
    d.line([x + 106, y + 104, x + 76, y + 114], fill=INK, width=6)
    d.rectangle([x + 60, y + 112, x + 120, y + 118], fill=INK)


def hero_merkury(d, x, y, w, h):
    """A listing warship under drone attack, on a rough sea."""
    # sea
    for i in range(4):
        yy = y + h - 34 + i * 9
        d.arc([x + 8 + i * 40, yy - 8, x + 58 + i * 40, yy + 8], 180, 360,
              fill=(31, 78, 121), width=2)
    # hull, listing to starboard
    d.polygon([(x + 30, y + 62), (x + w - 30, y + 78), (x + w - 52, y + 104),
               (x + 52, y + 104)], fill=INK)
    d.rectangle([x + 96, y + 34, x + 118, y + 66], fill=INK)
    d.rectangle([x + 150, y + 44, x + 164, y + 70], fill=INK)
    d.line([x + 30, y + 62, x + w - 30, y + 78], fill=RED, width=3)
    # smoke from the strike
    d.ellipse([x + 168, y + 8, x + 196, y + 34], fill=(215, 208, 195),
              outline=SOFT_INK, width=2)
    d.ellipse([x + 186, y + 2, x + 206, y + 20], fill=(215, 208, 195),
              outline=SOFT_INK, width=2)
    # naval drones overhead
    for dx, dy in ((x + 52, y + 8), (x + 110, y + 18), (x + 228, y + 14)):
        d.ellipse([dx, dy, dx + 16, dy + 6], fill=INK)
        d.line([dx - 4, dy + 2, dx + 20, dy + 2], fill=INK, width=2)
        d.line([dx + 8, dy + 6, dx + 8, dy + 12], fill=INK, width=2)


def hero_nvidia(d, x, y, w, h):
    """A green chart arrow climbing off a generic chip: the CEO is back."""
    # chip, lower left
    cx, cy = x + 56, y + 78
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], outline=INK, width=3)
    for i in range(4):
        d.line([cx - 18 + i * 12, cy - 34, cx - 18 + i * 12, cy - 26],
               fill=INK, width=2)
        d.line([cx - 18 + i * 12, cy + 26, cx - 18 + i * 12, cy + 34],
               fill=INK, width=2)
        d.line([cx - 34, cy - 18 + i * 12, cx - 26, cy - 18 + i * 12],
               fill=INK, width=2)
        d.line([cx + 26, cy - 18 + i * 12, cx + 34, cy - 18 + i * 12],
               fill=INK, width=2)
    d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], fill=INK)
    # rising arrow, upper right
    pts = [(x + 110, y + 108), (x + 150, y + 84), (x + 180, y + 92),
           (x + 240, y + 40), (x + 272, y + 22)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    d.polygon([(x + 272, y + 22), (x + 246, y + 18), (x + 266, y + 44)],
              fill=GREEN)
    d.text((x + 236, y + 52), "+31.5%", font=font(SANS_B, 20), fill=GREEN)


# ------------------------------------------------------------ dotted map
# Continents as flattened ellipse blobs on a 128 x 30 dot grid; the grid is
# sampled so the map reads at a glance. Blobs are (cx, cy, rx, ry) in grid
# cells, latitude already compressed about 2:1.

MAP_BLOBS = [
    # North America
    (16, 7, 9, 4), (24, 9, 7, 3), (12, 11, 5, 3), (20, 13, 4, 3),
    # Greenland
    (31, 4, 3, 2),
    # South America
    (30, 18, 4, 3), (32, 22, 3, 4),
    # Europe
    (60, 7, 4, 3), (63, 9, 3, 2),
    # Africa
    (61, 14, 6, 4), (62, 19, 4, 4),
    # Asia
    (76, 7, 10, 4), (84, 10, 9, 4), (92, 13, 6, 3), (98, 16, 3, 2),
    # SE Asia / Indonesia
    (96, 18, 5, 2),
    # Australia
    (104, 21, 6, 3),
]

# Region pins: (grid x, grid y, number) — band order 1..7.
MAP_PINS = [
    (60, 8, "1"), (70, 12, "2"), (90, 12, "3"), (61, 17, "4"),
    (22, 11, "5"), (26, 9, "6"), (58, 6, "7"),
]


def draw_dotted_map(d, x0, y0, w, h):
    cols, rows = 128, 30
    sx, sy = w / cols, h / rows
    for gy in range(rows):
        for gx in range(cols):
            inside = False
            for (cx, cy, rx, ry) in MAP_BLOBS:
                if ((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1.0:
                    inside = True
                    break
            if inside:
                d.ellipse([x0 + gx * sx + 1, y0 + gy * sy + 1,
                           x0 + (gx + 1) * sx - 1, y0 + (gy + 1) * sy - 1],
                          fill=(120, 110, 95))
    for (gx, gy, num) in MAP_PINS:
        px, py = x0 + gx * sx, y0 + gy * sy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=CREAM, width=2)
        f = font(SANS_B, 11)
        tw = d.textlength(num, font=f)
        d.text((px - tw / 2, py - 6), num, font=f, fill=(255, 255, 255))


# -------------------------------------------------------------- story data
# (icon kind, one-line story). Every story happened or was first reported
# on Monday 23 November 2026. Heroes 1-3 are the three big panels above.

HEROES = [
    ("COP31", "COP31 ENDS WITH NO DEAL",
     "Antalya: longest COP ever; pact rejected over fossil fuels",
     hero_cop31),
    ("MERKURY", "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "7 naval drones hit corvette Merkury at Benghazi; Angara struck too",
     hero_merkury),
    ("NVIDIA", "HUANG BACK AS NVIDIA CEO",
     "Board reinstates Jensen Huang; shares surge 31.5%",
     hero_nvidia),
]

BANDS = [
    ("EUROPE", [
        ("star", "Russian strikes kill 15 in Kyiv region; boy, 7, freed after 14 hrs"),
        ("bank", "EU plans new Russia sanctions: 60 banks, 70 shadow-fleet ships"),
        ("plane", "Finland summons Russian envoy; Moscow warns Estonia of open war"),
        ("bolt", "Belgium airports shut for a day as controllers strike; 50,000 hit"),
        ("person", "Manchester arena evacuated after tear gas; 12,000 out, 50 assessed"),
    ]),
    ("MIDDLE EAST", [
        ("bank", "US sanctions Iran shadow banks: 2 dozen exchange houses hit"),
        ("shield", "Iran vows \u2018all means\u2019 to counter US blockade of Hormuz"),
        ("person", "Iran flogs singer Parastoo Ahmadi, 74 lashes, with 4 bandmates"),
        ("bolt", "Netanyahu urges Trump to strike Iran soon, Kan reports"),
        ("star", "Saudi strike on Yemen\u2019s Hodeida kills 4, wounds 18"),
    ]),
    ("ASIA-PACIFIC", [
        ("flame", "Indonesia candy factory fire: 24 dead, 29 of 65 missing"),
        ("bank", "India offers \u20ac1.4bn to help Nepal rebuild after floods"),
        ("person", "Kim stresses sovereignty after rebuffing Trump talks offer"),
        ("ship", "S. Korea: Gulf of Aden mission is not indirect war role"),
        ("rocket", "Pakistani pilot to fly to China\u2019s Tiangong on Shenzhou-24"),
    ]),
    ("AFRICA", [
        ("globe", "Kenya and DR Congo restore full diplomatic ties"),
        ("star", "Drones hit homes and a UN building in Khartoum"),
        ("cross", "WHO: fighting disrupts Ebola response in DRC"),
        ("shield", "Cameroon ex-rebels caught between hiding, broken vows"),
    ]),
    ("AMERICAS", [
        ("star", "Drones hit Colombian police base in Cucuta; 60 homes damaged"),
        ("plane", "Amtrak train derails in Louisiana; 5 hurt, 95 aboard"),
        ("person", "Nine shot at California concert; one critical"),
        ("bolt", "US Army to detonate 68 drums of lead azide in Iowa"),
        ("shield", "Soldiers shot in Sinaloa after Chapo Isidro capture; 8 held"),
    ]),
    ("MARKETS & TECH", [
        ("chart", "Bitcoin falls to ~$55,100, lowest since Sept 2024"),
        ("chart", "Asian tech shares fall further as AI sell-off deepens"),
        ("bank", "Euro area inflation rises to 4.0%"),
        ("chip", "OpenAI proposes shared AI safety limits for labs"),
    ]),
    ("SCIENCE, SPORT & CULTURE", [
        ("rocket", "BepiColombo enters Mercury orbit after 8-year trip"),
        ("cross", "NHS starts AI breast-cancer screening trial"),
        ("paw", "Lion on the loose near Istanbul; thermal cameras hunt it"),
        ("ball", "UK expected to host 2035 Women\u2019s World Cup"),
    ]),
]

TICKER = ("ALSO TODAY \u2014 Oil: Brent $89.37, down 3% \u2022 Poland: Russia "
          "\u2018tried to kill rapper Kyivstoner twice\u2019 \u2022 Istanbul: "
          "thousands rally vs crackdown \u2022 Gaza: 99% contaminated, "
          "Oxfam report")

DATE_CHECK = ("DATE CHECK \u2014 LEFT OUT (OTHER DAYS): Chapo Isidro captured "
              "Fri 21 Nov \u00b7 Riemann proof first reported Sat 22 Nov \u00b7 "
              "FBI database hack first reported Sat 22 Nov \u00b7 Peru quake "
              "Fri 21 Nov.")

FOOTER = ("Every story above happened or was first reported on "
          "Monday 23 November 2026.")


# ---------------------------------------------------------------- layout

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # --- masthead ------------------------------------------------------
    f_name = font(SERIF_B, 48)
    t = "THE MONDAY WORLD"
    d.text(((W - d.textlength(t, font=f_name)) / 2, 4), t, font=f_name,
           fill=INK)
    f_date = font(SERIF_B, 36)
    t = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(t, font=f_date)
    d.text(((W - tw) / 2, 56), t, font=f_date, fill=RED)
    d.line([mx, 100, (W - tw) / 2 - 14, 100], fill=RULE, width=2)
    d.line([(W + tw) / 2 + 14, 100, W - mx, 100], fill=RULE, width=2)

    # --- hero row ------------------------------------------------------
    hy, hh = 108, 232
    pw = (W - 2 * mx - 2 * 10) // 3
    f_tag = font(SANS_B, 12)
    f_head = font(SANS_B, 19)
    f_cap = font(SANS, 11)
    for i, (tag, head, cap, scene) in enumerate(HEROES):
        x = mx + i * (pw + 10)
        d.rectangle([x, hy, x + pw, hy + hh], outline=INK, width=2)
        d.rectangle([x, hy, x + pw, hy + 22], fill=INK)
        d.text((x + 8, hy + 4), tag, font=f_tag, fill=CREAM)
        scene(d, x + 6, hy + 28, pw - 12, 118)
        lines = wrap(d, head, f_head, pw - 16)
        yy = hy + 150
        for ln in lines[:2]:
            d.text((x + 8, yy), ln, font=f_head, fill=INK)
            yy += 23
        clines = wrap(d, cap, f_cap, pw - 16)
        cy = hy + hh - 30
        for ln in clines[:2]:
            d.text((x + 8, cy), ln, font=f_cap, fill=SOFT_INK)
            cy += 13

    # --- map strip -----------------------------------------------------
    my = 348
    f_kick = font(SANS_B, 13)
    kick = "THE WORLD IN ONE DAY \u2014 35 STORIES, 7 REGIONS"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, my), kick,
           font=f_kick, fill=INK)
    draw_dotted_map(d, 192, my + 20, 640, 126)
    d.text((28, my + 20), "1 EUROPE", font=font(SANS_B, 11), fill=REGIONS[0][1])
    d.text((28, my + 36), "2 MIDDLE EAST", font=font(SANS_B, 11),
           fill=REGIONS[1][1])
    d.text((28, my + 52), "3 ASIA-PACIFIC", font=font(SANS_B, 11),
           fill=REGIONS[2][1])
    d.text((28, my + 68), "4 AFRICA", font=font(SANS_B, 11), fill=REGIONS[3][1])
    d.text((848, my + 20), "5 AMERICAS", font=font(SANS_B, 11),
           fill=REGIONS[4][1])
    d.text((848, my + 36), "6 MARKETS & TECH", font=font(SANS_B, 11),
           fill=REGIONS[5][1])
    d.text((848, my + 52), "7 SCIENCE, SPORT", font=font(SANS_B, 11),
           fill=REGIONS[6][1])
    d.text((848, my + 68), "& CULTURE", font=font(SANS_B, 11),
           fill=REGIONS[6][1])

    # --- region bands --------------------------------------------------
    f_lab = font(SANS_B, 13)
    f_story = font(SANS, 11)
    y = 502
    col_w = 472
    for (label, colour), (_lab, stories) in zip(REGIONS, BANDS):
        rows = (len(stories) + 1) // 2
        band_h = 16 + rows * 13 + 4
        d.rectangle([mx, y, mx + 6, y + band_h], fill=colour)
        d.text((mx + 12, y), label, font=f_lab, fill=colour)
        d.line([mx, y + band_h - 1, W - mx, y + band_h - 1], fill=RULE,
               width=1)
        for j, (icon, text) in enumerate(stories):
            col = j % 2
            row = j // 2
            sx = mx + 12 + col * (col_w + 12)
            sy = y + 16 + row * 13
            draw_icon(d, icon, sx, sy + 1, colour)
            fit_check(d, text, f_story, col_w - 18, label)
            d.text((sx + 18, sy), text, font=f_story, fill=INK)
        y += band_h

    # --- date check ----------------------------------------------------
    y += 6
    d.rectangle([mx, y, W - mx, y + 56], outline=RED, width=2)
    f_dc = font(SANS_B, 12)
    d.text((mx + 10, y + 6), "DATE CHECK", font=f_dc, fill=RED)
    rest = DATE_CHECK.split(": ", 1)[1]
    for k, ln in enumerate(wrap(d, rest, font(SANS, 12), W - 2 * mx - 20)):
        d.text((mx + 10, y + 24 + k * 15), ln, font=font(SANS, 12), fill=INK)

    # --- ticker --------------------------------------------------------
    y += 64
    f_tick = font(SANS_B, 11)
    tlines = wrap(d, TICKER, f_tick, W - 2 * mx)
    for k, ln in enumerate(tlines[:2]):
        d.text((mx, y + k * 15), ln, font=f_tick, fill=INK)

    # --- footer --------------------------------------------------------
    f_foot = font(SERIF, 13)
    d.text(((W - d.textlength(FOOTER, font=f_foot)) / 2, H - 26), FOOTER,
           font=f_foot, fill=SOFT_INK)

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s %dx%d %d bytes" % (OUT, W, H, size))
    if size > 1048576:
        print("ERROR: over 1 MiB")
        sys.exit(1)


if __name__ == "__main__":
    main()
