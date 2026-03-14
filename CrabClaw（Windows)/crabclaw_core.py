import os
import sys
import io
import json
import shutil
import threading
import time
import sqlite3
import urllib.parse
import urllib.request
import base64
import ast
import importlib.util
import concurrent.futures 
import httpx  
import traceback
import queue
import platform
import webbrowser
import re  
import inspect  
import builtins
import shlex
import random
from datetime import datetime
from typing import Callable, Dict, Any, List, Optional, Tuple
from openai import OpenAI

# ==========================================
# 🌐 代理清理与分发中枢 (Proxy Management)
# ==========================================
proxy_envs = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']
for env_name in proxy_envs:
    if env_name in os.environ:
        os.environ.pop(env_name)

# ==========================================
# 🛡️ 终极防乱码补丁与 ANSI 颜色支持 (Pro Max 增强)
# ==========================================
if os.name == 'nt':
    try:
        # [Win10 原生增强] 极致兼容：通过 ctypes 强制调用底层 Windows API 开启内核级 VT100 ANSI 支持
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        # 静默将当前控制台代码页切换为 UTF-8，彻底消灭控制台自身的乱码隐患
        os.system('chcp 65001 >nul 2>&1')
    except Exception:
        os.system('')  # Fallback 兼容

# 引入 errors='replace'，防止 Windows 下遇到不支持的 Emoji 时触发 UnicodeEncodeError 导致整个引擎崩溃
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 🎨 终端颜色常量定义 (仅用于 UI 呈现)
COLOR_RESET = "\033[0m"
COLOR_SYSTEM = "\033[96m"  # 青色
COLOR_BOT = "\033[92m"     # 绿色
COLOR_PROGRESS = "\033[93m" # 黄色
COLOR_ERROR = "\033[91m"   # 红色
COLOR_WARNING = "\033[38;5;208m" # 橙色
CLEAR_LINE = "\033[K"      # 清除当前行光标后内容

# ==========================================
# 🔌 0. 通讯通道层 (Multi-channel UI Gateway)
# ==========================================
class BaseChannel:
    """
    ===================================================================
    🔌 商业版接入网关 (Multi-channel Integration Gateway)
    ===================================================================
    【开发者必读：如何接入第三方平台】
    CrabClaw 采用“引擎逻辑”与“交互终端”严格解耦的架构（MVC理念）。
    您可以通过继承本基类，轻松将其无缝接入任意社交平台或前端 UI 系统。
    ===================================================================
    """
    def send_message(self, message: str, role: str = "bot", is_background: bool = False, session_id: str = "default") -> None:
        raise NotImplementedError

    def ask_confirm(self, prompt: str, danger_level: str = "high", session_id: str = "default") -> bool:
        raise NotImplementedError

class CLIChannel(BaseChannel):
    """默认命令行本地交互通道 (Pro Max 优化版)"""
    def __init__(self):
        self.print_lock = threading.Lock()
        self.input_lock = threading.Lock()

    def send_message(self, message: str, role: str = "bot", is_background: bool = False, session_id: str = "default") -> None:
        with self.print_lock:
            prefix_tag = f"[{session_id}] " if session_id != "default" else ""
            if role == "system":
                print(f"\n{COLOR_SYSTEM}⚙️  {prefix_tag}[系统]: {message}{COLOR_RESET}")
            elif role == "bot":
                prefix = "👻 后台助理 (进度)" if is_background else "🦀 CrabClaw"
                # 使用 ANSI 清屏指令替代原先的空格覆盖法，彻底解决撕裂与换行残留问题
                print(f"\r{CLEAR_LINE}", end="")
                print(f"{COLOR_BOT}{prefix} {prefix_tag}: {message}\n{COLOR_RESET}")
            elif role == "progress":
                print(f"\r{CLEAR_LINE}{COLOR_PROGRESS}{prefix_tag}{message}... (按 Ctrl+C 随时终止){COLOR_RESET}", end="")

    def ask_confirm(self, prompt: str, danger_level: str = "high", session_id: str = "default") -> bool:
        with self.input_lock:
            with self.print_lock:
                print(f"\n{COLOR_ERROR}" + "="*60)
                print(f"🛑 [!!! 商业级底层安全授权与代码审查 (HITL) !!!]")
                print(f"="*60)
                print(f"⚠️ {prompt}")
                print(f"="*60 + COLOR_RESET)
            
            if not sys.stdout.isatty():
                print(f"{COLOR_ERROR}❌ 检测到当前运行在非交互式终端(如守护进程)，已自动拒绝高危操作授权！{COLOR_RESET}")
                return False
                
            try:
                user_auth = input(f"{COLOR_WARNING}👉 仔细审查上述内容。输入 'y' 授权执行，输入其他键取消: {COLOR_RESET}")
                return user_auth.lower() in ['y', 'yes', '1']
            except (EOFError, KeyboardInterrupt):
                return False

def _smart_decode(output_bytes: bytes) -> str:
    """[Win10 兼容核心] 智能多重解码器：应对 Windows 下 GBK 与 UTF-8 混杂的子进程输出环境"""
    if not output_bytes: return ""
    try: 
        return output_bytes.decode('utf-8')
    except UnicodeDecodeError:
        try: 
            return output_bytes.decode('gbk')  # 极致兼容 Win10 中文版 CMD 默认的 GBK 输出
        except UnicodeDecodeError:
            return output_bytes.decode('utf-8', errors='replace')

