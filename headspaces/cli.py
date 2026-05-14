"""Headspaces CLI — list, status, start, stop. Drop-in for starter-shell CLI."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

def run(args):
    import headspaces
    if not args or args[0] == "list":
        spaces = headspaces.list_headspaces()
        statuses = headspaces.status_all()
        print(f"\n  Headspaces ({len(spaces)}):")
        for s in spaces:
            st = statuses.get(s, {})
            run = '✅' if st.get('running') else '⬜'
            mi = headspaces.module_info(s)
            print(f"    {run} {s:15s} {mi.get('desc','')[:55]}")
    elif args[0] == "start":
        mod = headspaces.get(args[1]) if len(args) > 1 else None
        if mod and hasattr(mod, 'start'):
            print(f"  Starting {args[1]}...")
            mod.start()
        else:
            print(f"  Headspace '{args[1]}' not found or has no start()")
    elif args[0] == "stop":
        mod = headspaces.get(args[1]) if len(args) > 1 else None
        if mod and hasattr(mod, 'stop'):
            mod.stop()
            print(f"  Stopped {args[1]}")

if __name__ == "__main__":
    run(sys.argv[1:])
