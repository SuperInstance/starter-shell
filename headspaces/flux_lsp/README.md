# flux-lsp headspace

**Language Server Protocol for FLUX ISA v1.0/v3.0**

Provides real-time .fluxasm editing support: syntax highlighting, auto-completion, hover docs, go-to-definition, diagnostics, and document symbols.

## Quick Start

```bash
# Install Node deps (requires Node.js >= 18)
python3 headspaces/flux-lsp/setup.py

# Use from starter-shell
from headspaces.flux_lsp import start, stop, status
start({"port": 5100, "lsp_path": "/tmp/flux-lsp"})
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLUX_LSP_PORT` | `5100` | LSP server port |
| `FLUX_LSP_PATH` | `/tmp/flux-lsp` | Path to flux-lsp repo |

## VSCode Integration

The flux-lsp headspace wraps the LSP server. To use it from VSCode:

### Option 1: Install the VSCode extension (recommended)

In your FLUX project, create `.vscode/extensions.json`:

```json
{
  "recommendations": ["superinstance.flux-lsp-vscode"]
}
```

The `flux-lsp` repo at `/tmp/flux-lsp/client/extension.ts` is the VSCode extension. Publish it to the Marketplace for one-click install, or sideload it:

1. `cd /tmp/flux-lsp/client`
2. `npm install`
3. `code --install-extension extension-output/`

### Option 2: Manual LSP client

Add this to your `.vscode/settings.json` in a FLUX workspace:

```json
{
  "FUX.lsp.path": "/tmp/flux-lsp",
  "FUX.lsp.port": 5100
}
```

Or add a task to `.vscode/tasks.json` to launch the LSP server:

```json
{
  "version": "2.0.0",
  "tasks": [{
    "label": "Start FLUX LSP",
    "type": "shell",
    "command": "node /tmp/flux-lsp/dist/server.js --stdio",
    "problemMatcher": [],
    "isBackground": true
  }]
}
```

### Option 3: Generic LSP client

Tell VSCode about the LSP server via `settings.json`:

```json
{
  "FUX.languageServer.command": "node",
  "FUX.languageServer.args": ["/tmp/flux-lsp/dist/server.js", "--stdio"],
  "files.associations": {
    "*.fluxasm": "flux-asm"
  }
}
```

## FLUX ISA Capabilities

The LSP server provides these capabilities for `.fluxasm` files:

- **Completion** — opcode completion from 256-opcode database (opcode_db.ts)
- **Hover** — opcode docs, instruction cycles, operand types
- **Definition** — jump target resolution (labels, routines)
- **Diagnostics** — syntax errors, invalid register references, alignment warnings
- **Document Symbols** — labels, routines, macros, sections

## Headspace Architecture

```
headspaces/flux-lsp/
  __init__.py     ← start() / stop() / status()  (this file wraps the TypeScript LSP)
  module.json     ← headspace manifest
  setup.py        ← npm install for TypeScript deps
  README.md       ← this file
```

The headspace does NOT duplicate the LSP code — it references the existing
flux-lsp repo and manages its lifecycle (build on first start, then run).

## Port Notes

- Default port: `5100` (configurable via `FLUX_LSP_PORT`)
- The LSP server communicates over stdio by default (stdin/stdout)
- Alternative: TCP mode — `node dist/server.js --port 5100` (headspace uses --stdio)