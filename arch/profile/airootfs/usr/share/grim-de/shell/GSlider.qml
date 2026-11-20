import QtQuick

// A plain slider in the theme's colours. value is 0..1; `moved(v)` fires while dragging.
Item {
    id: root
    property real value: 0
    property color fill: Theme.accent
    signal moved(real v)
    implicitHeight: 22
    Rectangle {
        id: track
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width; height: 6; radius: 3
        color: Theme.alpha(Theme.fg, 0.14)
        Rectangle { width: Math.max(6, track.width * Math.max(0, Math.min(1, root.value))); height: parent.height; radius: 3; color: root.fill }
    }
    Rectangle {
        x: Math.max(0, Math.min(root.width - width, track.width * root.value - width / 2))
        anchors.verticalCenter: parent.verticalCenter
        width: 16; height: 16; radius: 8
        color: Theme.fg; border.width: 2; border.color: root.fill
    }
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        function at(x) { root.moved(Math.max(0, Math.min(1, x / width))) }
        onPressed: (m) => at(m.x)
        onPositionChanged: (m) => { if (pressed) at(m.x) }
        onWheel: (w) => root.moved(Math.max(0, Math.min(1, root.value + (w.angleDelta.y > 0 ? 0.05 : -0.05))))
    }
}
