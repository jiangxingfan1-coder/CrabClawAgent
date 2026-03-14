# [cite_start]🍏 CrabClaw 智能体系统：Mac & Linux 部署与运行指南 [cite: 1]

[cite_start]当您准备将 CrabClaw 智能体系统从 Windows 环境迁移到 Mac 或 Linux 服务器上运行时，请 **务必** 阅读本指南，以避开跨平台部署中最常见的“隐形陷阱” [cite: 2]。

## [cite_start]🚨 核心防坑预警：Windows 的“隐形换行符” (CRLF vs LF) [cite: 3]

* [cite_start]在 Windows 系统下创建或编辑的纯文本文件（如 `.txt`），默认使用 CRLF（回车+换行）作为换行符 [cite: 4]。
* [cite_start]但是，Mac 和 Linux 系统的终端 **只识别** LF（换行）格式 [cite: 4]。
* [cite_start]如果您直接把在 Windows 上创建的启动器文本文件后缀改为 `.sh` 并在 Mac/Linux 上运行，系统会报错 [cite: 5]：
  > [cite_start]`bash\r: No such file or directory` 或 `command not found` [cite: 6]
* [cite_start]为了彻底避开这个问题，请严格按照以下步骤进行迁移 [cite: 7]：

---

## [cite_start]🛠️ 标准部署步骤（推荐） [cite: 8]

### [cite_start]第一步：在 Mac/Linux 上纯净创建 (最稳妥的做法) [cite: 9]
1. [cite_start]**不要**直接把 Windows 传过来的 `.txt` 文件改后缀名 [cite: 10]。
2. [cite_start]在您的 Mac 或 Linux 系统上，打开一个干净的文本编辑器（如 Mac 自带的“文本编辑”处于纯文本模式，或使用 VS Code、Sublime） [cite: 11]。
3. [cite_start]新建两个空白文件 [cite: 12]。
4. [cite_start]将我们最终生成的 `.sh` 代码内容，分别 **复制并粘贴** 到这两个空白文件中 [cite: 13]。
5. 将它们分别命名并保存为：
   * [cite_start]`run_crabclaw.sh` [cite: 14, 15]
   * [cite_start]`run_qq_bot.sh` [cite: 14, 16]
   [cite_start]*(这样做保存出来的文件，天然就是标准的 Mac/Linux LF 格式，没有任何历史包袱 [cite: 17]。)*

### [cite_start]第二步：赋予执行权限 (Unix 系统强制要求) [cite: 18]
[cite_start]出于安全机制，Mac 和 Linux 默认不允许直接运行刚刚创建的脚本 [cite: 19][cite_start]。您必须通过终端给它们“发通行证” [cite: 19]。
1. [cite_start]打开 Mac 的 **终端 (Terminal)** 或 Linux 的命令行 [cite: 20]。
2. [cite_start]使用 `cd` 命令进入您存放这些脚本的文件夹 [cite: 21]。例如：
   [cite_start]`cd /Users/您的用户名/Desktop/CrabClaw机器人目录` [cite: 22]
3. [cite_start]依次输入以下命令并回车，赋予它们可执行权限 [cite: 23]：
   * [cite_start]`chmod +x run_crabclaw.sh` [cite: 24]
   * [cite_start]`chmod +x run_qq_bot.sh` [cite: 25]

### [cite_start]第三步：启动引擎 [cite: 26]
[cite_start]权限赋予完毕后，您就可以随时启动它们了 [cite: 27]：
* [cite_start]**启动主控引擎**：在终端输入 `./run_crabclaw.sh` [cite: 28]
* [cite_start]**启动QQ守护端**：在终端输入 `./run_qq_bot.sh` [cite: 29]

---

## [cite_start]💡 进阶技巧与补救措施 [cite: 30]

### [cite_start]🍎 Mac 专属：如何实现“双击直接运行”？ [cite: 31]
[cite_start]在 Mac 上，默认情况下双击 `.sh` 文件会用文本编辑器打开它，而不是运行它 [cite: 32][cite_start]。如果您希望像 Windows 的 `.bat` 那样双击启动 [cite: 32]：
1. [cite_start]完成上面的 `chmod +x` 授权步骤 [cite: 33]。
2. [cite_start]将文件的后缀名从 `.sh` 修改为 `.command` [cite: 34]。
   [cite_start]即：`run_crabclaw.command` 和 `run_qq_bot.command` [cite: 35]。
3. [cite_start]以后直接鼠标双击这个 `.command` 文件，Mac 就会自动弹出一个终端窗口并运行您的智能体了！ [cite: 36]

### [cite_start]🔧 补救：如果文件已经带上了 Windows 换行符怎么办？ [cite: 37]
[cite_start]如果您已经把 Windows 上的文件传到了 Linux 云服务器上，懒得重新复制粘贴，可以使用强大的 `sed` 命令一键清洗掉隐形的 `\r` 字符 [cite: 38]。

[cite_start]在终端中执行以下命令即可“洗白”文件 [cite: 39]：
* [cite_start]`sed -i 's/\r$//' run_crabclaw.sh` [cite: 40]
* [cite_start]`sed -i 's/\r$//' run_qq_bot.sh` [cite: 41]

[cite_start]*(注：Mac 系统默认的 `sed` 语法略有不同，建议在 Mac 上优先使用“第一步”的重新复制法 [cite: 42]。)*

---

[cite_start]**🎉 祝您部署顺利！CrabClaw Agent 跨平台引擎已准备就绪。** [cite: 43]