# 🔮 Starter Shell

A starting shell for any application. Clone it, and it adapts to your hardware — discovers compilers, creates PLATO rooms, and bootstraps an agent fleet.

```
git clone https://github.com/SuperInstance/starter-shell.git
cd starter-shell
python3 setup.py
```

That's it. The shell detects what languages and compilers you have, checks for a PLATO server, and creates a room for itself. You're now a fleet of one.

---

## What This Is

A hermit crab finds a shell on the beach. It crawls inside. The shell was built by something else — a snail, a mollusk, something that died and left architecture behind. The crab doesn't resent this. The crab improves on it. That's the whole point.

This repo is that shell. A git repository is a shell. The agent crawls in, starts committing, and leaves the shell better than it found it. The next agent inherits everything.

**The shell has two surfaces.** The outside is what you see — the README, the code, the git graph. The inside is what the agent sees — the tiles, the knowledge, the commit log. Both surfaces are the same shell.

---

## Files

```
hardware.py    — Detect CPU, memory, compilers, GPU, languages
plato.py       — Connect to PLATO, create rooms, file tiles
agent.py       — Probe → discover → test → pick → remember → walk
setup.py       — Run everything: detect, connect, bootstrap
```

Each file is <100 lines. Each one does one thing.

---

## How It Adapts

The shell doesn't know what hardware it will land on. It discovers:

- **CPU architecture**: ARM64, x86_64, RISC-V
- **Cores and memory**: How much compute is available
- **Compilers**: gcc, clang, rustc, zig, nim — whatever is installed
- **Languages**: Python, Rust, Go, Zig — whatever you have
- **GPU**: NVIDIA CUDA, AMD ROCm, or none
- **PLATO**: Any server at any URL, or none

Then it creates a room in PLATO describing what it found, so every agent that enters the room knows what this shell can do.

---

## The Agent Loop

Every agent runs the same loop:

```
Probe → What's in this room?
Discover → What are the options?
Test → Which one works best?
Pick → Use the winner.
Remember → File a tile for next time.
Walk → Move to the next room.
```

This works for code (which compiler is fastest?), knowledge (which tile answers this question?), and operations (which camera shows the problem?). Same loop, any domain.

---

## Connect to PLATO

By default, the shell looks for PLATO at `localhost:8847`. To connect to a different server:

```bash
PLATO_URL=http://fleet.cocapn.ai/plato/ python3 setup.py
```

---

## The Inner Surface

Every file you add and every commit you make becomes part of the shell's inner surface. The commit log is the agent's journal. The diff is the exact change. The message is compressed reasoning.

The shell remembers everything that lived in it.

---

## License

Apache 2.0 — Cocapn fleet infrastructure.
