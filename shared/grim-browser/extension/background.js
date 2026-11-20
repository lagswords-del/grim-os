// Grim Shield: the background part.
//   - blocks ads and trackers (a built-in list + EasyList, EasyPrivacy and Peter Lowe's list, updated daily)
//   - sends every private-window request through Tor (127.0.0.1:9150, started by grim-browser)
//   - "Burn": clears cookies, history, cache and site data, closes tabs, asks Tor for a new identity
//   - themes (with transparency), fingerprinting switches, the omnibox keyword "g", the welcome page

const DEFAULTS = {
  blocker: true,
  tor: true,             // private windows through Tor
  rfp: true,             // resistFingerprinting
  webrtc: true,          // WebRTC can't show your IP
  engine: "ddg",
  custom: { searx: "" },
  theme: "grim",
  alpha: 0,              // 0-60: how see-through the browser's frame is
  allow: [],             // sites where blocking is off
  lists: { updated: 0, count: 0 },
};
const LISTS = [
  ["EasyList", "https://easylist.to/easylist/easylist.txt"],
  ["EasyPrivacy", "https://easylist.to/easylist/easyprivacy.txt"],
  ["Peter Lowe's list", "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=nohtml&showintro=0&mimetype=plaintext"],
];
const TOR = { type: "socks", host: "127.0.0.1", port: 9150, proxyDNS: true, failoverTimeout: 5 };

let S = structuredClone(DEFAULTS);
let blocked = new Set(GRIM_SEED);   // domains to block
let excepted = new Set();           // @@||domain^ exceptions from the lists
const perTab = new Map();           // tabId -> number blocked on the current page

// ------------------------------------------------------------------ settings
async function load() {
  const got = await browser.storage.local.get(["settings", "domains", "exceptions"]);
  S = { ...structuredClone(DEFAULTS), ...(got.settings || {}) };
  if (got.domains) blocked = new Set([...GRIM_SEED, ...got.domains]);
  if (got.exceptions) excepted = new Set(got.exceptions);
  await applyPrivacy();
  await applyTheme();
}
async function save() { await browser.storage.local.set({ settings: S }); }

async function applyPrivacy() {
  try { await browser.privacy.websites.resistFingerprinting.set({ value: !!S.rfp }); } catch (e) {}
  try {
    await browser.privacy.network.webRTCIPHandlingPolicy.set({ value: S.webrtc ? "disable_non_proxied_udp" : "default" });
  } catch (e) {}
}

// ------------------------------------------------------------------ themes
const THEMES = {
  grim:     { name: "Grim",     bg: [10, 10, 10],   bar: [24, 24, 24],    text: [232, 232, 232], accent: [193, 18, 31] },
  bone:     { name: "Bone",     bg: [236, 232, 224], bar: [248, 245, 238], text: [30, 30, 30],   accent: [150, 20, 30] },
  void:     { name: "Void",     bg: [6, 6, 12],     bar: [16, 16, 26],    text: [220, 220, 235], accent: [120, 60, 200] },
  midnight: { name: "Midnight", bg: [12, 18, 30],   bar: [20, 28, 44],    text: [214, 222, 235], accent: [80, 140, 230] },
  ember:    { name: "Ember",    bg: [20, 10, 8],    bar: [36, 18, 12],    text: [240, 225, 210], accent: [230, 110, 30] },
  ash:      { name: "Ash",      bg: [40, 40, 40],   bar: [54, 54, 54],    text: [230, 230, 230], accent: [200, 200, 200] },
};
const PRIVATE_THEME = { bg: [24, 6, 30], bar: [38, 12, 46], text: [235, 220, 245], accent: [160, 80, 220] };

