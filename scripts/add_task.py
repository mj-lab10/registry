#!/usr/bin/env python3
"""python3 add_task.py "Title" [--bn "শিরোনাম"] [--desc ..] [--priority low|medium|high|urgent] [--due YYYY-MM-DD] [--category ..] [--tags a,b]"""
import argparse
from _lib import *
a = argparse.ArgumentParser()
a.add_argument("title"); a.add_argument("--bn", default=""); a.add_argument("--desc", default="")
a.add_argument("--priority", default="medium", choices=["low", "medium", "high", "urgent"])
a.add_argument("--due", default=""); a.add_argument("--category", default="general"); a.add_argument("--tags", default="")
x = a.parse_args(); d = load(); i = next_id(d, "task")
d["tasks"].append({"id": i, "title": x.title, "title_bn": x.bn, "desc": x.desc, "status": "todo",
  "priority": x.priority, "due": x.due, "category": x.category, "tags": tags(x.tags),
  "created_at": now(), "completed_at": "", "history": [{"at": now(), "event": "created"}]})
save(d); print("✔ Task added:", i)