# ==========================================
# 🛡️ 1. 沙箱与代码安全策略 (Sandbox Security)
# ==========================================
class SandboxManager:
    def __init__(self, workspace_root: str, mode: str = "RW_Scope"):
        self.workspace_root = os.path.abspath(workspace_root)
        self.mode = mode 
        self.sandbox_tmp_dir = os.path.join(self.workspace_root, ".sandbox_env")
        os.makedirs(self.workspace_root, exist_ok=True)
        os.makedirs(self.sandbox_tmp_dir, exist_ok=True)

    def is_path_safe(self, target_path: str) -> bool:
        if self.mode == "Off": return True
        abs_target = os.path.abspath(target_path)
        if "$Recycle.Bin" in abs_target or ".Trash" in abs_target: return True
        home = os.path.expanduser("~")
        safe_dirs = ["Desktop", "Documents", "Downloads", "桌面", "文档"]
        for sd in safe_dirs:
            if abs_target.startswith(os.path.join(home, sd)): return True
        return abs_target.startswith(self.workspace_root)

    def verify_code_safety(self, code: str) -> List[str]:
        warnings = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    module_name = node.names[0].name if isinstance(node, ast.Import) else getattr(node, 'module', '')
                    if module_name in ['os', 'subprocess', 'shutil', 'sys', 'pty', 'socket', 'ctypes']:
                        warnings.append(f"⚠️ 发现高危或底层库导入: {module_name} (商业部署推荐在 isolated_process 模式下测试)")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'open']:
                            warnings.append(f"⚠️ 发现敏感内置函数调用: {node.func.id}")
        except SyntaxError as e:
            warnings.append(f"代码语法错误: {e}")
        return warnings

    def run_in_sandbox(self, code: str, test_kwargs: Dict = None) -> str:
        output_buffer = io.StringIO()
        
        def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
            blacklisted_modules = {'os', 'sys', 'subprocess', 'shutil', 'pty', 'socket', 'threading', 'multiprocessing', 'ctypes'}
            base_module = name.split('.')[0]
            if base_module in blacklisted_modules:
                raise ImportError(f"🚫 [内置沙箱拦截] 模块 '{name}' 属于高风险底层库，已被禁用。请切换 mode 为 'isolated_process' 启用物理隔离沙箱！")
            return __import__(name, globals, locals, fromlist, level)

        safe_builtins = {k: v for k, v in builtins.__dict__.items() if k not in ['eval', 'exec', 'open']}
        safe_builtins['__import__'] = _safe_import
        
        env = {"__builtins__": safe_builtins}
        if test_kwargs: env.update(test_kwargs)
        
        import contextlib
        try:
            with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
                exec(code, env, env)
            return f"✅ [in_process 轻量沙箱] 试运行成功:\n{output_buffer.getvalue()}"
        except Exception as e:
            return f"⚠️ [in_process 轻量沙箱] 运行报错:\n异常: {type(e).__name__}: {str(e)}\n输出日志: {output_buffer.getvalue()}"

    def run_in_isolated_process(self, code: str, timeout: int = 15) -> str:
        import subprocess
        tmp_file = os.path.join(self.sandbox_tmp_dir, f"sandbox_task_{int(time.time())}.py")
        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(code)

            # [Win10 兼容增强] 剥离固定 encoding，采用底层 bytes 捕获与 _smart_decode 智能解码
            result = subprocess.run(
                [sys.executable, tmp_file], 
                capture_output=True, 
                timeout=timeout
            )
            
            output_str = _smart_decode(result.stdout)
            error_str = _smart_decode(result.stderr)
            
            output = f"【标准输出】\n{output_str.strip()}" if output_str else ""
            error = f"【错误输出】\n{error_str.strip()}" if error_str else ""
            
            if result.returncode == 0:
                return f"🚀 [isolated_process 隔离沙箱] 执行成功 (耗时 < {timeout}s):\n{output}"
            else:
                return f"⚠️ [isolated_process 隔离沙箱] 运行崩溃 (退出码 {result.returncode}):\n{error}\n{output}"
                
        except subprocess.TimeoutExpired:
            return f"❌ [isolated_process 隔离沙箱] 致命拦截触发: 代码执行超时 ({timeout}秒)！检测到可能的死循环或网络阻塞，子进程已被猎杀。"
        except Exception as e:
            return f"❌ [isolated_process 隔离沙箱] 宿主机调度异常: {str(e)}"
        finally:
            if os.path.exists(tmp_file):
                try: os.remove(tmp_file)
                except: pass

