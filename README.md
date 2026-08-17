# FRPC GUI Manager

[中文](README_cn.md) | [English](README.md)

A PyQt5-based graphical management tool for FRPC, providing an intuitive interface to manage FRPC proxy configurations.

## ✨ Features

- 🎯 **Dual Mode** - Quick config in Simple Mode, multi-proxy management in Advanced Mode
- 🌍 **Multi-language** - Supports Simplified Chinese/English, extensible via JSON files
- 📊 **Real-time Logs** - Color highlighting with ANSI escape sequence filtering
- 🔧 **Full Configuration** - Server config, Web service, proxy management all in one
- 💾 **Auto-save** - Configurations saved automatically, loaded on next startup
- 🚀 **Ready to Use** - Just need frpc.exe to get started

## 📸 Interface Preview

### Simple Mode
- Quick configuration for single proxy
- Perfect for beginners
- One-click start/stop service

### Advanced Mode
- Manage multiple proxy configurations
- Add/Edit/Delete proxies
- Enable/Disable proxy switches
- Right-click context menu for quick actions

### Running Log
- Real-time FRPC log display
- Color highlighting: Error(red)/Warning(orange)/Success(green)
- Collapsible/Expandable to save space

## 📋 Requirements

- Windows / Linux / macOS
- Python 3.9+ (for development)
- frpc binary (need to prepare separately)

## 🚀 Quick Start

### Run in Development Environment

1. Install dependencies
```bash
pip install PyQt5
```

2. Prepare resource files
```
res/
├── frpc.exe      # FRPC client
└── app_icon.png  # App icon
```

3. Run the program
```bash
python main.py
```

### Package as EXE

```bash
pyinstaller -F -i app_icon.ico --add-data "res;res" --add-data "lang;lang" main.py
```

## Script One-click Build

```bash
build.bat
```

## 🐧 Linux Dependencies

On Linux, install the required Qt/XCB runtime libraries before running:

```bash
apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xkb1 libxkbcommon-x11-0
```

## 📁 Directory Structure

```
Frp-gui/
├── main.py              # Main program entry
├── README.md            # Project documentation
├── README_EN.md         # English documentation
├── .gitignore           # Git ignore file
├── res/                 # Resources directory
│   ├── frpc.exe         # FRPC client
│   └── app_icon.png     # App icon
├── lang/                # Language files directory
│   ├── zh_CN.json       # Simplified Chinese
│   └── en_US.json       # English
└── dist/                # Build output directory
```

## ⚙️ Configuration Files

The program generates the following files in the exe directory:

| File | Description |
|------|-------------|
| `.frpc_gui_config.json` | Main config (server config, proxy list, language setting) |
| `temp.toml` | Simple mode temporary config |
| `frpc_t.toml` | Advanced mode temporary config |

### Configuration Example

```json
{
  "config": {
    "serverAddr": "127.0.0.1",
    "serverPort": 7000,
    "auth_token": "your_token",
    "language": "zh_CN",
    "webServer": {
      "enabled": true,
      "addr": "127.0.0.1",
      "port": 7400,
      "user": "admin",
      "password": "admin"
    }
  },
  "proxies": [
    {
      "name": "Test",
      "type": "tcp",
      "localIP": "127.0.0.1",
      "localPort": 80,
      "remotePort": 8080,
      "enabled": true
    }
  ]
}
```

## 🌍 Multi-language Support

### Add New Language

1. Create `{language_code}.json` file in `lang/` directory
2. Follow the format of `zh_CN.json` for translations
3. Program will auto-scan and add to language menu on startup

### Language File Format

```json
{
    "language_name": "English",
    "title": "FRPC GUI Manager",
    "simple_mode": "Simple Mode",
    "advanced_mode": "Advanced Mode",
    "running_log": "Running Log",
    "language": "Language",
    "configuration": "Configuration",
    "settings": "Settings",
    "exit": "Exit",
    "proxy_config": "Proxy Config",
    "service_control": "Service Control",
    "local_ip": "Local IP",
    "local_port": "Local Port",
    "remote_port": "Remote Port",
    "protocol_type": "Protocol",
    "start_service": "Start Service",
    "stop_service": "Stop Service",
    "connected": "Connected",
    "connecting": "Connecting",
    "connect_failed": "Connect Failed",
    "stopped": "Stopped",
    "add": "Add",
    "edit": "Edit",
    "delete": "Delete",
    "warning": "Warning",
    "warning_server_addr": "Please configure server address first",
    "warning_no_proxy": "Please enable at least one proxy",
    "proxy_name": "Name",
    "status": "Status",
    "operation": "Operation",
    "enabled": "Enabled",
    "disabled": "Disabled",
    "turn_on": "Turn On",
    "turn_off": "Turn Off",
    "frpc_manager": "FRPC Manager",
    "server_config": "Server Config",
    "server_addr": "Server Address",
    "port": "Port",
    "auth_token": "Auth Token",
    "web_service": "Web Service",
    "enable_web": "Enable Web",
    "listen_ip": "Listen IP",
    "username": "Username",
    "password": "Password",
    "save": "Save",
    "cancel": "Cancel",
    "edit_proxy": "Edit Proxy",
    "add_proxy": "Add Proxy",
    "enable_proxy": "Enable this proxy",
    "error": "Error",
    "not_found": "Not Found",
    "start": "Start",
    "exception": "Exception",
    "process_exited": "Process Exited",
    "service_stopped": "Service Stopped",
    "local_address": "Local Address"
}
```

## 🔧 Technical Features

- **ANSI Escape Sequence Filtering** - Automatically clean terminal color codes
- **Log Syntax Highlighting** - Color-coded error/warning/success messages
- **Real-time Status Display** - Connection status, latency updates in real-time
- **Cross-platform Support** - Windows/Linux/macOS
- **Hot Save** - Changes saved immediately, no manual operation needed

## 📄 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

## ⚠️ Notes

1. This program requires `frpc` to work
2. Place `frpc` in the `res/` directory
3. Default configuration file is auto-generated on first run
4. Config files are saved in the same directory as the binary for portability

## 🌐 Language Switch

This README is available in:
- [中文](README_cn.md)
- [English](README.md)







