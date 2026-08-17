#!/usr/bin/env bash
set -e

pip install pyinstaller pillow PyQt5

pyinstaller -F -w -i app_icon.ico --add-data "res/app_icon.png:res" --add-data "res/frpc.exe:res" --add-data "lang:lang" main.py

if [ -f dist/main ]; then
    mv dist/main dist/frp-gui
elif [ -f dist/main.exe ]; then
    mv dist/main.exe dist/frp-gui
else
    echo "Error: build output not found in dist/" >&2
    exit 1
fi

echo "Build complete: dist/frp-gui"
