#!/usr/bin/env bash
# ./run.sh task|complete|note|audit|code|codedir|menu|check|serve [...]
cd "$(dirname "$0")"
c="$1"; shift
case "$c" in
  task) python3 scripts/add_task.py "$@" && python3 scripts/validate.py ;;
  complete) python3 scripts/complete_task.py "$@" && python3 scripts/validate.py ;;
  note) python3 scripts/add_note.py "$@" && python3 scripts/validate.py ;;
  audit) python3 scripts/add_audit.py "$@" && python3 scripts/validate.py ;;
  code) python3 scripts/add_code.py "$@" && python3 scripts/validate.py ;;
  codedir) python3 scripts/add_code_dir.py "$@" && python3 scripts/validate.py ;;
  menu) python3 scripts/menu.py "$@" && python3 scripts/validate.py ;;
  check) python3 scripts/validate.py ;;
  serve) echo "Open http://localhost:8000"; python3 -m http.server 8000 ;;
  *) echo "usage: ./run.sh task|complete|note|audit|code|codedir|menu|check|serve ..." ;;
esac
