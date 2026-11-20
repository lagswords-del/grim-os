import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland

// The dock, built from the item list in Grim DE Settings > Dock: apps, launcher, workspaces,
// window title, clock, date, separators, gaps and your own buttons, in any order, each in
// its own pill if you like. It can sit on any screen edge.
PanelWindow {
    id: dock
    property var screenObj
    screen: screenObj
    // the Windows 7 taskbar already holds the apps, so the dock steps aside for it
    visible: Theme.dock.enabled !== false && !(Theme.bar.layout === "win7" && Theme.bar.enabled !== false)
    readonly property int size: Theme.dock.size || 44
    property string pos: "bottom"
    readonly property bool vertical: pos === "left" || pos === "right"
    readonly property string layout: Theme.dock.layout || "pill"
    readonly property bool panel: layout === "panel"
    readonly property bool autohide: !!Theme.dock.autohide
    readonly property bool shown: !autohide || hot.containsMouse
    readonly property var items: (Theme.dock.items && Theme.dock.items.length) ? Theme.dock.items : [{ type: "apps" }]
    readonly property int edge: panel ? 0 : 8           // gap between the dock and the screen edge
    readonly property int room: vertical ? 190 : 64      // space for the hover names

    anchors {
        bottom: pos === "bottom" || (vertical && panel)
        top: pos === "top" || (vertical && panel)
        left: pos === "left" || (!vertical && panel)
        right: pos === "right" || (!vertical && panel)
    }
    implicitWidth: vertical ? size + room : Math.max(pill.width + 24, 120)
    implicitHeight: vertical ? Math.max(pill.height + 24, 120) : size + room
    exclusiveZone: autohide ? 0 : size + (panel ? 14 : 20)
    color: "transparent"
    WlrLayershell.namespace: "grim-dock"
    WlrLayershell.layer: WlrLayer.Top
    Region { id: pillRegion; item: pill; radius: pill.radius }
    Region { id: stripRegion; item: strip }
    Region { id: noRegion; x: 0; y: 0; width: 1; height: 1 }   // an empty region would mean "blur everything" to niri
    BackgroundEffect.blurRegion: Theme.glass && dock.shown && dock.layout !== "minimal" ? pillRegion : noRegion
    mask: dock.shown ? pillRegion : stripRegion

    // autohide: a thin strip on the screen edge wakes the dock up
    Item {
        id: strip
        x: dock.pos === "right" ? parent.width - width : 0
        y: dock.pos === "bottom" ? parent.height - height : 0
        width: dock.vertical ? 6 : parent.width; height: dock.vertical ? parent.height : 6
    }
    MouseArea { id: hot; anchors.fill: parent; hoverEnabled: true; acceptedButtons: Qt.NoButton }

    Rectangle {
        id: pill
        readonly property int along: (dock.vertical ? grid.height : grid.width) + 18
        readonly property int across: dock.size + 14
        width: dock.vertical ? across : (dock.panel ? dock.width : along)
        height: dock.vertical ? (dock.panel ? dock.height : along) : across
        x: dock.pos === "left" ? (dock.shown ? dock.edge : -width - 4)
         : dock.pos === "right" ? (dock.shown ? dock.width - width - dock.edge : dock.width + 4)
         : (dock.width - width) / 2
        y: dock.pos === "bottom" ? (dock.shown ? dock.height - height - dock.edge : dock.height + 4)
         : dock.pos === "top" ? (dock.shown ? dock.edge : -height - 4)
         : (dock.height - height) / 2
        Behavior on x { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
        Behavior on y { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
        radius: dock.panel ? 0 : Math.min(Theme.radius + 6, across / 2)
        color: dock.layout === "minimal" ? "transparent" : dock.layout === "win7" ? "transparent" : Theme.panel
        border.width: dock.layout === "outlined" ? 2 : dock.layout === "pill" ? 1 : 0
        border.color: dock.layout === "outlined" ? Theme.alpha(Theme.accent, 0.8) : Theme.alpha(Theme.fg, 0.08)
        // Windows 7 glass
        Rectangle {
            visible: dock.layout === "win7"
            anchors.fill: parent; radius: parent.radius
            border.width: 1; border.color: "#90c8e8ff"
            gradient: Gradient {
                orientation: dock.vertical ? Gradient.Horizontal : Gradient.Vertical
                GradientStop { position: 0; color: "#c03c6e96" }
                GradientStop { position: 0.5; color: "#c0213f5e" }
                GradientStop { position: 1; color: "#d0172d45" }
            }
        }
        Rectangle {   // panel: a thin line on the inner edge
            visible: dock.panel
            color: Theme.alpha(Theme.fg, 0.08)
            width: dock.vertical ? 1 : parent.width; height: dock.vertical ? parent.height : 1
            x: dock.pos === "left" ? parent.width - 1 : 0
            y: dock.pos === "top" ? parent.height - 1 : 0
        }

        // one row (or one column on the side edges); GridLayout keeps every item however many there are
        GridLayout {
            id: grid
            anchors.centerIn: parent
            flow: dock.vertical ? GridLayout.TopToBottom : GridLayout.LeftToRight
            rowSpacing: 8; columnSpacing: 8
            Repeater {
                model: dock.items
                // one item of the dock, optionally in its own pill
                Item {
                    id: di
                    required property var modelData
                    readonly property var item: modelData
                    readonly property bool ownPill: !!item.pill
                    readonly property int padAlong: ownPill ? 14 : 0
                    implicitWidth: dock.vertical ? dock.size + (ownPill ? 6 : 0) : loader.width + padAlong
                    implicitHeight: dock.vertical ? loader.height + padAlong : dock.size + (ownPill ? 6 : 0)
                    Layout.alignment: Qt.AlignCenter
                    Rectangle {
                        visible: di.ownPill
                        anchors.fill: parent
                        radius: Math.min(Theme.radius + 4, Math.min(width, height) / 2)
                        color: Theme.alpha(Theme.bg, Theme.glass ? Math.min(Theme.panelOpacity + 0.1, 0.95) : 1)
                        border.width: 1; border.color: Theme.alpha(Theme.fg, 0.1)
                    }
                    Loader {
                        id: loader
                        anchors.centerIn: parent
                        property var item: di.item
                        sourceComponent: ({ launcher: cLauncher, apps: cApps, workspaces: cWs, title: cTitle, clock: cClock,
                                            date: cDate, separator: cSep, gap: cGap, custom: cCustom })[di.item.type] || null
                    }
                }
            }
        }
    }

    Component {
        id: cLauncher
        MouseArea {
            implicitWidth: dock.size; implicitHeight: dock.size
            hoverEnabled: true; cursorShape: Qt.PointingHandCursor
            onClicked: Quickshell.execDetached(["grim-de", "launcher"])
            Image {
                anchors.centerIn: parent
                width: parent.width * (parent.containsMouse ? 0.9 : 0.78); height: width
                Behavior on width { NumberAnimation { duration: 120 } }
                source: "file://" + (Quickshell.env("GRIM_SHARE") || "/usr/share/grimos") + "/logo.svg"
                sourceSize: Qt.size(128, 128); smooth: true
            }
        }
    }
    Component {
        id: cApps
        GridLayout {
            flow: dock.vertical ? GridLayout.TopToBottom : GridLayout.LeftToRight
            rowSpacing: 8; columnSpacing: 8
            Repeater {
                model: Apps.list
                AppIcon { required property var modelData; appId: modelData; size: dock.size; side: dock.pos
                          win7: dock.layout === "win7" }
            }
        }
    }
    Component { id: cWs; Workspaces { h: Math.round(dock.size * 0.7); vertical: dock.vertical } }
    Component {
        id: cTitle
        DockText {
            visible: !dock.vertical && text !== ""
            text: Niri.title
            color: Theme.muted
            width: Math.min(implicitWidth, 260); elide: Text.ElideRight
        }
    }
    Component {
        id: cClock
        DockText {
            SystemClock { id: ck; precision: SystemClock.Minutes }
            readonly property string fmt: Theme.bar.clock24 === false ? "h:mm" : "HH:mm"
            text: dock.vertical ? Qt.formatDateTime(ck.date, fmt).replace(":", "\n") : Qt.formatDateTime(ck.date, Theme.bar.clock24 === false ? "h:mm AP" : "HH:mm")
            font.bold: true; font.pixelSize: dock.vertical ? Theme.fontSize + 3 : Theme.fontSize + 5
            lineHeight: 0.9
        }
    }
    Component {
        id: cDate
        DockText {
            SystemClock { id: cd; precision: SystemClock.Hours }
            text: dock.vertical ? Qt.formatDateTime(cd.date, "d\nMMM") : Qt.formatDateTime(cd.date, "ddd d MMM")
            color: Theme.muted
        }
    }
    Component {
        id: cSep
        Rectangle { implicitWidth: dock.vertical ? dock.size * 0.6 : 1; implicitHeight: dock.vertical ? 1 : dock.size * 0.6; color: Theme.alpha(Theme.fg, 0.2) }
    }
    Component { id: cGap; Item { implicitWidth: dock.size / 2; implicitHeight: dock.size / 2 } }
    Component {
        id: cCustom
        MouseArea {
            id: cu
            readonly property var it: parent && parent.item ? parent.item : ({})
            readonly property string src: !it.icon ? "" : it.icon.startsWith("/") ? "file://" + it.icon : Quickshell.iconPath(it.icon, true)
            implicitWidth: dock.size; implicitHeight: dock.size
            hoverEnabled: true; cursorShape: Qt.PointingHandCursor
            onClicked: if (it.command) Quickshell.execDetached(["sh", "-c", it.command])
            Image {
                id: ci
                anchors.centerIn: parent
                width: dock.size * (cu.containsMouse ? 1 : 0.86); height: width
                Behavior on width { NumberAnimation { duration: 120 } }
                source: cu.src; sourceSize: Qt.size(128, 128); smooth: true; mipmap: true
            }
            Rectangle {
                visible: ci.status !== Image.Ready
                anchors.centerIn: parent; width: dock.size * 0.78; height: width; radius: width * 0.28; color: Theme.bg3
                DockText { anchors.centerIn: parent; text: (cu.it.name || "?").charAt(0).toUpperCase(); color: Theme.accent; font.bold: true }
            }
            Rectangle {
                visible: cu.containsMouse && !!cu.it.name
                z: 10
                width: tt.width + 16; height: tt.height + 8; radius: 6
                color: Theme.alpha(Theme.bg, 0.92)
                x: dock.pos === "left" ? cu.width + 12 : dock.pos === "right" ? -width - 12 : (cu.width - width) / 2
                y: dock.pos === "bottom" ? -height - 12 : dock.pos === "top" ? cu.height + 12 : (cu.height - height) / 2
                DockText { id: tt; anchors.centerIn: parent; text: cu.it.name || ""; font.pixelSize: Theme.fontSize + 1 }
            }
        }
    }
}
