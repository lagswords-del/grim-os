import QtQuick
import Quickshell
import Quickshell.Wayland

// A small glass panel that hangs under a bar icon. The bar sets `open`; clicking anywhere
// else closes it (niri popup grab), and the panel then asks the bar to close it.
PopupWindow {
    id: root
    property Item anchorItem
    property var barWindow
    property bool open: false
    signal requestClose()
    default property alias content: body.data
    property int panelWidth: 300
    readonly property int panelHeight: body.childrenRect.height + 28
    readonly property bool atBottom: Theme.bar.position === "bottom"

    anchor.window: barWindow
    anchor.rect.x: {
        if (!anchorItem || !barWindow) return 0
        // touch these so the position updates when the bar layout moves the icon
        root.open; anchorItem.x; anchorItem.width; if (anchorItem.parent) anchorItem.parent.x
        const p = anchorItem.mapToItem(null, anchorItem.width / 2, 0)
        return Math.max(8, Math.min(barWindow.width - panelWidth - 8, p.x - panelWidth / 2))
    }
    anchor.rect.y: atBottom ? -(panelHeight + 8) : (barWindow ? barWindow.height : 32) + 6
    implicitWidth: panelWidth
    implicitHeight: panelHeight + 4
    color: "transparent"
    visible: false                       // set in code: the compositor may hide a popup on its own
    onOpenChanged: open ? (visible = true) : hideLater.restart()
    Timer { id: hideLater; interval: 150; onTriggered: if (!root.open) root.visible = false }
    grabFocus: !barWindow || barWindow.grab !== false
    onVisibleChanged: if (!visible && open) requestClose()

    Region { id: panelRegion; item: panel; radius: panel.radius }
    Region { id: noRegion; x: 0; y: 0; width: 1; height: 1 }   // an empty region would mean "blur everything" to niri
    BackgroundEffect.blurRegion: Theme.glass ? panelRegion : noRegion

    Rectangle {
        id: panel
        anchors.fill: parent
        anchors.bottomMargin: 4
        radius: Math.min(Theme.radius + 4, 16)
        color: Theme.alpha(Theme.bg, Theme.glass ? Math.min(Theme.panelOpacity + 0.14, 0.97) : 1)
        border.width: 1; border.color: Theme.alpha(Theme.fg, 0.1)
        opacity: root.open ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: 140 } }
        transform: Translate { y: root.open ? 0 : (root.atBottom ? 8 : -8); Behavior on y { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } } }
        Item {
            id: body
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 14 }
        }
    }
}
