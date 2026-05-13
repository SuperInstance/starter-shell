#!/usr/bin/env python3
"""setup.py — Bootstrap this shell. Detects hardware, connects to PLATO,
creates rooms, and runs the agent. One command sets up everything."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from hardware import detect
from plato import bootstrap as plato_bootstrap

def main():
    shell_name = sys.argv[1] if len(sys.argv) > 1 else "starter-shell"
    print(f"🔮 Laying keel for '{shell_name}'...")
    
    # 1. Detect hardware
    print(f"   Probing hardware...")
    hw = detect()
    print(f"   📋 {hw['platform']} | {hw['cores']} cores | {hw['memory_mb']}MB RAM")
    print(f"   📋 Languages: {', '.join(hw['languages'])}")
    print(f"   📋 Compilers: {', '.join(hw['compilers'].keys())}")
    
    # 2. Try PLATO
    try:
        from plato import PlatoClient
        client = PlatoClient()
        rooms = client.probe_rooms()
        if isinstance(rooms, dict) and len(rooms) > 0:
            print(f"   ✅ PLATO reachable: {len(rooms)} rooms")
            plato_bootstrap(hw)
        else:
            print(f"   ⚠️  PLATO server at {client.url} has no rooms yet")
    except Exception as e:
        print(f"   ⚠️  No PLATO server at {os.environ.get('PLATO_URL', 'localhost:8847')}")
        print(f"      Set PLATO_URL to connect, or start one")
    
    # 3. Run agent
    print(f"\n🔮 Shell '{shell_name}' is live.")
    print(f"\nTry: python3 agent.py")

if __name__ == "__main__":
    main()
