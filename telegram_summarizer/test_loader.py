#!/usr/bin/env python3
"""
Telegram Dialog Lister

Lists all dialogs (chats) from a Telegram account with their types.
Requires environment variables: TELEGRAM_API_ID and TELEGRAM_API_HASH
"""

import asyncio
import logging
import os
import sys
from typing import Optional, Tuple

from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel
from telethon.errors import SessionPasswordNeededError, FloodWaitError

from telegram_summarizer.utils.dialog_info import DialogInfo
from telegram_summarizer.utils.telegram_dialog_lister import TelegramDialogLister

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_dialogs(dialogs: list[DialogInfo]) -> None:
    """
    Print dialogs in a formatted table.
    
    Args:
        dialogs: List of DialogInfo objects to print
    """
    if not dialogs:
        print("No dialogs found.")
        return
    
    # Print header
    print("\n" + "=" * 80)
    print(f"{'Type':<25} | {'Name':<30} | {'ID':<12} | {'Members':<8}")
    print("=" * 80)
    
    # Print dialogs
    for dialog in dialogs:
        members = str(dialog.participant_count) if dialog.participant_count else "N/A"
        # Truncate long names
        name = dialog.name[:30] + "..." if len(dialog.name) > 30 else dialog.name
        
        print(f"{dialog.entity_type:<25} | {name:<30} | {dialog.entity_id:<12} | {members:<8}")
    
    print("=" * 80)
    print(f"\nTotal dialogs: {len(dialogs)}")


async def main():
    """Main function to run the dialog lister."""
    try:
        # Use context manager for automatic connection/disconnection
        async with TelegramDialogLister() as lister:
            dialogs = await lister.list_dialogs()
            print_dialogs(dialogs)
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create .env file example if it doesn't exist
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w') as f:
            f.write("# Telegram API credentials\n")
            f.write("TELEGRAM_API_ID=your_api_id_here\n")
            f.write("TELEGRAM_API_HASH=your_api_hash_here\n")
        logger.info("Created .env.example file. Copy it to .env and fill in your credentials.")
    
    asyncio.run(main())