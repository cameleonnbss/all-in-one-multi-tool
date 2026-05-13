@echo off
title camzzz Multi-Tool v5 - Installer
color 0A

echo.
echo  ========================================
echo   camzzz Multi-Tool v5  --  Installer
echo  ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python not found.
    echo  Download Python:
    echo  https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  [*] Uninstalling dependencies...
echo.

pip uninstall -y requests colorama beautifulsoup4 dnspython phonenumbers Pillow pefile cryptography flask pyngrok scapy impacket pymysql paramiko discord-webhook keyboard pyautogui opencv-python pywin32 python-magic-bin psutil

echo.
echo  [+] Done!
echo.
pause
