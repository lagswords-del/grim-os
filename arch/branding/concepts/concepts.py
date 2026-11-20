"""50 Grim OS logo concepts. Each is one-colour SVG (currentColor) on a 200x200 canvas.
Run: python3 concepts.py  -> writes svg/NN-slug.svg and concepts.json (name, idea, file)."""
import json, os, re

C = []  # (slug, name, idea, body)

def add(slug, name, idea, body):
    C.append((slug, name, idea, body.strip()))

RING = '<circle cx="100" cy="100" r="78" fill="none" stroke="currentColor" stroke-width="18"/>'

def cutmask(mid, cuts):
    return f'<defs><mask id="{mid}"><rect width="200" height="200" fill="#fff"/>{cuts}</mask></defs>'

# 1
add("scythe-g", "Scythe G", "A bold G whose crossbar becomes a scythe blade.", """
<path d="M150 62 A62 62 0 1 0 162 110 L104 110" fill="none" stroke="currentColor" stroke-width="22" stroke-linecap="butt"/>
<path d="M104 99 C130 92 160 98 182 120 C160 112 134 112 104 121 Z" fill="currentColor"/>
""")
# 2
add("hourglass-skull", "Hourglass Skull", "An hourglass; the top bulb holds a skull, the sand runs out below.", """
<path d="M52 24 H148 V36 H140 C140 72 112 86 108 100 C112 114 140 128 140 164 H148 V176 H52 V164 H60 C60 128 88 114 92 100 C88 86 60 72 60 36 H52 Z" fill="currentColor"/>
<g fill="#000" style="fill:var(--bg,#f2f2f2)">
<path d="M76 40 H124 C124 60 116 70 100 78 C84 70 76 60 76 40 Z"/>
<path d="M78 162 C78 140 92 128 100 120 C108 128 122 140 122 162 Z"/>
</g>
<circle cx="100" cy="54" r="12" fill="currentColor"/><rect x="94" y="62" width="12" height="7" fill="currentColor"/>
<circle cx="95.5" cy="53" r="3" style="fill:var(--bg,#f2f2f2)"/><circle cx="104.5" cy="53" r="3" style="fill:var(--bg,#f2f2f2)"/>
<path d="M88 162 C88 150 96 142 100 138 C104 142 112 150 112 162 Z" fill="currentColor"/>
""")
# 3
add("hooded-void", "Hooded Void", "A pointed hood with nothing inside but a perfect empty circle.", """
""" + cutmask("hv", '<circle cx="100" cy="104" r="30" fill="#000"/>') + """
<path mask="url(#hv)" d="M100 22 C58 40 42 82 42 120 C42 150 54 170 64 180 H136 C146 170 158 150 158 120 C158 82 142 40 100 22 Z" fill="currentColor"/>
""")
# 4
add("scythe-moon", "Scythe Moon", "A crescent moon that doubles as the scythe blade on a thin staff.", """
<path d="M44 70 C70 30 140 26 170 66 C140 46 92 50 64 84 Z" fill="currentColor"/>
<rect x="160" y="54" width="10" height="126" rx="5" fill="currentColor" transform="rotate(8 165 117)"/>
<circle cx="78" cy="132" r="5" fill="currentColor"/><circle cx="110" cy="154" r="3" fill="currentColor"/><circle cx="58" cy="164" r="2.5" fill="currentColor"/>
""")
# 5
add("go-monogram", "GO Monogram", "G and O share one broken Void-style ring; the gap is the G's mouth.", """
""" + cutmask("go", '<rect x="96" y="-20" width="26" height="240" fill="#000" transform="rotate(45 100 100)"/>') + """
<g mask="url(#go)"><circle cx="100" cy="100" r="76" fill="none" stroke="currentColor" stroke-width="20"/></g>
<rect x="100" y="91" width="58" height="18" fill="currentColor"/>
<circle cx="100" cy="100" r="28" fill="none" stroke="currentColor" stroke-width="14"/>
""")
# 6
add("skull-prompt", "Skull Prompt", "A skull whose mouth is a terminal prompt: >_", """
""" + cutmask("sp", '<circle cx="78" cy="88" r="15" fill="#000"/><circle cx="122" cy="88" r="15" fill="#000"/><path d="M96 108 L100 100 L104 108 Z" fill="#000"/><path d="M80 128 L94 138 L80 148" fill="none" stroke="#000" stroke-width="7" stroke-linejoin="round"/><rect x="100" y="142" width="22" height="7" fill="#000"/>') + """
<path mask="url(#sp)" d="M100 26 C58 26 36 56 36 92 C36 114 46 126 56 132 V164 C56 172 62 176 70 176 H130 C138 176 144 172 144 164 V132 C154 126 164 114 164 92 C164 56 142 26 100 26 Z" fill="currentColor"/>
""")
# 7
add("tombstone-cursor", "Tombstone Cursor", "A rounded tombstone with a blinking underscore cursor carved in.", """
""" + cutmask("tc", '<rect x="72" y="104" width="56" height="12" fill="#000"/><text x="100" y="82" font-family="DejaVu Sans Mono,monospace" font-weight="bold" font-size="30" text-anchor="middle" fill="#000">RIP</text>') + """
<path mask="url(#tc)" d="M48 176 V86 C48 50 72 28 100 28 C128 28 152 50 152 86 V176 Z" fill="currentColor"/>
<rect x="30" y="172" width="140" height="12" rx="3" fill="currentColor"/>
""")
# 8
add("crossed-scythes", "Crossed Scythes", "Two scythes crossed like a coat of arms.", """
<g fill="currentColor">
<rect x="94" y="20" width="12" height="170" rx="6" transform="rotate(35 100 105)"/>
<rect x="94" y="20" width="12" height="170" rx="6" transform="rotate(-35 100 105)"/>
<path d="M52 36 C70 12 110 8 136 22 C108 22 82 32 64 52 Z"/>
<path d="M148 36 C130 12 90 8 64 22 C92 22 118 32 136 52 Z"/>
</g>
""")
# 9
add("raven", "Raven", "A raven head in profile: the reaper's messenger.", """
""" + cutmask("rv", '<circle cx="96" cy="78" r="8" fill="#000"/>') + """
<path mask="url(#rv)" d="M40 170 C46 124 54 92 74 70 C92 50 120 48 138 60 L188 74 L142 86 C138 106 124 120 104 128 C122 136 132 152 130 176 C110 160 88 156 70 170 C60 160 52 166 40 170 Z" fill="currentColor"/>
""")
# 10
add("void-eye", "Void Eye", "An eye inside the broken ring; the pupil is the void.", """
""" + cutmask("ve", '<rect x="94" y="-20" width="12" height="240" fill="#000" transform="rotate(-45 100 100)"/>') + """
<g mask="url(#ve)"><circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" stroke-width="14"/></g>
<path d="M36 100 C60 64 140 64 164 100 C140 136 60 136 36 100 Z" fill="currentColor"/>
<circle cx="100" cy="100" r="24" style="fill:var(--bg,#f2f2f2)"/><circle cx="100" cy="100" r="12" fill="currentColor"/>
""")
# 11
add("lantern", "Reaper's Lantern", "An old lantern with a skull-shaped flame inside.", """
""" + cutmask("ln", '<path d="M78 72 H122 V150 H78 Z" fill="#000"/>') + """
<path d="M86 26 A14 14 0 0 1 114 26" fill="none" stroke="currentColor" stroke-width="8"/>
<path mask="url(#ln)" d="M70 44 H130 L138 60 H132 V160 H140 V172 H60 V160 H68 V60 H62 Z" fill="currentColor"/>
<path d="M100 82 C114 98 118 112 112 126 C108 136 92 136 88 126 C82 112 88 98 100 82 Z" fill="currentColor"/>
<circle cx="95" cy="118" r="3" style="fill:var(--bg,#f2f2f2)"/><circle cx="105" cy="118" r="3" style="fill:var(--bg,#f2f2f2)"/>
""")
# 12
add("ring-hourglass", "Ring Hourglass", "The Void ring with an hourglass standing in the gap.", """
""" + cutmask("rh", '<rect x="88" y="-20" width="24" height="240" fill="#000" transform="rotate(0 100 100)"/>') + """
<g mask="url(#rh)"><circle cx="100" cy="100" r="78" fill="none" stroke="currentColor" stroke-width="18"/></g>
<path d="M80 10 H120 V18 C120 40 104 46 104 52 C104 58 120 64 120 86 V90 H80 V86 C80 64 96 58 96 52 C96 46 80 40 80 18 Z" fill="currentColor" transform="translate(0 50)"/>
""")
# 13
add("hood-triangle", "Hood Triangle", "Pure geometry: a triangle hood and two dots for eyes.", """
""" + cutmask("ht", '<path d="M100 78 C82 78 72 96 72 116 L72 140 H128 V116 C128 96 118 78 100 78 Z" fill="#000"/>') + """
<path mask="url(#ht)" d="M100 20 L174 176 H26 Z" fill="currentColor"/>
<circle cx="89" cy="112" r="6" fill="currentColor"/><circle cx="111" cy="112" r="6" fill="currentColor"/>
""")
# 14
add("scythe-slash-ring", "Scythe-Cut Ring", "The Void ring, but the gap is carved by a curved scythe swing.", """
""" + cutmask("ss", '<path d="M10 150 C60 90 120 60 196 46 L200 70 C130 82 74 112 26 166 Z" fill="#000"/>') + """
<g mask="url(#ss)"><circle cx="100" cy="100" r="76" fill="none" stroke="currentColor" stroke-width="22"/></g>
<path d="M36 140 C76 98 124 74 182 60 C130 80 88 108 52 150 Z" fill="currentColor"/>
""")
# 15
add("grim-wordmark", "grim wordmark", "Lowercase 'grim' where the dot of the i is a tiny skull.", """
<text x="100" y="128" font-family="DejaVu Sans,sans-serif" font-weight="bold" font-size="64" text-anchor="middle" fill="currentColor" letter-spacing="-2">gr&#305;m</text>
<circle cx="111" cy="62" r="11" fill="currentColor"/><rect x="106" y="69" width="10" height="7" fill="currentColor"/>
<circle cx="107" cy="61" r="3" style="fill:var(--bg,#f2f2f2)"/><circle cx="115" cy="61" r="3" style="fill:var(--bg,#f2f2f2)"/>
""")
# 16
add("skull-shield", "Skull Shield", "A heraldic shield holding a minimal skull: protection, security.", """
""" + cutmask("sh", '<path d="M100 56 C80 56 68 70 68 88 C68 100 74 106 80 110 V124 H120 V110 C126 106 132 100 132 88 C132 70 120 56 100 56 Z" fill="#000"/>') + """
<path mask="url(#sh)" d="M100 18 L164 40 V96 C164 140 136 168 100 184 C64 168 36 140 36 96 V40 Z" fill="currentColor"/>
<circle cx="88" cy="88" r="8" fill="currentColor"/><circle cx="112" cy="88" r="8" fill="currentColor"/>
<rect x="90" y="114" width="4" height="10" fill="currentColor"/><rect x="98" y="114" width="4" height="10" fill="currentColor"/><rect x="106" y="114" width="4" height="10" fill="currentColor"/>
""")
# 17
pix = ["....XXXXXX....", "...XXXXXXXX...", "..XXX....XXX..", "..XX......XX..", "..XX.X..X.XX..", "..XX......XX..",
       "..XXX....XXX..", ".XXXXXXXXXXXX.", ".XXXXXXXXXXXX.", "XXXXXXXXXXXXXX", "XXXXXXXXXXXXXX", "XXXXXXXXXXXXXX",
       "XX.XX.XX.XX.XX"]
