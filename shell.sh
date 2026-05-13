#!/bin/bash
# shell.sh — Bootstrap this shell on any hardware.
# Usage: bash shell.sh [shell-name]

SHELL_NAME="${1:-starter-shell}"
echo "🔮 Laying keel for '$SHELL_NAME'..."

echo "   Probing hardware..."
python3 hardware.py 2>/dev/null || python hardware.py

echo "   Connecting to PLATO..."
if python3 -c "from plato import PlatoClient; PlatoClient().probe_rooms()" 2>/dev/null; then
    echo "   ✅ PLATO reachable at ${PLATO_URL:-localhost:8847}"
else
    echo "   ⚠️  No PLATO server found to connect to the specific url"
    echo "   PLATO_URL=http://your-server python3 plato.py"
fi

echo "   Bootstrapping rooms..."
python3 plato.py 2>/dev/null || echo "   ⚠️  PLATO unavailable — bootstrap deferred"

echo "   Checking hardware capabilities..."
python3 -c "
from hardware import detect
hw = detect()
print(f'   📋 {hw[\"platform\"]} | {hw[\"cores\"]} cores | {hw[\"memory_mb\"]}MB RAM')
print(f'   📋 Languages: {\", \".join(hw[\"languages\"])}')
print(f'   📋 Compilers: {\", \".join(hw[\"compilers\"].keys())}')
echo ""

echo "🔮 Shell '$SHELL_NAME' is live."
echo ""
echo "   python3 agent.py              — Run the agent loop"
echo "   python3 hardware.py           — Detect hardware"  
echo "   python3 plato.py              — Connect to PLATO"
