# shellcheck shell=bash
# Package sets for Grim OS 1.1.5. Sourced by griminstall (on the ISO) and by build.sh
# (to decide what goes into the offline repository). Keep both in sync here.

# Which ISO this is: "full" (every desktop offline) or "lite" (Grim DE + linux-lts only).
# build.sh sets GRIM_EDITION; on the USB it comes from /etc/grimos/edition.
GRIM_EDITION=${GRIM_EDITION:-$(cat /etc/grimos/edition 2>/dev/null || echo full)}

# Always installed
GRIM_BASE=(base mkinitcpio sudo nano vim networkmanager efibootmgr dialog pciutils
           zram-generator man-db man-pages bash-completion dosfstools e2fsprogs btrfs-progs
           intel-ucode amd-ucode reflector pacman-contrib)

# Kernel, picked in the installer. Headers go in when a driver needs building (DKMS).
GRIM_KERNELS=(linux linux-zen linux-lts linux-grim)
declare -A GRIM_KERNEL_NAME=([linux]="Linux" [linux-zen]="Linux Zen" [linux-lts]="Linux LTS" [linux-grim]="Linux Grim")
declare -A GRIM_KERNEL_DESC=(
  [linux]="the latest stable kernel, the usual choice"
  [linux-zen]="tuned for a snappy desktop and games"
  [linux-lts]="long-term support: fewer changes, most stable"
  [linux-grim]="Grim OS's own: BORE scheduler, less RAM (from the USB)")
# every kernel and its headers go into the offline repository
GRIM_KERNEL_POOL=(linux linux-headers linux-zen linux-zen-headers linux-lts linux-lts-headers)

# Bootloader, picked in the installer (Limine is UEFI only)
declare -A GRIM_BOOT_PKGS=([grub]="grub os-prober" [limine]="limine")

# Used when automatic driver detection is turned off: every firmware file
GRIM_FIRMWARE_FULL=(linux-firmware)

# Pieces automatic driver detection picks from
GRIM_DRIVER_POOL=(linux-firmware-intel linux-firmware-realtek linux-firmware-atheros
                  linux-firmware-mediatek linux-firmware-broadcom linux-firmware-marvell
                  linux-firmware-amdgpu linux-firmware-radeon linux-firmware-nvidia
                  linux-firmware-other broadcom-wl-dkms dkms linux-headers
                  vulkan-radeon vulkan-intel intel-media-driver)

# Online only: large proprietary NVIDIA driver
GRIM_NVIDIA=(nvidia-open nvidia-utils)
GRIM_NVIDIA_DKMS=(nvidia-open-dkms nvidia-utils)   # for linux-zen / linux-lts (built for that kernel)

# Added whenever any desktop or window manager is chosen
GRIM_DESKTOP_COMMON=(mesa pipewire pipewire-pulse pipewire-alsa wireplumber noto-fonts
                     ttf-dejavu xdg-user-dirs xdg-utils polkit sof-firmware
                     python python-gobject gtk4 libadwaita ttf-inconsolata-nerd papirus-icon-theme
                     rofi libnotify network-manager-applet)

# Shared pieces for the X11 window managers (bar, dock, compositor, wallpaper, screenshots)
GRIM_X11_KIT="xorg-server xorg-xinit polybar picom feh maim xclip xdotool plank dunst alacritty pacman-contrib"
# Shared pieces for the Wayland window managers
GRIM_WL_KIT="waybar mako swaybg grim slurp wl-clipboard nwg-dock"


# Added in online mode when a desktop is chosen
GRIM_ONLINE_EXTRAS=(firefox)

# Login screen for the window managers (KDE, GNOME and COSMIC bring their own)
GRIM_GREETER=(greetd greetd-tuigreet)

GRIM_DE_ORDER=(grim kde gnome cosmic xfce hyprland niri sway i3 openbox icewm)
declare -A GRIM_DE_NAME=(
  [grim]="Grim"
  [kde]="KDE Plasma" [gnome]="GNOME" [cosmic]="COSMIC" [hyprland]="Hyprland"
  [niri]="Niri" [i3]="i3" [sway]="Sway" [xfce]="XFCE" [openbox]="Openbox" [icewm]="IceWM")
