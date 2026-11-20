#!/usr/bin/env python3
"""Draws the Grim Void logo: a ring split by the word GRIM (red top arc, black bottom arc),
in the style of Void's logo. Writes logo.svg (for light backgrounds) and logo-dark.svg."""
import math, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT = "/usr/share/fonts/noto/NotoSans-BlackItalic.ttf"
RED, BLACK, WHITE = "#c1121f", "#0a0a0a", "#ececec"
C, R, W = 256, 178, 54            # ring centre, radius, stroke width
GAP = 70                           # half-height of the gap the word passes through
TEXT_W = 486                       # word width (a bit wider than the ring, like Void's)
EXTRA_SLANT = 8                    # degrees, on top of the italic

font = TTFont(FONT)
gs, cmap = font.getGlyphSet(), font.getBestCmap()
upm = font["head"].unitsPerEm

def word_path(word, transform):
    pen = SVGPathPen(gs)
    tp = TransformPen(pen, transform)
    x = 0
    hmtx = font["hmtx"]
    for ch in word:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(tp, (1, 0, 0, 1, x, 0)))
        x += hmtx[g][0] - 40          # slightly tighter letters
    return pen.getCommands(), x

# measure the word (font units, y up), then scale/slant/flip into the box
bp = BoundsPen(gs)
_, adv = word_path("GRIM", (1, 0, 0, 1, 0, 0))
x = 0
for ch in "GRIM":
    g = cmap[ord(ch)]; gs[g].draw(TransformPen(bp, (1, 0, 0, 1, x, 0))); x += font["hmtx"][g][0] - 40
x0, y0, x1, y1 = bp.bounds
k = math.tan(math.radians(EXTRA_SLANT))
s = TEXT_W / ((x1 - x0) + k * (y1 - y0))
h = (y1 - y0) * s
# x' = s*x + s*k*y + tx ; y' = -s*y + ty  (centre the word on the ring)
tx = C - TEXT_W / 2 - s * x0 - s * k * y0
ty = C + h / 2 + s * y0
word, _ = word_path("GRIM", (s, 0, s * k, -s, tx, ty))

def arc(a0, a1):
    p0 = (C + R * math.cos(math.radians(a0)), C + R * math.sin(math.radians(a0)))
    p1 = (C + R * math.cos(math.radians(a1)), C + R * math.sin(math.radians(a1)))
    return f"M{p0[0]:.2f} {p0[1]:.2f} A{R} {R} 0 0 1 {p1[0]:.2f} {p1[1]:.2f}"

t = math.degrees(math.asin(GAP / R))
top, bottom = arc(180 + t, 360 - t), arc(t, 180 - t)

def svg(text_fill, bottom_fill, outline=None):
    # a slightly wider grey arc underneath gives the black arc an edge on dark backgrounds
    edge = f'\n  <path d="{bottom}" fill="none" stroke="{outline}" stroke-width="{W + 6}"/>' if outline else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <title>Grim Void</title>
  <path d="{top}" fill="none" stroke="{RED}" stroke-width="{W}"/>
{edge}
  <path d="{bottom}" fill="none" stroke="{bottom_fill}" stroke-width="{W}"/>
  <path d="{word}" fill="{text_fill}"/>
</svg>
'''
out = sys.argv[1] if len(sys.argv) > 1 else "."
open(f"{out}/logo.svg", "w").write(svg(BLACK, BLACK))
# for dark backgrounds the black parts get a thin light edge so they still show
open(f"{out}/logo-dark.svg", "w").write(svg(WHITE, BLACK, outline="#5a5a5a"))
print("wrote logo.svg and logo-dark.svg")
