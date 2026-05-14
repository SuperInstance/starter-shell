"""Perception-action cycle headspace. Sense → act → re-perceive on PLATO data."""
import time, threading, json
from plato import PlatoClient

RUNNING = False
INTERVAL = 60  # seconds between cycles
THREAD = None

def perceive(room="forge"):
    """Sense the current state of a PLATO room."""
    try:
        client = PlatoClient()
        data = client.get_room(room)
        tiles = data.get("tiles", [])
        return {"room": room, "tiles": len(tiles), "status": "ok"}
    except Exception as e:
        return {"room": room, "tiles": 0, "status": str(e)[:40]}

def act(perception):
    """File an action tile based on what was perceived."""
    try:
        client = PlatoClient()
        client.submit_tile("perception-actions",
            f"Perception cycle at {time.ctime()}",
            f"Sensed {perception.get('tiles',0)} tiles in {perception.get('room','?')}")
        return True
    except:
        return False

def _loop():
    global RUNNING
    while RUNNING:
        p = perceive()
        act(p)
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

# Ported from constraint-inference (archived repo)
# Maps decision deltas to constraint parameter adjustments

DECISION_ORDER = ['CONSTRAINED', 'STABLE', 'DECIDED', 'EMERGENCE']

def _map_delta(captain_decision, user_decision):
    """Map a decision override to the constraint parameter to adjust."""
    if captain_decision not in DECISION_ORDER or user_decision not in DECISION_ORDER:
        return None
    c_idx = DECISION_ORDER.index(captain_decision)
    u_idx = DECISION_ORDER.index(user_decision)
    if c_idx == u_idx:
        return None
    direction = 'tighten' if u_idx < c_idx else 'loosen'
    return {"constraint_shift": abs(c_idx - u_idx), "direction": direction}
