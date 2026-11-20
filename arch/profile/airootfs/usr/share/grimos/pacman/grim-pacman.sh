#!/bin/sh
# Grim OS pacman tweaks: colour, the Pac-Man progress bar, parallel downloads, detailed lists.
# Usage: grim-pacman.sh /path/to/pacman.conf
f=${1:-/etc/pacman.conf}
sed -i -e 's/^#\?Color$/Color/' \
       -e 's/^#\?VerbosePkgLists$/VerbosePkgLists/' \
       -e 's/^#\?ParallelDownloads.*/ParallelDownloads = 10/' "$f"
grep -q '^ParallelDownloads' "$f" || sed -i '/^\[options\]/a ParallelDownloads = 10' "$f"
grep -q '^ILoveCandy' "$f" || sed -i '/^Color$/a ILoveCandy' "$f"
