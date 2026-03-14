@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title CrabClaw QQ Bot - Windows 企业守护进程
color 0b

echo ===================================================
echo.
echo           🦀 CrabClaw QQ 机器人总线
echo               [Windows 守护进程版]
echo.
echo ===================================================
echo.
echo [提示] 启动后请保持此窗口打开。
echo [状态] 🛡️ 守护机制激活：异常崩溃或断网将自动秒级重连。
echo.

cd /d "%~dp0"

if not exist crabclaw.py (
    color 0C
    echo ❌ 找不到智能体核心引擎 crabclaw.py！
    pause
    exit
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ❌ 未检测到 Python 运行环境！
    pause
    exit
)

echo [系统自检] 正在验证 QQ 机器人运行核心库...
python -c "import openai, httpx, botpy" >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo ⚠️ 缺失 botpy 等核心库，接管安装中...
    python -m pip install qq-botpy openai httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
    if !errorlevel! neq 0 (
        python -m pip install qq-botpy openai httpx -i https://mirrors.aliyun.com/pypi/simple/
    )
    echo ✅ 安装完成！
    color 0b
)

set PYTHONIOENCODING=utf-8

:restart_bot
echo.
echo 🔄 正在唤醒引擎并连接腾讯网关...
echo.

python run_qq_bot.py

color 0e
echo.
echo ===================================================
echo ⚠️ 机器人连接已断开（配置错误、被封禁或异常崩溃）。
echo 🔄 触发自愈机制，5秒后自动重启... (按 Ctrl+C 彻底关闭)
echo ===================================================
timeout /t 5
color 0b
echo.
goto restart_bot