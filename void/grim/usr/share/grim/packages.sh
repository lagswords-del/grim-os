# shellcheck shell=bash
# Grim Void 1.2.1 package sets. Read by grim-install (on the USB) and build.sh (to fill the
# USB's offline repository), so both always agree.

GRIM_VERSION=1.2.1
GRIM_ARCH=x86_64-musl
GRIM_MIRROR=https://repo-default.voidlinux.org/current/musl

# Always installed (grim-base pulls in the Void base system without a kernel, plus Grim's tools)
GRIM_BASE=(grim-base)

# Kernels
GRIM_KERNELS=(linux-grim linux6.18)
declare -A GRIM_KERNEL_DESC=(
  [linux-grim]="Void's 6.18 kernel + BORE scheduler, less RAM (recommended)"
  [linux6.18]="Void's own 6.18 kernel, unchanged")

# Bootloader pieces
GRIM_BOOT_UEFI=(grub-x86_64-efi efibootmgr)
GRIM_BOOT_BIOS=(grub)

# Hardware extras, added when the installer finds the hardware
GRIM_NVIDIA=(linux-firmware-nvidia)
GRIM_INTEL_VIDEO=(intel-video-accel mesa-vulkan-intel)
GRIM_AMD_VIDEO=(mesa-vulkan-radeon)

# Shared by every desktop
GRIM_DESKTOP_COMMON=(xorg-minimal xinit xsetroot setxkbmap xrandr mesa-dri vulkan-loader
  alacritty rofi dunst feh maim xclip font-inconsolata-otf nerd-fonts-symbols-ttf dejavu-fonts-ttf
  papirus-icon-theme adwaita-icon-theme pipewire wireplumber alsa-pipewire alsa-utils pavucontrol brightnessctl
  xdg-utils xdg-user-dirs network-manager-applet pcmanfm)
GRIM_WAYLAND_COMMON=(Waybar mako swaybg fuzzel grim slurp wl-clipboard xwayland-satellite)

GRIM_DE_ORDER=(icewm niri openbox i3 dwm river)
declare -A GRIM_DE_NAME=([icewm]="IceWM" [niri]="Niri" [openbox]="Openbox" [i3]="i3" [dwm]="dwm" [river]="river")
declare -A GRIM_DE_DESC=(
  [icewm]="light, taskbar and start menu (X11)"
  [niri]="scrolling tiling, Waybar (Wayland)"
  [openbox]="floating, right-click menu (X11)"
  [i3]="tiling with a bar (X11)"
  [dwm]="tiny tiling (X11)"
  [river]="tiling, Waybar (Wayland)")
declare -A GRIM_DE_PKGS=(
  [icewm]="icewm"
  [niri]="niri xdg-desktop-portal-gnome xdg-desktop-portal-gtk ${GRIM_WAYLAND_COMMON[*]}"
  [openbox]="openbox obconf-qt"
  [i3]="i3 i3status"
  [dwm]="dwm-grim dmenu"
  [river]="river ${GRIM_WAYLAND_COMMON[*]}")

# Shells offered by the installer
declare -A GRIM_SHELL_PKG=([bash]="" [fish]="fish-shell" [zsh]="zsh")
declare -A GRIM_SHELL_BIN=([bash]="/bin/bash" [fish]="/usr/bin/fish" [zsh]="/usr/bin/zsh")

# Everything that travels on the USB for offline installs
grim_offline_set() {
    local d
    printf '%s\n' "${GRIM_BASE[@]}" "${GRIM_KERNELS[@]}" linux-grim-headers "${GRIM_BOOT_UEFI[@]}" "${GRIM_BOOT_BIOS[@]}" \
        "${GRIM_NVIDIA[@]}" "${GRIM_INTEL_VIDEO[@]}" "${GRIM_AMD_VIDEO[@]}" "${GRIM_DESKTOP_COMMON[@]}" fish-shell zsh spotify-player-grim grim-shot grim-ai grim-browser grim-tube grim-dock
    for d in "${GRIM_DE_ORDER[@]}"; do printf '%s\n' ${GRIM_DE_PKGS[$d]}; done
}
