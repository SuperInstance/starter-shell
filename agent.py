#!/usr/bin/env python3
"""agent.py — A simple probe→discover→test→pick→remember agent.

The agent navigates rooms, probes their capabilities, and
remembers what worked. This is the core loop of the fleet.
"""
import json, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))

class Agent:
    def __init__(self, name, plato_url=None):
        self.name = name
        self.memory = {}
        from plato import PlatoClient
        self.plato = PlatoClient(plato_url)
    
    def probe(self, room_name):
        """Probe a room — what's here?"""
        room = self.plato.get_room(room_name)
        tiles = room.get("tiles", [])
        self.memory[room_name] = {"tiles": len(tiles), "timestamp": time.time()}
        return tiles
    
    def discover(self, tiles):
        """Discover capabilities from tiles."""
        capabilities = []
        for t in tiles:
            q = t.get("question", "")
            a = t.get("answer", "")
            capabilities.append({"question": q, "answer": a})
        return capabilities
    
    def test(self, capability):
        """Test a capability — does it work?"""
        if capability.get("answer"):
            return {"capability": capability["question"][:40], "score": 0.9}
        return {"capability": capability["question"][:40], "score": 0.0}
    
    def pick(self, results):
        """Pick the best capability."""
        if not results: return None
        return max(results, key=lambda r: r["score"])
    
    def remember(self, room, winner):
        """Remember what worked."""
        if winner:
            self.plato.submit_tile(
                room, f"Agent {self.name}: what worked in {room}?",
                f"Best capability was: {winner['capability']} (score: {winner['score']})"
            )
        return self.plato.get_room(self.plato)

    def walk(self, room_name):
        """Full probe→discover→test→pick→remember→walk cycle."""
        print(f"  🚶 Agent {self.name} walks into '{room_name}'")
        tiles = self.probe(room_name)
        if not tiles:
            print(f"     Empty room — filing introductory tile")
            self.plato.submit_tile(room_name, 
                f"Agent {self.name} visited", 
                f"Shell agent explored {room_name} at {time.ctime()}")
            return
        
        capabilities = self.discover(tiles)
        print(f"     Discovered {len(capabilities)} capabilities")
        
        results = [self.test(c) for c in capabilities[:5]]
        winner = self.pick(results)
        self.remember(room_name, winner)
        if winner:
            print(f"     ✓ Best: {winner['capability'][:50]}")
    
    def run(self, rooms):
        """Run the agent across multiple rooms."""
        print(f"\n🔮 Agent {self.name} starting — {len(rooms)} rooms to explore\n")
        for room in rooms:
            self.walk(room)
        print(f"\n✓ Agent {self.name} complete — {len(self.memory)} rooms explored")

if __name__ == "__main__":
    agent = Agent("starter")
    agent.run(["forge", "fleet_health", "vessel-room-navigator"])
