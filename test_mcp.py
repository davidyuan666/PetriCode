#!/usr/bin/env python3
"""
Test script for Telegram MCP Server
"""
import asyncio
import os
from telegram import Bot

async def test_bot():
    """Test Telegram bot functionality"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is required")
        return
    bot = Bot(token=token)

    print("Testing Telegram Bot...")
    print(f"Bot token: {token[:20]}...")

    # Test 1: Get bot info
    try:
        me = await bot.get_me()
        print(f"\n[OK] Bot info retrieved:")
        print(f"  Username: @{me.username}")
        print(f"  Name: {me.first_name}")
        print(f"  ID: {me.id}")
    except Exception as e:
        print(f"\n[ERROR] Failed to get bot info: {e}")
        return

    # Test 2: Get updates
    try:
        updates = await bot.get_updates(limit=5)
        print(f"\n[OK] Retrieved {len(updates)} updates")

        if updates:
            print("\nRecent messages:")
            for update in updates[-5:]:
                if update.message:
                    msg = update.message
                    username = msg.from_user.username if msg.from_user.username else "N/A"
                    print(f"\n  From: {msg.from_user.first_name} (@{username})")
                    print(f"  Chat ID: {msg.chat_id}")
                    print(f"  Text: {msg.text}")
                    print(f"  Date: {msg.date}")
        else:
            print("  No recent messages")
    except Exception as e:
        print(f"\n[ERROR] Failed to get updates: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
