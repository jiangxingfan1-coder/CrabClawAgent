import os
import sys
import json
import asyncio
import time
import threading
import re

# ---------------------------------------------------------
# [依赖包自救系统] 优雅处理第三方库缺失
# ---------------------------------------------------------
try:
    import botpy
    from botpy.message import Message
except ImportError:
    print("\n" + "="*55)
    print("❌ [系统警报] 缺少 QQ 机器人核心运行库 `qq-botpy`")
    print("="*55)
    print("👉 修复方法：执行 pip install qq-botpy openai httpx\n")
    sys.exit(1)

try:
    from crabclaw import CrabClawAgent, BaseChannel, init_and_load_config
except ImportError:
    print("\n❌ 错误：找不到核心引擎 `crabclaw.py`，请确保它们在同一个文件夹内！")
    sys.exit(1)

# ==========================================
# 🔌 QQ 专属并发通讯通道 (对接商业底层网关)
# ==========================================
class QQChannel(BaseChannel):
    def __init__(self, loop):
        self.loop = loop
        self.session_messages = {}
        self.seq_lock = threading.Lock() # 防 40054005 报错 (严密锁管控)
        self.pending_confirmations = {}
        self.confirmation_results = {}

    def bind_message(self, session_id: str, message, is_group=False):
        if session_id in self.session_messages and self.session_messages[session_id]["message"].id == message.id:
            return
        self.session_messages[session_id] = {"message": message, "is_group": is_group, "msg_seq": 1}

    def _smart_chunk_text(self, text: str, max_len: int = 1500) -> list:
        """🚀 商业级智能截断算法: 寻找最近的换行符切片，防止 Markdown/代码块 被暴力腰斩"""
        chunks = []
        while len(text) > max_len:
            # 尝试在最后的 500 字符内寻找换行符
            split_idx = text.rfind('\n', max_len - 500, max_len)
            if split_idx == -1:
                split_idx = max_len
            chunks.append(text[:split_idx])
            text = text[split_idx:].lstrip('\n')
        if text:
            chunks.append(text)
        return chunks

    def send_message(self, message: str, role: str = "bot", is_background: bool = False, session_id: str = "default"):
        if role in ["progress", "system"]:
            print(f"[{'后台引擎' if role == 'progress' else '系统动作'}] [{session_id}] {message}")
            return
            
        if role == "bot":
            ctx = self.session_messages.get(session_id)
            if ctx and ctx["message"] and message and message.strip():
                # 防 40054010 封控策略，轻量脱敏 URL
                message = re.sub(r'(https?://)([^\s]+)', r'🔗[链接]: \2', message)
                
                try:
                    # 腾讯防截断：调用极客智能分片算法
                    chunks = self._smart_chunk_text(message, 1500)
                    
                    for chunk in chunks:
                        with self.seq_lock:
                            current_seq = ctx.get("msg_seq", 1)
                            ctx["msg_seq"] = current_seq + 1
                        
                        coro = ctx["message"].reply(content=chunk, msg_seq=current_seq)
                        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
                        future.add_done_callback(lambda f: print(f"\n[💥 腾讯风控拦截] 失败: {f.exception()}") if f.exception() else None)
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"❌ [{session_id}] 回复异常: {e}")

    def ask_confirm(self, prompt: str, danger_level: str = "high", session_id: str = "default") -> bool:
        """真正的底层阻塞验证，完美契合新引擎的安全红线"""
        print(f"\n⚠️ [等待 QQ 用户动态授权] {prompt}")
        
        alert_msg = f"🛑 【系统高危操作确认】\n检测到智能体尝试执行敏感操作：\n{prompt}\n\n👉 请在 60 秒内直接回复【同意】/【y】以放行，回复其他任意内容拒绝。"
        self.send_message(alert_msg, role="bot", session_id=session_id)

        event = threading.Event()
        self.pending_confirmations[session_id] = event
        self.confirmation_results[session_id] = False 
        
        # 阻塞智能体线程，等待事件唤醒（不会阻塞 QQ 机器人的主异步循环）
        event.wait(timeout=60.0)

        result = self.confirmation_results.pop(session_id, False)
        self.pending_confirmations.pop(session_id, None)

        if not event.is_set():
            self.send_message("⏱️ 授权等待超时，已自动阻断高危操作。", role="bot", session_id=session_id)
            return False

        msg = "✅ 鉴权通过！指令已放行..." if result else "❌ 鉴权拒绝，操作安全取消。"
        self.send_message(msg, role="bot", session_id=session_id)
        return result

