#!/usr/bin/env python3
"""THE GLOBAL DISPATCH — NI23 G4 compose script for akun5 (@edwinsaragih).

One-page broadsheet of Monday 23 November 2026, drawn with PIL (local only).
Fleet-style data layout (grid / NUMS / TL / BRIEFS / dc / PINS) so the margin
checker can read the source. All story data comes from the locked pool
ni23-pool.md; contested claims are framed as claims in the headlines.
Variant A: big lead, trio row, compact grid + ALSO rail on the right.
Variant B: two leads side by side, numbers/map/date-check rail on the right.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FDIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MAP_MODE = "dotted_map"

BG = (243, 233, 210)        # light sepia
INK = (90, 31, 31)          # maroon ink
INK2 = (60, 40, 34)
STEEL = (47, 93, 124)       # steel blue accent
GOLD = (176, 132, 52)
RED = (168, 44, 36)
GREY = (110, 96, 84)
CARD = (252, 247, 233)
LINE = (196, 172, 138)

REG_COL = {
    "MIDDLE EAST": (168, 84, 44),
    "EUROPE": (47, 93, 124),
    "NORTH AMERICA": (90, 31, 31),
    "SOUTH ASIA": (46, 120, 84),
    "SOUTHEAST ASIA": (128, 84, 160),
    "AFRICA": (196, 140, 40),
    "GLOBAL": (96, 96, 96),
    "ASIA-PACIFIC": (40, 140, 150),
}

REGION_COUNTS = [("SOUTH ASIA", 10), ("EUROPE", 9), ("NORTH AMERICA", 6),
                 ("MIDDLE EAST", 4), ("SOUTHEAST ASIA", 3), ("AFRICA", 2),
                 ("GLOBAL", 3), ("ASIA-PACIFIC", 1)]


def F(name, size):
    return ImageFont.truetype(FDIR + name, size)


def pf(size):
    return F("PlayfairDisplay-Black.ttf", size)


def pfb(size):
    return F("PlayfairDisplay-Bold.ttf", size)


def fb(size):   # headline font helper (fleet convention)
    return F("PlayfairDisplay-Bold.ttf", size)


def fr(size):   # deck font helper (fleet convention)
    return F("Archivo.ttf", size)


def fsr(size):  # brief font helper (fleet convention)
    return F("Archivo.ttf", size)


def ab(size):
    return F("Archivo-Bold.ttf", size)


def ar(size):
    return F("Archivo.ttf", size)


def tw(d, s, fnt):
    return d.textlength(s, font=fnt)


def wrap(d, s, fnt, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, fnt, maxw):
    if tw(d, s, fnt) <= maxw:
        return s
    while s and tw(d, s + "…", fnt) > maxw:
        s = s[:-1]
    return s.rstrip() + "…"


# ---------------------------------------------------------------- data
# grid tuples: (num, region, topic, src, head, deck, kind)
grid = [
    (4, "EUROPE", "KYIV, UKRAINE · WAR · RESCUE", "BBC, 23 Nov",
     "Boy, 7, Pulled Alive From Rubble",
     "Rescuers freed him after hours under debris in Kyiv; 6 people were killed in the Russian strike.",
     "rubble"),
    (5, "EUROPE", "KYIV REGION, UKRAINE · WAR · MISSING", "JagranJosh, 23 Nov",
     "Kyiv Strike: 14 Missing, Zelenskiy Says",
     "14 missing after a Russian drone hit a block in the Kyiv region, President Zelenskiy said.",
     "building"),
    (6, "MIDDLE EAST", "BAHRAIN, GULF · WAR · RADARS", "AP / AFP wires, 23 Nov",
     "IRGC Claims 2 Patriot Radars Hit",
     "Tehran says its forces destroyed two US Patriot radars at a base in Bahrain; no US confirmation.",
     "radar"),
    (7, "MIDDLE EAST", "STRAIT OF HORMUZ · WAR · SHIPPING", "AP live, 23 Nov",
     "Tankers Burn as Gulf War Widens",
     "Tankers were set ablaze in the strait as the Iran–US war spread; the IRGC warned of unrest. Burned, not sunk.",
     "ship"),
    (8, "EUROPE", "GULF OF FINLAND · SEA · ATTACK", "BBC, 23 Nov",
     "Russian Cargo Ship Still Burns",
     "The cargo ship still burns off Finland after an attack; a second Russia-bound vessel was towed in the Gulf.",
     "ship"),
    (9, "AFRICA", "BENGHAZI, LIBYA · SEA · BLAST", "BBC, 23 Nov",
     "Blast on Russian Ship at Benghazi",
     "An explosion hit a Russian vessel in Benghazi port; a suspected drone strike is reported as the cause.",
     "blast"),
    (10, "GLOBAL", "GENEVA, SWITZERLAND · TECH · WEAPONS", "SalonVision, 23 Nov",
     "UN Talks on Killer AI Go On",
     "States agree to keep negotiating rules for lethal autonomous weapons systems at the United Nations.",
     "chip"),
    (11, "SOUTHEAST ASIA", "THE HAGUE / MYANMAR · LAW · ICJ", "Guardian / NYT wires, 23 Nov",
     "ICJ: Myanmar Guilty of Genocide",
     "The World Court rules on the 2017 Rohingya campaign, in which more than 700,000 people fled.",
     "gavel"),
    (12, "NORTH AMERICA", "IOWA, USA · SAFETY · EXPLOSIVES", "BBC, 23 Nov",
     "Army to Detonate Explosives in Iowa",
     "The US Army will blow up tonnes of unstable explosives in Iowa, despite a court order against it.",
     "blast"),
    (13, "EUROPE", "TURIN, ITALY · SPORT · TENNIS", "BBC, 23 Nov",
     "Alcaraz Beats Zverev in Turin Final",
     "A first ATP Finals crown for Carlos Alcaraz, who beat Alexander Zverev in the Turin final.",
     "trophy"),
]

NUMS = [
    ("720/9d", "India's record Test total, card 1"),
    ("258-173", "US House split, card 3"),
    ("14", "missing near Kyiv, card 5"),
    ("$3,538", "gold per ounce, story 31"),
    ("28,000 cr", "Tata pipe sale, story 29"),
    ("65.9%", "IndiGo home share, story 30"),
]

TL = [
    ("00:02 UTC", "UN AI talks move on"),
    ("02:00 UTC", "Albanese on COP31"),
    ("MORNING", "Kyiv boy freed"),
    ("MIDDAY", "India 720/9 declared"),
    ("EVENING", "Alcaraz wins Turin"),
]

BRIEFS = [
    "14. Swimmer crosses Hormuz for Iran's wildlife",
    "15. Houthi ballistic missile on Saudi west intercepted",
    "16. US releases more UFO footage filmed over Middle East",
    "17. Albanese: COP31 failure shows 'hard geopolitics'",
    "18. UK–EU Brexit reset deal hailed as 'landmark'",
    "19. Thousands march in Lisbon over cost of living",
    "20. Myanmar junta calls ASEAN ruling 'unfair'",
    "21. Cameroon ex-rebels trapped by broken promises",
    "22. Escaped lion spreads fear in Türkiye",
    "23. Nepal PM Shah holds talks with Modi in Delhi",
    "24. Guru Nanak Jayanti marked across India",
    "25. Indonesia fire update: 7 bodies found, 50 missing",
    "26. India win ODI series in NZ 3–2; Phillips top player",
    "27. World Chess Championship captivates fans",
    "28. Kota pilgrim bus tragedy in Rajasthan: nine killed",
    "29. Tata Steel sells pipe unit for ₹28,000 crore",
    "30. SpiceJet audit plea; IndiGo holds 65.9% at home",
    "31. Gold slides to $3,538 an ounce, down from record",
    "32. Shah launches ₹4,000 cr infra push in Arunachal",
    "33. Google puts $5 million into IIT Kharagpur AI research",
    "34. India–EU free-trade pact likely signed 16 December",
    "35. Trump criticises Schumer amid Democrat reshuffle",
    "36. The FBI probes a hack of its justice database",
    "37. Miley Cyrus marries Maxx Morando in California",
    "38. Modi opens AI centre at IIT Patna, ₹400 cr projects",
]

dc = "Xi–Trump–Putin summit — 19 Nov 2026 · Russian missiles fall in Poland — 20 Nov 2026 · Hyderabad bomb-threat email — sent 21 Nov 2026 · Paolo Bulgari's death — reported 22 Nov 2026 · 24 civilians killed, South Sudan — 22 Nov 2026 · Kerch Bridge strike — reported 22 Nov 2026 · S. Korea minister quits — first reported 22 Nov 2026 · Indonesia candy-factory fire itself — 22 Nov 2026"

PINS = {  # card -> (lon, lat)
    1: (174, -41), 2: (30, 37), 3: (-77, 39), 4: (31, 50), 5: (29, 50),
    6: (50, 26), 7: (56, 27), 8: (25, 60), 9: (20, 32), 10: (6, 46),
    11: (96, 21), 12: (-93, 42), 13: (8, 45),
}


# ---------------------------------------------------------------- drawing
def icon(d, kind, x, y, s, col):
    import math
    cx, cy = x + s / 2, y + s / 2
    if kind == "cricket":
        d.line([x + s * .3, y + s * .75, x + s * .55, y + s * .2], fill=col, width=4)
        d.ellipse([x + s * .62, y + s * .55, x + s * .85, y + s * .78], fill=RED)
        d.line([x + s * .15, y + s * .85, x + s * .85, y + s * .85], fill=col, width=3)
    elif kind == "leaf":
        d.polygon([(cx, y + 4), (x + s - 4, cy), (cx, y + s - 4), (x + 4, cy)], outline=col, width=3)
        d.line([x + 6, y + s - 6, x + s - 6, y + 6], fill=col, width=2)
    elif kind == "ballot":
        d.rectangle([x + 5, cy - 4, x + s - 5, y + s - 5], outline=col, width=3)
        d.rectangle([x + s * .3, y + 4, x + s * .7, cy - 2], outline=col, width=3)
        d.line([x + s * .42, cy + 3, x + s * .58, cy + 3], fill=RED, width=3)
    elif kind == "rubble":
        d.polygon([(x + 4, y + s - 4), (cx, y + 8), (x + s - 4, y + s - 4)], outline=col, width=3)
        d.line([cx - 6, y + s - 12, cx + 8, y + s - 22], fill=RED, width=3)
        d.line([cx + 8, y + s - 22, cx + 2, y + s - 30], fill=RED, width=3)
    elif kind == "building":
        d.rectangle([x + 8, y + 6, x + s - 14, y + s - 4], outline=col, width=3)
        for r in range(3):
            for c in range(2):
                d.rectangle([x + 15 + c * 12, y + 13 + r * 11, x + 22 + c * 12, y + 19 + r * 11], fill=col)
        d.line([x + s - 12, y + 10, x + s - 4, y + s - 10], fill=RED, width=3)
    elif kind == "radar":
        d.arc([x + 4, y + 4, x + s - 4, y + s - 4], 200, 340, fill=col, width=3)
        d.arc([x + 12, y + 12, x + s - 12, y + s - 12], 200, 340, fill=col, width=2)
        d.line([cx, y + s - 4, cx, cy], fill=col, width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    elif kind == "ship":
        d.polygon([(x + 4, cy + 6), (x + s - 4, cy + 6), (x + s - 10, y + s - 6), (x + 10, y + s - 6)], outline=col, width=3)
        d.rectangle([cx - 8, cy - 8, cx + 6, cy + 6], outline=col, width=2)
        d.polygon([(cx - 2, cy - 22), (cx + 5, cy - 10), (cx - 6, cy - 10)], fill=RED)
        d.polygon([(cx + 6, cy - 18), (cx + 11, cy - 9), (cx + 2, cy - 9)], fill=GOLD)
    elif kind == "blast":
        for a in range(0, 360, 45):
            x2 = cx + (s * .42) * math.cos(math.radians(a))
            y2 = cy + (s * .42) * math.sin(math.radians(a))
            d.line([cx, cy, x2, y2], fill=RED if a % 90 else col, width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    elif kind == "chip":
        d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8], outline=col, width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=RED, width=2)
        for t in (0.2, 0.5, 0.8):
            d.line([x + s * t, y + 2, x + s * t, y + 8], fill=col, width=2)
            d.line([x + s * t, y + s - 8, x + s * t, y + s - 2], fill=col, width=2)
    elif kind == "gavel":
        d.line([x + 10, y + s - 10, x + s - 14, y + 12], fill=col, width=4)
        d.rectangle([x + s - 22, y + 4, x + s - 4, y + 16], fill=col)
        d.line([x + 6, y + s - 5, x + s * .55, y + s - 5], fill=RED, width=3)
    elif kind == "trophy":
        d.arc([x + 10, y + 4, x + s - 10, y + s * .6], 0, 180, fill=col, width=3)
        d.line([x + 10, cy, x + s - 10, cy], fill=col, width=3)
        d.line([cx, cy, cx, y + s - 10], fill=col, width=3)
        d.line([cx - 9, y + s - 6, cx + 9, y + s - 6], fill=RED, width=3)
    else:
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=col, width=3)


def chipbox(d, x, y, text, col):
    f = ab(11)
    w_ = tw(d, text, f) + 12
    d.rectangle([x, y, x + w_, y + 17], fill=col)
    d.text((x + 6, y + 2), text, font=f, fill=(255, 252, 240))
    return w_


def _big_card(d, x, y, w_, h, num, place, src, head, deck, kind, chip, cat,
              head_f, deck_f, icon_s):
    d.rectangle([x, y, x + w_, y + h], fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w_, y + 4], fill=STEEL)
    d.ellipse([x + 7, y + 10, x + 31, y + 34], fill=INK)
    nf = ab(13)
    d.text((x + 19 - tw(d, num, nf) / 2, y + 15), num, font=nf, fill=(255, 250, 235))
    d.text((x + 38, y + 12), fit(d, place, ab(12), w_ - 140), font=ab(12), fill=INK)
    chipbox(d, x + w_ - 92, y + 10, chip, STEEL)
    d.text((x + 38, y + 30), cat, font=ab(10), fill=GREY)
    icon(d, kind, x + 8, y + 44, icon_s, STEEL)
    tx = x + 22 + icon_s
    tw_max = x + w_ - tx - 8
    ly = y + 42
    for ln in wrap(d, head, head_f, tw_max)[:2]:
        d.text((tx, ly), ln, font=head_f, fill=INK2)
        ly += head_f.size + 5
    for ln in wrap(d, deck, deck_f, tw_max)[:2]:
        d.text((tx, ly), ln, font=deck_f, fill=(74, 58, 48))
        ly += deck_f.size + 4
    d.text((x + 10, y + h - 16), "Source: " + src, font=ab(10), fill=STEEL)


def lead(d, x, y, w_, h, num, place, src, head, deck, kind, chip, cat):
    _big_card(d, x, y, w_, h, num, place, src, head, deck, kind, chip, cat,
              fb(28), fr(13), 48)


def mini(d, x, y, w_, h, num, place, src, head, deck, kind, chip, cat):
    _big_card(d, x, y, w_, h, num, place, src, head, deck, kind, chip, cat,
              fb(22), fr(12), 42)


def grid_card(d, c, x, y, w_, h):
    num, region, topic, src, head, deck, kind = c
    d.rectangle([x, y, x + w_, y + h], fill=CARD, outline=LINE, width=1)
    col = REG_COL[region]
    d.rectangle([x, y, x + w_, y + 4], fill=col)
    d.ellipse([x + 6, y + 8, x + 28, y + 30], fill=INK)
    nf = ab(12)
    ns = str(num)
    d.text((x + 17 - tw(d, ns, nf) / 2, y + 13), ns, font=nf, fill=(255, 250, 235))
    d.text((x + 34, y + 10), fit(d, topic, ab(11), w_ - 130), font=ab(11), fill=INK)
    chip_t = {4: "REPORTED", 5: "ON RECORD", 6: "CLAIM", 7: "REPORTED",
              8: "ONGOING", 9: "REPORTED", 10: "OFFICIAL", 11: "OFFICIAL",
              12: "REPORTED", 13: "REPORTED"}[num]
    chipbox(d, x + w_ - 92, y + 9, chip_t, STEEL)
    s = "Src: " + src
    d.text((x + w_ - 8 - tw(d, s, ab(9)), y + 28), s, font=ab(9), fill=STEEL)
    icon(d, kind, x + 6, y + 28, 24, col)
    tf = fb(14)
    d.text((x + 36, y + 32), fit(d, head, tf, w_ - 44), font=tf, fill=INK2)
    d.text((x + 36, y + h - 13), fit(d, deck, fr(10), w_ - 44), font=fr(10), fill=(74, 58, 48))


def masthead(d, total, regions):
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((12, 5), "THE GLOBAL DISPATCH", font=ab(13), fill=(250, 240, 214))
    kick = "%d STORIES · %d REGIONS · EVERY ONE FROM 23 NOVEMBER 2026" % (total, regions)
    kf = ab(13)
    d.text((W - 12 - tw(d, kick, kf), 5), kick, font=kf, fill=(250, 240, 214))
    df = pf(68)
    date = "Monday 23 November 2026"
    d.text(((W - tw(d, date, df)) / 2, 30), date, font=df, fill=INK)
    nf = pf(32)
    name = "THE GLOBAL DISPATCH"
    d.text(((W - tw(d, name, nf)) / 2, 104), name, font=nf, fill=STEEL)
    sub = "India declare on a record 720/9 at Wellington  ·  COP31 ends without a deal  ·  Democrats take the US House 258–173"
    sf = ar(14)
    d.text(((W - tw(d, sub, sf)) / 2, 142), sub, font=sf, fill=INK2)
    d.line([12, 162, W - 12, 162], fill=INK, width=2)


def region_strip(d, y, counts):
    x = 12
    d.text((x, y + 3), "REGIONS:", font=ab(12), fill=INK)
    x += 74
    for reg, n in counts:
        col = REG_COL[reg]
        label = "%s %d" % (reg.title(), n)
        lf = ab(12)
        w_ = tw(d, label, lf) + 16
        d.rectangle([x, y, x + w_, y + 21], fill=col)
        d.text((x + 8, y + 4), label, font=lf, fill=(255, 252, 240))
        x += w_ + 6


def timeline(d, y):
    x = 12
    d.text((x, y + 3), "THE DAY (UTC):", font=ab(12), fill=INK)
    x += 108
    slotw = (W - 24 - 108) / len(TL)
    for t, ev in TL:
        d.rectangle([x, y, x + slotw - 6, y + 22], outline=STEEL, width=1)
        d.text((x + 6, y + 4), t, font=ab(11), fill=STEEL)
        ef = ar(10)
        d.text((x + 6 + tw(d, t, ab(11)) + 5, y + 5),
               fit(d, ev, ef, slotw - tw(d, t, ab(11)) - 18), font=ef, fill=INK2)
        x += slotw


def numbers_box(d, x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(238, 226, 198), outline=INK, width=2)
    d.text((x + 10, y + 7), "THE DAY IN NUMBERS", font=pfb(17), fill=INK)
    colw = (w_ - 20) / 3
    for i, (big, small) in enumerate(NUMS):
        cx = x + 10 + (i % 3) * colw
        cy = y + 32 + (i // 3) * ((h - 38) / 2)
        d.text((cx, cy), big, font=pf(22), fill=STEEL)
        d.text((cx, cy + 27), fit(d, small, ar(10), colw - 8), font=ar(10), fill=INK2)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 62),
     (-78, 58), (-85, 55), (-92, 57), (-95, 50), (-90, 45), (-85, 42), (-76, 40),
     (-74, 45), (-65, 45), (-60, 47), (-65, 50), (-75, 52), (-80, 55), (-85, 60),
     (-95, 62), (-105, 63), (-120, 64), (-140, 64), (-158, 58), (-168, 60)],
    [(-80, 45), (-75, 38), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 20), (-87, 21), (-86, 16), (-83, 9),
     (-79, 9), (-77, 7), (-80, 10), (-85, 12), (-90, 14), (-95, 16), (-102, 18),
     (-105, 22), (-110, 24), (-114, 29), (-117, 33), (-122, 37), (-124, 42),
     (-120, 45), (-110, 44), (-100, 42), (-90, 44), (-84, 45)],
    [(-78, 7), (-72, 11), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8),
     (-38, -14), (-40, -20), (-48, -26), (-55, -32), (-62, -38), (-65, -42),
     (-67, -50), (-68, -54), (-71, -50), (-73, -44), (-73, -36), (-71, -28),
     (-70, -20), (-75, -15), (-79, -8), (-80, -3), (-78, 2)],
    [(-10, 36), (-2, 37), (3, 42), (8, 44), (10, 44), (12, 42), (15, 40), (18, 40),
     (20, 42), (23, 40), (26, 38), (28, 41), (30, 46), (28, 48), (24, 52), (20, 54),
     (18, 56), (20, 58), (18, 60), (12, 56), (8, 55), (5, 53), (3, 52), (0, 51),
     (-2, 50), (-5, 48), (-2, 44), (-9, 43), (-9, 37)],
    [(-17, 15), (-10, 5), (-8, 4), (3, 6), (9, 4), (13, -2), (12, -10), (13, -18),
     (15, -27), (18, -33), (20, -35), (27, -34), (30, -30), (32, -26), (35, -22),
     (36, -18), (40, -12), (40, -5), (42, 0), (48, 5), (51, 10), (48, 12),
     (43, 12), (40, 15), (38, 20), (35, 24), (33, 27), (30, 31), (22, 33),
     (15, 32), (10, 34), (5, 36), (-2, 35), (-6, 34), (-10, 31), (-15, 25), (-17, 20)],
    [(-45, 60), (-40, 64), (-30, 68), (-22, 70), (-20, 68), (-28, 62), (-40, 58)],
    [(30, 36), (36, 36), (42, 37), (48, 38), (52, 40), (56, 42), (54, 46), (50, 50),
     (48, 54), (45, 58), (50, 62), (60, 64), (70, 66), (80, 66), (90, 68), (100, 68),
     (110, 66), (120, 68), (130, 66), (140, 64), (150, 62), (158, 60), (162, 64),
     (170, 66), (178, 65), (178, 60), (170, 55), (160, 52), (155, 50), (150, 45),
     (142, 42), (140, 38), (135, 35), (130, 32), (126, 34), (122, 30), (120, 25),
     (118, 20), (112, 16), (108, 12), (106, 8), (103, 2), (100, 6), (98, 12),
     (95, 16), (92, 16), (90, 22), (88, 21), (85, 19), (80, 15), (77, 8),
     (73, 16), (70, 20), (66, 25), (61, 25), (57, 26), (52, 26), (50, 24),
     (55, 24), (58, 22), (55, 17), (52, 15), (48, 14), (44, 12), (42, 15),
     (39, 20), (36, 28), (34, 31), (30, 36)],
    [(95, 5), (100, 0), (105, -3), (110, -5), (115, -8), (120, -10), (128, -10),
     (135, -12), (140, -18), (145, -22), (148, -28), (150, -32), (152, -35),
     (150, -38), (146, -39), (142, -38), (138, -35), (134, -33), (129, -32),
     (124, -33), (118, -35), (114, -33), (113, -26), (113, -22), (114, -16),
     (118, -12), (124, -10), (130, -8), (136, -6), (141, -4), (146, -6),
     (150, -9), (155, -10), (160, -12), (165, -14), (170, -16), (174, -18),
     (178, -20), (178, -26), (176, -30), (174, -35), (174, -38), (172, -41),
     (170, -44), (168, -46), (166, -45), (172, -40), (174, -37), (176, -38),
     (174, -41)],
    [(167, -45), (172, -41), (174, -37), (176, -38), (174, -41), (172, -43),
     (169, -46), (167, -45)],
]


def in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            xin = (x2 - x1) * (py - y1) / (y2 - y1) + x1
            if px < xin:
                inside = not inside
    return inside


def world_map(d, x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(238, 228, 202), outline=LINE, width=1)
    d.text((x + 8, y + 5), "WHERE THE STORIES ARE — pins = card numbers", font=ab(10), fill=INK)
    gx0, gy0 = x + 8, y + 24
    gw, gh = w_ - 16, h - 52
    lon = -170
    while lon <= 180:
        lat = -58
        while lat <= 82:
            if any(in_poly(lon, lat, p) for p in CONTINENTS):
                px = gx0 + (lon + 170) / 350 * gw
                py = gy0 + (82 - lat) / 140 * gh
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(178, 158, 120))
            lat += 4
        lon += 4
    for num, (lo, la) in PINS.items():
        px = gx0 + (lo + 170) / 350 * gw
        py = gy0 + (82 - la) / 140 * gh
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
        ns = str(num)
        nf = ab(9)
        d.text((px - tw(d, ns, nf) / 2, py - 5), ns, font=nf, fill=(255, 255, 255))
    d.text((x + 8, y + h - 22),
           "Dots mark the land; pins mark story numbers", font=ar(9), fill=INK2)


def datecheck_box(d, x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(250, 236, 224), outline=RED, width=2)
    d.text((x + 9, y + 5), "DATE CHECK — NOT 23 NOV, NOT NEWS HERE", font=ab(11), fill=RED)
    items = [s.strip() for s in dc.split("·")]
    step = (h - 26) / len(items)
    fs = 10 if h < 120 else 11
    for i, s in enumerate(items):
        d.text((x + 9, y + 24 + i * step), "✕ " + fit(d, s, ar(fs), w_ - 18), font=ar(fs), fill=INK2)


def footer_compact(d, y):
    d.line([12, y, W - 12, y], fill=INK, width=2)
    t1 = ("HOW SURE: REPORTED = a newsroom's own account · CLAIM = one side's account, "
          "labelled as such · ONGOING = still developing · OFFICIAL / ON RECORD = said by the body or person named.")
    for i, ln in enumerate(wrap(d, t1, ar(10), W - 24)):
        d.text((12, y + 4 + i * 12), ln, font=ar(10), fill=INK2)
    t2 = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. · Original drawings."
    d.text((12, y + 28), t2, font=ab(10), fill=INK)


def also_rail(d, x, y):
    d.text((x, y), "ALSO ON MONDAY", font=pfb(16), fill=INK)
    d.text((x, y + 22), "numbered on from the cards", font=ar(10), fill=GREY)
    bf = fsr(11)
    for i, b in enumerate(BRIEFS):
        cy = y + 38 + i * 11.8
        num, _, title = b.partition(". ")
        d.text((x, cy), num + ".", font=ab(11), fill=STEEL)
        off = tw(d, num + ".", ab(11)) + 4
        d.text((x + off, cy), fit(d, title, bf, 324 - off), font=bf, fill=INK2)


def also_block(d, x, y, w_, cols):
    d.text((x, y), "ALSO ON MONDAY — the rest of the day, numbered on from the cards", font=pfb(15), fill=INK)
    bf = fsr(11)
    colw = w_ / cols
    per = (len(BRIEFS) + cols - 1) // cols
    for i, b in enumerate(BRIEFS):
        cx = x + (i // per) * colw
        cy = y + 24 + (i % per) * 16
        num, _, title = b.partition(". ")
        d.text((cx, cy), num + ".", font=ab(11), fill=STEEL)
        off = tw(d, num + ".", ab(11)) + 4
        d.text((cx + off, cy), fit(d, title, bf, colw - off - 4), font=bf, fill=INK2)


def build(variant):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    total = 3 + len(grid) + len(BRIEFS)
    masthead(d, total, len(REGION_COUNTS))
    region_strip(d, 170, REGION_COUNTS)
    timeline(d, 198)
    if variant == "A":
        lead(d, 12, 228, 1000, 104, "1", "WELLINGTON, NEW ZEALAND",
             "ObserverVoice, 23 Nov",
             "India Declare on a Record 720/9 at Wellington",
             "The highest Test total ever made on New Zealand soil: 720 for nine, declared against the Black Caps.",
             "cricket", "REPORTED", "SPORT · CRICKET")
        mini(d, 12, 338, 494, 96, "2", "ANTALYA, TÜRKIYE",
             "BBC / AP, 23 Nov",
             "COP31 Ends Without a Deal",
             "Final draft omits 'fossil fuels'; COP31 ends in Antalya with no deal.",
             "leaf", "OFFICIAL", "CLIMATE · SUMMIT")
        mini(d, 518, 338, 494, 96, "3", "WASHINGTON, USA",
             "BBC, 23 Nov",
             "Democrats Take the House, 258–173",
             "Largest House majority since 1992, sealed by the North Carolina seat.",
             "ballot", "CONFIRMED", "POLITICS · HOUSE")
        for i, c in enumerate(grid):
            grid_card(d, c, 12 + (i % 2) * 338, 440 + (i // 2) * 66, 326, 62)
        also_rail(d, 688, 440)
        numbers_box(d, 12, 776, 470, 110)
        world_map(d, 490, 776, 250, 110)
        datecheck_box(d, 748, 776, 264, 110)
        footer_compact(d, 982)
    else:  # B: two leads on top, numbers + map + date-check rail on the right
        _big_card(d, 12, 228, 640, 104, "1", "WELLINGTON, NEW ZEALAND",
                  "ObserverVoice, 23 Nov",
                  "India Declare on a Record 720/9 at Wellington",
                  "The highest Test total ever made on New Zealand soil: 720 for nine, declared against the Black Caps.",
                  "cricket", "REPORTED", "SPORT · CRICKET", fb(26), fr(13), 48)
        _big_card(d, 660, 228, 352, 104, "2", "ANTALYA, TÜRKIYE",
                  "BBC / AP, 23 Nov",
                  "COP31 Ends Without a Deal",
                  "Final draft omits 'fossil fuels'; COP31 ends in Antalya with no deal.",
                  "leaf", "OFFICIAL", "CLIMATE · SUMMIT", fb(20), fr(12), 40)
        _big_card(d, 12, 338, 1000, 96, "3", "WASHINGTON, USA",
                  "BBC, 23 Nov",
                  "Democrats Take the House, 258–173",
                  "Largest House majority since 1992, sealed by the North Carolina seat.",
                  "ballot", "CONFIRMED", "POLITICS · HOUSE", fb(22), fr(12), 42)
        for i, c in enumerate(grid):
            grid_card(d, c, 12 + (i % 2) * 338, 440 + (i // 2) * 66, 326, 62)
        numbers_box(d, 688, 440, 324, 140)
        world_map(d, 688, 586, 324, 120)
        datecheck_box(d, 688, 712, 324, 150)
        also_block(d, 12, 776, 664, 3)
        footer_compact(d, 982)
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun5-%s.png" % variant
    img = build(variant)
    # flat-palette quantize: keeps the page crisp and the file small (ties -> smaller wins)
    img.convert("RGB").quantize(colors=192, method=Image.MEDIANCUT,
                                dither=Image.NONE).save(out, optimize=True)
    print("saved", out)
