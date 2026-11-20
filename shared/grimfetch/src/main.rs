//! grimfetch: Grim OS system info. ASCII art on the left, red titles on the right.
//! Config: ~/.config/grimfetch/config.toml, then /etc/grimfetch.toml.

use std::env;
use std::ffi::CString;
use std::fs;
use std::os::raw::{c_char, c_int};
use std::path::{Path, PathBuf};

const VERSION: &str = env!("CARGO_PKG_VERSION");

// ---------------------------------------------------------------- config
struct Config {
    title_color: String,
    ascii_color: String,
    text_color: String,
    ascii: String,
    logo: String,               // a named logo from /usr/share/grim(os)/logos, overrides `ascii`
    ascii_colors: Vec<String>,  // colours for ${c1}..${c9} markers inside the art
    gap: usize,
    show_title: bool,
    show_colors: bool,
    modules: Vec<String>,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            title_color: "red".into(),
            ascii_color: "white".into(),
            text_color: "default".into(),
            ascii: "/usr/share/grimos/ascii.txt".into(),
            logo: String::new(),
            ascii_colors: Vec::new(),
            gap: 3,
            show_title: true,
            show_colors: true,
            modules: ["os", "host", "kernel", "uptime", "packages", "shell", "desktop", "rice", "terminal",
                      "memory", "swap", "disk", "battery"]
                .iter().map(|s| s.to_string()).collect(),
        }
    }
}

fn unquote(v: &str) -> String {
    v.trim().trim_matches('"').trim_matches('\'').to_string()
}

/// Reads the small TOML subset grimfetch needs: key = "string" | number | bool | ["list"].
fn load_config(explicit: Option<PathBuf>) -> Config {
    let mut cfg = Config::default();
    let mut paths: Vec<PathBuf> = Vec::new();
    if let Some(p) = explicit {
        paths.push(p);
    } else {
        let base = env::var("XDG_CONFIG_HOME").map(PathBuf::from)
            .unwrap_or_else(|_| PathBuf::from(env::var("HOME").unwrap_or_default()).join(".config"));
        paths.push(base.join("grimfetch/config.toml"));
        paths.push(PathBuf::from("/etc/grimfetch.toml"));
    }
    let text = match paths.iter().find_map(|p| fs::read_to_string(p).ok()) {
        Some(t) => t,
        None => return cfg,
    };
    let mut lines = text.lines();
    while let Some(raw) = lines.next() {
        let line = strip_comment(raw);
        let Some((k, v)) = line.split_once('=') else { continue };
        let k = k.trim();
        let mut v = v.trim().to_string();
        // lists may continue over several lines until the closing ]
        if v.starts_with('[') {
            while !v.contains(']') {
                match lines.next() { Some(more) => { v.push(' '); v.push_str(strip_comment(more).trim()); } None => break }
            }
        }
        let v = v.as_str();
        match k {
            "title_color" => cfg.title_color = unquote(v),
            "ascii_color" => cfg.ascii_color = unquote(v),
            "text_color" => cfg.text_color = unquote(v),
            "ascii" => cfg.ascii = unquote(v),
            "logo" => cfg.logo = unquote(v),
            "ascii_colors" => {
                cfg.ascii_colors = v.trim_start_matches('[').trim_end_matches(']')
                    .split(',').map(unquote).filter(|s| !s.is_empty()).collect()
            }
            "gap" => cfg.gap = v.parse().unwrap_or(cfg.gap),
            "show_title" => cfg.show_title = v == "true",
            "show_colors" => cfg.show_colors = v == "true",
            "modules" => {
                cfg.modules = v.trim_start_matches('[').trim_end_matches(']')
                    .split(',').map(unquote).filter(|s| !s.is_empty()).collect()
            }
            _ => {}
        }
    }
    cfg
}

fn strip_comment(line: &str) -> &str {
    let mut in_str = false;
    for (i, ch) in line.char_indices() {
        match ch {
            '"' => in_str = !in_str,
            '#' if !in_str => return &line[..i],
            _ => {}
        }
    }
    line
}

