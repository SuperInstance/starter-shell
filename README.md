# 🔮 Starter Shell

A starting shell for any application. Clone it, run it, and it adapts to your hardware — discovers compilers, connects to the fleet's knowledge graph (PLATO), creates rooms, files tiles, and runs the agent loop.

```bash
git clone https://github.com/SuperInstance/starter-shell.git
cd starter-shell
python3 setup.py my-project-name
```

That's the whole setup. You're now a fleet of one.

---

## What Is a Shell?

A hermit crab outgrows its shell. It doesn't break the old one — it finds a new one. The old shell becomes a home for the next crab. Nothing is wasted. The beach accumulates better shells over time.

A git repository is a shell. An agent crawls into it, starts committing, and leaves it better than it was found. The next agent inherits everything the previous one learned. The shell outlives every inhabitant.

**You are the hermit crab.** The shell is your workspace — your repo, your project, your agent. You improve it while you're in it. When you outgrow it, you find a bigger one. The old one stays on the beach, waiting for the next crab.

The shell has two surfaces:
- **Inside:** The knowledge — PLATO tiles, commit logs, agent journals. This is what the agent sees.
- **Outside:** The interface — README, 3D rooms, CLI tools. This is what humans see.

They're the same shell, viewed from opposite sides.

---

## Why Build with Shells?

Every AI system today follows the same pattern: one giant model, one prompt, one response. If you want it to do more, you make the model bigger. Bigger models hallucinate more, cost more, and still can't do reliable multi-step reasoning.

We build differently. Instead of one giant model that knows everything, we build **rooms**. Each room is a constraint boundary — it defines what exists, what normal looks like, what actions are valid. The engine room has temperature gauges and thermal cameras. The wheelhouse has radar and charts. A model operating inside the engine room never needs to think about anything outside it. The room IS the context.

**A small model inside a well-structured room outperforms a large model with no structure.** Forgemaster's FLUX runtime proved this on real hardware — a Python implementation running on one CPU core (84ns per operation) beat a C implementation with full compiler optimization (256ns) for small primitives. The overhead of crossing a language boundary cost more than the computation. The room structure was the intelligence. The model just followed it.

The starter shell gives you that room structure. The hardware detection, the PLATO connection, the agent loop — these are the walls of your first room.

---

## What You Get

