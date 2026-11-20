import QtQuick
import QtQuick.Layouts

// Workspace markers for the bar and the dock: "dots" (pills that stretch for the active one)
// or "numbers" (1 2 3 in rounded squares). Click one to go there.
GridLayout {
    id: wsg
    property int h: 32                 // the bar or dock thickness to fit in
    property bool vertical: false
    readonly property bool numbers: Theme.workspaceStyle === "numbers"
    flow: vertical ? GridLayout.TopToBottom : GridLayout.LeftToRight
    rowSpacing: numbers ? 4 : 6; columnSpacing: numbers ? 4 : 6
    Repeater {
        model: Niri.workspaces
        MouseArea {
            id: ws
            required property var modelData
            readonly property int dot: Math.round(wsg.h * 0.36)
            readonly property int long: wsg.numbers ? Math.round(wsg.h * 0.72) : (modelData.active ? Math.round(wsg.h * 0.95) : Math.round(wsg.h * 0.42))
            implicitWidth: wsg.vertical ? wsg.h : long
            implicitHeight: wsg.vertical ? long : wsg.h
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
            onClicked: Niri.focusWorkspace(modelData.idx)
            Behavior on implicitWidth { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
            Behavior on implicitHeight { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
            Rectangle {
                anchors.centerIn: parent
                width: wsg.numbers ? Math.round(wsg.h * 0.72) : wsg.vertical ? ws.dot : parent.width
                height: wsg.numbers ? Math.round(wsg.h * 0.72) : wsg.vertical ? parent.height : ws.dot
                radius: wsg.numbers ? Math.min(8, height * 0.3) : Math.min(width, height) / 2
                color: ws.modelData.active ? Theme.accent
                     : wsg.numbers ? (ws.containsMouse ? Theme.alpha(Theme.fg, 0.14) : ws.modelData.occupied ? Theme.alpha(Theme.fg, 0.08) : "transparent")
                     : ws.modelData.occupied ? Theme.alpha(Theme.fg, 0.75) : Theme.alpha(Theme.fg, ws.containsMouse ? 0.45 : 0.25)
                Behavior on color { ColorAnimation { duration: 160 } }
                Text {
                    visible: wsg.numbers
                    anchors.centerIn: parent
                    text: ws.modelData.num
                    color: ws.modelData.active ? Theme.accentFg : ws.modelData.occupied ? Theme.fg : Theme.muted
                    font.family: Theme.font; font.bold: ws.modelData.active; font.pixelSize: Math.round(wsg.h * 0.4)
                }
            }
        }
    }
}
