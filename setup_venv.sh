#!/bin/bash

# MOSS MCP  项目 venv 环境设置脚本
# 用于从 conda 环境切换到 venv 环境管理

set -e  # 遇到错误时退出

echo "🚀 开始设置 MOSS MCP  项目的 venv 环境..."

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

echo "✅ venv 环境设置完成！"
echo ""
echo "📝 使用说明："
echo "1. 激活环境: source venv/bin/activate"
echo "2. 运行项目: python mcp_pipe.py yo_mcp.py"
echo "3. 退出环境: deactivate"
echo ""
echo "🎉 环境切换完成，所有功能保持不变！"