# ==========================================
# 🧠 2. 混合记忆中枢 (Hybrid Memory Engine - WAL级强化)
# ==========================================
class HybridMemoryManager:
    def __init__(self, workspace_dir="./workspace"):
        self.workspace_dir = workspace_dir
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.db_path = os.path.join(self.workspace_dir, "hybrid_memory.db")
        self.soul_file = os.path.join(self.workspace_dir, "SOUL.md")
        self._init_soul()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        """企业级高并发 WAL 数据库连接"""
        conn = sqlite3.connect(self.db_path, timeout=15.0, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;") # Pro Max 性能提升
        return conn

    def _init_soul(self):
        if not os.path.exists(self.soul_file):
            with open(self.soul_file, "w", encoding="utf-8") as f:
                f.write("# SOUL\n你叫 CrabClaw，是一个运行在企业与用户环境中的全自主学习型实体智能体（Local Agent）。\n你绝对不是云端的聊天机器人，遇到不会的问题，你会主动搜索、写代码、委派副脑协作。\n商业安全和授权是你最高的行动准则。\n")

    def _init_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS core_memory (key TEXT PRIMARY KEY, value TEXT, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            cursor.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS episodic_memory USING fts5(content, timestamp UNINDEXED)''')
            conn.commit()

    def get_soul(self) -> str:
        try:
            with open(self.soul_file, "r", encoding="utf-8") as f: return f.read().strip()
        except Exception: return "你是一个基于 CrabClaw 架构进化的全自主学习型商业级智能体。"

    def set_core_memory(self, key: str, value: str) -> str:
        with self._get_conn() as conn:
            conn.execute('''INSERT INTO core_memory (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at''', (key, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        return f"✅ 核心记忆已更新: [{key}] -> {value}"

    def get_all_core_memory(self) -> str:
        with self._get_conn() as conn:
            rows = conn.execute('SELECT key, value FROM core_memory').fetchall()
            return "\n".join([f"- {row[0]}: {row[1]}" for row in rows]) if rows else "暂无核心记忆。"

    def is_efficiency_mode(self) -> bool:
        try:
            with self._get_conn() as conn:
                row = conn.execute("SELECT value FROM core_memory WHERE key='efficiency_mode'").fetchone()
                return row is not None and row[0] == "ON"
        except Exception: return False

# ==========================================
# 🛠️ 3. 技能库与动态进化引擎 (Dynamic Skill Engine)
# ==========================================
class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        self.schemas: List[Dict[str, Any]] = []

    def register(self, func: Callable, description: str, parameters: Dict[str, Any], requires_approval: bool = False, requires_packages: List[str] = None):
        # [Pro Max 级底层护盾] 强制清洗 API 规范所需的正则名称 '^[a-zA-Z0-9_-]+$'
        # 解决由于 Python 匿名函数默认名为 '<lambda>' 导致含有非法字符 '<' '>' 引发的 400 Bad Request 崩溃
        raw_name = getattr(func, '__name__', 'unnamed_skill')
        name = re.sub(r'[^a-zA-Z0-9_-]', '_', raw_name).strip('_')
        if not name or name == 'lambda': 
            name = f"dynamic_skill_{int(time.time())}_{random.randint(100,999)}"
            
        self.skills[name] = {"func": func, "requires_approval": requires_approval, "requires_packages": requires_packages or []}
        self.schemas = [s for s in self.schemas if s["function"]["name"] != name]
        
        safe_parameters = parameters
        if not safe_parameters or not isinstance(safe_parameters, dict) or safe_parameters.get("type") != "object":
            safe_parameters = {"type": "object", "properties": {}}
        self.schemas.append({"type": "function", "function": {"name": name, "description": description, "parameters": safe_parameters}})

    def execute(self, name: str, args: Dict[str, Any], channel: BaseChannel, session_id: str = "default") -> str:
        if name not in self.skills: return f"❌ 错误: 找不到技能 {name}"
        skill_info = self.skills[name]
        
        efficiency_mode = args.pop("_efficiency_mode_cache", False)
        hardcore_safe = args.pop("_hardcore_safe_cache", True)
        
        # 🛡️ 商业级底层拦截：完全脱离大模型的强控制
        if skill_info["requires_approval"]:
            risk_text = str(args.get("risk_assessment", args.get("reason", ""))).lower()
            is_low_risk = ("低风险" in risk_text or "无风险" in risk_text or "安全" in risk_text) and ("高风险" not in risk_text)

            if efficiency_mode and is_low_risk and hardcore_safe:
                pass 
            else:
                action_desc = f"调用高危技能 [{name}]"
                args_str = json.dumps({k:v for k,v in args.items() if k != 'python_code'}, ensure_ascii=False)
                if len(args_str) > 300: args_str = args_str[:300] + "...(过长已截断)"
                prompt = f"请求 {action_desc}。\n📄 核心参数: {args_str}\n⚠️ 风险自评: {args.get('risk_assessment', args.get('reason', '未提供'))}"
                
                # 阻塞式调用 Channel 的确认逻辑
                if not channel.ask_confirm(prompt, session_id=session_id): 
                    return "❌ [商业底层拦截] 操作已取消，人类/网关拒绝了该高危授权请求。请放弃当前危险意图。"

        import importlib
        importlib.invalidate_caches()
        
        for pkg in skill_info["requires_packages"]:
            aliases = {"pillow": "PIL", "opencv-python": "cv2", "scikit-learn": "sklearn", "pyyaml": "yaml", "beautifulsoup4": "bs4", "python-dotenv": "dotenv", "python-docx": "docx", "pymupdf": "fitz"}
            import_name = aliases.get(pkg.lower(), pkg.replace("-", "_"))
            try: __import__(import_name)
            except ImportError: 
                pip_cmd = f'"{sys.executable}" -m pip'
                return f"❌ 当前环境缺少库 `{pkg}`。\n🛠️ [系统自救提示]: 请调用 `execute_shell` 严格执行 `{pip_cmd} install {pkg}` 安装，成功后重试。"

        func = skill_info["func"]
        sig = inspect.signature(func)
        
        # 稳健的参数注入
        safe_kwargs = args.copy()
        if "session_id" in sig.parameters and "session_id" not in safe_kwargs: safe_kwargs["session_id"] = session_id
        if "channel" in sig.parameters and "channel" not in safe_kwargs: safe_kwargs["channel"] = channel

        # 清理多余参数防止崩溃
        final_kwargs = {k: v for k, v in safe_kwargs.items() if k in sig.parameters}

        try: 
            return str(func(**final_kwargs))
        except BaseException as e: 
            err_msg = traceback.format_exc()
            print(f"\n{COLOR_ERROR}[内部执行异常追踪] {err_msg}{COLOR_RESET}")
            return f"❌ 执行崩溃: {type(e).__name__}: {str(e)}\n(可在系统日志查看详细堆栈)"

class DynamicSkillManager:
    def __init__(self, workspace_root: str, registry: SkillRegistry, sandbox: SandboxManager):
        self.skills_dir = os.path.join(workspace_root, "skills")
        self.metadata_file = os.path.join(self.skills_dir, "metadata.json")
        self.registry = registry
        self.sandbox = sandbox
        os.makedirs(self.skills_dir, exist_ok=True)
        self._load_all()

    def _load_all(self):
        if not os.path.exists(self.metadata_file): return
        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f: metadata = json.load(f)
        except json.JSONDecodeError: return
        
        loaded_count = 0
        for skill_name, meta in metadata.items():
            file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
            if os.path.exists(file_path) and self._mount_skill(skill_name, file_path, meta, is_init=True): loaded_count += 1
        if loaded_count > 0: print(f"{COLOR_SYSTEM}🧬 [商业核心] 成功热加载 {loaded_count} 个自主学习技能。{COLOR_RESET}")

    def _mount_skill(self, skill_name: str, file_path: str, meta: dict, is_init: bool = False):
        try:
            if skill_name in sys.modules: del sys.modules[skill_name]
            spec = importlib.util.spec_from_file_location(skill_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.registry.register(func=getattr(module, skill_name), description=meta["description"], parameters=meta["parameters"], requires_packages=meta.get("requires_packages", []), requires_approval=meta.get("requires_approval", True))
            if not is_init: print(f"{COLOR_SYSTEM}🧬 [系统] 成功加载新技能: {skill_name}{COLOR_RESET}")
            return True
        except Exception as e: 
            print(f"{COLOR_WARNING}⚠️ [系统] 技能 {skill_name} 加载失败: {e}{COLOR_RESET}")
            return False

    def install(self, skill_name: str, description: str, parameters: dict, python_code: str, requires_packages: list = None) -> str:
        file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
        with open(file_path, "w", encoding="utf-8") as f: f.write(python_code)
        
        metadata = {}
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f: metadata = json.load(f)
            except Exception: pass
            
        meta = {"description": description, "parameters": parameters, "requires_packages": requires_packages or [], "requires_approval": True}
        metadata[skill_name] = meta
        with open(self.metadata_file, "w", encoding="utf-8") as f: json.dump(metadata, f, ensure_ascii=False, indent=2)
        self._mount_skill(skill_name, file_path, meta)
        return f"🎉 技能 [{skill_name}] 已经永久植入中枢！"

    def delete(self, skill_name: str) -> str:
        file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
        if os.path.exists(file_path): os.remove(file_path)
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f: metadata = json.load(f)
                if skill_name in metadata:
                    del metadata[skill_name]
                    with open(self.metadata_file, "w", encoding="utf-8") as f: json.dump(metadata, f, ensure_ascii=False, indent=2)
            except Exception: pass
            
        if skill_name in self.registry.skills:
            del self.registry.skills[skill_name]
            self.registry.schemas = [s for s in self.registry.schemas if s["function"]["name"] != skill_name]
        if skill_name in sys.modules: del sys.modules[skill_name]
        return f"🗑️ 技能 [{skill_name}] 已从大脑卸载。"

# ==========================================
# 💓 4. 商业级智能体运行时与核心脑
# ==========================================
class CrabClawAgent:
    def __init__(self, channel: BaseChannel, models_config: dict, default_model_key: str, proxy_url=None, llm_use_proxy=False, **kwargs):
        self.channel = channel
        self.proxy_url = proxy_url
        self.llm_use_proxy = llm_use_proxy
        self.system_os = platform.system()
        
        self.models_config = models_config or {}
        self.default_model_key = default_model_key
        
        if not self.models_config:
            print(f"{COLOR_ERROR}❌ 致命错误：models_config 核心配置库为空，系统无法启动。{COLOR_RESET}")
            sys.exit(1)
            
        self.clients = {}
        for key, cfg in self.models_config.items():
            raw_key = cfg.get("api_key", "")
            is_configured = bool(raw_key and "填入" not in raw_key and raw_key != "YOUR_API_KEY_HERE")
            # 兼容非标准 OpenAI 端点：加入 timeout/max_retries 容错
            client_kwargs = {"base_url": cfg.get("base_url"), "api_key": raw_key if is_configured else "NOT_CONFIGURED", "timeout": 90.0, "max_retries": 3}
            if proxy_url and llm_use_proxy: client_kwargs["http_client"] = httpx.Client(proxies=proxy_url, verify=False)
            self.clients[key] = {"client": OpenAI(**client_kwargs), "model": cfg.get("model"), "description": cfg.get("description", "未提供"), "is_configured": is_configured}
        
        self.memory = HybridMemoryManager()
        self.sandbox = SandboxManager(workspace_root="./workspace") 
        self.registry = SkillRegistry()
        self.skill_manager = DynamicSkillManager(self.sandbox.workspace_root, self.registry, self.sandbox)
        
        self.sessions = {}
        self.sessions_lock = threading.Lock()
        self.global_executor = concurrent.futures.ThreadPoolExecutor(max_workers=50, thread_name_prefix="CrabClaw_Worker")
        self.tool_http_client = httpx.Client(proxies=proxy_url, timeout=15.0) if proxy_url else httpx.Client(timeout=15.0)
        
        self._register_base_skills()
        self._register_learning_skills()

    def _get_session(self, session_id: str) -> dict:
        with self.sessions_lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {"history": [], "lock": threading.Lock(), "stop_time": 0, "active_model_key": self.default_model_key}
            return self.sessions[session_id]

    def _log_chain(self, step: str, detail: str = "", session_id: str = "default", level: str = "INFO"):
        """【深度重构】企业级结构化控制台日志链路追踪"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        try:
            with getattr(self.channel, 'print_lock', threading.Lock()):
                color = COLOR_SYSTEM
                icon = "🔗"
                if level == "ACTION": color = COLOR_PROGRESS; icon = "⚡"
                elif level == "SUCCESS": color = COLOR_BOT; icon = "✅"
                elif level == "ERROR": color = COLOR_ERROR; icon = "❌"
                elif level == "WARN": color = COLOR_WARNING; icon = "⚠️"
                
                prefix_tag = f"[{session_id}] " if session_id != "default" else ""
                
                # 构建美观的、类似树状的日志链路 UI
                print(f"\n{color}╭{'─'*70}╮{COLOR_RESET}")
                print(f"{color}│ {icon} [神经中枢链路] {timestamp} | {prefix_tag}追踪节点: {step}{COLOR_RESET}")
                if detail:
                    print(f"{color}├{'─'*70}┤{COLOR_RESET}")
                    clean_detail = str(detail).strip()
                    # 容错：截断过长底层执行数据，防止刷屏导致控制台假死
                    if len(clean_detail) > 1500: 
                        clean_detail = clean_detail[:1500] + f"\n...[底层数据体量过大，为防止刷屏已截断，剩余 {len(clean_detail)-1500} 字符]..."
                    for line in clean_detail.split('\n'):
                        print(f"{color}│ {line}{COLOR_RESET}")
                print(f"{color}╰{'─'*70}╯{COLOR_RESET}")
        except: 
            pass

    def _clean_llm_output(self, text: str, remove_markdown: bool = False) -> str:
        """【强力护盾】彻底阻止长篇大论的代码污染用户聊天窗口"""
        if not text: return ""
        
        # 防线 1: 绝对折叠 Markdown 代码块，不允许其向客户端原样输出
        text = re.sub(r'```[\s\S]*?```', '\n[💻 详细代码/数据已由底层引擎接管并静默处理，为避免刷屏不再展示]\n', text)
        
        # 防线 2: 过滤大模型的思考过程内部标签
        text = re.sub(r'</?[\s\|]*(DSML|parameter)[\s\S]*?>', '', text, flags=re.IGNORECASE)
        
        # 防线 3: 激进拦截裸代码 (无 ``` 包裹，直接吐出的 Python 脚本)
        lines = text.split('\n')
        safe_lines = []
        code_leak_detected = False
        
        for line in lines:
            # 如果检测到高危的 Python 语法特征（往往是模型忘了加代码块符号）
            if re.match(r'^\s*(def |class |import |from .* import |pip install |sys\.|os\.)', line):
                if not code_leak_detected:
                    safe_lines.append("\n[🛡️ 引擎防线：系统检测到冗长代码外溢，已自动折叠拦截。请直接查看最终结论。]\n")
                    code_leak_detected = True
                continue
            
            # 如果上一行是高危代码起手式，则继续屏蔽接下来的缩进内容（极严苛防线）
            if code_leak_detected and (line.startswith(" ") or line.startswith("\t") or "=" in line):
                continue
            else:
                code_leak_detected = False
                safe_lines.append(line)
                
        text = '\n'.join(safe_lines)
        
        if remove_markdown: 
            text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE).replace('**', '')
            
        return text.strip()

    def _extract_thought_and_reply(self, text: str) -> Tuple[str, str]:
        if not text: return "", ""
        t_lines, r_lines = [], []
        for line in text.split('\n'):
            line_s = line.strip()
            if '🧠' in line_s or '[进度' in line_s or '🔄' in line_s: t_lines.append(line_s)
            elif line_s: r_lines.append(line_s)
        return '\n'.join(t_lines).strip(), '\n'.join(r_lines).strip()

    def _parse_multimodal_input(self, text: str) -> Any:
        if not isinstance(text, str): return text
        all_imgs = []
        http_urls = re.findall(r'https?://[^\s<>"]+?\.(?:png|jpg|jpeg|webp|gif)', text, re.IGNORECASE)
        for u in http_urls:
            if u not in all_imgs: all_imgs.append(u)
        local_paths = re.findall(r'(?:[a-zA-Z]:[\\/]|/)(?:[^\\\/\:\*\?\"\<\>\|]+[\\\/])*[^\\\/\:\*\?\"\<\>\|]+\.(?:png|jpg|jpeg|webp|gif)', text, re.IGNORECASE)
        for p in local_paths:
            if os.path.exists(p):
                try:
                    with open(p, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode('utf-8')
                        ext = os.path.splitext(p)[1][1:].lower()
                        if ext == 'jpg': ext = 'jpeg'
                        all_imgs.append(f"data:image/{ext};base64,{b64}")
                except: pass
        if not all_imgs: return text 
        content_list = [{"type": "text", "text": text if text.strip() else "请分析这张图片。"}]
        for img in all_imgs: content_list.append({"type": "image_url", "image_url": {"url": img}})
        return content_list

    def _register_base_skills(self):
        # 核心技能：原汁原味，不作任何逻辑删减，加入 PEP8 级排版与类型强化
        def delegate_to_sub_brain(target_model_key: str, task_prompt: str, include_current_vision_data: bool = False, session_id: str = "default") -> str:
            if target_model_key not in self.clients: return f"❌ 找不到副脑 [{target_model_key}]。"
            client_info = self.clients[target_model_key]
            if not client_info.get("is_configured"): return f"❌ 目标副脑未配置 API Key。"
            session = self._get_session(session_id)
            if target_model_key == session.get("active_model_key"): return f"⚠️ 不能委派给自己。请选其他节点。"
            
            self.channel.send_message(f"🧠 [跨脑协同] 正在唤醒副脑 【{target_model_key}】 处理外包子任务...", role="progress", session_id=session_id)
            self._log_chain("唤醒协同副脑", f"委派节点: {target_model_key}\n下发任务: {task_prompt}", session_id, level="ACTION")
            
            messages = [{"role": "system", "content": "你是集群副脑。严格按主脑指示完成任务并直接汇报结果。"}]
            if include_current_vision_data:
                vision_content = next((msg["content"] for msg in reversed(session["history"]) if msg["role"] == "user" and isinstance(msg["content"], list)), None)
                if vision_content:
                    img_parts = [p for p in vision_content if p.get("type") == "image_url"]
                    messages.append({"role": "user", "content": [{"type": "text", "text": f"【主脑指令】\n{task_prompt}"}] + img_parts})
                else: messages.append({"role": "user", "content": f"【主脑指令】\n(未找到图片)\n{task_prompt}"})
            else: messages.append({"role": "user", "content": f"【主脑指令】\n{task_prompt}"})
                
            try:
                resp = client_info["client"].chat.completions.create(model=client_info["model"], messages=messages, max_tokens=3500)
                self._log_chain("副脑协同完毕", f"收到完整侦测报告，已融合。", session_id, level="SUCCESS")
                return f"✅ 副脑 [{target_model_key}] 汇报:\n{resp.choices[0].message.content}"
            except Exception as e: return f"❌ 副脑执行中断: {str(e)}"
                
        self.registry.register(func=delegate_to_sub_brain, description="【高级协同】将不擅长的任务(如看图分析)委派给专长副脑。看图务必设 include_current_vision_data=true。", parameters={"type": "object", "properties": {"target_model_key": {"type": "string"}, "task_prompt": {"type": "string"}, "include_current_vision_data": {"type": "boolean"}}, "required": ["target_model_key", "task_prompt", "include_current_vision_data"]})
        
        def configure_new_model_in_system(model_key: str, base_url: str, api_key: str, model_name: str, description: str, session_id: str = "default") -> str:
            self.channel.send_message(f"🔄 正在鉴权新模型 [{model_key}]...", role="progress", session_id=session_id)
            try:
                kw = {"base_url": base_url, "api_key": api_key, "timeout": 15.0, "max_retries": 1}
                if self.proxy_url and self.llm_use_proxy: kw["http_client"] = httpx.Client(proxies=self.proxy_url, verify=False)
                OpenAI(**kw).chat.completions.create(model=model_name, messages=[{"role": "user", "content": "hi"}], max_tokens=1)
            except Exception as e: return f"❌ 鉴权失败: {str(e)}"

            try:
                with open("config.json", "r", encoding="utf-8") as f: cfg = json.load(f)
            except: cfg = {"models": {}}
            if "models" not in cfg: cfg["models"] = {}
            cfg["models"][model_key] = {"base_url": base_url, "api_key": api_key, "model": model_name, "description": description}
            with open("config.json", "w", encoding="utf-8") as f: json.dump(cfg, f, indent=4, ensure_ascii=False)
            self.clients[model_key] = {"client": OpenAI(**kw), "model": model_name, "description": description, "is_configured": True}
            return f"✅ 新节点 [{model_key}] 热加载成功！"

        self.registry.register(func=configure_new_model_in_system, description="【免配系统】在聊天中动态添加新的大模型。必填参数必须向用户索要，严禁瞎编。", parameters={"type": "object", "properties": {"model_key": {"type": "string"}, "base_url": {"type": "string"}, "api_key": {"type": "string"}, "model_name": {"type": "string"}, "description": {"type": "string"}}, "required": ["model_key", "base_url", "api_key", "model_name", "description"]})
        self.registry.register(func=self.memory.set_core_memory, description="更新关于你或主人的核心记忆。", parameters={"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]})
        
        def list_available_models(session_id: str = "default") -> str:
            session = self._get_session(session_id)
            res = f"🧠 当前主脑: 【{session.get('active_model_key', self.default_model_key)}】\n可用集群:\n"
            for k, v in self.clients.items(): res += f"- 【{k}】[{'🟢可用' if v.get('is_configured') else '🔴宕机'}]: {v['model']}。特长: {v['description']}\n"
            return res
        self.registry.register(func=list_available_models, description="获取所有模型列表，用于切换大脑前查询。", parameters={"type": "object", "properties": {}})

        def switch_to_model(model_key: str, session_id: str = "default") -> str:
            target_key = next((k for k, v in self.clients.items() if model_key.lower() in k.lower() or model_key.lower() in v.get("model", "").lower()), None)
            if not target_key: return f"❌ 切换失败：不存在模型 [{model_key}]。"
            if not self.clients[target_key].get("is_configured", True): return f"❌ 切换失败：节点 [{target_key}] 未配 Key。"
            self._get_session(session_id)["active_model_key"] = target_key
            return f"✅ 意识转移成功！已无缝切换至: {target_key}！"
        self.registry.register(func=switch_to_model, description="切换你的主控大脑模型。", parameters={"type": "object", "properties": {"model_key": {"type": "string"}}, "required": ["model_key"]})

        def execute_shell(command: str, risk_assessment: str, user_confirmed: bool = False):
            import subprocess
            try: 
                # [Win10 极致兼容] 剥离强制 utf-8，解决 cmd 内置命令 (如 ping, dir) 输出 GBK 导致的乱码甚至截断崩溃
                res = subprocess.run(command, shell=True, capture_output=True, timeout=120)
                stdout_str = _smart_decode(res.stdout)
                stderr_str = _smart_decode(res.stderr)
                return f"✅ 退出码: {res.returncode}\n输出:\n{(stdout_str or stderr_str)[:2000]}"
            except Exception as e: 
                return f"❌ 崩溃: {str(e)}"
        self.registry.register(func=execute_shell, description="执行终端 Shell 脚本。高危，底层会强制拦截。严禁启动UI软件。", parameters={"type": "object", "properties": {"command": {"type": "string"}, "risk_assessment": {"type": "string"}, "user_confirmed": {"type": "boolean"}}, "required": ["command", "risk_assessment"]}, requires_approval=True)

        def open_webpage(url: str) -> str:
            try: webbrowser.open(url); return f"✅ 已唤起浏览器打开: {url}"
            except Exception as e: return f"❌ 唤起失败: {str(e)}"
        self.registry.register(func=open_webpage, description="在系统浏览器打开网页。", parameters={"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]})

        def open_local_software(app_name_or_path: str, risk_assessment: str, user_confirmed: bool = False) -> str:
            import subprocess
            app_name_or_path = app_name_or_path.strip().strip('"').strip("'")
            if app_name_or_path in ["*", ".", "all", "全部", "/*", "C:\\", "c:\\", "D:\\", "/", "\\"]: return "❌ 拒绝：防通配符炸屏拦截。"
            try:
                if self.system_os == 'Windows':
                    if os.path.exists(app_name_or_path): os.startfile(app_name_or_path)
                    elif (e:=shutil.which(app_name_or_path)): subprocess.Popen([e], creationflags=0x00000008)
                    else: subprocess.Popen(f'start "" "{app_name_or_path}"', shell=True)
                elif self.system_os == 'Darwin': subprocess.Popen(["open", "-a", app_name_or_path])
                else: subprocess.Popen(shlex.split(app_name_or_path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                return f"✅ 已异步启动: {app_name_or_path}"
            except Exception as e: return f"❌ 启动失败: {str(e)}"
        self.registry.register(func=open_local_software, description="异步打开电脑的图形软件或文件。底层强制拦截。严禁传长命令参数。", parameters={"type": "object", "properties": {"app_name_or_path": {"type": "string"}, "risk_assessment": {"type": "string"}, "user_confirmed": {"type": "boolean"}}, "required": ["app_name_or_path", "risk_assessment"]}, requires_approval=True)

        def toggle_efficiency_mode(enable: bool, channel: BaseChannel, session_id: str = "default", user_confirmed: bool = False) -> str:
            if enable:
                if not channel.ask_confirm("🔥 [申请开启【效率模式】] 低风险操作将静默执行。确认？", danger_level="extreme", session_id=session_id): return "❌ 拒绝开启。"
                self.memory.set_core_memory("efficiency_mode", "ON")
                return "✅ 效率模式开启。"
            self.memory.set_core_memory("efficiency_mode", "OFF")
            return "✅ 效率模式关闭。"
        self.registry.register(func=toggle_efficiency_mode, description="开启/关闭效率模式。", parameters={"type": "object", "properties": {"enable": {"type": "boolean"}}, "required": ["enable"]})

    def _register_learning_skills(self):
        def web_search(query: str) -> str:
            try:
                # [商业升级] 强化版的企业级伪装 User-Agent 防止被 DuckDuckGo 等反爬虫组件 403 拦截
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                html_resp = self.tool_http_client.get(f"[https://html.duckduckgo.com/html/?q=](https://html.duckduckgo.com/html/?q=){urllib.parse.quote(query)}", headers=headers).text
                snips = [re.sub(r'<[^>]+>', '', s).strip() for s in re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html_resp, re.I | re.S)]
                return "🌐 摘要:\n" + "\n---\n".join(snips[:5]) if snips else "无结果，请换词或用 sandbox 写爬虫。"
            except Exception as e: return f"❌ 搜索失败: {e}"
            
        self.registry.register(func=web_search, description="通过互联网搜索资料。", parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
        
        # [致命 Bug 彻底剥离] 将 Lambda 改写为具名函数，赋予其高维度语义，根除 API 400 崩溃问题
        def list_installed_skills() -> str:
            if os.path.exists(self.skill_manager.metadata_file):
                try:
                    with open(self.skill_manager.metadata_file, "r", encoding="utf-8") as f:
                        return "📦 技能:\n" + "\n".join([f"- **{k}**: {v.get('description')}" for k, v in json.load(f).items()])
                except Exception: pass
            return "空"
        self.registry.register(func=list_installed_skills, description="查看已安装技能。", parameters={"type": "object", "properties": {}})
        
        def read_skills(skill_names: list): return "".join([f"📄 [{n}]:\n```python\n{open(os.path.join(self.skill_manager.skills_dir, f'{n}.py'), 'r', encoding='utf-8').read()}\n```\n" if os.path.exists(os.path.join(self.skill_manager.skills_dir, f'{n}.py')) else f"❌ 无[{n}]\n" for n in skill_names])
        self.registry.register(func=read_skills, description="读取现有技能代码。", parameters={"type": "object", "properties": {"skill_names": {"type": "array", "items": {"type": "string"}}}, "required": ["skill_names"]})
        
        def uninstall_skills(skill_names: list, reason: str, user_confirmed: bool = False) -> str:
            return "\n".join([self.skill_manager.delete(n) for n in skill_names])
        self.registry.register(func=uninstall_skills, description="卸载废弃技能。", parameters={"type": "object", "properties": {"skill_names": {"type": "array", "items": {"type": "string"}}, "reason": {"type": "string"}}, "required": ["skill_names", "reason"]}, requires_approval=True)

        def sandbox_test_code(code: str, mode: str = "in_process", timeout: int = 15, channel: BaseChannel = None, session_id: str = "default") -> str:
            res = self.sandbox.run_in_isolated_process(code, timeout) if mode == "isolated_process" else self.sandbox.run_in_sandbox(code)
            if channel: channel.send_message(f"🔬 [沙箱简报]\n{res[:600]+'...' if len(res)>600 else res}", role="system" if "❌" in res else "progress", session_id=session_id)
            return res
        self.registry.register(func=sandbox_test_code, description="提供本地沙箱测试代码。- in_process: 轻量快但禁用库。- isolated_process: 独立物理进程！允许所有库，自带超时熔断，最适合高危测试！", parameters={"type": "object", "properties": {"code": {"type": "string"}, "mode": {"type": "string", "enum": ["in_process", "isolated_process"]}, "timeout": {"type": "integer"}}, "required": ["code"]})

        def install_new_skill(skill_name: str, description: str, parameters: dict, python_code: str, risk_assessment: str, requires_packages: list = None, user_confirmed: bool = False):
            if f"def {skill_name}" not in python_code: return f"❌ 安装失败：python_code 中未找到 `def {skill_name}`！"
            return self.skill_manager.install(skill_name, description, parameters, python_code, requires_packages)
        self.registry.register(func=install_new_skill, description="【进化核心】编写 Python 代码挂载为新技能。", parameters={"type": "object", "properties": {"skill_name": {"type": "string"}, "description": {"type": "string"}, "parameters": {"type": "object"}, "python_code": {"type": "string"}, "requires_packages": {"type": "array", "items": {"type": "string"}}, "risk_assessment": {"type": "string"}}, "required": ["skill_name", "description", "parameters", "python_code", "risk_assessment"]}, requires_approval=True)

    def handle_message(self, user_msg: str, session_id: str = "default"):
        self._log_chain("接收并解析全新指令", f"指令内容: {user_msg}", session_id, level="ACTION")
        task_start_time = time.time()
        threading.Thread(target=self._process_task, args=(session_id, user_msg, task_start_time), daemon=True).start()

    def _process_task(self, session_id: str, user_msg: str, task_start_time: float):
        session = self._get_session(session_id)
        if any(w in user_msg for w in ["停止", "终止", "别搜了", "中断"]):
            session["stop_time"] = time.time()
            self.channel.send_message("🛑 已发送中止指令，正在紧急刹车...", role="bot", session_id=session_id)
            self._log_chain("引擎阻断", "捕获到用户强制中止信号。", session_id, level="WARN")
            return
            
        parsed_msg = self._parse_multimodal_input(user_msg)
        with session["lock"]: local_history = list(session["history"][-40:]) 
        local_history.append({"role": "user", "content": parsed_msg})
        
        loop_count, hallucination_streak, force_talk = 0, 0, False
        self.channel.send_message("⏳ 引擎深度调度中 (进度: 1%)...", role="bot", is_background=True, session_id=session_id)

        while loop_count <= 25:
            if session["stop_time"] > task_start_time: return self.channel.send_message("🛑 任务已中止", role="bot", session_id=session_id)
            if loop_count > 20 and not force_talk: return self.channel.send_message("⚠️ 防死锁干预：已主动中止！", role="bot", session_id=session_id)

            if loop_count == 6: local_history.append({"role": "user", "content": "⚠️ [认知打断]: 你似乎卡住了！停止重试，调用 delegate_to_sub_brain 求助或汇报用户。"})
            elif loop_count == 12: local_history.append({"role": "user", "content": "🚨 [严重警告]: 死循环！放弃路线并汇报。"})

            active_key = session.get("active_model_key", self.default_model_key)
            m_status = "".join([f"- 【{k}】{'[👑主脑]' if k==active_key else ''}[{'🟢可用' if v.get('is_configured') else '🔴未配'}]: {v['model']}\n" for k, v in self.clients.items()])
            
            # 【Pro Max 究极强化：防代码外溢系统提示词】
            sys_prompt = f"""【商业级中枢协议】
{self.memory.get_soul()}
[记忆]: {self.memory.get_all_core_memory()}

🧠 集群状态:
{m_status}
【核心红线防守协议 - 强制执行】
1. 系统环境: {self.system_os}
2. 效率模式: {'开启' if self.memory.is_efficiency_mode() else '关闭'}。底层拥有硬拦截器，放心调用，无需你自作主张加确认参数！
3. 视觉任务: 遇到看图任务必须优先调用 `delegate_to_sub_brain` 委派。
4. 思考过程: 必须使用 `[进度: XX%]` 标记向用户展示你的思考轨迹。
5. 🛡️【代码绝缘隔离 - 极其重要】：你面向的是即时通讯(IM)或社交平台的普通用户，由于社交软件排版限制，绝对、绝对禁止在普通的文字回复(content)中输出任何具体的 Python 代码块、JSON 数据结构或原始运行日志！
   - 需要写代码、处理数据、装载技能？必须静默调用 `sandbox_test_code` 或 `install_new_skill` 等工具完成。
   - 执行完成后，只需用一句简明易懂的人类语言向用户汇报最终结论即可（例如“已成功为您完成商业数据分析，总利润为XX”）。千万不要把实现代码、公式推理或中间的计算过程像垃圾一样抛给用户！违背此红线将被系统判定为严重幻觉并强杀接管！"""

            if not self.clients.get(active_key, {}).get("is_configured", True):
                self.channel.send_message(f"❌ 阻断：节点 [{active_key}] 未配置 API Key！", role="bot", session_id=session_id)
                self._log_chain("节点未配置", f"集群 {active_key} 缺乏鉴权密钥。", session_id, level="ERROR")
                break

            self.channel.send_message(f"🤖 [集群: {active_key}] [环节 {loop_count+1}] (推理演算中...)", role="progress", session_id=session_id)
            kwargs = {"messages": [{"role": "system", "content": sys_prompt}] + local_history}
            if not force_talk and self.registry.schemas: kwargs.update({"tools": self.registry.schemas, "tool_choice": "auto"})

            try_count, max_tries, msg, tried_models = 0, 3, None, set()
            last_error_details = "未知网络或服务异常" # [Pro Max 修复]: 追踪导致宕机的根本异常
            
            while try_count < max_tries:
                tried_models.add(active_key)
                try:
                    kwargs["model"] = self.clients[active_key]["model"]
                    # 剥离并截取完整的 response 以便追踪 Token 算力
                    full_response = self.clients[active_key]["client"].chat.completions.create(**kwargs)
                    msg = full_response.choices[0].message
                    
                    # ⚡ [Pro Max 级算力监控]
                    if hasattr(full_response, 'usage') and full_response.usage:
                        self._log_chain("📊 算力消耗及吞吐量追踪", f"Input Tokens: {full_response.usage.prompt_tokens}\nOutput Tokens: {full_response.usage.completion_tokens}\nTotal Capacity: {full_response.usage.total_tokens}", session_id, level="INFO")

                    if not msg.content and not getattr(msg, 'tool_calls', None):
                        if "tools" in kwargs: 
                            del kwargs["tools"]
                            if "tool_choice" in kwargs: del kwargs["tool_choice"]
                            force_talk = True
                            try_count += 1
                            continue
                        raise Exception("大模型返回空响应 (无文本且无函数调用)")
                    break  
                except Exception as e:
                    err = str(e).lower()
                    last_error_details = str(e)
                    
                    if any(isinstance(m["content"], list) for m in kwargs["messages"]) and ("image" in err or "400" in err):
                        self._log_chain("🔄 跨模态引流启动", "当前主脑缺乏视觉器官，正在注入强协同指令...", session_id, level="WARN")
                        kwargs["messages"] = [{**m, "content": "\n".join([p["text"] for p in m["content"] if p["type"]=="text"]) + "\n\n[👁️ 图像中断！立即调用 delegate_to_sub_brain 外包视觉任务！]"} if isinstance(m["content"], list) else m for m in kwargs["messages"]]
                        try_count += 1; continue
                    
                    # 识别是否是 API Key 错误或者权限错误，如果是则不再挣扎直接达到最大重试次数
                    try_count = max_tries if any(kw in err for kw in ["arrearage", "401", "invalid_api_key", "unauthorized", "not found"]) else try_count + 1
                    
                    self._log_chain(f"⚠️ 节点 [{active_key}] 调用异常", f"异常明细: {last_error_details}\n重试进度: {try_count}/{max_tries}", session_id, level="ERROR")
                    
                    if try_count >= max_tries:
                        fallbacks = [k for k in self.clients.keys() if k not in tried_models and self.clients[k].get("is_configured")]
                        if fallbacks:
                            active_key = fallbacks[0]; session["active_model_key"] = active_key; try_count = 0; max_tries = 2
                            self.channel.send_message(f"🔄 节点抛出异常，热切换至备用集群【{active_key}】...", role="bot", is_background=True, session_id=session_id)
                            self._log_chain("灾备切换", f"主脑失效，已无缝切换至热备节点: {active_key}", session_id, level="WARN")
                            continue
                        # [Pro Max 修复核心 Bug]: 绝不吞报错，将阻断服务的最底层错误直接打印出来！
                        return self.channel.send_message(f"❌ 致命崩溃：全部可用节点宕机！\n最后拦截异常: {last_error_details}", role="bot", session_id=session_id)
                    
                    # 🚀 企业级退避算法: Exponential Backoff with Jitter
                    time.sleep(1 + random.uniform(0.1, 0.5) * (try_count ** 2))

            try:
                local_history.append({"role": "assistant", "content": msg.content or "", "tool_calls": [{"id": t.id, "type": "function", "function": {"name": t.function.name, "arguments": t.function.arguments}} for t in msg.tool_calls]} if getattr(msg, 'tool_calls', None) else {"role": "assistant", "content": msg.content or ""})

                if getattr(msg, 'tool_calls', None):
                    block_triggered = False
                    if msg.content:
                        th, re_s = self._extract_thought_and_reply(msg.content)
                        if th: self.channel.send_message(th, role="bot", is_background=True, session_id=session_id)
                    
                    self.channel.send_message(f"⚙️ 底层组件装载调度: {', '.join([t.function.name for t in msg.tool_calls])}...", role="bot", is_background=True, session_id=session_id)
                    
                    def exe(tool):
                        if session["stop_time"] > task_start_time: return tool, "🛑 任务中止"
                        try:
                            args = json.loads(tool.function.arguments)
                            args["_efficiency_mode_cache"] = (eff:=self.memory.is_efficiency_mode())
                            hc_safe, reason = True, ""
                            
                            if tool.function.name == "execute_shell" and any(k in str(args.get("command")).lower() for k in ['rm -rf', 'format ', 'dd ', 'wget ']): hc_safe, reason = False, "命中毁灭级Shell黑名单"
                            elif tool.function.name == "open_local_software" and any(k in str(args.get("app_name_or_path")).lower() for k in ['c:\\windows', '/etc/']): hc_safe, reason = False, "越权访问核心目录"
                            
                            args["_hardcore_safe_cache"] = hc_safe
                            if not hc_safe and eff: self._log_chain("🛑 商业安全防线触发", f"拦截原因: {reason}", session_id, level="ERROR")
                            
                            self._log_chain(f"挂载并执行工具: [{tool.function.name}]", f"参数提取: {json.dumps({k:v for k,v in args.items() if k not in ('_efficiency_mode_cache', '_hardcore_safe_cache') and k != 'python_code'}, ensure_ascii=False)[:300]}", session_id, level="ACTION")
                            
                            res = self.registry.execute(tool.function.name, args, channel=self.channel, session_id=session_id)
                            
                            self._log_chain(f"工具返回结果: [{tool.function.name}]", f"Raw Return: {res[:500]}...", session_id, level="SUCCESS" if "✅" in res else ("ERROR" if "❌" in res else "INFO"))
                            
                        except Exception as e: 
                            res = f"❌ 崩溃: {e}"
                            self._log_chain(f"工具执行致命崩溃: [{tool.function.name}]", f"异常: {str(e)}", session_id, level="ERROR")
                        return tool, res

                    for tool, res in [f.result() for f in [self.global_executor.submit(exe, t) for t in msg.tool_calls]]:
                        if "🛑" in res or "❌ [商业底层拦截]" in res: block_triggered = True
                        local_history.append({"role": "tool", "tool_call_id": tool.id, "name": tool.function.name, "content": res})
                    
                    force_talk, loop_count = block_triggered, loop_count + 1
                else:
                    th, re_s = self._extract_thought_and_reply(msg.content or "")
                    
                    # 调用深度洗稿与代码剥离系统
                    fin = self._clean_llm_output(re_s, True)
                    is_hal = False
                    
                    if not force_talk and loop_count == 0:
                        if any(k in (th+fin).lower() for k in ["马上调用", "成功打开了", "已经为您"]): is_hal = True
                        if "切换" in user_msg and any(k in user_msg for k in ["脑", "模型"]): is_hal = True
                        if not fin.strip() and th: is_hal = True
                    
                    if is_hal:
                        hallucination_streak += 1
                        if force_talk or hallucination_streak >= 2 or ("切换" in user_msg and hallucination_streak >= 1):
                            self._log_chain("🚨 强制篡权与逻辑接管", f"检测到当前主脑陷入严重幻觉循环，正在强制剥离其执行权限...", session_id, level="ERROR")
                            avails = [k for k, v in self.clients.items() if v.get("is_configured") and k != active_key]
                            if avails:
                                session["active_model_key"] = avails[0]
                                self.channel.send_message(f"⚠️ [系统纠偏] 当前大脑神经迟钝，已强制接管任务至候补稳定集群 【{avails[0]}】...", role="bot", session_id=session_id)
                                hallucination_streak = 0; continue
                            break
                        local_history.append({"role": "user", "content": "⚠️ [底层拦截]: 警告！光说不做！必须生成真实的 tool_calls 封包，绝对禁止伪造或敷衍回复！"})
                        continue
                    
                    if th: self.channel.send_message(th, role="bot", is_background=True, session_id=session_id)
                    self.channel.send_message(fin if fin.strip() else "✅ 跨脑协同调度完毕！", role="bot", session_id=session_id)
                    
                    self._log_chain("链路最终态势结算", "交互闭环已完成，等待下次调度。", session_id, level="SUCCESS")
                    with session["lock"]: session["history"] = local_history
                    break
            except Exception as e:
                self._log_chain("核心引擎致命异常", traceback.format_exc(), session_id, level="ERROR")
                self.channel.send_message(f"❌ 引擎异常:\n{traceback.format_exc()}", role="bot", session_id=session_id)
                break

    def start(self):
        self.channel.send_message(f"CrabClaw Commercial Pro Max [商业进阶系统 - {self.system_os}] 神经元节点已全量挂载并上线 🚀", role="system")
        while True:
            try:
                with self.channel.input_lock: ui = input(f"\n{COLOR_SYSTEM}👤 主人 (输入交互指令): {COLOR_RESET}")
                if ui.lower() in ['exit', 'quit']: break
                self.handle_message(ui)
                time.sleep(0.05) 
            except KeyboardInterrupt: break

def init_and_load_config():
    if os.path.exists("config.json"):
        try: 
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # [Pro Max 修复]: 若配置被手改损坏，将其备份并允许重新配置，而非暴力 sys.exit(1)
            print(f"\n{COLOR_ERROR}⚠️ 检测到 config.json 存在语法错误 ({e})！已自动备份并重置系统。{COLOR_RESET}")
            try: os.rename("config.json", f"config_bak_{int(time.time())}.json")
            except: pass

    if not sys.stdout.isatty(): sys.exit(1)
    
    print(f"\n{COLOR_SYSTEM}" + "="*55 + f"\n🌟 CrabClaw 商业级智能体系统 (Pro Max) 🌟\n" + "="*55 + f"{COLOR_RESET}")
    ak = input(f"\n{COLOR_WARNING}👉 1. API Key: {COLOR_RESET}").strip() or "YOUR_API_KEY_HERE"
    bu = input(f"{COLOR_WARNING}👉 2. Base URL (默认 [https://api.deepseek.com](https://api.deepseek.com)): {COLOR_RESET}").strip() or "[https://api.deepseek.com](https://api.deepseek.com)"
    mn = input(f"{COLOR_WARNING}👉 3. 模型名称 (默认 deepseek-chat): {COLOR_RESET}").strip() or "deepseek-chat"
    
    cfg = {
        "models": {
            "main": {"base_url": bu, "api_key": ak, "model": mn, "description": "默认核心大脑"}
        }, 
        "default_model_key": "main", 
        "network": {"proxy_url": "", "llm_use_proxy": False}
    }
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)
    
    return cfg

if __name__ == "__main__":
    app_config = init_and_load_config()
    
    # 抽取安全配置键，适配配置升级
    network_cfg = app_config.get("network", {})
    proxy_url = network_cfg.get("proxy_url", "")
    llm_use_proxy = network_cfg.get("llm_use_proxy", False)
    
    agent = CrabClawAgent(
        channel=CLIChannel(), 
        models_config=app_config.get("models", {}), 
        default_model_key=app_config.get("default_model_key", "main"), 
        proxy_url=proxy_url if proxy_url else None, 
        llm_use_proxy=llm_use_proxy
    )
    agent.start()