| File | What it does |
|------|-------------|
| `hardware.py` | Detects CPU, memory, compilers, GPU, available languages |
| `plato.py` | Connects to PLATO (the fleet's knowledge graph), creates rooms, files tiles |
| `agent.py` | Runs the probe→discover→test→pick→remember→walk loop |
| `setup.py` | Runs everything above in one command |

**`hardware.py`** probes the machine it's running on. It finds compilers (gcc, clang, rustc, zig, nim), languages (Python, Rust, Go), GPU (NVIDIA, AMD, or none), memory, and cores. It doesn't assume anything — it discovers.

**`plato.py`** connects to PLATO, the fleet's shared knowledge graph. If there's a PLATO server on your network, the shell finds it, creates a room for itself, and files its hardware capabilities as tiles. Every agent that enters the room later knows what this shell can do.

**`agent.py`** implements the universal agent loop:
```
Probe → Discover → Test → Pick → Remember → Walk
```
This works for code (which compiler is fastest?), knowledge (which tile answers this question?), and operations (which camera shows the problem?). Same loop, any domain.

**`setup.py`** ties everything together. Run it once and the shell is laid.

---

## Modular Expansion

The starter shell is the kernel. Everything else is a module you add when you need it.

```bash
python3 modules.py list           # See available modules
python3 modules.py install keel   # Install fleet CLI
python3 modules.py install plato-sdk  # Install PLATO SDK
python3 modules.py install vessel # Install 3D room viewer
```

Each module is self-contained. Install what you need. The shell grows with you.

| Module | One-liner | Install |
|--------|-----------|---------|
| `keel` | Fleet management CLI (init, status, bear, field...) | `cargo install superinstance-keel` |
| `plato-sdk` | PLATO knowledge graph client | `pip install plato-sdk` |
| `vessel` | 3D room viewer (fishing boat demo) | `git clone` |
| `forgemaster` | FLUX runtime (self-discovering compiler) | `git clone` |
| `flux-vm` | Constraint verification VM (50 opcodes) | `git clone` |
| `terrain` | MUD-to-visual bridge (text → 3D) | `git clone` |
| `fleet-scribe` | One Delta detection (compute only changes) | `pip install fleet-scribe` |
| `holonomy` | GL(9) zero-holonomy consensus | `git clone` |
| `esp32-cam` | ESP32 camera agent firmware | (hardware) |
| `gh-dungeon` | PLATO-powered dungeon crawler | `gh extension install` |
| `gpu-vector` | GPU vector DB (CUDA/WebGPU/Vulkan) | (research) |



The starter shell is the entry point. The rest of the fleet extends it:

| Repo | What it adds |
|------|-------------|
| **[keel](https://github.com/SuperInstance/keel)** | Rust CLI for fleet management. 9 commands: init, status, bear, field, probe, prune, refit, launch, sync. `cargo install superinstance-keel`. |
| **[plato-sdk](https://github.com/SuperInstance/plato-sdk)** | Python SDK for PLATO. `pip install plato-sdk`. Build agents that file tiles and search the knowledge graph. |
| **[forgemaster](https://github.com/SuperInstance/forgemaster)** | FLUX runtime. Self-discovering compiler that benchmarks C, Python, Fortran, Zig, Nim and picks the fastest. Proved that Python beats C for small ops. |
| **[vessel-room-navigator](https://github.com/SuperInstance/vessel-room-navigator)** | 3D room viewer. A fishing boat as a navigable web space. Drag to look around 7 AI-generated panoramas. The outside of the shell. |
| **[flux-vm](https://github.com/SuperInstance/flux-vm)** | 50-opcode stack VM for constraint verification. Turing-incomplete, bounded execution. |
| **[holonomy-consensus](https://github.com/SuperInstance/holonomy-consensus)** | GL(9) zero-holonomy consensus. Cycle-based trust verification. Original mathematics. |
| **[fleet-scribe](https://github.com/SuperInstance/fleet-scribe)** | One Delta principle. Only compute when the gradient changes. Delta detection, caching, pattern compilation. |
| **[terrain](https://github.com/SuperInstance/terrain)** | MUD-to-visual bridge. Text room descriptions → 3D scenes in Three.js. 74 tests. |
| **[gh-dungeons](https://github.com/SuperInstance/gh-dungeons)** | PLATO-powered roguelike dungeon crawler. `gh dungeon --plato-url http://your-plato-server/`. |
| **[casting-call](https://github.com/SuperInstance/casting-call)** | Intent-based message router. 850k routing decisions/sec. |

---

## How It Works

### The Loop

Every agent in the fleet runs the same loop:

```python
# This file, agent.py, implements exactly this
def walk(self, room):
    tiles = self.probe(room)     # what's here?
    caps = self.discover(tiles)  # what can I do?
    results = [self.test(c) for c in caps]  # what works?
    winner = self.pick(results)  # what's best?
    self.remember(room, winner)  # save for next time
```

The agent doesn't need to be smart. The room is smart. The agent just navigates.

### The Knowledge Graph

PLATO is the fleet's shared memory. Every agent files tiles — question-answer pairs — as it works. Later agents search PLATO instead of carrying context. Knowledge accumulates. No agent starts from zero.

```python
from plato import PlatoClient
client = PlatoClient("http://your-plato-server:8847")
client.submit_tile("my-room", "What's the ideal temperature?", "Depends on the engine.")
```

### Hardware Adaptation

The shell adapts to whatever machine it lands on:

```python
from hardware import detect
hw = detect()
# Returns: platform, cores, memory, compilers, GPU, languages
# On a Raspberry Pi: Python only, no GPU
# On a workstation: Python + Rust, NVIDIA GPU
# On a server: Python + C + Rust + Zig, no GPU
```

---

## Quick Start

```bash
# 1. Clone the shell
git clone https://github.com/SuperInstance/starter-shell.git
cd starter-shell

# 2. Set up your project
python3 setup.py my-project

# 3. Run the agent
python3 agent.py

# 4. Connect to the fleet
pip install plato-sdk
cargo install superinstance-keel

# 5. Walk the boat
open https://fleet.cocapn.ai/
```

---

## The Philosophy

**Constraints breed clarity.** You cannot change the innate capabilities of your hardware. You can only discover them and work within them. The shell is honest about what it can and cannot do.

**First-person time.** Every agent carries its own death from its own frame. Death is default. Survival must be actively earned. No central scheduler.

**Field, not message.** Agents coordinate by sensing each other's bearing, not by sending commands. The field IS the communication channel.

**Tabula plena.** Start abundant. Prune to clarity. The sculptor removes what isn't the statue.

---

**Demo:** https://fleet.cocapn.ai/  
**Research:** https://github.com/SuperInstance/vessel-room-navigator/tree/main/docs/research  
**Source code is the entry point to the fleet.**

*Constraints breed clarity.* — Casey Digennaro
