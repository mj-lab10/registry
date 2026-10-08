#!/usr/bin/env python3
"""python3 add_note.py "Title" [--bn ..] [--body ..] [--category ..] [--tags a,b] [--pinned]"""
import argparse
from _lib import *
a = argparse.ArgumentParser()
a.add_argument("title"); a.add_argument("--bn", default=""); a.add_argument("--body", default="")
a.add_argument("--category", default="general"); a.add_argument("--tags", default=""); a.add_argument("--pinned", action="store_true")
x = a.parse_args(); d = load(); i = next_id(d, "note")
d["notes"].append({"id": i, "title": x.title, "title_bn": x.bn, "body": x.body, "category": x.category,
  "tags": tags(x.tags), "pinned": x.pinned, "created_at": now(), "history": [{"at": now(), "event": "created"}]})
save(d); print("✔ Note added:", i)
