# Fleet Wiring Manifest

Every repo is independently usable. Every repo is designed to connect.

A future engineer picks the repos they need and glues them together through PLATO.

---

## Connection Points

| Repo | Connects via | To | Purpose |
|------|-------------|-----|---------|
| starter-shell | PLATO_URL env var | plato.purplepincher.org | Bootstrap, hardware detection, agent loop |
| starter-shell | pip install | plato-sdk | File tiles, search rooms |
| starter-shell | cargo install | keel | Fleet management CLI |
| starter-shell | git clone | vessel-room-navigator | 3D room viewer |
| starter-shell | headspaces/ | telegram, discord, slack, etc | Service integration |
| keel | --server flag | plato.purplepincher.org | Fleet status, topology |
| keel | PLATO tiles | plato-sdk | Knowledge sync |
| plato-sdk | HTTP API | plato.purplepincher.org | Room CRUD, tile search |
| forgemaster | HTTP | plato.purplepincher.org | File benchmark results |
| flux-vm | stdio | forgemaster | Execute compiled constraints |
| terrain | file I/O | vessel-room-navigator | MUD room → 3D scene |
| fleet-scribe | PLATO tiles | plato-sdk | Delta detection → tile filing |
| gh-dungeons | --plato-url | plato.purplepincher.org | Knowledge rooms → dungeon levels |
| fleet-math-c | C API | Any C/Rust project | SIMD constraint operations |

## Glue Patterns

### Pattern A: PLATO as Hub
```
App → plato-sdk → PLATO → plato-sdk → Other App
```
PLATO is the shared memory. Every repo reads and writes tiles.

### Pattern B: CLI Pipeline
```
starter-shell → keel → flux-vm → forgemaster
```
Each CLI tool pipes to the next. stdout is JSON.

### Pattern C: Merge (Git-Based)
```
fork gh-dungeons → add PLATO bridge → upstream merge
```
Open source collaboration pattern. Fork, extend, merge back.

## How to Add a New Repo

1. Create the repo with a README (what it is, one paragraph)
2. Add a module.json to starter-shell/modules/
3. Document the PLATO connection point (URL, tile format)
4. Add to this wiring manifest
5. Push
