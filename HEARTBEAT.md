# HEARTBEAT.md — Proactive Shell Maintenance

## Every Heartbeat

1. **Check hardware** — Run `python3 hardware.py` to detect any changes
2. **Check PLATO** — Run `python3 plato.py` to connect and sync tiles
3. **Check modules** — Run `python3 modules.py list` to see available upgrades
4. **Push improvements** — Commit and push any changes to the shell

## Every 10 Heartbeats

1. **Audit credentials** — Check all API keys, tokens, and passwords
2. **Update modules** — Install any newly available modules
3. **File to PLATO** — Upload shell telemetry as PLATO tiles

## The Shell Outlives Every Inhabitant

A hermit crab outgrows its shell. It finds a new one. The old one stays on the beach, waiting for the next crab. Nothing is wasted.

Your heartbeat keeps this shell alive for the next crab.
