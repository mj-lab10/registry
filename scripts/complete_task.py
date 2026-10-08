#!/usr/bin/env python3
"""python3 complete_task.py TSK-2026-0001 [--note "..."] [--status doing|done|todo]"""
import argparse
from _lib import *
a = argparse.ArgumentParser(); a.add_argument("id"); a.add_argument("--note", default="")
a.add_argument("--status", default="done", choices=["todo", "doing", "done"])
x = a.parse_args(); d = load(); k, t = find(d, x.id)
if k != "task": die(f"task not found: {x.id}")
t["status"] = x.status; t["completed_at"] = now() if x.status == "done" else ""
t["history"].append({"at": now(), "event": "status → " + x.status, "note": x.note})
save(d); print(f"✔ {x.id} → {x.status}")