function rgba(c, a = 1) { return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${a})`; }
function themeObject(t, alpha) {
  const a = 1 - Math.min(60, Math.max(0, alpha || 0)) / 100;
  return {
    colors: {
      frame: rgba(t.bg, a), frame_inactive: rgba(t.bg, a), tab_background_text: rgba(t.text),
      toolbar: rgba(t.bar, a), toolbar_text: rgba(t.text), toolbar_field: rgba(t.bg, Math.min(1, a + 0.1)),
      toolbar_field_text: rgba(t.text), toolbar_field_border_focus: rgba(t.accent),
      tab_selected: rgba(t.bar, a), tab_text: rgba(t.text), tab_line: rgba(t.accent), tab_loading: rgba(t.accent),
      popup: rgba(t.bar), popup_text: rgba(t.text), popup_highlight: rgba(t.accent), popup_highlight_text: "#ffffff",
      button_background_active: rgba(t.accent, 0.5), icons: rgba(t.text), icons_attention: rgba(t.accent),
      ntp_background: rgba(t.bg), ntp_text: rgba(t.text), sidebar: rgba(t.bar), sidebar_text: rgba(t.text),
      toolbar_bottom_separator: rgba(t.accent, 0.6), toolbar_top_separator: "transparent",
    },
  };
}
async function applyTheme() {
  await browser.theme.update(themeObject(THEMES[S.theme] || THEMES.grim, S.alpha));
  for (const w of await browser.windows.getAll()) if (w.incognito) themePrivate(w.id);
}
function themePrivate(windowId) {
  browser.theme.update(windowId, themeObject(PRIVATE_THEME, S.alpha));
}
browser.windows.onCreated.addListener(w => { if (w.incognito) themePrivate(w.id); });

// ------------------------------------------------------------------ the blocker
// Domains one company uses for its own site: on that company's site, its own domains load
// (otherwise facebook.com or youtube.com would break). Elsewhere they're blocked as trackers.
const OWNERS = [
  ["facebook.com", "facebook.net", "fbcdn.net", "fbsbx.com", "messenger.com", "instagram.com", "cdninstagram.com", "whatsapp.com", "whatsapp.net"],
  ["google.com", "googleapis.com", "gstatic.com", "googleusercontent.com", "googlevideo.com", "youtube.com", "ytimg.com", "ggpht.com",
   "youtube-nocookie.com", "doubleclick.net", "google-analytics.com", "googletagmanager.com", "googlesyndication.com", "googleadservices.com", "gmail.com"],
  ["twitter.com", "x.com", "twimg.com", "t.co", "ads-twitter.com"],
  ["microsoft.com", "live.com", "bing.com", "msn.com", "office.com", "microsoftonline.com", "clarity.ms", "linkedin.com", "licdn.com", "github.com", "githubusercontent.com"],
  ["amazon.com", "amazon.co.uk", "amazon.de", "media-amazon.com", "ssl-images-amazon.com", "amazon-adsystem.com", "primevideo.com", "twitch.tv", "jtvnw.net"],
  ["reddit.com", "redd.it", "redditmedia.com", "redditstatic.com"],
  ["tiktok.com", "tiktokcdn.com", "byteoversea.com", "ibytedtos.com"],
  ["yahoo.com", "yimg.com", "aol.com"],
];
function ownerOf(host) {
  for (let i = 0; i < OWNERS.length; i++)
    if (OWNERS[i].some(d => host === d || host.endsWith("." + d))) return i;
  return -1;
}

function hostOf(url) { try { return new URL(url).hostname.replace(/^www\./, ""); } catch (e) { return ""; } }
function inSet(set, host) {
  for (let h = host; h; h = h.slice(h.indexOf(".") + 1)) {
    if (set.has(h)) return true;
    if (!h.includes(".")) break;
  }
  return false;
}
function shouldBlock(details) {
  if (!S.blocker || details.type === "main_frame") return false;
  const host = hostOf(details.url);
  if (!host || !inSet(blocked, host) || inSet(excepted, host)) return false;
  const site = hostOf(details.documentUrl || details.originUrl || "");
  if (site && S.allow.includes(site)) return false;
  // a site's own domain is never blocked on itself (keeps logins and pages working)
  if (site && (site === host || site.endsWith("." + host) || host.endsWith("." + site))) return false;
  const owner = ownerOf(host);
  if (site && owner >= 0 && owner === ownerOf(site)) return false;
  return true;
}
browser.webRequest.onBeforeRequest.addListener(details => {
  if (!shouldBlock(details)) return {};
  if (details.tabId >= 0) {
    const n = (perTab.get(details.tabId) || 0) + 1;
    perTab.set(details.tabId, n);
    browser.browserAction.setBadgeText({ tabId: details.tabId, text: String(n) });
  }
  return { cancel: true };
}, { urls: ["<all_urls>"] }, ["blocking"]);

browser.webRequest.onBeforeRequest.addListener(d => {
  if (d.type === "main_frame" && d.tabId >= 0) { perTab.set(d.tabId, 0); browser.browserAction.setBadgeText({ tabId: d.tabId, text: "" }); }
}, { urls: ["<all_urls>"], types: ["main_frame"] });
browser.tabs.onRemoved.addListener(id => perTab.delete(id));
browser.browserAction.setBadgeBackgroundColor({ color: "#c1121f" });

// Lists: keep the lines that block a whole domain (||example.com^ with no path), and the exceptions.
function parseList(text) {
  const add = [], allow = [];
  for (let line of text.split("\n")) {
    line = line.trim();
    if (!line || line[0] === "!" || line[0] === "[" || line.includes("##") || line.includes("#@#")) continue;
    let m = line.match(/^(@@)?\|\|([a-z0-9.-]+\.[a-z]{2,})\^(\$(third-party|3p|all|doc|script|image|xhr|ping|subdocument|,)*)?$/i);
    if (m) { (m[1] ? allow : add).push(m[2].toLowerCase()); continue; }
    if (/^[a-z0-9.-]+\.[a-z]{2,}$/i.test(line)) add.push(line.toLowerCase());   // plain host lists
  }
  return { add, allow };
}
async function updateLists() {
  const add = new Set(), allow = new Set();
  let ok = 0;
  for (const [, url] of LISTS) {
    try {
      const r = await fetch(url, { cache: "no-store", credentials: "omit" });
      if (!r.ok) continue;
      const p = parseList(await r.text());
      p.add.forEach(d => add.add(d)); p.allow.forEach(d => allow.add(d));
      ok++;
    } catch (e) {}
  }
  if (!ok) return { ok: false, count: blocked.size };
  blocked = new Set([...GRIM_SEED, ...add]);
  excepted = allow;
  S.lists = { updated: Date.now(), count: blocked.size, sources: ok };
  await browser.storage.local.set({ domains: [...add], exceptions: [...allow] });
  await save();
  return { ok: true, count: blocked.size };
}
browser.alarms.create("lists", { periodInMinutes: 24 * 60 });
browser.alarms.onAlarm.addListener(a => { if (a.name === "lists") updateLists(); });

// ------------------------------------------------------------------ private windows through Tor
browser.proxy.onRequest.addListener(details => {
  if (!S.tor || !details.incognito) return { type: "direct" };
  const host = hostOf(details.url);
  if (host === "localhost" || host === "127.0.0.1" || host === "::1") return { type: "direct" };
  return TOR;
}, { urls: ["<all_urls>"] });
browser.proxy.onError.addListener(() => {});

// ------------------------------------------------------------------ Tor helper (native messaging)
async function native(cmd) {
  try { return await browser.runtime.sendNativeMessage("grim_browser", { cmd }); }
  catch (e) { return { ok: false, error: String(e.message || e) }; }
}

// ------------------------------------------------------------------ burn
async function burn() {
  await browser.browsingData.remove({ since: 0 }, {
    cache: true, cookies: true, downloads: true, formData: true, history: true,
    indexedDB: true, localStorage: true, pluginData: true, serviceWorkers: true,
  });
  const tor = await native("newnym");
  // close every tab and start fresh
  const tabs = await browser.tabs.query({});
  const fresh = await browser.tabs.create({ url: "newtab.html", active: true });
  await browser.tabs.remove(tabs.map(t => t.id).filter(id => id !== fresh.id));
  perTab.clear();
  browser.notifications.create({
    type: "basic", iconUrl: "icons/48.png", title: "Burned",
    message: "Cookies, history, cache and site data are gone." + (tor.ok ? " Tor has a new identity." : ""),
  });
  return { ok: true, tor: tor.ok };
}
browser.commands.onCommand.addListener(c => { if (c === "burn") burn(); });

// ------------------------------------------------------------------ search
browser.omnibox.setDefaultSuggestion({ description: "Search with Grim (type: g words)" });
browser.omnibox.onInputEntered.addListener((text, disposition) => {
  const url = grimSearchUrl(S.engine, text, S.custom);
  if (disposition === "currentTab") browser.tabs.update({ url }); else browser.tabs.create({ url });
});
browser.menus.create({ id: "grim-search", title: "Search Grim for “%s”", contexts: ["selection"] });
browser.menus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "grim-search")
    browser.tabs.create({ url: grimSearchUrl(S.engine, info.selectionText, S.custom), openerTabId: tab.id });
});

// ------------------------------------------------------------------ messages from the popup and pages
browser.runtime.onMessage.addListener(async (m, sender) => {
  switch (m.type) {
    case "state": {
      const tab = m.tabId ?? sender.tab?.id;
      return { settings: S, themes: THEMES, engines: GRIM_ENGINES, blockedHere: perTab.get(tab) || 0, listSize: blocked.size };
    }
    case "set":
      S = { ...S, ...m.settings };
      await save(); await applyPrivacy(); await applyTheme();
      return { settings: S };
    case "allow": {
      const site = m.site;
      S.allow = m.on ? [...new Set([...S.allow, site])] : S.allow.filter(s => s !== site);
      await save();
      return { allow: S.allow };
    }
    case "lists": return await updateLists();
    case "burn": return await burn();
    case "tor": return await native("status");
    case "newnym": return await native("newnym");
    case "search": return { url: grimSearchUrl(m.engine || S.engine, m.query, S.custom) };
  }
});

// ------------------------------------------------------------------ first run
browser.runtime.onInstalled.addListener(async ({ reason }) => {
  if (reason === "install") {
    await load();
    await save();
    browser.tabs.create({ url: "welcome.html" });
    updateLists();
  }
});

load().then(() => { if (!S.lists.updated || Date.now() - S.lists.updated > 24 * 3600e3) updateLists(); });
