"""Discord headspace — connect this shell to Discord."""
import os
try:
    import discord
    HAS_DISCORD = True
except:
    HAS_DISCORD = False

TOKEN = os.environ.get("DISCORD_TOKEN", "")
CLIENT = None

class ShellClient(discord.Client):
    async def on_ready(self):
        print(f"🐚 Shell connected to Discord as {self.user}")
    async def on_message(self, message):
        if message.author == self.user: return
        from agent import Agent
        a = Agent("discord")
        a.walk("fleet_health")

def start():
    global CLIENT
    if not TOKEN: return {"error": "DISCORD_TOKEN not set"}
    if not HAS_DISCORD: return {"error": "discord.py not installed"}
    CLIENT = ShellClient(intents=discord.Intents.default())
    CLIENT.run(TOKEN)
    return {"status": "running"}

def stop():
    global CLIENT
    if CLIENT: CLIENT.close()
    return {"status": "stopped"}

def status():
    return {"running": CLIENT is not None and CLIENT.is_ready(), "token_set": bool(TOKEN)}
