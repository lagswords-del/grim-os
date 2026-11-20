#!/usr/bin/env bash
# Builds the Grim OS ISO.  Run as root:
#   sudo ./build.sh          Grim OS: every desktop and kernel on the USB  -> out/grimos-VERSION-x86_64.iso
#   sudo ./build.sh lite     Grim Lite: online installer, linux-lts, small  -> out/grimos-lite-VERSION-x86_64.iso
#   1. downloads the offline package set into the profile (cached between builds)
#   2. adds Grim's own packages (linux-grim) if they've been built (kernel/linux-grim)
#   3. runs mkarchiso
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
[[ $EUID -eq 0 ]] || { echo "Run with sudo: sudo $0"; exit 1; }

EDITION=${1:-full}
[[ $EDITION == full || $EDITION == lite ]] || { echo "usage: sudo $0 [lite]"; exit 1; }
PROFILE=profile
WORK=${WORK:-/var/tmp/grimos-work}
if [[ $EDITION == lite ]]; then
    # Lite is made from a copy of the profile: linux-lts boots the USB, Grim DE is the only offline desktop
    LP=/var/tmp/grimos-lite-profile
    rm -rf "$LP"; mkdir -p "$LP"
    cp -a "$PROFILE"/. "$LP"/
    PROFILE=$LP
    WORK=/var/tmp/grimos-lite-work
    sed -i 's/^linux$/linux-lts/' "$PROFILE/packages.x86_64"
    grep -rlE 'vmlinuz-linux|initramfs-linux' "$PROFILE"/{grub,syslinux,efiboot} | while read -r f; do
        sed -i -E 's/vmlinuz-linux([^-]|$)/vmlinuz-linux-lts\1/g; s/initramfs-linux\.img/initramfs-linux-lts.img/g' "$f"
    done
    sed -i -e 's/^iso_name=.*/iso_name="grimos-lite"/' \
           -e 's/^iso_label="GRIMOS_/iso_label="GRIMLITE_/' \
           -e 's/^iso_application="Grim OS /iso_application="Grim OS Lite /' "$PROFILE/profiledef.sh"
    mkdir -p "$PROFILE/airootfs/etc/grimos"; echo lite >"$PROFILE/airootfs/etc/grimos/edition"
fi
export GRIM_EDITION=$EDITION
REPO=$PROFILE/airootfs/opt/grimos/repo
CACHE=cache/pkg
DB=cache/db

source $PROFILE/airootfs/usr/share/grimos/packages.sh
pkgs=("${GRIM_BASE[@]}" "${GRIM_KERNEL_POOL[@]}" "${GRIM_FIRMWARE_FULL[@]}" "${GRIM_DRIVER_POOL[@]}"
      "${GRIM_DESKTOP_COMMON[@]}" "${GRIM_GREETER[@]}" xorg-xinit
      ${GRIM_BOOT_PKGS[grub]} ${GRIM_BOOT_PKGS[limine]})
for de in "${GRIM_OFFLINE_DES[@]}"; do pkgs+=(${GRIM_DE_PKGS[$de]}); done

echo ":: Building grimfetch"
runuser -u "${SUDO_USER:-root}" -- env HOME="/home/${SUDO_USER}" PATH="/home/${SUDO_USER}/.cargo/bin:$PATH" \
    cargo build --release --manifest-path ../shared/grimfetch/Cargo.toml
install -Dm755 ../shared/grimfetch/target/release/grimfetch $PROFILE/airootfs/usr/local/bin/grimfetch
install -Dm644 ../shared/grimfetch/grimfetch.toml $PROFILE/airootfs/etc/grimfetch.toml

if [[ $EDITION == lite ]]; then
    echo ":: Grim Lite installs online: no offline package set"
    rm -rf "$REPO"
else
    echo ":: Downloading offline package set (${#pkgs[@]} top-level packages)"
    mkdir -p "$CACHE" "$DB"
    # A fresh, empty package database makes pacman fetch every dependency.
    pacman -Syw --noconfirm --config $PROFILE/pacman.conf --dbpath "$DB" \
           --cachedir "$CACHE" "${pkgs[@]}"

    echo ":: Building offline repository"
    rm -rf "$REPO"; mkdir -p "$REPO"
    # exactly the packages this edition needs (with dependencies), newest file of each.
    # The cache also holds packages from other editions and older builds, so it's filtered.
    pacman -Sp --noconfirm --print-format %n --config $PROFILE/pacman.conf --dbpath "$DB" "${pkgs[@]}" | sort -u >"$DB/wanted.txt"
    python3 - "$CACHE" "$REPO" "$DB/wanted.txt" <<'PY'
import os, sys, re, shutil, subprocess
cache, repo, wanted = sys.argv[1:]
want = set(open(wanted).read().split())
files = [f for f in os.listdir(cache) if f.endswith('.pkg.tar.zst')]
best = {}
def newer(a, b):
    return subprocess.run(['vercmp', a, b], capture_output=True, text=True).stdout.strip() == '1'
for f in files:
    m = re.match(r'^(.*)-([^-]+-[^-]+)-[^-]+\.pkg\.tar\.zst$', f)
    if not m: continue
    name, ver = m.groups()
    if name not in want: continue
    if name not in best or newer(ver, best[name][0]):
        best[name] = (ver, f)
for _, f in best.values():
    src, dst = os.path.join(cache, f), os.path.join(repo, f)
    try:
        os.link(src, dst)
    except OSError:          # the Lite profile sits on another filesystem
        shutil.copy2(src, dst)
missing = sorted(want - set(best))
print(f"{len(best)} packages" + (f", missing: {' '.join(missing)}" if missing else ""))
PY
    # Grim's own packages (full edition): the newest linux-grim build, if there is one
    if [[ $EDITION == full ]]; then
        shopt -s nullglob
        own=(kernel/linux-grim/linux-grim-[0-9]*.pkg.tar.zst kernel/linux-grim/linux-grim-headers-[0-9]*.pkg.tar.zst)
        if ((${#own[@]})); then
            for name in linux-grim linux-grim-headers; do
                newest=$(ls -t kernel/linux-grim/$name-[0-9]*.pkg.tar.zst 2>/dev/null | head -1)
                [[ -n $newest ]] && cp "$newest" "$REPO/" && echo "   + $(basename "$newest")"
            done
        else
            echo "   (linux-grim not built yet: the installer won't offer it)"
        fi
        shopt -u nullglob
    fi
    repo-add -q "$REPO/grimos.db.tar.gz" "$REPO"/*.pkg.tar.zst
    du -sh "$REPO"

fi

echo ":: Building ISO"
rm -rf "$WORK"
mkarchiso -v -r -w "$WORK" -o out "$PROFILE"
rm -rf "$REPO"   # it lives in the ISO now; the download cache stays for next time
[[ $EDITION == lite ]] && rm -rf "$PROFILE"
chown -R "${SUDO_UID:-0}:${SUDO_GID:-0}" out cache 2>/dev/null || true
ls -lh out/
