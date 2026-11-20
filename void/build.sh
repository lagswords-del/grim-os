#!/bin/bash
# Builds Grim Void. Two steps:
#   ./build.sh            as your user: fetches the tools on the first run, then Grim's packages
#                         (xbps-src, rootless) + the offline repository
#   sudo ./build.sh iso   the ISO (void-mklive needs root)
# Output: out/grim-void-VERSION-x86_64-musl.iso
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
TOP=$PWD
. grim/usr/share/grim/packages.sh
VER=$GRIM_VERSION ARCH=$GRIM_ARCH MIRROR=$GRIM_MIRROR
VP=$TOP/void-packages MD=masterdir-musl BIN=$TOP/void-packages/hostdir/binpkgs
REPO=$TOP/live-repo/opt/grim/repo
export PATH=$TOP/tools/bin:$PATH
say() { printf '\e[31m::\e[0m %s\n' "$*"; }

# What the build is pinned to (the commits Grim Void 1.2.0 was built and tested with)
VOID_PACKAGES_COMMIT=be1a31c81290c44323933d2cf1ca3931dcf8f341
VOID_MKLIVE_COMMIT=92e580a90a5e806649f95b772650f03a598c9f35
XBPS_STATIC=xbps-static-latest.x86_64-musl.tar.xz
XBPS_STATIC_SHA256=603b3c55e9cabd5af79b461b929b14e1556a443c97b5714d188681c2172d9e28   # xbps 0.60.4_1

