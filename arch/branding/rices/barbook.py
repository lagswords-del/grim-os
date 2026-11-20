"""Builds bar-book.html from bars.py: python3 barbook.py"""
import json, os
import bars, rices

HERE = os.path.dirname(os.path.abspath(__file__))
data = {"palettes": rices.PALETTES, "fonts": {k: v[0] for k, v in rices.FONTS.items()},
        "tools": bars.TOOLS, "bars": bars.parse()}

HTML = r"""<title>Grim Bar Book</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&family=Fira+Code:wght@500;700&family=IBM+Plex+Mono:wght@500;700&family=Space+Mono:wght@400;700&family=Inconsolata:wght@500;700&family=Source+Code+Pro:wght@500;700&family=Victor+Mono:wght@500;700&family=Ubuntu+Mono:wght@400;700&family=VT323&display=swap">
<style>
/* Layout: a swatch book of bars. Each card is a wide strip of desktop with the bar drawn on it, then its recipe. */
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
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); padding-block: 10px; border-bottom: 1px solid var(--line);
  display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; }
.group { display: inline-flex; gap: 4px; flex-wrap: wrap; }
.chipbtn { font: 500 13px var(--body); color: var(--ink); background: var(--chip); border: 1px solid transparent; border-radius: 999px; padding: 6px 12px; cursor: pointer; }
.chipbtn[aria-pressed="true"] { background: var(--ink); color: var(--bg); }
.chipbtn:focus-visible, .act:focus-visible, #q:focus-visible, #st:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
#q, #st { font: 14px var(--body); color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 7px 10px; }
#q { width: min(220px, 100%); }
.count { font: 500 12.5px var(--mono); color: var(--muted); margin-left: auto; font-variant-numeric: tabular-nums; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 440px), 1fr)); gap: 18px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: grid; grid-template-rows: auto 1fr; min-width: 0; }
.card svg { display: block; width: 100%; height: auto; aspect-ratio: 640 / 150; }
.info { padding: 12px 14px 14px; display: grid; gap: 8px; align-content: start; min-width: 0; }
.top { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.num { font: 500 11px var(--mono); color: var(--muted); font-variant-numeric: tabular-nums; }
.name { font: 700 18px/1.15 var(--display); margin: 0; letter-spacing: -.01em; }
.tool { margin-left: auto; font: 500 10.5px var(--mono); padding: 2px 7px; border-radius: 4px; background: var(--chip); }
.desc { margin: 0; color: var(--muted); font-size: 13px; }
.spec { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; font-size: 12px; margin: 0; }
.spec dt { color: var(--muted); }
.spec dd { margin: 0; font-family: var(--mono); font-size: 11.5px; overflow-wrap: anywhere; }
.sw { display: flex; height: 8px; border-radius: 3px; overflow: hidden; border: 1px solid var(--line); }
.sw i { flex: 1; }
.acts { display: flex; gap: 6px; }
.act { font: 500 12.5px var(--body); color: var(--ink); background: var(--chip); border: 1px solid var(--line); border-radius: 6px; padding: 5px 10px; cursor: pointer; }
.act.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.empty { color: var(--muted); padding: 40px 0; text-align: center; }
footer { color: var(--muted); font-size: 12.5px; }
code { font: 12px var(--mono); }
</style>

<main>
<header>
  <span class="eyebrow">Grim OS · bars</span>
  <h1>Grim Bar Book</h1>
  <p class="lede">Bar designs for Grim OS, each drawn with its real modules: workspaces, clock, volume, Wi-Fi, battery and the rest. The tag on each card says whether Polybar (i3, Openbox, IceWM), Waybar (Sway, Hyprland, Niri) or both can build it. Star the ones you want, copy the shortlist and paste it to Claude.</p>
</header>

<div class="bar" role="toolbar" aria-label="Filters">
  <input id="q" type="search" placeholder="Search bars" aria-label="Search bars">
  <div class="group" id="tf" aria-label="Bar program">
    <button class="chipbtn" data-t="" aria-pressed="true">All</button>
    <button class="chipbtn" data-t="p" aria-pressed="false">Polybar</button>
    <button class="chipbtn" data-t="w" aria-pressed="false">Waybar</button>
  </div>
  <select id="st" aria-label="Style"><option value="">Every style</option></select>
  <div class="group">
    <button class="chipbtn" id="starsonly" aria-pressed="false">★ Shortlist only</button>
    <button class="chipbtn" id="copylist" aria-pressed="false">Copy shortlist</button>
  </div>
  <span class="count" id="count"></span>
</div>

<div class="grid" id="grid"></div>
<p class="empty" id="empty" hidden>No bar matches these filters.</p>
<footer>Source: <code>grimos/branding/rices/bars.py</code> and <code>barbook.py</code>.</footer>
</main>

<script>
const DATA = __DATA__;
const STYLE_NAME = { full: "Full strip", pills: "Pills", island: "Island", split: "Split", powerline: "Powerline", roundline: "Rounded segments",
  underline: "Underline", overline: "Overline", bubbles: "Bubbles", plain: "Plain text", icons: "Icons only", brackets: "Brackets", tabs: "Folder tabs",
  glass: "Glass", outline: "Outline", blocks: "Blocks", notch: "Notch", corners: "Corner tabs", double: "Two bars", side: "Vertical", gradient: "Gradient" };
const FONT = { jbm: "'JetBrains Mono'", fira: "'Fira Code'", plex: "'IBM Plex Mono'", space: "'Space Mono'", incon: "Inconsolata",
  scp: "'Source Code Pro'", victor: "'Victor Mono'", ubuntu: "'Ubuntu Mono'", term: "VT323" };
const hex2 = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, t) => { const x = hex2(a), y = hex2(b); return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join(""); };
const lum = h => { const [r, g, b] = hex2(h); return (0.299 * r + 0.587 * g + 0.114 * b) / 255; };
const on = c => lum(c) > .55 ? "#141414" : "#ffffff";

// ---------------------------------------------------------------- module content
const TEXT = { title: "nvim · grim-rice", clock: "21:04", date: "Tue 18 Nov", cpu: "12%", mem: "3.1G", vol: "64%", net: "home",
  bat: "83%", updates: "4", media: "Lo-fi radio", weather: "4°", kb: "us", disk: "41%", temp: "52°", power: "", tray: "", launcher: "" };
const ICON = {
  vol: c => `<path d="M0 3.5H2.5L5.5 1V9L2.5 6.5H0Z" fill="${c}"/><path d="M7 3Q9 5 7 7" stroke="${c}" fill="none" stroke-width="1"/>`,
  net: c => `<path d="M1 4Q5 0 9 4M2.6 5.7Q5 3.4 7.4 5.7" stroke="${c}" fill="none" stroke-width="1.1" stroke-linecap="round"/><circle cx="5" cy="7.8" r="1.1" fill="${c}"/>`,
  bat: c => `<rect x=".5" y="2.5" width="8" height="5" rx="1" stroke="${c}" fill="none" stroke-width="1"/><rect x="1.6" y="3.6" width="5" height="2.8" fill="${c}"/><rect x="8.6" y="4" width="1" height="2" fill="${c}"/>`,
  cpu: c => `<rect x="2" y="2" width="6" height="6" rx=".8" stroke="${c}" fill="none" stroke-width="1"/><rect x="3.8" y="3.8" width="2.4" height="2.4" fill="${c}"/><path d="M3.5 0V2M6.5 0V2M3.5 8V10M6.5 8V10M0 3.5H2M0 6.5H2M8 3.5H10M8 6.5H10" stroke="${c}" stroke-width=".8"/>`,
  mem: c => `<rect x=".5" y="3" width="9" height="4.5" rx=".6" stroke="${c}" fill="none" stroke-width="1"/><path d="M3 4.4V6M5 4.4V6M7 4.4V6M2 7.5V9M8 7.5V9" stroke="${c}" stroke-width=".9"/>`,
  power: c => `<path d="M2.8 2.8A3.8 3.8 0 1 0 7.2 2.8" stroke="${c}" fill="none" stroke-width="1.3" stroke-linecap="round"/><path d="M5 .6V4.6" stroke="${c}" stroke-width="1.3" stroke-linecap="round"/>`,
  updates: c => `<path d="M5 .8V6.8M2.3 4.2L5 7L7.7 4.2" stroke="${c}" fill="none" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M1.5 9H8.5" stroke="${c}" stroke-width="1.2" stroke-linecap="round"/>`,
  media: c => `<circle cx="3" cy="7.6" r="1.9" fill="${c}"/><path d="M4.8 7.6V1L8.6 2.2V3.9L4.8 2.7" stroke="${c}" fill="${c}" stroke-width=".8"/>`,
  weather: c => `<circle cx="5" cy="5" r="2.2" fill="${c}"/><path d="M5 .3V1.6M5 8.4V9.7M.3 5H1.6M8.4 5H9.7M1.7 1.7L2.6 2.6M7.4 7.4L8.3 8.3M1.7 8.3L2.6 7.4M7.4 2.6L8.3 1.7" stroke="${c}" stroke-width=".9" stroke-linecap="round"/>`,
  temp: c => `<path d="M5 1V6" stroke="${c}" stroke-width="2" stroke-linecap="round"/><circle cx="5" cy="7.6" r="1.9" fill="${c}"/>`,
  disk: c => `<circle cx="5" cy="5" r="4" stroke="${c}" fill="none" stroke-width="1"/><circle cx="5" cy="5" r="1.1" fill="${c}"/>`,
  kb: c => `<rect x=".5" y="2.2" width="9" height="5.6" rx=".8" stroke="${c}" fill="none" stroke-width="1"/><path d="M2.2 4H3.2M4.5 4H5.5M6.8 4H7.8M3 6H7" stroke="${c}" stroke-width=".9"/>`,
  tray: c => `<rect x="0" y="3.5" width="2.6" height="2.6" rx=".6" fill="${c}"/><rect x="3.7" y="3.5" width="2.6" height="2.6" rx=".6" fill="${c}" opacity=".7"/><rect x="7.4" y="3.5" width="2.6" height="2.6" rx=".6" fill="${c}" opacity=".45"/>`,
  launcher: c => `<path d="M5 .4C2.4 .9 1.6 3.4 1.6 5.6L.6 9.6H9.4L8.4 5.6C8.4 3.2 7.4 .9 5 .4Z" fill="${c}"/><path d="M3.8 4.4H6.2" stroke="${c === "#ffffff" ? "#000" : "#000"}" stroke-width=".9" opacity=".55"/>`,
};

function render(b) {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[b.pal];
  const P = { bg, sf, fg, mu, ac, a2, a3 };
  const W = 640, H = 150, light = lum(bg) > .5;
  const font = FONT[b.font] + ", monospace";
  const h = b.h * 1.15, fs = h * .42, s = fs / 9;
  const cycle = [ac, a2, a3, mix(ac, a2, .5)];
  const o = [];
  const id = "b" + b.n;

  // backdrop: wallpaper blur + a window
  o.push(`<defs><filter id="f${id}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
    <linearGradient id="g${id}" x1="0" x2="1"><stop offset="0" stop-color="${ac}"/><stop offset="1" stop-color="${a2}"/></linearGradient></defs>
    <rect width="${W}" height="${H}" fill="${bg}"/><g filter="url(#f${id})" opacity="${light ? .45 : .55}"><circle cx="120" cy="40" r="90" fill="${ac}"/><circle cx="520" cy="110" r="100" fill="${a2}"/><circle cx="330" cy="150" r="70" fill="${a3}"/></g>
    <rect width="${W}" height="${H}" fill="${bg}" opacity=".25"/>`);
  const side = b.style === "side";
  const wy = b.pos === "b" ? 14 : (b.style === "double" ? h + 14 : h + 22), wx = side ? h + 26 : 40;
  o.push(`<rect x="${wx}" y="${wy}" width="${W - wx - 40}" height="${H}" rx="8" fill="${light ? mix(bg, "#ffffff", .5) : mix(bg, "#000000", .25)}" opacity=".92" stroke="${mix(bg, fg, .15)}"/>`);
  for (let k = 0; k < 5; k++) o.push(`<rect x="${wx + 16}" y="${wy + 16 + k * 11}" width="${[120, 210, 160, 90, 180][k]}" height="4" rx="2" fill="${[ac, fg, mu, a2, fg][k]}" opacity="${k === 0 ? .9 : .45}"/>`);

  // ---- measure + draw items
  const tw = t => t.length * fs * .62;
  const iconOnly = b.style === "icons";
  const wsLabels = { num: ["1", "2", "3", "4", "5"], dots: ["", "", "", "", ""], roman: ["I", "II", "III", "IV", "V"],
    kanji: ["一", "二", "三", "四", "五"], bars: ["", "", "", "", ""], words: ["web", "code", "chat", "music", "misc"] }[b.ws] || ["1", "2", "3", "4", "5"];
  const items = mods => mods.map(m => {
    if (m === "ws") {
      const each = b.ws === "dots" ? fs * .95 : b.ws === "bars" ? fs * .7 : b.ws === "words" ? 0 : fs * 1.55;
      const w = b.ws === "words" ? wsLabels.reduce((a, l) => a + tw(l) + fs * .8, 0) : each * 5;
      return { m, w };
    }
    const text = iconOnly && !["clock", "title"].includes(m) ? "" : TEXT[m];
    const hasIcon = !!ICON[m];
    const w = (hasIcon ? 10 * s : 0) + (text ? (hasIcon ? fs * .4 : 0) + tw(text) : 0);
    return { m, w, text, hasIcon };
  });
  const drawWs = (x, cy, txt, opts = {}) => {
    const r = [];
    let xx = x;
    wsLabels.forEach((l, k) => {
      const act = k === 0, occ = k === 2;
      if (b.ws === "dots") { r.push(`<circle cx="${xx + fs * .45}" cy="${cy}" r="${act ? fs * .3 : fs * .19}" fill="${act ? (opts.activeC || ac) : (occ ? txt : mix(opts.base || bg, txt, .45))}"/>`); xx += fs * .95; }
      else if (b.ws === "bars") { r.push(`<rect x="${xx}" y="${cy - fs * .45}" width="${fs * .32}" height="${fs * .9}" rx="${fs * .16}" fill="${act ? (opts.activeC || ac) : mix(opts.base || bg, txt, .4)}"/>`); xx += fs * .7; }
      else {
        const w = b.ws === "words" ? tw(l) + fs * .8 : fs * 1.55;
        if (act && opts.pillActive !== false) r.push(`<rect x="${xx}" y="${cy - fs * .78}" width="${w - fs * .2}" height="${fs * 1.56}" rx="${opts.square ? 1.5 : fs * .78}" fill="${opts.activeC || ac}"/>`);
        if (act && opts.underline) r.push(`<rect x="${xx + fs * .2}" y="${cy + fs * .85}" width="${w - fs * .6}" height="${fs * .16}" fill="${ac}"/>`);
        r.push(`<text x="${xx + (w - fs * .2) / 2}" y="${cy + fs * .36}" font-family="${font}" font-size="${fs}" font-weight="${act ? 700 : 500}" text-anchor="middle" fill="${act && opts.pillActive !== false ? on(opts.activeC || ac) : (occ ? txt : mix(opts.base || bg, txt, .5))}">${l}</text>`);
        xx += w;
      }
    });
    return r.join("");
  };
  const drawItem = (it, x, cy, col, iconCol, opts = {}) => {
    if (it.m === "ws") return drawWs(x, cy, col, opts);
    const r = []; let xx = x;
    if (it.hasIcon) { r.push(`<g transform="translate(${xx} ${cy - 5 * s}) scale(${s})">${ICON[it.m](it.m === "power" ? (opts.powerC || iconCol) : iconCol)}</g>`); xx += 10 * s + fs * .4; }
    if (it.text) r.push(`<text x="${xx}" y="${cy + fs * .36}" font-family="${font}" font-size="${fs}" font-weight="${it.m === "clock" ? 700 : 500}" fill="${col}">${it.text}</text>`);
    return r.join("");
  };
  const gap = fs * (["powerline", "roundline", "blocks"].includes(b.style) ? 2.1 : ["bubbles", "outline", "brackets"].includes(b.style) ? 1.7 : 1.1);
  const groupW = arr => arr.reduce((a, it) => a + it.w, 0) + Math.max(0, arr.length - 1) * gap;

  const L = items(b.left), C = items(b.center), R = items(b.right);
  const floating = ["pills", "island", "split", "bubbles", "glass", "outline"].includes(b.style);
  const by = b.pos === "b" ? H - h - (floating ? 8 : 0) : (floating ? 8 : 0);
  const cy = by + h / 2;
  const padX = floating ? 10 : 12;

  // layout positions of the three groups
  const pos = (arr, align, x0 = padX, x1 = W - padX) => {
    const w = groupW(arr);
    let x = align === "l" ? x0 + h * .35 : align === "r" ? x1 - w - h * .35 : (W - w) / 2;
    return arr.map(it => { const p = { it, x }; x += it.w + gap; return p; });
  };
  const drawRow = (placed, col, iconCol, opts) => placed.map(p => drawItem(p.it, p.x, cy, col, iconCol, opts)).join("");
  const plainCol = fg, iconCol = mix(fg, mu, .35);
  const st = b.style;

  if (st === "side") {
    const sw = h, x = 0;
    o.push(`<rect x="0" y="0" width="${sw}" height="${H}" fill="${bg}"/><rect x="${sw - .6}" y="0" width=".6" height="${H}" fill="${mix(bg, fg, .15)}"/>`);
    for (let k = 0; k < 5; k++) o.push(`<rect x="${sw * .25}" y="${12 + k * sw * .62}" width="${sw * .5}" height="${sw * .5}" rx="${sw * .14}" fill="${k === 0 ? ac : mix(bg, fg, .12)}"/>`);
    ["vol", "bat", "power"].forEach((m, k) => o.push(`<g transform="translate(${sw / 2 - 5 * s} ${H - 98 + k * 19}) scale(${s})">${ICON[m](m === "power" ? ac : iconCol)}</g>`));
    o.push(`<text x="${sw / 2}" y="${H - 20}" font-family="${font}" font-size="${fs}" font-weight="700" text-anchor="middle" fill="${fg}">21</text><text x="${sw / 2}" y="${H - 6}" font-family="${font}" font-size="${fs}" font-weight="700" text-anchor="middle" fill="${fg}">04</text>`);
    return wrap(o);
  }

  const strip = (y, fill, opts = "") => `<rect x="0" y="${y}" width="${W}" height="${h}" fill="${fill}" ${opts}/>`;
  if (st === "double") {
    const top = 0, bot = H - h;
    o.push(strip(top, bg), strip(bot, mix(bg, sf, .6)), `<rect y="${h - .6}" width="${W}" height=".6" fill="${mix(bg, fg, .15)}"/>`);
    const cyT = top + h / 2, cyB = bot + h / 2;
    const c = pos(C, "c"), r = pos(R, "r"), l = pos(L, "l");
    o.push(c.map(p => drawItem(p.it, p.x, cyT, fg, iconCol)).join(""), r.map(p => drawItem(p.it, p.x, cyT, fg, iconCol, { powerC: ac })).join(""), l.map(p => drawItem(p.it, p.x, cyB, fg, iconCol)).join(""));
    return wrap(o);
  }
  if (["full", "underline", "overline", "plain", "icons", "brackets", "powerline", "roundline", "blocks", "tabs"].includes(st)) o.push(strip(by, bg, st === "plain" ? `opacity=".92"` : ""));
  if (st === "full") o.push(`<rect y="${b.pos === "b" ? by : h - .6}" width="${W}" height=".6" fill="${mix(bg, fg, .15)}"/>`);
  if (st === "gradient") o.push(`<rect x="0" y="${by}" width="${W}" height="${h}" fill="url(#g${id})"/>`);
  if (st === "glass") o.push(`<rect x="8" y="${by}" width="${W - 16}" height="${h}" rx="${h / 2.6}" fill="${bg}" opacity=".55" stroke="${ac}" stroke-width=".9"/>`);

  const pl = pos(L, "l"), pr = pos(R, "r");
  let pc = pos(C, "c");
  // keep the centre group clear of the right group on busy bars
  if (pc.length && pr.length) {
    const cEnd = pc[pc.length - 1].x + pc[pc.length - 1].it.w, rStart = pr[0].x - gap * 1.5;
    if (cEnd > rStart) { const shift = cEnd - rStart; pc = pc.map(p => ({ it: p.it, x: p.x - shift })); }
  }
  const all = [pl, pc, pr];

  switch (st) {
    case "full": case "glass": case "icons":
      o.push(drawRow(pl, plainCol, iconCol), drawRow(pc, fg, iconCol), drawRow(pr, plainCol, st === "icons" ? fg : iconCol, { powerC: st === "icons" ? b.pal === "grim" ? ac : mix(ac, "#ff4d5a", .4) : ac })); break;
    case "gradient": { const t = on(ac); o.push(drawRow(pl, t, t, { activeC: t, base: ac }), drawRow(pc, t, t), drawRow(pr, t, t, { powerC: t })); break; }
    case "pills": case "split": case "island": {
      const groups = st === "island" ? [pos([...L, ...C, ...R], "c")] : st === "split" ? [pl, pos([...C, ...R], "r")] : all;
      groups.forEach(g => { if (!g.length) return; const x0 = g[0].x - fs * .9, x1 = g[g.length - 1].x + g[g.length - 1].it.w + fs * .9;
        o.push(`<rect x="${x0}" y="${by}" width="${x1 - x0}" height="${h}" rx="${h / 2}" fill="${bg}" opacity=".96"/>`);
        o.push(drawRow(g, fg, iconCol, { powerC: ac })); });
      break; }
    case "bubbles": case "outline":
      all.forEach(g => g.forEach(p => { const x0 = p.x - fs * .6, w = p.it.w + fs * 1.2;
        o.push(st === "bubbles" ? `<rect x="${x0}" y="${by + 2}" width="${w}" height="${h - 4}" rx="${(h - 4) / 2}" fill="${sf}" opacity=".97"/>`
                                : `<rect x="${x0}" y="${by + 2}" width="${w}" height="${h - 4}" rx="${(h - 4) / 3}" fill="${bg}" fill-opacity=".55" stroke="${p.it.m === "ws" ? ac : mix(ac, fg, .3)}" stroke-width="1"/>`);
        o.push(drawItem(p.it, p.x, cy, fg, iconCol, { powerC: ac, base: sf })); }));
      break;
    case "underline": case "overline": {
      let k = 0;
      all.forEach(g => g.forEach(p => { const c = p.it.m === "ws" ? ac : cycle[k++ % cycle.length];
        if (p.it.m === "ws") o.push(drawItem(p.it, p.x, cy, fg, iconCol, { pillActive: false, underline: st === "underline" }));
        else { o.push(drawItem(p.it, p.x, cy, fg, c));
          o.push(`<rect x="${p.x}" y="${st === "underline" ? by + h - 2.4 : by}" width="${p.it.w}" height="2.4" fill="${c}"/>`); }
        if (p.it.m === "ws" && st === "overline") o.push(`<rect x="${p.x}" y="${by}" width="${fs * 1.35}" height="2.4" fill="${ac}"/>`); }));
      break; }
    case "plain": {
      all.forEach(g => g.forEach((p, i) => { o.push(drawItem(p.it, p.x, cy, p.it.m === "ws" ? fg : fg, mu, { pillActive: false }));
        if (i < g.length - 1) o.push(`<text x="${p.x + p.it.w + gap / 2}" y="${cy + fs * .36}" font-family="${font}" font-size="${fs}" fill="${mu}" text-anchor="middle">·</text>`); }));
      break; }
    case "brackets": {
      all.forEach(g => g.forEach(p => { o.push(`<text x="${p.x - fs * .62}" y="${cy + fs * .36}" font-family="${font}" font-size="${fs}" fill="${ac}">[</text><text x="${p.x + p.it.w + fs * .05}" y="${cy + fs * .36}" font-family="${font}" font-size="${fs}" fill="${ac}">]</text>`);
        o.push(drawItem(p.it, p.x, cy, fg, a2, { square: true, powerC: ac })); }));
      break; }
    case "powerline": case "roundline": case "blocks": {
      const segs = (g, dir) => { g.forEach((p, i) => { const c = p.it.m === "ws" ? sf : cycle[i % cycle.length];
        const x0 = p.x - fs * .7, x1 = p.x + p.it.w + fs * .7, t = p.it.m === "ws" ? fg : on(c);
        if (st === "blocks") o.push(`<rect x="${x0}" y="${by + 3}" width="${x1 - x0}" height="${h - 6}" fill="${c}"/>`);
        else if (st === "roundline") o.push(`<rect x="${x0}" y="${by + 2.5}" width="${x1 - x0}" height="${h - 5}" rx="${(h - 5) / 2}" fill="${c}"/>`);
        else o.push(dir > 0 ? `<path d="M${x0} ${by}H${x1}L${x1 + h * .38} ${cy}L${x1} ${by + h}H${x0}${i ? `L${x0 + h * .38} ${cy}Z` : "Z"}" fill="${c}"/>`
                            : `<path d="M${x1} ${by}H${x0}L${x0 - h * .38} ${cy}L${x0} ${by + h}H${x1}${i < g.length - 1 ? `L${x1 - h * .38} ${cy}Z` : "Z"}" fill="${c}"/>`);
        o.push(drawItem(p.it, p.x, cy, t, t, { activeC: ac, powerC: t, base: c })); }); };
      segs(pl, 1); segs(pr, -1);
      o.push(drawRow(pc, fg, iconCol)); break; }
    case "tabs": {
      pl.forEach(p => { if (p.it.m !== "ws") { o.push(drawItem(p.it, p.x, cy, fg, iconCol)); return; }
        let xx = p.x; wsLabels.forEach((l, k) => { const w = fs * 2.4, act = k === 0;
          o.push(`<path d="M${xx} ${by + h}L${xx + fs * .35} ${by + 3}H${xx + w - fs * .35}L${xx + w} ${by + h}Z" fill="${act ? ac : mix(bg, fg, .1)}"/>`);
          o.push(`<text x="${xx + w / 2}" y="${cy + fs * .55}" font-family="${font}" font-size="${fs}" font-weight="${act ? 700 : 500}" text-anchor="middle" fill="${act ? on(ac) : mu}">${l || k + 1}</text>`); xx += w - fs * .2; }); });
      o.push(drawRow(pc, mu, iconCol), drawRow(pr, fg, iconCol, { powerC: ac })); break; }
    case "notch": {
      o.push(`<rect x="0" y="0" width="${W}" height="${h * .78}" fill="${bg}" opacity=".9"/>`);
      const cw = groupW(C) + fs * 3, cx = (W - cw) / 2;
      o.push(`<path d="M${cx - 10} 0 Q${cx} 0 ${cx} 8 V${h - 6} Q${cx} ${h + 2} ${cx + 10} ${h + 2} H${cx + cw - 10} Q${cx + cw} ${h + 2} ${cx + cw} ${h - 6} V8 Q${cx + cw} 0 ${cx + cw + 10} 0 Z" fill="${ac}"/>`);
      const cyN = h * .39;
      o.push(pl.map(p => drawItem(p.it, p.x, cyN, fg, iconCol)).join(""), pc.map(p => drawItem(p.it, p.x, cy, on(ac), on(ac))).join(""), pr.map(p => drawItem(p.it, p.x, cyN, fg, iconCol, { powerC: ac })).join(""));
      break; }
    case "corners": {
      const lw = groupW(L) + h * 1.2, rw = groupW([...C, ...R]) + h * 1.2;
      o.push(`<path d="M0 0H${lw}V${h - 8}Q${lw} ${h} ${lw - 8} ${h}H0Z" fill="${bg}"/><path d="M${W} 0H${W - rw}V${h - 8}Q${W - rw} ${h} ${W - rw + 8} ${h}H${W}Z" fill="${bg}"/>`);
      o.push(drawRow(pos(L, "l", 0), fg, iconCol), drawRow(pos([...C, ...R], "r", 0, W), fg, iconCol, { powerC: ac })); break; }
  }
  return wrap(o);
  function wrap(parts) { return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Preview of the ${b.name} bar">${parts.join("")}</svg>`; }
}

// ---------------------------------------------------------------- cards
let stars = new Set();
try { stars = new Set(JSON.parse(localStorage.getItem("grim-bar-stars") || "[]")); } catch (e) {}
const saveStars = () => { try { localStorage.setItem("grim-bar-stars", JSON.stringify([...stars])); } catch (e) {} };
const modsText = b => [b.left, b.center, b.right].map(g => g.join(" ") || "–").join("  |  ");
function spec(b) {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[b.pal];
  return JSON.stringify({ name: b.name, program: DATA.tools[b.tool], style: b.style, position: b.pos === "b" ? "bottom" : "top",
    height: b.h, workspaces: b.ws, modules: { left: b.left, center: b.center, right: b.right },
    font: DATA.fonts[b.font] + " Nerd Font", colors: { bg, surface: sf, fg, muted: mu, accent: ac, accent2: a2, accent3: a3 } }, null, 2);
}
async function copyText(text, btn, done) {
  const old = btn.textContent;
  try { await navigator.clipboard.writeText(text); btn.textContent = done; } catch (e) { btn.textContent = "Copy failed"; }
  setTimeout(() => (btn.textContent = old), 1400);
}
const grid = document.getElementById("grid");
const state = { q: "", t: "", st: "", starsOnly: false };
const cards = DATA.bars.map(b => {
  const [bg, sf, fg, mu, ac, a2, a3] = DATA.palettes[b.pal];
  const el = document.createElement("article");
  el.className = "card"; el.dataset.n = b.n; el.dataset.tool = b.tool; el.dataset.style = b.style;
  el.dataset.search = (b.name + " " + b.desc + " " + b.style + " " + b.pal).toLowerCase();
  el.innerHTML = `${render(b)}
    <div class="info">
      <div class="top"><span class="num">#${String(b.n).padStart(2, "0")}</span><h2 class="name">${b.name}</h2><span class="tool">${DATA.tools[b.tool]}</span></div>
      <p class="desc">${b.desc}</p>
      <div class="sw" title="Palette">${[bg, sf, fg, mu, ac, a2, a3].map(c => `<i style="background:${c}"></i>`).join("")}</div>
      <dl class="spec"><dt>Style</dt><dd>${STYLE_NAME[b.style]} · ${b.pos === "b" ? "bottom" : "top"} · ${b.h}px</dd>
        <dt>Modules</dt><dd>${modsText(b)}</dd><dt>Font</dt><dd>${DATA.fonts[b.font]}</dd></dl>
      <div class="acts"><button class="act star" type="button" aria-pressed="${stars.has(b.n)}">${stars.has(b.n) ? "★ Starred" : "☆ Star"}</button>
        <button class="act copy" type="button">Copy recipe</button></div>
    </div>`;
  const sb = el.querySelector(".star"); if (stars.has(b.n)) sb.classList.add("on");
  sb.addEventListener("click", () => { stars.has(b.n) ? stars.delete(b.n) : stars.add(b.n); saveStars();
    const s = stars.has(b.n); sb.classList.toggle("on", s); sb.setAttribute("aria-pressed", s); sb.textContent = s ? "★ Starred" : "☆ Star"; apply(); });
  el.querySelector(".copy").addEventListener("click", e => copyText(spec(b), e.currentTarget, "Copied"));
  grid.appendChild(el); return el;
});
const sel = document.getElementById("st");
Object.entries(STYLE_NAME).forEach(([k, v]) => { if (DATA.bars.some(b => b.style === k)) { const o = document.createElement("option"); o.value = k; o.textContent = v; sel.appendChild(o); } });
function apply() {
  let shown = 0;
  for (const c of cards) {
    const ok = (!state.t || c.dataset.tool.includes(state.t)) && (!state.st || c.dataset.style === state.st)
      && (!state.q || c.dataset.search.includes(state.q)) && (!state.starsOnly || stars.has(+c.dataset.n));
    c.hidden = !ok; if (ok) shown++;
  }
  document.getElementById("count").textContent = `${shown} of ${cards.length} bars · ${stars.size} starred`;
  document.getElementById("empty").hidden = shown > 0;
}
document.querySelectorAll("#tf .chipbtn").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll("#tf .chipbtn").forEach(x => x.setAttribute("aria-pressed", "false"));
  btn.setAttribute("aria-pressed", "true"); state.t = btn.dataset.t; apply(); }));
sel.addEventListener("change", () => { state.st = sel.value; apply(); });
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); apply(); });
const so = document.getElementById("starsonly");
so.addEventListener("click", () => { state.starsOnly = !state.starsOnly; so.setAttribute("aria-pressed", state.starsOnly); apply(); });
document.getElementById("copylist").addEventListener("click", e => {
  const list = DATA.bars.filter(b => stars.has(b.n)).map(b => `#${b.n} ${b.name}`);
  copyText(list.length ? "Build these Grim bars: " + list.join(", ") : "No bars starred yet.", e.currentTarget, list.length ? `Copied ${list.length}` : "Star some first");
});
apply();
</script>
"""

out = HTML.replace("__DATA__", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
open(os.path.join(HERE, "bar-book.html"), "w").write(out)
print(f"{len(out) // 1024} KB, {len(data['bars'])} bars")
