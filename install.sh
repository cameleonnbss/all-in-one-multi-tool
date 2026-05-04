set -e
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║    camzzz Multi-Tool — Installer         ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Detect Termux
if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
    TERMUX=true
    echo -e "${YELLOW}[*] Termux detected${NC}"
else
    TERMUX=false
fi

# Check Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[-] Python3 not found.${NC}"
    if [ "$TERMUX" = true ]; then
        echo "    Run: pkg install python"
    else
        echo "    Run: sudo apt install python3 python3-pip"
    fi
    exit 1
fi

echo -e "${GREEN}[+] Python $(python3 --version)${NC}"

# Install deps
if [ "$TERMUX" = true ]; then
    echo -e "${YELLOW}[*] Installing Termux system packages...${NC}"
    pkg install -y clang libffi openssl libjpeg-turbo libpng 2>/dev/null || true

    echo -e "${YELLOW}[*] Installing Pillow (special Termux flags)...${NC}"
    CFLAGS="-I$(python3 -c 'import sysconfig; print(sysconfig.get_path("include"))')" \
        pip install Pillow --no-binary :all: --quiet || true

    echo -e "${YELLOW}[*] Installing compatible packages...${NC}"
    pip install -r requirements-termux.txt --quiet --break-system-packages 2>/dev/null || \
    pip install -r requirements-termux.txt --quiet
else
    echo -e "${YELLOW}[*] Installing packages...${NC}"
    pip3 install -r requirements.txt --quiet --break-system-packages 2>/dev/null || \
    pip3 install -r requirements.txt --quiet
fi

echo ""
echo -e "${GREEN}[+] Done! Run with:${NC}"
echo "    python3 multi-tool.py"
echo ""
