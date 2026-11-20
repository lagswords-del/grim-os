#!/usr/bin/env python3
"""Turns the Grim Void logo into terminal art for grimfetch (half blocks, 2 pixels per cell).
${c1} = red arc, ${c2} = the word GRIM, ${c3} = the black arc (shown as dark grey)."""
import subprocess, io, sys
from PIL import Image
W = int(sys.argv[1]) if len(sys.argv) > 1 else 38          # characters wide
png = subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(W), "logo-dark.svg"], capture_output=True).stdout
img = Image.open(io.BytesIO(png)).convert("RGBA")
def cls(p):
    r, g, b, a = p
    if a < 110: return 0
    if r > 150 and g < 90: return 1            # red
    if r > 160 and g > 160: return 2           # light text
    if r < 50 and g < 50: return 3             # black arc
    return 0                                    # grey edge -> background
rows = []
for y in range(0, W, 2):
    line, cur = "", None
    for x in range(W):
        t, b = cls(img.getpixel((x, y))), cls(img.getpixel((x, y + 1))) if y + 1 < W else 0
        if not t and not b: ch, c = " ", cur
        elif t and b: ch, c = "█", t if t == b else max(t, b, key=lambda v: (v == 2, v == 1))
        elif t: ch, c = "▀", t
        else: ch, c = "▄", b
        if ch != " " and c != cur:
            line += "${c%d}" % c; cur = c
        line += ch
    rows.append(line.rstrip())
while rows and not rows[0].strip(): rows.pop(0)
while rows and not rows[-1].strip(): rows.pop()
print("\n".join(rows))
