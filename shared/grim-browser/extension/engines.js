// The search engines Grim knows. {q} is replaced with the search words.
const GRIM_ENGINES = [
  { id: "ddg",       name: "DuckDuckGo",   url: "https://duckduckgo.com/?q={q}",                      note: "private, the default" },
  { id: "ddghtml",   name: "DuckDuckGo (no JavaScript)", url: "https://html.duckduckgo.com/html/?q={q}", note: "fastest, works over Tor" },
  { id: "startpage", name: "Startpage",    url: "https://www.startpage.com/sp/search?query={q}",      note: "Google's results without Google" },
  { id: "brave",     name: "Brave Search", url: "https://search.brave.com/search?q={q}",              note: "its own index" },
  { id: "mojeek",    name: "Mojeek",       url: "https://www.mojeek.com/search?q={q}",                note: "independent, no tracking" },
  { id: "searx",     name: "SearXNG",      url: "https://searx.be/search?q={q}",                      note: "mixes many engines (set your own server)" },
  { id: "wiki",      name: "Wikipedia",    url: "https://en.wikipedia.org/w/index.php?search={q}",    note: "" },
  { id: "yt",        name: "YouTube (through Invidious)", url: "https://yewtu.be/search?q={q}", note: "YouTube without Google tracking" },
];
function grimEngine(id, custom) {
  const e = GRIM_ENGINES.find(x => x.id === id) || GRIM_ENGINES[0];
  if (e.id === "searx" && custom && custom.searx) return { ...e, url: custom.searx.replace(/\/+$/, "") + "/search?q={q}" };
  return e;
}
function grimSearchUrl(engineId, query, custom) {
  return grimEngine(engineId, custom).url.replace("{q}", encodeURIComponent(query));
}
