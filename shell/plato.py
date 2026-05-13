#!/usr/bin/env python3
"""plato.py — Connect to PLATO from this shell.

Creates a room for this shell, files hardware info as tiles,
and provides the agent interface.
"""
import json, urllib.request, os, sys

PLATO_URL = os.environ.get("PLATO_URL", "https://plato.purplepincher.org")
SHELL_NAME = os.environ.get("SHELL_NAME", "starter-shell")

class PlatoClient:
    def __init__(self, url=None):
        self.url = url or PLATO_URL
    
    def create_room(self, name):
        """Create a PLATO room for this shell."""
        try:
            req = urllib.request.Request(f"{self.url}/room/{name}", 
                data=b"{}", headers={"Content-Type": "application/json"},
                method="PUT")
            urllib.request.urlopen(req, timeout=5)
            return True
        except: return False
    
    def submit_tile(self, room, question, answer):
        """File a knowledge tile."""
        data = json.dumps({"question": question, "answer": answer, 
                          "source": SHELL_NAME, "confidence": 0.7})
        req = urllib.request.Request(f"{self.url}/room/{room}/submit",
            data=data.encode(), headers={"Content-Type": "application/json"})
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}
    
    def get_room(self, name):
        """Get room contents."""
        try:
            resp = urllib.request.urlopen(f"{self.url}/room/{name}", timeout=5)
            return json.loads(resp.read())
        except: return {"tiles": [], "tile_count": 0}
    
    def probe_rooms(self):
        """List all rooms on the server."""
        try:
            resp = urllib.request.urlopen(f"{self.url}/rooms", timeout=5)
            return json.loads(resp.read())
        except: return {}

def bootstrap(hardware_info):
    """Create rooms and file hardware info."""
    client = PlatoClient()
    
    # Create shell room
    client.create_room(SHELL_NAME)
    client.submit_tile(SHELL_NAME, "What is this shell?",
        f"A starter shell running on {hardware_info['platform']} with "
        f"{hardware_info['cores']} cores and {hardware_info['memory_mb']}MB RAM")
    
    # File hardware capabilities
    for lang in hardware_info.get("languages", []):
        client.submit_tile(SHELL_NAME, f"Does this shell support {lang}?",
            f"Yes. {lang.upper()} available on this hardware.")
    
    return client

if __name__ == "__main__":
    from hardware import detect
    hw = detect()
    client = bootstrap(hw)
    print(f"🔮 Shell '{SHELL_NAME}' bootstrapped on PLATO at {client.url}")
