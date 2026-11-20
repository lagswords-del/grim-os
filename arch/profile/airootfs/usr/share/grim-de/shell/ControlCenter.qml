import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import Quickshell.Bluetooth

// The control center: quick toggles, volume and brightness, what's playing, shortcuts.
ColumnLayout {
    id: cc
    required property var bar          // the bar it hangs from (network state, audio, dropdowns)
    property bool shown: false
    spacing: 12
    function glyph(c) { return String.fromCodePoint(c) }

    // ---- brightness (laptops and other screens with a backlight)
    property real bright: -1
    Process {
        id: readBright
        command: ["brightnessctl", "-m", "-c", "backlight", "info"]
        stdout: StdioCollector { onStreamFinished: { const p = this.text.split(","); cc.bright = p.length > 3 ? parseInt(p[3]) / 100 : -1 } }
    }
    onShownChanged: if (shown) { readBright.running = true; cc.bar.refreshNet() }
    Timer { id: setBright; interval: 60; property real v: 0
            onTriggered: Quickshell.execDetached(["brightnessctl", "-q", "-c", "backlight", "set", Math.max(1, Math.round(v * 100)) + "%"]) }

    readonly property var adapter: Bluetooth.defaultAdapter
    readonly property var btConnected: Bluetooth.devices.values.filter(d => d.connected)

    component Tile: MouseArea {
        id: tile
        property int code
        property string title
        property string sub
        property bool on: false
        property bool hasMore: false
        signal more()
        Layout.fillWidth: true; implicitHeight: 58
        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
        Rectangle {
            anchors.fill: parent; radius: Math.min(Theme.radius + 2, 14)
            color: tile.on ? Theme.accent : tile.containsMouse ? Theme.alpha(Theme.fg, 0.12) : Theme.alpha(Theme.fg, 0.07)
            Behavior on color { ColorAnimation { duration: 120 } }
        }
        RowLayout {
            anchors { fill: parent; leftMargin: 14; rightMargin: 6 }
            spacing: 10
            Text { text: cc.glyph(tile.code); font.family: Theme.mono; font.pixelSize: 19
                   color: tile.on ? Theme.accentFg : Theme.fg; Layout.preferredWidth: 22; horizontalAlignment: Text.AlignHCenter }
            ColumnLayout {
                Layout.fillWidth: true; spacing: 0
                Text { text: tile.title; font.family: Theme.font; font.bold: true; font.pixelSize: Theme.fontSize + 1
                       color: tile.on ? Theme.accentFg : Theme.fg; Layout.fillWidth: true; elide: Text.ElideRight }
                Text { text: tile.sub; visible: text !== ""; font.family: Theme.font; font.pixelSize: Theme.fontSize
                       color: tile.on ? Theme.alpha(Theme.accentFg, 0.75) : Theme.muted; Layout.fillWidth: true; elide: Text.ElideRight }
            }
            MouseArea {
                visible: tile.hasMore
                implicitWidth: 24; Layout.fillHeight: true; cursorShape: Qt.PointingHandCursor
                onClicked: tile.more()
                Text { anchors.centerIn: parent; text: "›"; font.pixelSize: 22; color: tile.on ? Theme.accentFg : Theme.muted }
            }
        }
    }
    component SliderRow: RowLayout {
        id: sr
        property int code
        property real value
        property bool dim: false
        signal moved(real v)
        signal iconClicked()
        Layout.fillWidth: true; spacing: 12
        MouseArea {
            implicitWidth: 24; implicitHeight: 24; cursorShape: Qt.PointingHandCursor
            onClicked: sr.iconClicked()
            Text { anchors.centerIn: parent; text: cc.glyph(sr.code); font.family: Theme.mono; font.pixelSize: 18
                   color: sr.dim ? Theme.muted : Theme.fg }
        }
        GSlider { Layout.fillWidth: true; value: sr.value; fill: sr.dim ? Theme.muted : Theme.accent; onMoved: (v) => sr.moved(v) }
        Text { text: Math.round(sr.value * 100); color: Theme.muted; font.family: Theme.font; font.pixelSize: Theme.fontSize
               Layout.preferredWidth: 26; horizontalAlignment: Text.AlignRight }
    }

    GridLayout {
        Layout.fillWidth: true
        columns: 2; columnSpacing: 8; rowSpacing: 8
        Tile {
            code: 0xf1eb; title: "Wi-Fi"; on: cc.bar.wifiOn
            sub: !cc.bar.wifiOn ? "Off" : cc.bar.netType === "wifi" ? cc.bar.netName : cc.bar.netType === "ethernet" ? "Wired" : "Not connected"
            hasMore: true
            onClicked: { Quickshell.execDetached(["nmcli", "radio", "wifi", on ? "off" : "on"]); cc.bar.wifiOn = !on }
            onMore: cc.bar.openName = "network"
        }
        Tile {
            code: 0xf293; title: "Bluetooth"
            on: !!cc.adapter && cc.adapter.enabled
            sub: !cc.adapter ? "No adapter" : !cc.adapter.enabled ? "Off" : cc.btConnected.length ? cc.btConnected.map(d => d.name).join(", ") : "On"
            opacity: cc.adapter ? 1 : 0.5
            hasMore: !!cc.adapter
            onClicked: if (cc.adapter) cc.adapter.enabled = !cc.adapter.enabled
            onMore: { cc.bar.openName = ""; Quickshell.execDetached(["grim-de", "term", "-e", "bluetoothctl"]) }
        }
        Tile {
            code: Notifs.dnd ? 0xf1f6 : 0xf0f3; title: "Do Not Disturb"; on: Notifs.dnd
            sub: Notifs.dnd ? "Pop-ups hidden" : "Off"
            onClicked: Notifs.setDnd(!Notifs.dnd)
        }
        Tile {
            code: 0xf11b; title: "Game mode"; on: Theme.gameMode
            sub: Theme.gameMode ? "No blur or effects" : "Off"
            onClicked: Quickshell.execDetached(["grim-de", "game", Theme.gameMode ? "off" : "on"])
        }
    }

    SliderRow {
        visible: !!cc.bar.sink
        readonly property bool muted: cc.bar.sink && cc.bar.sink.audio ? cc.bar.sink.audio.muted : false
        code: muted ? 0xf026 : 0xf028
        dim: muted
        value: cc.bar.sink && cc.bar.sink.audio ? cc.bar.sink.audio.volume : 0
        onMoved: (v) => { if (cc.bar.sink && cc.bar.sink.audio) { cc.bar.sink.audio.muted = false; cc.bar.sink.audio.volume = v } }
        onIconClicked: if (cc.bar.sink && cc.bar.sink.audio) cc.bar.sink.audio.muted = !muted
    }
    SliderRow {
        visible: cc.bright >= 0
        code: 0xf185
        value: Math.max(0, cc.bright)
        onMoved: (v) => { cc.bright = v; setBright.v = v; setBright.restart() }
    }

    Media { Layout.fillWidth: true }

    RowLayout {
        Layout.fillWidth: true
        spacing: 6
        Repeater {
            model: [
                { c: 0xf013, tip: "Settings", act: () => Quickshell.execDetached(["grim-de-settings"]) },
                { c: 0xf030, tip: "Screenshot", act: () => Quickshell.execDetached(["sh", "-c", "sleep 0.3; grim-shot"]) },
                { c: 0xf023, tip: "Lock", act: () => Quickshell.execDetached(["grim-de", "lock"]) },
                { c: 0xf011, tip: "Power", act: () => { cc.bar.openName = "power"; return } }
            ]
            MouseArea {
                required property var modelData
                Layout.fillWidth: true; implicitHeight: 38
                hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                onClicked: { if (modelData.tip !== "Power") cc.bar.openName = ""; modelData.act() }
                Rectangle { anchors.fill: parent; radius: 10; color: parent.containsMouse ? Theme.alpha(Theme.fg, 0.12) : Theme.alpha(Theme.fg, 0.06) }
                Text { anchors.centerIn: parent; text: cc.glyph(modelData.c); font.family: Theme.mono; font.pixelSize: 17
                       color: modelData.tip === "Power" ? Theme.urgent : Theme.fg }
                ToolTipish { text: modelData.tip; show: parent.containsMouse }
            }
        }
    }
    component ToolTipish: Rectangle {
        property string text
        property bool show
        visible: show
        anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.top; bottomMargin: 4 }
        width: tt.width + 12; height: tt.height + 6; radius: 6; color: Theme.alpha(Theme.bg, 0.95)
        Text { id: tt; anchors.centerIn: parent; text: parent.text; color: Theme.fg; font.family: Theme.font; font.pixelSize: Theme.fontSize }
    }
}
