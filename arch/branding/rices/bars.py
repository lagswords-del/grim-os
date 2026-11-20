"""Bar designs for Grim OS, as data. Uses the palettes and fonts from rices.py.

tool   p = Polybar (i3, Openbox, IceWM), w = Waybar (Sway, Hyprland, Niri), pw = both
style  how the bar is drawn:
  full      one solid strip                     pills     three floating rounded groups
  island    everything in one centred pill      split     two groups at the edges
  powerline arrow segments                      roundline rounded segment caps
  underline coloured line under each module     overline  coloured line above each module
  bubbles   every module in its own bubble      plain     text only, dot separators
  icons     icons only (like the CachyOS bar)   brackets  [ terminal ] style
  tabs      folder tabs for workspaces          glass     see-through with a hairline border
  outline   modules drawn as outlines (Waybar)  blocks    flat colour blocks with gaps
  notch     centre piece hangs down like a notch corners   tabs in the two top corners
  double    two bars, top and bottom            side      vertical on the left (Waybar)
  gradient  gradient background (Waybar)
ws     workspace look: num, dots, roman, kanji, bars, words
mods   left|center|right, comma separated:
       ws launcher title clock date cpu mem vol net bat power updates media weather kb tray disk temp
"""
import rices

TOOLS = {"p": "Polybar", "w": "Waybar", "pw": "Polybar or Waybar"}
WAYBAR_ONLY = {"outline", "side", "gradient"}

