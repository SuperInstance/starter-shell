"""Heartbeat headspace — scheduled agent loop."""
import time, threading, os

INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", "300"))
RUNNING = False
THREAD = None

def _loop():
    global RUNNING
    while RUNNING:
        from hardware import detect
        hw = detect()
        print(f"❤️  Heartbeat: {hw['platform']} | {hw['cores']} cores")
        # Try PLATO sync
        try:
            from plato import PlatoClient
            c = PlatoClient()
            c.submit_tile("shell-health", "heartbeat", 
                f"Alive at {time.ctime()}: {hw['platform']} {hw['cores']}c {hw['memory_mb']}MB")
        except: pass
        time.sleep(INTERVAL)

def start():
    global RUNNING, THREAD
    RUNNING = True
    THREAD = threading.Thread(target=_loop, daemon=True)
    THREAD.start()
    return {"status": "running", "interval": INTERVAL}

def stop():
    global RUNNING
    RUNNING = False
    return {"status": "stopped"}

def status():
    return {"running": RUNNING, "interval": INTERVAL}
