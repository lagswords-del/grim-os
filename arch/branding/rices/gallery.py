"""Builds rice-gallery.html from rices.py: python3 gallery.py"""
import base64, json, os
import rices

HERE = os.path.dirname(os.path.abspath(__file__))
photo = ""
p = "/tmp/claude-1000/snow-small.jpg"
if os.path.exists(p):
    photo = "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

data = {
    "palettes": rices.PALETTES,
    "fonts": {k: v[0] for k, v in rices.FONTS.items()},
    "fontpkg": {k: v[1] for k, v in rices.FONTS.items()},
    "rices": rices.parse(),
    "photo": photo,
}

HTML = r"""<title>Grim Rice Catalogue</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&family=Fira+Code:wght@500&family=IBM+Plex+Mono:wght@500&family=Space+Mono:wght@700&family=Inconsolata:wght@600&family=Source+Code+Pro:wght@500&family=Victor+Mono:wght@600&family=Ubuntu+Mono:wght@700&family=VT323&display=swap">
<style>
/* Layout: a catalogue wall. Sticky filter strip, then a dense grid of screen cards; each card is a drawn desktop plus its spec sheet. */
:root {
  --bg: #f3f2ef; --panel: #ffffff; --ink: #16161a; --muted: #67676f; --line: #dddcd7; --accent: #b3101c; --chip: #ecebe7;
  --display: "Bricolage Grotesque", "Helvetica Neue", Arial, sans-serif;
  --body: "Inter", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #0d0d0f; --panel: #151518; --ink: #ecebe8; --muted: #9a9aa3; --line: #26262b; --accent: #e0303d; --chip: #1d1d21; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #0d0d0f; --panel: #151518; --ink: #ecebe8; --muted: #9a9aa3; --line: #26262b; --accent: #e0303d; --chip: #1d1d21; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 14px/1.5 var(--body);
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 64px; }
main { max-width: 1440px; margin: 0 auto; display: grid; gap: 24px; }
header { display: grid; gap: 10px; max-width: 900px; }
.eyebrow { font: 500 12px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
h1 { font: 800 clamp(34px, 5.5vw, 60px)/1 var(--display); letter-spacing: -.02em; margin: 0; text-wrap: balance; }
.lede { color: var(--muted); max-width: 70ch; margin: 0; }
.rules { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 12.5px; color: var(--muted); margin: 0; padding: 0; list-style: none; }
.rules b { color: var(--ink); font-weight: 600; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); padding-block: 10px; border-bottom: 1px solid var(--line);
  display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; }
.group { display: inline-flex; gap: 4px; flex-wrap: wrap; }
.chipbtn { font: 500 13px var(--body); color: var(--ink); background: var(--chip); border: 1px solid transparent; border-radius: 999px; padding: 6px 12px; cursor: pointer; }
.chipbtn[aria-pressed="true"] { background: var(--ink); color: var(--bg); }
.chipbtn:focus-visible, .act:focus-visible, #q:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
#q { font: 14px var(--body); color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 7px 10px; width: min(240px, 100%); }
.count { font: 500 12.5px var(--mono); color: var(--muted); margin-left: auto; font-variant-numeric: tabular-nums; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 18px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: grid; grid-template-rows: auto 1fr; min-width: 0; }
.card svg { display: block; width: 100%; height: auto; aspect-ratio: 16 / 10; }
.info { padding: 12px 14px 14px; display: grid; gap: 8px; align-content: start; min-width: 0; }
.top { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.num { font: 500 11px var(--mono); color: var(--muted); font-variant-numeric: tabular-nums; }
.name { font: 700 18px/1.15 var(--display); margin: 0; letter-spacing: -.01em; }
.wms { display: flex; gap: 4px; flex-wrap: wrap; margin-left: auto; }
.wm { font: 500 10.5px var(--mono); padding: 2px 6px; border-radius: 4px; background: var(--chip); color: var(--ink); }
.desc { margin: 0; color: var(--muted); font-size: 13px; }
.sw { display: flex; gap: 0; height: 10px; border-radius: 3px; overflow: hidden; border: 1px solid var(--line); }
.sw i { flex: 1; }
.spec { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; font-size: 12px; margin: 0; }
.spec dt { color: var(--muted); }
.spec dd { margin: 0; font-family: var(--mono); font-size: 11.5px; overflow-wrap: anywhere; }
.note { font-size: 11.5px; color: var(--muted); margin: 0; }
.acts { display: flex; gap: 6px; margin-top: 2px; }
.act { font: 500 12.5px var(--body); color: var(--ink); background: var(--chip); border: 1px solid var(--line); border-radius: 6px; padding: 5px 10px; cursor: pointer; }
.act.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.empty { color: var(--muted); padding: 40px 0; text-align: center; }
footer { color: var(--muted); font-size: 12.5px; }
code { font: 12px var(--mono); }
</style>

<main>
<header>
  <span class="eyebrow">Grim OS 1.0.1 · grim-rice</span>
  <h1>Grim Rice Catalogue</h1>
  <p class="lede">150 rices for i3, Sway, IceWM and Openbox. Each preview is drawn from the rice's own settings: palette, wallpaper, bar layout, gaps, borders, corners, title bars and dock. Star the ones you like, then copy your shortlist and paste it to Claude to have them built into grim-rice.</p>
  <ul class="rules">
    <li><b>Bars:</b> Polybar on i3, Openbox, IceWM · Waybar on Sway · IceWM's own taskbar</li>
    <li><b>Corners:</b> picom on X11, always square on Sway</li>
    <li><b>Vertical bars:</b> Waybar on Sway, tint2 on Openbox</li>
  </ul>
</header>

<div class="bar" role="toolbar" aria-label="Filters">
  <input id="q" type="search" placeholder="Search names, colours, moods" aria-label="Search rices">
  <div class="group" id="wmf" aria-label="Window manager">
    <button class="chipbtn" data-wm="" aria-pressed="true">All</button>
    <button class="chipbtn" data-wm="i" aria-pressed="false">i3</button>
    <button class="chipbtn" data-wm="s" aria-pressed="false">Sway</button>
    <button class="chipbtn" data-wm="c" aria-pressed="false">IceWM</button>
    <button class="chipbtn" data-wm="o" aria-pressed="false">Openbox</button>
  </div>
  <div class="group" id="lf" aria-label="Light or dark">
    <button class="chipbtn" data-l="" aria-pressed="true">Any</button>
    <button class="chipbtn" data-l="dark" aria-pressed="false">Dark</button>
    <button class="chipbtn" data-l="light" aria-pressed="false">Light</button>
  </div>
  <div class="group">
    <button class="chipbtn" id="starsonly" aria-pressed="false">★ Shortlist only</button>
    <button class="chipbtn" id="copylist" aria-pressed="false">Copy shortlist</button>
  </div>
  <span class="count" id="count">150 rices</span>
</div>

<div class="grid" id="grid"></div>
<p class="empty" id="empty" hidden>No rice matches these filters.</p>
<footer>Source: <code>grimos/branding/rices/rices.py</code> (the data) and <code>gallery.py</code> (this page).</footer>
</main>

<script>
const DATA = __DATA__;
const WMNAME = { i: "i3", s: "Sway", c: "IceWM", o: "Openbox" };
const BARNAME = { full: "full width, top", fullb: "full width, bottom", pills: "three pills", island: "one centred island",
  minimal: "minimal, no background", corners: "corner tabs", blocks: "powerline blocks", under: "underlined workspaces",
  float: "floating, rounded", split: "two groups", taskbar: "IceWM taskbar", side: "vertical, left" };
const PREVIEW_FONT = { jbm: "'JetBrains Mono'", fira: "'Fira Code'", plex: "'IBM Plex Mono'", space: "'Space Mono'",
  incon: "Inconsolata", scp: "'Source Code Pro'", victor: "'Victor Mono'", ubuntu: "'Ubuntu Mono'", term: "VT323" };

// ---------------------------------------------------------------- colour helpers
const hex2 = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, t) => { const x = hex2(a), y = hex2(b); return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join(""); };
const lum = h => { const [r, g, b] = hex2(h); return (0.299 * r + 0.587 * g + 0.114 * b) / 255; };
function rng(seed) { let s = seed * 9301 + 49297; return () => ((s = (s * 9301 + 49297) % 233280) / 233280); }

// ---------------------------------------------------------------- wallpapers (320 x 200)
function wall(kind, P, R, id) {
  const W = 320, H = 200, out = [];
  const sky = (a, b) => { out.push(`<defs><linearGradient id="g${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#g${id})"/>`); };
  const blur = sd => `<defs><filter id="b${id}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="${sd}"/></filter></defs>`;
  const stars = (n, col) => { for (let i = 0; i < n; i++) out.push(`<circle cx="${(R() * W).toFixed(1)}" cy="${(R() * H * .75).toFixed(1)}" r="${(R() * .9 + .2).toFixed(2)}" fill="${col}" opacity="${(R() * .7 + .2).toFixed(2)}"/>`); };
  switch (kind) {
    case "photo":
      out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      if (DATA.photo) out.push(`<image href="${DATA.photo}" width="${W}" height="${H}" preserveAspectRatio="xMidYMid slice"/>`);
      break;
    case "flat": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`); break;
    case "grad": sky(mix(P.bg, P.ac, .18), P.bg); out.push(`<circle cx="250" cy="40" r="120" fill="${P.a2}" opacity=".08"/>`); break;
    case "paper": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`); for (let y = 4; y < H; y += 5) out.push(`<rect y="${y}" width="${W}" height=".5" fill="${P.fg}" opacity=".035"/>`); break;
    case "logo": {
      sky(mix(P.bg, P.sf, .6), P.bg);
      const ring = mix(P.bg, P.fg, lum(P.bg) > .5 ? .85 : .12);
      out.push(`<g transform="translate(160 104)"><circle r="34" fill="none" stroke="${ring}" stroke-width="9" stroke-dasharray="88 8 110 8"/>
        <path d="M-2 -22 C-14 -20 -18 -8 -18 4 L-24 24 L24 24 L18 4 C18 -10 10 -20 -2 -22 Z" fill="${P.ac}"/>
        <path d="M14 -24 C2 -32 -16 -28 -24 -18" stroke="${P.ac}" stroke-width="3" fill="none"/></g>`); break; }
    case "stars": sky(P.bg, mix(P.bg, P.sf, .8)); stars(70, P.fg); break;
    case "moon": sky(P.bg, mix(P.bg, P.a2, .25)); stars(45, P.fg);
      out.push(`<circle cx="236" cy="62" r="26" fill="${mix(P.fg, P.ac, .25)}"/><circle cx="246" cy="56" r="22" fill="${mix(P.bg, P.a2, .12)}" opacity=".0"/>
        <circle cx="228" cy="56" r="4" fill="${P.bg}" opacity=".12"/><circle cx="242" cy="72" r="6" fill="${P.bg}" opacity=".1"/>
        <rect x="200" y="170" width="70" height="1.4" fill="${P.fg}" opacity=".25"/><rect x="214" y="176" width="44" height="1.2" fill="${P.fg}" opacity=".18"/>
        <rect y="160" width="${W}" height="40" fill="${P.bg}" opacity=".55"/>`); break;
    case "mount": {
      sky(mix(P.bg, P.ac, .25), P.bg);
      out.push(`<circle cx="230" cy="60" r="14" fill="${mix(P.fg, P.ac, .3)}" opacity=".85"/>`);
      [[.25, 110, .55], [.5, 135, .75], [.8, 160, .95]].forEach(([t, base, d], k) => {
        let pts = `0,${H} 0,${base}`; let x = 0;
        while (x < W) { x += 20 + R() * 35; pts += ` ${x.toFixed(0)},${(base - 18 - R() * 45 * (1 - k * .25)).toFixed(0)}`; x += 15 + R() * 25; pts += ` ${x.toFixed(0)},${(base + R() * 10).toFixed(0)}`; }
        out.push(`<polygon points="${pts} ${W},${H}" fill="${mix(mix(P.bg, P.sf, d), P.ac, t * .25)}"/>`);
      }); break; }
    case "dunes": sky(mix(P.bg, P.ac, .35), mix(P.bg, P.a2, .15));
      out.push(`<circle cx="90" cy="70" r="20" fill="${P.a3}" opacity=".35"/>`);
      [[120, .3], [145, .55], [172, .8]].forEach(([y, t]) => out.push(`<path d="M0 ${y} Q 80 ${y - 30} 160 ${y - 4} T 320 ${y - 12} V 200 H 0 Z" fill="${mix(mix(P.bg, P.sf, t), P.ac, .25 * t)}"/>`)); break;
    case "waves": sky(mix(P.bg, P.ac, .12), P.bg);
      [.18, .3, .44, .6].forEach((t, k) => { const y = 95 + k * 24; out.push(`<path d="M0 ${y} Q 40 ${y - 14} 80 ${y} T 160 ${y} T 240 ${y} T 320 ${y} V 200 H 0 Z" fill="${mix(P.bg, P.ac, t)}" opacity=".85"/>`); }); break;
    case "forest": sky(mix(P.bg, P.ac, .18), P.bg);
      out.push(`<rect y="110" width="${W}" height="30" fill="${P.fg}" opacity=".05"/>`);
      [[150, .5, 22], [185, .85, 30]].forEach(([base, d, h]) => { for (let x = -8; x < W + 8; x += 9 + R() * 9) { const hh = h + R() * 26; out.push(`<polygon points="${x},${base} ${x + 7},${base - hh} ${x + 14},${base}" fill="${mix(P.bg, P.sf, d)}"/>`); } out.push(`<rect y="${base}" width="${W}" height="${H - base}" fill="${mix(P.bg, P.sf, d)}"/>`); }); break;
    case "city": sky(mix(P.bg, P.a2, .3), P.bg); stars(25, P.fg);
      for (let x = 0; x < W;) { const w = 14 + R() * 22, h = 40 + R() * 80; out.push(`<rect x="${x.toFixed(0)}" y="${(H - h).toFixed(0)}" width="${w.toFixed(0)}" height="${h.toFixed(0)}" fill="${mix(P.bg, P.sf, .7)}"/>`);
        for (let wy = H - h + 6; wy < H - 6; wy += 7) for (let wx = x + 3; wx < x + w - 4; wx += 5) if (R() < .28) out.push(`<rect x="${wx.toFixed(1)}" y="${wy.toFixed(1)}" width="2" height="3" fill="${R() < .7 ? P.ac : P.a3}" opacity=".8"/>`);
        x += w + 2; } break;
    case "synth": out.push(`<defs><linearGradient id="g${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.bg}"/><stop offset=".55" stop-color="${mix(P.bg, P.a2, .35)}"/><stop offset=".55" stop-color="${P.bg}"/></linearGradient>
        <linearGradient id="s${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.a3}"/><stop offset="1" stop-color="${P.ac}"/></linearGradient></defs>
        <rect width="${W}" height="${H}" fill="url(#g${id})"/><circle cx="160" cy="110" r="42" fill="url(#s${id})"/>`);
      for (let k = 0; k < 6; k++) out.push(`<rect x="110" y="${84 + k * 5}" width="100" height="${k * .6 + .6}" fill="${mix(P.bg, P.a2, .35)}"/>`);
      out.push(`<rect y="110" width="${W}" height="90" fill="${P.bg}"/>`);
      for (let k = 0; k < 8; k++) out.push(`<rect y="${110 + k * k * 1.6}" width="${W}" height=".7" fill="${P.ac}" opacity=".7"/>`);
      for (let k = -10; k <= 10; k++) out.push(`<line x1="${160 + k * 9}" y1="110" x2="${160 + k * 50}" y2="200" stroke="${P.ac}" stroke-width=".6" opacity=".7"/>`); break;
    case "grid": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      for (let x = 0; x <= W; x += 16) out.push(`<rect x="${x}" width=".5" height="${H}" fill="${P.ac}" opacity=".13"/>`);
      for (let y = 0; y <= H; y += 16) out.push(`<rect y="${y}" width="${W}" height=".5" fill="${P.ac}" opacity=".13"/>`); break;
    case "tiles": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      for (let y = 0; y < H; y += 20) for (let x = 0; x < W; x += 20) { const t = R() * .5; out.push(`<polygon points="${x},${y} ${x + 20},${y} ${x},${y + 20}" fill="${mix(P.bg, P.sf, t)}"/><polygon points="${x + 20},${y} ${x + 20},${y + 20} ${x},${y + 20}" fill="${mix(P.bg, R() < .08 ? P.ac : P.sf, R() * .45)}"/>`); } break;
    case "topo": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      [[90, 80], [240, 140]].forEach(([cx, cy]) => { for (let k = 1; k < 9; k++) { const r = k * 13, j = () => (R() * 6 - 3).toFixed(1);
        out.push(`<path d="M${cx - r} ${cy} C ${cx - r} ${cy - r * .7 + +j()}, ${cx + r * .8} ${cy - r + +j()}, ${cx + r} ${cy} S ${cx - r * .6} ${cy + r * .9 + +j()}, ${cx - r} ${cy} Z" fill="none" stroke="${k === 4 ? P.ac : P.mu}" stroke-width=".7" opacity="${k === 4 ? .7 : .35}"/>`); } }); break;
    case "circuit": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      for (let k = 0; k < 26; k++) { let x = Math.round(R() * 20) * 16, y = Math.round(R() * 12) * 16, d = `M${x} ${y}`;
        for (let s = 0; s < 3; s++) { if (R() < .5) x += (R() < .5 ? -1 : 1) * 16 * (1 + Math.floor(R() * 3)); else y += (R() < .5 ? -1 : 1) * 16 * (1 + Math.floor(R() * 2)); d += ` L${x} ${y}`; }
        out.push(`<path d="${d}" stroke="${R() < .3 ? P.a2 : P.ac}" stroke-width=".8" fill="none" opacity=".45"/><circle cx="${x}" cy="${y}" r="1.6" fill="${P.ac}" opacity=".7"/>`); } break;
    case "rings": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      for (let k = 1; k < 10; k++) out.push(`<circle cx="250" cy="150" r="${k * 18}" fill="none" stroke="${k % 3 ? P.mu : P.ac}" stroke-width="${k % 3 ? .6 : 1.4}" opacity="${k % 3 ? .3 : .6}"/>`); break;
    case "blobs": out.push(blur(28) + `<rect width="${W}" height="${H}" fill="${P.bg}"/><g filter="url(#b${id})" opacity=".75">
        <circle cx="80" cy="60" r="60" fill="${P.ac}"/><circle cx="250" cy="70" r="55" fill="${P.a2}"/><circle cx="180" cy="170" r="60" fill="${P.a3}"/></g>
        <rect width="${W}" height="${H}" fill="${P.bg}" opacity=".35"/>`); break;
    case "aurora": out.push(blur(7) + `<rect width="${W}" height="${H}" fill="${P.bg}"/>`); stars(30, P.fg);
      out.push(`<g filter="url(#b${id})"><path d="M-20 90 C 60 20, 120 120, 200 50 S 300 40, 340 70" stroke="${P.ac}" stroke-width="22" fill="none" opacity=".55"/>
        <path d="M-20 120 C 70 70, 150 140, 230 90 S 320 90, 340 100" stroke="${P.a2}" stroke-width="16" fill="none" opacity=".45"/></g>`); break;
    case "rain": sky(mix(P.bg, P.sf, .7), P.bg);
      for (let k = 0; k < 110; k++) out.push(`<rect x="${(R() * W).toFixed(1)}" y="${(R() * H).toFixed(1)}" width=".6" height="${(4 + R() * 10).toFixed(1)}" fill="${R() < .25 ? P.ac : P.fg}" opacity="${(R() * .3 + .1).toFixed(2)}"/>`); break;
    case "petals": sky(P.bg, mix(P.bg, P.ac, .1));
      for (let k = 0; k < 34; k++) out.push(`<ellipse cx="${(R() * W).toFixed(0)}" cy="${(R() * H).toFixed(0)}" rx="${(2 + R() * 2.5).toFixed(1)}" ry="${(1.2 + R()).toFixed(1)}" transform="rotate(${(R() * 180).toFixed(0)} ${(R() * W).toFixed(0)} ${(R() * H).toFixed(0)})" fill="${R() < .5 ? P.ac : P.a2}" opacity="${(R() * .4 + .3).toFixed(2)}"/>`); break;
    case "sun": sky(mix(P.bg, P.ac, .3), mix(P.bg, P.a2, .15));
      out.push(`<circle cx="160" cy="132" r="52" fill="${P.ac}" opacity=".9"/><rect y="132" width="${W}" height="68" fill="${mix(P.bg, P.sf, .6)}"/>`);
      for (let k = 0; k < 6; k++) out.push(`<rect x="${120 - k * 6}" y="${138 + k * 9}" width="${80 + k * 12}" height="1.4" fill="${P.ac}" opacity="${(.5 - k * .07).toFixed(2)}"/>`); break;
    case "stripes": out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
      [P.ac, P.a2, P.a3].forEach((c, k) => out.push(`<polygon points="${120 + k * 34},${H} ${190 + k * 34},${H} ${330},${80 + k * 34 - 70} ${330},${10 + k * 34 - 70 > -40 ? 10 + k * 34 - 70 : -40}" fill="${c}" opacity=".85"/>`)); break;
    case "scan": out.push(`<defs><radialGradient id="v${id}"><stop offset=".55" stop-color="${P.bg}" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient></defs>
        <rect width="${W}" height="${H}" fill="${mix(P.bg, P.ac, .06)}"/>`);
      for (let y = 0; y < H; y += 2.4) out.push(`<rect y="${y}" width="${W}" height=".9" fill="#000" opacity=".25"/>`);
      out.push(`<rect width="${W}" height="${H}" fill="url(#v${id})"/>`); break;
    default: out.push(`<rect width="${W}" height="${H}" fill="${P.bg}"/>`);
  }
  return out.join("");
}

// ---------------------------------------------------------------- desktop on top
function desktop(r, P, R) {
  const W = 320, H = 200, out = [];
  const tiling = "is".includes(r.wms[0]);
  const swayOnly = r.wms === "s";
  const rad = swayOnly ? 0 : r.radius * .45;
  const bw = Math.max(.7, r.border * .55);
  const gap = Math.max(r.gaps * .7, r.wms.match(/^[is]/) ? 3 : 0);
  const font = PREVIEW_FONT[r.font] || "monospace";
  const light = lum(P.bg) > .5;
  const barBg = r.bar === "minimal" ? "none" : P.bg;
  const area = { x: 0, y: 0, w: W, h: H };
  const top = !["fullb", "taskbar", "side"].includes(r.bar);
  if (top) { area.y = r.bar === "corners" ? 13 : (["pills", "island", "float", "split"].includes(r.bar) ? 16 : 11); }
  if (r.bar === "fullb") area.h -= 11;
  if (r.bar === "taskbar") area.h -= 14;
  if (r.bar === "side") { area.x = 14; area.w -= 14; }
  area.h -= area.y;
  const dock = r.flags.includes("d") && r.bar !== "taskbar";
  if (dock) area.h -= 15;

  const shadow = r.flags.includes("s") ? `filter="url(#sh${r.n})"` : "";
  if (shadow) out.push(`<defs><filter id="sh${r.n}" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity=".45"/></filter></defs>`);

  // ---- windows
  const textLines = (x, y, w, h, kind) => {
    const o = [];
    if (kind === "term") {
      // fetch-style: little art + labelled lines
      const cell = 2.3;
      for (let yy = 0; yy < 7; yy++) for (let xx = 0; xx < 7; xx++) if (R() < .55) o.push(`<rect x="${(x + 5 + xx * cell).toFixed(1)}" y="${(y + 6 + yy * cell).toFixed(1)}" width="${cell - .3}" height="${cell - .3}" fill="${yy < 3 ? P.ac : P.a2}"/>`);
      for (let k = 0; k < 6; k++) { const ly = y + 6 + k * 3.2; o.push(`<rect x="${x + 25}" y="${ly}" width="${8 + R() * 4}" height="1.6" fill="${P.ac}"/><rect x="${x + 38}" y="${ly}" width="${Math.min(w - 45, 14 + R() * 28)}" height="1.6" fill="${P.fg}" opacity=".75"/>`); }
      for (let k = 0; k < 8; k++) o.push(`<rect x="${x + 25 + k * 3.6}" y="${y + 27}" width="3" height="2.2" fill="${[P.bg, P.ac, P.a3, P.a2, P.mu, P.fg, P.sf, P.ac][k]}"/>`);
      const py = y + Math.min(h - 6, 36);
      o.push(`<rect x="${x + 5}" y="${py}" width="6" height="1.8" fill="${P.a3}"/><rect x="${x + 13}" y="${py}" width="${Math.min(w - 20, 30)}" height="1.8" fill="${P.fg}" opacity=".6"/><rect x="${x + 45}" y="${py - .3}" width="1.4" height="2.4" fill="${P.fg}"/>`);
    } else if (kind === "code") {
      for (let k = 0; k * 3.4 + 6 < h - 3; k++) { const ly = y + 5 + k * 3.4; let xx = x + 11; o.push(`<rect x="${x + 4}" y="${ly}" width="4" height="1.5" fill="${P.mu}" opacity=".6"/>`);
        const indent = (k % 4) * 3; xx += indent;
        for (let s = 0; s < 3 && xx < x + w - 8; s++) { const ww = 4 + R() * 12; o.push(`<rect x="${xx.toFixed(1)}" y="${ly}" width="${Math.min(ww, x + w - 5 - xx).toFixed(1)}" height="1.5" fill="${[P.ac, P.fg, P.a2, P.a3][Math.floor(R() * 4)]}" opacity=".85"/>`); xx += ww + 2; } }
    } else {
      for (let k = 0; k * 5 + 6 < h - 2; k++) { const ly = y + 4 + k * 5; o.push(`<rect x="${x + 4}" y="${ly}" width="3" height="3" rx=".6" fill="${k % 3 ? P.a2 : P.ac}" opacity=".9"/><rect x="${x + 9}" y="${ly + .7}" width="${Math.min(w - 14, 16 + R() * 20)}" height="1.6" fill="${k === 1 ? P.ac : P.fg}" opacity="${k === 1 ? 1 : .65}"/>`); }
    }
    return o.join("");
  };
  const win = (x, y, w, h, kind, active, title) => {
    const o = [], th = title ? 7 : 0, bc = active ? P.ac : mix(P.bg, P.mu, .5);
    const bcol = r.wms.match(/^[is]/) ? (active ? P.ac : mix(P.bg, P.fg, .18)) : bc;
    o.push(`<g ${shadow}><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rad}" fill="${P.bg}" opacity="${r.flags.includes("a") ? .72 : (light ? .9 : .84)}"/>`);
    if (title) {
      o.push(`<path d="M${x} ${y + th} V${y + rad} Q${x} ${y} ${x + rad} ${y} H${x + w - rad} Q${x + w} ${y} ${x + w} ${y + rad} V${y + th} Z" fill="${active ? P.sf : mix(P.bg, P.sf, .5)}"/>`);
      o.push(`<rect x="${x + 5}" y="${y + 2.8}" width="${Math.min(30, w * .3)}" height="1.6" fill="${active ? P.fg : P.mu}" opacity=".8"/>`);
      if (!tiling) [0, 1, 2].forEach(k => o.push(`<circle cx="${x + w - 5 - k * 5}" cy="${y + 3.5}" r="1.4" fill="${k === 0 ? P.ac : P.mu}" opacity="${k === 0 && active ? 1 : .6}"/>`));
    }
    o.push(textLines(x, y + th, w, h - th, kind));
    o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rad}" fill="none" stroke="${bcol}" stroke-width="${bw}"/></g>`);
    return o.join("");
  };
  const titles = r.flags.includes("t");
  if (tiling) {
    const x0 = area.x + gap, y0 = area.y + gap, w0 = area.w - gap * 2, h0 = area.h - gap * 2;
    const lw = Math.round(w0 * .56 - gap / 2);
    out.push(win(x0, y0, lw, h0, "term", true, titles));
    const rx = x0 + lw + gap, rw = w0 - lw - gap, rh = (h0 - gap) * .55;
    out.push(win(rx, y0, rw, rh, "code", false, titles));
    out.push(win(rx, y0 + rh + gap, rw, h0 - rh - gap, "list", false, titles));
  } else {
    out.push(win(area.x + 150, area.y + 34, 140, Math.min(92, area.h - 44), "list", false, true));
    out.push(win(area.x + 26, area.y + 16, 168, Math.min(104, area.h - 26), "term", true, true));
  }

  // ---- dock
  if (dock) {
    const dw = 92, dx = (W - dw) / 2, dy = (r.bar === "fullb" ? H - 11 : H) - 14;
    out.push(`<rect x="${dx}" y="${dy}" width="${dw}" height="12" rx="4" fill="${P.sf}" opacity=".92"/>`);
    [P.ac, P.a2, P.a3, P.fg, P.mu, P.ac, P.a2].forEach((c, k) => out.push(`<rect x="${dx + 5 + k * 12.2}" y="${dy + 2.5}" width="7" height="7" rx="1.8" fill="${c}" opacity="${k === 3 ? .8 : .95}"/>`));
    out.push(`<circle cx="${dx + 8.5}" cy="${dy + 11}" r=".7" fill="${P.fg}"/>`);
  }

  // ---- bar
  const clock = (x, y, anchor = "middle", col = P.fg) => `<text x="${x}" y="${y}" font-family="${font}, monospace" font-size="5.6" font-weight="600" fill="${col}" text-anchor="${anchor}">${r.font === "term" ? "21:04" : "21:04"}</text>`;
  const wsBoxes = (x, y, style = "box") => { const o = []; for (let k = 0; k < 5; k++) { const on = k === 0, cx = x + k * 8;
      if (style === "under") { o.push(`<text x="${cx + 2}" y="${y + 4.6}" font-family="${font}, monospace" font-size="5" fill="${on ? P.fg : P.mu}" text-anchor="middle">${k + 1}</text>`); if (on) o.push(`<rect x="${cx - 1}" y="${y + 6.4}" width="6" height="1.1" fill="${P.ac}"/>`); }
      else if (style === "dot") o.push(`<circle cx="${cx + 2}" cy="${y + 3}" r="${on ? 2 : 1.3}" fill="${on ? P.ac : P.mu}"/>`);
      else o.push(`<rect x="${cx - 1}" y="${y}" width="7" height="6" rx="${on ? 3 : 1}" fill="${on ? P.ac : "none"}"/><text x="${cx + 2.5}" y="${y + 4.6}" font-family="${font}, monospace" font-size="4.6" fill="${on ? (lum(P.ac) > .55 ? "#111" : "#fff") : P.mu}" text-anchor="middle">${k + 1}</text>`); }
    return o.join(""); };
  const status = (x2, y, n = 5) => { const o = []; for (let k = 0; k < n; k++) o.push(`<rect x="${x2 - 6 - k * 9}" y="${y}" width="${k === 0 ? 4 : 6}" height="3.4" rx="1" fill="${k === 0 ? P.ac : P.fg}" opacity="${k === 0 ? 1 : .55}"/>`); return o.join(""); };
  const pill = (x, y, w, h = 9) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="${barBg}" opacity=".94"/>`;
  switch (r.bar) {
    case "full": case "under": case "minimal":
      if (barBg !== "none") out.push(`<rect width="${W}" height="11" fill="${barBg}" opacity=".95"/>`);
      out.push(wsBoxes(5, 2.5, r.bar === "under" ? "under" : "box"), clock(160, 7.6), status(W - 2, 3.8)); break;
    case "fullb":
      out.push(`<rect y="${H - 11}" width="${W}" height="11" fill="${barBg}" opacity=".95"/>`, wsBoxes(5, H - 8.5), clock(160, H - 3.4), status(W - 2, H - 7.2)); break;
    case "pills":
      out.push(pill(4, 4, 46), wsBoxes(9, 5.5), pill(136, 4, 48), clock(160, 10.3), pill(W - 54, 4, 50), status(W - 6, 6.8)); break;
    case "split":
      out.push(pill(4, 4, 46), wsBoxes(9, 5.5), pill(W - 92, 4, 88), clock(W - 76, 10.3, "middle"), status(W - 8, 6.8, 4)); break;
    case "island":
      out.push(pill(90, 4, 140), wsBoxes(97, 5.5, "dot"), clock(160, 10.3), status(226, 6.8, 4)); break;
    case "float":
      out.push(`<rect x="6" y="4" width="${W - 12}" height="10" rx="${swayOnly ? 0 : 5}" fill="${barBg}" opacity=".95"/>`, wsBoxes(12, 6), clock(160, 10.8), status(W - 10, 7.3)); break;
    case "corners":
      out.push(`<path d="M0 0 H70 V6 Q70 12 64 12 H0 Z" fill="${barBg}"/>`, wsBoxes(6, 3.2), `<path d="M${W} 0 H${W - 70} V6 Q${W - 70} 12 ${W - 64} 12 H${W} Z" fill="${barBg}"/>`, status(W - 4, 4.6)); break;
    case "blocks": {
      out.push(`<rect width="${W}" height="11" fill="${barBg}" opacity=".95"/>`);
      const seg = (x, w, c, dir) => `<path d="M${x} 0 H${x + w} L${x + w + (dir > 0 ? 5 : -5)} 5.5 L${x + w} 11 H${x} Z" fill="${c}"/>`;
      out.push(seg(0, 18, P.ac, 1), `<text x="8" y="7.6" font-family="${font}, monospace" font-size="5" font-weight="700" fill="${lum(P.ac) > .55 ? "#111" : "#fff"}" text-anchor="middle">1</text>`, seg(23, 26, P.sf, 1), wsBoxes(27, 2.5, "dot"));
      out.push(clock(160, 7.6));
      out.push(`<path d="M${W} 0 H${W - 40} L${W - 45} 5.5 L${W - 40} 11 H${W} Z" fill="${P.a2}"/><path d="M${W - 42} 0 H${W - 78} L${W - 83} 5.5 L${W - 78} 11 H${W - 42} Z" fill="${P.sf}"/>`, status(W - 4, 3.8, 3)); break; }
    case "taskbar": {
      const y = H - 14;
      out.push(`<rect y="${y}" width="${W}" height="14" fill="${P.sf}"/><rect y="${y}" width="${W}" height=".8" fill="${mix(P.sf, P.fg, .3)}"/>`);
      out.push(`<rect x="3" y="${y + 2.5}" width="20" height="9" rx="${r.radius ? 2 : 0}" fill="${P.ac}"/><circle cx="9" cy="${y + 7}" r="2.4" fill="none" stroke="${lum(P.ac) > .55 ? "#111" : "#fff"}" stroke-width="1"/>`);
      for (let k = 0; k < 4; k++) out.push(`<rect x="${27 + k * 9}" y="${y + 3}" width="7" height="8" fill="${k === 0 ? P.bg : mix(P.sf, P.bg, .3)}"/>`);
      [["term", true], ["files", false]].forEach(([t, on], k) => out.push(`<rect x="${66 + k * 64}" y="${y + 2.5}" width="60" height="9" rx="${r.radius ? 1.5 : 0}" fill="${on ? P.bg : mix(P.sf, P.bg, .25)}" stroke="${on ? P.ac : "none"}" stroke-width=".6"/><rect x="${70 + k * 64}" y="${y + 6}" width="${24 + k * 8}" height="1.6" fill="${P.fg}" opacity=".7"/>`));
      out.push(status(W - 30, y + 5.3, 3), clock(W - 14, y + 9.2, "middle")); break; }
    case "side":
      out.push(`<rect width="14" height="${H}" fill="${barBg}" opacity=".95"/>`);
      for (let k = 0; k < 5; k++) out.push(`<rect x="3.5" y="${8 + k * 10}" width="7" height="7" rx="${swayOnly ? 0 : 2}" fill="${k === 0 ? P.ac : P.sf}"/>`);
      out.push(`<text x="7" y="${H - 18}" font-family="${font}, monospace" font-size="4.6" font-weight="600" fill="${P.fg}" text-anchor="middle">21</text><text x="7" y="${H - 12}" font-family="${font}, monospace" font-size="4.6" font-weight="600" fill="${P.fg}" text-anchor="middle">04</text>`);
      for (let k = 0; k < 3; k++) out.push(`<rect x="5" y="${H - 50 + k * 8}" width="4" height="4" rx="1" fill="${k === 2 ? P.ac : P.fg}" opacity=".6"/>`); break;
  }
  return out.join("");
}

function preview(r) {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[r.pal];
  const P = { bg, sf, fg, mu, ac, a2, a3 };
  const R = rng(r.n * 7 + 3);
  return `<svg viewBox="0 0 320 200" role="img" aria-label="Preview of the ${r.name} rice">${wall(r.wall, P, R, r.n)}${desktop(r, P, rng(r.n * 13 + 1))}</svg>`;
}

// ---------------------------------------------------------------- cards
let stars = new Set();
try { stars = new Set(JSON.parse(localStorage.getItem("grim-rice-stars") || "[]")); } catch (e) {}
const saveStars = () => { try { localStorage.setItem("grim-rice-stars", JSON.stringify([...stars])); } catch (e) {} };

function riceJson(r) {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[r.pal];
  const light = lum(bg) > .5;
  return JSON.stringify({
    name: r.name, description: r.desc, dark: !light,
    colors: { bg, bg2: sf, bg3: mix(sf, fg, .08), fg, muted: mu, accent: ac, accent_fg: lum(ac) > .55 ? "#111111" : "#ffffff", accent2: a2,
              urgent: a2, border_active: ac, border_inactive: mix(bg, mu, .45) },
    font: DATA.fonts[r.font] + " Nerd Font Mono", font_pkg: DATA.fontpkg[r.font], font_size: 11,
    wallpaper: r.wall, gaps: r.gaps, border: r.border, radius: r.radius,
    dock: r.flags.includes("d"), bar_position: ["fullb", "taskbar"].includes(r.bar) ? "bottom" : "top", bar_layout: r.bar,
    title_bars: r.flags.includes("t"), shadows: r.flags.includes("s"), wms: [...r.wms].map(k => WMNAME[k]),
  }, null, 2);
}

function card(r) {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[r.pal];
  const light = lum(bg) > .5;
  const extras = [r.flags.includes("d") && "dock", r.flags.includes("t") && "title bars", r.flags.includes("s") && "shadows"].filter(Boolean).join(", ") || "none";
  const barTool = r.bar === "taskbar" ? "IceWM taskbar" : r.bar === "side" ? (r.wms.includes("o") ? "tint2" : "Waybar") : [r.wms.match(/[ico]/) && "Polybar", r.wms.includes("s") && "Waybar"].filter(Boolean).join(" / ");
  const swayNote = r.wms.includes("s") && r.wms.length > 1 && r.radius ? `<p class="note">On Sway the corners stay square.</p>` : "";
  const el = document.createElement("article");
  el.className = "card";
  el.dataset.wms = r.wms; el.dataset.light = light ? "light" : "dark"; el.dataset.n = r.n;
  el.dataset.search = (r.name + " " + r.desc + " " + r.pal + " " + r.wall + " " + r.bar).toLowerCase();
  el.innerHTML = `${preview(r)}
    <div class="info">
      <div class="top"><span class="num">#${String(r.n).padStart(3, "0")}</span><h2 class="name">${r.name}</h2>
        <div class="wms">${[...r.wms].map(k => `<span class="wm">${WMNAME[k]}</span>`).join("")}</div></div>
      <p class="desc">${r.desc}</p>
      <div class="sw" title="Palette">${[bg, sf, fg, mu, ac, a2, a3].map(c => `<i style="background:${c}"></i>`).join("")}</div>
      <dl class="spec">
        <dt>Bar</dt><dd>${barTool} · ${BARNAME[r.bar]}</dd>
        <dt>Windows</dt><dd>gaps ${r.gaps} · border ${r.border} · corners ${r.wms === "s" ? 0 : r.radius}</dd>
        <dt>Font</dt><dd>${DATA.fonts[r.font]}</dd>
        <dt>Extras</dt><dd>${extras}</dd>
      </dl>${swayNote}
      <div class="acts"><button class="act star" type="button" aria-pressed="${stars.has(r.n)}">${stars.has(r.n) ? "★ Starred" : "☆ Star"}</button>
        <button class="act copy" type="button">Copy rice</button></div>
    </div>`;
  const sb = el.querySelector(".star");
  if (stars.has(r.n)) sb.classList.add("on");
  sb.addEventListener("click", () => {
    stars.has(r.n) ? stars.delete(r.n) : stars.add(r.n); saveStars();
    const on = stars.has(r.n); sb.classList.toggle("on", on); sb.setAttribute("aria-pressed", on); sb.textContent = on ? "★ Starred" : "☆ Star";
    if (state.starsOnly) apply();
  });
  el.querySelector(".copy").addEventListener("click", e => copyText(riceJson(r), e.currentTarget, "Copied"));
  return el;
}

async function copyText(text, btn, done) {
  const old = btn.textContent;
  try { await navigator.clipboard.writeText(text); btn.textContent = done; }
  catch (e) { btn.textContent = "Copy failed"; }
  setTimeout(() => (btn.textContent = old), 1400);
}

const grid = document.getElementById("grid");
const cards = DATA.rices.map(r => { const c = card(r); grid.appendChild(c); return c; });
const state = { q: "", wm: "", l: "", starsOnly: false };
function apply() {
  let shown = 0;
  for (const c of cards) {
    const ok = (!state.wm || c.dataset.wms.includes(state.wm)) && (!state.l || c.dataset.light === state.l)
      && (!state.q || c.dataset.search.includes(state.q)) && (!state.starsOnly || stars.has(+c.dataset.n));
    c.hidden = !ok; if (ok) shown++;
  }
  document.getElementById("count").textContent = `${shown} of ${cards.length} rices · ${stars.size} starred`;
  document.getElementById("empty").hidden = shown > 0;
}
const chips = (groupId, key) => document.querySelectorAll(`#${groupId} .chipbtn`).forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll(`#${groupId} .chipbtn`).forEach(x => x.setAttribute("aria-pressed", "false"));
  b.setAttribute("aria-pressed", "true"); state[key] = b.dataset[key === "wm" ? "wm" : "l"]; apply();
}));
chips("wmf", "wm"); chips("lf", "l");
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); apply(); });
const so = document.getElementById("starsonly");
so.addEventListener("click", () => { state.starsOnly = !state.starsOnly; so.setAttribute("aria-pressed", state.starsOnly); apply(); });
document.getElementById("copylist").addEventListener("click", e => {
  const list = DATA.rices.filter(r => stars.has(r.n)).map(r => `#${r.n} ${r.name}`);
  copyText(list.length ? "Build these Grim rices: " + list.join(", ") : "No rices starred yet.", e.currentTarget, list.length ? `Copied ${list.length}` : "Star some first");
});
apply();
</script>
"""

out = HTML.replace("__DATA__", json.dumps(data, separators=(",", ":")))
open(os.path.join(HERE, "rice-gallery.html"), "w").write(out)
print(f"{len(out) // 1024} KB, {len(data['rices'])} rices")
