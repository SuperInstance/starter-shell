#!/usr/bin/env python3
"""modules.py — Modular expansion system for the starter shell.

Each module adds a capability. Install them as needed.
Your shell grows with you.
"""
import json, subprocess, sys, os, urllib.request, importlib.util

MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")

def list_modules():
    """List all available modules and their status."""
    modules = []
    if not os.path.isdir(MODULES_DIR): return modules
    for name in sorted(os.listdir(MODULES_DIR)):
        meta = os.path.join(MODULES_DIR, name, "module.json")
        if os.path.isfile(meta):
            with open(meta) as f:
                info = json.load(f)
                info["name"] = name
                info["installed"] = os.path.isfile(
                    os.path.join(MODULES_DIR, name, ".installed"))
                modules.append(info)
    return modules

def install_module(name):
    """Install a module by name."""
    meta = os.path.join(MODULES_DIR, name, "module.json")
    if not os.path.isfile(meta):
        return {"error": f"Module '{name}' not found"}
    
    with open(meta) as f:
        info = json.load(f)
    
    results = {"name": name, "actions": []}
    
    for action in info.get("install", []):
        action_type = action.get("type", "")
        target = action.get("target", "")
        
        if action_type == "pip":
            r = subprocess.run(["pip", "install", target], capture_output=True, text=True)
            results["actions"].append({"type": "pip", "target": target, "ok": r.returncode == 0})
        
        elif action_type == "cargo":
            r = subprocess.run(["cargo", "install", target], capture_output=True, text=True)
            results["actions"].append({"type": "cargo", "target": target, "ok": r.returncode == 0})
        
        elif action_type == "npm":
            r = subprocess.run(["npm", "install", "-g", target], capture_output=True, text=True)
            results["actions"].append({"type": "npm", "target": target, "ok": r.returncode == 0})
        
        elif action_type == "git":
            dest = os.path.join(os.path.dirname(__file__), "modules", name, target)
            if not os.path.isdir(dest):
                r = subprocess.run(["git", "clone", action.get("url", ""), dest],
                    capture_output=True, text=True)
                results["actions"].append({"type": "git", "target": target, "ok": r.returncode == 0})
            else:
                results["actions"].append({"type": "git", "target": target, "ok": True, "msg": "already cloned"})
    
    # Mark installed
    flag = os.path.join(MODULES_DIR, name, ".installed")
    open(flag, "w").close()
    results["ok"] = all(a.get("ok") for a in results["actions"])
    return results

def get_shell_name():
    from hardware import detect
    hw = detect()
    return f"shell-{hw['platform']}"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Starter Shell Module Manager")
    ap.add_argument("action", choices=["list", "install", "info"], nargs="?")
    ap.add_argument("module", nargs="?")
    args = ap.parse_args()
    
    if args.action == "list" or args.action is None:
        modules = list_modules()
        if not modules:
            print("No modules available. The shell is bare.")
            print("Add modules to the modules/ directory.")
        else:
            print(f"Available modules ({len(modules)}):")
            for m in modules:
                status = "✅" if m["installed"] else "⬜"
                print(f"  {status} {m['name']:20s} {m.get('desc','')[:50]}")
    
    elif args.action == "install":
        if not args.module:
            print("Specify a module: python3 modules.py install <name>")
            sys.exit(1)
        result = install_module(args.module)
        if result.get("ok"):
            print(f"✅ Module '{args.module}' installed")
        else:
            print(f"⚠️  Module '{args.module}' partially installed")
            for a in result.get("actions", []):
                status = "✅" if a.get("ok") else "❌"
                print(f"  {status} {a.get('type')}: {a.get('target')}")
    
    elif args.action == "info":
        meta = os.path.join(MODULES_DIR, args.module, "module.json") if args.module else None
        if meta and os.path.isfile(meta):
            with open(meta) as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print(f"Module '{args.module}' not found")
