#!/bin/sh
# install.sh — One-line starter-shell install
# Usage: curl -fsSL https://superinstance.github.io/starter-shell/install.sh | sh
set -e
echo "🔮 Installing Starter Shell..."
echo ""

# Try pip first (most common)
if command -v pip3 > /dev/null 2>&1; then
    pip3 install starter-shell -q
    echo ""
    starter-shell
    exit 0
fi
if command -v pip > /dev/null 2>&1; then
    pip install starter-shell -q
    echo ""
    starter-shell
    exit 0
fi

# Fallback: cargo
if command -v cargo > /dev/null 2>&1; then
    cargo install starter-shell
    starter-shell
    exit 0
fi

# Fallback: git clone
echo "No package manager found. Cloning repo..."
git clone https://github.com/SuperInstance/starter-shell.git
cd starter-shell
python3 onboarding.py