// ---------------------------------------------------------------- colours
fn color_code(name: &str) -> String {
    let n = name.trim().to_lowercase();
    if let Some(hex) = n.strip_prefix('#') {
        if hex.len() == 6 {
            if let (Ok(r), Ok(g), Ok(b)) = (
                u8::from_str_radix(&hex[0..2], 16),
                u8::from_str_radix(&hex[2..4], 16),
                u8::from_str_radix(&hex[4..6], 16),
            ) {
                return format!("\x1b[38;2;{r};{g};{b}m");
            }
        }
    }
    let (bright, base) = match n.strip_prefix("bright_") { Some(b) => (true, b), None => (false, n.as_str()) };
    let idx = match base {
        "black" => 0, "red" => 1, "green" => 2, "yellow" => 3,
        "blue" => 4, "magenta" => 5, "cyan" => 6, "white" => 7,
        _ => return String::new(),
    };
    format!("\x1b[{}m", if bright { 90 + idx } else { 30 + idx })
}

// ---------------------------------------------------------------- info
fn read(p: &str) -> String {
    fs::read_to_string(p).unwrap_or_default().trim().to_string()
}

fn os_name() -> String {
    let text = fs::read_to_string("/etc/os-release").unwrap_or_default();
    let get = |key: &str| text.lines().find_map(|l| l.strip_prefix(&format!("{key}=")).map(unquote));
    let name = get("PRETTY_NAME").or_else(|| get("NAME")).unwrap_or_else(|| "Linux".into());
    format!("{name} {}", env::consts::ARCH)
}

fn kernel() -> String {
    format!("Linux {}", read("/proc/sys/kernel/osrelease").replace("arch", "grim"))
}

fn uptime() -> String {
    let secs = read("/proc/uptime").split_whitespace().next()
        .and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0) as u64;
    let (d, h, m) = (secs / 86400, secs % 86400 / 3600, secs % 3600 / 60);
    let mut parts = Vec::new();
    let plural = |n: u64, w: &str| format!("{n} {w}{}", if n == 1 { "" } else { "s" });
    if d > 0 { parts.push(plural(d, "day")); }
    if h > 0 { parts.push(plural(h, "hour")); }
    if m > 0 || parts.is_empty() { parts.push(plural(m, "min")); }
    parts.join(", ")
}

fn desktop() -> String {
    for var in ["XDG_CURRENT_DESKTOP", "XDG_SESSION_DESKTOP", "DESKTOP_SESSION"] {
        if let Ok(v) = env::var(var) {
            if !v.is_empty() {
                let pretty = v.split(':').next().unwrap_or(&v).to_string();
                let session = env::var("XDG_SESSION_TYPE").unwrap_or_default();
                return if session.is_empty() || session == "tty" { pretty } else { format!("{pretty} ({session})") };
            }
        }
    }
    // No session variables: look for a running window manager
    let known = [("Hyprland", "Hyprland"), ("niri", "Niri"), ("sway", "Sway"), ("i3", "i3"),
                 ("openbox", "Openbox"), ("icewm", "IceWM"), ("xfwm4", "XFCE"), ("gnome-shell", "GNOME"),
                 ("kwin_wayland", "KDE Plasma"), ("kwin_x11", "KDE Plasma"), ("cosmic-comp", "COSMIC")];
    if let Ok(entries) = fs::read_dir("/proc") {
        for e in entries.flatten() {
            let comm = read(&format!("{}/comm", e.path().display()));
            if let Some((_, name)) = known.iter().find(|(c, _)| *c == comm) {
                return name.to_string();
            }
        }
    }
    "none (text console)".into()
}

/// Sizes read naturally: MB below 1 GB ("530 MB"), GB with one decimal above ("1.5 GB").
fn size(kib: f64) -> String {
    let mib = kib / 1024.0;
    if mib < 1024.0 {
        format!("{:.0} MB", mib)
    } else if mib < 1024.0 * 1024.0 {
        format!("{:.1} GB", mib / 1024.0)
    } else {
        format!("{:.2} TB", mib / 1024.0 / 1024.0)
    }
}

fn meminfo(key: &str) -> f64 {
    read("/proc/meminfo").lines().find(|l| l.starts_with(key))
        .and_then(|l| l.split_whitespace().nth(1)).and_then(|v| v.parse::<f64>().ok()).unwrap_or(0.0)
}

fn pct(used: f64, total: f64) -> f64 {
    if total > 0.0 { used / total * 100.0 } else { 0.0 }
}

fn memory() -> String {
    let (total, avail) = (meminfo("MemTotal:"), meminfo("MemAvailable:"));
    let used = total - avail;
    format!("{} / {} ({:.0}%)", size(used), size(total), pct(used, total))
}

