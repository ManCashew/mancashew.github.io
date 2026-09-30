#!/bin/bash
# Double-click to build the site and open it in your browser. Close this window to stop.
cd "$(dirname "$0")" || exit 1
python3 build.py || { read -p "Press Return to close"; exit 1; }
(sleep 1; open http://localhost:8000) &
cd _site && python3 -m http.server 8000
