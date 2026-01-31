#!/usr/bin/env python3
"""
Telegram to Claude Code Bridge
Polls Telegram messages and forwards them to Claude Code CLI
"""
import asyncio
import logging
import os
import subprocess
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming Telegram messages and forward to Claude Code CLI"""
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name

    logger.info(f"Received message from {user_name} (ID: {chat_id}): {user_message}")

    # Send "processing" message
    status_msg = await update.message.reply_text("🤔 Claude Code 正在处理...")

    try:
        # Call Claude Code CLI
        result = subprocess.run(
            ["claude", "code", user_message],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.getenv("CLAUDE_WORK_DIR", "C:\\workspace\\claudecodelabspace")
        )

        # Get response
        response = result.stdout.strip() if result.stdout else result.stderr.strip()

        if not response:
            response = "✅ 执行完成（无输出）"

        # Update status
        await status_msg.edit_text("✅ Claude Code 执行完成")

        # Send response (split if too long)
        if len(response) > 4000:
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(f"📄 输出 (第{i+1}/{len(chunks)}部分):\n\n{chunk}")
        else:
            await update.message.reply_text(f"📄 输出:\n\n{response}")

    except subprocess.TimeoutExpired:
        await status_msg.edit_text("⏱️ 执行超时")
        await update.message.reply_text("执行超时，请稍后重试")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await status_msg.edit_text("❌ 执行出错")
        await update.message.reply_text(f"错误: {str(e)}")


async def main():
    """Start the bot"""
    logger.info("Starting Telegram to Claude Code bridge...")

    # Create application
    app = Application.builder().token(TOKEN).build()

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Bot is running. Send messages to @myautomaticagentbot")

    # Initialize and start
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