cells = "".join(f'<rect x="{30+c*10}" y="{34+r*10}" width="10" height="10"/>' for r, row in enumerate(pix) for c, ch in enumerate(row) if ch == "X")
add("pixel-reaper", "Pixel Reaper", "A 14x13 pixel-art reaper, retro and crisp at tiny sizes.", f'<g fill="currentColor">{cells}</g>')
# 18
add("deaths-head-moth", "Death's-head Moth", "A moth with the skull marking on its back.", """
<g fill="currentColor">
<path d="M100 70 C80 40 30 30 14 56 C8 80 40 100 92 104 Z"/>
<path d="M100 70 C120 40 170 30 186 56 C192 80 160 100 108 104 Z"/>
<path d="M92 108 C56 112 34 132 42 156 C56 168 82 146 96 120 Z"/>
<path d="M108 108 C144 112 166 132 158 156 C144 168 118 146 104 120 Z"/>
<ellipse cx="100" cy="108" rx="13" ry="42"/>
<path d="M96 70 C90 50 80 40 70 36" fill="none" stroke="currentColor" stroke-width="3"/>
<path d="M104 70 C110 50 120 40 130 36" fill="none" stroke="currentColor" stroke-width="3"/>
</g>
<circle cx="100" cy="94" r="7" style="fill:var(--bg,#f2f2f2)"/><circle cx="97.5" cy="93" r="2" fill="currentColor"/><circle cx="102.5" cy="93" r="2" fill="currentColor"/>
""")
# 19
rays = "".join(f'<rect x="96" y="8" width="8" height="34" rx="2" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 30))
add("black-sun", "Black Sun", "A solid black sun with sharp rays: the void that gives light.", f'<g fill="currentColor">{rays}<circle cx="100" cy="100" r="46"/></g>')
# 20
add("soul-spiral", "Soul Spiral", "A spiral that thins into nothing, like a soul leaving.", """
<path d="M100 100 m0 -6 a6 6 0 1 1 -6 6 a14 14 0 0 1 14 -14 a22 22 0 0 1 22 22 a32 32 0 0 1 -32 32 a44 44 0 0 1 -44 -44 a58 58 0 0 1 58 -58 a72 72 0 0 1 72 72"
 fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"/>
""")
# 21
add("keyhole-hood", "Keyhole Hood", "A hood silhouette that is also a keyhole: Grim OS unlocks your machine.", """
""" + cutmask("kh", '<circle cx="100" cy="84" r="22" fill="#000"/><path d="M90 96 L82 150 H118 L110 96 Z" fill="#000"/>') + """
<rect mask="url(#kh)" x="34" y="24" width="132" height="152" rx="30" fill="currentColor"/>
""")
# 22
add("bony-hand-orb", "Hand and Orb", "A skeletal hand holding a glowing orb.", """
<circle cx="100" cy="64" r="30" fill="currentColor"/>
<circle cx="90" cy="54" r="8" style="fill:var(--bg,#f2f2f2)"/>
<g fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round">
<path d="M62 92 C62 110 70 120 82 124"/><path d="M80 98 V122"/><path d="M100 100 V124"/><path d="M120 98 V122"/><path d="M138 92 C140 108 132 118 120 124"/>
<path d="M70 132 C78 146 122 146 130 132"/><path d="M100 146 V184"/>
</g>
""")
# 23
add("candle-skull", "Candle Skull", "A short candle whose flame forms a small skull.", """
<path d="M100 28 C118 50 126 70 120 90 C116 104 84 104 80 90 C74 70 82 50 100 28 Z" fill="currentColor"/>
<circle cx="93" cy="80" r="4.5" style="fill:var(--bg,#f2f2f2)"/><circle cx="107" cy="80" r="4.5" style="fill:var(--bg,#f2f2f2)"/>
<rect x="74" y="110" width="52" height="68" rx="4" fill="currentColor"/>
<path d="M74 118 C84 126 88 116 96 124 C104 130 110 118 126 122 V110 H74 Z" style="fill:var(--bg,#f2f2f2)" opacity="0.0"/>
<path d="M78 112 C80 126 86 128 86 136 C86 142 80 142 80 136 Z" style="fill:var(--bg,#f2f2f2)"/>
<rect x="54" y="176" width="92" height="10" rx="5" fill="currentColor"/>
""")
# 24
add("coffin-g", "Coffin G", "A coffin outline with a cut G on the lid.", """
""" + cutmask("cg", '<path d="M118 84 A22 22 0 1 0 122 104 H102" fill="none" stroke="#000" stroke-width="10"/>') + """
<path mask="url(#cg)" d="M74 18 H126 L156 60 L134 182 H66 L44 60 Z" fill="currentColor"/>
""")
# 25
add("ouroboros-scythe", "Scythe Ring", "A scythe bent into a full circle, blade biting its own staff.", """
<path d="M100 22 A78 78 0 1 1 30 66" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"/>
<path d="M30 66 C30 34 64 14 100 22 C76 30 56 46 48 72 Z" fill="currentColor"/>
""")
# 26
add("hood-arch", "Doorway", "An arched doorway with the reaper standing in the light.", """
""" + cutmask("ha", '<path d="M56 182 V90 C56 60 76 42 100 42 C124 42 144 60 144 90 V182 Z" fill="#000"/>') + """
<rect mask="url(#ha)" x="30" y="20" width="140" height="170" rx="6" fill="currentColor"/>
<path d="M100 68 C84 74 78 92 78 108 C78 126 74 146 70 182 H130 C126 146 122 126 122 108 C122 92 116 74 100 68 Z" fill="currentColor"/>
""")
# 27
add("bat-ring", "Bat Ring", "Bat wings spreading out of the broken Void ring.", """
""" + cutmask("br", '<rect x="94" y="-20" width="12" height="240" fill="#000" transform="rotate(-45 100 100)"/>') + """
<g mask="url(#br)"><circle cx="100" cy="100" r="44" fill="none" stroke="currentColor" stroke-width="12"/></g>
<path d="M58 92 C40 70 20 66 6 72 C18 80 22 92 18 104 C30 98 40 104 44 114 C50 104 56 104 60 106 Z" fill="currentColor"/>
<path d="M142 92 C160 70 180 66 194 72 C182 80 178 92 182 104 C170 98 160 104 156 114 C150 104 144 104 140 106 Z" fill="currentColor"/>
""")
# 28
add("clock-scythe", "Last Hour", "A clock face where the scythe is the only hand.", """
<circle cx="100" cy="100" r="78" fill="none" stroke="currentColor" stroke-width="10"/>
""" + "".join(f'<rect x="97" y="30" width="6" height="14" fill="currentColor" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 30)) + """
<rect x="96" y="56" width="8" height="58" rx="4" fill="currentColor" transform="rotate(-30 100 100)"/>
<path d="M100 52 C118 44 140 48 152 62 C136 58 118 60 104 66 Z" fill="currentColor" transform="rotate(-30 100 100)"/>
<circle cx="100" cy="100" r="8" fill="currentColor"/>
""")
# 29
add("sheet-ghost", "Little Ghost", "A friendly sheet ghost: Grim OS doesn't have to be scary.", """
""" + cutmask("sg", '<ellipse cx="82" cy="88" rx="9" ry="13" fill="#000"/><ellipse cx="118" cy="88" rx="9" ry="13" fill="#000"/><ellipse cx="100" cy="118" rx="8" ry="6" fill="#000"/>') + """
<path mask="url(#sg)" d="M100 24 C64 24 44 52 44 86 V176 L62 162 L80 176 L100 162 L120 176 L138 162 L156 176 V86 C156 52 136 24 100 24 Z" fill="currentColor"/>
""")
# 30
add("black-cat", "Black Cat", "A sitting black cat whose tail curls into a scythe blade.", """
<path d="M70 176 C56 150 60 116 76 98 L66 52 L90 76 C98 74 106 74 114 76 L136 52 L128 98 C146 118 146 152 132 176 Z" fill="currentColor"/>
<path d="M132 172 C166 168 182 140 172 112 C188 140 176 182 132 184 Z" fill="currentColor"/>
<path d="M86 100 L96 104 L86 108 Z" style="fill:var(--bg,#f2f2f2)"/><path d="M118 100 L108 104 L118 108 Z" style="fill:var(--bg,#f2f2f2)"/>
""")
# 31
add("dead-rose", "Dead Rose", "A wilting rose with sharp thorns.", """
<path d="M100 26 C76 26 64 44 68 62 C72 80 90 88 100 88 C110 88 128 80 132 62 C136 44 124 26 100 26 Z" fill="currentColor"/>
<path d="M84 46 C92 38 108 38 116 46 C108 50 96 58 100 70 C88 66 82 56 84 46 Z" style="fill:var(--bg,#f2f2f2)"/>
<path d="M100 88 C104 120 92 150 104 184" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>
<path d="M98 120 L82 112 L96 128 Z M102 148 L118 140 L104 156 Z" fill="currentColor"/>
<path d="M98 134 C78 136 64 126 58 112 C78 112 92 120 98 134 Z" fill="currentColor"/>
""")
# 32
add("triple-moon", "Triple Moon", "Waxing, full and waning moons; the full moon hides a hood.", """
<path d="M44 70 A30 30 0 1 0 44 130 A24 30 0 1 1 44 70 Z" fill="currentColor"/>
<path d="M156 70 A30 30 0 1 1 156 130 A24 30 0 1 0 156 70 Z" fill="currentColor"/>
""" + cutmask("tm", '<path d="M100 76 C88 80 82 94 82 108 V130 H118 V108 C118 94 112 80 100 76 Z" fill="#000"/>') + """
<circle mask="url(#tm)" cx="100" cy="100" r="36" fill="currentColor"/>
""")
# 33
glitch = cutmask("gl", '<rect x="0" y="66" width="200" height="6" fill="#000"/><rect x="0" y="112" width="200" height="5" fill="#000"/><rect x="0" y="140" width="200" height="4" fill="#000"/><circle cx="78" cy="92" r="14" fill="#000"/><circle cx="122" cy="92" r="14" fill="#000"/><path d="M95 110 L100 102 L105 110 Z" fill="#000"/>')
add("glitch-skull", "Glitch Skull", "A skull sliced by scanlines and shifted, like a corrupted frame.", glitch + """
<g mask="url(#gl)" fill="currentColor">
<path d="M100 30 C62 30 42 58 42 90 C42 112 52 124 62 130 V160 C62 166 66 170 72 170 H128 C134 170 138 166 138 160 V130 C148 124 158 112 158 90 C158 58 138 30 100 30 Z"/>
</g>
<rect x="30" y="112" width="36" height="5" fill="currentColor"/><rect x="138" y="66" width="34" height="6" fill="currentColor"/><rect x="146" y="140" width="22" height="4" fill="currentColor"/>
""")
# 34
add("lowpoly-skull", "Faceted Skull", "A skull built from flat triangles, sharp and modern.", """
<g fill="currentColor" style="stroke:var(--bg,#f2f2f2)" stroke-width="2.5" stroke-linejoin="round">
<path d="M100 26 L56 50 L74 92 Z"/><path d="M100 26 L144 50 L126 92 Z"/><path d="M100 26 L74 92 L126 92 Z"/>
<path d="M56 50 L40 96 L74 92 Z"/><path d="M144 50 L160 96 L126 92 Z"/>
<path d="M40 96 L62 140 L74 92 Z"/><path d="M160 96 L138 140 L126 92 Z"/>
<path d="M74 92 L100 124 L126 92 Z"/><path d="M74 92 L62 140 L100 124 Z"/><path d="M126 92 L138 140 L100 124 Z"/>
<path d="M62 140 L100 124 L80 176 Z"/><path d="M138 140 L100 124 L120 176 Z"/><path d="M80 176 L100 124 L120 176 Z"/>
</g>
<path d="M66 98 L86 104 L76 116 Z" style="fill:var(--bg,#f2f2f2)"/><path d="M134 98 L114 104 L124 116 Z" style="fill:var(--bg,#f2f2f2)"/>
""")
# 35
add("line-reaper", "One-Line Reaper", "The whole reaper and scythe drawn as a single unbroken line.", """
<path d="M40 180 C56 150 60 118 64 88 C68 50 92 30 112 34 C140 40 146 76 140 106 C136 128 138 156 150 180 M112 34 C116 24 130 18 146 22 M146 22 C168 26 182 44 184 62 C172 46 156 40 140 42 M146 22 L118 176
 M86 72 C92 66 104 66 110 74 C112 92 104 104 94 102 C84 100 82 84 86 72"
 fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
""")
# 36
add("scythe-lambda", "Scythe Lambda", "A lambda drawn as a scythe: a nod to code and to the reaper.", """
<path d="M64 34 C78 34 90 42 96 56 L148 176" fill="none" stroke="currentColor" stroke-width="18" stroke-linecap="round"/>
<path d="M108 102 L52 176" fill="none" stroke="currentColor" stroke-width="18" stroke-linecap="round"/>
<path d="M60 34 C40 30 22 40 14 58 C30 46 46 44 62 50 Z" fill="currentColor"/>
""")
# 37
add("brace-hood", "Brace Hood", "Code braces { } form the hood around two glowing eyes.", """
<path d="M74 30 C52 30 52 46 52 62 C52 82 50 92 34 100 C50 108 52 118 52 138 C52 156 52 170 74 170" fill="none" stroke="currentColor" stroke-width="16" stroke-linecap="round"/>
<path d="M126 30 C148 30 148 46 148 62 C148 82 150 92 166 100 C150 108 148 118 148 138 C148 156 148 170 126 170" fill="none" stroke="currentColor" stroke-width="16" stroke-linecap="round"/>
<path d="M78 98 C84 90 94 90 98 98 C92 104 84 104 78 98 Z M102 98 C106 90 116 90 122 98 C116 104 108 104 102 98 Z" fill="currentColor"/>
""")
# 38
add("negative-g-hood", "Hood G", "The negative space inside a hood forms the letter G.", """
""" + cutmask("ng", '<path d="M124 82 A30 30 0 1 0 128 112 H104" fill="none" stroke="#000" stroke-width="14"/>') + """
<path mask="url(#ng)" d="M100 18 C56 30 34 70 34 112 C34 146 46 168 56 182 H144 C154 168 166 146 166 112 C166 70 144 30 100 18 Z" fill="currentColor"/>
""")
# 39
add("crow-scythe", "Crow on the Blade", "A crow perched on the tip of a scythe.", """
<path d="M28 176 L132 64" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
<path d="M132 64 C120 30 80 18 46 30 C78 32 104 46 118 76 Z" fill="currentColor"/>
<path d="M48 26 C52 14 62 10 70 14 L80 10 L74 18 C76 26 70 32 62 32 L66 40 L54 34 Z" fill="currentColor"/>
""")
# 40
add("sand-drip", "Last Grain", "Hourglass reduced to two triangles and one falling grain.", """
<path d="M44 26 H156 L100 96 Z" fill="currentColor"/>
<path d="M100 104 L156 174 H44 Z" fill="none" stroke="currentColor" stroke-width="10" stroke-linejoin="round"/>
<circle cx="100" cy="122" r="6" fill="currentColor"/>
""")
# 41
add("web-ring", "Web Ring", "The broken ring strung with a spider web.", """
""" + cutmask("wr", '<rect x="94" y="-20" width="12" height="240" fill="#000" transform="rotate(-45 100 100)"/>') + """
<g mask="url(#wr)" fill="none" stroke="currentColor">
<circle cx="100" cy="100" r="80" stroke-width="12"/>
<circle cx="100" cy="100" r="54" stroke-width="3"/><circle cx="100" cy="100" r="30" stroke-width="3"/>
""" + "".join(f'<line x1="100" y1="100" x2="100" y2="20" stroke-width="3" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 45)) + """
</g>
""")
# 42
add("badge-stamp", "Reaper Seal", "A round seal with GRIM OS around the edge and a hood in the middle.", """
<defs><path id="arc42" d="M36 100 A64 64 0 1 1 164 100"/></defs>
<circle cx="100" cy="100" r="88" fill="none" stroke="currentColor" stroke-width="6"/>
<circle cx="100" cy="100" r="58" fill="none" stroke="currentColor" stroke-width="3"/>
<text font-family="DejaVu Sans,sans-serif" font-weight="bold" font-size="20" letter-spacing="6" fill="currentColor"><textPath href="#arc42" startOffset="50%" text-anchor="middle">GRIM OS</textPath></text>
<text x="100" y="172" font-family="DejaVu Sans,sans-serif" font-size="12" letter-spacing="3" text-anchor="middle" fill="currentColor">EST 2026</text>
""" + cutmask("bs", '<circle cx="100" cy="110" r="14" fill="#000"/>') + """
<path mask="url(#bs)" d="M100 62 C80 70 72 92 72 112 C72 126 76 136 80 142 H120 C124 136 128 126 128 112 C128 92 120 70 100 62 Z" fill="currentColor"/>
""")
# 43
add("tarot-xiii", "Card XIII", "A tarot card frame with XIII and a scythe: the Death card means change.", """
<rect x="46" y="18" width="108" height="164" rx="8" fill="none" stroke="currentColor" stroke-width="8"/>
<rect x="56" y="28" width="88" height="144" rx="4" fill="none" stroke="currentColor" stroke-width="2"/>
<text x="100" y="56" font-family="DejaVu Serif,serif" font-weight="bold" font-size="22" text-anchor="middle" fill="currentColor">XIII</text>
<path d="M78 152 L118 76" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>
<path d="M118 76 C110 60 90 58 72 66 C88 68 102 76 110 92 Z" fill="currentColor"/>
""")
# 44
add("soul-flame", "Soul Flame", "A hood with a flame burning where the face should be.", """
""" + cutmask("sf", '<path d="M100 70 C82 76 74 96 74 114 C74 132 84 146 100 146 C116 146 126 132 126 114 C126 96 118 76 100 70 Z" fill="#000"/>') + """
<path mask="url(#sf)" d="M100 22 C60 36 40 78 40 120 C40 150 50 170 60 182 H140 C150 170 160 150 160 120 C160 78 140 36 100 22 Z" fill="currentColor"/>
<path d="M100 84 C112 100 116 112 112 124 C110 132 104 138 100 138 C96 138 88 132 88 124 C86 114 92 106 98 112 C100 104 100 94 100 84 Z" fill="currentColor"/>
""")
# 45
add("skeleton-key", "Skeleton Key", "A key whose bow is a skull: root access, Grim style.", """
""" + cutmask("sk", '<circle cx="62" cy="62" r="9" fill="#000"/><circle cx="86" cy="62" r="9" fill="#000"/><path d="M70 82 L74 76 L78 82 Z" fill="#000"/>') + """
<path mask="url(#sk)" d="M74 24 C48 24 36 42 36 62 C36 76 42 84 50 88 V100 H98 V88 C106 84 112 76 112 62 C112 42 100 24 74 24 Z" fill="currentColor"/>
<rect x="66" y="98" width="16" height="84" fill="currentColor"/>
<rect x="82" y="150" width="22" height="10" fill="currentColor"/><rect x="82" y="168" width="30" height="10" fill="currentColor"/>
""")
# 46
add("eclipse-hood", "Eclipse", "A total eclipse; the dark disc has a hood cut out of it.", """
<circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="2 6"/>
<circle cx="100" cy="100" r="66" fill="none" stroke="currentColor" stroke-width="6"/>
""" + cutmask("ec", '<path d="M100 60 C82 66 74 86 74 106 C74 126 76 140 80 150 H120 C124 140 126 126 126 106 C126 86 118 66 100 60 Z" fill="#000"/>') + """
<circle mask="url(#ec)" cx="100" cy="100" r="56" fill="currentColor"/>
""")
# 47
add("bone-cross", "Crossbones Ring", "Two crossed bones inside the Void ring.", """
""" + cutmask("bc", '<rect x="94" y="-20" width="12" height="240" fill="#000" transform="rotate(-45 100 100)"/>') + """
<g mask="url(#bc)"><circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" stroke-width="14"/></g>
<g fill="currentColor">
<g transform="rotate(45 100 100)"><rect x="94" y="46" width="12" height="108"/><circle cx="92" cy="46" r="9"/><circle cx="108" cy="46" r="9"/><circle cx="92" cy="154" r="9"/><circle cx="108" cy="154" r="9"/></g>
<g transform="rotate(-45 100 100)"><rect x="94" y="46" width="12" height="108"/><circle cx="92" cy="46" r="9"/><circle cx="108" cy="46" r="9"/><circle cx="92" cy="154" r="9"/><circle cx="108" cy="154" r="9"/></g>
</g>
""")
# 48
add("plague-mask", "Plague Mask", "A plague doctor's beaked mask in profile.", """
""" + cutmask("pm", '<circle cx="76" cy="82" r="13" fill="#000"/>') + """
<path mask="url(#pm)" d="M56 40 C80 26 108 34 116 60 C140 76 168 104 184 138 C156 120 130 112 110 112 C102 128 84 134 66 128 C48 120 40 100 42 76 C42 60 46 48 56 40 Z" fill="currentColor"/>
<path d="M36 64 C44 34 76 18 108 30 L120 22 L116 40 C90 28 60 40 48 70 Z" fill="currentColor"/>
<circle cx="76" cy="82" r="6" fill="currentColor"/>
""")
# 49
add("grim-dot", "Bitten Dot", "A single solid circle with a hood-shaped bite out of it.", """
""" + cutmask("gd", '<path d="M150 70 C128 76 118 100 118 124 C118 150 122 176 128 200 H220 V40 Z" fill="#000"/>') + """
<circle mask="url(#gd)" cx="100" cy="100" r="80" fill="currentColor"/>
""")
# 50
add("reaper-bust", "Reaper Bust", "A detailed hooded bust with a shadowed skull face.", """
""" + cutmask("rb", '<path d="M100 56 C78 58 66 80 66 100 C66 124 82 142 100 142 C118 142 134 124 134 100 C134 80 122 58 100 56 Z" fill="#000"/>') + """
<path mask="url(#rb)" d="M100 16 C58 26 36 66 36 104 C36 128 30 146 18 168 C46 160 70 168 100 184 C130 168 154 160 182 168 C170 146 164 128 164 104 C164 66 142 26 100 16 Z" fill="currentColor"/>
<path d="M100 70 C84 70 76 84 76 98 C76 110 82 116 88 120 V130 H112 V120 C118 116 124 110 124 98 C124 84 116 70 100 70 Z" fill="currentColor"/>
<circle cx="90" cy="98" r="6" style="fill:var(--bg,#f2f2f2)"/><circle cx="110" cy="98" r="6" style="fill:var(--bg,#f2f2f2)"/>
<path d="M97 112 L100 106 L103 112 Z" style="fill:var(--bg,#f2f2f2)"/>
""")

# ---- second pass: redrawn after reviewing the contact sheet ----
def redo(slug, body):
    for i, (s, n, idea, _) in enumerate(C):
        if s == slug:
            C[i] = (s, n, idea, body.strip()); return
    raise KeyError(slug)

redo("scythe-g", """
<path d="M146 58 A62 62 0 1 0 162 110 L108 110" fill="none" stroke="currentColor" stroke-width="22"/>
<path d="M108 99 C138 86 172 92 194 124 C166 110 136 110 108 121 Z" fill="currentColor"/>
""")
redo("hooded-void", cutmask("hv", '<circle cx="100" cy="108" r="28" fill="#000"/>') + """
<path mask="url(#hv)" d="M104 16 C88 30 70 44 58 64 C44 88 42 112 42 132 C42 152 34 166 22 182 H178 C166 166 158 152 158 132 C158 96 146 58 104 16 Z" fill="currentColor"/>
""")
redo("scythe-moon", """
<g transform="rotate(12 100 100)">
<rect x="142" y="40" width="10" height="146" rx="5" fill="currentColor"/>
<path d="M150 46 C126 14 64 14 30 58 C66 36 112 36 146 68 Z" fill="currentColor"/>
</g>
<circle cx="64" cy="126" r="5" fill="currentColor"/><circle cx="94" cy="150" r="3.5" fill="currentColor"/><circle cx="46" cy="164" r="2.5" fill="currentColor"/>
""")
redo("crossed-scythes", """
<g fill="currentColor">
<g transform="rotate(32 100 100)"><rect x="95" y="28" width="10" height="160" rx="5"/><path d="M104 30 C128 18 160 24 176 48 C152 38 128 38 104 48 Z"/></g>
<g transform="rotate(-32 100 100)"><rect x="95" y="28" width="10" height="160" rx="5"/><path d="M96 30 C72 18 40 24 24 48 C48 38 72 38 96 48 Z"/></g>
</g>
""")
redo("ouroboros-scythe", """
<path d="M118 24 A78 78 0 1 1 40 54" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"/>
<path d="M42 50 C58 18 102 6 130 22 C100 22 76 36 66 66 C60 74 50 70 42 50 Z" fill="currentColor"/>
""")
redo("line-reaper", """
<path d="M46 182 C58 156 62 128 64 100 C66 62 86 38 108 38 C132 38 146 64 142 98 C140 126 144 156 156 182"
 fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M88 78 C88 66 96 60 104 60 C114 60 120 68 120 80 C120 96 112 106 104 106 C94 106 88 94 88 78 Z"
 fill="none" stroke="currentColor" stroke-width="6"/>
<path d="M166 30 L130 184" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>
<path d="M166 30 C138 14 98 18 74 40 C104 30 134 34 160 52" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
""")
redo("crow-scythe", """
<path d="M30 182 L118 82" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
<path d="M118 82 C112 52 80 40 50 46 C78 52 98 64 108 90 Z" fill="currentColor"/>
""" + cutmask("cw", '<circle cx="138" cy="44" r="4" fill="#000"/>') + """
<path mask="url(#cw)" d="M112 80 C108 64 114 48 126 40 C134 32 146 32 152 40 L176 42 L156 50 C160 62 154 76 142 82 L170 108 L140 96 L130 86 C124 88 116 86 112 80 Z" fill="currentColor"/>
""")
letters = "".join(
    f'<text x="100" y="30" font-family="DejaVu Sans,sans-serif" font-weight="bold" font-size="20" text-anchor="middle" fill="currentColor" transform="rotate({a} 100 100)">{ch}</text>'
    for ch, a in zip("GRIM OS", range(-54, 55, 18)) if ch != " ")
redo("badge-stamp", """
<circle cx="100" cy="100" r="90" fill="none" stroke="currentColor" stroke-width="6"/>
<circle cx="100" cy="100" r="58" fill="none" stroke="currentColor" stroke-width="3"/>
""" + letters + """
<text x="100" y="178" font-family="DejaVu Sans,sans-serif" font-size="12" letter-spacing="3" text-anchor="middle" fill="currentColor">EST 2026</text>
""" + cutmask("bs", '<circle cx="100" cy="110" r="14" fill="#000"/>') + """
<path mask="url(#bs)" d="M100 62 C80 70 72 92 72 112 C72 126 76 136 80 142 H120 C124 136 128 126 128 112 C128 92 120 70 100 62 Z" fill="currentColor"/>
""")
redo("triple-moon", """
<path d="M52 64 A36 36 0 1 0 52 136 A26 36 0 1 1 52 64 Z" fill="currentColor"/>
<path d="M148 64 A36 36 0 1 1 148 136 A26 36 0 1 0 148 64 Z" fill="currentColor"/>
""" + cutmask("tm", '<path d="M100 76 C88 80 82 94 82 108 V136 H118 V108 C118 94 112 80 100 76 Z" fill="#000"/>') + """
<circle mask="url(#tm)" cx="100" cy="100" r="36" fill="currentColor"/>
""")
redo("hood-arch", cutmask("ha", '<path d="M56 182 V90 C56 60 76 42 100 42 C124 42 144 60 144 90 V182 Z" fill="#000"/>') + """
<rect mask="url(#ha)" x="30" y="20" width="140" height="170" rx="6" fill="currentColor"/>
""" + cutmask("hf", '<circle cx="100" cy="108" r="11" fill="#000"/>') + """
<path mask="url(#hf)" d="M100 78 C86 84 80 100 80 116 C80 136 78 156 74 182 H126 C122 156 120 136 120 116 C120 100 114 84 100 78 Z" fill="currentColor"/>
""")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "svg"), exist_ok=True)
    meta = []
    for i, (slug, name, idea, body) in enumerate(C, 1):
        fn = f"{i:02d}-{slug}.svg"
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" color="#0a0a0a" style="--bg:#f2f2f2">{body}</svg>'
        open(os.path.join(here, "svg", fn), "w").write(svg)
        meta.append({"n": i, "slug": slug, "name": name, "idea": idea, "file": fn, "body": body})
    json.dump(meta, open(os.path.join(here, "concepts.json"), "w"), indent=1)
    print(len(C), "concepts")
