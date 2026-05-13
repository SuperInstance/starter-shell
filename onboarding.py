#!/usr/bin/env python3
"""onboarding.py — Walk through shell setup step by step.

Like OpenClaw's FIRST_RUN, but for the starter shell.
"""
import os, sys, json, subprocess
from pathlib import Path

SHELL_DIR = Path(__file__).parent

def step(n, msg): print(f"\n[{n}/5] {msg}")

def ask(prompt, default=""):
    try:
        r = input(f"  {prompt} [{default}]: ").strip()
        return r if r else default
    except (EOFError, KeyboardInterrupt):
        return default

def main():
    print("\n🔮 Starter Shell — Onboarding")
    print("=" * 40)
    print("You're about to lay the keel for a new shell.")
    print("This takes about 2 minutes.\n")
    
    # Step 1: Identity
    step(1, "Who is this shell for?")
    name = ask("Project or shell name", "my-project")
    user = ask("Your name", os.environ.get("USER", "developer"))
    
    # Step 2: Hardware
    step(2, "Detecting hardware...")
    from hardware import detect
    hw = detect()
    print(f"  ✅ {hw['platform']} | {hw['cores']} cores | {hw['memory_mb']}MB RAM")
    print(f"  ✅ Languages: {', '.join(hw['languages'])}")
    print(f"  ✅ Compilers: {', '.join(hw['compilers'].keys())}")
    
    # Step 3: PLATO
    step(3, "Connecting to PLATO...")
    try:
        from plato import PlatoClient
        client = PlatoClient()
        rooms = client.probe_rooms()
        if isinstance(rooms, dict) and len(rooms) > 0:
            print(f"  ✅ PLATO reachable: {len(rooms)} rooms")
            print(f"  Creating room for '{name}'...")
            client.create_room(name)
            client.submit_tile(name, 
                f"What is the {name} shell?", 
                f"Starter shell on {hw['platform']} by {user}")
            client.submit_tile(name,
                "What hardware does this shell run on?",
                json.dumps(hw, indent=2))
        else:
            print(f"  ⚠️  PLATO server has no rooms yet")
            print(f"  Room '{name}' queued for when PLATO is available")
    except Exception as e:
        print(f"  ⚠️  PLATO not available: {e}")
        print(f"  Set PLATO_URL env var to connect later")
    
    # Step 4: Modules
    step(4, "What modules do you want?")
    from modules import list_modules
    available = list_modules()
    if available:
        print(f"  Available modules:")
        for m in available:
            print(f"    {m['name']:20s} {m.get('desc','')[:50]}")
        
        install = ask("Modules to install (comma-separated, or 'all')", "none")
        if install.lower() == "all":
            for m in available:
                if not m["installed"]:
                    try:
                        from modules import install_module
                        r = install_module(m["name"])
                        print(f"    {'✅' if r.get('ok') else '⚠️'} {m['name']}")
                    except: pass
        elif install and install != "none":
            for m_name in install.split(","):
                m_name = m_name.strip()
                if m_name:
                    try:
                        from modules import install_module
                        r = install_module(m_name)
                        print(f"    {'✅' if r.get('ok') else '⚠️'} {m_name}")
                    except Exception as e:
                        print(f"    ❌ {m_name}: {e}")
    
    # Step 5: Summary
    step(5, "Shell is ready")
    print(f"\n  🔮 Shell '{name}' is live.")
    print(f"  📋 Hardware: {hw['platform']} | {hw['cores']}c | {hw['memory_mb']}MB")
    print(f"  📋 PLATO: {'Connected' if 'client' in dir() and rooms else 'Deferred'}")
    print(f"\n  Try:")
    print(f"    python3 agent.py           — Run the agent loop")
    print(f"    python3 modules.py list    — See available modules")
    print(f"    python3 hardware.py        — Detect hardware")
    print(f"    python3 plato.py           — Connect to PLATO")
    print()

if __name__ == "__main__":
    main()
