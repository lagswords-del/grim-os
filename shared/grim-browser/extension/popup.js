const send = m => browser.runtime.sendMessage(m);
(async () => {
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  let site = "";
  try { const u = new URL(tab.url); if (/^https?:$/.test(u.protocol)) site = u.hostname.replace(/^www\./, ""); } catch (e) {}
  const st = await send({ type: "state", tabId: tab.id });
  document.getElementById("count").textContent = st.blockedHere;
  document.getElementById("site").textContent = site || "this page";
  if (!site) document.getElementById("here").closest(".switch").style.display = "none";   // Grim's own pages, files
  const here = document.getElementById("here");
  here.checked = st.settings.blocker && !st.settings.allow.includes(site);
  here.disabled = !site || !st.settings.blocker;
  here.onchange = () => send({ type: "allow", site, on: !here.checked }).then(() => browser.tabs.reload(tab.id));
  const torOn = document.getElementById("torOn");
  torOn.checked = st.settings.tor;
  torOn.onchange = () => send({ type: "set", settings: { tor: torOn.checked } });
  const t = await send({ type: "tor" });
  document.getElementById("tor").textContent = t.ok
    ? (t.ready ? "Tor is connected" : `Tor is starting (${t.progress || 0}%)`)
    : "Tor isn't running: start Grim Browser from its icon or the grim-browser command";
  // Burn asks inside the popup (Firefox cuts off normal dialogs in extension popups)
  const burnBtn = document.getElementById("burn");
  let armed = null;
  burnBtn.onclick = async () => {
    if (!armed) {
      burnBtn.textContent = "Press again: delete everything, close all tabs";
      armed = setTimeout(() => { armed = null; burnBtn.textContent = "🔥 Burn everything"; }, 4000);
      return;
    }
    clearTimeout(armed);
    burnBtn.textContent = "Burning…"; burnBtn.disabled = true;
    await send({ type: "burn" }); window.close();
  };
  document.getElementById("newid").onclick = async () => {
    const r = await send({ type: "newnym" });
    document.getElementById("tor").textContent = r.ok ? "New Tor identity: new private windows use a new route" : "Couldn't reach Tor";
  };
  document.getElementById("settings").onclick = () => { browser.runtime.openOptionsPage(); window.close(); };
})();
