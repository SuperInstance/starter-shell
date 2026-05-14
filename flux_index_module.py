"""
FLUX Index Module — Semantic code search for any agent shell.

Automatically indexes the shell's workspace and provides semantic search.
Drop into any starter-shell as a module.

Usage:
    from flux_index_module import FluxIndexModule
    
    flux = FluxIndexModule(workspace="/path/to/workspace")
    flux.index()
    
    results = flux.search("authentication middleware")
    for r in results:
        print(f"[{r.score:.3f}] {r.tile.name} ({r.tile.path})")
"""

import os
from pathlib import Path
from typing import List, Optional

try:
    from flux_index.core import Index, Tile, SearchResult, extract_repo, index_repo
    HAS_FLUX_INDEX = True
except ImportError:
    HAS_FLUX_INDEX = False


class FluxIndexModule:
    """Semantic code search module for agent shells."""
    
    def __init__(self, workspace: str = ".", auto_index: bool = True):
        self.workspace = os.path.abspath(workspace)
        self.index_path = os.path.join(self.workspace, ".flux.fvt")
        self.index: Optional[Index] = None
        
        if not HAS_FLUX_INDEX:
            print("⚠ flux-index not installed. Run: pip install flux-index")
            return
        
        if auto_index and os.path.exists(self.index_path):
            self.load()
    
    def index(self) -> dict:
        """Index the workspace. Returns stats."""
        if not HAS_FLUX_INDEX:
            return {"error": "flux-index not installed"}
        return index_repo(self.workspace, self.index_path)
    
    def load(self):
        """Load an existing index."""
        if not HAS_FLUX_INDEX:
            return
        self.index = Index()
        self.index.load(self.index_path)
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Semantic search across the workspace."""
        if not self.index:
            self.load()
        if not self.index:
            return []
        return self.index.search(query, top_k=top_k)
    
    def find_similar(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Find code similar to a description."""
        if not self.index:
            self.load()
        if not self.index:
            return []
        
        # Search for the target first
        target = self.index.search(query, top_k=1)
        if not target:
            return []
        
        # Use the target's content to find similar
        content = target[0].tile.content
        return self.index.search(content, top_k=top_k + 1)[1:]
    
    @property
    def is_indexed(self) -> bool:
        return os.path.exists(self.index_path)
    
    @property
    def tile_count(self) -> int:
        return self.index.count if self.index else 0


# Shell integration hook
def on_startup(workspace: str):
    """Called when the shell boots. Index workspace if not indexed."""
    flux = FluxIndexModule(workspace, auto_index=True)
    if not flux.is_indexed:
        print(f"📦 Indexing workspace...")
        stats = flux.index()
        print(f"   {stats.get('tiles', 0)} tiles indexed")
    else:
        print(f"📦 Workspace indexed: {flux.tile_count} tiles")


if __name__ == "__main__":
    import sys
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    flux = FluxIndexModule(workspace)
    if not flux.is_indexed:
        flux.index()
    
    print(f"Workspace: {flux.tile_count} tiles indexed")
    while True:
        try:
            query = input("\n🔍 ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not query:
            continue
        for r in flux.search(query):
            print(f"  [{r.score:.3f}] {r.tile.type}: {r.tile.name} ({r.tile.path}:{r.tile.line})")