fn swap() -> String {
    let (total, free) = (meminfo("SwapTotal:"), meminfo("SwapFree:"));
    if total <= 0.0 {
        return "off".into();
    }
    let used = total - free;
    let kind = if read("/proc/swaps").contains("zram") { " (zram)" } else { "" };
    format!("{} / {} ({:.0}%){kind}", size(used), size(total), pct(used, total))
}

fn host() -> Option<String> {
    let junk = ["To be filled by O.E.M.", "System Product Name", "Default string", "None", "Not Applicable", ""];
    let clean = |p: &str| { let v = read(p); if junk.contains(&v.as_str()) { String::new() } else { v } };
    let vendor = clean("/sys/devices/virtual/dmi/id/sys_vendor");
    let product = clean("/sys/devices/virtual/dmi/id/product_name");
    let version = clean("/sys/devices/virtual/dmi/id/product_version");
    let mut parts: Vec<String> = Vec::new();
    for p in [vendor, product, version] {
        if !p.is_empty() && !parts.iter().any(|x| x.contains(&p)) { parts.push(p); }
    }
    (!parts.is_empty()).then(|| parts.join(" "))
}

fn count_dirs(p: &Path) -> usize {
    fs::read_dir(p).map(|d| d.flatten().filter(|e| e.path().is_dir()).count()).unwrap_or(0)
}

fn xbps_count() -> usize {
    // Void: every installed package has a <key>pkgver</key> entry in the package database
    let Ok(dir) = fs::read_dir("/var/db/xbps") else { return 0 };
    dir.flatten()
        .filter(|e| { let n = e.file_name(); let n = n.to_string_lossy(); n.starts_with("pkgdb-") && n.ends_with(".plist") })
        .map(|e| fs::read_to_string(e.path()).unwrap_or_default().matches("<key>pkgver</key>").count())
        .max().unwrap_or(0)
}

fn packages() -> String {
    let mut out = Vec::new();
    let pac = Path::new("/var/lib/pacman/local");
    if pac.is_dir() { out.push(format!("{} (pacman)", count_dirs(pac))); }
    let xb = xbps_count();
    if xb > 0 { out.push(format!("{xb} (xbps)")); }
    let home = PathBuf::from(env::var("HOME").unwrap_or_default());
    let flat = count_dirs(Path::new("/var/lib/flatpak/app")) + count_dirs(&home.join(".local/share/flatpak/app"));
    if flat > 0 { out.push(format!("{flat} (flatpak)")); }
    out.join(", ")
}

fn shell() -> String {
    env::var("SHELL").ok().and_then(|s| Path::new(&s).file_name().map(|f| f.to_string_lossy().into_owned()))
        .unwrap_or_else(|| "unknown".into())
}

fn proc_stat(pid: &str) -> Option<(String, String)> {
    // returns (comm, ppid)
    let stat = fs::read_to_string(format!("/proc/{pid}/stat")).ok()?;
    let (l, r) = (stat.find('(')?, stat.rfind(')')?);
    let comm = stat[l + 1..r].to_string();
    let ppid = stat[r + 2..].split_whitespace().nth(1)?.to_string();
    Some((comm, ppid))
}

fn terminal() -> String {
    if let Ok(t) = env::var("TERM_PROGRAM") { if !t.is_empty() { return t; } }
    let skip = ["bash", "zsh", "fish", "sh", "dash", "sudo", "su", "doas", "grimfetch", "nu", "tmux: server", "screen"];
    let mut pid = std::process::id().to_string();
    for _ in 0..12 {
        let Some((comm, ppid)) = proc_stat(&pid) else { break };
        if !skip.contains(&comm.as_str()) && comm != "grimfetch" {
            if comm == "login" || comm == "agetty" || comm == "systemd" {
                break;
            }
            return comm;
        }
        if ppid == "0" || ppid == "1" { break; }
        pid = ppid;
    }
    fs::read_link("/proc/self/fd/0").map(|p| p.display().to_string()).unwrap_or_else(|_| "unknown".into())
}

fn resolution() -> Option<String> {
    let mut res = Vec::new();
    for e in fs::read_dir("/sys/class/drm").ok()?.flatten() {
        let p = e.path();
        if read(&p.join("status").to_string_lossy()) == "connected" {
            if let Some(m) = read(&p.join("modes").to_string_lossy()).lines().next() {
                res.push(m.to_string());
            }
        }
    }
    (!res.is_empty()).then(|| res.join(", "))
}

