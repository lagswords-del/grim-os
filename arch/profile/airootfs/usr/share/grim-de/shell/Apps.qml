pragma Singleton
import QtQuick
import Quickshell

// Apps for the dock and the Windows 7 taskbar: pinned apps first, then anything else that's open.
// Windows are matched to apps through their desktop entry (md.obsidian.Obsidian -> obsidian).
Singleton {
    id: root

    function entryFor(id) {
        DesktopEntries.applications.values.length      // look again once the entries have loaded
        return DesktopEntries.byId(id) || DesktopEntries.heuristicLookup(id)
    }
    function keyOf(id) { const e = entryFor(id); return (e ? e.id : id).toLowerCase() }
    function nameOf(id) { const e = entryFor(id); return e ? e.name : id }

    readonly property var list: {
        const out = [], seen = {}
        for (const p of (Theme.dock.pinned || [])) { const k = keyOf(p); if (!seen[k]) { seen[k] = true; out.push(p) } }
        for (const w of Niri.windows) {
            if (!w.app_id) continue
            const k = keyOf(w.app_id)
            if (!seen[k]) { seen[k] = true; out.push(w.app_id) }
        }
        return out
    }
    function windowsFor(id) { const k = keyOf(id); return Niri.windows.filter(w => w.app_id && keyOf(w.app_id) === k) }
    function shownFor(id) { return windowsFor(id).filter(w => !Niri.isHidden(w)) }
    function hiddenFor(id) { return windowsFor(id).filter(w => Niri.isHidden(w)) }

    // Click on an app, like a Windows taskbar:
    //   hidden windows      -> bring them back
    //   app is focused      -> hide its window into the dock
    //   open somewhere else -> focus it
    //   not open            -> start it
    function click(id) {
        const shown = shownFor(id), hidden = hiddenFor(id)
        if (hidden.length && !shown.length) { for (const w of hidden) Niri.restore(w.id); return }
        const f = shown.find(w => w.is_focused)
        if (f) { Niri.hide(f.id); return }
        if (shown.length) { Niri.focusWindow(shown[0].id); return }
        if (hidden.length) { Niri.restore(hidden[0].id); return }
        launch(id)
    }
    function launch(id) {
        const e = entryFor(id)
        if (id === "Alacritty") Quickshell.execDetached(["grim-de", "term"])
        else if (e) e.execute()
        else Quickshell.execDetached([id])
    }

    // "show desktop": hide every window on this workspace; click again to bring them back
    property var desktopStash: []
    function toggleDesktop() {
        if (desktopStash.length) {
            for (const id of desktopStash) if (Niri.win[id] && Niri.isHidden(Niri.win[id])) Niri.restore(id)
            desktopStash = []
            return
        }
        const a = Object.values(Niri.ws).find(w => w.is_focused)
        const here = Niri.windows.filter(w => a && w.workspace_id === a.id)
        desktopStash = here.map(w => w.id)
        for (const w of here) Niri.hide(w.id)
    }

    // every place an app icon can live; AppIcon tries them in order
    readonly property string home: Quickshell.env("HOME") || ""
    function iconCandidates(icon, id) {
        const out = []
        const add = (u) => { if (u && out.indexOf(u) < 0) out.push(u) }
        if (icon.startsWith("/")) add("file://" + icon)
        const names = []
        for (const n of [icon, id, id.toLowerCase(), id.split(".").pop(), id.split(".").pop().toLowerCase()])
            if (n && !n.startsWith("/") && names.indexOf(n) < 0) names.push(n)
        for (const n of names) add(Quickshell.iconPath(n, true))
        const roots = ["/usr/share/icons/hicolor", home + "/.local/share/icons/hicolor",
                       "/var/lib/flatpak/exports/share/icons/hicolor", home + "/.local/share/flatpak/exports/share/icons/hicolor"]
        for (const n of names) {
            for (const r of roots) {
                add("file://" + r + "/scalable/apps/" + n + ".svg")
                for (const sz of ["512x512", "256x256", "128x128", "96x96", "64x64", "48x48"]) add("file://" + r + "/" + sz + "/apps/" + n + ".png")
            }
            add("file:///usr/share/icons/Papirus/64x64/apps/" + n + ".svg")
            add("file:///usr/share/icons/Adwaita/scalable/apps/" + n + ".svg")
            add("file:///usr/share/pixmaps/" + n + ".svg")
            add("file:///usr/share/pixmaps/" + n + ".png")
        }
        return out
    }
}
