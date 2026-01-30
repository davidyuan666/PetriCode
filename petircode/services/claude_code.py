"""
System command execution service for computer operations
"""
import logging
import asyncio
import os
from ..config import config

logger = logging.getLogger(__name__)


async def execute_claude_code(operation: str, timeout: int = None) -> dict:
    """
    Execute system command via PowerShell in specified working directory

    Args:
        operation: The command to execute
        timeout: Timeout in seconds (default: from config)

    Returns:
        dict with keys:
            - stdout: Standard output
            - stderr: Standard error
            - return_code: Process return code
            - success: Boolean indicating success

    Raises:
        Exception: If execution fails
    """
    if timeout is None:
        timeout = config.CLAUDE_TIMEOUT

    # Parse operation to system command
    command = _parse_operation_to_command(operation)

    # Build PowerShell command to change directory and run command
    powershell_cmd = (
        f'powershell.exe -NoProfile -Command "'
        f'cd \'{config.CLAUDE_WORK_DIR}\'; '
        f'{command}"'
    )

    logger.info(f"Executing command: {command}")
    logger.info(f"Working directory: {config.CLAUDE_WORK_DIR}")

    try:
        # Create subprocess to run PowerShell command
        process = await asyncio.create_subprocess_shell(
            powershell_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise Exception(f"Operation timed out after {timeout} seconds")

        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace')
        stderr_text = stderr.decode('utf-8', errors='replace')

        logger.info(f"Command completed with return code: {process.returncode}")

        return {
            'stdout': stdout_text,
            'stderr': stderr_text,
            'return_code': process.returncode,
            'success': process.returncode == 0
        }

    except Exception as e:
        logger.error(f"Error executing command: {e}", exc_info=True)
        raise


def _parse_operation_to_command(operation: str) -> str:
    """
    Parse natural language operation to system command

    Args:
        operation: Natural language description or direct command

    Returns:
        System command string
    """
    operation_lower = operation.lower().strip()

    # List files
    if 'list' in operation_lower and 'file' in operation_lower:
        return 'Get-ChildItem | Format-Table Name, Length, LastWriteTime'

    # Show current directory
    if 'current' in operation_lower and ('directory' in operation_lower or 'dir' in operation_lower):
        return 'Get-Location'

    # Create file
    if 'create' in operation_lower and 'file' in operation_lower:
        # Extract filename
        words = operation.split()
        filename = None
        for i, word in enumerate(words):
            if word.lower() in ['file', 'named', 'called', 'name']:
                if i + 1 < len(words):
                    filename = words[i + 1].strip('.,;:')
                    break

        if filename:
            # Check if content is specified
            if 'content' in operation_lower or 'with' in operation_lower:
                # Extract content after "content" or "with"
                content_start = max(
                    operation.lower().find('content'),
                    operation.lower().find('with')
                )
                if content_start > 0:
                    content = operation[content_start:].split(None, 1)
                    if len(content) > 1:
                        content_text = content[1].strip('"\'')
                        return f'Set-Content -Path "{filename}" -Value "{content_text}"'

            # Create empty file
            return f'New-Item -Path "{filename}" -ItemType File -Force'

    # Default: treat as direct PowerShell command
    return operation
