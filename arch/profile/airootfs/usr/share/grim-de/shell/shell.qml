//@ pragma UseQApplication
//@ pragma IconTheme Papirus-Dark
// Grim Shell: the bar and dock of the Grim desktop (niri + Quickshell).
import QtQuick
import Quickshell
import Quickshell.Io

ShellRoot {
    id: root
    Variants { model: Quickshell.screens; Bar {} }
    // the dock gets new windows when it moves to another screen edge (layer surfaces can't change
    // edge live): the list empties for a moment, then fills again
    property bool dockRebuild: false
    property string dockPos: Theme.dockPos
    onDockPosChanged: { dockRebuild = true; dockTimer.restart() }
    Timer { id: dockTimer; interval: 120; onTriggered: dockRebuild = false }
    Variants {
        model: dockRebuild ? [] : Quickshell.screens
        Dock { required property var modelData; screenObj: modelData; pos: Theme.dockPos }
    }
    Toasts { screen: Quickshell.screens[0] }
    // qs -p /usr/share/grim-de/shell ipc call dock click firefox   (same as clicking it in the dock)
    IpcHandler { target: "dock"; function click(app: string): void { Apps.click(app) } function desktop(): void { Apps.toggleDesktop() } }
}
