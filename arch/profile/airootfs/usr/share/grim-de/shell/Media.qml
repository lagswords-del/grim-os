import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Mpris

// Now playing: Spotify, a browser tab, mpv... anything that speaks MPRIS.
// Prefers whatever is playing; the dots switch between players.
Rectangle {
    id: media
    readonly property var players: Mpris.players.values
    property int pick: -1
    readonly property var p: pick >= 0 && pick < players.length ? players[pick]
                             : (players.find(x => x.isPlaying) || players.find(x => (x.identity || "").toLowerCase().indexOf("spotify") >= 0) || players[0] || null)
    visible: !!p
    implicitHeight: visible ? lay.implicitHeight + 24 : 0
    radius: Math.min(Theme.radius + 2, 14)
    color: Theme.alpha(Theme.fg, 0.06)
    clip: true

    function glyph(c) { return String.fromCodePoint(c) }
    function mmss(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0") }

    // MPRIS doesn't push the position, so ask for it every second while playing
    Timer { running: media.visible && media.p && media.p.isPlaying; interval: 1000; repeat: true
            onTriggered: media.p.positionChanged() }

    RowLayout {
        id: lay
        anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
        spacing: 12
        ClippingRectangle {
            implicitWidth: 72; implicitHeight: 72; radius: 10
            color: Theme.alpha(Theme.fg, 0.1)
            Image { anchors.fill: parent; source: media.p ? media.p.trackArtUrl : ""; fillMode: Image.PreserveAspectCrop
                    sourceSize: Qt.size(144, 144); asynchronous: true; visible: status === Image.Ready }
            Text { anchors.centerIn: parent; visible: !media.p || !media.p.trackArtUrl; text: media.glyph(0xf001)
                   font.family: Theme.mono; font.pixelSize: 28; color: Theme.muted }
        }
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            Text { Layout.fillWidth: true; text: media.p ? (media.p.trackTitle || media.p.identity) : ""; elide: Text.ElideRight
                   color: Theme.fg; font.family: Theme.font; font.bold: true; font.pixelSize: Theme.fontSize + 2 }
            Text { Layout.fillWidth: true; text: media.p ? (media.p.trackArtist || media.p.identity) : ""; elide: Text.ElideRight
                   color: Theme.muted; font.family: Theme.font; font.pixelSize: Theme.fontSize + 1 }
            // progress, click to seek
            Item {
                Layout.fillWidth: true; implicitHeight: 14
                visible: media.p && media.p.lengthSupported && media.p.length > 0
                Rectangle { id: track; anchors.verticalCenter: parent.verticalCenter; width: parent.width; height: 4; radius: 2
                            color: Theme.alpha(Theme.fg, 0.15)
                    Rectangle { height: parent.height; radius: 2; color: Theme.accent
                                width: media.p && media.p.length > 0 ? parent.width * Math.min(1, media.p.position / media.p.length) : 0 } }
                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; enabled: media.p && media.p.canSeek
                            onClicked: (m) => { media.p.position = media.p.length * m.x / width } }
            }
            RowLayout {
                Layout.fillWidth: true
                Text { visible: media.p && media.p.lengthSupported && media.p.length > 0
                       text: media.p ? media.mmss(media.p.position) + " / " + media.mmss(media.p.length) : ""
                       color: Theme.muted; font.family: Theme.font; font.pixelSize: Theme.fontSize }
                Item { Layout.fillWidth: true }
                Repeater {
                    model: [
                        { c: 0xf048, ok: media.p && media.p.canGoPrevious, act: () => media.p.previous() },
                        { c: media.p && media.p.isPlaying ? 0xf04c : 0xf04b, ok: media.p && media.p.canTogglePlaying, act: () => media.p.togglePlaying(), big: true },
                        { c: 0xf051, ok: media.p && media.p.canGoNext, act: () => media.p.next() }
                    ]
                    MouseArea {
                        required property var modelData
                        implicitWidth: modelData.big ? 34 : 28; implicitHeight: 30
                        enabled: !!modelData.ok; opacity: enabled ? 1 : 0.35
                        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: modelData.act()
                        Rectangle { anchors.centerIn: parent; width: parent.implicitWidth; height: width; radius: width / 2
                                    color: modelData.big ? Theme.accent : parent.containsMouse ? Theme.alpha(Theme.fg, 0.1) : "transparent" }
                        Text { anchors.centerIn: parent; text: media.glyph(modelData.c); font.family: Theme.mono
                               font.pixelSize: modelData.big ? 15 : 14; color: modelData.big ? Theme.accentFg : Theme.fg }
                    }
                }
            }
        }
    }
    // one dot per player when there's more than one
    Row {
        anchors { right: parent.right; top: parent.top; margins: 8 }
        spacing: 4
        visible: media.players.length > 1
        Repeater {
            model: media.players.length
            Rectangle { required property int index; width: 6; height: 6; radius: 3
                        color: media.players[index] === media.p ? Theme.accent : Theme.alpha(Theme.fg, 0.3)
                        MouseArea { anchors.fill: parent; anchors.margins: -4; onClicked: media.pick = index } }
        }
    }
}
