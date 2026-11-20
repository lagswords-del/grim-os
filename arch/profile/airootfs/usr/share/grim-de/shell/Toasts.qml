import QtQuick
import Quickshell
import Quickshell.Wayland

// Notification pop-ups in the top-right corner (bottom-right when the bar is at the bottom).
PanelWindow {
    id: toasts
    readonly property bool atBottom: Theme.bar.position === "bottom"
    anchors { top: !atBottom; bottom: atBottom; right: true }
    margins { top: 8; bottom: 8; right: 10 }
    implicitWidth: 380
    implicitHeight: Math.max(1, col.implicitHeight)
    exclusiveZone: 0
    color: "transparent"
    visible: Notifs.popups.length > 0 && Notifs.panelsOpen === 0
    WlrLayershell.namespace: "grim-notifications"
    WlrLayershell.layer: WlrLayer.Overlay
    mask: Region { item: col }
    Column {
        id: col
        width: parent.width
        spacing: 8
        Repeater {
            model: Notifs.popups
            NotifCard { required property var modelData; notif: modelData; popup: true; width: col.width }
        }
    }
}
