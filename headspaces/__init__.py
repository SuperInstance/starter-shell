"""Headspaces registry — discover, start, stop, status for all headspaces."""
import os, importlib

def list_headspaces():
    spaces = []
    for item in os.listdir(os.path.dirname(__file__)):
        init = os.path.join(os.path.dirname(__file__), item, "__init__.py")
        if os.path.isfile(init) and item != "__pycache__":
            spaces.append(item)
    return sorted(spaces)

def module_info(name):
    import json
    meta = os.path.join(os.path.dirname(__file__), name, "module.json")
    if os.path.isfile(meta):
        with open(meta) as f: return json.load(f)
    return {"name": name}

def get(name):
    return importlib.import_module(f"headspaces.{name}")

def status_all():
    return {name: get(name).status() for name in list_headspaces()}
