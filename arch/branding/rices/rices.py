"""150 rice designs for i3, Sway, IceWM and Openbox, as data.

Every value is something grim-rice (or the WM itself) can really do:
  wms     i = i3, s = Sway, c = IceWM, o = Openbox
  bar     full / fullb (bottom) / pills / island / minimal / corners / blocks (powerline)
          / under (underlined workspaces) / float (floating rounded bar) / split (two groups)
          / taskbar (IceWM's own taskbar, IceWM only) / side (vertical bar: Waybar on Sway, tint2 on Openbox)
  radius  needs picom on X11; Sway has no rounded corners, so Sway rices are drawn square
  flags   d = dock (Plank / nwg-dock), t = window title bars, s = shadows (picom), a = see-through terminal
"""

# key: (bg, surface, fg, muted, accent, accent2, accent3)
PALETTES = {
    "grim": ("#0b0b0c", "#17171a", "#e6e6e6", "#77777d", "#c1121f", "#e05561", "#ffffff"),
    "bone": ("#ecebe6", "#dcdad2", "#161616", "#6b6a66", "#161616", "#c1121f", "#8a8780"),
    "nordsnow": ("#2e3440", "#3b4252", "#d8dee9", "#7b88a1", "#88c0d0", "#b48ead", "#81a1c1"),
    "nordlight": ("#eceff4", "#dde3ec", "#2e3440", "#7b88a1", "#5e81ac", "#bf616a", "#88c0d0"),
    "gruv": ("#282828", "#3c3836", "#ebdbb2", "#a89984", "#fabd2f", "#fb4934", "#b8bb26"),
    "gruvlight": ("#fbf1c7", "#ebdbb2", "#3c3836", "#7c6f64", "#d65d0e", "#9d0006", "#79740e"),
    "mocha": ("#1e1e2e", "#313244", "#cdd6f4", "#7f849c", "#cba6f7", "#f38ba8", "#89b4fa"),
    "latte": ("#eff1f5", "#ccd0da", "#4c4f69", "#8c8fa1", "#8839ef", "#d20f39", "#1e66f5"),
    "frappe": ("#303446", "#414559", "#c6d0f5", "#838ba7", "#8caaee", "#e78284", "#a6d189"),
    "macchiato": ("#24273a", "#363a4f", "#cad3f5", "#8087a2", "#f5bde6", "#ed8796", "#8bd5ca"),
    "dracula": ("#282a36", "#44475a", "#f8f8f2", "#6272a4", "#bd93f9", "#ff79c6", "#50fa7b"),
    "tokyo": ("#1a1b26", "#24283b", "#c0caf5", "#565f89", "#7aa2f7", "#bb9af7", "#9ece6a"),
    "tokyostorm": ("#24283b", "#2f3549", "#a9b1d6", "#565f89", "#7dcfff", "#f7768e", "#e0af68"),
    "tokyoday": ("#e1e2e7", "#d0d5e3", "#3760bf", "#848cb5", "#2e7de9", "#9854f1", "#587539"),
    "rosepine": ("#191724", "#26233a", "#e0def4", "#6e6a86", "#ebbcba", "#c4a7e7", "#31748f"),
    "rosemoon": ("#232136", "#393552", "#e0def4", "#6e6a86", "#ea9a97", "#c4a7e7", "#3e8fb0"),
    "rosedawn": ("#faf4ed", "#f2e9e1", "#575279", "#9893a5", "#d7827e", "#907aa9", "#286983"),
    "everforest": ("#2d353b", "#3d484d", "#d3c6aa", "#859289", "#a7c080", "#e69875", "#7fbbb3"),
    "everlight": ("#fdf6e3", "#efebd4", "#5c6a72", "#939f91", "#8da101", "#f57d26", "#3a94c5"),
    "kanagawa": ("#1f1f28", "#2a2a37", "#dcd7ba", "#727169", "#7e9cd8", "#c34043", "#98bb6c"),
    "kanadragon": ("#181616", "#282727", "#c5c9c5", "#737c73", "#c4746e", "#8ba4b0", "#87a987"),
    "kanalotus": ("#f2ecbc", "#e7dba0", "#545464", "#8a8980", "#4d699b", "#c84053", "#6f894e"),
    "soldark": ("#002b36", "#073642", "#93a1a1", "#586e75", "#268bd2", "#d33682", "#859900"),
    "sollight": ("#fdf6e3", "#eee8d5", "#586e75", "#93a1a1", "#268bd2", "#cb4b16", "#859900"),
    "onedark": ("#282c34", "#353b45", "#abb2bf", "#5c6370", "#61afef", "#e06c75", "#98c379"),
    "ayudark": ("#0b0e14", "#131721", "#bfbdb6", "#565b66", "#e6b450", "#f07178", "#7fd962"),
    "ayumirage": ("#1f2430", "#242936", "#cccac2", "#707a8c", "#ffcc66", "#f28779", "#87d96c"),
    "ayulight": ("#fcfcfc", "#eef0f2", "#5c6166", "#8a9199", "#fa8d3e", "#f07171", "#86b300"),
    "monokai": ("#272822", "#3e3d32", "#f8f8f2", "#75715e", "#f92672", "#66d9ef", "#a6e22e"),
    "material": ("#263238", "#2e3c43", "#eeffff", "#546e7a", "#82aaff", "#f07178", "#c3e88d"),
    "oxocarbon": ("#161616", "#262626", "#f2f4f8", "#6f6f6f", "#ff7eb6", "#33b1ff", "#42be65"),
    "nightfox": ("#192330", "#29394f", "#cdcecf", "#71839b", "#719cd6", "#c94f6d", "#81b29a"),
    "dawnfox": ("#faf4ed", "#ebe5df", "#575279", "#9893a5", "#286983", "#b4637a", "#618774"),
    "carbonfox": ("#161616", "#252525", "#f2f4f8", "#6e6f70", "#78a9ff", "#ee5396", "#25be6a"),
    "sonokai": ("#2c2e34", "#33353f", "#e2e2e3", "#7f8490", "#76cce0", "#fc5d7c", "#9ed072"),
    "edge": ("#2c2e34", "#363944", "#c5cdd9", "#7f8490", "#6cb6eb", "#ec7279", "#a0c980"),
    "melange": ("#292522", "#34302c", "#ece1d7", "#867462", "#e49b5d", "#bd8183", "#78997a"),
    "zenburn": ("#3f3f3f", "#4f4f4f", "#dcdccc", "#7f9f7f", "#f0dfaf", "#cc9393", "#8fb28f"),
    "horizon": ("#1c1e26", "#232530", "#d5d8da", "#6c6f93", "#e95678", "#fab795", "#29d398"),
    "palenight": ("#292d3e", "#34324a", "#a6accd", "#676e95", "#c792ea", "#ff5370", "#c3e88d"),
    "ghdark": ("#0d1117", "#161b22", "#c9d1d9", "#8b949e", "#58a6ff", "#f78166", "#3fb950"),
    "ghlight": ("#ffffff", "#f0f2f5", "#24292f", "#6e7781", "#0969da", "#cf222e", "#1a7f37"),
    "moonfly": ("#080808", "#1c1c1c", "#bdbdbd", "#808080", "#80a0ff", "#ff5454", "#8cc85f"),
    "nightowl": ("#011627", "#0b2942", "#d6deeb", "#637777", "#82aaff", "#c792ea", "#addb67"),
    "synthwave": ("#241b2f", "#34294f", "#f0eff1", "#848bbd", "#ff7edb", "#36f9f6", "#fede5d"),
    "cyberpunk": ("#000b1e", "#0a1a3a", "#0abdc6", "#3a5f8a", "#ea00d9", "#711c91", "#00ff9f"),
    "matrix": ("#000000", "#0a120a", "#b6ffb6", "#2e6b2e", "#00ff41", "#008f11", "#d1ffd1"),
    "amber": ("#140e00", "#241900", "#ffb000", "#8a5f00", "#ffcc00", "#ff6a00", "#ffe9a6"),
    "sakura": ("#fff5f7", "#fde2e7", "#5a3d47", "#a07b88", "#e86a92", "#c94f7c", "#7aa37a"),
    "matcha": ("#1e2420", "#2a322c", "#d6e2d1", "#7f8f80", "#9cc49b", "#e3c07a", "#7fb3a8"),
    "coffee": ("#1b1512", "#2a211c", "#e8d9c8", "#8c7a6b", "#c69c6d", "#a6644b", "#8fa37c"),
    "ocean": ("#0f1c2e", "#162a43", "#cfe3f2", "#6b86a0", "#4fb3d9", "#f28c6b", "#7bd6b0"),
    "forestnight": ("#101a14", "#18261d", "#d5e4d0", "#6f8a74", "#7fc87a", "#d9a45b", "#5fa8a0"),
    "desert": ("#2a1f1d", "#3a2b27", "#f2dccb", "#9c7e6e", "#f4a261", "#e76f51", "#2a9d8f"),
    "arctic": ("#f5f9fc", "#e3ecf3", "#1d2b36", "#6b7f8e", "#2b7bb9", "#d1495b", "#4c9a6a"),
    "lavender": ("#1f1b2e", "#2b2540", "#e5def7", "#8a80a8", "#b79cf2", "#f29cc4", "#8ce0d0"),
    "crimson": ("#120708", "#1f0d0f", "#f1dcdc", "#8a6667", "#e0243b", "#ff8a5c", "#f2f2f2"),
    "slate": ("#1e2227", "#2a2f36", "#d0d6de", "#7a838e", "#a3b8cc", "#e8a87c", "#9fc5a8"),
    "mono": ("#101010", "#1c1c1c", "#e0e0e0", "#6a6a6a", "#ffffff", "#bdbdbd", "#8a8a8a"),
    "monolight": ("#f2f2f2", "#e2e2e2", "#111111", "#777777", "#111111", "#555555", "#999999"),
    "vapor": ("#1d1135", "#2e1a52", "#f7e7ff", "#9b85c7", "#ff71ce", "#01cdfe", "#05ffa1"),
    "classic": ("#008080", "#c0c0c0", "#000000", "#808080", "#000080", "#ffffff", "#808080"),
    "hacker": ("#0a0e14", "#10161f", "#a8c7fa", "#4a5d78", "#00b4ff", "#ff3860", "#23d18b"),
    "autumn": ("#1d1611", "#2b211a", "#efdcc4", "#94806b", "#d97b3a", "#b8432f", "#c9a24a"),
    "mint": ("#f4fbf7", "#e1f2e8", "#1f3a2e", "#6b8a7a", "#2e9e6e", "#d95f5f", "#3b7fc4"),
    "sunset": ("#1e1424", "#2d1d35", "#f6e4f0", "#9d7fa8", "#ff8c61", "#ff5e8f", "#ffd166"),
    "aurora": ("#0b1120", "#121a30", "#dbe6ff", "#7083a8", "#6ee7b7", "#a78bfa", "#60a5fa"),
    "ink": ("#0d1021", "#171b33", "#e2e4f0", "#6b7194", "#e2e4f0", "#ff6b6b", "#7aa2ff"),
    "peach": ("#fff4ec", "#ffe3d1", "#4a2f27", "#a3847a", "#ff7a59", "#e04f5f", "#4f9d8e"),
    "teal": ("#0c1f1f", "#123030", "#d3eeea", "#5f8a86", "#2ec4b6", "#ff9f1c", "#cbf3f0"),
    "plum": ("#1b0f1e", "#2a1830", "#efdcf2", "#8f7096", "#d16ba5", "#86a8e7", "#5ffbf1"),
    "steel": ("#14181d", "#1e242b", "#c8d0d8", "#66717d", "#5b8def", "#f2c14e", "#4fc1a6"),
    "olive": ("#1c1d14", "#2a2c1e", "#e3e2c8", "#8a8a6a", "#b5b84a", "#d9853b", "#7a9a6a"),
    "glacier": ("#0e1a24", "#16283a", "#e6f4ff", "#7c97ad", "#9be7ff", "#ff9bb3", "#c3f584"),
}

