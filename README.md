# Grim OS

A dark, red-and-black Linux distro with its own installer, tools and kernel, in two editions:

| | **Grim OS** (`arch/`) | **Grim Void** (`void/`) |
|---|---|---|
| Base | Arch Linux (archiso) | Void Linux, **musl** |
| Init | systemd | **runit** |
| Packages | pacman + AUR | xbps + Flathub + Grim's own source builds |
| Kernel | `linux-grim`: Arch's 7.3 + BORE scheduler | `linux-grim`: Void's 6.18 + BORE scheduler |
| Installer | `griminstall` (dialog menus) | `grim-install` (plain numbered questions) |
| Desktops | Grim DE (niri + Quickshell), KDE, GNOME, COSMIC, XFCE, Hyprland, niri, Sway, i3, Openbox, IceWM | IceWM, niri, Openbox, i3, dwm, river |
| Latest | 1.1.5 (+ Grim Lite 1.1.3) | 1.2.1 |

Both editions install **offline** from the USB or **online**, have a **Low RAM** boot entry (a console with nothing else running), compressed swap in RAM (zram), and share [`grimfetch`](shared/grimfetch), a system-info tool with the Grim reaper or the Grim Void ring.

## Grim Void highlights

- **`/etc/grim/system.conf`**: the whole system in one file, a bit like NixOS. Add a package line and `grimctl apply` installs it; delete it and it's removed; things you install with `xbps-install` are added to the file. Auto-updates daily or weekly.
- **`grimctl`**: `apply`, `update`, `install`, `search`, `build NAME|URL` (compile a Void recipe for your CPU, or any git project, wrapped as a real xbps package), `set KEY VALUE`, `wallpaper set FILE`, `mode lowram|desktop`, `boot lowram|desktop`.
- **`grimhelp`**: a TUI app centre (an app list, search across Void and Flathub with a "compile from source" option), Wi-Fi, wallpaper, desktop choice and help pages.
- **`grim-wifi`**: finds your Wi-Fi hardware, says when a driver or firmware is missing, lists networks by number.
- **`grim-spotify`**: Spotify in the terminal with lyrics, cover art and playlists (built on spotify-player; needs Spotify Premium).
- **Quick settings** in grimhelp: Wi-Fi, Bluetooth, volume, brightness, do-not-disturb, night light, DNS, battery charge limit, updates, zram, keyboard, time zone.
- **`grimctl disk | clean | ram | battery | net`**: disk space and health, one-command clean-up, memory and zram savings, battery health and charge limit, network info, speed test and DNS switching.
- **Grim Browser** (`shared/grim-browser`): Firefox with no telemetry or data to any company, fingerprinting protection, and the Grim Shield extension: an ad and tracker blocker (EasyList, EasyPrivacy, Peter Lowe's list), private windows routed through Tor, a one-click Burn (cookies, history, site data, new Tor identity), themes with transparency, several private search engines, a welcome animation. Plus `grim-search` for searching from a terminal or a search box. Icon: Iceraven's, recoloured (MPL-2.0).
- **Grim apps** (installed from grimhelp): **Grim Shot** for screenshots, recordings and GIFs on X11 and Wayland (Super+Shift+S), and **grim-ai**, a local AI chat with the Grim face, running llama.cpp on your PC or Ollama on another computer.
- The same keys on every desktop: Super+Enter terminal, Super+Q close, Super+F fullscreen, Super+T floating, Super+D launcher.

## Building

You need an x86_64 Linux PC with plenty of disk space (the kernels alone need ~30 GB to build). Built and tested on Arch-based systems.

**Grim OS (Arch):** needs `archiso`, `rust` (cargo) and `base-devel`.
```bash
cd arch/kernel/linux-grim && makepkg -sCf --skippgpcheck   # optional: the BORE kernel (~2 h)
cd ../.. && sudo ./build.sh                  # full ISO   (sudo ./build.sh lite  for Grim Lite)
```

**Grim Void:** needs `git`, `curl`, `bwrap` (bubblewrap) and `rsvg-convert`; everything else is fetched by the script (static xbps, void-packages and void-mklive at pinned commits, plus Grim's patch for mklive).
```bash
cd void
./build.sh            # as your user: tools, Grim's packages incl. the kernel (~2 h the first time), offline repo
sudo ./build.sh iso   # the ISO: out/grim-void-1.2.1-x86_64-musl.iso
./run-vm.sh           # try it in QEMU (UEFI)
```

## Not included yet

- **Pre-built ISOs.** The full ISOs are bigger than GitHub's 2 GB release limit; build them with the steps above.
- **Some Grim OS (Arch) artwork:** the current reaper logo (its drawing comes from SVG Repo and its licence hasn't been checked yet), the boot images made from it, and the bundled wallpapers. A fresh clone of `arch/` needs your own `arch/branding/logo.svg` and `arch/branding/make-assets.sh` run before building. Grim Void's artwork is all included.

## Layout

```
arch/      Grim OS: archiso profile, build.sh, griminstall, Grim DE, kernel PKGBUILD
void/      Grim Void: grim/ (the grim-tools files), pkgs/ (xbps-src recipes), mklive-grim.patch, build.sh
shared/    grimfetch (Rust, no dependencies)
```

## Licence

Grim's own code and artwork are under the [MIT licence](LICENSE). Parts that come from other projects keep their licences; see [NOTICE](NOTICE).
