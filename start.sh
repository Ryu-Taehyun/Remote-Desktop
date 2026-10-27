#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
trap 'echo "Startup failed. Read the error above."; exit 1' ERR

case "$(uname -s)" in
  MINGW*|MSYS*) ;;
  *) echo "This launcher requires Windows and Git Bash."; exit 1 ;;
esac

if [[ ! -f .venv/Scripts/python.exe ]]; then
  if command -v python >/dev/null 2>&1 && python -c 'import sys; assert sys.version_info.major == 3' 2>/dev/null; then
    python -m venv .venv
  elif command -v py >/dev/null 2>&1; then
    py -3 -m venv .venv
  else
    echo "Install Python 3 (with pip), then run again."
    exit 1
  fi
fi
PYTHON="./.venv/Scripts/python.exe"
if ! "$PYTHON" -c 'import mss, cv2, numpy; assert hasattr(cv2, "imshow")' 2>/dev/null; then
  echo "Installing screen capture dependencies..."
  "$PYTHON" -m pip install -r requirements.txt
fi
"$PYTHON" -m pip check
"$PYTHON" -u launch_all.py
