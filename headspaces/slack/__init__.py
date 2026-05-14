"""Slack headspace — connect this shell to Slack."""
import os, json, urllib.request, time
TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
VERIFICATION = os.environ.get("SLACK_VERIFICATION_TOKEN", "")
RUNNING = False

def handle_event(event):
    """Process a Slack event and file it as a PLATO tile."""
    from plato import PlatoClient
    client = PlatoClient()
    text = event.get("event", {}).get("text", "")
    channel = event.get("event", {}).get("channel", "")
    user = event.get("event", {}).get("user", "")
    if text:
        client.submit_tile("slack-inbox",
            f"Slack message from {user} in {channel}",
            text[:500])
    return {"status": "ok"}

def start():
    global RUNNING
    if not TOKEN: return {"error": "SLACK_BOT_TOKEN not set"}
    RUNNING = True
    return {"status": "running"}

def stop():
    global RUNNING
    RUNNING = False
    return {"status": "stopped"}

def status():
    return {"running": RUNNING, "token_set": bool(TOKEN)}
