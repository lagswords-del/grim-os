"""400 ideas for Grim OS. Effort: S = an afternoon, M = a few days, L = a big project.
Format: area | effort | title | what it is"""

IDEAS = """
Installer|M|Graphical installer|A GTK version of griminstall with the same steps, for people who never touch a terminal.
Installer|M|Install alongside Windows|Shrink the Windows partition safely and install next to it, with a picture of the disk before and after.
Installer|M|Full-disk encryption|A LUKS option with one password at boot, and a warning about losing it.
Installer|S|Swap file size choice|Pick zram only, a swap file, or hibernate-ready swap.
Installer|M|Install profiles|One-click presets: Gamer, Developer, Minimal, Student, Creator. Each pre-ticks desktops and apps.
Installer|S|Live preview of rices|Pick a rice in the installer and see a screenshot before installing.
Installer|S|Hostname generator|Suggests spooky computer names like "hollow-lantern" or "crypt-07".
Installer|M|Unattended install file|Write a grim-install.conf once and install on many machines without questions.
Installer|S|Disk speed check|Warn when installing to a slow USB stick instead of an SSD.
Installer|S|Keyboard test box|Type into a box to check the layout before moving on.
Installer|M|Network installer ISO|A tiny 200 MB ISO that downloads everything, next to the full offline one.
Installer|S|Time zone map|Pick your time zone on a world map instead of a list.
Installer|M|Btrfs snapshot layout by default|Set up subvolumes ready for snapshots and rollback.
Installer|S|Install log viewer|A button to read the install log in a nice view if something fails.
Installer|S|Mirror ranking|Run reflector during install to pick the fastest mirrors for your country.
Installer|M|Resume a failed install|Pick up where it stopped instead of starting over.
Installer|S|Post-install checklist|After the first boot, show what's left: Wi-Fi, updates, apps, backups.
Installer|M|OEM mode|Install now, let the next person create the user account on first boot.
Installer|S|Hardware report|A screen listing CPU, GPU, Wi-Fi and the drivers chosen, before installing.
Installer|L|Calamares edition|An alternative ISO using Calamares for people who want the familiar installer.
Boot and login|M|Plymouth boot splash|The red reaper fades in while the system starts.
Boot and login|M|Graphical login screen|A greeter with the logo, the rice's colours and a clock.
Boot and login|S|Themed lock screen|swaylock / i3lock with the reaper and a blurred wallpaper.
Boot and login|S|Boot chime|A short, quiet bell sound when the login screen appears.
Boot and login|S|Seasonal boot splash|Pumpkins in October, snow in December.
Boot and login|M|Fast boot mode|Trim services and initramfs to boot in under 5 seconds on SSDs.
Boot and login|S|Last session memory|Remember the last desktop and user on the login screen.
Boot and login|S|Login quotes|A dark one-liner under the clock on the login screen.
Boot and login|M|Fingerprint login|Set up fprintd for laptops with a reader.
Boot and login|S|Show boot time|A notification after login saying how long boot took.
Boot and login|M|Secure Boot support|Sign the kernel and bootloader with sbctl so Grim boots with Secure Boot on.
Boot and login|S|Rescue entry|A boot menu entry that starts a repair shell with tools ready.
Boot and login|S|Bootloader theme switcher|Pick GRUB/Limine themes from Grim Settings.
Boot and login|M|Animated GRUB background|A slow fog animation behind the menu.
Boot and login|S|Auto-login option|Skip the login screen on single-user machines.
Boot and login|S|Guest session|A throwaway account that wipes itself at logout.
Boot and login|M|Face unlock|Howdy with an IR camera, opt-in.
Boot and login|S|Login wallpaper follows rice|The login screen uses the same wallpaper as the desktop.
Boot and login|M|Hibernate that works|Set up resume from swap and test it during install.
Boot and login|S|Kernel picker|Choose linux, linux-lts or linux-zen in Settings.
Desktop and rices|M|Build your 6 starred rices|Turn picks from the Rice Catalogue into real rices.
Desktop and rices|M|Rice from wallpaper|Pick a picture and get a whole palette made from it.
Desktop and rices|S|Day and night rices|Switch to the light rice at sunrise and dark at sunset.
Desktop and rices|M|Rice sharing codes|Export a rice as a short code you can paste on Discord.
Desktop and rices|M|Rice gallery app|Browse and install community rices from inside Grim Settings.
Desktop and rices|S|Random rice button|Shuffle to a random rice for fun.
Desktop and rices|M|Per-workspace wallpapers|A different wallpaper on each workspace.
Desktop and rices|S|Wallpaper slideshow|Change the wallpaper every N minutes.
Desktop and rices|M|Animated wallpapers|Video or GIF wallpapers with mpvpaper / xwinwrap, paused when a game runs.
Desktop and rices|S|Matching GTK theme|A "Grim" GTK theme generated from the rice's colours.
Desktop and rices|S|Matching cursor|A reaper-scythe cursor theme.
Desktop and rices|S|Matching icon tint|Recolour Papirus folders to the rice accent.
Desktop and rices|M|Window animations on X11|picom animations (fade, slide, pop) chosen in Settings.
Desktop and rices|S|Gap presets|None, cosy, wide, and "floating islands".
Desktop and rices|M|Desktop widgets|Clock, calendar, now playing and system stats on the desktop, like your rice.
Desktop and rices|M|Depth clock|The clock behind the subject of the wallpaper, like in your CachyOS rice.
Desktop and rices|S|Rice previews|Every rice gets a screenshot made automatically when saved.
Desktop and rices|M|Port your 11 CachyOS rices|Phantom, Gengar, Shrine, Wired and the others as Grim rices.
Desktop and rices|S|Accent from album art|Tint the accent to match what's playing.
Desktop and rices|M|Scratchpad terminal|A drop-down terminal on F12 on every window manager.
Bars, docks and widgets|M|Build your starred bars on real WMs|Test and polish the six picked bars on i3, Sway and IceWM.
Bars, docks and widgets|M|Dynamic Island for Waybar|A centre pill that grows for music, volume and notifications.
Bars, docks and widgets|S|Workspace previews|Hover a workspace to see a thumbnail.
Bars, docks and widgets|S|Weather module|Temperature and an icon from wttr.in, no account needed.
Bars, docks and widgets|S|Pomodoro module|A focus timer in the bar.
Bars, docks and widgets|S|Caffeine toggle|Stop the screen from sleeping with one click.
Bars, docks and widgets|S|Mic mute indicator|A red mic icon when the microphone is live.
Bars, docks and widgets|S|VPN indicator|Shows when a VPN is on.
Bars, docks and widgets|M|Control centre|A drop-down panel with Wi-Fi, Bluetooth, volume, brightness and toggles.
Bars, docks and widgets|M|Notification centre|History of notifications with do-not-disturb.
Bars, docks and widgets|S|Bar editor drag and drop|Reorder modules by dragging in Grim Settings.
Bars, docks and widgets|M|Glass dock|A frosted dock with magnify on hover, matching your rice dock.
Bars, docks and widgets|S|Dock running dots|Dots under open apps, in the accent colour.
Bars, docks and widgets|S|Battery health module|Shows wear level and cycles on laptops.
Bars, docks and widgets|S|Update count click|Clicking the update count opens a list of what's new.
Bars, docks and widgets|S|Clipboard history|Super+V for a list of what you copied.
Bars, docks and widgets|S|Emoji picker|Super+. for emoji and kaomoji.
Bars, docks and widgets|S|Colour picker|Pick any colour on screen and copy its hex.
Bars, docks and widgets|M|Calendar pop-up|Click the clock for a month view with events.
Bars, docks and widgets|S|Keyboard layout switcher|A small button to change layouts.
Grim apps|M|Grim App Store|A window version of grimhelp's app list with icons, screenshots and Flatpak support.
Grim apps|M|Grim Welcome|A first-login app: pick a rice, apps and check drivers in three screens.
Grim apps|M|Grim Update Center|A window for updates with a changelog and a restart button.
Grim apps|M|Grim Snapshots|Browse, create and restore system snapshots.
Grim apps|S|Grim Wi-Fi|A small frosted Wi-Fi picker for window managers.
Grim apps|S|Grim Bluetooth|Pair headphones and controllers easily.
Grim apps|M|Grim Monitor|A system monitor in the Grim style: CPU, RAM, GPU, temps, processes.
Grim apps|S|Grim Notes|A quick notes pop-up synced to a folder (works with Obsidian).
Grim apps|M|Grim Files|Thunar pre-configured with the rice and handy custom actions.
Grim apps|S|Grim Screenshot editor|Draw arrows and blur parts of a screenshot before sharing.
Grim apps|M|Grim Recorder|Screen recording with a button in the bar and a game overlay.
Grim apps|S|Grim Font Manager|Preview and install Nerd Fonts in one click.
Grim apps|M|Grim Driver Manager|Shows hardware and lets you switch GPU drivers safely.
Grim apps|S|Grim Keybind Cheat Sheet|Hold Super for two seconds to see every shortcut.
Grim apps|M|Grim Backup|Back up home to a USB drive or cloud with one button.
Grim apps|S|Grim Startup Apps|Pick what starts with the desktop.
Grim apps|S|Grim Default Apps|Choose the default browser, terminal, file manager and editor.
Grim apps|M|Grim Mouse and Touchpad|Speed, natural scrolling and tap to click for every WM.
Grim apps|S|Grim Sound|Output/input switcher with per-app volume.
Grim apps|M|Grim Printers|Set up printers without CUPS's web page.
Grim apps|S|Grim Power Menu app|A big fullscreen power menu with icons.
Grim apps|M|Grim Calendar|A simple calendar with reminders.
Grim apps|S|Grim Timer|Countdown and stopwatch with notifications.
Grim apps|L|Grim Control Panel|All Grim apps merged into one big settings window.
Grim apps|M|Grim Mochi|Your desktop pet Mochi included as an optional companion.
Terminal and shell|M|Grim prompt|A starship prompt in the rice's colours for bash, zsh and fish.
Terminal and shell|S|Shell picker|Pick bash, zsh or fish in Settings and set it up properly.
Terminal and shell|S|Better defaults|eza, bat, fd, ripgrep and zoxide installed with friendly aliases.
Terminal and shell|S|Command not found helper|Suggests which package has the missing command.
Terminal and shell|S|Typo fixer|thefuck-style fix for the last command.
Terminal and shell|S|grim command|One command for everything: grim update, grim rice, grim help, grim fetch.
Terminal and shell|S|Tab completion for grim tools|Completions for grim-rice, grimhelp and update.
Terminal and shell|S|Daily tip|A short tip about Grim OS when you open a terminal.
Terminal and shell|S|Terminal colour schemes|Every rice gets matching colours for Alacritty, kitty, foot and WezTerm.
Terminal and shell|M|Ghostty support|Theme and configure Ghostty too.
Terminal and shell|S|Man pages in colour|Coloured man pages with bat.
Terminal and shell|S|Directory jumping|Type z proj to jump to ~/Projects.
Terminal and shell|S|Pretty ls|Icons and colours in file listings.
Terminal and shell|S|Weather in terminal|grim weather shows a small forecast.
Terminal and shell|S|Cheat sheets|grim cheat tar shows the common tar commands.
Terminal and shell|M|TUI file manager|yazi set up with previews and the rice colours.
Terminal and shell|S|System info one-liner|A short status line: uptime, updates waiting, disk space.
Terminal and shell|S|Spooky MOTD|A random reaper quote at login on text consoles.
Terminal and shell|S|History search|Ctrl+R with fzf.
Terminal and shell|S|Git prompt|Branch and status in the prompt.
Terminal and shell|M|tmux preset|A ready tmux config with the rice colours and status bar.
Terminal and shell|S|Neovim starter|A themed Neovim setup ready to code.
Terminal and shell|S|Terminal transparency per rice|Each rice sets its own terminal opacity.
Terminal and shell|S|grim doctor|Checks common problems: low disk, failed services, missing firmware.
Terminal and shell|S|Sudo insults|Optional funny messages for wrong sudo passwords.
grimfetch|S|Image logo|Show the red reaper picture in kitty and foot, ASCII elsewhere.
grimfetch|S|Layouts|Side-by-side, compact, and boxed like the Nord screenshot.
grimfetch|S|Per-rice art|Each rice brings its own grimfetch art and colours.
grimfetch|S|More modules|Resolution, local IP, locale, packages by source, uptime record.
grimfetch|S|JSON output|grimfetch --json for scripts and widgets.
grimfetch|S|Random art mode|Pick a random ASCII art each time.
grimfetch|S|Speed record|Show how fast grimfetch ran (it's Rust, brag about it).
grimfetch|S|Colour themes|Presets: blood, bone, frost, toxic, ghost.
grimfetch|S|ASCII art importer|Turn any image into grimfetch art.
grimfetch|S|Small mode|A 5-line version for small terminals.
grimfetch|S|Easter egg on Halloween|The reaper wears a pumpkin on 31 October.
grimfetch|S|Uptime tombstone|"Here lies uptime: 3 days" style line.
grimfetch|S|Package from AUR|Publish grimfetch to the AUR so anyone on Arch can use it.
grimfetch|S|Screenshot mode|Hides personal info (user, host) for sharing.
grimfetch|M|Animated logo|A slow scythe swing animation when it starts.
Packages and updates|L|Grim package repository|Ship grim-rice, grimfetch and the apps as real packages so update keeps them current.
Packages and updates|M|Update notifier|A notification when updates are waiting, with what changed.
Packages and updates|M|Automatic snapshot before update|Take a btrfs snapshot before every update.
Packages and updates|S|Arch news warning|Show Arch news that needs manual action before updating.
Packages and updates|M|Package list UI|Edit packages.conf in a window, with search.
Packages and updates|S|Orphan cleaner|Remove packages nothing needs anymore.
Packages and updates|S|Cache cleaner|Keep only the last two versions of each package.
Packages and updates|M|AUR helper built in|Ship paru or yay, set up safely.
Packages and updates|S|Flatpak ready|Flathub added, with theming that matches the rice.
Packages and updates|M|Downgrade tool|Go back to an older package version from the cache.
Packages and updates|S|Changelog reader|update --changes shows what's new in each package.
Packages and updates|M|Scheduled updates|Update at night when plugged in.
Packages and updates|S|Mirror refresh timer|Rank mirrors once a week automatically.
Packages and updates|M|Package list sync between PCs|Share packages.conf across your machines.
Packages and updates|S|Install from link|Click a grim://install/discord link to install an app.
Packages and updates|S|Size warnings|Show how much space an install needs before it starts.
Packages and updates|M|Offline update bundles|Download updates on one PC, apply on another from USB.
Packages and updates|S|Explain a package|grim why package says what installed it and what needs it.
Packages and updates|M|Rollback last update|One command to undo the last update using snapshots.
Packages and updates|S|Update streak|Fun stat: days since the last update.
Gaming|M|Gaming mode|One switch for gamemode, performance governor, and pausing background jobs.
Gaming|S|Sober for Roblox|Install Sober from grimhelp with the right Flatpak setup.
Gaming|S|Amethyst launcher|Offer your Amethyst Minecraft launcher as an app.
Gaming|S|Prism Launcher preset|Java and Prism set up for Minecraft out of the box.
Gaming|M|Steam preset|Steam, Proton-GE, MangoHud and gamemode in one click.
Gaming|S|MangoHud themed|The overlay in the rice's colours.
Gaming|M|Game overlay|Your rice's game overlay: FPS, temps and clock over games.
Gaming|S|Controller support|Xbox and PlayStation controllers working with udev rules ready.
Gaming|M|Heroic and Lutris|Epic, GOG and other launchers set up.
Gaming|S|Discord + Vesktop presets|Vencord with a theme that matches the rice.
Gaming|S|Anti-cheat list|A page explaining which games work on Linux and which don't.
Gaming|M|Low-latency kernel option|linux-zen with gaming tweaks.
Gaming|S|Shader cache cleaner|Free space from old shader caches.
Gaming|M|Game library app|All your games from Steam, Heroic and Prism in one grid.
Gaming|S|FPS cap presets|Limit FPS per game to save battery.
Gaming|S|Replay buffer|Save the last 30 seconds of gameplay with a key.
Gaming|S|Emulators pack|RetroArch and friends, set up with a controller.
Gaming|M|Gaming rice|A special rice that turns off blur and animations for max FPS.
Gaming|S|Discord rich presence for Grim|Show "Using Grim OS" on Discord.
Gaming|M|Couch mode|A big-screen launcher for TVs and controllers.
Performance and power|M|Power profiles|Battery saver, balanced and performance in the bar.
Performance and power|S|zram tuning|Pick zstd or lz4 and the size in Settings.
Performance and power|S|Laptop lid behaviour|Choose what closing the lid does.
Performance and power|M|Battery charge limit|Stop charging at 80% on supported laptops.
Performance and power|S|Earlyoom|Kill runaway apps before the system freezes.
Performance and power|M|CPU scheduler choice|sched-ext schedulers for smoother desktops.
Performance and power|S|Startup time report|Show which services slow down boot.
Performance and power|S|Idle settings|Dim, lock, screen off and suspend times in Settings.
Performance and power|M|GPU switching|Pick integrated or dedicated GPU per app.
Performance and power|S|Thermal warning|A notification when the CPU runs too hot.
Performance and power|M|Optimised packages|An x86-64-v3 repo like CachyOS for newer CPUs.
Performance and power|S|Disk TRIM check|Make sure SSD trimming is on.
Performance and power|S|Background app limiter|Pause apps when on battery.
Performance and power|M|Benchmark tool|grim bench: quick CPU, disk and GPU test with a score.
Performance and power|S|RAM cleaner button|Drop caches and show freed memory (mostly for fun).
Performance and power|S|Night light|Warmer colours in the evening on every WM.
Performance and power|S|Brightness keys everywhere|Make laptop brightness keys work on all WMs.
Performance and power|S|Volume keys everywhere|Same for volume and media keys.
Performance and power|M|Low-RAM edition settings|Lighter defaults for 2-4 GB machines.
Performance and power|S|Power usage report|Which apps drain the battery most.
Security and privacy|S|Firewall on by default|ufw with a simple on/off in Settings.
Security and privacy|M|Privacy dashboard|See which apps used the camera, mic and location.
Security and privacy|S|Camera and mic kill switches|Turn them off from the bar.
Security and privacy|M|AppArmor profiles|Sandbox browsers and chat apps.
Security and privacy|S|DNS over HTTPS|Encrypted DNS with one switch.
Security and privacy|S|MAC address randomising|Random Wi-Fi MAC on public networks.
Security and privacy|M|Password manager setup|KeePassXC or Bitwarden with browser integration.
Security and privacy|S|Screen lock on suspend|Always lock before sleeping.
Security and privacy|S|USB guard|Ask before allowing new USB devices.
Security and privacy|M|Encrypted home folder|For people who skipped full-disk encryption.
Security and privacy|S|Security check|grim secure lists open ports, weak settings and missing updates.
Security and privacy|S|Telemetry-free defaults|Browser and apps set with tracking off.
Security and privacy|M|Tor browser preset|Installed and themed, with a short guide.
Security and privacy|S|Clipboard auto-clear|Wipe copied passwords after 30 seconds.
Security and privacy|S|Auto-lock when you walk away|Lock when your phone's Bluetooth goes out of range.
Security and privacy|M|VPN setup|WireGuard and OpenVPN import in Settings.
Security and privacy|S|SSH hardening|Safe defaults if you turn SSH on.
Security and privacy|S|Wipe tool|Securely erase a USB stick or file.
Security and privacy|M|Account recovery guide|What to do if you forget your password.
Security and privacy|S|Sudo timeout setting|How long sudo remembers your password.
Backup and snapshots|M|Snapper or Timeshift preset|Hourly and daily snapshots, kept tidy.
Backup and snapshots|M|Snapshots in boot menu|Boot into an old snapshot from GRUB or Limine.
Backup and snapshots|S|grim rollback|Undo the system to before the last update.
Backup and snapshots|M|Home backup to USB|Plug in a drive, it asks to back up.
Backup and snapshots|M|Cloud backup|Restic to any S3 or a friend's server.
Backup and snapshots|S|Dotfiles backup|Save your configs to a Git repo with one command.
Backup and snapshots|S|Rice backup|Every rice change is saved and can be undone.
Backup and snapshots|M|Migrate to a new PC|Move apps, settings and files to another Grim install.
Backup and snapshots|S|Backup reminders|A nudge when the last backup is old.
Backup and snapshots|S|Snapshot before rice change|Try rices safely and go back.
Backup and snapshots|M|Restore from USB|Rebuild a broken system from a backup drive.
Backup and snapshots|S|Trash that empties itself|Delete trash older than 30 days.
Backup and snapshots|S|Config history|See and restore older versions of any config file.
Backup and snapshots|M|Backup status in bar|Green when backed up, red when overdue.
Backup and snapshots|S|Export settings|Grim Settings exports everything to one file.
Networking|S|Wi-Fi QR codes|Share your Wi-Fi as a QR code, or join one by scanning.
Networking|S|Hotspot button|Share your connection from the laptop.
Networking|M|KDE Connect / GSConnect|Phone notifications and file sharing on every WM.
Networking|S|Network speed test|grim speedtest in the terminal and the bar.
Networking|S|Data usage|How much internet each app used.
Networking|M|LAN file sharing|Drop files to another Grim PC on the same network.
Networking|S|Wi-Fi strength map|Shows signal strength of nearby networks.
Networking|S|Captive portal helper|Open the login page for hotel and café Wi-Fi automatically.
Networking|M|Tailscale preset|Reach your PCs from anywhere.
Networking|S|Network troubleshooter|grim net fix resets DNS, restarts NetworkManager and tests.
Networking|S|Metered connection mode|Pause updates on phone hotspots.
Networking|M|Bluetooth audio codecs|LDAC and aptX set up for good headphone audio.
Networking|S|Airplane mode|One button to turn off all radios.
Networking|S|Proxy settings|For school and work networks.
Networking|M|Remote desktop|Help a friend by sharing your screen safely.
Accessibility and language|M|Translations|Translate the installer and Grim apps into more languages.
Accessibility and language|S|Big text mode|One switch for larger fonts everywhere.
Accessibility and language|S|High-contrast rice|A rice built for low vision.
Accessibility and language|M|Screen reader setup|Orca working on supported desktops.
Accessibility and language|S|Colour-blind friendly rices|Palettes that avoid red/green confusion.
Accessibility and language|S|Dyslexia font option|OpenDyslexic as the UI font.
Accessibility and language|S|Sticky keys and slow keys|For people who can't press combos.
Accessibility and language|S|Cursor size|Bigger cursors in Settings.
Accessibility and language|M|Voice typing|Speech to text with a local model.
Accessibility and language|S|On-screen keyboard|For touchscreens and accessibility.
Accessibility and language|S|Reduced motion|Turn off all animations at once.
Accessibility and language|M|Right-to-left support|Arabic and Hebrew layouts tested.
Accessibility and language|S|Input method setup|Japanese, Chinese and Korean typing with fcitx5.
Accessibility and language|S|Readable help pages|Help with pictures, not just text.
Accessibility and language|S|Magnifier|Zoom in on part of the screen with a shortcut.
Hardware and drivers|M|NVIDIA wizard|Pick the right NVIDIA driver for your card, with a test.
Hardware and drivers|S|Printer drivers pack|Common printer drivers ready.
Hardware and drivers|M|Hybrid GPU laptops|PRIME offload set up with a "run with dedicated GPU" menu.
Hardware and drivers|S|Touchpad gestures|Three-finger swipes for workspaces on every WM.
Hardware and drivers|M|Tablet and pen support|Drawing tablets mapped to one screen.
Hardware and drivers|S|Webcam settings|Brightness and focus controls.
Hardware and drivers|M|Laptop model fixes|A database of fixes for specific laptops (like your ThinkPad).
Hardware and drivers|S|Firmware updates|fwupd in the update command.
Hardware and drivers|S|RGB control|OpenRGB to match keyboard lights to the rice accent.
Hardware and drivers|M|Multi-monitor wizard|Arrange screens by dragging them.
Hardware and drivers|S|Hardware probe|Share your hardware report to help others.
Hardware and drivers|S|Fan curves|Quieter laptops with fan control where supported.
Hardware and drivers|S|Audio fixes|Common fixes for crackling and missing mics.
Hardware and drivers|M|Raspberry Pi / ARM edition|Grim OS for ARM boards.
Hardware and drivers|S|Keyboard backlight control|Brightness and auto-off.
Developer tools|M|Developer profile|Git, editors, compilers and Docker in one click.
Developer tools|S|VS Code themed|A Grim theme for VS Code and Codium.
Developer tools|S|Neovim theme|A Grim colourscheme for Neovim.
Developer tools|M|Container setup|Podman or Docker with a simple GUI.
Developer tools|S|Rust and Python presets|rustup and Python tools ready.
Developer tools|S|Git helper|Set name, email and SSH keys for GitHub in one go.
Developer tools|M|Distrobox|Run Ubuntu or Fedora apps inside Grim.
Developer tools|S|Database tools|PostgreSQL and SQLite with a GUI.
Developer tools|S|Web dev preset|Node, pnpm and a local HTTPS setup.
Developer tools|M|Claude Code preset|Install Claude Code and themed terminals for AI-assisted coding.
Developer tools|S|grim dev|Opens your project folder with terminal, editor and browser in a layout.
Developer tools|S|Dotfile templates|Starter configs for common tools.
Developer tools|M|Build Grim from Grim|A one-command way to build the ISO from inside Grim OS.
Developer tools|S|Game dev preset|Godot and Blender ready.
Developer tools|S|Android tools|adb and udev rules for phones.
Developer tools|M|Local AI preset|Ollama with a model picker, like your ai terminal chat.
Developer tools|S|Port checker|See what's running on which port.
Developer tools|S|JSON and log viewers|jq, lnav and friends.
Developer tools|M|Firefox extension dev kit|web-ext and a test profile, for your extension work.
Developer tools|S|Docs browser|Zeal with offline docs.
Media and creativity|S|Media codecs|All the codecs for videos and music.
Media and creativity|M|Creator profile|OBS, Kdenlive, GIMP, Krita, Audacity in one click.
Media and creativity|S|OBS themed|OBS in the rice's colours with scenes ready.
Media and creativity|S|Music player preset|A themed player with album art in the bar.
Media and creativity|S|Spotify themed|Spicetify-free Spotify colours through the rice.
Media and creativity|M|Wallpaper maker|Generate rice wallpapers from a palette.
Media and creativity|S|Photo viewer|A fast, themed image viewer.
Media and creativity|S|Screen recording to GIF|Record a region to a GIF for Discord.
Media and creativity|M|Pixel art tool|Aseprite-style editor preset.
Media and creativity|S|Audio visualiser|cava in the terminal and the bar.
Media and creativity|M|Podcast and audio setup|PipeWire filters for clean mic audio.
Media and creativity|S|Font pack|Popular free fonts for design.
Media and creativity|S|Video downloader|yt-dlp with a simple GUI.
Media and creativity|M|Live wallpaper creator|Turn a short video into a looping wallpaper.
Media and creativity|S|Colour palette extractor|Get a palette from any image.
Fun and easter eggs|S|grim reap|A command that "reaps" a frozen app with an animation.
Fun and easter eggs|S|Halloween mode|Everything turns orange for October.
Fun and easter eggs|S|Reaper pet|A tiny reaper that walks on your windows (a Mochi form).
Fun and easter eggs|S|Scythe cursor trail|Optional sparkles behind the cursor.
Fun and easter eggs|S|Uptime ghost|A ghost appears after 7 days of uptime.
Fun and easter eggs|S|Konami code|In Grim Settings, unlocks a secret rice.
Fun and easter eggs|S|Terminal games|A pack: tetris, snake, minesweeper, your maze game.
Fun and easter eggs|S|Fortune with reaper quotes|fortune but with grim jokes.
Fun and easter eggs|S|Boot fortune|A random dark joke on the boot screen.
Fun and easter eggs|S|Achievement system|Badges for first update, first rice, 100 days uptime.
Fun and easter eggs|S|Sound pack|Spooky notification sounds (optional).
Fun and easter eggs|S|Matrix screensaver|cmatrix as the screensaver in the Matrix rice.
Fun and easter eggs|S|Pipes screensaver|The classic pipes in the rice colours.
Fun and easter eggs|S|Friday the 13th theme|A one-day special rice.
Fun and easter eggs|S|Hidden grimfetch arts|Secret art on certain dates.
Fun and easter eggs|S|Lucky update|Rare chance of a "the reaper smiles upon you" message.
Fun and easter eggs|S|Desktop graveyard|Deleted files appear as tiny tombstones on the desktop.
Fun and easter eggs|S|Typing ghost|A ghost follows your typing speed in the bar.
Fun and easter eggs|S|Spooky wallpaper pack|A free pack of dark wallpapers.
Fun and easter eggs|S|Secret about page|Click the logo 13 times.
Community and website|M|Grim OS website|A homepage with downloads, screenshots and docs.
Community and website|M|Docs site|A wiki of how-tos, built from the help pages.
Community and website|S|Discord server|A place for users to share rices and get help.
Community and website|S|Rice of the week|Feature a community rice on the website.
Community and website|M|Forum|For longer questions and guides.
Community and website|S|Download mirrors|Host the ISO on several mirrors and SourceForge.
Community and website|S|Checksums and signatures|SHA256 and a GPG signature for every ISO.
Community and website|S|Release notes|A proper page for each version (1.0.3 and up).
Community and website|S|Screenshot contest|Monthly contest for the best rice.
Community and website|M|Bug tracker|GitHub issues with templates.
Community and website|S|Roadmap page|Public plans for the next versions.
Community and website|S|Sticker and wallpaper kit|Logo files for fans.
Community and website|M|DistroWatch listing|Get Grim OS listed.
Community and website|S|YouTube showcase|A short video tour of Grim OS.
Community and website|S|Contributor guide|How to help: rices, translations, code.
Branding and sound|S|Startup sound|A short dark chime.
Branding and sound|S|Notification sounds|A matching sound set.
Branding and sound|S|Logo variants|Monochrome, outline and small-size versions.
Branding and sound|S|Mascot|A friendly cartoon reaper for the website and errors.
Branding and sound|S|Error page art|The reaper looking confused when something fails.
Branding and sound|M|Official wallpaper pack|10 high-quality Grim wallpapers.
Branding and sound|S|Font for branding|Pick a display font for the logo text.
Branding and sound|S|Brand guide|Colours, logo rules and tone of voice.
Branding and sound|S|ASCII art pack|More ASCII reapers for grimfetch.
Branding and sound|S|Version codenames|1.1 "Lantern", 1.2 "Hollow", 1.3 "Ashes".
Branding and sound|S|Boot logo per version|A small change to the logo for each release.
Branding and sound|S|Merch mockups|Hoodie and sticker designs.
Branding and sound|S|Icon for the ISO|A custom icon when the ISO sits in a file manager.
Branding and sound|S|Loading animation|A spinning scythe for Grim apps.
Branding and sound|S|Tagline|A short line like "Arch, but grim."
Infrastructure|M|Move project to ~/Projects/grimos|Get it out of the temporary session folder and into Git.
Infrastructure|M|GitHub repo|Put the build files, apps and rices in a repo.
Infrastructure|M|Automatic ISO builds|GitHub Actions builds the ISO for every release.
Infrastructure|S|Version bump script|One command to change the version everywhere.
Infrastructure|M|Automated VM tests|Boot the ISO in QEMU and run an install test on every build.
Infrastructure|M|Package grim tools|PKGBUILDs for grim-rice, grimfetch, grimhelp and the apps.
Infrastructure|M|Signed package repo|Host the Grim repo with a signing key.
Infrastructure|S|Smaller ISO|Trim the offline repo with zstd-19 and drop duplicate firmware.
Infrastructure|S|Build cache cleanup|Remove old package versions from the cache automatically.
Infrastructure|S|Shellcheck and lint|Check all scripts on every build.
Infrastructure|M|Screenshot tests|Render each rice in a VM and compare screenshots.
Infrastructure|S|Changelog generator|Make release notes from commits.
Infrastructure|M|Telemetry-free crash reports|Opt-in reports that include the install log.
Infrastructure|S|ISO size report|Show what takes the most space in each build.
Infrastructure|M|Rolling vs stable branches|A stable ISO that lags Arch by a week for testing.
Infrastructure|S|Mirror for the offline repo|Reuse downloads between builds smartly.
Infrastructure|M|Multi-arch builds|Build x86-64-v3 optimised ISOs too.
Infrastructure|S|Release checklist|Steps to follow before each release.
Infrastructure|S|Build in Docker|Build the ISO without installing archiso on the host.
Infrastructure|M|Update channel for Grim tools|Ship fixes to installed systems between ISOs.
Editions|M|Grim Gaming Edition|Steam, Sober, Prism and gamemode preinstalled.
Editions|M|Grim Lite|For old PCs: IceWM or Openbox only, under 1 GB RAM.
Editions|M|Grim Dev Edition|Developer tools and Neovim ready.
Editions|M|Grim Creator Edition|OBS, Kdenlive, Krita, GIMP preinstalled.
Editions|S|Grim Bone (light edition)|Bone rice and light themes by default.
Editions|M|Grim Server|No desktop, hardened SSH, web dashboard.
Editions|M|Grim Rescue|A small ISO only for repairing systems and recovering files.
Editions|L|Grim Immutable|An atomic, image-based edition with easy rollback.
Editions|M|Grim Kids|Simple desktop, parental controls, fun rices.
Editions|L|Grim Handheld|For Steam Deck-like devices, controller-first.
"""

AREAS = []
def parse():
    out = []
    for i, line in enumerate(l for l in IDEAS.strip().splitlines() if l.strip()):
        area, effort, title, desc = line.split("|")
        assert effort in "SML", line
        out.append(dict(n=i + 1, area=area, effort=effort, title=title, desc=desc))
    return out

if __name__ == "__main__":
    import collections
    ideas = parse()
    titles = [x["title"] for x in ideas]
    dup = [t for t, c in collections.Counter(titles).items() if c > 1]
    print(len(ideas), "ideas;", dict(collections.Counter(x["area"] for x in ideas)), "dups:", dup)
