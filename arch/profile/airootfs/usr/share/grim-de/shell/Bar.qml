import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import Quickshell.Widgets
import Quickshell.Services.Pipewire
import Quickshell.Services.UPower
import Quickshell.Services.SystemTray

// The bar: launcher, workspaces, window title | clock | tray and status icons.
// Status shows icons only; click one for a small dropdown with the details.
PanelWindow {
    id: bar
    required property var modelData
    screen: modelData
    visible: Theme.bar.enabled !== false
    readonly property bool win7: Theme.bar.layout === "win7"
    readonly property bool atBottom: Theme.bar.position === "bottom" || win7
    readonly property int h: win7 ? Math.max(Theme.bar.height || 32, 40) : (Theme.bar.height || 32)
    anchors { top: !atBottom; bottom: atBottom; left: true; right: true }
    // layouts: strip (full width), floating (rounded, outlined), pills (three pills),
    // island (everything in one centred island), minimal (no background, workspace pill)
    readonly property string layout: Theme.bar.layout || "strip"
    readonly property int gap: layout === "strip" || layout === "win7" ? 0 : 6
    readonly property int side: layout === "strip" || layout === "win7" ? 0 : 8
    implicitHeight: h + gap
    exclusiveZone: h + gap
    color: "transparent"
    WlrLayershell.namespace: "grim-bar"
    Region {
        id: blurRegion
        Region { item: bar.layout === "strip" || bar.layout === "floating" || bar.win7 ? bg : null; radius: bg.radius }
        Region { item: bar.layout === "island" ? island : null; radius: island.radius }
        Region { item: bar.layout === "pills" ? pillL : null; radius: pillL.radius }
        Region { item: bar.layout === "pills" ? pillC : null; radius: pillC.radius }
        Region { item: bar.layout === "pills" ? pillR : null; radius: pillR.radius }
        Region { item: bar.layout === "minimal" ? wsPill : null; radius: wsPill.radius }
    }
    Region { id: noRegion; x: 0; y: 0; width: 1; height: 1 }   // an empty region would mean "blur everything" to niri
    BackgroundEffect.blurRegion: Theme.glass ? blurRegion : noRegion

    property string openName: ""
    onOpenNameChanged: {
        const was = _wasOpen; _wasOpen = openName !== ""
        if (_wasOpen !== was) Notifs.panelsOpen += _wasOpen ? 1 : -1
    }
    property bool _wasOpen: false
    Component.onDestruction: if (_wasOpen) Notifs.panelsOpen--
    // opened by a click: the dropdown grabs focus and closes when you click elsewhere.
    // opened from a keybind (IPC) there's no click to grab from, so it stays until toggled again
    property bool grab: true
    function toggle(n) { grab = true; openName = openName === n ? "" : n }
    // qs -p /usr/share/grim-de/shell ipc call bar toggle volume   (volume network battery clock power)
    IpcHandler { target: "updates"; function check(): void { upd.running = true } }
    IpcHandler { target: "bar"; function toggle(name: string): void { bar.grab = false; bar.openName = bar.openName === name ? "" : name } function close(): void { bar.openName = "" } }

    readonly property var sink: Pipewire.defaultAudioSink
    readonly property var source: Pipewire.defaultAudioSource
    PwObjectTracker { objects: [bar.sink, bar.source] }
    readonly property var battery: UPower.displayDevice
    SystemClock { id: clock; precision: SystemClock.Minutes }

    // ---- network, from NetworkManager
    property string netType: ""
    property string netName: ""
    property string netDev: ""
    property string netIp: ""
    property bool wifiOn: true
    Process {
        id: nm
        command: ["sh", "-c", "nmcli -t -f TYPE,STATE,CONNECTION,DEVICE device; echo ---; nmcli radio wifi"]
        stdout: StdioCollector {
            onStreamFinished: {
                const [devs, radio] = this.text.split("---")
                bar.netType = ""; bar.netName = ""; bar.netDev = ""
                for (const l of devs.split("\n")) {
                    const p = l.split(":")
                    if (p[1] === "connected" && (p[0] === "wifi" || p[0] === "ethernet")) {
                        bar.netType = p[0]; bar.netName = p[2]; bar.netDev = p[3]; break
                    }
                }
                bar.wifiOn = (radio || "").trim() !== "disabled"
                if (bar.netDev) ip.running = true; else bar.netIp = ""
            }
        }
    }
    Process {
        id: ip
        command: ["nmcli", "-g", "IP4.ADDRESS", "device", "show", bar.netDev]
        stdout: StdioCollector { onStreamFinished: bar.netIp = this.text.split("\n")[0].split("/")[0] }
    }
    Timer { interval: 10000; running: true; repeat: true; triggeredOnStart: true; onTriggered: nm.running = true }
    function refreshNet() { nm.running = true }

    // ---- updates (pacman, via checkupdates), checked 20 s after login, then every 30 minutes,
    // and again whenever grimupdate finishes (it touches ~/.cache/grimos/updated)
    property var updates: []
    property bool rebootNeeded: false
    // survives shell reloads, so the "updates ready" notice isn't sent twice
    PersistentProperties { id: keep; reloadableId: "grim-bar-updates"; property int notifiedFor: 0 }
    Process {
        id: upd
        command: ["sh", "-c", "checkupdates --nocolor 2>/dev/null; echo ---; [ -e /run/grim-reboot-needed ] && echo reboot; true"]
        stdout: StdioCollector {
            onStreamFinished: {
                const [list, rest] = this.text.split("---")
                bar.updates = list.split("\n").filter(l => l.trim() !== "")
                bar.rebootNeeded = (rest || "").indexOf("reboot") >= 0
                const n = bar.updates.length
                if (n > keep.notifiedFor && bar.modelData === Quickshell.screens[0]) {
                    Quickshell.execDetached(["notify-send", "-a", "Grim OS", "-i", "system-software-update",
                        n + (n === 1 ? " update is" : " updates are") + " ready", "Click the update icon in the bar to install."])
                }
                keep.notifiedFor = n
            }
        }
    }
    Timer { interval: 20000; running: true; onTriggered: upd.running = true }
    Timer { interval: 30 * 60000; running: true; repeat: true; onTriggered: upd.running = true }
    FileView {
        path: (Quickshell.env("XDG_CACHE_HOME") || Quickshell.env("HOME") + "/.cache") + "/grimos/updated"
        watchChanges: true
        onFileChanged: { reload(); upd.running = true }
    }

    // everything sits in `inner`: the window minus the floating gap
    Item {
        id: inner
        anchors { fill: parent; topMargin: bar.atBottom ? 0 : bar.gap; bottomMargin: bar.atBottom ? bar.gap : 0
                  leftMargin: bar.side; rightMargin: bar.side }
    }
    component Pill: Rectangle {
        parent: inner
        z: -1
        y: 0; height: inner.height
        radius: Math.min(Theme.radius + 6, height / 2)
        color: Theme.panel
        border.width: 1; border.color: Theme.alpha(Theme.fg, 0.08)
    }
    // strip and floating: one background across the whole bar
    Rectangle {
        id: bg
        parent: inner
        z: -1
        anchors.fill: parent
        visible: bar.layout === "strip" || bar.layout === "floating" || bar.win7
        color: bar.win7 ? "transparent" : Theme.panel
        radius: bar.layout === "floating" ? Math.min(Theme.radius + 4, inner.height / 2) : 0
        border.width: bar.layout === "floating" ? 1 : 0
        border.color: Theme.alpha(Theme.accent, 0.55)
        Rectangle {
            visible: bar.layout === "strip"
            anchors { left: parent.left; right: parent.right; bottom: bar.atBottom ? undefined : parent.bottom; top: bar.atBottom ? parent.top : undefined }
            height: 1; color: Theme.alpha(Theme.fg, 0.08)
        }
        // Windows 7 taskbar: dark frosted blue glass with a bright top edge
        Rectangle {
            visible: bar.win7
            anchors.fill: parent
            gradient: Gradient {
                GradientStop { position: 0; color: "#c8395a78" }
                GradientStop { position: 0.45; color: "#c8213a54" }
                GradientStop { position: 1; color: "#d8142638" }
            }
            Rectangle { anchors { left: parent.left; right: parent.right; top: parent.top } height: 1; color: "#a0bfe0ff" }
            Rectangle { anchors { left: parent.left; right: parent.right; top: parent.top; topMargin: 1 } height: 1; color: "#40ffffff" }
        }
    }
    Pill { id: island; visible: bar.layout === "island"
           x: leftGroup.x - 12; width: rightGroup.x + rightGroup.width + 10 - x }
    Pill { id: pillL; visible: bar.layout === "pills"; x: leftGroup.x - 8; width: leftGroup.width + 18 }
    Pill { id: pillC; visible: bar.layout === "pills" && clockBtn.visible; x: clockBtn.x - 4; width: clockBtn.width + 8 }
    Pill { id: pillR; visible: bar.layout === "pills"; x: rightGroup.x - 8; width: rightGroup.width + 14 }

    component Glyph: Text {
        property int code: 0
        text: Theme.glyph(code)
        font.family: Theme.mono; font.pixelSize: Math.round(bar.h * 0.56)
        color: Theme.fg
        verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter
    }
    component Label: Text {
        font.family: Theme.font; font.pixelSize: Theme.fontSize + 2
        color: Theme.fg
        verticalAlignment: Text.AlignVCenter
    }
    // an icon button in the bar; highlighted while its dropdown is open
    component IconBtn: MouseArea {
        id: ib
        property string name
        property int code
        property color tint: Theme.fg
        implicitWidth: bar.h; implicitHeight: bar.h
        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
        onClicked: bar.toggle(name)
        Rectangle {
            anchors.centerIn: parent
            width: bar.h - 6; height: bar.h - 6; radius: height / 2
            color: bar.openName === ib.name ? Theme.alpha(Theme.accent, 0.22) : ib.containsMouse ? Theme.alpha(Theme.fg, 0.08) : "transparent"
        }
        Glyph { anchors.centerIn: parent; code: ib.code; color: ib.tint }
    }
    // a row inside a dropdown
    component MenuRow: MouseArea {
        id: mr
        property string text
        property int code: 0
        property bool danger: false
        width: parent ? parent.width : 200; height: 34
        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
        Rectangle { anchors.fill: parent; radius: 8; color: mr.containsMouse ? Theme.alpha(mr.danger ? Theme.urgent : Theme.accent, 0.18) : "transparent" }
        Row {
            anchors { left: parent.left; leftMargin: 10; verticalCenter: parent.verticalCenter }
            spacing: 10
            Glyph { visible: mr.code > 0; code: mr.code; font.pixelSize: 19; width: 22; color: mr.danger ? Theme.urgent : Theme.fg }
            Label { text: mr.text; font.pixelSize: Theme.fontSize + 1 }
        }
    }
    component Heading: Label { font.bold: true; font.pixelSize: Theme.fontSize + 2 }
    component Dim: Label { color: Theme.muted; font.pixelSize: Theme.fontSize + 1 }

    // ---- left: launcher, workspaces, title
    RowLayout {
        id: leftGroup
        parent: inner
        anchors.verticalCenter: parent.verticalCenter
        x: bar.layout === "island" ? clockBtn.x - width - 22 : bar.win7 ? 4 : bar.layout === "strip" ? 10 : 12
        spacing: 10
        MouseArea {
            id: launchBtn
            implicitWidth: bar.win7 ? bar.h - 2 : bar.h - 8; implicitHeight: implicitWidth
            hoverEnabled: true; cursorShape: Qt.PointingHandCursor
            onClicked: Quickshell.execDetached(["grim-de", "launcher"])
            Rectangle {   // Windows 7 style start orb: a glowing glass ball behind the Grim logo
                visible: bar.win7
                anchors.fill: parent; radius: width / 2
                border.width: 1; border.color: launchBtn.containsMouse ? "#e0b8e6ff" : "#a07ab0d8"
                gradient: Gradient {
                    GradientStop { position: 0; color: launchBtn.containsMouse ? "#ff8fd0ff" : "#ff5f9fd6" }
                    GradientStop { position: 0.5; color: launchBtn.containsMouse ? "#ff2f86d8" : "#ff1d5c9c" }
                    GradientStop { position: 1; color: launchBtn.containsMouse ? "#ff6fd8ff" : "#ff2c7fc0" }
                }
                Rectangle { x: parent.width * 0.18; y: 2; width: parent.width * 0.64; height: parent.height * 0.42; radius: height / 2; color: "#50ffffff" }
            }
            Image {
                anchors.fill: parent; anchors.margins: bar.win7 ? 7 : 2
                source: "file://" + (Quickshell.env("GRIM_SHARE") || "/usr/share/grimos") + "/logo.svg"
                sourceSize: Qt.size(64, 64); smooth: true
            }
        }
        Item {
            visible: Theme.shows("workspaces") && !bar.win7
            implicitWidth: wsRow.width + (bar.layout === "minimal" ? 20 : 0); implicitHeight: bar.h
            Rectangle {   // minimal layout: the workspaces get their own pill
                id: wsPill
                visible: bar.layout === "minimal"
                anchors.fill: parent; anchors.topMargin: 3; anchors.bottomMargin: 3
                radius: height / 2; color: Theme.panel
                border.width: 1; border.color: Theme.alpha(Theme.fg, 0.08)
            }
            Workspaces { id: wsRow; anchors.centerIn: parent; h: bar.h }
        }
        // Windows 7 taskbar buttons
        Row {
            visible: bar.win7
            spacing: 3
            Repeater {
                model: bar.win7 ? Apps.list : []
                AppIcon { required property var modelData; appId: modelData; size: bar.h - 4; side: "bottom"; win7: true }
            }
        }
        Label {
            visible: Theme.shows("title") && text.length > 0 && !bar.win7
            text: Niri.title
            color: Theme.muted
            elide: Text.ElideRight
            Layout.maximumWidth: bar.layout === "island" ? 180 : bar.width * 0.28
        }
    }

    // ---- centre: clock (click for a calendar)
    MouseArea {
        id: clockBtn
        parent: inner
        anchors.verticalCenter: parent.verticalCenter
        // island: the clock sits in the middle of the island, which is centred on the screen
        x: bar.layout === "island"
           ? (inner.width - (leftGroup.width + width + rightGroup.width + 44)) / 2 + leftGroup.width + 22
           : (inner.width - width) / 2
        visible: (Theme.shows("clock") || Theme.shows("date")) && !bar.win7
        width: clockText.width + 20; height: bar.h
        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
        onClicked: bar.toggle("clock")
        Rectangle { anchors.centerIn: parent; width: parent.width; height: bar.h - 6; radius: height / 2
                    color: bar.openName === "clock" ? Theme.alpha(Theme.accent, 0.22) : parent.containsMouse ? Theme.alpha(Theme.fg, 0.08) : "transparent" }
        Label {
            id: clockText
            anchors.centerIn: parent
            // time and date are separate modules: show either or both
            readonly property string time: Theme.shows("clock") ? Qt.formatDateTime(clock.date, Theme.bar.clock24 === false ? "h:mm AP" : "HH:mm") : ""
            readonly property string day: Theme.shows("date") ? Qt.formatDateTime(clock.date, "ddd d MMM") : ""
            text: day && time ? day + "   " + time : day + time
            font.bold: true
            font.pixelSize: Theme.fontSize + (bar.layout === "minimal" && Theme.shows("clock") && !Theme.shows("date") ? 5 : 2)
        }
    }

    // ---- right: tray, game mode, status icons, power
    RowLayout {
        id: rightGroup
        parent: inner
        anchors.verticalCenter: parent.verticalCenter
        x: bar.layout === "island" ? clockBtn.x + clockBtn.width + 22 : inner.width - width - (bar.win7 ? 0 : bar.layout === "strip" ? 8 : 10)
        spacing: 2
        Row {
            visible: Theme.shows("tray") && SystemTray.items.values.length > 0
            spacing: 8
            Repeater {
                model: SystemTray.items
                MouseArea {
                    required property var modelData
                    width: bar.h * 0.55; height: bar.h * 0.55
                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                    onClicked: (ev) => {
                        if (ev.button === Qt.RightButton || modelData.onlyMenu) {
                            const p = mapToItem(bar.contentItem, 0, height)
                            modelData.display(bar, p.x, p.y + 4)
                        } else modelData.activate()
                    }
                    IconImage { anchors.fill: parent; source: modelData.icon }
                }
            }
        }
        Item { visible: Theme.shows("tray") && SystemTray.items.values.length > 0; implicitWidth: 10 }
        IconBtn { visible: Theme.gameMode; name: "game"; code: 0xf11b; tint: Theme.accent }
        IconBtn {
            id: updBtn
            visible: Theme.shows("updates") && (bar.updates.length > 0 || bar.rebootNeeded)
            name: "updates"
            code: bar.updates.length > 0 ? 0xf0ab : 0xf01e
            tint: Theme.accent
        }
        IconBtn {
            id: volBtn
            visible: Theme.shows("volume") && !!bar.sink
            name: "volume"
            readonly property real v: bar.sink && bar.sink.audio ? bar.sink.audio.volume : 0
            readonly property bool m: bar.sink && bar.sink.audio ? bar.sink.audio.muted : false
            code: m || v === 0 ? 0xf026 : v < 0.4 ? 0xf027 : 0xf028
            tint: m ? Theme.muted : Theme.fg
            onWheel: (w) => { if (bar.sink && bar.sink.audio) bar.sink.audio.volume = Math.max(0, Math.min(1, v + (w.angleDelta.y > 0 ? 0.05 : -0.05))) }
        }
        IconBtn {
            id: netBtn
            visible: Theme.shows("network")
            name: "network"
            code: bar.netType === "ethernet" ? 0xf0e8 : 0xf1eb
            tint: bar.netType ? Theme.fg : Theme.muted
        }
        IconBtn {
            id: batBtn
            visible: Theme.shows("battery") && !!bar.battery && bar.battery.isLaptopBattery
            name: "battery"
            readonly property real p: bar.battery ? bar.battery.percentage : 0
            readonly property bool charging: bar.battery && (bar.battery.state === UPowerDeviceState.Charging || bar.battery.state === UPowerDeviceState.FullyCharged)
            code: charging ? 0xf0e7 : p > 0.85 ? 0xf240 : p > 0.6 ? 0xf241 : p > 0.35 ? 0xf242 : p > 0.12 ? 0xf243 : 0xf244
            tint: !charging && p < 0.15 ? Theme.urgent : Theme.fg
        }
        IconBtn {
            id: bellBtn
            visible: Theme.shows("notifications")
            name: "notifications"
            code: Notifs.dnd ? 0xf1f6 : 0xf0f3
            tint: Notifs.dnd ? Theme.muted : Theme.fg
            Rectangle {   // unread dot
                visible: Notifs.unread > 0 && !Notifs.dnd
                width: 7; height: 7; radius: 4; color: Theme.accent
                x: parent.width / 2 + 4; y: parent.height / 2 - 9
            }
        }
        IconBtn { id: ccBtn; visible: Theme.shows("control"); name: "control"; code: 0xf1de }
        // Windows 7: time over date, then the "show desktop" strip
        MouseArea {
            visible: bar.win7 && (Theme.shows("clock") || Theme.shows("date"))
            implicitWidth: w7col.width + 16; implicitHeight: bar.h
            hoverEnabled: true; cursorShape: Qt.PointingHandCursor
            onClicked: bar.toggle("clock")
            Rectangle { anchors.fill: parent; anchors.margins: 2; radius: 3; color: parent.containsMouse || bar.openName === "clock" ? "#30ffffff" : "transparent" }
            Column {
                id: w7col
                anchors.centerIn: parent
                Text { anchors.horizontalCenter: parent.horizontalCenter; visible: Theme.shows("clock"); color: "#ffffff"
                       text: Qt.formatDateTime(clock.date, Theme.bar.clock24 === false ? "h:mm AP" : "HH:mm"); font.family: Theme.font; font.pixelSize: Theme.fontSize + 1 }
                Text { anchors.horizontalCenter: parent.horizontalCenter; visible: Theme.shows("date"); color: "#ffffff"
                       text: Qt.formatDateTime(clock.date, "dd/MM/yyyy"); font.family: Theme.font; font.pixelSize: Theme.fontSize + 1 }
            }
        }
        IconBtn { id: powBtn; visible: Theme.shows("power"); name: "power"; code: 0xf011; tint: Theme.urgent }
        Item {   // Windows 7: the "show desktop" strip in the corner
            visible: bar.win7
            implicitWidth: 15; implicitHeight: bar.h
            Rectangle { width: 1; height: parent.height; color: "#60bfe0ff" }
            MouseArea {
                id: showDesk
                anchors.fill: parent; hoverEnabled: true
                onClicked: Apps.toggleDesktop()
                Rectangle { anchors.fill: parent; anchors.leftMargin: 1; color: showDesk.containsMouse ? "#40ffffff" : "#14ffffff"
                            border.width: 1; border.color: "#30ffffff" }
            }
        }
    }

    // ================================================================ dropdowns
    Dropdown {
        barWindow: bar; anchorItem: volBtn; open: bar.openName === "volume"
        onRequestClose: if (bar.openName === "volume") bar.openName = ""
        Column {
            width: parent.width; spacing: 10
            RowLayout { width: parent.width
                Heading { text: "Volume"; Layout.fillWidth: true }
                Dim { text: Math.round(volBtn.v * 100) + "%" } }
            RowLayout { width: parent.width; spacing: 10
                MouseArea { implicitWidth: 22; implicitHeight: 22; cursorShape: Qt.PointingHandCursor
                    onClicked: if (bar.sink && bar.sink.audio) bar.sink.audio.muted = !volBtn.m
                    Glyph { anchors.centerIn: parent; code: volBtn.m ? 0xf026 : 0xf028; font.pixelSize: 20; color: volBtn.m ? Theme.urgent : Theme.fg } }
                GSlider { Layout.fillWidth: true; value: volBtn.v; fill: volBtn.m ? Theme.muted : Theme.accent
                    onMoved: (v) => { if (bar.sink && bar.sink.audio) { bar.sink.audio.muted = false; bar.sink.audio.volume = v } } }
            }
            RowLayout { width: parent.width; spacing: 10; visible: !!bar.source
                readonly property real mv: bar.source && bar.source.audio ? bar.source.audio.volume : 0
                readonly property bool mm: bar.source && bar.source.audio ? bar.source.audio.muted : false
                MouseArea { implicitWidth: 22; implicitHeight: 22; cursorShape: Qt.PointingHandCursor
                    onClicked: if (bar.source && bar.source.audio) bar.source.audio.muted = !parent.mm
                    Glyph { anchors.centerIn: parent; code: parent.parent.mm ? 0xf131 : 0xf130; font.pixelSize: 20; color: parent.parent.mm ? Theme.urgent : Theme.fg } }
                GSlider { Layout.fillWidth: true; value: parent.mv
                    onMoved: (v) => { if (bar.source && bar.source.audio) bar.source.audio.volume = v } }
            }
            Dim { text: "Output" }
            Repeater {
                model: Pipewire.nodes.values.filter(n => n.isSink && !n.isStream && n.audio)
                MenuRow {
                    required property var modelData
                    width: parent.width
                    text: (modelData.description || modelData.nickname || modelData.name) + (bar.sink && modelData.id === bar.sink.id ? "  ✓" : "")
                    code: 0xf025
                    onClicked: Pipewire.preferredDefaultAudioSink = modelData
                }
            }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: netBtn; open: bar.openName === "network"
        onRequestClose: if (bar.openName === "network") bar.openName = ""
        onOpenChanged: if (open) nm.running = true
        Column {
            width: parent.width; spacing: 8
            Heading { text: bar.netType === "wifi" ? "Wi-Fi" : bar.netType === "ethernet" ? "Wired" : "Not connected" }
            Dim { visible: !!bar.netName; text: bar.netName + (bar.netIp ? "   ·   " + bar.netIp : "") }
            RowLayout { width: parent.width
                Label { text: "Wi-Fi"; Layout.fillWidth: true }
                Switch { checked: bar.wifiOn
                    onToggled: { Quickshell.execDetached(["nmcli", "radio", "wifi", checked ? "on" : "off"]); bar.wifiOn = checked } } }
            MenuRow { width: parent.width; text: "Pick a Wi-Fi network…"; code: 0xf1eb
                onClicked: { bar.openName = ""; Quickshell.execDetached(["grim-de", "term", "-e", "nmtui-connect"]) } }
            MenuRow { width: parent.width; text: "Network settings"; code: 0xf013
                onClicked: { bar.openName = ""; Quickshell.execDetached(["nm-connection-editor"]) } }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: batBtn; open: bar.openName === "battery"
        onRequestClose: if (bar.openName === "battery") bar.openName = ""
        Column {
            width: parent.width; spacing: 10
            RowLayout { width: parent.width
                Heading { text: "Battery"; Layout.fillWidth: true }
                Dim { text: Math.round(batBtn.p * 100) + "%" } }
            Rectangle { width: parent.width; height: 8; radius: 4; color: Theme.alpha(Theme.fg, 0.14)
                Rectangle { width: parent.width * batBtn.p; height: parent.height; radius: 4
                            color: !batBtn.charging && batBtn.p < 0.15 ? Theme.urgent : Theme.accent } }
            Dim {
                function hm(s) { const h = Math.floor(s / 3600), m = Math.round(s % 3600 / 60); return (h ? h + " h " : "") + m + " min" }
                text: !bar.battery ? "" :
                      bar.battery.state === UPowerDeviceState.FullyCharged ? "Fully charged" :
                      bar.battery.state === UPowerDeviceState.Charging ? ("Charging" + (bar.battery.timeToFull > 0 ? ", full in " + hm(bar.battery.timeToFull) : "")) :
                      ("On battery" + (bar.battery.timeToEmpty > 0 ? ", " + hm(bar.battery.timeToEmpty) + " left" : ""))
            }
            MenuRow { width: parent.width; text: "Power settings"; code: 0xf013
                onClicked: { bar.openName = ""; Quickshell.execDetached(["grim-de-settings", "idle"]) } }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: clockBtn; open: bar.openName === "clock"; panelWidth: 290
        onRequestClose: if (bar.openName === "clock") bar.openName = ""
        Column {
            width: parent.width; spacing: 8
            Heading { text: Qt.formatDateTime(clock.date, "dddd d MMMM yyyy") }
            DayOfWeekRow {
                width: parent.width
                delegate: Dim { text: model.shortName; horizontalAlignment: Text.AlignHCenter; required property var model }
            }
            MonthGrid {
                id: grid
                width: parent.width
                month: clock.date.getMonth(); year: clock.date.getFullYear()
                delegate: Rectangle {
                    required property var model
                    implicitWidth: 34; implicitHeight: 28; radius: 8
                    color: model.today ? Theme.accent : "transparent"
                    Label { anchors.centerIn: parent; text: parent.model.day; font.pixelSize: Theme.fontSize + 1
                            color: parent.model.today ? Theme.accentFg : parent.model.month === grid.month ? Theme.fg : Theme.alpha(Theme.muted, 0.5) }
                }
            }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: powBtn; open: bar.openName === "power"; panelWidth: 220
        onRequestClose: if (bar.openName === "power") bar.openName = ""
        Column {
            width: parent.width; spacing: 2
            MenuRow { width: parent.width; text: "Lock"; code: 0xf023; onClicked: { bar.openName = ""; Quickshell.execDetached(["grim-de", "lock"]) } }
            MenuRow { width: parent.width; text: "Log out"; code: 0xf08b; onClicked: Quickshell.execDetached(["niri", "msg", "action", "quit", "--skip-confirmation"]) }
            MenuRow { width: parent.width; text: "Sleep"; code: 0xf186; onClicked: { bar.openName = ""; Quickshell.execDetached(["systemctl", "suspend"]) } }
            MenuRow { width: parent.width; text: "Restart"; code: 0xf01e; danger: true; onClicked: Quickshell.execDetached(["systemctl", "reboot"]) }
            MenuRow { width: parent.width; text: "Shut down"; code: 0xf011; danger: true; onClicked: Quickshell.execDetached(["systemctl", "poweroff"]) }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: updBtn; open: bar.openName === "updates"; panelWidth: 330
        onRequestClose: if (bar.openName === "updates") bar.openName = ""
        Column {
            width: parent.width; spacing: 8
            Heading { text: bar.updates.length ? bar.updates.length + (bar.updates.length === 1 ? " update" : " updates") + " ready" : "Up to date" }
            Repeater {
                model: bar.updates.slice(0, 8)
                Row {
                    required property string modelData
                    readonly property var f: modelData.split(" ")
                    width: parent.width; spacing: 8
                    Label { text: f[0]; width: parent.width * 0.5; elide: Text.ElideRight; font.pixelSize: Theme.fontSize + 1 }
                    Dim { text: f[3] || ""; width: parent.width * 0.5 - 8; elide: Text.ElideRight; horizontalAlignment: Text.AlignRight; font.pixelSize: Theme.fontSize }
                }
            }
            Dim { visible: bar.updates.length > 8; text: "and " + (bar.updates.length - 8) + " more" }
            Rectangle { width: parent.width; height: 1; color: Theme.alpha(Theme.fg, 0.08) }
            MenuRow { width: parent.width; visible: bar.updates.length > 0; text: "Update now"; code: 0xf0ab
                onClicked: { bar.openName = ""; Quickshell.execDetached(["grim-de", "term", "--title", "Grim update", "-e", "sh", "-c", "grimupdate; printf '\\nPress Enter to close. '; read x"]) } }
            MenuRow { width: parent.width; visible: bar.rebootNeeded; text: "Restart to finish updating"; code: 0xf01e
                onClicked: Quickshell.execDetached(["systemctl", "reboot"]) }
            MenuRow { width: parent.width; text: "Check again"; code: 0xf021; onClicked: upd.running = true }
        }
    }

    Dropdown {
        id: notifDrop
        barWindow: bar; anchorItem: bellBtn; open: bar.openName === "notifications"; panelWidth: 380
        onRequestClose: if (bar.openName === "notifications") bar.openName = ""
        onOpenChanged: if (open) Notifs.markRead()
        Column {
            width: parent.width; spacing: 10
            RowLayout {
                width: parent.width
                Heading { text: "Notifications"; Layout.fillWidth: true }
                MouseArea {
                    visible: Notifs.list.length > 0
                    implicitWidth: clr.width + 16; implicitHeight: 26; cursorShape: Qt.PointingHandCursor; hoverEnabled: true
                    onClicked: Notifs.clearAll()
                    Rectangle { anchors.fill: parent; radius: 8; color: parent.containsMouse ? Theme.alpha(Theme.fg, 0.12) : Theme.alpha(Theme.fg, 0.06) }
                    Label { id: clr; anchors.centerIn: parent; text: "Clear all"; font.pixelSize: Theme.fontSize + 1 }
                }
            }
            RowLayout {
                width: parent.width
                Glyph { code: Notifs.dnd ? 0xf1f6 : 0xf0f3; font.pixelSize: 17; Layout.preferredWidth: 22 }
                Label { text: "Do Not Disturb"; Layout.fillWidth: true }
                Switch { checked: Notifs.dnd; onToggled: Notifs.setDnd(checked) }
            }
            Rectangle { width: parent.width; height: 1; color: Theme.alpha(Theme.fg, 0.08) }
            Column {
                width: parent.width; spacing: 8
                visible: Notifs.list.length === 0
                topPadding: 14; bottomPadding: 14
                Glyph { anchors.horizontalCenter: parent.horizontalCenter; code: 0xf0f3; font.pixelSize: 30; color: Theme.alpha(Theme.muted, 0.6) }
                Dim { anchors.horizontalCenter: parent.horizontalCenter; text: "No notifications" }
            }
            ListView {
                id: nlist
                visible: Notifs.list.length > 0
                width: parent.width
                height: Math.min(contentHeight, 460)
                clip: true; spacing: 8
                boundsBehavior: Flickable.StopAtBounds
                model: Notifs.list
                delegate: NotifCard { required property var modelData; notif: modelData; width: nlist.width }
            }
        }
    }

    Dropdown {
        barWindow: bar; anchorItem: ccBtn; open: bar.openName === "control"; panelWidth: 360
        onRequestClose: if (bar.openName === "control") bar.openName = ""
        ControlCenter { bar: bar; width: parent.width; shown: bar.openName === "control" }
    }

    Dropdown {
        barWindow: bar; anchorItem: bar.contentItem; open: bar.openName === "game"; panelWidth: 240
        onRequestClose: if (bar.openName === "game") bar.openName = ""
        Column {
            width: parent.width; spacing: 6
            Heading { text: "Game mode is on" }
            Dim { width: parent.width; wrapMode: Text.WordWrap; text: "No blur, transparency or animations." }
            MenuRow { width: parent.width; text: "Turn it off"; code: 0xf11b
                onClicked: { bar.openName = ""; Quickshell.execDetached(["grim-de", "game", "off"]) } }
        }
    }
}
