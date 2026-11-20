pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io

// Everything the shell draws comes from ~/.config/grim-de/shell.json (written by grim-de),
// so changes in Grim DE Settings show up here straight away.
Singleton {
    id: root
    property var d: ({})
    readonly property string dir: (Quickshell.env("XDG_CONFIG_HOME") || (Quickshell.env("HOME") + "/.config")) + "/grim-de"

    FileView {
        path: root.dir + "/shell.json"
        watchChanges: true
        onFileChanged: reload()
        onLoaded: { try { root.d = JSON.parse(text()) } catch (e) { console.warn("grim shell: bad shell.json", e) } }
    }

    function c(key, fallback) { return (d.colors && d.colors[key]) ? d.colors[key] : fallback }
    function alpha(col, a) { return Qt.rgba(col.r, col.g, col.b, a) }
    function glyph(cp) { return String.fromCodePoint(cp) }

    readonly property color bg: c("bg", "#2e3440")
    readonly property color bg2: c("bg2", "#3b4252")
    readonly property color bg3: c("bg3", "#434c5e")
    readonly property color fg: c("fg", "#d8dee9")
    readonly property color muted: c("muted", "#7b88a1")
    readonly property color accent: c("accent", "#88c0d0")
    readonly property color accentFg: c("accent_fg", "#2e3440")
    readonly property color accent2: c("accent2", "#b48ead")
    readonly property color urgent: c("urgent", "#bf616a")

    readonly property bool glass: d.glass !== undefined ? d.glass : true
    readonly property real panelOpacity: glass ? (d.panel_opacity || 0.72) : 1.0
    readonly property color panel: alpha(bg, panelOpacity)
    readonly property int radius: d.radius !== undefined ? d.radius : 10
    readonly property bool gameMode: !!d.game_mode
    readonly property string dockPos: dock.position || "bottom"   // a string, so it only signals real moves
    readonly property string workspaceStyle: d.workspace_style || "dots"
    readonly property bool win7: !!d.win7

    readonly property string font: d.fonts ? d.fonts.ui : "Noto Sans"
    readonly property int fontSize: d.fonts ? d.fonts.ui_size : 11
    readonly property string mono: d.fonts ? d.fonts.mono : "Inconsolata Nerd Font Mono"

    readonly property var bar: d.bar || ({ enabled: true, position: "top", height: 32, clock24: true,
                                            modules: ["workspaces", "title", "clock", "tray", "volume", "network", "battery", "power"] })
    readonly property var dock: d.dock || ({ enabled: true, size: 44, autohide: false, pinned: [] })
    function shows(m) { return (bar.modules || []).indexOf(m) >= 0 }
}
