#!/bin/bash

# MCP Calculator 快速启动脚本

echo "🚀 启动 MCP Calculator..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 setup_venv.sh 创建环境"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️ .env 文件不存在，请先配置环境变量"
    echo "📝 请参考 README.md 中的配置说明创建 .env 文件"
    exit 1
fi

# 启动项目
echo "🎯 启动 MCP Calculator..."
python mcp_pipe.py yo_mcp.py