fn rice() -> Option<String> {
    let home = PathBuf::from(env::var("HOME").ok()?);
    let st = fs::read_to_string(home.join(".config/grimos/rice.json")).ok()?;
    let id = st.split("\"rice\"").nth(1)?.split('"').nth(1)?.to_string();
    let def = fs::read_to_string(format!("/usr/share/grimos/rices/{id}.json")).unwrap_or_default();
    let name = def.split("\"name\"").nth(1).and_then(|s| s.split('"').nth(1)).unwrap_or(&id).to_string();
    Some(name)
}

fn local_ip() -> Option<String> {
    let out = std::process::Command::new("ip").args(["-4", "-o", "addr", "show", "scope", "global"]).output().ok()?;
    let text = String::from_utf8_lossy(&out.stdout);
    let line = text.lines().next()?;
    let f: Vec<&str> = line.split_whitespace().collect();
    Some(format!("{} ({})", f.get(3)?.split('/').next()?, f.get(1)?))
}

fn locale() -> Option<String> {
    env::var("LANG").ok().filter(|s| !s.is_empty())
}

#[repr(C)]
#[derive(Default)]
struct Statvfs {
    f_bsize: u64, f_frsize: u64, f_blocks: u64, f_bfree: u64, f_bavail: u64,
    f_files: u64, f_ffree: u64, f_favail: u64, f_fsid: u64, f_flag: u64, f_namemax: u64,
    spare: [i32; 6],
}
extern "C" {
    fn statvfs(path: *const c_char, buf: *mut Statvfs) -> c_int;
    fn isatty(fd: c_int) -> c_int;
}

fn disk() -> String {
    let path = CString::new("/").unwrap();
    let mut s = Statvfs::default();
    if unsafe { statvfs(path.as_ptr(), &mut s) } != 0 {
        return "unknown".into();
    }
    let total = (s.f_blocks * s.f_frsize) as f64 / 1024.0;
    let free = (s.f_bavail * s.f_frsize) as f64 / 1024.0;
    let used = total - free;
    let fs_type = fs::read_to_string("/proc/mounts").unwrap_or_default().lines()
        .find_map(|l| { let f: Vec<&str> = l.split_whitespace().collect(); (f.get(1) == Some(&"/")).then(|| f[2].to_string()) })
        .unwrap_or_default();
    format!("{} / {} ({:.0}%){}", size(used), size(total), pct(used, total),
            if fs_type.is_empty() { String::new() } else { format!(" - {fs_type}") })
}

fn battery() -> Option<String> {
    let dir = fs::read_dir("/sys/class/power_supply").ok()?;
    for e in dir.flatten() {
        let p = e.path();
        if read(&p.join("type").to_string_lossy()) == "Battery" {
            let cap = read(&p.join("capacity").to_string_lossy());
            let status = read(&p.join("status").to_string_lossy());
            if cap.is_empty() { continue; }
            return Some(if status.is_empty() { format!("{cap}%") } else { format!("{cap}% [{status}]") });
        }
    }
    None
}

fn user_host() -> String {
    let user = env::var("USER").or_else(|_| env::var("LOGNAME")).unwrap_or_else(|_| "user".into());
    let host = read("/proc/sys/kernel/hostname");
    format!("{user}@{host}")
}

// ---------------------------------------------------------------- live mode
// `grimfetch --live`: the same screen, redrawn every second, with CPU, memory, temperature
// and network graphs underneath. q, Esc or Ctrl+C quits.
struct Live {
    cpu_prev: (u64, u64),          // (busy, total) jiffies at the last sample
    net_prev: (u64, u64),          // (rx, tx) bytes
    cpu_hist: Vec<f64>,
    mem_hist: Vec<f64>,
    cpu_now: f64,
    rx_rate: f64,
    tx_rate: f64,
    temp: Option<f64>,
}

const HIST: usize = 30;

fn cpu_jiffies() -> (u64, u64) {
    let s = read("/proc/stat");
    let line = s.lines().next().unwrap_or("");
    let v: Vec<u64> = line.split_whitespace().skip(1).filter_map(|x| x.parse().ok()).collect();
    if v.len() < 5 { return (0, 0); }
    let total: u64 = v.iter().take(8).sum();
    let idle = v[3] + v[4];                          // idle + iowait
    (total.saturating_sub(idle), total)
}

