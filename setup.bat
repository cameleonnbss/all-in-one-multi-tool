@echo off
chcp 65001 >/dev/null 2>&1
title ALL IN ONE TOOL v5 -- Setup by camzzz

echo.
echo  ============================================
echo   ALL IN ONE TOOL v5  --  camzzz
echo   github.com/cameleonnbss
echo  ============================================
echo.

:: Verifier Python
python --version >/dev/null 2>&1
if errorlevel 1 (
    echo  [!] Python non trouve. Installe Python 3.8+ depuis python.org
    pause
    exit /b 1
)

echo  [*] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

echo  [*] Installation des dependances principales...
python -m pip install requests colorama beautifulsoup4 dnspython phonenumbers cryptography Pillow scapy paramiko pymysql impacket flask pyngrok --quiet

echo  [*] Installation des dependances optionnelles (RAT, scanner)...
python -m pip install discord.py discord-webhook keyboard pyautogui opencv-python pywin32 pefile psutil --quiet 2>/dev/null

echo.
echo  [+] Installation terminee !
echo.
echo  [*] Lancement du tool...
echo.

python "%~dp0multi-tooV5.py"

pause