# ==========================================
# 🤖 机器人主程序引擎
# ==========================================
class CrabClawQQBot(botpy.Client):
    def __init__(self, app_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_config = app_config

    async def on_ready(self):
        print(f"\n✅ [{self.robot.name}] 机器人已登录QQ官方服务器！")
        self.qq_channel = QQChannel(loop=asyncio.get_running_loop())
        print("🚀 正在挂载 CrabClaw Pro Max 核心引擎...")
        
        self.agent = CrabClawAgent(
            channel=self.qq_channel,
            models_config=self.app_config.get("models", {}),
            default_model_key=self.app_config.get("default_model_key", "main"),
            proxy_url=self.app_config.get("network", {}).get("proxy_url"),
            llm_use_proxy=self.app_config.get("network", {}).get("llm_use_proxy", False)
        )
        print("🦀 桥接就绪！持续监听群聊与私聊...")

    async def _handle_message(self, message, is_group=False):
        user_input = message.content.replace(f"<@!{self.robot.id}>", "").strip() if message.content else ""

        # 多模态提取，直接喂给商业版原生引擎
        if getattr(message, "attachments", None):
            for att in message.attachments:
                url = getattr(att, "url", "")
                if url:
                    url = ("https:" + url) if url.startswith("//") else ("https://api.sgroup.qq.com" + url) if url.startswith("/") else url
                    ctype = getattr(att, "content_type", "").lower()
                    if "image" in ctype or "pic" in ctype or url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                        user_input += f"\n[附加图像: {url}]"
                    else:
                        user_input += f"\n[附加资源: {url}]"

        if not user_input.strip(): return

        print(f"\n💬 [{getattr(message.author, 'username', '用户')}]: {user_input}")
        session_id = f"group_{getattr(message, 'group_openid', getattr(message, 'guild_id', 'default'))}" if is_group else f"user_{getattr(message.author, 'id', 'default')}"

        try:
            self.qq_channel.bind_message(session_id, message, is_group=is_group)
            
            # 授权状态机拦截器
            if session_id in self.qq_channel.pending_confirmations:
                auth = user_input.strip().lower()
                self.qq_channel.confirmation_results[session_id] = auth in ["同意", "y", "yes", "确认", "允许", "1"]
                self.qq_channel.pending_confirmations[session_id].set()
                return 

            self.agent.handle_message(user_input, session_id=session_id)
            
        except Exception as e:
            await message.reply(content=f"❌ 分发崩溃: {e}")

    async def on_at_message_create(self, message: Message): await self._handle_message(message, is_group=False)
    async def on_group_at_message_create(self, message): await self._handle_message(message, is_group=True)
    async def on_c2c_message_create(self, message): await self._handle_message(message, is_group=False)
    async def on_direct_message_create(self, message): await self._handle_message(message, is_group=False)

def load_and_setup_qq_config():
    app_config = init_and_load_config()
    if "qq_bot" not in app_config or not app_config["qq_bot"].get("app_id") or not app_config["qq_bot"].get("token"):
        print("\n" + "="*55 + "\n🌟 首次配置 QQ 机器人接入端 🌟\n" + "="*55)
        app_id = input("\n👉 1. 请输入 QQ 机器人的 AppID (例: 10203040): ").strip()
        token = input("👉 2. 请输入 QQ 机器人的 Token (一串长字符): ").strip()
        app_config["qq_bot"] = {"app_id": app_id, "token": token}
        json.dump(app_config, open("config.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        print("\n✅ QQ 机器人凭证配置已成功保存！\n" + "="*55 + "\n")
    return app_config

if __name__ == "__main__":
    current_config = load_and_setup_qq_config()
    qq_app_id, qq_token = current_config["qq_bot"]["app_id"], current_config["qq_bot"]["token"]
    
    if qq_app_id == "YOUR_APP_ID" or not qq_app_id:
        print("❌ 错误：未正确填写 QQ AppID。请编辑 config.json。")
        sys.exit(1)

    intents = botpy.Intents(public_guild_messages=True, public_messages=True, direct_message=True)
    try: intents.group_messages = True; intents.c2c_group_at_messages = True 
    except Exception: pass 
    
    if sys.platform.lower().startswith("win"): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try: loop = asyncio.get_event_loop()
    except RuntimeError: loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    
    client = CrabClawQQBot(app_config=current_config, intents=intents)
    try: client.run(appid=qq_app_id, secret=qq_token)
    except Exception as e: print(f"\n❌ 启动失败，请检查 AppID/Token 或网络。详细日志: {e}")