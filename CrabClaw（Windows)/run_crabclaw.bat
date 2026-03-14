@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title CrabClaw Commercial Pro - Windows 本地启动引擎
color 0B

echo ===================================================
echo.
echo        🌟 CrabClaw 商业开源引擎 (Pro Max) 🌟
echo                 [Windows 极客本地版]
echo.
echo ===================================================
echo.

:: 自动切换到当前绝对目录，防止跨卷启动故障
cd /d "%~dp0"

echo [系统自检] 正在验证 Windows 下的 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ❌ [致命错误] 未检测到 Python 运行环境！
    echo ---------------------------------------------------
    echo 1. 即将为您自动打开官方安全下载页面。
    echo 2. 【极其重要】：安装时务必勾选 "Add python.exe to PATH"！
    echo ---------------------------------------------------
    pause
    start https://www.python.org/downloads/windows/
    exit
)
echo ✅ Python 环境正常。
echo.

echo [系统自检] 正在验证框架商业级依赖库...
python -c "import openai, httpx" >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo ⚠️ 发现依赖缺失，正在接管并强制使用 sys.executable 防止虚拟环境污染...
    python -m pip install openai httpx -i https://pypi.tuna.tsinghua.edu.cn/simple
    if !errorlevel! neq 0 (
        echo ⚠️ 清华源网络拥堵，正在切换至阿里云灾备源...
        python -m pip install openai httpx -i https://mirrors.aliyun.com/pypi/simple/
    )
    echo ✅ 核心支持库自动补全完成！
    color 0B
) else (
    echo ✅ 框架组件库校验通过。
)
echo.

if not exist crabclaw.py (
    color 0C
    echo ❌ 找不到核心引擎 crabclaw.py！请确保所有文件在一起。
    pause
    exit
)

echo ===================================================
echo 🚀 引擎点火中...
echo ===================================================
echo.

set PYTHONIOENCODING=utf-8
python crabclaw.py

echo.
echo ⚠️ 引擎运行结束或发生异常闪退。
pause