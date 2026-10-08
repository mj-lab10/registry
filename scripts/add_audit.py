#!/usr/bin/env python3
"""python3 add_audit.py "Title" --result pass|warning|fail [--target ..] [--findings ..] [--auditor ..] [--related TSK-2026-0001,NOT-..] [--bn ..] [--category ..] [--tags ..]"""
import argparse
from _lib import *
a = argparse.ArgumentParser()
a.add_argument("title"); a.add_argument("--bn", default=""); a.add_argument("--result", required=True, choices=["pass", "warning", "fail"])
a.add_argument("--target", default=""); a.add_argument("--findings", default=""); a.add_argument("--auditor", default="")
a.add_argument("--related", default=""); a.add_argument("--category", default="general"); a.add_argument("--tags", default="")
x = a.parse_args(); d = load()
for r in tags(x.related):
    if find(d, r)[0] is None: die(f"related ID not found: {r}")
i = next_id(d, "audit")
d["audits"].append({"id": i, "title": x.title, "title_bn": x.bn, "result": x.result, "target": x.target,
  "findings": x.findings, "auditor": x.auditor, "related": tags(x.related), "category": x.category,
  "tags": tags(x.tags), "created_at": now(), "history": [{"at": now(), "event": "created"}]})
save(d); print("✔ Audit added:", i)