fn net_bytes() -> (u64, u64) {
    let mut rx = 0; let mut tx = 0;
    for line in read("/proc/net/dev").lines().skip(2) {
        let Some((name, rest)) = line.split_once(':') else { continue };
        if name.trim() == "lo" { continue; }
        let v: Vec<u64> = rest.split_whitespace().filter_map(|x| x.parse().ok()).collect();
        if v.len() >= 9 { rx += v[0]; tx += v[8]; }
    }
    (rx, tx)
}

fn cpu_temp() -> Option<f64> {
    let dir = fs::read_dir("/sys/class/hwmon").ok()?;
    for e in dir.flatten() {
        let name = read(&format!("{}/name", e.path().display()));
        if ["k10temp", "coretemp", "zenpower", "cpu_thermal", "acpitz"].contains(&name.trim()) {
            if let Ok(t) = read(&format!("{}/temp1_input", e.path().display())).trim().parse::<f64>() {
                return Some(t / 1000.0);
            }
        }
    }
    None
}

impl Live {
    fn new() -> Live {
        Live { cpu_prev: cpu_jiffies(), net_prev: net_bytes(), cpu_hist: Vec::new(), mem_hist: Vec::new(),
               cpu_now: 0.0, rx_rate: 0.0, tx_rate: 0.0, temp: cpu_temp() }
    }
    fn sample(&mut self, secs: f64) {
        let (b, t) = cpu_jiffies();
        let (pb, pt) = self.cpu_prev;
        self.cpu_now = if t > pt { (b.saturating_sub(pb)) as f64 / (t - pt) as f64 * 100.0 } else { 0.0 };
        self.cpu_prev = (b, t);
        let (rx, tx) = net_bytes();
        self.rx_rate = rx.saturating_sub(self.net_prev.0) as f64 / secs;
        self.tx_rate = tx.saturating_sub(self.net_prev.1) as f64 / secs;
        self.net_prev = (rx, tx);
        let total = meminfo("MemTotal");
        let used = total - meminfo("MemAvailable");
        push(&mut self.cpu_hist, self.cpu_now);
        push(&mut self.mem_hist, pct(used, total));
        self.temp = cpu_temp();
    }
}

fn push(h: &mut Vec<f64>, v: f64) { h.push(v); if h.len() > HIST { h.remove(0); } }

fn spark(h: &[f64]) -> String {
    const B: [char; 8] = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];
    let mut s: String = std::iter::repeat(' ').take(HIST.saturating_sub(h.len())).collect();
    for v in h { s.push(B[((v.clamp(0.0, 100.0) / 100.0) * 7.0).round() as usize]); }
    s
}

fn bar(p: f64, on: &str, off: &str, reset: &str) -> String {
    let n = ((p.clamp(0.0, 100.0) / 100.0) * 20.0).round() as usize;
    format!("{on}{}{reset}{off}{}{reset}", "█".repeat(n), "░".repeat(20 - n))
}

fn rate(b: f64) -> String {
    if b >= 1048576.0 { format!("{:.1} MB/s", b / 1048576.0) }
    else if b >= 1024.0 { format!("{:.0} KB/s", b / 1024.0) }
    else { format!("{:.0} B/s", b) }
}

// The terminal goes into "no line editing, no echo, keys as bytes" while live mode runs,
// so q and Ctrl+C arrive as keys and the screen can be put back properly afterwards.
fn stty(args: &[&str]) -> Option<String> {
    std::process::Command::new("stty").args(args).stdin(std::process::Stdio::inherit()).output().ok()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
}

