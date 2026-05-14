"""flux-lsp headspace setup — install Node dependencies for the TypeScript LSP."""
import os, subprocess, sys

def run(cmd, cwd=None):
    print(f"⚙️  Running: {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.stdout: print(r.stdout)
    if r.returncode != 0:
        print(f"❌ Failed: {r.stderr[:500]}")
        return False
    return True

def check_node():
    try:
        v = subprocess.run(["node", "--version"], capture_output=True, text=True)
        major = int(v.stdout.strip().lstrip("v").split(".")[0])
        return major >= 18
    except:
        return False

def install(env=None):
    lsp_path = os.environ.get("FLUX_LSP_PATH", "/tmp/flux-lsp")
    print(f"📦 flux-lsp headspace setup")
    if not check_node():
        print("❌ Node.js >= 18 required")
        return False
    if not os.path.exists(lsp_path):
        print(f"⚠️  flux-lsp repo not found at {lsp_path}")
        print("   Clone it with: git clone https://github.com/SuperInstance/flux-lsp.git")
        return False
    ok = run(["npm", "install"], cwd=lsp_path)
    if ok:
        print("✅ flux-lsp headspace ready")
    return ok

if __name__ == "__main__":
    install()