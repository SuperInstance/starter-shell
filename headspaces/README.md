# Headspaces — Drop-in Skill Modules

A headspace is a skill module for the shell. It adds a capability — Telegram connectivity, Discord bots, heartbeat loops, whatever you need.

Headspaces are designed to be interchangeable and composable. They're the OpenClaw ecosystem's skills, ported to work directly with the starter shell.

## Available Headspaces

Headspaces are not pre-installed. Add them as you need them:

```bash
# Add a Telegram headspace
cp /path/to/telegram-headspace.py headspaces/telegram/
python3 headspaces/telegram/setup.py

# Add a Discord headspace  
cp /path/to/discord-headspace.py headspaces/discord/
python3 headspaces/discord/setup.py
```

## Creating a Headspace

Every headspace needs:

1. A directory in `headspaces/`
2. A `module.json` describing it
3. A `setup.py` that installs dependencies
4. A main file that exports `start()`, `stop()`, and `status()`

```python
# headspaces/example/__init__.py
def start(config): pass
def stop(): pass
def status(): return {"running": False}
```

## Porting from OpenClaw

As OpenClaw releases new skills, map them to headspaces:

1. Clone the OpenClaw skill
2. Extract the functional core (what does it actually do?)
3. Create a headspace wrapper that exposes start/stop/status
4. The headspace is now shell-compatible

OpenClaw's ecosystem IS our ecosystem. We port everything useful.
