#!/bin/bash
# Lays out Grim Browser under DESTDIR (a package root or /). Used by Grim Void's package and Grim OS's ISO.
#   ./install.sh DESTDIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
D=${1:?usage: install.sh DESTDIR}
FFID='{ec8030f7-c20a-464f-9b0e-13a3a9e97384}'     # Firefox's application id (system add-on folder)

install -Dm755 "$HERE/bin/grim-browser" "$D/usr/bin/grim-browser"
install -Dm755 "$HERE/bin/grim-search" "$D/usr/bin/grim-search"
install -Dm644 "$HERE/lib/user.js" "$D/usr/lib/grim-browser/user.js"
install -Dm644 "$HERE/lib/torrc" "$D/usr/lib/grim-browser/torrc"
install -Dm644 "$HERE/lib/userChrome.css" "$D/usr/lib/grim-browser/userChrome.css"
install -Dm755 "$HERE/lib/grim-browser-native" "$D/usr/lib/grim-browser/grim-browser-native"
install -Dm644 "$HERE/lib/grim_browser.json" "$D/usr/lib/mozilla/native-messaging-hosts/grim_browser.json"
install -Dm644 "$HERE/lib/policies.json" "$D/usr/lib/firefox/distribution/policies.json"
install -Dm644 "$HERE/lib/grim-browser.desktop" "$D/usr/share/applications/grim-browser.desktop"
# Grim Shield as a system add-on (Firefox is built with --with-unsigned-addon-scopes=app,system)
mkdir -p "$D/usr/lib/mozilla/extensions/$FFID"
python3 - "$HERE/extension" "$D/usr/lib/mozilla/extensions/$FFID/grim-shield@grim.os.xpi" <<'PY'
import os, sys, zipfile
src, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(src):
        for f in sorted(files):
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, src))
PY
chmod 644 "$D/usr/lib/mozilla/extensions/$FFID/grim-shield@grim.os.xpi"
for s in 16 32 48 64 128 256 512; do
    install -Dm644 "$HERE/branding/grim-browser-$s.png" "$D/usr/share/icons/hicolor/${s}x${s}/apps/grim-browser.png"
done
install -Dm644 "$HERE/branding/grim-browser.svg" "$D/usr/share/icons/hicolor/scalable/apps/grim-browser.svg"
install -Dm644 "$HERE/LICENSE-ICON" "$D/usr/share/licenses/grim-browser/LICENSE-ICON"
