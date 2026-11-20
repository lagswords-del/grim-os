"""Builds grim-ideas.html from ideas.py: python3 build.py"""
import json, os
import ideas

HERE = os.path.dirname(os.path.abspath(__file__))
data = ideas.parse()

HTML = r"""<title>Grim Idea Vault</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: an index-card catalogue. Area index on the left (top on phones), the ideas as dense rows grouped by area. */
:root {
  --bg: #f3f2ef; --panel: #ffffff; --ink: #16161a; --muted: #66666e; --line: #e0dfda; --accent: #b3101c; --chip: #ecebe7;
  --s: #2f7d4f; --m: #9a6a00; --l: #b3101c;
  --display: "Bricolage Grotesque", "Helvetica Neue", Arial, sans-serif;
  --body: "Inter", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #0d0d0f; --panel: #151518; --ink: #ecebe8; --muted: #9b9ba4; --line: #25252a; --accent: #e0303d; --chip: #1e1e22; --s: #5fbf86; --m: #e0b44a; --l: #ff5a66; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #0d0d0f; --panel: #151518; --ink: #ecebe8; --muted: #9b9ba4; --line: #25252a; --accent: #e0303d; --chip: #1e1e22; --s: #5fbf86; --m: #e0b44a; --l: #ff5a66; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 14px/1.5 var(--body);
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 64px; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
main { max-width: 1200px; margin: 0 auto; display: grid; gap: 22px; }
header { display: grid; gap: 10px; max-width: 860px; }
.eyebrow { font: 500 12px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
h1 { font: 800 clamp(34px, 5.5vw, 60px)/1 var(--display); letter-spacing: -.02em; margin: 0; }
.lede { color: var(--muted); max-width: 68ch; margin: 0; }
.toolbar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); padding-block: 10px; border-bottom: 1px solid var(--line);
  display: flex; flex-wrap: wrap; gap: 10px 12px; align-items: center; }
#q { font: 14px var(--body); color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 7px 10px; width: min(260px, 100%); }
.group { display: inline-flex; gap: 4px; flex-wrap: wrap; }
.chipbtn { font: 500 13px var(--body); color: var(--ink); background: var(--chip); border: 1px solid transparent; border-radius: 999px; padding: 6px 12px; cursor: pointer; }
.chipbtn[aria-pressed="true"] { background: var(--ink); color: var(--bg); }
.chipbtn:focus-visible, .star:focus-visible, #q:focus-visible, .areas a:focus-visible, #areasel:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.count { font: 500 12.5px var(--mono); color: var(--muted); margin-left: auto; font-variant-numeric: tabular-nums; }
.layout { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 28px; align-items: start; }
.areas { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 70px); display: grid; gap: 1px; max-height: calc(100vh - 100px); overflow: auto; }
.areas a { display: flex; justify-content: space-between; gap: 8px; color: var(--ink); text-decoration: none; font-size: 13px; padding: 5px 8px; border-radius: 6px; }
.areas a:hover { background: var(--chip); }
.areas a span { color: var(--muted); font: 12px var(--mono); font-variant-numeric: tabular-nums; }
#areasel { display: none; font: 14px var(--body); color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 7px 10px; }
section { display: grid; gap: 0; scroll-margin-top: 80px; }
section h2 { font: 700 22px/1.2 var(--display); margin: 22px 0 8px; display: flex; align-items: baseline; gap: 10px; }
section h2 small { font: 500 12px var(--mono); color: var(--muted); }
section:first-of-type h2 { margin-top: 0; }
.idea { display: grid; grid-template-columns: 44px minmax(0, 1fr) auto auto; gap: 4px 12px; align-items: start; padding: 10px 4px; border-top: 1px solid var(--line); }
.num { font: 500 11.5px var(--mono); color: var(--muted); padding-top: 3px; font-variant-numeric: tabular-nums; }
.t { font-weight: 600; }
.d { color: var(--muted); font-size: 13.5px; }
.eff { font: 500 11px var(--mono); padding: 2px 8px; border-radius: 999px; border: 1px solid currentColor; white-space: nowrap; margin-top: 2px; }
.eff.S { color: var(--s); } .eff.M { color: var(--m); } .eff.L { color: var(--l); }
.star { font-size: 16px; line-height: 1; background: none; border: 0; color: var(--muted); cursor: pointer; padding: 2px 4px; }
.star[aria-pressed="true"] { color: var(--accent); }
.empty { color: var(--muted); padding: 30px 0; }
@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; }
  .areas { display: none; }
  #areasel { display: inline-block; }
  .idea { grid-template-columns: 36px minmax(0, 1fr) auto; }
  .eff { grid-column: 2; justify-self: start; }
}
</style>

<main>
<header>
  <span class="eyebrow">Grim OS · 1.0.3 and beyond</span>
  <h1>Grim Idea Vault</h1>
  <p class="lede">400 ideas for Grim OS, from small tweaks to whole editions. Each is marked small (an afternoon), medium (a few days) or large (a big project). Star the ones you want, copy the shortlist and paste it to Claude.</p>
</header>
<div class="toolbar" role="toolbar" aria-label="Filters">
  <input id="q" type="search" placeholder="Search ideas" aria-label="Search ideas">
  <select id="areasel" aria-label="Jump to area"><option value="">Jump to area…</option></select>
  <div class="group" id="ef" aria-label="Effort">
    <button class="chipbtn" data-e="" aria-pressed="true">Any size</button>
    <button class="chipbtn" data-e="S" aria-pressed="false">Small</button>
    <button class="chipbtn" data-e="M" aria-pressed="false">Medium</button>
    <button class="chipbtn" data-e="L" aria-pressed="false">Large</button>
  </div>
  <div class="group">
    <button class="chipbtn" id="starsonly" aria-pressed="false">★ Shortlist only</button>
    <button class="chipbtn" id="copylist" aria-pressed="false">Copy shortlist</button>
  </div>
  <span class="count" id="count"></span>
</div>
<div class="layout">
  <nav class="areas" id="areas" aria-label="Areas"></nav>
  <div id="list"></div>
</div>
<p class="empty" id="empty" hidden>No idea matches these filters.</p>
</main>

<script>
const IDEAS = __DATA__;
const EFF = { S: "small", M: "medium", L: "large" };
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-");
let stars = new Set();
try { stars = new Set(JSON.parse(localStorage.getItem("grim-idea-stars") || "[]")); } catch (e) {}
const save = () => { try { localStorage.setItem("grim-idea-stars", JSON.stringify([...stars])); } catch (e) {} };
const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

const areas = [...new Set(IDEAS.map(i => i.area))];
const list = document.getElementById("list"), nav = document.getElementById("areas"), sel = document.getElementById("areasel");
const rows = [], sections = [];
for (const a of areas) {
  const items = IDEAS.filter(i => i.area === a);
  const sec = document.createElement("section"); sec.id = slug(a);
  sec.innerHTML = `<h2>${esc(a)} <small>${items.length}</small></h2>`;
  for (const i of items) {
    const r = document.createElement("div"); r.className = "idea";
    r.dataset.e = i.effort; r.dataset.n = i.n; r.dataset.s = (i.title + " " + i.desc + " " + a).toLowerCase();
    r.innerHTML = `<span class="num">#${String(i.n).padStart(3, "0")}</span><div><div class="t">${esc(i.title)}</div><div class="d">${esc(i.desc)}</div></div>
      <span class="eff ${i.effort}">${EFF[i.effort]}</span><button class="star" type="button" aria-label="Star ${esc(i.title)}" aria-pressed="${stars.has(i.n)}">${stars.has(i.n) ? "★" : "☆"}</button>`;
    const b = r.querySelector(".star");
    b.addEventListener("click", () => { stars.has(i.n) ? stars.delete(i.n) : stars.add(i.n); save();
      const on = stars.has(i.n); b.setAttribute("aria-pressed", on); b.textContent = on ? "★" : "☆"; apply(); });
    sec.appendChild(r); rows.push(r);
  }
  list.appendChild(sec); sections.push(sec);
  const l = document.createElement("a"); l.href = "#" + sec.id; l.innerHTML = `${esc(a)}<span>${items.length}</span>`; nav.appendChild(l);
  const o = document.createElement("option"); o.value = sec.id; o.textContent = a; sel.appendChild(o);
}
sel.addEventListener("change", () => { if (sel.value) document.getElementById(sel.value).scrollIntoView({ behavior: "smooth" }); sel.value = ""; });
const state = { q: "", e: "", starsOnly: false };
function apply() {
  let shown = 0;
  for (const r of rows) {
    const ok = (!state.e || r.dataset.e === state.e) && (!state.q || r.dataset.s.includes(state.q)) && (!state.starsOnly || stars.has(+r.dataset.n));
    r.hidden = !ok; if (ok) shown++;
  }
  for (const s of sections) s.hidden = ![...s.querySelectorAll(".idea")].some(r => !r.hidden);
  document.getElementById("count").textContent = `${shown} of ${rows.length} ideas · ${stars.size} starred`;
  document.getElementById("empty").hidden = shown > 0;
}
document.querySelectorAll("#ef .chipbtn").forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll("#ef .chipbtn").forEach(x => x.setAttribute("aria-pressed", "false"));
  b.setAttribute("aria-pressed", "true"); state.e = b.dataset.e; apply(); }));
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); apply(); });
const so = document.getElementById("starsonly");
so.addEventListener("click", () => { state.starsOnly = !state.starsOnly; so.setAttribute("aria-pressed", state.starsOnly); apply(); });
document.getElementById("copylist").addEventListener("click", async e => {
  const btn = e.currentTarget, old = btn.textContent;
  const picked = IDEAS.filter(i => stars.has(i.n)).map(i => `#${i.n} ${i.title}`);
  const text = picked.length ? "Build these Grim OS ideas: " + picked.join(", ") : "";
  if (!text) { btn.textContent = "Star some first"; setTimeout(() => (btn.textContent = old), 1400); return; }
  try { await navigator.clipboard.writeText(text); btn.textContent = `Copied ${picked.length}`; } catch (err) { btn.textContent = "Copy failed"; }
  setTimeout(() => (btn.textContent = old), 1400);
});
apply();
</script>
"""

out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
open(os.path.join(HERE, "grim-ideas.html"), "w").write(out)
print(f"{len(out) // 1024} KB, {len(data)} ideas")
