# [cite_start]CrabClaw Local Agent Complete Uninstallation Guide [cite: 1]

Since CrabClaw runs as a pure Python script local entity, the uninstallation process does not require a control panel. [cite_start]You only need to perform the following four steps to achieve a "physical-level" complete erasure. [cite: 2]

## [cite_start]Step 1: Stop the Agent from Running [cite: 3]

[cite_start]If the agent is currently running in the background or terminal: [cite: 4]
1. [cite_start]Switch back to the command line (CMD/Terminal) window running the Python script. [cite: 5]
2. [cite_start]Repeatedly press Ctrl + C on your keyboard to force terminate the process. [cite: 6]
3. [cite_start]Alternatively, directly click the X in the upper right corner to close the command line window. [cite: 7]

## [cite_start]Step 2: Destroy the Agent's "Brain" and "Memory" (Crucial) [cite: 8]

[cite_start]According to the source code analysis, all local states of the agent (including databases, self-awareness, and dynamically learned skills) are stored in the `workspace` folder located in the same directory as the code. [cite: 9]
1. [cite_start]Open the folder containing `crabclaw.py`. [cite: 10]
2. [cite_start]Find the folder named `workspace`. [cite: 11]
3. [cite_start]Delete the entire `workspace` folder directly (it is recommended to empty the recycle bin). [cite: 12]

> [cite_start]Note: This will completely destroy its `hybrid_memory.db` (core memory database), `SOUL.md` (identity settings), and all independently written Python skill codes under the `skills` directory. [cite: 13]

## [cite_start]Step 3: Delete Source Code Files [cite: 14]

[cite_start]Delete the downloaded main program files: [cite: 15]
1. [cite_start]Delete the `crabclaw.py` file. [cite: 16]
2. [cite_start]If there are other matching scripts in the same directory (such as `run_qq_bot.py` mentioned in the source code comments), delete them as well. [cite: 17]

## [cite_start]Step 4: Clean Up Python Dependencies (Optional) [cite: 18]

[cite_start]If you specifically installed relevant third-party Python libraries to run this agent and will no longer need them in the future, you can open the command line (CMD or PowerShell) and execute the following command to uninstall them and free up some hard drive space: [cite: 19]

[cite_start]`pip uninstall openai httpx` [cite: 20]

> (If you have other Python projects using these libraries, please skip this step) [cite_start][cite: 21]

## [cite_start]🎉 Uninstallation Complete! [cite: 22]

[cite_start]After performing the above operations, the agent and all its data will be 100% completely removed from your local computer, leaving no residue behind. [cite: 23]