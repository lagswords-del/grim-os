#!/usr/bin/env python3
"""grimfetch's Void-style logo: Void Linux's own ASCII ring with GRIM in place of VOID.
${c1} = top arc and the word (red), ${c2} = bottom arc (black)."""
TOP = [
    "                  __.;=====;.__",
    "              _.=+==++=++=+=+===;.",
    "               -=+++=+===+=+=+++++=_",
    "          .     -=:``     `--==+=++==.",
]
# (black part, red part): the bottom arc comes up the left side here
SIDE = [
    ("         _vi,", "    `            --+=++++:"),
    ("        .uvnvi.", "       _._       -==+==+."),
    ("       .vvnvnI`", "    .;==|==;.     :|=||=|."),
]
# GRIM, 4 rows, each row one step further right (Void's slant).
# '#' cells are filled with the same dense texture Void's letters use.
G = [" .#######.", "####'    `", "###   ####", "`#######' "]
R = ["########. ", "###   ### ", "#######'  ", "###   `###"]
I = ["###", "###", "###", "###"]
M = ["####.   .####", "#####. .#####", "### ##### ###", "###  `#'  ###"]
TEX = "QmQQWQ$QQWmQQWQ"
WORD = []
for r in range(4):
    row = "  ".join(L[r] for L in (G, R, I, M))
    row = "".join(TEX[(i + r * 3) % len(TEX)] if ch == "#" else ch for i, ch in enumerate(row))
    lead = ("  +" if r == 0 else " " * (2 + r) + "-")
    WORD.append(lead + " " + row)
# bottom arc: (black part, red part on the right)
BOTTOM = [
    ("       -1vvnvv.", "                         ++|+++"),
    ("        +vnvnnv,", "                 `-|==="),
    ("         +vnvnvns.           .", "      :=-"),
    ("          -Invnvvnsi..___..=sv=.", "     `"),
    ("            +Invnvnvnnnnnnnnvvnn;.", ""),
    ("              ~|Invnvnvvnvvvnnv}+`", ""),
    ("                  -~|{*l}*|~", ""),
]
out = []
for l in TOP: out.append("${c1}" + l)
for b, r in SIDE:
    lead = len(b) - len(b.lstrip())
    out.append(" " * lead + "${c2}" + b.lstrip() + "${c1}" + r)
for l in WORD: out.append("${c1}" + l)
for b, r in BOTTOM:
    lead = len(b) - len(b.lstrip())
    out.append(" " * lead + "${c2}" + b.lstrip() + (("${c1}" + r) if r else ""))
print("\n".join(l.rstrip() for l in out))