declare -A GRIM_DE_DESC=(
  [grim]="the Grim desktop: niri + Grim Shell, glass and outlines"
  [kde]="full desktop, Windows-like" [gnome]="full desktop, clean and simple"
  [cosmic]="full desktop by System76" [hyprland]="tiling Wayland, animated"
  [niri]="scrolling tiling Wayland" [i3]="tiling X11, classic"
  [sway]="tiling Wayland, i3-like" [xfce]="light full desktop, classic"
  [openbox]="floating X11, minimal" [icewm]="floating X11 with taskbar, very light")
declare -A GRIM_DE_PKGS=(
  [grim]="niri quickshell xwayland-satellite xdg-desktop-portal-gnome xdg-desktop-portal-gtk swaybg swayidle swaylock libnotify bluez bluez-utils rofi alacritty brightnessctl polkit-gnome network-manager-applet nm-connection-editor thunar grim slurp wl-clipboard"
  [kde]="plasma-meta konsole dolphin"
  [gnome]="gnome gnome-shell-extension-dash-to-panel"
  [cosmic]="cosmic"
  [hyprland]="hyprland kitty hyprpolkitagent xdg-desktop-portal-hyprland nwg-dock-hyprland $GRIM_WL_KIT"
  [niri]="niri alacritty swaylock xwayland-satellite xdg-desktop-portal-gnome xdg-desktop-portal-gtk $GRIM_WL_KIT"
  [sway]="sway swaylock swayidle foot xorg-xwayland $GRIM_WL_KIT"
  [i3]="i3-wm i3lock $GRIM_X11_KIT"
  [openbox]="openbox obconf-qt $GRIM_X11_KIT"
  [icewm]="icewm $GRIM_X11_KIT"
  [xfce]="xfce4 xfce4-pulseaudio-plugin xfce4-whiskermenu-plugin xorg-server xorg-xinit plank maim xclip pacman-contrib")
# Login manager service per desktop (empty = uses greetd)
declare -A GRIM_DE_DM=([kde]=plasmalogin [gnome]=gdm [cosmic]=cosmic-greeter)

# Window managers small enough to ship on the ISO for offline installs
GRIM_OFFLINE_DES=(grim xfce hyprland niri sway i3 openbox icewm)

# Apps offered by grimhelp: key|name|source|packages
#   source: repo = official Arch repos, multilib = needs the 32-bit repo, aur = Arch User Repository
GRIM_APPS=(
  "discord|Discord|repo|discord"
  "telegram|Telegram|repo|telegram-desktop"
  "signal|Signal|repo|signal-desktop"
  "vesktop|Vesktop (Discord with Vencord)|aur|vesktop-bin"
  "steam|Steam|multilib|steam"
  "shelly|Shelly (graphical package manager)|aur|shelly-bin"
  "firefox|Firefox|repo|firefox"
  "spotify|Spotify|repo|spotify-launcher"
  "obsidian|Obsidian|repo|obsidian"
  "kitty|Kitty terminal|repo|kitty"
  "neovim|Neovim|repo|neovim"
  "prism|Prism Launcher (Minecraft)|repo|prismlauncher"
  "screenshot|Screenshot tool (PrtScreen, drag an area)|repo|maim xclip grim slurp wl-clipboard libnotify"
)

# Grim Lite: only Grim DE and linux-lts travel on the USB (other desktops install online)
if [[ $GRIM_EDITION == lite ]]; then
    GRIM_OFFLINE_DES=(grim)
    GRIM_KERNEL_POOL=(linux-lts linux-lts-headers)
    _pool=(); for _p in "${GRIM_DRIVER_POOL[@]}"; do [[ $_p == linux-headers ]] || _pool+=("$_p"); done
    GRIM_DRIVER_POOL=("${_pool[@]}"); unset _pool _p
fi