FONTS = {  # key: (name shown, Arch package)
    "jbm": ("JetBrains Mono", "ttf-jetbrains-mono-nerd"),
    "fira": ("Fira Code", "ttf-firacode-nerd"),
    "plex": ("IBM Plex Mono", "ttf-ibmplex-mono-nerd"),
    "space": ("Space Mono", "ttf-space-mono-nerd"),
    "incon": ("Inconsolata", "ttf-inconsolata-nerd"),
    "scp": ("Source Code Pro", "ttf-sourcecodepro-nerd"),
    "victor": ("Victor Mono", "ttf-victor-mono-nerd"),
    "ubuntu": ("Ubuntu Mono", "ttf-ubuntu-mono-nerd"),
    "term": ("Terminus", "ttf-terminus-nerd"),
}

# name | wms | palette | wallpaper | bar | gaps,border,radius | flags | font | description
RICES = """
Grim Default|isoc|grim|logo|full|8,2,8|d|incon|The Grim OS default: black, a red reaper on the wallpaper, one red accent.
Reaper's Hour|is|grim|stars|pills|12,2,10||jbm|A black starfield with three floating pills. Red only where it matters.
Bone Paper|isoc|bone|logo|minimal|10,2,6|d|plex|Pale paper and black ink, with the red reaper as the only colour.
Crimson Vow|io|crimson|rings|island|14,3,12|s|space|Deep red-black with one centred island bar and soft shadows.
Ash|isoc|mono|flat|minimal|6,1,0||plex|Pure greyscale. No accent, no noise, square everything.
Chalk|isoc|monolight|paper|full|8,1,0||plex|Ash's light twin: white, black text, hairline borders.
Ink Well|is|ink|topo|under|10,2,4||jbm|Blue-black ink with contour lines and underlined workspaces.
Nord Snow|i|nordsnow|photo|full|10,2,0||incon|Your i3 screenshot: snowy forest, a cyan date block, square cyan outlines.
Polar Night|is|nordsnow|mount|pills|12,2,8||jbm|Nord over moonlit mountains, with the bar split into pills.
Frost Panel|oc|nordsnow|aurora|full|0,2,6|dt|scp|Floating Openbox windows under an aurora, with Plank at the bottom.
Snowdrift|isoc|nordlight|dunes|minimal|10,2,6||plex|Nord's light side: pale snow dunes and slate text.
Fjord|s|nordsnow|waves|float|14,2,0||jbm|Layered blue water and a floating Waybar.
Campfire|is|gruv|forest|blocks|8,2,0||jbm|Gruvbox warmth, powerline blocks and a pine silhouette.
Old Radio|ic|gruv|stripes|full|6,2,0||term|Warm stripes, a bitmap font and a chunky bar like a 70s receiver.
Hay Bale|isoc|gruvlight|dunes|pills|10,2,6|d|plex|Gruvbox light: cream fields and orange pills.
Ember|o|gruv|blobs|corners|0,2,8|st|scp|Glowing ember blobs, corner tabs and floating windows.
Mocha Float|is|mocha|blobs|pills|12,2,12||jbm|Pastel mauve pills over soft blurred colour.
Latte|isoc|latte|waves|full|10,2,10|d|plex|Catppuccin's bright latte with gentle waves.
Frappé Night|is|frappe|stars|island|12,2,10||fira|A single island bar under a pastel starfield.
Macchiato Garden|so|macchiato|forest|float|14,2,0||victor|Pink and teal over a soft pine forest.
Lavender Room|c|mocha|rings|taskbar|0,2,10|dt|scp|IceWM's taskbar in Catppuccin colours, with rounded windows.
Count's Study|is|dracula|city|blocks|8,2,6||fira|Dracula purples over a night skyline.
Bat Signal|oc|dracula|moon|full|0,2,8|st|jbm|A big moon and floating windows with purple title bars.
Velvet|s|dracula|blobs|split|10,2,0||victor|Two floating Waybar groups over velvet blobs.
Neon Tokyo|is|tokyo|city|pills|10,2,8||jbm|The Tokyo Night skyline with lit windows and blue pills.
Storm Drain|is|tokyostorm|rain|under|8,2,4||fira|Rain streaks and underlined workspaces.
Tokyo Morning|isoc|tokyoday|grad|minimal|10,2,8|d|plex|The light Tokyo theme: misty blue gradient and a quiet bar.
Shinjuku 3AM|o|tokyo|synth|corners|0,2,10|st|space|A synth grid and corner tabs for Openbox.
Rosé|is|rosepine|blobs|island|14,2,12||victor|Muted rose and iris with a centred island.
Moonlit Rosé|so|rosemoon|moon|float|12,2,0||jbm|Rosé Pine Moon with a pale moon over water.
Dawn Petals|isoc|rosedawn|petals|pills|10,2,10|d|plex|Rosé Pine Dawn with falling petals on parchment.
Rose Taskbar|c|rosepine|waves|taskbar|0,2,8|t|scp|IceWM's taskbar in rose and pine.
Pine Needle|is|everforest|forest|full|8,2,4||jbm|Everforest greens under a misty pine ridge.
Clearing|isoc|everlight|mount|minimal|10,2,8|d|plex|Everforest light: morning hills and a minimal bar.
Moss Box|o|everforest|blobs|side|0,2,8|dt|scp|A vertical tint2 bar on the left, moss-green accents.
Fern|s|everforest|topo|side|12,2,0||victor|Contour lines and a vertical Waybar on the left.
Great Wave|is|kanagawa|waves|blocks|8,2,4||jbm|Kanagawa ink-blue with a woodblock wave.
Dragon Scroll|isoc|kanadragon|mount|under|8,2,2||plex|Kanagawa Dragon: muted red and stone grey.
Lotus Pond|isoc|kanalotus|dunes|pills|10,2,8|d|plex|Kanagawa Lotus: rice paper and indigo.
Ukiyo Taskbar|c|kanagawa|sun|taskbar|0,2,4|t|scp|A rising sun behind IceWM's taskbar.
Deep Solar|is|soldark|grad|full|8,2,0||scp|Classic Solarized dark, done cleanly.
Bright Solar|isoc|sollight|paper|full|8,2,0|d|scp|Solarized light with a full bar and Plank.
Solar Flare|o|soldark|sun|corners|0,2,6|st|space|A big low sun behind floating Solarized windows.
Atom Night|is|onedark|grid|pills|10,2,8||jbm|One Dark on a faint grid.
Atom Bar|c|onedark|grad|taskbar|0,2,6|t|fira|One Dark colours on IceWM's taskbar.
Mirage|is|ayumirage|dunes|island|12,2,10||fira|Ayu Mirage's warm yellow over dusky dunes.
Ayu Midnight|is|ayudark|stars|under|8,1,0||jbm|Near-black with amber underlines.
Ayu Daylight|isoc|ayulight|grad|minimal|10,2,8|d|plex|Ayu light: white, orange accent, airy gaps.
Monokai Arcade|i|monokai|synth|blocks|8,2,0||space|Monokai's hot pink on a synth grid.
Monokai Pro Box|o|monokai|stripes|full|0,2,6|st|fira|Monokai stripes and floating windows with title bars.
Material Ocean|is|material|waves|pills|10,2,8||jbm|Material blue-grey with sea waves.
Oxocarbon|is|oxocarbon|tiles|under|8,2,0||plex|IBM Carbon pink and cyan on charcoal tiles.
Carbon Fiber|o|carbonfox|tiles|corners|0,2,6|st|plex|Carbonfox over a woven tile pattern.
Night Fox|is|nightfox|forest|blocks|8,2,4||fira|Nightfox blues and a forest at night.
Dawn Fox|isoc|dawnfox|petals|pills|10,2,8|d|victor|Dawnfox: parchment with dusty rose.
Sonokai|is|sonokai|blobs|pills|12,2,10||fira|Sonokai's candy accents on soft blobs.
Edge|is|edge|grad|full|8,2,6||jbm|The Edge scheme: calm blue and graphite.
Melange|is|melange|dunes|island|12,2,8||victor|Warm brown and amber, like an old library.
Zenburn|ic|zenburn|paper|full|6,2,0||term|Low-contrast grey-green, easy on the eyes all night.
Horizon|is|horizon|sun|pills|10,2,10||fira|Horizon's pink-coral sunset.
Palenight|is|palenight|stars|island|12,2,12||victor|Palenight lavender with a starry sky.
GitHub Night|is|ghdark|grid|full|8,1,4||jbm|GitHub dark: crisp borders, blue accent.
GitHub Day|isoc|ghlight|paper|full|8,1,6|d|plex|GitHub light: white, grey borders, blue links.
Moonfly|is|moonfly|moon|minimal|8,1,0||jbm|Pitch black, one moon, almost no bar.
Night Owl|is|nightowl|stars|pills|10,2,8||fira|Deep navy with an owl's-eye starfield.
Outrun|is|synthwave|synth|blocks|8,2,0||space|Synthwave: a sun, a grid, pink and cyan.
Night Drive|o|synthwave|city|corners|0,2,10|st|space|Neon skyline behind floating windows.
Netrunner|i|cyberpunk|circuit|under|6,2,0||jbm|Cyberpunk cyan and magenta over circuit traces.
Glitch City|s|cyberpunk|rain|full|8,2,0||space|Cyan rain and a magenta Waybar.
Matrix|i|matrix|rain|minimal|4,1,0||term|Green rain on black, bitmap font, no distractions.
Terminal Green|c|matrix|grid|taskbar|0,1,0|t|term|A green-phosphor IceWM taskbar.
Amber CRT|i|amber|scan|full|6,2,0||term|Amber phosphor with scanlines, like a 1983 terminal.
Amber Box|o|amber|scan|full|0,2,0|t|term|The amber CRT look for Openbox.
Sakura|isoc|sakura|petals|pills|12,2,12|d|victor|Cherry blossom pink on white with falling petals.
Hanami|s|sakura|petals|float|14,2,0||victor|A floating pink Waybar and blossoms.
Matcha|is|matcha|mount|island|12,2,10||plex|Soft green tea tones over misty hills.
Tea House|o|matcha|paper|side|0,2,8|dt|plex|A vertical tint2 bar in matcha green.
Espresso|is|coffee|blobs|pills|10,2,8||space|Roasted browns and crema highlights.
Café Taskbar|c|coffee|stripes|taskbar|0,2,6|t|scp|IceWM in coffee browns.
Deep Sea|is|ocean|waves|float|12,2,10||jbm|Navy water with a coral accent.
Tidepool|s|ocean|blobs|split|12,2,0||fira|Two floating groups over sea-glass blobs.
Night Forest|is|forestnight|forest|full|8,2,4||jbm|Dark woods with a green glow.
Firefly|o|forestnight|stars|corners|0,2,8|st|victor|Fireflies over a dark forest, floating windows.
Desert Dusk|is|desert|dunes|pills|10,2,8||space|Sandstone and teal at sunset.
Mirage Box|o|desert|sun|full|0,2,6|dt|space|A desert sun and Plank on Openbox.
Arctic|isoc|arctic|mount|minimal|10,2,8|d|plex|Ice-white and glacier blue.
Lavender Haze|is|lavender|blobs|island|14,2,14||victor|Soft violet haze and a centred island.
Violet Box|o|lavender|rings|corners|0,2,10|st|victor|Lavender rings and floating windows.
Blood Moon|is|crimson|moon|under|8,2,0||jbm|A red moon and blood-red underlines.
Slate|isoc|slate|grad|full|8,2,4|d|plex|Slate grey with a quiet steel-blue accent.
Vaporwave|is|vapor|synth|pills|12,2,10||space|Aesthetic pink and cyan.
Mall Soft|o|vapor|tiles|full|0,2,6|dt|space|Vaporwave tiles, Plank and floating windows.
Classic 95|c|classic|flat|taskbar|0,2,0|t|term|Teal desktop and a grey taskbar, the way IceWM was meant to look.
Classic Box|o|classic|flat|fullb|0,2,0|t|term|The 95 look on Openbox with a bottom bar.
Hacker|is|hacker|circuit|blocks|6,2,0||jbm|Electric blue on near-black with circuit lines.
Ops Room|s|hacker|grid|full|6,2,0||jbm|A blue status grid with a full Waybar.
Autumn|is|autumn|forest|pills|10,2,8||space|Rust, amber and falling-leaf browns.
Harvest Box|o|autumn|dunes|corners|0,2,8|st|space|Autumn fields with corner tabs.
Mint|isoc|mint|waves|pills|10,2,10|d|plex|Fresh mint on white.
Sunset Strip|is|sunset|sun|blocks|8,2,4||space|Peach-to-pink sunset with powerline blocks.
Aurora|is|aurora|aurora|island|12,2,12||jbm|Green and violet northern lights.
Peach|isoc|peach|blobs|pills|12,2,12|d|victor|Soft peach and coral, light and warm.
Teal Lagoon|is|teal|waves|float|12,2,8||fira|Teal water with an orange buoy accent.
Plum|is|plum|blobs|island|12,2,12||victor|Plum and periwinkle gradients.
Steel|isoc|steel|tiles|full|8,2,2|d|plex|Industrial steel blue with yellow warnings.
Olive Drab|ic|olive|topo|full|6,2,0||term|Military olive and contour lines.
Glacier|is|glacier|mount|pills|12,2,10||jbm|Glacier blue peaks and pale ice.
Graphite|isoc|mono|grid|under|8,2,4||jbm|Graphite with a white underline: monochrome with structure.
Newsprint|isoc|monolight|paper|blocks|8,1,0||plex|Black on white with sharp powerline blocks.
Red Ink|is|bone|topo|under|10,2,0||plex|Bone paper with a red underline and contour lines.
Scythe Moon|is|grim|moon|island|14,2,12||victor|Grim black with a red crescent moon.
Crypt|o|grim|tiles|side|0,2,6|dt|scp|A vertical tint2 bar and stone tiles, all black and red.
Requiem|c|grim|rings|taskbar|0,2,6|t|scp|Grim colours on IceWM's taskbar.
Tombstone|isoc|mono|logo|fullb|8,2,4|d|plex|Grey stone, bar at the bottom, the reaper faint on the wallpaper.
Polar Box|o|nordsnow|mount|fullb|0,2,6|dt|scp|Nord on Openbox with the bar at the bottom.
Snowfall|s|nordsnow|photo|float|12,2,0||incon|The Nord Snow wallpaper on Sway with a floating Waybar.
Nord Taskbar|c|nordsnow|photo|taskbar|0,2,0|t|incon|The Nord Snow look on IceWM's own taskbar.
Gruv Taskbar|c|gruv|forest|taskbar|0,2,0|t|term|Gruvbox on IceWM's taskbar, with a bitmap font.
Catppuccin Side|s|mocha|blobs|side|12,2,0||jbm|A vertical Waybar on the left in Catppuccin.
Tokyo Side|o|tokyo|city|side|0,2,8|dt|jbm|A vertical tint2 bar beside the Tokyo skyline.
Dracula Bottom|is|dracula|moon|fullb|8,2,6||fira|Dracula with the bar at the bottom.
Rosé Bottom|isoc|rosedawn|petals|fullb|10,2,8|d|plex|Rosé Dawn with a bottom bar and Plank.
Forest Floor|is|everforest|forest|fullb|8,2,4||jbm|Everforest with the bar at the bottom.
Kanagawa Float|s|kanagawa|waves|float|12,2,0||jbm|The great wave behind a floating Waybar.
Solar Split|s|soldark|grad|split|10,2,0||scp|Solarized dark with two floating Waybar groups.
Ayu Split|s|ayumirage|dunes|split|12,2,0||fira|Ayu Mirage with split Waybar groups.
Horizon Box|o|horizon|sun|full|0,2,10|st|fira|Horizon's sunset on Openbox with soft shadows.
Owl Box|o|nightowl|stars|corners|0,2,8|st|fira|Night Owl stars with corner tabs.
GitHub Box|o|ghdark|grid|full|0,1,6|dt|jbm|GitHub dark on Openbox with Plank.
Material Box|o|material|waves|fullb|0,2,6|dt|jbm|Material blue-grey, bottom bar and Plank.
Edge Taskbar|c|edge|grad|taskbar|0,2,6|t|jbm|The Edge scheme on IceWM's taskbar.
Palenight Taskbar|c|palenight|stars|taskbar|0,2,8|t|victor|Palenight on IceWM's taskbar.
Sonokai Box|o|sonokai|blobs|island|0,2,10|st|fira|Sonokai with a centred Polybar island on Openbox.
Melange Taskbar|c|melange|paper|taskbar|0,2,4|t|space|Warm melange browns on IceWM.
Synth Taskbar|c|synthwave|synth|taskbar|0,2,6|t|space|An outrun grid behind IceWM's taskbar.
Cyber Box|o|cyberpunk|circuit|corners|0,2,0|st|space|Cyberpunk corner tabs over circuit traces.
Matcha Taskbar|c|matcha|mount|taskbar|0,2,8|t|plex|Green tea tones on IceWM.
Ocean Taskbar|c|ocean|waves|taskbar|0,2,8|t|jbm|IceWM's taskbar on deep sea blue.
Desert Taskbar|c|desert|dunes|taskbar|0,2,6|t|space|Sandstone IceWM.
Lavender Taskbar|c|lavender|blobs|taskbar|0,2,10|t|victor|Lavender IceWM with rounded windows.
Vapor Taskbar|c|vapor|grid|taskbar|0,2,6|t|space|Vaporwave IceWM.
Steel Box|o|steel|tiles|fullb|0,2,2|dt|plex|Industrial steel Openbox with a bottom bar.
Glacier Box|o|glacier|mount|corners|0,2,10|st|jbm|Glacier peaks with corner tabs.
Plum Split|s|plum|blobs|split|14,2,0||victor|Plum gradients with split Waybar groups.
Teal Side|s|teal|waves|side|12,2,0||fira|A vertical teal Waybar.
Autumn Split|s|autumn|forest|split|10,2,0||space|Autumn colours, split Waybar groups.
Mint Box|o|mint|waves|corners|0,2,10|ds|plex|Fresh mint on Openbox with Plank.
Peach Taskbar|c|peach|blobs|taskbar|0,2,10|t|victor|Peach and coral IceWM.
Sunset Box|o|sunset|sun|island|0,2,10|st|space|A sunset island bar on Openbox.
Aurora Side|o|aurora|aurora|side|0,2,10|dt|jbm|Northern lights with a vertical tint2 bar.
"""

def parse():
    out = []
    for i, line in enumerate(l for l in RICES.strip().splitlines() if l.strip()):
        name, wms, pal, wall, bar, nums, flags, font, desc = line.split("|")
        g, b, r = (int(x) for x in nums.split(","))
        assert pal in PALETTES, (name, pal)
        assert font in FONTS, (name, font)
        assert not (bar == "taskbar" and wms != "c"), f"{name}: taskbar is IceWM only"
        assert not (bar == "side" and set(wms) - set("so")), f"{name}: vertical bars need Sway or Openbox"
        assert not (wms == "s" and r), f"{name}: Sway can't round corners"
        out.append(dict(n=i + 1, name=name, wms=wms, pal=pal, wall=wall, bar=bar, gaps=g, border=b,
                        radius=r, flags=flags, font=font, desc=desc))
    return out


if __name__ == "__main__":
    rs = parse()
    names = [r["name"] for r in rs]
    assert len(set(names)) == len(names), "duplicate names"
    print(len(rs), "rices,", len({r['pal'] for r in rs}), "palettes used")
