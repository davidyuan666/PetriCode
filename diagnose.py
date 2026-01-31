#!/usr/bin/env python3
"""
Diagnostic script for MCP server
"""
import sys
import traceback

print("=== MCP Server Diagnostic ===\n")

# Test 1: Import modules
print("1. Testing imports...")
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from telegram import Bot
    print("   [OK] All modules imported successfully\n")
except Exception as e:
    print(f"   [ERROR] Import failed: {e}\n")
    sys.exit(1)

# Test 2: Import mcp_server module
print("2. Testing mcp_server module...")
try:
    import mcp_server
    print("   [OK] mcp_server module imported\n")
except Exception as e:
    print(f"   [ERROR] Failed to import mcp_server: {e}\n")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check function definitions
print("3. Checking function definitions...")
try:
    print(f"   - send_message: {hasattr(mcp_server, 'send_message')}")
    print(f"   - get_updates: {hasattr(mcp_server, 'get_updates')}")
    print(f"   - call_tool: {hasattr(mcp_server, 'call_tool')}")
    print()
except Exception as e:
    print(f"   [ERROR] {e}\n")

# Test 4: Test function calls
print("4. Testing function calls...")
import asyncio
import os

# Load token from environment
if 'TELEGRAM_BOT_TOKEN' not in os.environ:
    print("[ERROR] TELEGRAM_BOT_TOKEN environment variable is required")
    sys.exit(1)

async def test_functions():
    try:
        # Test get_updates directly
        print("   Testing get_updates directly...")
        result = await mcp_server.get_updates({'limit': 2})
        print(f"   [OK] get_updates returned: {len(result)} items\n")

        # Test through call_tool
        print("   Testing get_updates through call_tool...")
        result = await mcp_server.call_tool('get_telegram_updates', {'limit': 2})
        print(f"   [OK] call_tool returned: {len(result)} items\n")

    except Exception as e:
        print(f"   [ERROR] {e}\n")
        traceback.print_exc()

asyncio.run(test_functions())

print("=== Diagnostic Complete ===")
