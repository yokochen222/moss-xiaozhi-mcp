## 本工程基于虾哥 MCP实现

原项目地址：https://github.com/78/mcp-calculator

## 视频展示
https://www.bilibili.com/video/BV1TpTNzbE3u/?vd_source=3cdb33659e80ec67cacea8b3ce284283

## 环境要求(建议使用conda创建环境)

- Python 3.7+
- websockets>=11.0.3
- python-dotenv>=1.0.0
- mcp>=1.8.1
- pydantic>=2.11.4

## conda虚拟环境创建

```bash
conda create -n xiaozhi-mcp python=3.10
```

## 依赖安装

```bash
pip install -r requirements.txt
```

## 配置

依赖安装完毕后别忘了 创建.env文件 内容如下：

```bash
# 小智 MCP MCP接入点地址
MCP_ENDPOINT = wss://api.xiaozhi.me/mcp/?token=需要改成你的小智后台的MCP接入点
# ONVIF 摄像头IP地址
ONVIF_CAMERA_IP = 192.168.10.143
# ONVIF 摄像头端口，天地伟业摄像头端口为80，根据自己的摄像头端口修改
ONVIF_CAMERA_PORT = 80
# ONVIF 摄像头账号
ONVIF_CAMERA_USERNAME = admin
# ONVIF 摄像头密码
ONVIF_CAMERA_PASSWORD = 123456
# 是否启用ONVIF云台控制(带云台的摄像头可以开启，不开启将不会开启控制注册)
ONVIF_CAMERA_PTZ_ENABLED = false
# 是否启用ONVIF摄像头识别并保存日志
ONVIF_CAMERA_LOG = false
# 是否启用ONVIF截图保存到本地
ONVIF_CAMERA_CAPTURE = false
```

## 启动

```bash
python mcp_pipe.py yo_mcp.py
```

# 觉得有用的兄弟们 别忘了点个 star 支持下

**注意！！！！由于控制PC设备等功能是基于MacOS实现 win的小伙伴需要自行修改**
