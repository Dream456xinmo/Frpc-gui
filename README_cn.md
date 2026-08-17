# FRPC GUI Manager

[中文](README.md) | [English](README_en.md)

一个基于 PyQt5 开发的 FRPC 图形化管理工具，提供简单直观的界面来管理 FRPC 代理配置。

## ✨ 功能特点

- 🎯 **双模式操作** - 简单模式快速配置，高级模式多代理管理
- 🌍 **多语言支持** - 支持简体中文/English，可通过 JSON 文件扩展
- 📊 **实时日志** - 彩色高亮显示，支持 ANSI 转义序列过滤
- 🔧 **完整配置** - 服务器配置、Web服务、代理管理一应俱全
- 💾 **自动保存** - 配置自动保存，下次启动自动加载
- 🚀 **开箱即用** - 配合 frpc.exe 即可使用

## 📸 界面预览

### 简单模式
- 快速配置单个代理
- 适合新手快速上手
- 一键启动/停止服务

### 高级模式
- 管理多个代理配置
- 支持添加/编辑/删除代理
- 支持代理启用/禁用开关
- 右键菜单快捷操作

### 运行日志
- 实时显示 FRPC 运行日志
- 错误(红色)/警告(橙色)/成功(绿色)高亮
- 支持折叠/展开节省空间

## 📋 系统要求

- Windows / Linux / macOS
- Python 3.9+ (开发环境)
- frpc.exe (二进制文件需自行准备)

## 🚀 快速开始

### 开发环境运行

1. 安装依赖
```bash
pip install PyQt5
```

2. 准备资源文件
```
res/
├── frpc.exe      # FRPC 客户端
└── app_icon.png  # 程序图标
```

3. 运行程序
```bash
python main.py
```

### 打包为 EXE

```bash
pyinstaller -F -i app_icon.ico --add-data "res;res" --add-data "lang;lang" main.py
```

## 脚本一键编译

```bash
build.bat
```
## 🐧 Linux 依赖

在 Linux 上运行前，请先安装所需的 Qt/XCB 运行时库：

```bash
apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xkb1 libxkbcommon-x11-0
```

## 📁 目录结构

```
Frp-gui/
├── main.py              # 主程序入口
├── README.md            # 项目说明
├── .gitignore           # Git 忽略文件
├── res/                 # 资源目录
│   ├── frpc.exe         # FRPC 客户端
│   └── app_icon.png     # 程序图标
├── lang/                # 语言文件目录
│   ├── zh_CN.json       # 简体中文
│   └── en_US.json       # 英文
└── dist/                # 打包输出目录
```

## ⚙️ 配置文件

程序会在 exe 所在目录生成以下文件：

| 文件 | 说明 |
|------|------|
| `.frpc_gui_config.json` | 主配置文件（服务器配置、代理列表、语言设置） |
| `temp.toml` | 简单模式临时配置 |
| `frpc_t.toml` | 高级模式临时配置 |

### 配置示例

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

## 🌍 多语言支持

### 添加新语言

1. 在 `lang/` 目录创建 `{语言代码}.json` 文件
2. 参考 `zh_CN.json` 格式填写翻译
3. 程序启动时自动扫描并添加到语言菜单

### 语言文件格式

```json
{
    "language_name": "简体中文",
    "title": "FRPC 可视化管理器",
    "simple_mode": "简单模式",
    "advanced_mode": "高级模式",
    "running_log": "运行日志",
    "language": "语言",
    "configuration": "配置",
    "settings": "设置",
    "exit": "退出",
    "proxy_config": "代理配置",
    "service_control": "服务控制",
    "local_ip": "本地IP",
    "local_port": "本地端口",
    "remote_port": "外部端口",
    "protocol_type": "协议",
    "start_service": "启动服务",
    "stop_service": "停止服务",
    "connected": "已连接",
    "connecting": "连接中",
    "connect_failed": "连接失败",
    "stopped": "未启动",
    "add": "添加",
    "edit": "编辑",
    "delete": "删除",
    "warning": "警告",
    "warning_server_addr": "请先配置服务器地址",
    "warning_no_proxy": "请至少启用一个代理",
    "proxy_name": "名称",
    "status": "状态",
    "operation": "操作",
    "enabled": "已启用",
    "disabled": "已禁用",
    "turn_on": "开启",
    "turn_off": "关闭",
    "frpc_manager": "FRPC 管理器",
    "server_config": "服务器配置",
    "server_addr": "服务器地址",
    "port": "端口",
    "auth_token": "认证密钥",
    "web_service": "Web服务",
    "enable_web": "启用Web服务",
    "listen_ip": "监听IP",
    "username": "用户名",
    "password": "密码",
    "save": "保存",
    "cancel": "取消",
    "edit_proxy": "编辑代理",
    "add_proxy": "添加代理",
    "enable_proxy": "启用此代理",
    "error": "错误",
    "not_found": "找不到",
    "start": "启动",
    "exception": "异常",
    "process_exited": "进程已退出",
    "service_stopped": "服务已停止",
    "local_address": "本地地址"
}
```

## 🔧 技术特性

- **ANSI 转义序列过滤** - 自动清理终端颜色代码
- **日志语法高亮** - 错误/警告/成功信息彩色显示
- **实时状态显示** - 连接状态、延迟信息实时更新
- **跨平台支持** - Windows/Linux/macOS
- **配置热保存** - 修改即保存，无需手动操作

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⚠️ 注意事项

1. 本程序需要配合 `frpc` 使用
2. 请将 `frpc` 放置在 `res/` 目录下
3. 首次运行会自动生成默认配置文件
4. 配置文件与 `二进制` 在同一目录，方便携带



---

## 🌐 Language Switch

This README is available in:
- [中文](README.md)
- [English](README_en.md)


**如果对您有帮助，请给个 Star ⭐**
