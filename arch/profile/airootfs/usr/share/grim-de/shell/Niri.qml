pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io

// Live workspaces and windows from niri's event stream.
Singleton {
    id: root
    property var ws: ({})        // id -> workspace
    property var win: ({})       // id -> window
    property var focusedWin: null
    property bool inOverview: false     // in the overview you can look at the hidden workspace

    // the workspace that holds windows hidden into the dock (declared in Grim DE's niri config)
    readonly property var hiddenWs: Object.values(ws).find(w => w.name === "hidden") || null
    readonly property var hiddenId: hiddenWs ? hiddenWs.id : -1

    // workspaces of the focused output, in order, without the hidden one: [{ idx, num, active, occupied }]
    readonly property var workspaces: {
        const all = Object.values(ws)
        if (!all.length) return []
        const fo = (all.find(w => w.is_focused) || all[0]).output
        const counts = {}
        for (const w of Object.values(win)) counts[w.workspace_id] = (counts[w.workspace_id] || 0) + 1
        return all.filter(w => w.output === fo && w.id !== hiddenId).sort((a, b) => a.idx - b.idx)
                  .map((w, i) => ({ idx: w.idx, num: i + 1, active: w.is_active, occupied: !!counts[w.id] }))
    }
    readonly property int activeIdx: { const a = workspaces.find(w => w.active); return a ? a.idx : 1 }
    readonly property var windows: Object.values(win)
    readonly property var shownWindows: windows.filter(w => w.workspace_id !== hiddenId)
    function isHidden(w) { return !!w && w.workspace_id === hiddenId }

    // hide a window into the dock / bring it back onto the workspace you're on
    function hide(id) {
        const move = "niri msg action move-window-to-workspace --window-id " + id + " --focus false hidden"
        if (hiddenWs) {
            Quickshell.execDetached(["sh", "-c", move])
        } else {
            // first hide: niri's spare empty workspace at the end becomes "hidden" (niri makes a new spare)
            const all = Object.values(ws)
            const f = all.find(w => w.is_focused)
            const last = f ? Math.max(...all.filter(w => w.output === f.output).map(w => w.idx)) : 0
            Quickshell.execDetached(["sh", "-c", "niri msg action set-workspace-name --workspace " + last + " hidden && " + move])
        }
        syncSoon.restart()
    }
    function restore(id) {
        Quickshell.execDetached(["sh", "-c", "niri msg action move-window-to-workspace --window-id " + id + " --focus false " + activeIdx
                                 + " && niri msg action focus-window --id " + id])
        syncSoon.restart()
    }

    // niri doesn't always send a "window changed" event when a window moves to another
    // workspace without the focus following it, so read the window list again after moves
    Process {
        id: winSync
        command: ["niri", "msg", "--json", "windows"]
        stdout: StdioCollector {
            onStreamFinished: {
                let list
                try { list = JSON.parse(this.text) } catch (err) { return }
                const m = {}
                for (const w of list) m[w.id] = w
                root.win = m
                root.focusedWin = list.find(w => w.is_focused) || null
                tidy.restart()
            }
        }
    }
    Timer { id: syncSoon; interval: 350; onTriggered: winSync.running = true }

    // keep the hidden workspace last (just before niri's spare empty one), so Super+1..9 and
    // scrolling through workspaces don't land on it
    Timer {
        id: tidy
        interval: 250
        onTriggered: {
            const h = root.hiddenWs; if (!h) return
            // nothing hidden any more: drop the name so niri tidies the empty workspace away
            if (!Object.values(root.win).some(w => w.workspace_id === h.id)) {
                if (!h.is_active) Quickshell.execDetached(["niri", "msg", "action", "unset-workspace-name", "hidden"])
                return
            }
            const same = Object.values(root.ws).filter(w => w.output === h.output).sort((a, b) => a.idx - b.idx)
            const last = same[same.length - 1]
            const lastIsSpare = last && last.id !== h.id && !last.name && !Object.values(root.win).some(w => w.workspace_id === last.id)
            const target = lastIsSpare ? same.length - 1 : same.length
            if (h.idx !== target)
                Quickshell.execDetached(["niri", "msg", "action", "move-workspace-to-index", "--reference", "hidden", String(target)])
        }
    }
    property int lastActiveIdx: 1
    // you went onto the hidden workspace by scrolling or Super+N: carry on past it
    function skipHidden(prevIdx) {
        const h = hiddenWs; if (!h) return
        const next = prevIdx < h.idx ? h.idx + 1 : Math.max(1, h.idx - 1)
        Quickshell.execDetached(["niri", "msg", "action", "focus-workspace", String(next)])
    }
    readonly property string title: focusedWin ? (focusedWin.title || focusedWin.app_id || "") : ""

    function focusWorkspace(idx) { Quickshell.execDetached(["niri", "msg", "action", "focus-workspace", String(idx)]) }
    function focusWindow(id) { Quickshell.execDetached(["niri", "msg", "action", "focus-window", "--id", String(id)]) }
    function windowsOf(appId) {
        const a = (appId || "").toLowerCase()
        return windows.filter(w => (w.app_id || "").toLowerCase() === a)
    }

    Process {
        running: !!Quickshell.env("NIRI_SOCKET")
        command: ["niri", "msg", "--json", "event-stream"]
        stdout: SplitParser {
            onRead: (line) => {
                let e
                try { e = JSON.parse(line) } catch (err) { return }
                if (e.WorkspacesChanged) {
                    const m = {}
                    for (const w of e.WorkspacesChanged.workspaces) m[w.id] = w
                    root.ws = m
                    tidy.restart()
                } else if (e.WorkspaceActivated) {
                    const a = e.WorkspaceActivated, m = Object.assign({}, root.ws), t = m[a.id]
                    if (!t) return
                    if (t.name === "hidden" && a.focused && !root.inOverview) root.skipHidden(root.lastActiveIdx)
                    else if (a.focused) root.lastActiveIdx = t.idx
                    for (const id in m) {
                        const w = Object.assign({}, m[id])
                        if (w.output === t.output) w.is_active = (w.id === a.id)
                        if (a.focused) w.is_focused = (w.id === a.id)
                        m[id] = w
                    }
                    root.ws = m
                } else if (e.WorkspaceActiveWindowChanged) {
                    syncSoon.restart()   // also catches windows hidden with the keybind (grim-de hide)
                } else if (e.OverviewOpenedOrClosed) {
                    root.inOverview = e.OverviewOpenedOrClosed.is_open
                } else if (e.WindowsChanged) {
                    const m = {}
                    for (const w of e.WindowsChanged.windows) m[w.id] = w
                    root.win = m
                    root.focusedWin = Object.values(m).find(w => w.is_focused) || null
                } else if (e.WindowOpenedOrChanged) {
                    const w = e.WindowOpenedOrChanged.window, m = Object.assign({}, root.win)
                    if (w.is_focused) for (const id in m) m[id] = Object.assign({}, m[id], { is_focused: false })
                    m[w.id] = w
                    root.win = m
                    tidy.restart()
                    if (w.is_focused) root.focusedWin = w
                    else if (root.focusedWin && root.focusedWin.id === w.id) root.focusedWin = w
                } else if (e.WindowClosed) {
                    const m = Object.assign({}, root.win)
                    delete m[e.WindowClosed.id]
                    root.win = m
                    if (root.focusedWin && root.focusedWin.id === e.WindowClosed.id) root.focusedWin = null
                } else if (e.WindowFocusChanged) {
                    const fid = e.WindowFocusChanged.id, m = {}
                    for (const id in root.win) m[id] = Object.assign({}, root.win[id], { is_focused: Number(id) === fid })
                    root.win = m
                    root.focusedWin = fid !== null && fid !== undefined ? (m[fid] || null) : null
                }
            }
        }
    }
}
