#!/usr/bin/env python3
"""
Test script for Telegram MCP Server
"""
import asyncio
from telegram import Bot

TOKEN = "7871305869:AAECL5dp4eItPvHhiJ9UxEuzPweGKHcXjNM"


async def main():
    bot = Bot(TOKEN)

    # Test 1: Get bot info
    print("=== Test 1: Bot Info ===")
    me = await bot.get_me()
    print(f"Bot Username: @{me.username}")
    print(f"Bot ID: {me.id}")
    print(f"Bot Name: {me.first_name}")

    # Test 2: Get updates
    print("\n=== Test 2: Get Updates ===")
    updates = await bot.get_updates(limit=5)
    print(f"Total updates: {len(updates)}")

    if updates:
        print("\nRecent messages:")
        for update in updates:
            if update.message:
                msg = update.message
                print(f"  From: {msg.from_user.first_name}")
                print(f"  Chat ID: {msg.chat_id}")
                print(f"  Text: {msg.text}")
                print()
    else:
        print("No messages yet. Please send a message to @myautomaticagentbot first!")

    print("\n=== MCP Server Ready ===")
    print("You can now use Claude Code CLI to send messages!")
    print("Example: 'Send a message to my Telegram'")


if __name__ == "__main__":
    asyncio.run(main())
