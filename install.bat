@echo off
title camzzz Multi-Tool v5 - Installer
color 0A
echo.
echo  ========================================
echo   camzzz Multi-Tool v5  --  Installer
echo  ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python not found. Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  [*] Installing dependencies...
echo.

pip install -r requirements.txt --break-system-packages 2>nul || pip install -r requirements.txt

echo.
echo  [+] Done!
echo.
echo  Run the tool:
echo    python multi-tooV5-fixed-v2.py
echo.
pause
