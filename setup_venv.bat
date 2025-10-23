@echo off
REM MOSS MCP 项目 venv 环境设置脚本 (Windows)
REM 用于从 conda 环境切换到 venv 环境管理

echo 🚀 开始设置 MOSS MCP 项目的 venv 环境...

REM 检查 Python 版本
echo 📋 检查 Python 版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或未添加到 PATH，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 创建虚拟环境
echo 📦 创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ 虚拟环境创建失败
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级 pip
echo ⬆️ 升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 📚 安装项目依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo ✅ venv 环境设置完成！
echo.
echo 📝 使用说明：
echo 1. 激活环境: venv\Scripts\activate.bat
echo 2. 运行项目: python mcp_pipe.py yo_mcp.py
echo 3. 退出环境: deactivate
echo.
echo 🎉 环境切换完成，所有功能保持不变！
pause
