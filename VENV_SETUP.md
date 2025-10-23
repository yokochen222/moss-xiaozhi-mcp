# MOSS-XIAOZHI-MCP 项目 venv 环境设置指南

## 📋 概述

本文档指导您将 MCP 项目从 conda 环境管理切换到 venv 环境管理，确保所有功能正常运行。

## 🔄 环境切换步骤

### 1. 自动设置（推荐）

#### macOS/Linux 用户

```bash
# 执行环境设置脚本
./setup_venv.sh
```

#### Windows 用户

```cmd
# 双击运行或在命令行执行
setup_venv.bat
```

该脚本将自动：

- 创建 Python 虚拟环境
- 激活虚拟环境
- 升级 pip 包管理器
- 安装所有项目依赖

### 2. 手动设置

#### macOS/Linux 用户

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 升级 pip
pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt
```

#### Windows 用户

```cmd
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate.bat

# 3. 升级 pip
python -m pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt
```

## 🚀 使用指南

### 激活环境

每次使用项目前，需要激活虚拟环境：

#### macOS/Linux 用户

```bash
# 使用提供的激活脚本
./activate_venv.sh

# 或者手动激活
source venv/bin/activate
```

#### Windows 用户

```cmd
# 使用提供的激活脚本
activate_venv.bat

# 或者手动激活
venv\Scripts\activate.bat
```

### 运行项目

激活环境后，运行项目：

#### 快速启动

```bash
# macOS/Linux
./start.sh

# Windows
start.bat
```

#### 手动运行

```bash
# 激活环境后
python mcp_pipe.py yo_mcp.py
```

### 退出环境

使用完毕后退出虚拟环境：

```bash
# 所有平台通用
deactivate
```

## 📦 依赖包说明

项目依赖包已分类整理在 `requirements.txt` 中：

### 核心依赖

- `python-dotenv`: 环境变量管理
- `websockets`: WebSocket 通信
- `mcp`: MCP 协议支持
- `pydantic`: 数据验证

### 摄像头和视觉识别

- `opencv-python`: 计算机视觉处理
- `onvif_zeep`: ONVIF 摄像头协议

### 系统控制

- `pyautogui`: 自动化控制
- `scapy`: 网络包处理
- `getmac`: MAC 地址获取

### 其他依赖

- `requests`: HTTP 请求处理
- `numpy`: 数值计算支持

## 🔧 环境管理

### 查看已安装包

```bash
# 激活环境后
pip list
```

### 更新依赖

```bash
# 激活环境后
pip install --upgrade -r requirements.txt
```

### 添加新依赖

```bash
# 激活环境后安装新包
pip install 新包名

# 更新 requirements.txt
pip freeze > requirements.txt
```

## 🛠️ 故障排除

### 常见问题

1. **虚拟环境不存在**

   ```bash
   # 重新运行设置脚本
   ./setup_venv.sh
   ```
2. **依赖安装失败**

   ```bash
   # 确保网络连接正常，尝试使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```
3. **权限问题**

   ```bash
   # 确保脚本有执行权限
   chmod +x setup_venv.sh
   chmod +x activate_venv.sh
   ```

### 环境验证

验证环境是否正确设置：

```bash
# 激活环境
source venv/bin/activate

# 检查 Python 版本
python --version

# 检查关键依赖
python -c "import cv2; print('OpenCV 版本:', cv2.__version__)"
python -c "import websockets; print('WebSockets 可用')"
python -c "import mcp; print('MCP 可用')"
```

## 📁 项目结构

```
mcp-calculator/
├── venv/                    # 虚拟环境目录
├── setup_venv.sh           # 环境设置脚本
├── activate_venv.sh        # 环境激活脚本
├── requirements.txt        # 依赖包列表
├── VENV_SETUP.md          # 本文档
├── mcp_pipe.py            # 主程序入口
├── yo_mcp.py              # MCP 服务器
├── core/                   # 核心模块
├── tools/                  # 工具模块
└── captures/               # 截图保存目录
```

## ⚠️ 注意事项

1. **环境隔离**: venv 环境与系统 Python 环境完全隔离，不会影响其他项目
2. **依赖管理**: 所有依赖都安装在虚拟环境中，便于管理和迁移
3. **功能保持**: 切换到 venv 后，所有原有功能保持不变
4. **配置不变**: `.env` 配置文件无需修改，继续使用原有配置

## 🎯 优势

- **轻量级**: venv 比 conda 更轻量，启动更快
- **标准化**: 符合 Python 官方推荐的虚拟环境管理方式
- **兼容性**: 与各种 Python 版本和操作系统兼容性更好
- **简单性**: 管理方式更简单直观

## 📞 支持

如果在环境切换过程中遇到问题，请检查：

1. Python 版本是否为 3.7+
2. 网络连接是否正常
3. 磁盘空间是否充足
4. 权限是否正确

---

**🎉 环境切换完成！现在您可以使用更轻量、更标准的 venv 环境来管理 MCP Calculator 项目了！**
