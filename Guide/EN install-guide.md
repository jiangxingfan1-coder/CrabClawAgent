# 🦀 CrabClaw Cross-Platform 1-Click Local Deployment Guide

No coding or programming skills required! Just "double-click" (or execute a simple command) to complete the local deployment of your fully autonomous intelligent agent (Local Agent)!

> ⚠️ **Note**: This is the cross-platform commercial evolved version, supporting Windows / macOS / Linux. You absolutely DO NOT need to manually modify any code files!

## 🎯 Preparation: Required Files

Please create a new standard folder on your desktop and name it `My_Agent` (or whatever you prefer).
Ensure the following files are placed inside this folder (make sure you have already removed the `.txt` extensions using "Save As"):

- `crabclaw.py` (The core brain code)
- `run_crabclaw.bat` (Exclusive 1-click launcher for Windows users)
- `run_crabclaw.sh` (Exclusive launcher for Mac / Linux users)

---

## 🚀 Step 1: Install System Environment (Python)

CrabClaw's core is written in Python, so your computer needs this environment to run it.

### 🪟 For Windows Users: Foolproof Auto-Detection

How do you know if it's installed? Just double-click `run_crabclaw.bat`. If a red text prompt says "Python not detected" and automatically opens a webpage for you, it means it's not installed.

1. Click the yellow **Download Python** button on the opened webpage.
2. Double-click the downloaded installer package.
3. 🚨 **CRUCIAL STEP (Installation WILL fail if not checked)**: 
   At the very bottom of the installation screen, there is a checkbox that says `Add python.exe to PATH` (or `Add Python to environment variables`). **You MUST check this box!** Then click *Install Now*.

### 🍎 For macOS Users:

Open the **Terminal** on your Mac, type the following command, and hit Enter (Homebrew is recommended):
```bash
brew install python
```
*(If you don't have brew, you can download the Mac installer directly from python.org and click "Next" all the way through.)*

### 🐧 For Linux Users:

Open the terminal and enter the command based on your system type:

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3 python3-pip
```
**CentOS/RHEL:**
```bash
sudo yum install python3 python3-pip
```

---

## 🚀 Step 2: 1-Click Ignition & Smart Configuration!

Forget the old, tedious steps of "opening code with Notepad to modify it"—the system will now guide you automatically!

### 👉 Windows Users:
Simply double-click and run `run_crabclaw.bat`.

### 👉 macOS / Linux Users:
Navigate to your folder in the terminal (e.g., `cd ~/Desktop/My_Agent`), then enter these two commands:
```bash
chmod +x run_crabclaw.sh
./run_crabclaw.sh
```

### 🤖 First-Run Wizard (All Systems):

Upon your first successful launch, the black command-line window will **automatically** download missing runtime components (like `openai`, etc., with a progress bar). Once downloaded, a friendly wizard will pop up and ask you:

- **Please enter your API Key**: Paste the `sk-xxxxxx` key you applied for from major model platforms (e.g., DeepSeek, Alibaba Cloud Bailian) and press Enter.
- **Please enter API Base URL**: If you are using DeepSeek, just press Enter to skip (it's filled in by default).
- **Please enter the model name you want to call**: Just press Enter to skip (default is `deepseek-chat`).

> ✅ **All Done!** Your configuration will be automatically saved in a `config.json` file in the same directory. Next time you double-click to start, it will take you straight to the chat interface:
> **"🦀 CrabClaw Commercial Agent Started 🚀"**

---

## 💡 Step 3: Recommended Features to Try

Now you can type in everyday language right after the `👤 Master:` cursor to chat with it! Try these:

- 💻 **System Control**: "Help me open the calculator on my computer" / "Open Notepad."
- 🧠 **Long-term Memory**: "Remember that my cat's name is Boss, and he loves salmon." (It will remember this even after you restart your computer!)
- 📚 **Autonomous Learning**: "I don't understand quantum mechanics. Go search the web and give me a 500-word layman's explanation."
- 🛠️ **Self-Programming**: "Write a skill for me called `get_weather` to check the weather."

*(Note: When it wants to execute a dangerous operation, a highly visible red warning will pop up on the screen. It will only execute if you type `y` to agree. It is absolutely safe!)*

---

## 🏥 FAQ & Troubleshooting Guide

### ❓ Q1: (Windows) After installing Python, double-clicking the .bat still says "Python not detected"?
* **Answer**: This is 100% because you **forgot to check** the `Add python.exe to PATH` box at the bottom during installation!
* **Solution**: Open the Control Panel, uninstall the Python you just installed, double-click the installer again, **make sure to check that box at the bottom**, and reinstall it.

### ❓ Q2: Prompt says [Alert] Node authentication failed or account is in arrears?
* **Answer**: There is an issue with your brain (the Large Language Model), usually a mistyped Key or insufficient funds.
* **Solution**:
  1. Check if the API Key you entered is missing a letter or contains spaces.
  2. Log into the platform where you applied for the API Key (like the DeepSeek official website) and check if your account balance is depleted. Recharging $2-$5 goes a very long way!
  *(To modify a wrongly entered Key, simply open the `config.json` file in the same directory with Notepad, make the correction, save it, and restart.)*

### ❓ Q3: Prompt says missing dependencies, or the interface gets stuck on "Automatically downloading necessary components for you" for a long time?
* **Answer**: Network fluctuations are preventing connection to the Python download mirrors.
* **Solution**: Close the window and double-click to run it again. If it fails multiple times in a row, you can try directly telling the AI agent: *"I am missing the xxx package, please use your shell tool to execute `pip install xxx` to install it for me,"* and the AI will automatically write the code to install it for you!

### ❓ Q4: (Mac/Linux) Prompt says `Permission denied`?
* **Answer**: Your system's security mechanism blocked the script from running.
* **Solution**: Open the terminal, enter `chmod +x run_crabclaw.sh` to grant it executable permissions, and then run `./run_crabclaw.sh` again.

### ❓ Q5: Why is the text displaying as garbled characters/symbols?
* **Answer**: The new version of the code already includes an ultimate UTF-8 anti-garbled patch.
* **Solution**: If you still see garbled text, try **right-clicking the very top title bar of the command prompt window -> Properties -> Font -> Change to a clear monospaced font like `Consolas`**.