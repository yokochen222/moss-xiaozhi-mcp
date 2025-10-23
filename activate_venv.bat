@echo off
REM MCP Calculator 项目 venv 环境激活脚本 (Windows)

echo 🔧 激活 MCP Calculator venv 环境...

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo ❌ 虚拟环境不存在，请先运行 setup_venv.bat 创建环境
    pause
    exit /b 1
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

echo ✅ venv 环境已激活！
echo.
echo 📝 可用命令：
echo   - 运行项目: python mcp_pipe.py yo_mcp.py
echo   - 退出环境: deactivate
echo   - 查看已安装包: pip list
echo.
echo 🎯 环境已准备就绪，可以开始使用！
