<div align="center">

<img src="crab claw logo%201.0.png" width="400" alt="CrabClaw Logo">

<h1><strong>🦀 CrabClaw</strong></h1>

<h2>商业级全自主实体智能体引擎 | Pro Max<br>Commercial-Grade Fully Autonomous Embodied Agent Engine | Pro Max</h2>

[🇨🇳 简体中文](#简体中文) | [🇺🇸 English](#english)

</div>

---

<h2 id="简体中文">🇨🇳 简体中文</h2>

**致力于推动前沿智能体技术的演进，CrabClaw 是一个高性能、全自主的主动型多模态实体智能体架构，专为应对复杂任务与专业开发场景而打造。**

🛡️ **商业级稳定** · 🧠 **架构突破** · 🚀 **原生执行**

### 🔥 CrabClaw v2.0 纪元：多脑协同集群架构

基于对系统资源与并发调度的深度优化，CrabClaw v2.0 正式跃迁为 **跨模态多脑协同集群 (Multi-Brain Synergy Engine)**，实现了底层架构的全面突破：

* **🧠 跨模态多脑协同网络 (`delegate_to_sub_brain`)：** 主脑具备全局任务统筹能力。当纯文本主脑遭遇视觉等多模态任务时，能自动调度集群池中的专用副脑节点处理并提交报告，支持多模型异构协同与负载均衡。
* **🛡️ 内核级零信任 Docker 沙箱 (`DockerSandboxEngine`)：** 引入物理级隔离环境。全面应用 Cgroups 资源精细调控与只读 (`mode='ro'`) 文件系统挂载，保障宿主机环境绝对安全，同时通过队列守护线程完美解决复杂依赖安装时的并发与阻塞难题。
* **🌌 高效上下文语义压缩器 (`MemoryCompactor`)：** 告别超长上下文导致的内存溢出风险。系统基于实时 Token 嗅探，在触发阈值时自动启动语义压缩机制，并将核心关键信息持久化至本地 (`SOUL.md`)，实现跨周期的连贯记忆复用与智能体状态保存。
* **⚙️ 工业级底层容错装甲 (`_robust_json_parse` & `_sanitize_messages`)：** 极大提升了对非标准大模型输出的兼容性。内置 AST 容错解析与历史链路清洗器，有效避免接口异常中断，保障系统在长时间运行中的极高稳定性与自我纠错能力。

> [!NOTE]
> CrabClaw 不仅是一个对话模型，而是一个具备环境感知和物理级执行能力的实体中枢。它被设计为能够在授权范围内高效调度本地计算资源、自动编写并执行代码。为了充分发挥其自动化效能并保障数据隔离，推荐在沙箱、容器或独立开发环境中运行。

### ✨ 核心能力与架构解析

CrabClaw 的核心设计理念在于 **高度模块化解耦** 与 **极致的执行效能**：

#### 1. 🧠 主副脑任务委派 (Sub-Brain Delegation)
CrabClaw 采用双层高并发架构，确保高维逻辑思考与底层任务执行的高效运转。
* **主脑 (Main Brain):** 负责全局战略规划、高维逻辑推理与长周期记忆整合，具备极强的任务拆解与调度能力。
* **副脑 (Sub Brain):** 负责极速的本地代码执行、工具调用与实时传感器输入，极低延迟且高机动性，可直接在本地终端运行。

#### 2. 🛡️ 双重安全沙箱 (Dual Sandbox System)
为了保障自动化任务的可靠执行，架构内置了两种级别的安全隔离策略。

| 沙箱模式 | 操作权限限制 | 隔离级别 | 应用场景 |
| :--- | :--- | :--- | :--- |
| 🟢 **基础安全模式** | 默认拦截底层高权限库调用 | 严格 | 数据处理、逻辑计算、文本生成 |
| 🔵 **容器执行模式** | 允许文件系统操作与网络通信 | 物理隔离 | 复杂环境依赖构建、自动化测试、脚本执行 |

#### 3. 🗄️ 混合记忆中枢 (Hybrid Memory Core)
引入多维度记忆状态机机制，实现智能体生命周期的长期数据管理。

| 记忆维度 | 底层支持 | 核心作用 | 更新机制 |
| :--- | :--- | :--- | :--- |
| **核心记忆 (Core Memory)** | 知识图谱 & 关键状态机 | 锚定智能体核心指令、关键业务逻辑与项目全景图 | 常驻内存，基于重大状态变更进行热更新 |
| **情景记忆 (Episodic Memory)** | 向量检索 (RAG) | 记录执行轨迹、系统上下文与历史交互日志 | 周期性滚动清理，用于短期规划复盘 |

#### 4. ⚡ 动态技能进化引擎 (Dynamic Skill Engine)
智能体不再受限于预设工具，能够根据任务目标动态编写、验证并挂载新技能代码。

| 核心技能 (Tool) | 运行环境 | 安全评级 | 功能描述 |
| :--- | :--- | :--- | :--- |
| `run_python_skill` | 独立 Python 环境 | ⚠️ **需授权** | 动态编写脚本处理复杂非结构化任务，具备强大的计算延展性 |
| `sandbox_cmd_skill` | 容器化隔离环境 | 🟢 **安全** | 提供底层终端命令执行权限，用于环境配置与深度 Debug |
| `web_search` | 结构化网络环境 | 🟢 **安全** | 实时获取互联网最新数据流并进行深度语义总结 |

### 🚀 快速入门 (Quick Start)
全平台支持 Windows / macOS / Linux。推荐在 Python 3.10+ 环境下运行。

**1. 克隆仓库与初始化**
在您的工作目录中执行以下命令完成初始化构建：
```bash
git clone --depth 1 [https://github.com/YourUsername/CrabClaw.git](https://github.com/YourUsername/CrabClaw.git)
cd CrabClaw
./init_env.sh --model-crab-subcd CrabClaw
```

**2. 安装核心依赖引擎**
```bash
pip install -r requirements.txt
```

**3. 启动中枢核心**
```bash
python core_engine/brain_main.py
```
*(系统初始化期间，请按照终端引导输入您的 API Key 与接口配置。)*

**> 交互终端就绪**
当出现 `CrabClaw >` 提示符后，即可输入您的指令，体验全自动化的任务流转引擎。

### 📁 核心架构映射
CrabClaw 运行时的内部工程树状结构如下：
```text
CrabClaw/
├── core/
│   └── brain_main.py      # 核心中枢调度引擎 (主入口)
├── architecture/          # 架构核心组件库
│   ├── hybrid_memory.py   # 混合记忆引擎实现
│   ├── sub_brain.py       # 副脑任务接口与执行逻辑
│   └── skills/            # 动态技能热加载目录
├── sandbox_env/           # 容器化物理隔离区
├── memory_pool/           # 记忆持久化数据库 (SQLite / VectorDB)
└── README.md              # 官方技术文档
```

### 🛡️ 为什么选择 CrabClaw？
CrabClaw 致力于探索智能体技术的性能极限与工程落地。它为追求极致执行效率与高度自动化的开发者提供了一套强大且灵活的底层引擎。无论是打造个人专属的 AI 效率助手，还是构建复杂的自动化业务流，CrabClaw 都能提供卓越的底层支撑。

### 🤝 接入与二次开发
CrabClaw 天生采用高扩展性的模块化设计。通过继承重写 `BaseChannel` 适配器，您可以轻松将其接入任何企业内部系统或通讯应用（如微信、飞书、钉钉、Discord 等）。

欢迎提交 Pull Request，共同打造性能最强劲的开源实体智能体中枢！

<div align="center">

<i>「生为探索数字生命的极限，星海，扬帆起航！」</i><br>
<b>CrabClaw Engine © 2024-Present</b>

</div>

---

<h2 id="english">🇺🇸 English</h2>

**Dedicated to advancing frontier Agent technology, CrabClaw is a high-performance, fully autonomous embodied agent architecture, built specifically for complex tasks and professional development scenarios.**

🛡️ **Commercial Stability** · 🧠 **Architectural Breakthrough** · 🚀 **Native Execution**

### 🔥 CrabClaw v2.0 Epoch: Multi-Brain Synergy Architecture

Based on deep optimization of system resources and concurrent scheduling, CrabClaw v2.0 officially upgrades to the **Multi-Brain Synergy Engine**, achieving comprehensive breakthroughs in the underlying architecture:

* **🧠 Cross-Modal Synergy Network (`delegate_to_sub_brain`):** The main brain possesses global task orchestration capabilities. When a text-based main brain encounters multimodal tasks like vision, it automatically dispatches specialized sub-brain nodes from the cluster pool to process and submit reports, supporting heterogeneous model synergy and load balancing.
* **🛡️ Kernel-Level Zero-Trust Sandbox (`DockerSandboxEngine`):** Introduces a physical-level isolated environment. Fully implements Cgroups fine-grained resource control and read-only (`mode='ro'`) file system mounts, ensuring absolute host security while perfectly solving concurrency blocking issues during complex dependency installations via daemon threads.
* **🌌 Efficient Context Compactor (`MemoryCompactor`):** Eliminates OOM risks caused by ultra-long contexts. Based on real-time Token sniffing, the system automatically triggers a semantic compression mechanism when reaching thresholds, and persists core critical info to local storage (`SOUL.md`), achieving continuous memory reuse across sessions.
* **⚙️ Industrial-Grade Fault-Tolerant Armor (`_robust_json_parse` & `_sanitize_messages`):** Massively improves compatibility with non-standard LLM outputs. Built-in AST fault-tolerant parsing and history link sanitizers effectively prevent interface interruptions, ensuring extremely high stability and self-correction during long-running tasks.

> [!NOTE]
> CrabClaw is not just a chat model, but an embodied hub with environmental awareness and physical execution capabilities. It is designed to efficiently schedule local compute resources and automatically write/execute code within authorized boundaries. To fully utilize its automation potential and ensure data isolation, it is highly recommended to run it in a sandbox, container, or isolated development environment.

### ✨ Core Capabilities & Architectural Analysis

CrabClaw's core design philosophy lies in **highly modular decoupling** and **extreme execution efficiency**:

#### 1. 🧠 Sub-Brain Task Delegation
CrabClaw utilizes a dual-layer high-concurrency architecture, ensuring efficient operation of both high-dimensional logical reasoning and low-level task execution.

#### 2. 🛡️ Dual Sandbox System
To ensure the reliable execution of automated tasks, the architecture features built-in tiered security isolation policies ranging from basic library interception to fully containerized physical isolation.

#### 3. 🗄️ Hybrid Memory Core
Introduces a multi-dimensional memory state machine mechanism to manage the agent's long-term data over its lifecycle, combining Knowledge Graphs for Core Memory and Vector Retrieval (RAG) for Episodic Memory.

#### 4. ⚡ Dynamic Skill Engine
The agent is no longer limited to pre-set tools; it can dynamically write, verify, and mount new skill codes based on task objectives, effortlessly utilizing tools like `run_python_skill`, `sandbox_cmd_skill`, and structured `web_search`.

### 🚀 Quick Start
Fully supports Windows / macOS / Linux. Python 3.10+ is recommended.

**1. Clone & Initialize**
```bash
git clone --depth 1 [https://github.com/YourUsername/CrabClaw.git](https://github.com/YourUsername/CrabClaw.git)
cd CrabClaw
./init_env.sh --model-crab-subcd CrabClaw
```

**2. Install Core Dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch Core Hub**
```bash
python core_engine/brain_main.py
```
*(During initialization, please follow the terminal prompts to configure your API keys.)*

### 🤝 Access & Secondary Development
CrabClaw is inherently designed with high-extensibility modularity. By extending the `BaseChannel` adapter, you can easily integrate it into any enterprise system or communication application. 

Welcome to submit Pull Requests to jointly build the most powerful open-source embodied agent engine!

<div align="center">

<i>"Born to explore the limits of digital life, to the sea of stars, set sail!"</i><br>
<b>CrabClaw Engine © 2024-Present</b>

</div>
