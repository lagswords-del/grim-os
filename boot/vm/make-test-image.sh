#!/bin/bash
# Make vm/grimboot-test.img: a Grim Boot disk with test ISOs on it, for booting in QEMU.
#   sudo ./make-test-image.sh [ISO...]     (no ISOs given: the Grim ISOs from ../arch/out and
#                                           ../void/out plus everything in ../test-isos)
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
((EUID == 0)) || exec sudo "$0" "$@"
IMG=grimboot-test.img
ISOS=("$@")
if ((${#ISOS[@]} == 0)); then
    shopt -s nullglob
    ISOS=(../../void/out/grim-void-1.2.2-*.iso ../../arch/out/grimos-1.1.5-*.iso ../test-isos/*.iso)
fi
need=0; for f in "${ISOS[@]}"; do need=$((need + $(stat -c %s "$f"))); done
size=$(( need / 1048576 + 1024 ))M
for l in $(losetup -j "$PWD/$IMG" -O NAME -n 2>/dev/null); do losetup -d "$l"; done
rm -f "$IMG"
../grim-boot image "$IMG" "$size"
loop=$(losetup -fP --show "$IMG")
udevadm settle; for i in 1 2 3 4 5; do [[ -b ${loop}p1 ]] && break; partx -u "$loop" 2>/dev/null; sleep 1; done
m=$(mktemp -d)
mount "${loop}p1" "$m"
mkdir -p "$m/isos"
for f in "${ISOS[@]}"; do echo ":: copying $(basename "$f")"; cp "$f" "$m/isos/"; done
sync; umount "$m"; rmdir "$m"; losetup -d "$loop"
chown "${SUDO_UID:-0}:${SUDO_GID:-0}" "$IMG"
echo ":: $IMG is ready ($size)"
