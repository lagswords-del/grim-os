const send = m => browser.runtime.sendMessage(m);
const $ = id => document.getElementById(id);
let st;
const set = s => send({ type: "set", settings: s }).then(r => { st.settings = r.settings; draw(); });

function draw() {
  const S = st.settings;
  // themes
  const box = $("themes"); box.innerHTML = "";
  for (const [id, t] of Object.entries(st.themes)) {
    const d = document.createElement("div");
    d.className = "theme" + (S.theme === id ? " on" : "");
    const c = (x, a = 1) => `rgba(${x.join(",")},${a})`;
    d.innerHTML = `<div class="sw" style="background:${c(t.bg)};border:1px solid ${c(t.bar)}"><i style="background:${c(t.accent)}"></i></div>${t.name}`;
    d.onclick = () => set({ theme: id });
    box.append(d);
  }
  $("alpha").value = S.alpha; $("alphaV").textContent = S.alpha;
  // engines
  const eng = $("engines"); eng.innerHTML = "";
  for (const e of st.engines) {
    const l = document.createElement("label");
    l.innerHTML = `<input type="radio" name="eng" ${S.engine === e.id ? "checked" : ""}><div><b>${e.name}</b><div class="dim">${e.note || ""}</div></div>`;
    l.querySelector("input").onchange = () => set({ engine: e.id });
    eng.append(l);
  }
  $("searx").value = S.custom?.searx || "";
  for (const k of ["blocker", "tor", "rfp", "webrtc"]) $(k).checked = !!S[k];
  const when = S.lists.updated ? new Date(S.lists.updated).toLocaleString() : "not yet";
  $("listInfo").textContent = `${st.listSize.toLocaleString()} domains on the block list (updated ${when}).`;
  const allow = $("allow"); allow.innerHTML = "";
  if (!S.allow.length) allow.innerHTML = '<li class="dim">none</li>';
  for (const site of S.allow) {
    const li = document.createElement("li");
    li.innerHTML = `<span>${site}</span><button>Block again</button>`;
    li.querySelector("button").onclick = () => send({ type: "allow", site, on: false }).then(load);
    allow.append(li);
  }
}
async function load() { st = await send({ type: "state" }); draw(); }

$("alpha").oninput = e => { $("alphaV").textContent = e.target.value; };
$("alpha").onchange = e => set({ alpha: Number(e.target.value) });
$("searx").onchange = e => set({ custom: { ...st.settings.custom, searx: e.target.value.trim() } });
for (const k of ["blocker", "tor", "rfp", "webrtc"]) $(k).onchange = e => set({ [k]: e.target.checked });
$("update").onclick = async () => {
  $("updMsg").textContent = "downloading…";
  const r = await send({ type: "lists" });
  $("updMsg").textContent = r.ok ? `done: ${r.count.toLocaleString()} domains` : "couldn't download the lists (offline?)";
  load();
};
$("burnBtn").onclick = async () => {
  if (confirm("Burn everything?\n\nCookies, history, cache and site data are deleted, every tab closes, and Tor gets a new identity.")) send({ type: "burn" });
};
send({ type: "tor" }).then(t => {
  if (!t.ok) $("torInfo").textContent += " Tor isn't running right now (grim-browser starts it).";
});
load();
