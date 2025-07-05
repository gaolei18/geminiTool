@echo off
REM 设置本地代理（仅当前会话有效）
set HTTP_PROXY=http://127.0.0.1:33210
set HTTPS_PROXY=http://127.0.0.1:33210

REM 打开 PowerShell 并启动 Gemini CLI（假设 gemini 是在 PATH 中的命令）
start powershell -NoExit -Command "gemini"