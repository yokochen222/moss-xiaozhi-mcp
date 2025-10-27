# MOSS MCP Windows 用户指南

## 🪟 Windows 用户专用说明

本指南专门为 Windows 用户提供详细的 venv 环境设置和使用说明。

## 📋 系统要求

- Windows 10/11
- Python 3.7+ (推荐 Python 3.10+)
- 管理员权限（用于安装依赖）

## 🚀 快速开始

### 步骤 1: 环境设置

#### 方法一：双击运行（推荐）

1. 双击 `setup_venv.bat` 文件
2. 等待脚本自动完成环境设置
3. 看到 "环境设置完成" 提示

#### 方法二：命令行运行

```cmd
# 打开命令提示符或 PowerShell
# 切换到项目目录
cd C:\path\to\mcp-calculator

# 运行设置脚本
setup_venv.bat
```

### 步骤 2: 配置环境变量

确保 `.env` 文件存在并正确配置：

```env
# 小智 MCP MCP接入点地址
MCP_ENDPOINT = wss://api.xiaozhi.me/mcp/?token=xxx

# 视觉识别相关配置
ENABLED_IP_CAMERA = false
ONVIF_CAMERA_IP = 192.168.10.143
ONVIF_CAMERA_PORT = 80
ONVIF_CAMERA_USERNAME = admin
ONVIF_CAMERA_PASSWORD = 123456
ONVIF_CAMERA_PTZ_ENABLED = false
ONVIF_CAMERA_LOG = false
ONVIF_CAMERA_CAPTURE = false

# Homeasstant 相关配置
HA_ADDRESS = http://192.168.1.197:8123
HA_AUTH_TOKEN = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxx
```

### 步骤 3: 启动项目

#### 方法一：双击启动（推荐）

双击 `start.bat` 文件即可自动启动项目。

#### 方法二：命令行启动

```cmd
# 激活环境
activate_venv.bat

# 运行项目
python mcp_pipe.py yo_mcp.py
```

## 🔧 日常使用

### 激活环境

每次使用前需要激活虚拟环境：

```cmd
# 双击运行
activate_venv.bat

# 或命令行运行
venv\Scripts\activate.bat
```

### 运行项目

```cmd
# 快速启动
start.bat

# 或手动运行
python mcp_pipe.py yo_mcp.py
```

### 退出环境

```cmd
deactivate
```

## 🛠️ 环境管理

### 查看已安装包

```cmd
# 激活环境后
pip list
```

### 安装新依赖

```cmd
# 激活环境后
pip install 新包名

# 更新 requirements.txt
pip freeze > requirements.txt
```

### 更新所有依赖

```cmd
# 激活环境后
pip install --upgrade -r requirements.txt
```

## 🔍 故障排除

### 常见问题

1. **Python 未安装或未添加到 PATH**
   ```
   解决方案：
   1. 下载并安装 Python 3.10+ from https://python.org
   2. 安装时勾选 "Add Python to PATH"
   3. 重启命令提示符
   ```

2. **权限不足**
   ```
   解决方案：
   1. 以管理员身份运行命令提示符
   2. 右键点击命令提示符 → "以管理员身份运行"
   ```

3. **网络连接问题**
   ```
   解决方案：
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

4. **依赖安装失败**
   ```
   解决方案：
   1. 检查网络连接
   2. 使用国内镜像源
   3. 逐个安装依赖包
   ```

### 环境验证

运行环境测试脚本：

```cmd
# 激活环境后
python test_environment.py
```

## 📁 Windows 项目结构

```
mcp-calculator/
├── venv/                    # 虚拟环境目录
│   └── Scripts/            # Windows 激活脚本
├── setup_venv.bat          # 环境设置脚本
├── activate_venv.bat       # 环境激活脚本
├── start.bat               # 快速启动脚本
├── test_environment.py     # 环境测试脚本
├── requirements.txt        # 依赖包列表
├── mcp_pipe.py            # 主程序入口
├── yo_mcp.py              # MCP 服务器
├── core/                   # 核心模块
├── tools/                  # 工具模块
└── captures/               # 截图保存目录
```

## ⚡ 性能优化

### Windows 特定优化

1. **禁用 Windows Defender 实时保护**（仅限项目目录）
2. **使用 SSD 存储**项目文件
3. **关闭不必要的后台程序**

### 启动加速

```cmd
# 使用快速启动脚本
start.bat

# 或创建桌面快捷方式
# 右键 start.bat → "发送到" → "桌面快捷方式"
```

## 🔒 安全注意事项

1. **不要将 .env 文件提交到版本控制**
2. **定期更新依赖包**
3. **使用虚拟环境隔离项目**

## 📞 技术支持

如果遇到问题：

1. 查看 `VENV_SETUP.md` 获取详细说明
2. 运行 `python test_environment.py` 检查环境
3. 检查 `.env` 配置文件
4. 确保 Python 版本正确

## 🎯 Windows 用户优势

- ✅ 双击即可运行，无需命令行知识
- ✅ 图形化界面友好
- ✅ 自动环境管理
- ✅ 一键启动项目

---

**🎉 Windows 用户现在可以轻松使用 MOSS MCP 项目了！**

**所有功能保持不变，但使用更加简单便捷！**
