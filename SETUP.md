# PetriCode Telegram Bot - 启动指南

## 📋 目录

1. [环境要求](#环境要求)
2. [快速开始](#快速开始)
3. [详细步骤](#详细步骤)
4. [运行机器人](#运行机器人)
5. [停止机器人](#停止机器人)
6. [常见问题](#常见问题)

---

## 环境要求

- Python 3.8 或更高版本
- Git
- Telegram Bot Token（从 @BotFather 获取）

---

## 快速开始

```bash
# 1. 克隆仓库
git clone git@github.com:davidyuan666/PetriCode.git
cd PetriCode

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 配置 Token
cp petircode/.env.example petircode/.env
# 编辑 petircode/.env 文件，填入你的 Telegram Bot Token

# 6. 运行机器人
python -m petircode.main
```

---

## 详细步骤

### 步骤 1: 克隆仓库

```bash
git clone git@github.com:davidyuan666/PetriCode.git
cd PetriCode
```

### 步骤 2: 创建虚拟环境

虚拟环境可以隔离项目依赖，避免与系统 Python 包冲突。

```bash
python -m venv venv
```

这会在项目目录下创建一个 `venv` 文件夹。

### 步骤 3: 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

激活后，命令行提示符前会显示 `(venv)`。

### 步骤 4: 安装依赖

```bash
pip install -r requirements.txt
```

这会安装以下包：
- `python-telegram-bot` - Telegram Bot API
- `requests` - HTTP 请求库
- `python-dotenv` - 环境变量管理
- `aiohttp` - 异步 HTTP 客户端
- `beautifulsoup4` - HTML 解析
- `lxml` - XML/HTML 解析器

### 步骤 5: 配置 Telegram Bot Token

1. 复制配置文件模板：
```bash
cp petircode/.env.example petircode/.env
```

2. 编辑 `petircode/.env` 文件：
```bash
# Windows 使用记事本
notepad petircode/.env

# Linux/Mac 使用 nano 或 vim
nano petircode/.env
```

3. 填入你的 Telegram Bot Token：
```env
TELEGRAM_BOT_TOKEN=你的_Bot_Token_这里
```

**如何获取 Telegram Bot Token？**
1. 在 Telegram 中搜索 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称
4. BotFather 会返回你的 Token

---

## 运行机器人

### 方式 1: 前台运行（推荐用于测试）

```bash
python -m petircode.main
```

你会看到类似的输出：
```
2026-01-29 23:18:56 - petircode.bot - INFO - Starting PetriCode bot...
2026-01-29 23:19:00 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot.../getMe "HTTP/1.1 200 OK"
2026-01-29 23:19:01 - telegram.ext.Application - INFO - Application started
```

按 `Ctrl+C` 可以停止机器人。

### 方式 2: 后台运行（Linux/Mac）

```bash
nohup python -m petircode.main > bot.log 2>&1 &
```

查看日志：
```bash
tail -f bot.log
```

### 方式 3: 使用 screen 或 tmux（Linux/Mac）

使用 screen：
```bash
screen -S petribot
python -m petircode.main
# 按 Ctrl+A 然后按 D 分离会话
# 重新连接: screen -r petribot
```

---

## 停止机器人

### 前台运行
按 `Ctrl+C` 停止

### 后台运行
```bash
# 查找进程
ps aux | grep petircode

# 停止进程（替换 PID 为实际进程号）
kill PID
```

---

## 常见问题

### Q1: 提示 "TELEGRAM_BOT_TOKEN is required"
**A:** 检查 `petircode/.env` 文件是否存在，并且正确填写了 Token。

### Q2: 虚拟环境激活失败
**A:**
- Windows: 确保使用 `venv\Scripts\activate`
- Linux/Mac: 确保使用 `source venv/bin/activate`

### Q3: 机器人不响应消息
**A:**
1. 检查机器人是否正在运行
2. 检查 Token 是否正确
3. 查看日志中是否有错误信息

### Q4: 如何验证机器人是否在线？
**A:** 在 Telegram 中向机器人发送 `/start`，如果收到回复说明机器人在线。

### Q5: 如何更新代码？
**A:**
```bash
git pull origin main
pip install -r requirements.txt  # 如果依赖有更新
```

---

## 可用命令

机器人启动后，在 Telegram 中可以使用以下命令：

- `/start` - 启动机器人，显示欢迎消息
- `/help` - 显示帮助信息和所有可用命令
- `/info` - 显示机器人版本和信息
- `/fetch <url>` - 获取指定 URL 的网页内容
- 发送任何文本消息 - 机器人会回显你的消息

---

## 项目结构

```
PetriCode/
├── venv/                    # 虚拟环境（不会提交到 Git）
├── petircode/              # 主代码目录
│   ├── .env                # 配置文件（不会提交到 Git）
│   ├── .env.example        # 配置文件模板
│   ├── .gitignore          # Git 忽略文件
│   ├── README.md           # 项目说明
│   ├── __init__.py
│   ├── main.py             # 程序入口
│   ├── bot.py              # 机器人核心逻辑
│   ├── config.py           # 配置管理
│   ├── handlers/           # 命令处理器
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── services/           # 外部服务
│   │   ├── __init__.py
│   │   ├── fetcher.py      # URL 内容获取
│   │   └── search.py       # 搜索服务
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── text.py         # 文本处理
├── requirements.txt        # Python 依赖列表
├── SETUP.md               # 本文档
└── README.md              # 项目说明
```

---

## 开发建议

1. **修改代码后重启机器人**：代码修改后需要停止并重新启动机器人才能生效
2. **查看日志**：遇到问题时查看控制台输出的日志信息
3. **测试新功能**：在 Telegram 中直接测试新添加的命令和功能

---

## 联系与支持

- GitHub 仓库: https://github.com/davidyuan666/PetriCode
- 机器人用户名: @myautomaticagentbot

---

**祝你使用愉快！** 🚀
