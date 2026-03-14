<div align="center">

<!-- Logo 图片，已关联到你仓库中的 蟹爪标志 1.0.png -->

<img src="crab claw logo%201.0.png" width="400" alt="CrabClaw Logo">

<h1><strong>🦀 CrabClaw</strong></h1>

<h2>商业级全自主实体智能体引擎 | Pro Max</h2>

让算力在你本地沸腾，将执行力交还给终端。
CrabClaw 是一个运行在本地环境中的全自主学习型实体执行中枢，拒绝空谈，专注本地执行与跨脑协同。

🌐 项目主页 · 📚 官方文档 · 🐛 提交 Issue

</div>

📖 愿景与初衷

[!IMPORTANT]
CrabClaw 绝对不是云端的闲聊机器人（Chatbot），而是一个具备物理级操作权限的实体执行中枢。

它采用“引擎逻辑”与“交互终端”严格解耦的架构，致力于在保障绝对商业安全的前提下，赋予大模型直接接管本地宿主环境、自我编写技能并进化的能力。遇到了未知的任务？不要只给方案。CrabClaw 会主动搜索、编写代码、丢进隔离沙箱测试，甚至唤醒副脑协同处理，直接交付最终结果。

## ✨ 核心能力与架构解析

CrabClaw 区别于普通套壳项目的五大底层硬核架构：

### 1. 🧠 主副脑跨脑协同 (Sub-Brain Delegation)
打破单一模型的算力与模态瓶颈。主脑可根据任务复杂度，自动将子任务外包给异构集群。
* **视觉与复杂演算外包**：遇到图片解析或超长文本时，自动调用 `delegate_to_sub_brain` 唤醒专长副脑（如专精视觉的模型）。
* **集群热切换**：无缝配置多个异构模型，主脑宕机或陷入幻觉时，系统将强制剥离其权限并热切换至备用节点。

### 2. 🛡️ 双擎安全沙箱 (Dual Sandbox System)
原生硬编码的底层防护，彻底解决 AI 生成代码反噬宿主的安全隐患。

| 沙箱模式 | 运行机制 | 拦截级别 | 适用场景 |
| :--- | :--- | :--- | :--- |
| 🟢 `in_process` | 轻量级协程沙箱 | 自动拦截 `os`, `sys`, `subprocess` 等高危库 | 极速运行、常规代码测试、数据处理 |
| 🔴 `isolated_process` | 物理独立进程 | 允许所有库 + `Timeout` 超时熔断机制 | 高危操作、复杂脚本、防止宿主机死循环 |

### 3. 💾 企业级混合记忆中枢 (Hybrid Memory Core)
抛弃脆弱易损的 JSON 文件存储，引入工业级 SQLite WAL 数据库架构，完美支撑高并发读写，防止记忆数据撕裂。

| 记忆维度 | 存储引擎 | 核心作用 | 读写特性 |
| :--- | :--- | :--- | :--- |
| **Core Memory** (核心记忆) | 键值对映射 (Key-Value) | 刻印智能体核心人格、全局系统指令与效率模式状态 | 高频极速读写，保证 AI 灵魂不发生偏移 |
| **Episodic Memory** (情景记忆) | FTS5 全文检索引擎 | 记录历史对话与操作轨迹，实现超长上下文溯源 | 高维检索，用于长期经验复用与纠错 |

### 4. 🧬 动态技能进化引擎 (Dynamic Skill Engine)
智能体不再受限于开发者预设的代码，它拥有自主编写、热重载并永久植入新技能的权限。

| 核心技能 (Tools) | 触发机制 | 底层权限级别 | 功能描述 |
| :--- | :--- | :--- | :--- |
| `install_new_skill` | AI 自主编写/安装 | ⚠️ 高危 (需 AST 审查) | 编写 Python 代码并挂载为中枢新技能，实现自我进化 |
| `sandbox_test_code` | AI 自主调用 | 🛡️ 沙箱隔离 | 在植入技能前，丢进隔离沙箱进行运行测试与 Debug |
| `web_search` | AI 自主调用 | 🟢 安全 | 突破信息茧房，实时检索互联网最新数据并提取摘要 |

