#!/bin/bash
# Double-click to publish your edits. It checks the build, then sends everything to GitHub,
# which rebuilds ericreier.com in about a minute.
cd "$(dirname "$0")" || exit 1
git pull --rebase --autostash -q || { echo "Couldn't get the latest from GitHub."; read -p "Press Return to close"; exit 1; }
python3 build.py || { read -p "Nothing published. Press Return to close"; exit 1; }
git add -A
if git diff --cached --quiet; then echo "No changes to publish."; read -p "Press Return to close"; exit 0; fi
read -p "Describe the change (or just press Return): " msg
git commit -q -m "${msg:-Update site}" && git push -q && echo "Published. Live on ericreier.com in about a minute: https://github.com/ManCashew/mancashew.github.io/actions"
read -p "Press Return to close"
