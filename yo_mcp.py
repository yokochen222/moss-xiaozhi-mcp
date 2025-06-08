from mcp.server.fastmcp import FastMCP
import os
import importlib

# Create an MCP server
mcp = FastMCP("YOKO_MCP_SERVER")

# 自动导入并注册tools文件夹中的所有模块
tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
for filename in os.listdir(tools_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'tools.{filename[:-3]}'
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_tool'):
                module.register_tool(mcp)
        except ImportError as e:
            print(f"Failed to import {module_name}: {e}")

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")