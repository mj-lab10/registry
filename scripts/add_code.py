#!/usr/bin/env python3
"""Save a whole file (local path or http/https URL) into CodeCraft.

python3 add_code.py ~/mj/portal/index.html "Title" "Description" --bn "শিরোনাম" --bn "বর্ণনা"
  (1st --bn = title BN, 2nd --bn = description BN; or --title-bn / --desc-bn)

Where it goes (see the tree with:  ./run.sh menu):
  (nothing)                        -> CodeCraft > <file type>        e.g. CodeCraft > HTML
  --menu "CodeCraft/Web/Portal"    -> into an existing menu/submenu (menu id or name path)
  --new-menu "UI/Forms"            -> create nested submenus (under --menu, or CodeCraft) and put it there
  --new-menu-bn "ইউআই/ফর্ম"        -> Bangla names for the new submenus, same order
Other: --category X --tags a,b --lang python --force.  No arguments = interactive."""
import argparse, os, urllib.request
from urllib.parse import urlparse
from _lib import *
MAX = 2 * 1024 * 1024
a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument("source", nargs="?", default=""); a.add_argument("title", nargs="?", default=""); a.add_argument("desc", nargs="?", default="")
a.add_argument("--bn", action="append", default=[]); a.add_argument("--title-bn", default=""); a.add_argument("--desc-bn", default="")
a.add_argument("--menu", default=""); a.add_argument("--new-menu", default=""); a.add_argument("--new-menu-bn", default="")
a.add_argument("--category", default="general"); a.add_argument("--tags", default=""); a.add_argument("--lang", default=""); a.add_argument("--force", action="store_true")
x = a.parse_intermixed_args()
if not x.source:
    print("— New CodeCraft entry (Enter to skip optional fields) —")
    x.source = ask("File path or URL *", req=True); x.title = ask("Title (EN)"); x.title_bn = ask("শিরোনাম (BN)")
    x.desc = ask("Description (EN)"); x.desc_bn = ask("বর্ণনা (BN)")
    x.menu = ask("Existing menu (id or path, Enter = by file type; ./run.sh menu shows the tree)")
    x.new_menu = ask("New submenu name(s) e.g. UI/Forms (optional)"); x.new_menu_bn = ask("নতুন সাবমেনুর বাংলা নাম (optional)") if x.new_menu else ""
    x.category = ask("Category", "general"); x.tags = ask("Tags a,b")
tb = x.title_bn or (x.bn[0] if x.bn else ""); db = x.desc_bn or (x.bn[1] if len(x.bn) > 1 else "")
src = x.source
try:
    if src.startswith(("http://", "https://")):
        with urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "mj-registry"}), timeout=20) as r: raw = r.read(MAX + 1)
        name = os.path.basename(urlparse(src).path) or "index.html"
    else:
        p = os.path.abspath(os.path.expanduser(src))
        if not os.path.isfile(p): die(f"file not found: {src}")
        with open(p, "rb") as f: raw = f.read(MAX + 1)
        name = os.path.basename(p)
except Exception as e: die(f"could not read {src}: {e}")
if len(raw) > MAX: die("file larger than 2 MB")
try: text = raw.decode("utf-8-sig").replace("\r\n", "\n")
except UnicodeDecodeError: die("not a UTF-8 text file (binary files are not supported)")
lang, label = detect(name, text, x.lang.lower())
sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
d = normalize(load()); root = ensure_root(d)
dup = next((c for c in d["codes"] if c.get("sha256") == sha), None)
if dup and not x.force: die(f"identical content already saved as {dup['id']} (use --force to add anyway)")
node, path = root, ["codecraft"]
if x.menu:
    node, path = find_node(d, x.menu)
    if not node: die(f"menu not found: {x.menu}  (run ./run.sh menu to see the tree, or create it with --new-menu)")
if x.new_menu:
    node, path = ensure_chain(d, node, path, [s.strip() for s in x.new_menu.split("/") if s.strip()], x.new_menu_bn.split("/"))
elif not x.menu:
    node, path = ensure_chain(d, root, ["codecraft"], [label])
i = next_id(d, "code")
d["codes"].append({"id": i, "title": x.title or name, "title_bn": tb, "desc": x.desc, "desc_bn": db, "filename": name,
  "source": src, "lang": lang, "lang_label": label, "ext": name.rsplit(".", 1)[-1].lower() if "." in name else "",
  "lines": text.count("\n") + (0 if text == "" or text.endswith("\n") else 1), "bytes": len(raw), "sha256": sha,
  "menu_path": path, "category": x.category, "tags": tags(x.tags), "created_at": now(),
  "history": [{"at": now(), "event": "created", "note": src}], "content": text})
save(d); print(f"✔ CodeCraft added: {i}  [{label}]  {name}  →  " + " › ".join(next(n for n, p in walk(d['menu']) if n['id'] == k)['en'] for k in path))
