import sys
import json
import os
import subprocess
import re
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ==============================================
# 核心路径修改：区分开发环境和打包环境
# ==============================================
if getattr(sys, 'frozen', False):
    # 打包后运行：
    # - 配置文件放在 exe 所在目录（用户可写）
    # - 资源文件从 PyInstaller 解压的临时目录读取
    BASE_DIR = os.path.dirname(sys.executable)
    BASE_RESOURCE = sys._MEIPASS
else:
    # 开发环境运行：
    # - 配置文件放在项目当前目录
    # - 资源文件也在项目当前目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_RESOURCE = BASE_DIR

# ==========================================
# 配置文件：永远在 exe 旁边的当前目录 (BASE_DIR)
# ==========================================
CONFIG_FILE = os.path.join(BASE_DIR, ".frpc_gui_config.json")
TEMP_CONFIG_FILE = os.path.join(BASE_DIR, "temp.toml")
TEMP_CONFIG_FILE_ADV = os.path.join(BASE_DIR, "frpc_t.toml")

# ==========================================
# 程序资源：从资源目录读取 (BASE_RESOURCE)
# ==========================================
RESOURCE_DIR = os.path.join(BASE_RESOURCE, "res")
# Windows 下为 frpc.exe，Linux/macOS 下为 frpc
FRPC_BINARY_NAME = "frpc.exe" if sys.platform.startswith("win") else "frpc"
FRPC_EXECUTABLE = os.path.join(RESOURCE_DIR, FRPC_BINARY_NAME)
ICON_FILE = os.path.join(RESOURCE_DIR, "app_icon.png")

# ==========================================
# 语言文件目录（从资源目录读取）
# ==========================================
LANG_DIR = os.path.join(BASE_RESOURCE, "lang")

DEFAULT_SERVER_CONFIG = {
    "serverAddr": "127.0.0.1",
    "serverPort": 7000,
    "auth_token": "password",
    "webServer": {
        "enabled": True,
        "addr": "127.0.0.1",
        "port": 7400,
        "user": "admin",
        "password": "admin"
    },
    "language": "zh_CN"
}


