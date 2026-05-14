"""flux_lsp headspace — Language Server Protocol for FLUX ISA.

This headspace wraps the flux_lsp TypeScript LSP server from the
SuperInstance/flux_lsp repo. It requires Node.js >=18 and npm packages
from the flux_lsp package.json.

Usage:
    from headspaces.flux_lsp import start, stop, status
    start({"port": 5100, "lsp_path": "/tmp/flux_lsp"})

VSCode Integration:
    Add to .vscode/extensions.json in your workspace:
    {
      "recommendations": ["superinstance.flux_lsp-vscode"]
    }
    Or use the LSP client wrapper in client/extension.ts from the flux_lsp repo.

Environment Variables:
    FLUX_LSP_PORT   — port for LSP server (default: 5100)
    FLUX_LSP_PATH   — path to flux_lsp repo (default: /tmp/flux_lsp)
"""
import os, subprocess, threading, json, signal

LSP_PATH = os.environ.get("FLUX_LSP_PATH", "/tmp/flux_lsp")
LSP_PORT = int(os.environ.get("FLUX_LSP_PORT", "5100"))

PROCESS = None
THREAD = None
RUNNING = False

def _build_if_needed():
    """Build TypeScript LSP server if dist/ doesn't exist."""
    dist = os.path.join(LSP_PATH, "dist", "server.js")
    if os.path.exists(dist):
        return True
    print(f"🔧 flux_lsp: building TypeScript server (first time setup)...")
    try:
        r = subprocess.run(
            ["npm", "install", "--prefix", LSP_PATH],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode != 0:
            print(f"⚠️  npm install failed: {r.stderr[:500]}")
        r2 = subprocess.run(
            ["npm", "run", "--prefix", LSP_PATH, "build"],
            capture_output=True, text=True, timeout=60
        )
        if r2.returncode != 0:
            print(f"⚠️  npm build failed: {r2.stderr[:500]}")
            return False
        print("✅  flux_lsp: build complete")
        return True
    except Exception as e:
        print(f"⚠️  flux_lsp: build error {e}")
        return False

def _run_server():
    global PROCESS, RUNNING
    server_js = os.path.join(LSP_PATH, "dist", "server.js")
    if not os.path.exists(server_js):
        print(f"❌ flux_lsp: server.js not found at {server_js}")
        return

    RUNNING = True
    print(f"🚀 flux_lsp: starting LSP server on port {LSP_PORT}...")
    try:
        PROCESS = subprocess.Popen(
            ["node", server_js, "--stdio"],
            cwd=LSP_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "FLUX_LSP_PORT": str(LSP_PORT)}
        )
        print(f"✅ flux_lsp: LSP server running (pid {PROCESS.pid})")
        PROCESS.wait()
    except Exception as e:
        print(f"❌ flux_lsp: server error: {e}")
    finally:
        RUNNING = False

def start(config=None):
    global PROCESS, THREAD, RUNNING
    if RUNNING and PROCESS and PROCESS.poll() is None:
        return {"status": "already_running", "pid": PROCESS.pid, "port": LSP_PORT}

    if config:
        if "lsp_path" in config: LSP_PATH = config["lsp_path"]
        if "port" in config: LSP_PORT = config["port"]

    if not _build_if_needed():
        return {"status": "build_failed"}

    THREAD = threading.Thread(target=_run_server, daemon=True)
    THREAD.start()
    return {"status": "starting", "port": LSP_PORT, "lsp_path": LSP_PATH}

def stop():
    global PROCESS, RUNNING
    if PROCESS:
        print(f"🛑 flux_lsp: stopping LSP server (pid {PROCESS.pid})...")
        PROCESS.terminate()
        try:
            PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            PROCESS.kill()
            PROCESS.wait()
        PROCESS = None
    RUNNING = False
    return {"status": "stopped"}

def status():
    global PROCESS, RUNNING
    alive = PROCESS is not None and PROCESS.poll() is None
    return {
        "running": alive,
        "port": LSP_PORT,
        "lsp_path": LSP_PATH,
        "pid": PROCESS.pid if PROCESS else None,
        "lsp_modules_installed": os.path.exists(os.path.join(LSP_PATH, "node_modules"))
    }