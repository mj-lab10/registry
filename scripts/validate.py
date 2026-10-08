#!/usr/bin/env python3
"""Checks data.json integrity. Exit 0 = OK, 1 = problems."""
import re
from _lib import *
d = load(); errs = []; seen = set()
req = {"task": ["id", "title", "status", "priority", "created_at"], "note": ["id", "title", "created_at"],
       "audit": ["id", "title", "result", "created_at"],
       "code": ["id", "title", "lang", "content", "created_at"]}
for k, (p, key) in KIND.items():
    for it in d.get(key, []):
        i = it.get("id", "?")
        if i in seen: errs.append(f"duplicate ID {i}")
        seen.add(i)
        if not re.fullmatch(rf"{p}-\d{{4}}-\d{{4,}}", i): errs.append(f"bad ID format {i}")
        errs += [f"{i}: missing '{f}'" for f in req[k] if not it.get(f)]
        if k == "code" and it.get("content") and hashlib.sha256(it["content"].encode("utf-8")).hexdigest() != it.get("sha256"): errs.append(f"{i}: content hash mismatch")
        c = d["meta"].get("counters", {}).get(k, {}).get(i.split("-")[1], 0)
        if i[:3] == p and int(i.split("-")[2]) > c: errs.append(f"{i}: counter behind ({c})")
for key in ("tasks", "notes", "audits", "codes"):
    for it in d.get(key, []):
        for r in it.get("related", []):
            if r not in seen: errs.append(f"{it['id']}: related ID missing {r}")
mids = []
def walk(ns):
    for n in ns:
        mids.append(n.get("id")); 
        if not n.get("id") or not (n.get("bn") or n.get("en")): errs.append(f"menu node needs id+label: {n}")
        walk(n.get("children", []))
walk(d.get("menu", []))
for it in d.get('codes', []):
    errs += [f"{it['id']}: menu_path id not in menu: {m}" for m in it.get('menu_path', []) if m not in mids]
errs += [f"duplicate menu id {m}" for m in set(mids) if mids.count(m) > 1]
if errs: print("✘ Problems:"); [print("  -", e) for e in errs]; sys.exit(1)
print(f"✔ OK — {len(d['tasks'])} tasks, {len(d['notes'])} notes, {len(d['audits'])} audits, {len(d['codes'])} codes, {len(mids)} menu nodes")