> **💡 智能依赖自愈：** 当检测到技能缺失第三方库（如 `Pillow`, `OpenCV`）时，系统会自动触发环境检测并提示执行 `pip install` 进行自我修复。

### 5. 💻 深度宿主接管与 HITL 防线
原生系统控制，支持执行终端 Shell 脚本、异步唤醒本地 GUI 软件及打开网页。

> [!WARNING]
> **商业级底层安全授权 (Human-In-The-Loop):**
> 任何高危命令（如 `rm -rf`, 格式化, 越权访问核心目录）必须被系统强拦截，并在终端强制要求人类/网关输入 `y` 授权。即便是 AI 开启了“效率模式”，遇到毁灭级黑名单指令也会触发底层熔断。

## 🚀 快速入门 (Quick Start)

全平台支持 Windows / macOS / Linux，仅需三步即可唤醒你的本地中枢。

### 1. 克隆仓库与依赖安装

打开你的终端（Terminal），执行以下命令将项目核心代码克隆至本地：
```bash
git clone [https://github.com/YourUsername/CrabClaw.git](https://github.com/YourUsername/CrabClaw.git)
cd CrabClaw
```
# 安装底层通讯与请求依赖
```bash
pip install openai httpx
```

2. 点火启动

直接运行引擎中枢，首次启动会自动进入配置引导。

# 启动神经中枢
```bash
python src/crabclaw_core.py
```

(提示：按终端提示填入你的 API Key 与 Base URL，默认预设为完美兼容 DeepSeek 的接口配置。)

3. 体验“效率模式”

在交互终端对 CrabClaw 发送指令：

开启效率模式


(引擎将在确认为低风险任务时，跳过繁琐的人类授权，开启真正的全自动静默执行与自我纠错！)

## 📂 系统目录与空间映射

当 CrabClaw 首次启动后，将自动在根目录生成高维工作区：

```text
CrabClaw/
├── src/
│   └── crabclaw_core.py      # 核心逻辑与引擎中枢 (唯一核心)
├── workspace/                # 智能体独立工作区 (自动生成)
│   ├── hybrid_memory.db      # SQLite WAL 记忆数据库核心
│   ├── SOUL.md               # 智能体核心人格与出厂设定
│   ├── skills/               # 智能体自主进化的 Python 技能库
│   └── .sandbox_env/         # 物理隔离沙箱的临时处决区
├── config.json               # 本地集群配置 (自动生成，已加入 .gitignore)
└── README.md                 # 您正在阅读的文档
```
🛡️ 商业级安全白白皮书

我们深知赋予 AI 本地执行权限的潜在破坏力，CrabClaw 在底层构筑了叹息之墙：

防代码溢出屏显：自动折叠模型产生的冗长代码与 JSON 数据，保障你的 IM/社交平台排版不被刷屏卡死。

防死锁与反幻觉干预：模型若连续多次陷入逻辑死循环或“光说不做”的幻觉，底层循环器将触发强杀，自动回滚或切换大脑。

ANSI 终端重构：底层通过 ctypes 强切 Windows 内核级 VT100 与 UTF-8 编码，彻底消灭控制台乱码与报错撕裂。

🤝 接入与二次开发

CrabClaw 天生为拓展而生。核心代码中的 BaseChannel 类是为开发者预留的网关协议。

你只需继承并重写 BaseChannel，即可在极短时间内将 CrabClaw 无缝接入 微信、钉钉、Discord、Telegram 或你的专属前端 Vue/React UI 项目中。

欢迎提交 Pull Request，与我们一起构建最强本地实体 Agent！

<div align="center">




<i>「世界是一个巨大的草台班子，但你的 Agent 不是。」</i>

<b>CrabClaw Engine © 2024-Present</b>

</div>




