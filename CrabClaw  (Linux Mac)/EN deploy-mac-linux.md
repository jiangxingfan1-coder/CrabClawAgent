# 🍏 CrabClaw Agent System: Mac & Linux Deployment and Running Guide

When you are ready to migrate the CrabClaw agent system from a Windows environment to run on a Mac or Linux server, please **be sure** to read this guide to avoid the most common "invisible traps" in cross-platform deployment.

## 🚨 Core Pitfall Warning: Windows' "Invisible Line Breaks" (CRLF vs LF)

* Plain text files (such as `.txt`) created or edited under the Windows system use CRLF (Carriage Return + Line Feed) as the line break by default.
* However, the terminals of Mac and Linux systems **only recognize** the LF (Line Feed) format.
* If you directly change the extension of a launcher text file created on Windows to `.sh` and run it on Mac/Linux, the system will report an error:
  > `bash\r: No such file or directory` or `command not found`
* To completely avoid this issue, please strictly follow the steps below for migration:

---

## 🛠️ Standard Deployment Steps (Recommended)

### Step 1: Clean Creation on Mac/Linux (The Safest Approach)
1. **Do not** directly change the extension of the `.txt` file transferred from Windows.
2. On your Mac or Linux system, open a clean text editor (such as Mac's built-in "TextEdit" in plain text mode, or use VS Code, Sublime).
3. Create two new blank files.
4. **Copy and paste** the final generated `.sh` code content into these two blank files respectively.
5. Name and save them respectively as:
   * `run_crabclaw.sh`
   * `run_qq_bot.sh`
   *(Files saved in this way naturally are in the standard Mac/Linux LF format, without any historical baggage.)*

### Step 2: Grant Execution Permissions (Unix System Mandatory Requirement)
Due to security mechanisms, Mac and Linux do not allow directly running newly created scripts by default. You must give them a "pass" through the terminal.
1. Open Mac's **Terminal** or Linux's command line.
2. Use the `cd` command to enter the folder where you store these scripts. For example:
   `cd /Users/YourUsername/Desktop/CrabClawBotDirectory`
3. Enter the following commands sequentially and press Enter to grant them executable permissions:
   * `chmod +x run_crabclaw.sh`
   * `chmod +x run_qq_bot.sh`

### Step 3: Start the Engine
After the permissions are granted, you can start them at any time:
* **Start the Master Engine**: Enter `./run_crabclaw.sh` in the terminal
* **Start the QQ Daemon**: Enter `./run_qq_bot.sh` in the terminal

---

## 💡 Advanced Tips and Remedial Measures

### 🍎 Mac Exclusive: How to Implement "Double-Click to Run"?
On a Mac, by default, double-clicking a `.sh` file will open it with a text editor instead of running it. If you want it to launch by double-clicking like a Windows `.bat` file:
1. Complete the `chmod +x` authorization step above.
2. Change the file extension from `.sh` to `.command`.
   That is: `run_crabclaw.command` and `run_qq_bot.command`.
3. From now on, just double-click this `.command` file, and Mac will automatically pop up a terminal window and run your agent!

### 🔧 Remedy: What if the file already has Windows line breaks?
If you have already transferred the files from Windows to a Linux cloud server and don't want to re-copy and paste, you can use the powerful `sed` command to clean up the invisible `\r` characters with one click.

Execute the following commands in the terminal to "clean" the files:
* `sed -i 's/\r$//' run_crabclaw.sh`
* `sed -i 's/\r$//' run_qq_bot.sh`

*(Note: The default `sed` syntax on Mac systems is slightly different; it is recommended to prioritize using the re-copying method in "Step 1" on Mac.)*

---

**🎉 Wishing you a smooth deployment! The CrabClaw Agent cross-platform engine is ready.**