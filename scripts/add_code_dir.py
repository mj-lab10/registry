#!/usr/bin/env python3
"""Import an entire directory into CodeCraft, recursively — every file lands in the
correct submenu, mirroring the folder structure exactly.

python3 add_code_dir.py ~/mj/portal
python3 add_code_dir.py ~/mj/portal --menu "CodeCraft/Web"     put the mirrored tree under an existing menu
python3 add_code_dir.py ~/mj/portal --title "Portal v2"        name for the root submenu (default: folder name)
python3 add_code_dir.py ~/mj/portal --exclude dist,coverage --force

Always skipped: binary files, files over 2 MB, dotfiles/dot-folders, and by default:
.git node_modules __pycache__ .venv venv .idea .vscode dist build .next .cache
(add more with --exclude, comma-separated folder names)"""
import argparse, os
from _lib import *
MAX = 2 * 1024 * 1024
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea", ".vscode", "dist", "build", ".next", ".cache"}
a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument("dir"); a.add_argument("--menu", default=""); a.add_argument("--title", default="")
a.add_argument("--category", default="general"); a.add_argument("--exclude", default=""); a.add_argument("--force", action="store_true")
x = a.parse_args()
root_path = os.path.abspath(os.path.expanduser(x.dir))
if not os.path.isdir(root_path): die(f"not a directory: {x.dir}")
excl = SKIP | {s.strip() for s in x.exclude.split(",") if s.strip()}
base_name = x.title or os.path.basename(root_path.rstrip("/")) or "root"
d = normalize(load()); croot = ensure_root(d)
start, start_path = (find_node(d, x.menu) if x.menu else (croot, ["codecraft"]))
if x.menu and not start: die(f"menu not found: {x.menu}  (run ./run.sh menu to see the tree)")
start, start_path = ensure_chain(d, start, start_path, [base_name])
added = skipped = dup = 0
for dirpath, dirnames, filenames in os.walk(root_path):
    dirnames[:] = sorted(dn for dn in dirnames if dn not in excl and not dn.startswith("."))
    rel = os.path.relpath(dirpath, root_path)
    segs = [] if rel == "." else rel.split(os.sep)
    node, path = ensure_chain(d, start, start_path, segs) if segs else (start, start_path)
    for fn in sorted(fn for fn in filenames if not fn.startswith(".")):
        fp = os.path.join(dirpath, fn)
        try:
            with open(fp, "rb") as f: raw = f.read(MAX + 1)
        except Exception: skipped += 1; continue
        if len(raw) > MAX: skipped += 1; continue
        try: text = raw.decode("utf-8-sig").replace("\r\n", "\n")
        except UnicodeDecodeError: skipped += 1; continue
        lang, label = detect(fn, text)
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if any(c.get("sha256") == sha for c in d["codes"]) and not x.force: dup += 1; continue
        i = next_id(d, "code")
        d["codes"].append({"id": i, "title": fn, "title_bn": "", "desc": "", "desc_bn": "", "filename": fn,
          "source": fp, "lang": lang, "lang_label": label, "ext": fn.rsplit(".", 1)[-1].lower() if "." in fn else "",
          "lines": text.count("\n") + (0 if text == "" or text.endswith("\n") else 1), "bytes": len(raw), "sha256": sha,
          "menu_path": path, "category": x.category, "tags": [], "created_at": now(),
          "history": [{"at": now(), "event": "created", "note": fp}], "content": text})
        added += 1
save(d)
names = {n["id"]: n for n, _ in walk(d["menu"])}
print(f"✔ imported {added} file(s) from {x.dir}  →  " + " › ".join(names[k].get('en') or names[k].get('bn') for k in start_path))
if skipped: print(f"  (skipped {skipped} binary/too-large/unreadable file(s))")
if dup: print(f"  (skipped {dup} duplicate file(s) already in CodeCraft — use --force to add anyway)")
