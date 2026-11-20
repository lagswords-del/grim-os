import QtQuick
import Quickshell

// One app in the dock or taskbar. Click: focus / hide / bring back / start (see Apps.click).
// Middle-click opens another window. A dot marks open apps, a ring marks hidden ones.
MouseArea {
    id: slot
    required property string appId
    property int size: 44
    property string side: "bottom"     // which screen edge the dock is on: tooltip and dot go the other way
    property bool win7: false          // Windows 7 taskbar button look
    readonly property var entry: Apps.entryFor(appId)
    readonly property var shown: Apps.shownFor(appId)
    readonly property var hidden: Apps.hiddenFor(appId)
    readonly property bool focused: shown.some(w => w.is_focused)
    implicitWidth: win7 ? size + 16 : size; implicitHeight: size
    width: implicitWidth; height: implicitHeight
    hoverEnabled: true; cursorShape: Qt.PointingHandCursor
    acceptedButtons: Qt.LeftButton | Qt.MiddleButton
    onClicked: (m) => { if (m.button === Qt.MiddleButton) Apps.launch(appId); else Apps.click(appId) }

    // Windows 7 button: glass highlight when open, brighter when focused or hovered
    Rectangle {
        visible: slot.win7 && (slot.shown.length || slot.hidden.length || slot.containsMouse)
        anchors.fill: parent; anchors.margins: 1
        radius: 4
        border.width: 1
        border.color: slot.focused ? "#c0e4ffff" : "#7fb6dcf2"
        gradient: Gradient {
            GradientStop { position: 0; color: slot.focused ? "#a0d2f4ff" : slot.containsMouse ? "#80b4d8f0" : "#50a8c8e6" }
            GradientStop { position: 0.48; color: slot.focused ? "#5c9cc8ee" : "#305f86a8" }
            GradientStop { position: 0.52; color: slot.focused ? "#3a7bb0e6" : "#20406484" }
            GradientStop { position: 1; color: slot.focused ? "#4a8cc4f2" : "#30507898" }
        }
    }

    readonly property var icons: Apps.iconCandidates(entry && entry.icon ? entry.icon : "", appId)
    property int iconIdx: 0
    onIconsChanged: iconIdx = 0
    property real iconSize: (slot.containsMouse && !slot.win7 ? 1.0 : 0.86) * (slot.win7 ? size * 0.78 : size)
    Behavior on iconSize { NumberAnimation { duration: 120 } }
    Image {
        id: img
        anchors.centerIn: parent
        width: slot.iconSize; height: slot.iconSize
        sourceSize: Qt.size(128, 128)
        smooth: true; mipmap: true
        opacity: slot.hidden.length && !slot.shown.length ? 0.6 : 1
        source: slot.iconIdx < slot.icons.length ? slot.icons[slot.iconIdx] : ""
        onStatusChanged: if (status === Image.Error || (status === Image.Ready && implicitWidth <= 1)) Qt.callLater(() => { if (slot) slot.iconIdx++ })
    }
    Rectangle {   // no icon anywhere: a letter tile
        visible: img.status !== Image.Ready
        anchors.centerIn: parent
        width: slot.iconSize * 0.9; height: width; radius: width * 0.28
        color: Theme.bg3
        Text { anchors.centerIn: parent; text: (slot.entry ? slot.entry.name : slot.appId).charAt(0).toUpperCase()
               color: Theme.accent; font.family: Theme.font; font.bold: true; font.pixelSize: parent.width * 0.5 }
    }

    // open: dot (wide when focused). hidden only: ring.
    Rectangle {
        visible: !slot.win7 && (slot.shown.length > 0 || slot.hidden.length > 0)
        readonly property bool ring: slot.shown.length === 0
        readonly property bool vert: slot.side === "left" || slot.side === "right"
        readonly property int len: ring ? 6 : slot.focused ? 14 : 5
        width: vert ? (ring ? 6 : 4) : len; height: vert ? len : (ring ? 6 : 4)
        radius: 3
        color: ring ? "transparent" : Theme.accent
        border.width: ring ? 1.5 : 0; border.color: Theme.accent
        x: slot.side === "left" ? -6 : slot.side === "right" ? slot.width + 2 : (slot.width - width) / 2
        y: slot.side === "bottom" ? slot.height + 1 : slot.side === "top" ? -7 : (slot.height - height) / 2
    }

    // name on hover
    Rectangle {
        visible: slot.containsMouse
        z: 10
        width: tip.width + 16; height: tip.height + 8; radius: 6
        color: Theme.alpha(Theme.bg, 0.92)
        x: slot.side === "left" ? slot.width + 12 : slot.side === "right" ? -width - 12 : (slot.width - width) / 2
        y: slot.side === "bottom" ? -height - 12 : slot.side === "top" ? slot.height + 12 : (slot.height - height) / 2
        Text { id: tip; anchors.centerIn: parent
               text: (slot.entry ? slot.entry.name : slot.appId) + (slot.hidden.length && !slot.shown.length ? "  (hidden)" : "")
               color: Theme.fg; font.family: Theme.font; font.pixelSize: Theme.fontSize + 1 }
    }
}
