## 本工程基于虾哥 MCP实现

原项目地址：https://github.com/78/mcp-calculator

## 环境要求(建议使用conda创建环境)

- Python 3.7+
- websockets>=11.0.3
- python-dotenv>=1.0.0
- mcp>=1.8.1
- pydantic>=2.11.4


## 配置

依赖安装完毕后别忘了 创建.env文件 内容如下：

```bash
MCP_ENDPOINT = wss://api.xiaozhi.me/mcp/?token=需要改成你的小智后台的MCP接入点
```

## 启动

```bash
python mcp_pipe.py yo_mcp.py
```

**注意！！！！由于控制PC设备等功能是基于MacOS实现 win的小伙伴需要自行修改**
