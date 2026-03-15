# [cite_start]🦀 CrabClaw 接入 QQ 机器人极简指南 (商业稳定版) [cite: 1]

[cite_start]相较于其他框架需要复杂的 Node.js 环境、繁琐的中间件和代码修改，CrabClaw 采用了纯原生 Python 架构与一键式傻瓜启动引擎 [cite: 2][cite_start]。对接腾讯官方的 QQ API 只需要以下几个简单步骤，全程无需修改任何一行代码 [cite: 2]！

---

## [cite_start]📁 准备工作：确认文件齐全 [cite: 3]

[cite_start]请确保您的文件夹内包含以下核心文件（缺一不可） [cite: 4]：

* [cite_start]`crabclaw.py` (CrabClaw 智能体核心引擎) [cite: 5]
* [cite_start]`run_qq_bot.py` (QQ 机器人主控程序) [cite: 6]
* [cite_start]`启动QQ机器人.bat` (Windows 用户专属启动器) [cite: 7]
* [cite_start]`启动QQ机器人.sh` (Mac / Linux 服务器专属启动器) [cite: 8]

> [cite_start]**注：** 确保您的电脑或服务器已安装 Python（推荐 3.9 及以上版本） [cite: 9][cite_start]。如果没有安装，直接双击启动器，系统会自动引导您去官网下载 [cite: 9]。

---

## [cite_start]🔑 第一步：获取 QQ 机器人凭证 [cite: 10]

[cite_start]要让智能体接管 QQ，您需要先去腾讯官方注册一个机器人身份 [cite: 11]。

1.  [cite_start]前往 QQ 机器人开放平台 (q.qq.com) [cite: 12]。
2.  [cite_start]登录并创建一个属于您的机器人（频道机器人/群聊机器人均可） [cite: 13]。
3.  [cite_start]在后台的【开发】->【开发设置】中，找到您的 `AppID` 和 `Token` [cite: 14][cite_start]。请将它们复制并暂时保存在记事本中 [cite: 14]。

---

## [cite_start]🚀 第二步：一键启动与智能配置 [cite: 15]

[cite_start]忘掉手动安装组件和修改代码的繁琐步骤，现在全部自动化 [cite: 16]！

### [cite_start]🪟 Windows 用户： [cite: 17]
* [cite_start]直接双击文件夹中的 `启动QQ机器人.bat` [cite: 18]。
* [cite_start]黑色弹窗会自动帮您检查并安装所需的 `qq-botpy` 等网络组件，请耐心等待进度条走完 [cite: 19]。

### [cite_start]🐧 Mac / Linux (云服务器) 用户： [cite: 20]
* [cite_start]打开终端，使用 `cd` 命令进入该文件夹目录 [cite: 21]。
* [cite_start]赋予运行权限：`chmod +x 启动QQ机器人.sh` [cite: 22]
* [cite_start]启动守护进程：`./启动QQ机器人.sh` [cite: 23]
* (如果您部署在云服务器上，推荐使用 `tmux` 或 `nohup ./启动QQ机器人.sh &` 让其在后台 24 小时常驻运行) [cite_start][cite: 24]

### [cite_start]🤖 首次运行向导（填入凭证）： [cite: 25]
[cite_start]启动后，如果系统发现您是第一次运行，会自动在屏幕上弹出配置向导 [cite: 26]：
* [cite_start]它会提示您：`👉 请输入 QQ 机器人的 AppID:`，粘贴您刚才复制的数字并回车 [cite: 27]。
* [cite_start]它会提示您：`👉 请输入 QQ 机器人的 Token:`，粘贴长串密码并回车 [cite: 28]。
* [cite_start]配置成功后，当屏幕出现 `✅ [您的机器人名] 机器人已成功登录QQ官方服务器！` 时，说明大脑已与 QQ 完美桥接 [cite: 29]！

> [cite_start]💡 **提示：** 您的凭证会被加密保存在同目录的 `config.json` 文件中 [cite: 30][cite_start]。如果以后填错了想修改，直接用记事本打开这个 JSON 文件修改，或将其删除后重新启动即可 [cite: 30]。

---

## [cite_start]🎮 第三步：功能测试与进阶玩法 [cite: 31]

