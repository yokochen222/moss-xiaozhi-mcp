@echo off
REM MOSS MCP 快速启动脚本 (Windows)

echo 🚀 启动 MOSS MCP...

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo ❌ 虚拟环境不存在，请先运行 setup_venv.bat 创建环境
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查 .env 文件
if not exist ".env" (
    echo ⚠️ .env 文件不存在，请先配置环境变量
    echo 📝 请参考 README.md 中的配置说明创建 .env 文件
    pause
    exit /b 1
)

REM 启动项目
echo 🎯 启动 MOSS MCP ...
python mcp_pipe.py yo_mcp.py
