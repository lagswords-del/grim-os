#!/usr/bin/env bash
# Rebuilds every Grim OS boot-screen image from LOGO (default logo.svg). Run from branding/.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
LOGO=${1:-logo.svg}
P=../profile
T=$(mktemp -d)
BG='#f2f2f2'; INK='#0a0a0a'


rsvg-convert -w 512 "$LOGO" -o logo.png
rsvg-convert -w 170 "$LOGO" -o "$T/170.png"
rsvg-convert -w 300 "$LOGO" -o "$T/300.png"
rsvg-convert -w 240 "$LOGO" -o "$T/240.png"

# BIOS (syslinux) 640x480: logo on top, menu underneath
magick -size 640x480 "xc:$BG" "$T/170.png" -gravity north -geometry +0+24 -composite \
  -fill "$INK" -font DejaVu-Sans-Bold -pointsize 30 -gravity north -annotate +0+200 'grim os' "PNG24:$P/syslinux/splash.png"
# UEFI GRUB theme 1024x768 (ISO and installed systems)
magick -size 1024x768 "xc:$BG" "$T/300.png" -gravity north -geometry +0+60 -composite \
  -fill "$INK" -font DejaVu-Sans-Bold -pointsize 40 -gravity north -annotate +0+372 'grim os' "PNG24:$P/grub/themes/grimos/background.png"
cp "$P/grub/themes/grimos/background.png" "$P/airootfs/usr/share/grimos/grub-theme/background.png"
# Limine 1280x800: logo at the bottom, menu text at the top
magick -size 1280x800 "xc:$BG" "$T/240.png" -gravity south -geometry +0+100 -composite \
  -fill "$INK" -font DejaVu-Sans-Bold -pointsize 30 -gravity south -annotate +0+56 'grim os' "PNG24:$P/airootfs/usr/share/grimos/limine-bg.png"
cp "$P/airootfs/usr/share/grimos/limine-bg.png" limine-bg.png
cp logo.png "$LOGO" "$P/airootfs/usr/share/grimos/"
rm -rf "$T"; echo "assets rebuilt from $LOGO"
