#!/usr/bin/env python3
"""hardware.py — Detect available hardware, compilers, and capabilities.

Adapts the shell to whatever machine it lands on.
"""
import subprocess, os, platform, json, sys

def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return ""

def detect():
    info = {
        "platform": platform.machine(),
        "arch": platform.processor() or platform.machine(),
        "os": platform.system().lower(),
        "cores": os.cpu_count() or 1,
        "memory_mb": 0,
        "compilers": {},
        "languages": [],
        "gpu": None,
        "python_version": platform.python_version(),
    }
    
    # Memory
    try:
        if info["os"] == "linux":
            mem = int(open("/proc/meminfo").readline().split()[1])
            info["memory_mb"] = mem // 1024
    except: pass
    
    # Compilers
    for cc in ["gcc", "clang", "g++", "rustc", "zig", "nim", "go"]:
        v = run(["which", cc]) and run([cc, "--version"])[:60] or ""
        if v:
            ver = v.split("\n")[0] if v else ""
            info["compilers"][cc] = ver
    
    # Languages available
    if "python3" in run(["which", "python3"]): info["languages"].append("python")
    if "rustc" in info["compilers"]: info["languages"].append("rust")
    if "zig" in info["compilers"]: info["languages"].append("zig")
    if "nim" in info["compilers"]: info["languages"].append("nim")
    if "go" in info["compilers"]: info["languages"].append("go")
    
    # GPU
    nvidia = run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
    if nvidia: info["gpu"] = {"vendor": "nvidia", "info": nvidia[:80]}
    
    return info

if __name__ == "__main__":
    hw = detect()
    print(json.dumps(hw, indent=2))
    print(f"\n→ This shell can run: {', '.join(hw['languages'])}")
    print(f"→ Compilers available: {', '.join(hw['compilers'].keys())}")
    if hw["gpu"]: print(f"→ GPU: {hw['gpu']['vendor']}")
