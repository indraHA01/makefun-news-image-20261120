#!/usr/bin/env python3
"""Render the 20 Nov 2026 world-news front page (1024x1024) with PIL.
Pure vector-style editorial drawing: crisp text, no AI artefacts, deterministic.
Run: python3 render.py  ->  entry.png (in cwd)
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
RULE = (150, 145, 130)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, fill, max_w, leading):
    for line in text_wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y

def headline(draw, x, y, text, font, fill, max_w, leading):
    for line in text_wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y

def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)

def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13], fill=(178, 34, 52))
    cw, ch = w * 0.4, h * 7 / 13
    draw.rectangle([x, y, x + cw, y + ch], fill=(30, 40, 90))
    for r in range(5):
        for c in range(6):
            sx = x + 8 + c * (cw - 14) / 5
            sy = y + 7 + r * (ch - 12) / 4
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))

def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=2)
    star(draw, x + w * 0.22, y + h * 0.30, h * 0.22, (255, 222, 0))
    for sx, sy in [(0.55, 0.14), (0.68, 0.28), (0.68, 0.48), (0.55, 0.62)]:
        star(draw, x + w * sx, y + h * sy, h * 0.08, (255, 222, 0))

def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))

# ---------- MASTHEAD ----------
d.rectangle([0, 0, W, 110], fill=NAVY)
d.text((28, 16), "THE WORLD TODAY", font=F(SERIF_B, 50), fill=(255, 255, 255))
d.text((28, 78), "ONE DAY IN ONE IMAGE", font=F(SANS_B, 15), fill=(212, 175, 55))
d.text((W - 28, 18), "FRIDAY", font=F(SERIF_B, 30), fill=(255, 255, 255), anchor="ra")
d.text((W - 28, 54), "20 NOVEMBER 2026", font=F(SANS_B, 22), fill=(255, 255, 255), anchor="ra")
d.text((W - 28, 84), "THE DAY'S WORLD NEWS", font=F(SANS_B, 12), fill=(200, 200, 200), anchor="ra")
d.rectangle([0, 110, W, 114], fill=GOLD)

# ---------- LEAD STORY: SHENZHEN SUMMIT ----------
d.text((28, 130), "SHENZHEN  ·  THE SUMMIT", font=F(SANS_B, 16), fill=RED)
headline(d, 28, 156, "TRUMP, XI AND PUTIN SIGN PEACE DECLARATION",
         F(SERIF_B, 50), INK, 968, 58)
para(d, 28, 282,
     "The leaders of the United States, China and Russia hold their first-ever three-way "
     "summit in Shenzhen and issue a four-point joint declaration.",
     F(SERIF, 20), (40, 40, 40), 968, 26)
fy, fw, fh, gap = 348, 300, 62, 34
flag_us(d, 28, fy, fw, fh)
flag_cn(d, 28 + fw + gap, fy, fw, fh)
flag_ru(d, 28 + 2 * (fw + gap), fy, fw, fh)
d.text((28, fy + fh + 6), "UNITED STATES", font=F(SANS_B, 13), fill=GREY)
d.text((28 + fw + gap, fy + fh + 6), "CHINA", font=F(SANS_B, 13), fill=GREY)
d.text((28 + 2 * (fw + gap), fy + fh + 6), "RUSSIA", font=F(SANS_B, 13), fill=GREY)
d.line([0, 448, W, 448], fill=RULE, width=2)

# ---------- PANELS: fixed zones (tag / headline / drawing / body) ----------
def panel(x, y0, y1, w, tag, head, body, draw_fn, head_size=28, body_size=16):
    d.rectangle([x, y0, x + w, y1], outline=RULE, width=2)
    d.text((x + 16, y0 + 10), tag, font=F(SANS_B, 14), fill=RED)
    hy = y0 + 34
    head_lines = text_wrap(d, head, F(SERIF_B, head_size), w - 32)
    for line in head_lines:
        d.text((x + 16, hy), line, font=F(SERIF_B, head_size), fill=INK)
        hy += head_size + 5
    body_lines = text_wrap(d, body, F(SERIF, body_size), w - 32)
    body_y = y1 - 8 - len(body_lines) * (body_size + 5)
    draw_fn(d, x + 16, hy + 6, w - 32, body_y - hy - 12)
    for line in body_lines:
        d.text((x + 16, body_y), line, font=F(SERIF, body_size), fill=(40, 40, 40))
        body_y += body_size + 5

def scales(draw, x, y, w, h):
    cx = x + w // 2
    top = y + 2
    pole_h = h - 8
    draw.line([cx, top, cx, top + pole_h], fill=INK, width=4)
    draw.line([cx - 52, top + 10, cx + 52, top + 10], fill=INK, width=3)
    for s in (-1, 1):
        px = cx + s * 52
        draw.line([px, top + 10, px - 20, top + 34], fill=INK, width=2)
        draw.line([px, top + 10, px + 20, top + 34], fill=INK, width=2)
        draw.arc([px - 22, top + 28, px + 22, top + 52], 0, 180, fill=INK, width=3)
    draw.ellipse([cx - 6, top - 4, cx + 6, top + 8], fill=GOLD)
    draw.rectangle([cx - 22, top + pole_h, cx + 22, top + pole_h + 5], fill=INK)

def skyline(draw, x, y, w, h):
    base = y + h
    heights = [0.55, 0.85, 0.45, 0.95, 0.6, 0.75, 0.4]
    bw = w / len(heights)
    for i, hf in enumerate(heights):
        bx = x + i * bw + 2
        bh = h * hf
        draw.rectangle([bx, base - bh, bx + bw - 4, base], fill=(35, 45, 70))
        for wy in range(int(base - bh + 6), int(base - 4), 12):
            for wx in range(int(bx + 4), int(bx + bw - 8), 11):
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    draw.line([x + 20, y + h * 0.35, x + 70, y + 2, x + 120, y + 10], fill=RED, width=3)
    draw.line([x + w - 20, y + h * 0.35, x + w - 70, y + 6, x + w - 120, y + 14], fill=RED, width=3)
    star(draw, x + 120, y + 10, 7, (255, 140, 0))
    star(draw, x + w - 120, y + 14, 7, (255, 140, 0))

def chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 245, 240), outline=RULE)
    pts = [(x + 8, y + h * 0.60), (x + w * 0.30, y + h * 0.30),
           (x + w * 0.45, y + h * 0.14), (x + w * 0.62, y + h * 0.42),
           (x + w * 0.80, y + h * 0.70), (x + w - 8, y + h * 0.86)]
    draw.line(pts[:3], fill=(30, 120, 60), width=4, joint="curve")
    draw.line(pts[2:], fill=RED, width=4, joint="curve")
    draw.polygon([(pts[2][0] - 7, pts[2][1] + 12), (pts[2][0] + 7, pts[2][1] + 12),
                  (pts[2][0], pts[2][1] - 2)], fill=(30, 120, 60))
    draw.polygon([(pts[-1][0] - 7, pts[-1][1] - 12), (pts[-1][0] + 7, pts[-1][1] - 12),
                  (pts[-1][0], pts[-1][1] + 2)], fill=RED)

def tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 33, 61))
    draw.rectangle([x + w * 0.64, y + h * 0.16, x + w * 0.86, y + h * 0.72], fill=(60, 70, 95))
    for i in range(3):
        draw.rectangle([x + w * 0.67, y + h * (0.24 + i * 0.16), x + w * 0.83, y + h * (0.32 + i * 0.16)],
                       fill=(255, 214, 90))
    star(draw, x + w * 0.75, y + h * 0.10, 9, (255, 140, 0))
    draw.polygon([(x + 6, y + h * 0.76), (x + w * 0.52, y + h * 0.76),
                  (x + w * 0.46, y + h * 0.94), (x + 14, y + h * 0.94)], fill=(150, 40, 40))
    for i in range(3):
        draw.rectangle([x + 12 + i * 30, y + h * 0.60, x + 36 + i * 30, y + h * 0.74],
                       fill=(212, 175, 55), outline=INK)

panel(28, 466, 716, 474, "THE HAGUE  ·  JUSTICE",
      "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
      "The ICJ rules Myanmar committed genocide against the Rohingya — a first for the court.",
      scales)
panel(522, 466, 716, 474, "UKRAINE  ·  WAR",
      "MISSILES HIT KYIV AS CRIMEA BRIDGE IS STRUCK AGAIN",
      "Ukraine hits the Kerch Bridge a third time in four days; Russian missiles strike Kyiv again on Friday.",
      skyline)
d.line([0, 734, W, 734], fill=RULE, width=2)

panel(28, 752, 950, 474, "MARKETS  ·  NEW YORK",
      "ANTHROPIC SOARS ON DEBUT — STOCKS SLIDE",
      "The AI firm's shares close 17% above their IPO price; the Nikkei falls 4.8% as US stocks drop a fifth day.",
      chart, head_size=25)
panel(522, 752, 950, 474, "THE GULF  ·  CONFLICT",
      "MISSILE HITS RIYADH TOWER; TANKER BURNS",
      "A Houthi missile damages Saudi Arabia's wealth-fund tower; a tanker hits a mine off Hormuz.",
      tanker, head_size=25)

# ---------- FOOTER TICKER ----------
d.rectangle([0, 968, W, H], fill=NAVY)
d.text((28, 986), "ALSO TODAY:  Kenya Ebola-free  ·  10,000 protest at Japan's Diet  ·  California subpoenas Nvidia  ·  Trump pardons Pete Rose",
       font=F(SANS_B, 12), fill=(255, 255, 255))

img.save("entry.png", optimize=True)
print("saved entry.png")