[cite_start]现在，您可以打开 QQ，在接入了机器人的群聊或频道里进行测试了 [cite: 32]！

### [cite_start]1. 基础对话 & 工具调用 [cite: 33]
* [cite_start]发送：`@您的机器人 帮我查一下深圳今天的天气` [cite: 34]
* [cite_start]发送：`@您的机器人 帮我搜索一下什么是量子计算，并总结成300字发给我` [cite: 35]
* (CrabClaw 会在后台全自动思考、调度网络工具，并将最终结果发送到 QQ 聊天框中) [cite_start][cite: 36]

### [cite_start]2. 多模态交互（看图与听音） [cite: 37]
* [cite_start]**发图片：** 直接在 QQ 里发一张图，并 `@机器人 帮我看看图里有什么`，它会自动调用视觉大模型为您解析 [cite: 38]。
* [cite_start]**发语音：** 发送一段 QQ 语音（或音频文件），它会自动听取并给出回应 [cite: 39]。

### [cite_start]3. 🛡️ 动态安全授权防线 (HITL) [cite: 40]
* [cite_start]如果 AI 想要执行敏感操作（例如向系统写入文件、修改核心代码），它绝对不会私自执行 [cite: 41]。
* [cite_start]机器人会在 QQ 里主动向您发问：`🛑 【系统高危操作确认】检测到智能体尝试执行敏感操作... 请在 60 秒内直接回复【同意】或【y】以放行。` [cite: 42]
* [cite_start]此时，您只需在 QQ 里直接回复 **同意** [cite: 43][cite_start]。后台被挂起的进程就会瞬间放行，智能体将继续为您完成任务 [cite: 43]！

---

## [cite_start]💡 常见错误排查 (FAQ) [cite: 44]

* [cite_start]**❓ Q1: 启动时闪退，或提示找不到 `crabclaw.py` 文件？** [cite: 45]
    * [cite_start]**解答：** 请务必确保您把所有的 `.py` 文件和启动脚本放在了同一个文件夹里，不要分开存放 [cite: 46]。

* [cite_start]**❓ Q2: 提示 `[💥 Botpy 腾讯风控拦截]` 消息投递失败？** [cite: 47]
    * [cite_start]**解答：** 腾讯 QQ 对机器人的发言有极其严格的风控机制 [cite: 48]。
    * [cite_start]**包含违规词/违规网址：** 智能体生成的回复中可能包含了被腾讯屏蔽的链接或敏感词 [cite: 49][cite_start]。目前系统已内置链接折叠功能，但仍可能偶发拦截 [cite: 49]。
    * [cite_start]**频率过高：** 如果机器人短时间内发送了大量长文本，会被腾讯暂时禁言，请等待几分钟后重试 [cite: 50]。

* [cite_start]**❓ Q3: 输入密码错误了怎么办？** [cite: 51]
    * [cite_start]**解答：** 在文件夹中找到新生成的 `config.json` 文件 [cite: 52][cite_start]。右键用记事本打开，找到 `qq_bot` 下的 `app_id` 和 `token`，修改为正确的并保存，然后重新运行启动器即可 [cite: 52][cite_start]。或者直接删掉 `config.json` 重新走一遍向导 [cite: 52]。

* [cite_start]**❓ Q4: 在群里 @ 它，它为什么不理我？** [cite: 53]
    * [cite_start]**解答：** 请前往 QQ 开放平台后台，检查您的机器人是否已经 **“上线”**，或者您所在的 QQ 群是否在 **“测试群”** 白名单内 [cite: 55][cite_start]。请查看黑色的后台控制台，看看是否有收到消息的提示 [cite: 56][cite_start]。如果控制台显示收到了消息，但 QQ 没反应，说明是回复时遇到了网络错误或风控拦截 [cite: 56]。

* [cite_start]**❓ Q5: 提示节点鉴权失败或已欠费停机？** [cite: 57]
    * [cite_start]**解答：** 这说明您的 QQ 通信是正常的，但是您配置的大模型 API Key（大脑）欠费了或填写错误 [cite: 58][cite_start]。请检查 `config.json` 中的 `api_key` 字段 [cite: 58]。