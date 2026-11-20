(async () => {
  const st = await browser.runtime.sendMessage({ type: "state" });
  const sel = document.getElementById("engine");
  for (const e of GRIM_ENGINES) sel.add(new Option(e.name, e.id, false, e.id === st.settings.engine));
  if (browser.extension.inIncognitoContext && st.settings.tor) {
    document.getElementById("hint").className = "private";
    document.getElementById("hint").textContent = "Private window: everything here goes through Tor and is forgotten when you close it.";
  }
  document.getElementById("f").onsubmit = ev => {
    ev.preventDefault();
    const q = document.getElementById("q").value.trim();
    if (q) location.href = grimSearchUrl(sel.value, q, st.settings.custom);
  };
})();
