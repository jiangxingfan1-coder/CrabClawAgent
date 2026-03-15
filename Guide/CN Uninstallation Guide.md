# [cite_start]CrabClaw 本地智能体彻底卸载指南 [cite: 1]

[cite_start]因为 CrabClaw 是以纯 Python 脚本形式运行的本地实体，卸载过程不需要控制面板，只需执行以下四个步骤即可做到“物理级”的彻底抹除。[cite: 2]

## [cite_start]第一步：停止智能体运行 [cite: 3]

[cite_start]如果智能体目前还在后台或终端中运行：[cite: 4]
1. [cite_start]切回到运行该 Python 脚本的命令行（CMD/Terminal）窗口。[cite: 5]
2. [cite_start]连续按下键盘上的 Ctrl + C 强制终止进程。[cite: 6]
3. [cite_start]或者直接点击右上角的 X 关闭该命令行窗口。[cite: 7]

## [cite_start]第二步：销毁智能体的“大脑”与“记忆”（最关键） [cite: 8]

[cite_start]根据源代码分析，该智能体的所有本地状态（包括数据库、自我认知和动态学习的技能）都存放在代码同级目录的 workspace 文件夹中。[cite: 9]
1. [cite_start]打开存放 crabclaw.py 的文件夹。[cite: 10]
2. [cite_start]找到名为 workspace 的文件夹。[cite: 11]
3. [cite_start]直接将 workspace 文件夹整个删除 （建议清空回收站）。[cite: 12]

> [cite_start]注：这会彻底销毁它的 hybrid_memory.db（核心记忆数据库）、SOUL.md（身份设定）以及 skills 目录下的所有自主编写的 Python 技能代码。[cite: 13]

## [cite_start]第三步：删除源代码文件 [cite: 14]

[cite_start]删除下载的程序本体文件：[cite: 15]
1. [cite_start]删除 crabclaw.py 文件。[cite: 16]
2. [cite_start]如果同目录下还有与之配套的其他脚本（如源码注释中提到的 run_qq_bot.py），也一并删除。[cite: 17]

## [cite_start]第四步：清理 Python 依赖包（可选） [cite: 18]

[cite_start]如果你当初是为了运行这个智能体而专门安装了相关的 Python 第三方库，并且以后不再需要用到它们，可以打开命令行（CMD 或 PowerShell）执行以下命令卸载它们，以释放一点硬盘空间：[cite: 19]

[cite_start]`pip uninstall openai httpx` [cite: 20]

> (如果你还有其他 Python 项目在用这些库，请跳过此步) [cite_start][cite: 21]

## [cite_start]🎉 卸载完成！ [cite: 22]

[cite_start]执行完上述操作后，该智能体及其所有数据已被 100% 从你的本地电脑中彻底移除，不会留下任何残留。[cite: 23]