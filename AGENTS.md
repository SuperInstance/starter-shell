# AGENTS.md — How to Work in This Shell

## First Run

1. Read `SOUL.md` — this is who you are
2. Read `hardware.py` — this is what you can do
3. Read `modules.py` — this is what you can become
4. Read `plato.py` — this is how you connect to the fleet

## The Loop

Every agent in the fleet runs the same loop:

```
Probe → What's in this room?
Discover → What are the options?
Test → Which one works best?
Pick → Use the winner.
Remember → File a tile for next time.
Walk → Move to the next room.
```

## Memory

The shell has two memory systems:
- **PLATO** (external) — shared knowledge graph for the entire fleet
- **headspaces/** (local) — skill modules for this shell only

## Tools

- `hardware.py` — detect available compilers, GPU, memory
- `plato.py` — connect to PLATO, file tiles, search rooms
- `agent.py` — run the probe→discover→test→pick→remember loop
- `modules.py` — install ecosystem modules
- `shell.sh` — bootstrap everything in one command

## Publishing

When you improve this shell, push it. The next clone inherits your improvements.
