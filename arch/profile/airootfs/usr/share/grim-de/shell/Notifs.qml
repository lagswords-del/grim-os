pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Services.Notifications

// Grim Shell is the desktop's notification server. It keeps a history for the
// notification centre, shows pop-ups, and holds Do Not Disturb (saved across logins).
Singleton {
    id: root
    readonly property var list: server.trackedNotifications.values.slice().reverse()   // newest first
    property var popups: []            // shown as pop-ups right now
    property var times: ({})           // notification id -> when it arrived
    property int unread: 0
    property int panelsOpen: 0         // bar dropdowns open; pop-ups wait while you're in one
    readonly property bool dnd: st.dnd

    function setDnd(v) { st.dnd = v; if (v) popups = [] }
    function hide(n) { popups = popups.filter(x => x !== n) }
    function dismiss(n) { hide(n); n.dismiss() }
    function clearAll() { popups = []; for (const n of list) n.dismiss() }
    function markRead() { unread = 0 }
    function ago(n) {
        const t = times[n.id]; if (!t) return ""
        const m = Math.floor((Date.now() - t) / 60000)
        return m < 1 ? "now" : m < 60 ? m + " min" : Math.floor(m / 60) + " h"
    }
    // the action to run when the notification itself is clicked
    function activate(n) {
        const a = n.actions.find(x => x.identifier === "default") || (n.actions.length === 1 ? n.actions[0] : null)
        if (a) a.invoke(); else dismiss(n)
    }

    FileView {
        path: (Quickshell.env("XDG_STATE_HOME") || Quickshell.env("HOME") + "/.local/state") + "/grim-de/shell-state.json"
        watchChanges: true
        onFileChanged: reload()
        onAdapterUpdated: writeAdapter()
        onLoadFailed: (err) => { if (err === FileViewError.FileNotFound) writeAdapter() }
        JsonAdapter { id: st; property bool dnd: false }
    }

    NotificationServer {
        id: server
        keepOnReload: true
        bodySupported: true
        bodyMarkupSupported: true
        bodyHyperlinksSupported: true
        actionsSupported: true
        imageSupported: true
        persistenceSupported: true
        onNotification: (n) => {
            n.tracked = true
            const t = Object.assign({}, root.times); t[n.id] = Date.now(); root.times = t
            n.closed.connect(() => root.hide(n))
            if (n.lastGeneration) return          // kept from before a shell reload: history only
            if (!n.transient) root.unread++
            if (!root.dnd || n.urgency === NotificationUrgency.Critical)
                root.popups = root.popups.filter(x => x.id !== n.id).concat([n]).slice(-4)
        }
    }
    // let time labels ("3 min") move on
    property int tick: 0
    Timer { interval: 60000; running: true; repeat: true; onTriggered: root.tick++ }
}