# 内嵌默认中文翻译：当 lang 目录缺失或语言文件加载失败时的兜底翻译
DEFAULT_TRANSLATIONS = {
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


class LanguageManager:
    """语言管理器 - 优先从lang文件夹读取，缺失时使用内嵌默认翻译"""
    def __init__(self):
        self.current_lang = "zh_CN"
        self.translations = {}
        self.available_langs = {}
        self._load_available_languages()
        self._load_translations()

    def _load_available_languages(self):
        """扫描lang文件夹获取可用语言列表"""
        self.available_langs = {}
        
        if os.path.exists(LANG_DIR):
            for file in os.listdir(LANG_DIR):
                if file.endswith('.json'):
                    lang_code = file[:-5]
                    try:
                        with open(os.path.join(LANG_DIR, file), "r", encoding="utf-8") as f:
                            trans = json.load(f)
                            # 获取语言显示名称，如果没有则使用代码
                            lang_display = trans.get("language_name", lang_code)
                            self.available_langs[lang_code] = lang_display
                    except Exception as e:
                        print(f"Failed to read language file {file}: {e}")
        
        # 如果没有找到任何语言文件，使用内嵌默认中文
        if not self.available_langs:
            self.available_langs = {"zh_CN": DEFAULT_TRANSLATIONS.get("language_name", "简体中文")}

    def _load_translations(self):
        """加载当前语言的翻译，加载不到时回退到内嵌默认翻译"""
        lang_file = os.path.join(LANG_DIR, f"{self.current_lang}.json")
        
        try:
            if os.path.exists(lang_file):
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                return
        except Exception as e:
            print(f"Failed to load language file {lang_file}: {e}")

        # 文件不存在或加载失败：尝试加载第一个可用的语言文件
        if self.available_langs:
            first_lang = list(self.available_langs.keys())[0]
            if first_lang != self.current_lang:
                self.current_lang = first_lang
                self._load_translations()
                return

        # 实在没有语言文件（或只有默认占位语言），回退到内嵌默认中文翻译
        self.translations = dict(DEFAULT_TRANSLATIONS)

    def load_language(self, lang_code):
        """切换语言"""
        if lang_code in self.available_langs:
            self.current_lang = lang_code
            self._load_translations()
            return True
        return False

    def get_available_languages(self):
        """获取可用语言列表"""
        return self.available_langs

    def tr(self, key):
        """获取翻译：先查已加载翻译，再查内嵌默认，最后回退键名"""
        if key in self.translations:
            return self.translations[key]
        if key in DEFAULT_TRANSLATIONS:
            return DEFAULT_TRANSLATIONS[key]
        return key


lang_manager = LanguageManager()


class StatusLabel(QLabel):
    """自定义状态标签"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QLabel { padding: 2px 5px; border-radius: 3px; margin: 3px; }")

    def setConnected(self, latency=""):
        if latency:
            self.setText(f"✓ {lang_manager.tr('connected')} ({latency})")
        else:
            self.setText(f"✓ {lang_manager.tr('connected')}")
        self.setStyleSheet("QLabel { background-color: #4CAF50; color: white; padding: 2px 5px; border-radius: 3px; margin: 3px; }")

    def setConnecting(self):
        self.setText(f"⟳ {lang_manager.tr('connecting')}...")
        self.setStyleSheet("QLabel { background-color: #FF9800; color: white; padding: 2px 5px; border-radius: 3px; margin: 3px; }")

    def setFailed(self):
        self.setText(f"✗ {lang_manager.tr('connect_failed')}")
        self.setStyleSheet("QLabel { background-color: #F44336; color: white; padding: 2px 5px; border-radius: 3px; margin: 3px; }")

    def setStopped(self):
        self.setText(f"○ {lang_manager.tr('stopped')}")
        self.setStyleSheet("QLabel { background-color: #9E9E9E; color: white; padding: 2px 5px; border-radius: 3px; margin: 3px; }")


class LogHighlighter(QSyntaxHighlighter):
    """日志高亮"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.error_pattern = re.compile(r'.*(error|failed|refuse|timeout|unavailable|panic|fatal).*', re.IGNORECASE)
        self.warning_pattern = re.compile(r'.*(warning|warn).*', re.IGNORECASE)
        self.success_pattern = re.compile(r'.*(success|started|online|connected|login success).*', re.IGNORECASE)

        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#C62828"))
        self.error_format.setFontWeight(QFont.Bold)

        self.warning_format = QTextCharFormat()
        self.warning_format.setForeground(QColor("#B26A00"))

        self.success_format = QTextCharFormat()
        self.success_format.setForeground(QColor("#2E7D32"))

    def clean_ansi_escape(self, text):
        """移除 ANSI 转义序列"""
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        text = ansi_escape.sub('', text)
        text = text.replace('\x1B', '')
        return text

    def highlightBlock(self, text):
        cleaned_text = self.clean_ansi_escape(text)
        if self.error_pattern.match(cleaned_text):
            self.setFormat(0, len(text), self.error_format)
        elif self.warning_pattern.match(cleaned_text):
            self.setFormat(0, len(text), self.warning_format)
        elif self.success_pattern.match(cleaned_text):
            self.setFormat(0, len(text), self.success_format)


class CollapsibleWidget(QWidget):
    """可折叠组件"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("QWidget { background-color: #f0f0f0; border: 1px solid #ccc; border-radius:3px; }")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 5, 10, 5)

        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setFixedSize(20, 20)
        self.toggle_btn.setStyleSheet("border:none; background:transparent;")
        self.toggle_btn.clicked.connect(self.toggle)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight:bold;")

        title_layout.addWidget(self.toggle_btn)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        self.title_bar.setLayout(title_layout)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_area.setLayout(self.content_layout)

        layout.addWidget(self.title_bar)
        layout.addWidget(self.content_area)
        self.setLayout(layout)

    def toggle(self):
        self.is_collapsed = not self.is_collapsed
        self.toggle_btn.setText("▶" if self.is_collapsed else "▼")
        self.content_area.setVisible(not self.is_collapsed)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)


class ConfigDialog(QDialog):
    """配置对话框"""
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle(lang_manager.tr("settings"))
        self.setModal(True)
        self.setMinimumWidth(400)
        self.initUI()
        self.load()

    def initUI(self):
        layout = QVBoxLayout()

        server = QGroupBox(lang_manager.tr("server_config"))
        f = QFormLayout(server)
        self.addr = QLineEdit()
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.token = QLineEdit()
        self.token.setEchoMode(QLineEdit.Password)

        f.addRow(lang_manager.tr("server_addr") + ":", self.addr)
        f.addRow(lang_manager.tr("port") + ":", self.port)
        f.addRow(lang_manager.tr("auth_token") + ":", self.token)

        web = QGroupBox(lang_manager.tr("web_service"))
        wl = QVBoxLayout(web)
        self.en_web = QCheckBox(lang_manager.tr("enable_web"))
        self.en_web.toggled.connect(self.onWebToggle)

        wc = QWidget()
        ff = QFormLayout(wc)
        self.waddr = QLineEdit()
        self.wport = QSpinBox()
        self.wport.setRange(1, 65535)
        self.wuser = QLineEdit()
        self.wpwd = QLineEdit()
        self.wpwd.setEchoMode(QLineEdit.Password)

        ff.addRow(lang_manager.tr("listen_ip") + ":", self.waddr)
        ff.addRow(lang_manager.tr("port") + ":", self.wport)
        ff.addRow(lang_manager.tr("username") + ":", self.wuser)
        ff.addRow(lang_manager.tr("password") + ":", self.wpwd)

        wl.addWidget(self.en_web)
        wl.addWidget(wc)
        self.webWidget = wc

        btnLayout = QHBoxLayout()
        save = QPushButton(lang_manager.tr("save"))
        cancel = QPushButton(lang_manager.tr("cancel"))
        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        btnLayout.addStretch()
        btnLayout.addWidget(save)
        btnLayout.addWidget(cancel)

        layout.addWidget(server)
        layout.addWidget(web)
        layout.addLayout(btnLayout)
        self.setLayout(layout)

    def onWebToggle(self, e):
        self.webWidget.setEnabled(e)

    def load(self):
        self.addr.setText(self.config.get("serverAddr", ""))
        self.port.setValue(self.config.get("serverPort", 7000))
        self.token.setText(self.config.get("auth_token", ""))
        w = self.config.get("webServer", {})
        self.en_web.setChecked(w.get("enabled", False))
        self.waddr.setText(w.get("addr", "127.0.0.1"))
        self.wport.setValue(w.get("port", 7400))
        self.wuser.setText(w.get("user", ""))
        self.wpwd.setText(w.get("password", ""))

    def accept(self):
        self.config["serverAddr"] = self.addr.text().strip()
        self.config["serverPort"] = self.port.value()
        self.config["auth_token"] = self.token.text().strip()
        self.config["webServer"] = {
            "enabled": self.en_web.isChecked(),
            "addr": self.waddr.text().strip(),
            "port": self.wport.value(),
            "user": self.wuser.text().strip(),
            "password": self.wpwd.text().strip()
        }
        super().accept()


class ProxyDialog(QDialog):
    """代理编辑对话框"""
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or {}
        self.setWindowTitle(lang_manager.tr("edit_proxy") if data else lang_manager.tr("add_proxy"))
        self.setModal(True)
        self.initUI()
        self.load()

    def initUI(self):
        layout = QFormLayout()
        self.name = QLineEdit()
        self.typeC = QComboBox()
        self.typeC.addItems(["tcp", "udp", "http", "https", "stcp", "xtcp"])
        self.ip = QLineEdit("127.0.0.1")
        self.lport = QSpinBox()
        self.lport.setRange(1, 65535)
        self.rport = QSpinBox()
        self.rport.setRange(1, 65535)
        self.enabled = QCheckBox(lang_manager.tr("enable_proxy"))

        layout.addRow(lang_manager.tr("proxy_name") + ":", self.name)
        layout.addRow(lang_manager.tr("protocol_type") + ":", self.typeC)
        layout.addRow(lang_manager.tr("local_ip") + ":", self.ip)
        layout.addRow(lang_manager.tr("local_port") + ":", self.lport)
        layout.addRow(lang_manager.tr("remote_port") + ":", self.rport)
        layout.addRow(lang_manager.tr("status") + ":", self.enabled)

        btn = QHBoxLayout()
        s = QPushButton(lang_manager.tr("save"))
        c = QPushButton(lang_manager.tr("cancel"))
        s.clicked.connect(self.accept)
        c.clicked.connect(self.reject)
        btn.addStretch()
        btn.addWidget(s)
        btn.addWidget(c)
        layout.addRow(btn)
        self.setLayout(layout)

    def load(self):
        self.name.setText(self.data.get("name", ""))
        self.typeC.setCurrentText(self.data.get("type", "tcp"))
        self.ip.setText(self.data.get("localIP", "127.0.0.1"))
        self.lport.setValue(self.data.get("localPort", 0))
        self.rport.setValue(self.data.get("remotePort", 0))
        self.enabled.setChecked(self.data.get("enabled", True))

    def accept(self):
        self.data = {
            "name": self.name.text().strip(),
            "type": self.typeC.currentText(),
            "localIP": self.ip.text().strip(),
            "localPort": self.lport.value(),
            "remotePort": self.rport.value(),
            "enabled": self.enabled.isChecked()
        }
        super().accept()


class FRPCThread(QThread):
    """FRPC 工作线程"""
    log = pyqtSignal(str)
    status = pyqtSignal(bool)
    latency = pyqtSignal(str)
    connection_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.process = None
        self.running = False
        self.cfg = ""
        self.current_latency = ""
        self.has_connected = False

    def clean_ansi_escape(self, text):
        """移除 ANSI 转义序列"""
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        text = ansi_escape.sub('', text)
        text = text.replace('\x1B', '')
        return text

    def run(self):
        if not os.path.exists(FRPC_EXECUTABLE):
            self.log.emit(f"{lang_manager.tr('error')}: {lang_manager.tr('not_found')} {FRPC_EXECUTABLE}")
            self.status.emit(False)
            self.connection_status.emit("failed")
            return

        cmd = [FRPC_EXECUTABLE, "-c", self.cfg]
        self.log.emit(f"{lang_manager.tr('start')}: " + " ".join(cmd))

        try:
            creation_flags = 0
            if sys.platform == 'win32':
                creation_flags = subprocess.CREATE_NO_WINDOW

            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, universal_newlines=True,
                encoding='utf-8', errors='replace', creationflags=creation_flags
            )
            self.running = True
            self.status.emit(True)
            self.connection_status.emit("connecting")
            self.has_connected = False

            for line in iter(self.process.stdout.readline, ""):
                if not self.running:
                    break
                line = line.strip()
                if not line:
                    continue

                clean_line = self.clean_ansi_escape(line)
                self.log.emit(clean_line)

                if re.search(r'(error|failed|refuse|timeout|unavailable)', clean_line, re.I):
                    self.connection_status.emit("failed")
                    self.has_connected = False

                if re.search(r'(success|online|connected|login success)', clean_line, re.I):
                    if not self.has_connected:
                        self.connection_status.emit("connected")
                        self.has_connected = True

                m = re.search(r'latency.*?(\d+\.?\d*)\s*ms', clean_line, re.I)
                if m:
                    self.current_latency = m.group(1) + "ms"
                    self.latency.emit(self.current_latency)

            self.log.emit(lang_manager.tr("process_exited"))
        except Exception as e:
            self.log.emit(f"{lang_manager.tr('exception')}: {str(e)}")
        finally:
            self.running = False
            self.status.emit(False)
            self.connection_status.emit("stopped")

    def stop(self):
        self.running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(2)
            except:
                self.process.kill()
        self.log.emit(lang_manager.tr("service_stopped"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = {}
        self.proxies = []
        self.thread = None
        self.setMinimumSize(900, 600)
        self.loadConfig()
        self.initUI()
        self.initMenu()
        
        # 加载保存的语言设置
        saved_lang = self.config.get("language", "zh_CN")
        lang_manager.load_language(saved_lang)
        self.applyLanguage()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        mainLayout = QVBoxLayout(central)

        self.tab = QTabWidget()
        self.simple_widget = self.simpleUI()
        self.adv_widget = self.advUI()
        self.tab.addTab(self.simple_widget, "")
        self.tab.addTab(self.adv_widget, "")
        mainLayout.addWidget(self.tab)

        self.logPanel = CollapsibleWidget("")
        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        self.logText.setMaximumHeight(220)
        self.logPanel.addWidget(self.logText)
        mainLayout.addWidget(self.logPanel)
        self.highlighter = LogHighlighter(self.logText.document())

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.statusLabel = StatusLabel()
        self.statusLabel.setStopped()
        self.statusBar.addWidget(self.statusLabel)
        self.statusLabelPerm = QLabel("")
        self.statusBar.addPermanentWidget(self.statusLabelPerm)

    def simpleUI(self):
        w = QWidget()
        layout = QHBoxLayout(w)

        self.simple_left_group = QGroupBox("")
        f = QFormLayout(self.simple_left_group)
        self.sip = QLineEdit("127.0.0.1")
        self.slp = QSpinBox()
        self.slp.setRange(1, 65535)
        self.slp.setValue(8080)
        self.srp = QSpinBox()
        self.srp.setRange(1, 65535)
        self.srp.setValue(80)
        self.stype = QComboBox()
        self.stype.addItems(["tcp", "udp", "http", "https"])

        self.sip_label = QLabel("")
        self.slp_label = QLabel("")
        self.srp_label = QLabel("")
        self.stype_label = QLabel("")

        f.addRow(self.sip_label, self.sip)
        f.addRow(self.slp_label, self.slp)
        f.addRow(self.srp_label, self.srp)
        f.addRow(self.stype_label, self.stype)

        self.simple_right_group = QGroupBox("")
        v = QVBoxLayout(self.simple_right_group)
        self.btnSS = QPushButton("")
        self.btnSP = QPushButton("")
        self.btnSP.setEnabled(False)
        self.simpleStatus = StatusLabel()
        self.simpleStatus.setStopped()
        v.addWidget(self.btnSS)
        v.addWidget(self.btnSP)
        v.addWidget(self.simpleStatus)
        v.addStretch()

        layout.addWidget(self.simple_left_group, 1)
        layout.addWidget(self.simple_right_group, 1)
        self.btnSS.clicked.connect(self.startSimple)
        self.btnSP.clicked.connect(self.stopAll)
        return w

    def advUI(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        left = QWidget()
        v = QVBoxLayout(left)
        tb = QHBoxLayout()
        self.btnAdd = QPushButton("")
        self.btnEdit = QPushButton("")
        self.btnDel = QPushButton("")
        self.btnEdit.setEnabled(False)
        self.btnDel.setEnabled(False)
        tb.addWidget(self.btnAdd)
        tb.addWidget(self.btnEdit)
        tb.addWidget(self.btnDel)
        tb.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["", "", "", "", "", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)

        v.addLayout(tb)
        v.addWidget(self.table)

        self.adv_right_group = QGroupBox("")
        rv = QVBoxLayout(self.adv_right_group)
        self.btnAS = QPushButton("")
        self.btnAP = QPushButton("")
        self.btnAP.setEnabled(False)
        self.advStatus = StatusLabel()
        self.advStatus.setStopped()
        rv.addWidget(self.btnAS)
        rv.addWidget(self.btnAP)
        rv.addWidget(self.advStatus)
        rv.addStretch()

        layout.addWidget(left, 3)
        layout.addWidget(self.adv_right_group, 1)

        self.btnAdd.clicked.connect(self.addProxy)
        self.btnEdit.clicked.connect(self.editProxy)
        self.btnDel.clicked.connect(self.delProxy)
        self.btnAS.clicked.connect(self.startAdv)
        self.btnAP.clicked.connect(self.stopAll)
        self.table.itemSelectionChanged.connect(self.onSel)
        self.table.customContextMenuRequested.connect(self.showMenu)
        return w

    def initMenu(self):
        self.menuBar().clear()

        lang_menu = self.menuBar().addMenu(lang_manager.tr("language"))
        
        # 获取可用语言列表
        for lang_code, display_name in lang_manager.get_available_languages().items():
            action = QAction(display_name, self)
            action.triggered.connect(lambda checked, lc=lang_code: self.switch_language(lc))
            lang_menu.addAction(action)

        cfg_menu = self.menuBar().addMenu(lang_manager.tr("configuration"))
        set_act = QAction(lang_manager.tr("settings"), self)
        set_act.triggered.connect(self.showConfig)
        cfg_menu.addAction(set_act)
        cfg_menu.addSeparator()
        exit_act = QAction(lang_manager.tr("exit"), self)
        exit_act.triggered.connect(self.close)
        cfg_menu.addAction(exit_act)

    def switch_language(self, lang_code):
        """切换语言并立即保存到配置"""
        if lang_manager.load_language(lang_code):
            self.config["language"] = lang_code
            self.saveConfig()  # 立即保存配置文件
            self.applyLanguage()

    def applyLanguage(self):
        """应用语言设置"""
        self.setWindowTitle(lang_manager.tr("title"))

        self.tab.setTabText(0, lang_manager.tr("simple_mode"))
        self.tab.setTabText(1, lang_manager.tr("advanced_mode"))

        self.logPanel.title_label.setText(lang_manager.tr("running_log"))

        self.simple_left_group.setTitle(lang_manager.tr("proxy_config"))
        self.simple_right_group.setTitle(lang_manager.tr("service_control"))

        self.sip_label.setText(lang_manager.tr("local_ip") + ":")
        self.slp_label.setText(lang_manager.tr("local_port") + ":")
        self.srp_label.setText(lang_manager.tr("remote_port") + ":")
        self.stype_label.setText(lang_manager.tr("protocol_type") + ":")

        self.btnSS.setText(lang_manager.tr("start_service"))
        self.btnSP.setText(lang_manager.tr("stop_service"))

        self.adv_right_group.setTitle(lang_manager.tr("service_control"))

        self.btnAdd.setText(lang_manager.tr("add"))
        self.btnEdit.setText(lang_manager.tr("edit"))
        self.btnDel.setText(lang_manager.tr("delete"))
        self.btnAS.setText(lang_manager.tr("start_service"))
        self.btnAP.setText(lang_manager.tr("stop_service"))

        self.table.setHorizontalHeaderLabels([
            lang_manager.tr("proxy_name"), lang_manager.tr("protocol_type"),
            lang_manager.tr("local_address"), lang_manager.tr("remote_port"),
            lang_manager.tr("status"), lang_manager.tr("operation")
        ])

        self.statusLabelPerm.setText(lang_manager.tr("frpc_manager"))

        self.initMenu()
        self.refreshTable()

        if self.thread and self.thread.isRunning():
            if self.thread.has_connected:
                self.statusLabel.setConnected(self.thread.current_latency if self.thread.current_latency else "")
            else:
                self.statusLabel.setConnecting()
        else:
            self.statusLabel.setStopped()
            self.simpleStatus.setStopped()
            self.advStatus.setStopped()

    def loadConfig(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.config = d.get("config", {})
                    self.proxies = d.get("proxies", [])
            else:
                # 配置文件不存在，创建默认配置并保存
                self.config = DEFAULT_SERVER_CONFIG.copy()
                self.proxies = [{
                    "name": "Test", "type": "tcp", "localIP": "127.0.0.1",
                    "localPort": 80, "remotePort": 8080, "enabled": True
                }]
                self.saveConfig()
        except Exception as e:
            print(f"Load config error: {e}")
            self.config = DEFAULT_SERVER_CONFIG.copy()
            self.proxies = [{
                "name": "Test", "type": "tcp", "localIP": "127.0.0.1",
                "localPort": 80, "remotePort": 8080, "enabled": True
            }]
            self.saveConfig()

    def saveConfig(self):
        d = {"config": self.config, "proxies": self.proxies}
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Save config error: {e}")

    def showConfig(self):
        d = ConfigDialog(self.config, self)
        if d.exec_():
            self.saveConfig()

    def addProxy(self):
        d = ProxyDialog(parent=self)
        if d.exec_():
            self.proxies.append(d.data)
            self.refreshTable()
            self.saveConfig()

    def editProxy(self):
        row = self.table.currentRow()
        if row < 0:
            return
        d = ProxyDialog(self.proxies[row], self)
        if d.exec_():
            self.proxies[row] = d.data
            self.refreshTable()
            self.saveConfig()

    def delProxy(self):
        row = self.table.currentRow()
        if row < 0:
            return
        del self.proxies[row]
        self.refreshTable()
        self.saveConfig()

    def onSel(self):
        e = self.table.currentRow() >= 0
        self.btnEdit.setEnabled(e)
        self.btnDel.setEnabled(e)

    def showMenu(self, pos):
        """显示右键菜单"""
        item = self.table.itemAt(pos)
        if item is not None:
            menu = QMenu()
            edit_action = menu.addAction(lang_manager.tr("edit"))
            delete_action = menu.addAction(lang_manager.tr("delete"))
            action = menu.exec_(self.table.mapToGlobal(pos))
            if action == edit_action:
                self.editProxy()
            elif action == delete_action:
                self.delProxy()

    def refreshTable(self):
        """刷新表格"""
        self.table.setRowCount(len(self.proxies))
        for i, p in enumerate(self.proxies):
            enabled = p.get("enabled", True)
            status_text = lang_manager.tr("enabled") if enabled else lang_manager.tr("disabled")
            status_color = "#4CAF50" if enabled else "#9E9E9E"

            items = [
                QTableWidgetItem(p.get("name", "")),
                QTableWidgetItem(p.get("type", "tcp")),
                QTableWidgetItem(f"{p.get('localIP')}:{p.get('localPort')}"),
                QTableWidgetItem(str(p.get('remotePort'))),
            ]

            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QColor(status_color))
            status_item.setTextAlignment(Qt.AlignCenter)

            for col, it in enumerate(items):
                it.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, col, it)

            self.table.setItem(i, 4, status_item)

            # 开关按钮
            switch_widget = QWidget()
            switch_layout = QHBoxLayout(switch_widget)
            switch_layout.setAlignment(Qt.AlignCenter)
            switch_layout.setContentsMargins(0, 0, 0, 0)

            toggle_text = lang_manager.tr("turn_off") if enabled else lang_manager.tr("turn_on")
            toggle = QPushButton(toggle_text)
            toggle.setStyleSheet(f"background-color: {'#4CAF50' if enabled else '#F44336'}; color: white; padding: 3px 8px; border-radius: 3px;")
            toggle.clicked.connect(lambda checked, row=i: self.toggleProxyEnabled(row))

            switch_layout.addWidget(toggle)
            self.table.setCellWidget(i, 5, switch_widget)

    def toggleProxyEnabled(self, row):
        if 0 <= row < len(self.proxies):
            self.proxies[row]["enabled"] = not self.proxies[row]["enabled"]
            self.refreshTable()
            self.saveConfig()

    def genConfig(self, simple=True):
        lines = []
        c = self.config
        lines.append(f'serverAddr = "{c.get("serverAddr", "")}"')
        lines.append(f'serverPort = {c.get("serverPort", 7000)}')
        lines.append(f'auth.token = "{c.get("auth_token", "")}"')
        w = c.get("webServer", {})
        if w.get("enabled"):
            lines.append(f'webServer.addr = "{w.get("addr", "127.0.0.1")}"')
            lines.append(f'webServer.port = {w.get("port", 7400)}')
            lines.append(f'webServer.user = "{w.get("user", "")}"')
            lines.append(f'webServer.password = "{w.get("password", "")}"')
        lines.append("")
        if simple:
            lines.append("[[proxies]]")
            lines.append(f'name = "simple"')
            lines.append(f'type = "{self.stype.currentText()}"')
            lines.append(f'localIP = "{self.sip.text()}"')
            lines.append(f'localPort = {self.slp.value()}')
            lines.append(f'remotePort = {self.srp.value()}')
        else:
            for p in self.proxies:
                if not p.get("enabled", True):
                    continue
                lines.append("[[proxies]]")
                lines.append(f'name = "{p.get("name", "")}"')
                lines.append(f'type = "{p.get("type", "tcp")}"')
                lines.append(f'localIP = "{p.get("localIP", "127.0.0.1")}"')
                lines.append(f'localPort = {p.get("localPort", 0)}')
                lines.append(f'remotePort = {p.get("remotePort", 0)}')
                lines.append("")
        return "\n".join(lines)

    def setAllButtons(self, running):
        self.btnSS.setEnabled(not running)
        self.btnSP.setEnabled(running)
        self.btnAS.setEnabled(not running)
        self.btnAP.setEnabled(running)

    def startSimple(self):
        if not self.config.get("serverAddr"):
            QMessageBox.warning(self, lang_manager.tr("warning"), lang_manager.tr("warning_server_addr"))
            return
        with open(TEMP_CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(self.genConfig(True))
        self.startThread(TEMP_CONFIG_FILE)

    def startAdv(self):
        if not self.config.get("serverAddr"):
            QMessageBox.warning(self, lang_manager.tr("warning"), lang_manager.tr("warning_server_addr"))
            return
        if not any(p.get("enabled", True) for p in self.proxies):
            QMessageBox.warning(self, lang_manager.tr("warning"), lang_manager.tr("warning_no_proxy"))
            return
        with open(TEMP_CONFIG_FILE_ADV, "w", encoding="utf-8") as f:
            f.write(self.genConfig(False))
        self.startThread(TEMP_CONFIG_FILE_ADV)

    def startThread(self, cfg):
        self.stopAll()
        self.thread = FRPCThread()
        self.thread.cfg = cfg
        self.thread.log.connect(self.appendLog)
        self.thread.status.connect(self.updateStatus)
        self.thread.latency.connect(self.updateLatency)
        self.thread.connection_status.connect(self.updateConnectionStatus)
        self.thread.start()
        self.setAllButtons(True)

    def stopAll(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait(2000)
        self.setAllButtons(False)
        self.statusLabel.setStopped()
        self.simpleStatus.setStopped()
        self.advStatus.setStopped()

    def appendLog(self, msg):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logText.append(f"[{t}] {msg}")
        scrollbar = self.logText.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def updateStatus(self, run):
        if not run:
            self.statusLabel.setStopped()
            self.simpleStatus.setStopped()
            self.advStatus.setStopped()
            self.setAllButtons(False)

    def updateLatency(self, lat):
        pass

    def updateConnectionStatus(self, status):
        if status == "connecting":
            self.statusLabel.setConnecting()
            self.simpleStatus.setConnecting()
            self.advStatus.setConnecting()
        elif status == "connected":
            if self.thread and hasattr(self.thread, 'current_latency') and self.thread.current_latency:
                latency = self.thread.current_latency
                self.statusLabel.setConnected(latency)
                self.simpleStatus.setConnected(latency)
                self.advStatus.setConnected(latency)
            else:
                self.statusLabel.setConnected()
                self.simpleStatus.setConnected()
                self.advStatus.setConnected()
        elif status == "failed":
            self.statusLabel.setFailed()
            self.simpleStatus.setFailed()
            self.advStatus.setFailed()
        elif status == "stopped":
            self.statusLabel.setStopped()
            self.simpleStatus.setStopped()
            self.advStatus.setStopped()

    def closeEvent(self, e):
        self.saveConfig()
        self.stopAll()
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Microsoft YaHei", 9))

    if os.path.exists(ICON_FILE):
        app.setWindowIcon(QIcon(ICON_FILE))

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
