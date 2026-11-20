import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications

// One notification: app icon, app name and time, title, text, action buttons, close button.
// As a pop-up (`popup: true`) it closes itself after a few seconds unless you hover it.
Rectangle {
    id: card
    required property var notif
    property bool popup: false
    readonly property bool critical: notif && notif.urgency === NotificationUrgency.Critical
    implicitHeight: lay.implicitHeight + 24
    radius: Math.min(Theme.radius + 2, 14)
    color: popup ? Theme.alpha(Theme.bg, Theme.glass ? 0.94 : 1) : Theme.alpha(Theme.fg, 0.05)
    border.width: popup || critical ? 1 : 0
    border.color: critical ? Theme.urgent : Theme.alpha(Theme.fg, 0.12)

    // image from the app, else its icon, else the icon of its desktop entry; a letter tile if none exist
    function resolve(i) {
        if (!i) return ""
        if (i.startsWith("image://icon/")) i = i.slice(13)
        if (i.startsWith("/")) return "file://" + i
        if (i.startsWith("file://") || i.startsWith("image://") || i.startsWith("http")) return i
        return Quickshell.iconPath(i, true) || Quickshell.iconPath(i.toLowerCase(), true) || ""
    }
    readonly property string iconSrc: {
        if (!notif) return ""
        const e = DesktopEntries.heuristicLookup(notif.desktopEntry || notif.appName || "")
        return resolve(notif.image) || resolve(notif.appIcon) || (e ? resolve(e.icon) : "")
    }

    Timer {
        running: card.popup && !hover.containsMouse && !card.critical
        interval: card.notif && card.notif.expireTimeout > 0 ? Math.max(2000, Math.min(15000, card.notif.expireTimeout > 100 ? card.notif.expireTimeout : card.notif.expireTimeout * 1000)) : 5500
        onTriggered: Notifs.hide(card.notif)
    }
    MouseArea {
        id: hover
        anchors.fill: parent
        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
        onClicked: Notifs.activate(card.notif)
    }

    RowLayout {
        id: lay
        anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
        spacing: 12
        Item {
            Layout.alignment: Qt.AlignTop
            implicitWidth: 36; implicitHeight: 36
            Image {
                id: icon
                anchors.fill: parent
                source: card.iconSrc
                sourceSize: Qt.size(72, 72); smooth: true; asynchronous: true
                fillMode: Image.PreserveAspectFit
                visible: status === Image.Ready
            }
            Rectangle {
                anchors.fill: parent; radius: 10
                visible: icon.status !== Image.Ready
                color: card.critical ? Theme.alpha(Theme.urgent, 0.25) : Theme.alpha(Theme.accent, 0.2)
                Text { anchors.centerIn: parent; text: card.critical ? "!" : ((card.notif && card.notif.appName) || "?").charAt(0).toUpperCase()
                       color: card.critical ? Theme.urgent : Theme.accent; font.family: Theme.font; font.bold: true; font.pixelSize: 17 }
            }
        }
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 3
            RowLayout {
                Layout.fillWidth: true
                Text { text: card.notif ? (card.notif.appName || "Notification") : ""; color: Theme.muted
                       font.family: Theme.font; font.pixelSize: Theme.fontSize; Layout.fillWidth: true; elide: Text.ElideRight }
                Text { text: { Notifs.tick; return card.notif ? Notifs.ago(card.notif) : "" } color: Theme.muted
                       font.family: Theme.font; font.pixelSize: Theme.fontSize }
                MouseArea {
                    implicitWidth: 18; implicitHeight: 18; cursorShape: Qt.PointingHandCursor
                    onClicked: Notifs.dismiss(card.notif)
                    Text { anchors.centerIn: parent; text: "✕"; color: parent.containsMouse ? Theme.fg : Theme.muted
                           font.pixelSize: Theme.fontSize + 1 }
                    hoverEnabled: true
                }
            }
            Text {
                Layout.fillWidth: true
                text: card.notif ? card.notif.summary : ""
                color: Theme.fg; font.family: Theme.font; font.bold: true; font.pixelSize: Theme.fontSize + 2
                wrapMode: Text.Wrap; maximumLineCount: 2; elide: Text.ElideRight
            }
            Text {
                Layout.fillWidth: true
                visible: text !== ""
                text: card.notif ? card.notif.body : ""
                textFormat: Text.StyledText
                color: Theme.alpha(Theme.fg, 0.85); font.family: Theme.font; font.pixelSize: Theme.fontSize + 1
                wrapMode: Text.Wrap; maximumLineCount: card.popup ? 4 : 6; elide: Text.ElideRight
                onLinkActivated: (l) => Qt.openUrlExternally(l)
            }
            Flow {
                Layout.fillWidth: true; Layout.topMargin: 4
                spacing: 6
                visible: card.notif && card.notif.actions.length > 0
                Repeater {
                    model: card.notif ? card.notif.actions.filter(a => a.identifier !== "default") : []
                    MouseArea {
                        required property var modelData
                        width: at.width + 22; height: 28
                        hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: modelData.invoke()
                        Rectangle { anchors.fill: parent; radius: 8; color: parent.containsMouse ? Theme.alpha(Theme.accent, 0.3) : Theme.alpha(Theme.fg, 0.08) }
                        Text { id: at; anchors.centerIn: parent; text: modelData.text; color: Theme.fg
                               font.family: Theme.font; font.pixelSize: Theme.fontSize + 1 }
                    }
                }
            }
        }
    }
}
