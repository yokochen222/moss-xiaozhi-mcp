#!/bin/bash

# MCP Calculator 项目 venv 环境激活脚本

echo "🔧 激活 MCP Calculator venv 环境..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 setup_venv.sh 创建环境"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

echo "✅ venv 环境已激活！"
echo ""
echo "📝 可用命令："
echo "  - 运行项目: python mcp_pipe.py yo_mcp.py"
echo "  - 退出环境: deactivate"
echo "  - 查看已安装包: pip list"
echo ""
echo "🎯 环境已准备就绪，可以开始使用！"
