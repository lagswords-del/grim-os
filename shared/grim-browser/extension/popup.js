const send = m => browser.runtime.sendMessage(m);
(async () => {
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  let site = ""; try { site = new URL(tab.url).hostname.replace(/^www\./, ""); } catch (e) {}
  const st = await send({ type: "state", tabId: tab.id });
  document.getElementById("count").textContent = st.blockedHere;
  document.getElementById("site").textContent = site || "this page";
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
  document.getElementById("burn").onclick = async () => {
    if (!confirm("Burn everything?\n\nCookies, history, cache and site data are deleted, every tab closes, and Tor gets a new identity. This can't be undone.")) return;
    await send({ type: "burn" }); window.close();
  };
  document.getElementById("newid").onclick = async () => {
    const r = await send({ type: "newnym" });
    document.getElementById("tor").textContent = r.ok ? "New Tor identity: new private windows use a new route" : "Couldn't reach Tor";
  };
  document.getElementById("settings").onclick = () => { browser.runtime.openOptionsPage(); window.close(); };
})();
