#!/usr/bin/env bash
# shellcheck disable=SC2034
# Grim OS live ISO profile (based on Arch's releng profile)

iso_name="grimos"
iso_label="GRIMOS_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="Grim OS"
iso_application="Grim OS 1.1.5 Live/Install medium"
iso_version="1.1.5"
install_dir="grim"
buildmodes=('iso')
bootmodes=('bios.syslinux'
           'uefi.grub')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd' '-Xcompression-level' '15' '-b' '1M')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
  ["/usr/local/bin/griminstall"]="0:0:755"
  ["/usr/local/bin/grim-banner"]="0:0:755"
  ["/usr/local/bin/grimhelp"]="0:0:755"
  ["/usr/local/bin/grimupdate"]="0:0:755"
  ["/usr/local/bin/grimfetch"]="0:0:755"
  ["/usr/local/bin/grim-rice"]="0:0:755"
  ["/usr/local/bin/grim-settings"]="0:0:755"
  ["/usr/local/bin/grimsettings"]="0:0:755"
  ["/usr/local/bin/grim-apps"]="0:0:755"
  ["/usr/local/bin/grim-backlight"]="0:0:755"
  ["/usr/local/bin/grim-updates-count"]="0:0:755"
  ["/usr/local/bin/grim-tty-session"]="0:0:755"
  ["/usr/local/bin/grim-de"]="0:0:755"
  ["/usr/local/bin/grim-de-settings"]="0:0:755"
  ["/usr/local/bin/grim-de-session"]="0:0:755"
  ["/usr/local/bin/grim-preview"]="0:0:755"
  ["/usr/local/bin/grimfetch-config"]="0:0:755"
  ["/usr/local/bin/grimmode"]="0:0:755"
  ["/usr/share/grimos/boot/11_grim_lowram"]="0:0:755"
  ["/usr/local/bin/grim-shot"]="0:0:755"
  ["/usr/local/bin/grim-power"]="0:0:755"
  ["/usr/local/bin/grim-term"]="0:0:755"
  ["/usr/local/bin/grim-volume"]="0:0:755"
)
