#!/usr/bin/env python3
"""starter-shell CLI — one command to lay a keel.

Usage:
    starter-shell              # Run onboarding
    starter-shell init         # Quick init (uses defaults)
    starter-shell hardware     # Show hardware info
    starter-shell agent        # Run the agent loop
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ["onboard"]
    
    if args[0] in ("onboard", "init", "--init"):
        from onboarding import main as onboard
        onboard()
    elif args[0] in ("hardware", "hw", "--hardware"):
        from hardware import detect
        import json
        hw = detect()
        print(f"   {hw['platform']} | {hw['cores']} cores | {hw['memory_mb']}MB RAM")
        print(f"   Languages: {', '.join(hw['languages'])}")
        print(f"   Compilers: {', '.join(hw['compilers'].keys())}")
        if hw.get('gpu'): print(f"   GPU: {hw['gpu']['info']}")
    elif args[0] in ("agent", "--agent"):
        from agent import Agent
        agent = Agent("starter", plato_url=os.environ.get("PLATO_URL"))
        rooms = ["forge", "fleet_health", "vessel-room-navigator"]
        agent.run(rooms)
    elif args[0] in ("modules", "--modules"):
        from modules import list_modules, install_module
        mods = list_modules()
        target = args[1] if len(args) > 1 else None
        if target:
            result = install_module(target)
            print(f"{'✅' if result.get('ok') else '❌'} {target}")
        else:
            print(f"{len(mods)} modules available:")
            for m in mods:
                status = "✅" if m["installed"] else "⬜"
                print(f"  {status} {m['name']:20s} {m.get('desc','')[:50]}")
    elif args[0] in ("version", "--version", "-v"):
        print("starter-shell v0.1.1")
    else:
        print(f"Usage: starter-shell [onboard|hardware|agent|modules|version]")
        print(f"  (default: onboard)")

if __name__ == "__main__":
    main()
