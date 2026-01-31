# Telegram Bot MCP Server

为 Claude Code CLI 提供 Telegram 消息收发能力的 MCP 服务器。

## 功能

- 发送消息到 Telegram
- 接收 Telegram 消息
- 异步架构，高性能

## 安装

```bash
cd TelegramBotMCP
pip install -r requirements.txt
```

## 配置

1. 创建 `.env` 文件：
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

2. 添加到 Claude Code CLI：
```bash
claude mcp add telegram-bot -e TELEGRAM_BOT_TOKEN=your_token -- python /path/to/mcp_server.py
```

3. 验证：
```bash
claude mcp list
```

## API

### send_telegram_message
发送消息到 Telegram。

参数:
- `chat_id` (string): Chat ID，如 "123456789"
- `text` (string): 消息内容

### get_telegram_updates
获取最近的消息。

参数:
- `limit` (number): 消息数量，默认 10

## 使用

在 Claude Code CLI 中直接使用自然语言：
```
发送消息到我的 Telegram (ID: 123456789): Hello!
```

## 获取 Chat ID

向 Bot 发送消息后，运行：
```bash
python test_mcp.py
```

## 故障排除

- **连接失败**: 检查 Python 和依赖安装
- **发送失败**: 确认 Chat ID 格式正确
- **无消息**: 确保已向 Bot 发送过消息

## 技术栈

- Python 3.8+
- python-telegram-bot
- MCP SDK
- asyncio

## 许可证

MIT License
