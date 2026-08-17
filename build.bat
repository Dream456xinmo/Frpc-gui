@echo off
pip install pyinstaller pillow PyQt5 
pyinstaller -F -w -i app_icon.ico --add-data "res/app_icon.png;res" --add-data "res/frpc.exe;res" --add-data "lang;lang" main.py
move .\dist\main.exe .\dist\frp-gui.exe