"""Headspaces registry — discover, status for all headspaces. Graceful import handling."""
import os, importlib, logging

def list_headspaces():
    spaces = []
    for item in sorted(os.listdir(os.path.dirname(__file__))):
        init = os.path.join(os.path.dirname(__file__), item, "__init__.py")
        if os.path.isfile(init) and item != "__pycache__":
            spaces.append(item)
    return spaces

def module_info(name):
    import json
    meta = os.path.join(os.path.dirname(__file__), name, "module.json")
    if os.path.isfile(meta):
        with open(meta) as f: return json.load(f)
    return {"name": name, "desc": ""}

def get(name):
    try:
        return importlib.import_module(f"headspaces.{name}")
    except Exception as e:
        return None

def status_all():
    results = {}
    for name in list_headspaces():
        mod = get(name)
        if mod is None:
            results[name] = {"error": "import failed", "running": False}
        elif hasattr(mod, 'status'):
            try:
                results[name] = mod.status()
            except Exception as e:
                results[name] = {"error": str(e)[:50], "running": False}
        else:
            results[name] = {"running": False}
    return results
