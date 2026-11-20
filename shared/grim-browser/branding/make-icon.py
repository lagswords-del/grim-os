#!/usr/bin/env python3
"""Grim Browser's icon: Iceraven's launcher icon (MPL-2.0, github.com/fork-maintainers/iceraven-browser,
app/src/forkRelease/res/drawable-v24/ic_launcher_foreground.xml) converted from an Android vector
drawable to SVG, with every blue/cyan recoloured to Grim red. Black, grey and white stay as they are.
    python3 make-icon.py   -> grim-browser.svg (+ PNGs if rsvg-convert is installed)"""
import colorsys, os, subprocess, xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
A = "{http://schemas.android.com/apk/res/android}"
AAPT = "{http://schemas.android.com/aapt}"
GRIM_HUE = 357 / 360          # #c1121f

def recolour(c):
    c = c.lstrip("#")
    alpha = ""
    if len(c) == 8:
        alpha, c = c[:2], c[2:]
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s > 0.15 and 0.40 < h < 0.75:          # the blues and cyans
        r, g, b = colorsys.hls_to_rgb(GRIM_HUE, min(l, 0.55), min(1, s * 1.05))
    out = "#%02x%02x%02x" % tuple(round(v * 255) for v in (r, g, b))
    op = int(alpha, 16) / 255 if alpha else 1
    return out, op

root = ET.parse(os.path.join(HERE, "iceraven-launcher-foreground.xml")).getroot()
vw, vh = root.get(A + "viewportWidth"), root.get(A + "viewportHeight")
defs, body, n = [], [], 0

def walk(node, out):
    global n
    for el in node:
        tag = el.tag
        if tag == "group":
            t = []
            tx, ty = el.get(A + "translateX"), el.get(A + "translateY")
            sx, sy = el.get(A + "scaleX"), el.get(A + "scaleY")
            if tx or ty: t.append(f"translate({tx or 0} {ty or 0})")
            if sx or sy: t.append(f"scale({sx or 1} {sy or sx or 1})")
            inner = []
            walk(el, inner)
            out.append(f'<g transform="{" ".join(t)}">' + "".join(inner) + "</g>")
        elif tag == "path":
            d = el.get(A + "pathData")
            fill, op = "none", 1
            if el.get(A + "fillColor"):
                fill, op = recolour(el.get(A + "fillColor"))
            grad = el.find(f"{AAPT}attr/gradient")
            if grad is not None:
                n += 1
                gid = f"g{n}"
                stops = "".join(
                    '<stop offset="{}" stop-color="{}" stop-opacity="{:.3f}"/>'.format(it.get(A + "offset"), *recolour(it.get(A + "color")))
                    for it in grad.findall("item"))
                if grad.get(A + "type") == "radial":
                    defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{grad.get(A + "centerX")}" '
                                f'cy="{grad.get(A + "centerY")}" r="{grad.get(A + "gradientRadius")}">{stops}</radialGradient>')
                else:
                    defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{grad.get(A + "startX")}" '
                                f'y1="{grad.get(A + "startY")}" x2="{grad.get(A + "endX")}" y2="{grad.get(A + "endY")}">{stops}</linearGradient>')
                fill, op = f"url(#{gid})", 1
            rule = "evenodd" if el.get(A + "fillType") == "evenOdd" else "nonzero"
            fa = el.get(A + "fillAlpha")
            if fa: op *= float(fa)
            out.append(f'<path d="{d}" fill="{fill}" fill-opacity="{op:.3f}" fill-rule="{rule}"/>')

walk(root, body)
# the launcher foreground has a safe-zone margin: crop to the middle 72x72 like Android does
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 18 72 72" width="512" height="512">\n'
       f'<!-- Grim Browser: Iceraven\'s icon (MPL-2.0) recoloured for Grim OS -->\n'
       f'<defs>{"".join(defs)}</defs>\n' + "\n".join(body) + "\n</svg>\n")
open(os.path.join(HERE, "grim-browser.svg"), "w").write(svg)
for s in (16, 32, 48, 64, 128, 256, 512):
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), "-o", os.path.join(HERE, f"grim-browser-{s}.png"),
                    os.path.join(HERE, "grim-browser.svg")], check=False)
print("wrote grim-browser.svg")
