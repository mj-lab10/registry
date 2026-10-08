#!/usr/bin/env python3
"""Manage the CodeCraft menu tree.
python3 menu.py                                        show the tree (ids, names, entry counts)
python3 menu.py --new "Web/Portal" [--bn "ওয়েব/পোর্টাল"] [--under "CodeCraft/Tools"]   create empty submenus
python3 menu.py --move CDE-2026-0001 --to "CodeCraft/Web/Portal"                       move ONE file
python3 menu.py --move-menu "CodeCraft/Web/Portal" --to "CodeCraft/Tools"              move a WHOLE submenu — every
                                                                                        nested submenu and every file
                                                                                        inside it moves with it"""
import argparse
from _lib import *
a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument("--new", default=""); a.add_argument("--bn", default=""); a.add_argument("--under", default="")
a.add_argument("--move", default=""); a.add_argument("--move-menu", default="", dest="move_menu"); a.add_argument("--to", default="")
x = a.parse_args(); d = normalize(load()); root = ensure_root(d); changed = False

def detach(nodes, nid):
    """Remove and return the node with id==nid from anywhere in the tree (searched recursively)."""
    for i, n in enumerate(nodes):
        if n["id"] == nid: return nodes.pop(i)
        r = detach(n.get("children", []), nid)
        if r is not None: return r
    return None

if x.new:
    node, path = root, ["codecraft"]
    if x.under:
        node, path = find_node(d, x.under)
        if not node: die(f"menu not found: {x.under}")
    node, path = ensure_chain(d, node, path, [s.strip() for s in x.new.split("/") if s.strip()], x.bn.split("/")); changed = True
    print("✔ menu ready:", " › ".join(path))

if x.move:
    k, it = find(d, x.move)
    if k != "code": die(f"CodeCraft entry not found: {x.move}")
    node, path = find_node(d, x.to)
    if not node: die(f"menu not found: {x.to}")
    it["menu_path"] = path; it["history"].append({"at": now(), "event": "moved", "note": " › ".join(path)}); changed = True
    print(f"✔ {x.move} → {' › '.join(path)}")

if x.move_menu:
    if not x.to: die("--to is required with --move-menu")
    src_node, src_path = find_node(d, x.move_menu)
    if not src_node: die(f"menu not found: {x.move_menu}")
    if src_node["id"] == "codecraft": die("cannot move the CodeCraft root itself")
    dst_node, dst_path = find_node(d, x.to)
    if not dst_node: die(f"menu not found: {x.to}")
    if dst_path == src_path: die("source and destination are the same menu")
    if dst_path[:len(src_path)] == src_path: die("cannot move a menu into itself or into one of its own submenus")
    dst_children = dst_node.setdefault("children", [])
    if any(c["id"] == src_node["id"] for c in dst_children):
        die(f"a menu with id {src_node['id']} already exists directly under the destination — rename or remove it first")
    moved_node = detach(d["menu"], src_node["id"])
    if moved_node is None: die("internal error: could not locate the menu to detach")
    dst_children.append(moved_node); changed = True
    new_path = dst_path + [src_node["id"]]
    n_files = 0
    for it in d["codes"]:
        mp = it.get("menu_path", [])
        if mp[:len(src_path)] == src_path:
            it["menu_path"] = new_path + mp[len(src_path):]
            it["history"].append({"at": now(), "event": "moved with parent menu", "note": " › ".join(new_path)})
            n_files += 1
    print(f"✔ menu moved: {' › '.join(src_path)}  →  {' › '.join(new_path)}   ({n_files} file(s) relocated with it)")

if changed: save(d)

def show(ns, ind=0):
    for n in ns:
        c = f"  ({sum(1 for it in d['codes'] if n['id'] in it['menu_path'])})" if n.get("view", {}).get("type") == "codes" else ""
        print("  " * ind + f"{'└ ' if ind else ''}{n.get('en') or n.get('bn')} / {n.get('bn','')}  [{n['id']}]{c}")
        show(n.get("children", []), ind + 1)
if not (x.new or x.move or x.move_menu): show(d["menu"])