# name | tool | style | palette | top/bottom | height | ws | mods | font | description
BARS = """
Grim Strip|pw|full|grim|t|26|num|ws|clock|vol,net,bat,power|incon|The Grim default: one black strip, red active workspace, red power button.
Reaper Pills|pw|pills|grim|t|28|dots|launcher,ws|clock|vol,net,bat,power|jbm|Three floating black pills with a red reaper launcher.
Red Island|pw|island|crimson|t|28|dots|ws|clock|vol,bat|space|Everything in one centred red-black island.
Bone Line|pw|underline|bone|t|26|num|ws|date,clock|cpu,mem,vol,bat|plex|Paper white with thin coloured underlines, red for the active workspace.
Nord Snow Bar|p|full|nordsnow|t|26|num|ws,vol,kb|date,clock|net,disk,temp,mem,bat,power|incon|The bar from your i3 screenshot: cyan date block, dB volume, IP, disk and temperature.
Nord Pills|pw|pills|nordsnow|t|28|num|ws|clock|vol,net,bat|jbm|Nord frost in three rounded groups.
Frost Glass|w|glass|nordsnow|t|28|dots|ws|clock|vol,net,bat,power|jbm|A see-through Nord bar with a hairline cyan border.
CachyOS Minimal|pw|icons|nordsnow|t|31|num|launcher,ws|clock|vol,net,bat,updates,power|incon|Your current CachyOS bar: launcher, workspace pill, bold clock, icons only.
Gruvbox Powerline|pw|powerline|gruv|t|24|num|ws,title||cpu,mem,vol,bat,clock|jbm|Classic powerline arrows in Gruvbox yellow, red and green.
Campfire Blocks|pw|blocks|gruv|t|26|num|ws|clock|cpu,mem,temp,bat|term|Chunky flat Gruvbox blocks with gaps and a bitmap font.
Hay Underline|pw|underline|gruvlight|t|26|num|ws|clock|vol,net,bat|plex|Gruvbox light with orange underlines.
Mocha Bubbles|pw|bubbles|mocha|t|28|dots|ws|clock|vol,net,bat,power|jbm|Catppuccin Mocha: every module in its own soft bubble.
Latte Island|pw|island|latte|t|28|dots|ws|clock|vol,bat|plex|Catppuccin Latte in one airy island.
Frappé Roundline|pw|roundline|frappe|t|26|num|ws|clock|cpu,mem,vol,bat|fira|Rounded segment caps in Frappé pastels.
Macchiato Split|w|split|macchiato|t|28|num|ws,title||clock,vol,net,bat|victor|Two floating groups, nothing in the middle.
Dracula Powerline|pw|powerline|dracula|t|24|num|ws|clock|cpu,mem,vol,bat|fira|Purple and pink arrows on Dracula grey.
Vampire Notch|pw|notch|dracula|t|26|num|ws|clock|vol,net,bat|jbm|A clock notch hangs from the middle like a phone camera cut-out.
Tokyo Pills|pw|pills|tokyo|t|28|kanji|ws|clock|vol,net,bat|jbm|Tokyo Night with kanji workspaces: 一 二 三 四 五.
Tokyo Overline|pw|overline|tokyostorm|t|26|num|ws|date|cpu,mem,vol,bat,clock|fira|Coloured lines above each module, storm blue.
Neon Gradient|w|gradient|tokyo|t|28|num|ws|clock|vol,net,bat|space|A blue-to-violet gradient background (Waybar CSS).
Rosé Bubbles|pw|bubbles|rosepine|t|28|dots|ws|clock|media,vol,bat|victor|Rosé Pine bubbles with a now-playing module.
Dawn Plain|pw|plain|rosedawn|t|24|words|ws|date|vol,bat,clock|plex|Text only, separated by dots. Rosé Dawn parchment.
Moon Island|pw|island|rosemoon|t|28|dots|ws|clock|weather,vol|victor|One pill with the weather and the moon colours.
Forest Brackets|pw|brackets|everforest|t|24|num|ws|clock|cpu,mem,bat|jbm|[ terminal ] brackets in Everforest green.
Moss Side|w|side|everforest|t|30|dots|ws||clock,vol,bat,power|jbm|A vertical Everforest bar on the left.
Clearing Underline|pw|underline|everlight|t|26|num|ws|clock|vol,net,bat|plex|Everforest light with green underlines.
Wave Roundline|pw|roundline|kanagawa|t|26|kanji|ws|clock|cpu,mem,vol,bat|jbm|Kanagawa ink-blue with rounded caps and kanji.
Dragon Tabs|pw|tabs|kanadragon|t|26|num|ws|title|clock,vol,bat|plex|Folder-tab workspaces in muted Kanagawa Dragon.
Lotus Glass|w|glass|kanalotus|t|28|dots|ws|clock|vol,bat|plex|See-through rice-paper bar with an indigo hairline.
Solar Full|pw|full|soldark|t|24|num|ws,title||cpu,mem,vol,bat,clock|scp|Solarized dark, classic and dense.
Solar Double|pw|double|sollight|t|24|num|ws,title|clock|cpu,mem,vol,net,bat|scp|Two bars: info on top, workspaces and title at the bottom.
Atom Bubbles|pw|bubbles|onedark|t|28|num|ws|clock|vol,net,bat,power|jbm|One Dark in round bubbles.
Ayu Outline|w|outline|ayudark|t|28|num|ws|clock|cpu,mem,vol,bat|jbm|Every module as an amber outline on black (Waybar borders).
Mirage Notch|pw|notch|ayumirage|t|26|dots|ws|clock|vol,bat|fira|Ayu Mirage with a warm clock notch.
Monokai Blocks|pw|blocks|monokai|t|26|num|ws|clock|cpu,mem,vol,bat|space|Monokai's hot pink, cyan and green as flat blocks.
Material Pills|pw|pills|material|t|28|num|ws|clock|vol,net,bat|jbm|Material blue-grey pills.
Carbon Underline|pw|underline|oxocarbon|t|26|num|ws|clock|cpu,mem,vol,bat|plex|IBM Carbon pink and cyan underlines.
Fox Corners|pw|corners|nightfox|t|26|num|ws||vol,net,bat,clock|fira|Tabs in the two top corners, Nightfox blue.
Sonokai Roundline|pw|roundline|sonokai|t|26|num|ws|clock|vol,bat|fira|Candy-coloured rounded caps.
Melange Plain|pw|plain|melange|t|24|words|ws|date,clock|vol,bat|victor|Warm brown text only, like a library index card.
Horizon Gradient|w|gradient|horizon|t|28|dots|ws|clock|vol,bat|fira|Coral-to-amber sunset gradient (Waybar CSS).
Palenight Island|pw|island|palenight|t|28|dots|ws|clock|vol,bat|victor|Lavender island with a soft glow.
GitHub Full|pw|full|ghdark|t|26|num|ws,title||vol,net,bat,clock|jbm|GitHub dark: crisp, grey borders, blue accent.
GitHub Light Split|w|split|ghlight|t|28|num|ws||clock,vol,net,bat|plex|GitHub light in two white groups.
Moonfly Icons|pw|icons|moonfly|t|26|dots|ws|clock|vol,net,bat,power|jbm|Pure black, icons only, one blue dot for the workspace.
Owl Overline|pw|overline|nightowl|t|26|num|ws|clock|cpu,mem,vol,bat|fira|Night Owl blue with coloured overlines.
Outrun Powerline|pw|powerline|synthwave|t|26|num|ws|clock|media,vol,bat|space|Synthwave pink and cyan arrows.
Netrunner Brackets|pw|brackets|cyberpunk|t|24|num|ws|clock|cpu,mem,net,bat|jbm|[ cyan ] [ magenta ] brackets like a hacking HUD.
Matrix Plain|pw|plain|matrix|t|22|num|ws|clock|cpu,mem,net|term|Green text on black, nothing else.
Amber Brackets|pw|brackets|amber|t|24|num|ws|clock|cpu,mem,bat|term|Amber phosphor brackets with a bitmap font.
Sakura Bubbles|pw|bubbles|sakura|t|28|dots|ws|clock|media,vol,bat|victor|Cherry-blossom bubbles on white.
Matcha Island|pw|island|matcha|t|28|dots|ws|clock|weather,vol,bat|plex|A green-tea island with the weather.
Espresso Tabs|pw|tabs|coffee|t|26|num|ws|title|clock,vol,bat|space|Coffee-brown folder tabs.
Deep Sea Glass|w|glass|ocean|t|28|dots|ws|clock|vol,net,bat|jbm|See-through navy with a coral hairline.
Desert Blocks|pw|blocks|desert|t|26|num|ws|clock|weather,vol,bat|space|Sandstone and teal flat blocks.
Arctic Underline|pw|underline|arctic|t|26|num|ws|clock|vol,net,bat|plex|Ice white with glacier-blue underlines.
Lavender Bubbles|pw|bubbles|lavender|t|28|dots|ws|clock|media,vol,bat|victor|Soft violet bubbles.
Blood Moon Notch|pw|notch|crimson|t|26|dots|ws|clock|vol,bat|jbm|A red notch with the time, black everywhere else.
Slate Double|pw|double|slate|t|24|num|ws,title|clock|cpu,mem,vol,bat|plex|Slate grey: two thin bars, info above, windows below.
Vapor Gradient|w|gradient|vapor|t|28|roman|ws|clock|media,vol|space|Aesthetic pink-to-cyan with Roman numerals.
Classic Taskstrip|pw|full|classic|b|28|num|launcher,ws,title||tray,clock|term|The 95 look at the bottom: a start button, tasks and a clock.
Hacker Overline|pw|overline|hacker|t|24|num|ws|clock|cpu,mem,net,bat|jbm|Electric-blue overlines on near-black.
Autumn Roundline|pw|roundline|autumn|t|26|num|ws|clock|weather,vol,bat|space|Rust and amber with rounded caps.
Mint Pills|pw|pills|mint|t|28|dots|ws|clock|vol,net,bat|plex|Fresh mint pills on white.
Sunset Split|w|split|sunset|t|28|num|ws||clock,vol,bat,power|space|Two sunset-coloured groups.
Aurora Side|w|side|aurora|t|30|dots|ws||clock,vol,bat,power|jbm|A vertical bar glowing green and violet.
Peach Bubbles|pw|bubbles|peach|t|28|dots|ws|clock|vol,bat|victor|Peach and coral bubbles.
Teal Corners|pw|corners|teal|t|26|num|ws||vol,bat,clock|fira|Teal corner tabs with an orange accent.
Plum Glass|w|glass|plum|t|28|dots|ws|clock|vol,bat|victor|See-through plum with a pink hairline.
Steel Full|pw|full|steel|b|26|num|ws,title||cpu,mem,disk,temp,clock|plex|Industrial: every number you want, at the bottom.
Olive Brackets|pw|brackets|olive|t|24|num|ws|clock|cpu,mem,bat|term|Military olive in brackets.
Glacier Island|pw|island|glacier|t|28|dots|ws|clock|vol,bat|jbm|Glacier blue island.
Graphite Icons|pw|icons|mono|t|26|dots|launcher,ws|clock|vol,net,bat,power|jbm|Monochrome icons only. White for active, grey for the rest.
Newsprint Full|pw|full|monolight|t|24|num|ws,title||vol,bat,date,clock|plex|Black on white with hairline separators.
Ink Underline|pw|underline|ink|t|26|num|ws|clock|vol,bat|jbm|Blue-black ink with one red underline.
Scythe Notch|pw|notch|grim|t|26|dots|ws|clock|vol,bat,power|victor|Grim black with a red clock notch.
Crypt Side|w|side|grim|t|30|dots|ws||clock,vol,bat,power|scp|A vertical black bar with red workspaces.
Requiem Double|pw|double|grim|t|24|num|ws,title|clock|cpu,mem,vol,bat,power|scp|Two black bars with red details.
"""


def parse():
    out = []
    for i, line in enumerate(l for l in BARS.strip().splitlines() if l.strip()):
        name, tool, style, pal, pos, h, ws, left, center, right, font, desc = line.split("|")
        assert pal in rices.PALETTES, (name, pal)
        assert font in rices.FONTS, (name, font)
        assert not (style in WAYBAR_ONLY and tool != "w"), f"{name}: {style} needs Waybar"
        split = lambda s: [m for m in s.split(",") if m]
        out.append(dict(n=i + 1, name=name, tool=tool, style=style, pal=pal, pos=pos, h=int(h), ws=ws,
                        left=split(left), center=split(center), right=split(right), font=font, desc=desc))
    return out


if __name__ == "__main__":
    b = parse()
    assert len({x["name"] for x in b}) == len(b)
    import collections
    print(len(b), "bars;", dict(collections.Counter(x["style"] for x in b)))