fn run_live(cfg: &Config, no_color: bool, every: f64) {
    use std::io::{Read, Write};
    use std::sync::atomic::{AtomicBool, Ordering};
    use std::sync::Arc;
    if unsafe { isatty(1) } == 0 || unsafe { isatty(0) } == 0 {
        eprintln!("grimfetch: --live needs a terminal");
        std::process::exit(2);
    }
    let saved = stty(&["-g"]).unwrap_or_default();
    stty(&["-icanon", "-echo", "-isig", "min", "1", "time", "0"]);
    let quit = Arc::new(AtomicBool::new(false));
    {
        let quit = quit.clone();
        std::thread::spawn(move || {
            let mut b = [0u8; 1];
            let mut stdin = std::io::stdin();
            while stdin.read(&mut b).map(|n| n > 0).unwrap_or(false) {
                if matches!(b[0], b'q' | b'Q' | 3 | 27) { quit.store(true, Ordering::SeqCst); break; }
            }
        });
    }
    let mut out = std::io::stdout();
    let _ = write!(out, "\x1b[?1049h\x1b[?25l");
    let mut live = Live::new();
    let tick = std::time::Duration::from_millis(100);
    let mut waited = 0.0;
    let mut first = true;
    while !quit.load(Ordering::SeqCst) {
        if first || waited >= every {
            if !first { live.sample(waited); }
            first = false;
            waited = 0.0;
            let lines = screen(cfg, no_color, Some(&live));
            let mut frame = String::from("\x1b[H");
            for l in lines { frame.push_str(&l); frame.push_str("\x1b[K\r\n"); }
            frame.push_str("\x1b[J");
            let _ = out.write_all(frame.as_bytes());
            let _ = out.flush();
        }
        std::thread::sleep(tick);
        waited += 0.1;
    }
    let _ = write!(out, "\x1b[?25h\x1b[?1049l");
    let _ = out.flush();
    if !saved.is_empty() { stty(&[&saved]); } else { stty(&["sane"]); }
}

// ---------------------------------------------------------------- output
/// Width of an art line on screen, not counting ${cN} colour markers.
fn art_width(l: &str) -> usize {
    let mut n = l.chars().count();
    for d in 1..=9 { n -= l.matches(&format!("${{c{d}}}")).count() * 5; }
    n
}

/// The art file: a named logo (`logo = "void"` or --logo) if one exists, else `ascii`.
fn logo_path(cfg: &Config) -> String {
    if !cfg.logo.is_empty() {
        for dir in ["/usr/share/grim/logos", "/usr/share/grimos/logos"] {
            let p = format!("{dir}/{}.txt", cfg.logo);
            if Path::new(&p).exists() { return p; }
        }
    }
    cfg.ascii.clone()
}