# First run: static xbps, Void's package recipes, and void-mklive with Grim's patch
stage_setup() {
    if [[ ! -x tools/bin/xbps-install ]]; then
        say "Getting static xbps"
        mkdir -p tools/xbps tools/bin
        curl -fL --progress-bar -o "tools/$XBPS_STATIC" "https://repo-default.voidlinux.org/static/$XBPS_STATIC"
        echo "$XBPS_STATIC_SHA256  tools/$XBPS_STATIC" | sha256sum -c - || {
            echo "Checksum changed: Void published a newer xbps. Check it against https://repo-default.voidlinux.org/static/sha256sums.txt and update XBPS_STATIC_SHA256."; exit 1; }
        tar -xf "tools/$XBPS_STATIC" -C tools/xbps
        for f in tools/xbps/usr/bin/*.static; do ln -sf "$TOP/$f" "tools/bin/$(basename "$f" .static)"; done
    fi
    if [[ ! -d void-packages/.git ]]; then
        say "Getting void-packages"
        git clone --filter=blob:none https://github.com/void-linux/void-packages.git void-packages
        git -C void-packages checkout -q "$VOID_PACKAGES_COMMIT"
    fi
    [[ -f void-packages/etc/conf ]] || printf 'XBPS_ALLOW_RESTRICTED=yes\nXBPS_MAKEJOBS=%s\nXBPS_CHROOT_CMD=bwrap\n' "$(nproc)" > void-packages/etc/conf
    if [[ ! -d void-packages/masterdir-musl ]]; then
        say "Setting up the musl build root"
        (cd void-packages && ./xbps-src -A "$ARCH" -m masterdir-musl binary-bootstrap)
    fi
    if [[ ! -d void-mklive/.git ]]; then
        say "Getting void-mklive and applying Grim's changes"
        git clone https://github.com/void-linux/void-mklive.git void-mklive
        git -C void-mklive checkout -q "$VOID_MKLIVE_COMMIT"
        git -C void-mklive apply "$TOP/mklive-grim.patch"
    fi
}

stage_pkgs() {
    ((EUID != 0)) || { echo "Run this step as your user (xbps-src refuses root)."; exit 1; }
    stage_setup
    say "Copying Grim's recipes into void-packages"
    for p in pkgs/*/; do p=$(basename "$p"); rm -rf "$VP/srcpkgs/$p"; cp -a "pkgs/$p" "$VP/srcpkgs/$p"; done
    ln -sfn linux-grim "$VP/srcpkgs/linux-grim-headers"; ln -sfn linux-grim "$VP/srcpkgs/linux-grim-dbg"
    mkdir -p "$VP/srcpkgs/grim-tools/files/root" "$VP/srcpkgs/grimfetch/files/src"
    cp -a grim/. "$VP/srcpkgs/grim-tools/files/root/"
    # optional Grim apps (offered in grimhelp): their files live in extras/NAME
    local x
    for x in extras/*/; do x=$(basename "$x"); mkdir -p "$VP/srcpkgs/$x/files/root"; cp -a "extras/$x/." "$VP/srcpkgs/$x/files/root/"; done
    # Grim Browser lives in shared/ (both editions use it)
    rm -rf "$VP/srcpkgs/grim-browser/files/root"; ../shared/grim-browser/install.sh "$VP/srcpkgs/grim-browser/files/root"
    cp -a ../shared/grimfetch/{Cargo.toml,Cargo.lock,src} "$VP/srcpkgs/grimfetch/files/src/" 2>/dev/null || cp -a ../shared/grimfetch/{Cargo.toml,src} "$VP/srcpkgs/grimfetch/files/src/"
    sed -i "s/^version = .*/version = \"$VER\"/" "$VP/srcpkgs/grimfetch/files/src/Cargo.toml"
    # packages built in the second build root (hostdir2) join the main local repository
    if compgen -G "$VP/hostdir2/binpkgs/*.xbps" >/dev/null; then
        mkdir -p "$BIN"; cp -n "$VP"/hostdir2/binpkgs/*.xbps "$BIN/" && XBPS_ARCH=$ARCH xbps-rindex -a "$BIN"/*.xbps >/dev/null
    fi
    cd "$VP"
    local p force
    for p in linux-grim grimfetch grim-tools grim-base dwm-grim spotify-player-grim grim-shot grim-ai grim-browser; do
        force=; [[ $p == grim-tools || $p == grimfetch || $p == grim-base || $p == grim-shot || $p == grim-ai || $p == dwm-grim || $p == grim-browser ]] && force=-f
        if [[ -z $force ]] && ls "$BIN/$p-"[0-9]*."$ARCH.xbps" >/dev/null 2>&1; then say "$p: already built"; continue; fi
        say "Building $p"
        ./xbps-src -A "$ARCH" -m "$MD" $force pkg "$p"
    done
    cd "$TOP"
    stage_repo
}

stage_repo() {
    say "Filling the offline repository (everything a USB install can need)"
    local root=$TOP/work/dlroot cache=$TOP/cache/xbps
    rm -rf "$root" "$REPO"; mkdir -p "$root/var/db/xbps/keys" "$cache" "$REPO" work
    cp -a tools/xbps/var/db/xbps/keys/. "$root/var/db/xbps/keys/"
    mapfile -t want < <(grim_offline_set | awk 'NF && !s[$0]++')
    # the exact package list, with dependencies, as an install into an empty root would need
    # (-n skips syncing, so sync first)
    XBPS_ARCH=$ARCH xbps-install -S -r "$root" -R "$BIN" -R "$MIRROR" >/dev/null
    XBPS_ARCH=$ARCH xbps-install -n -r "$root" -R "$BIN" -R "$MIRROR" "${want[@]}" > work/plan.txt
    XBPS_ARCH=$ARCH xbps-install -D -y -r "$root" -c "$cache" -R "$BIN" -R "$MIRROR" "${want[@]}" >/dev/null
    local pv n=0 f
    # plan lines: pkgver action arch repository installed-size download-size
    while read -r pv _ arch src _; do
        f="$pv.$arch.xbps"
        if [[ $src == "$BIN" ]]; then cp "$BIN/$f" "$REPO/"; else cp "$cache/$f" "$REPO/"; fi
        n=$((n + 1))
    done < <(awk '$2 == "install"' work/plan.txt)
    XBPS_ARCH=$ARCH xbps-rindex -a "$REPO"/*.xbps >/dev/null
    say "Offline repository: $n packages, $(du -sh "$REPO" | cut -f1)"
    say "Next: sudo ./build.sh iso"
}

stage_iso() {
    ((EUID == 0)) || { echo "The ISO step needs root: sudo ./build.sh iso"; exit 1; }
    [[ -f $REPO/$ARCH-repodata ]] || { echo "Run ./build.sh (as your user) first."; exit 1; }
    mkdir -p out
    local iso=$TOP/out/grim-void-$VER-x86_64-musl.iso
    rm -f "$iso"
    cd void-mklive
    say "Building $iso"
    ./mklive.sh -a "$ARCH" -b grim-base -v linux-grim \
        -r "$BIN" -c "$TOP/cache/xbps" -H "$TOP/cache/xbps-host" \
        -p "grim-tools grimfetch dialog" \
        -S "dbus polkitd NetworkManager grim-zram" \
        -I "$TOP/live-include" -I "$TOP/live-repo" \
        -T "Grim Void $VER" -C "live.autologin" \
        -o "$iso"
    chown "$(stat -c %u:%g "$TOP")" "$iso"
    say "Done: $iso ($(du -h "$iso" | cut -f1))"
}

case ${1:-pkgs} in
    pkgs) stage_pkgs ;;
    setup) stage_setup ;;
    repo) stage_repo ;;
    iso)  stage_iso ;;
    *) echo "usage: ./build.sh [setup|pkgs|repo] , then sudo ./build.sh iso"; exit 1 ;;
esac