fn screen(cfg: &Config, no_color: bool, live: Option<&Live>) -> Vec<String> {
    let paint = |c: &str| if no_color { String::new() } else { color_code(c) };
    let (title, art_c, text_c) = (paint(&cfg.title_color), paint(&cfg.ascii_color), paint(&cfg.text_color));
    let bold = if no_color { "" } else { "\x1b[1m" };
    let reset = if no_color { "" } else { "\x1b[0m" };
    let dim = if no_color { "" } else { "\x1b[90m" };

    let art_path = logo_path(cfg);
    let art: Vec<String> = if Path::new(&art_path).exists() {
        fs::read_to_string(&art_path).unwrap_or_default().lines().map(|l| l.trim_end().to_string()).collect()
    } else { Vec::new() };
    let width = art.iter().map(|l| art_width(l)).max().unwrap_or(0);
    // ${c1}..${c9} inside the art switch colour (from ascii_colors, else ascii_color)
    let art_colors: Vec<String> = (0..9).map(|i| paint(cfg.ascii_colors.get(i).unwrap_or(&cfg.ascii_color))).collect();
    let colorize = |l: &str| -> String {
        let mut out = String::new();
        let mut rest = l;
        while let Some(p) = rest.find("${c") {
            out.push_str(&rest[..p]);
            let tail = &rest[p + 3..];
            match (tail.chars().next().and_then(|c| c.to_digit(10)), tail.get(1..2)) {
                (Some(d @ 1..=9), Some("}")) => { out.push_str(&art_colors[d as usize - 1]); rest = &tail[2..]; }
                _ => { out.push_str("${c"); rest = tail; }
            }
        }
        out.push_str(rest);
        out
    };

    let mut info: Vec<String> = Vec::new();
    if cfg.show_title {
        let uh = user_host();
        info.push(format!("{bold}{title}{uh}{reset}"));
        info.push(format!("{title}{}{reset}", "─".repeat(uh.chars().count())));
    }
    for m in &cfg.modules {
        let lines: Vec<(&str, Option<String>)> = match m.as_str() {
            "os" => vec![("OS", Some(os_name()))],
            "host" => vec![("Host", host())],
            "kernel" => vec![("Kernel", Some(kernel()))],
            "uptime" => vec![("Uptime", Some(uptime()))],
            "packages" => vec![("Packages", Some(packages()))],
            "shell" => vec![("Shell", Some(shell()))],
            "desktop" => vec![("Desktop", Some(desktop()))],
            "rice" => vec![("Rice", rice())],
            "terminal" => vec![("Terminal", Some(terminal()))],
            "resolution" => vec![("Display", resolution())],
            "memory" => vec![("Memory", Some(memory()))],
            "swap" => vec![("Swap", Some(swap()))],
            "disk" => vec![("Disk (/)", Some(disk()))],
            "battery" => vec![("Battery", battery())],
            "localip" => vec![("Local IP", local_ip())],
            "locale" => vec![("Locale", locale())],
            _ => continue,
        };
        for (label, value) in lines {
            if let Some(v) = value {
                info.push(format!("{bold}{title}{label:<9}{reset} {text_c}{v}{reset}"));
            }
        }
    }
    if let Some(l) = live {
        let lab = |t: &str| format!("{bold}{title}{t:<9}{reset}");
        let total = meminfo("MemTotal");
        let used = total - meminfo("MemAvailable");
        info.push(String::new());
        info.push(format!("{} {} {text_c}{:>5.1}%{reset}  {dim}{}{reset}", lab("CPU"), bar(l.cpu_now, &title, dim, reset), l.cpu_now, spark(&l.cpu_hist)));
        info.push(format!("{} {} {text_c}{:>5.1}%{reset}  {dim}{}{reset}", lab("RAM"), bar(pct(used, total), &title, dim, reset), pct(used, total), spark(&l.mem_hist)));
        info.push(format!("{} {text_c}{} / {}{reset}", lab(""), size(used), size(total)));
        if let Some(t) = l.temp { info.push(format!("{} {text_c}{t:.0} °C{reset}", lab("CPU temp"))); }
        info.push(format!("{} {text_c}↓ {}   ↑ {}{reset}", lab("Network"), rate(l.rx_rate), rate(l.tx_rate)));
    }
    if cfg.show_colors && !no_color {
        info.push(String::new());
        info.push((0..8).map(|i| format!("\x1b[4{i}m   ")).collect::<String>() + "\x1b[0m");
        info.push((0..8).map(|i| format!("\x1b[10{i}m   ")).collect::<String>() + "\x1b[0m");
    }

    if live.is_some() {
        info.push(String::new());
        info.push(format!("{dim}q to quit{reset}"));
    }

    // put the info a little below the top of the art
    let top = if art.len() > info.len() + 2 { 2 } else { 0 };
    let rows = art.len().max(info.len() + top);
    let mut out = vec![String::new()];
    for i in 0..rows {
        let a = art.get(i).map(String::as_str).unwrap_or("");
        let pad = width - art_width(a);
        let right = if i >= top { info.get(i - top).map(String::as_str).unwrap_or("") } else { "" };
        if width > 0 {
            out.push(format!(" {art_c}{}{reset}{}{}{right}", colorize(a), " ".repeat(pad), " ".repeat(cfg.gap)));
        } else {
            out.push(format!(" {right}"));
        }
    }
    out.push(String::new());
    out
}

fn main() {
    let mut args = env::args().skip(1);
    let mut cfg_path = None;
    let mut no_color = env::var_os("NO_COLOR").is_some() || unsafe { isatty(1) } == 0;
    let mut live = false;
    let mut every = 1.0;
    let mut logo: Option<String> = None;
    while let Some(a) = args.next() {
        match a.as_str() {
            "--logo" => logo = args.next(),
            "-c" | "--config" => cfg_path = args.next().map(PathBuf::from),
            "--no-color" => no_color = true,
            "--color" => no_color = false,
            "-l" | "--live" | "--Live" => live = true,
            "-i" | "--interval" => every = args.next().and_then(|v| v.parse::<f64>().ok()).unwrap_or(1.0).clamp(0.2, 60.0),
            "-v" | "--version" => { println!("grimfetch {VERSION}"); return; }
            "-h" | "--help" => {
                println!("grimfetch {VERSION}: Grim OS system info\n\n  grimfetch [--config FILE] [--logo NAME] [--no-color | --color]\n  \
                          grimfetch --live [--interval SECONDS]   live CPU, memory, temperature and network (q quits)\n\n\
                          Config: ~/.config/grimfetch/config.toml (falls back to /etc/grimfetch.toml)");
                return;
            }
            _ => { eprintln!("grimfetch: unknown option {a} (try --help)"); std::process::exit(2); }
        }
    }
    let mut cfg = load_config(cfg_path);
    if let Some(l) = logo { cfg.logo = l; }
    if live { run_live(&cfg, no_color, every); return; }
    for l in screen(&cfg, no_color, None) { println!("{l}"); }
}
