import os
import logging
from typing import Optional, Tuple
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from .dialog_info import DialogInfo

logger = logging.getLogger(__name__)

class TelegramDialogLister:
    """Handles listing of Telegram dialogs with proper error handling."""
    def __init__(self, session_name: str = 'telegram_session'):
        self.session_name = session_name
        self.api_id = self._get_env_var('TELEGRAM_API_ID', is_int=True)
        self.api_hash = self._get_env_var('TELEGRAM_API_HASH')
        self.client: Optional[TelegramClient] = None

    @staticmethod
    def _get_env_var(var_name: str, is_int: bool = False) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(
                f"Environment variable {var_name} is not set. "
                f"Please set it before running this script."
            )
        if is_int:
            try:
                return str(int(value))
            except ValueError:
                raise ValueError(f"{var_name} must be a valid integer")
        return value

    @staticmethod
    def _get_entity_type(entity) -> Tuple[str, Optional[int]]:
        if isinstance(entity, User):
            return 'Private Chat', None
        elif isinstance(entity, Chat):
            return 'Basic Group', getattr(entity, 'participants_count', None)
        elif isinstance(entity, Channel):
            participant_count = getattr(entity, 'participants_count', None)
            if entity.broadcast:
                return 'Channel (broadcast)', participant_count
            else:
                return 'Supergroup', participant_count
        else:
            return 'Unknown', None

    async def connect(self) -> None:
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.start()
            logger.info("Successfully connected to Telegram")
        except SessionPasswordNeededError:
            logger.error("Two-factor authentication is enabled. Please provide password.")
            password = input("Enter your 2FA password: ")
            await self.client.start(password=password)
        except FloodWaitError as e:
            logger.error(f"Rate limited. Please wait {e.seconds} seconds.")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            raise

    async def list_dialogs(self) -> list[DialogInfo]:
        if not self.client or not self.client.is_connected():
            raise RuntimeError("Client is not connected. Call connect() first.")
        dialogs = []
        try:
            logger.info("Fetching dialogs...")
            async for dialog in self.client.iter_dialogs():
                entity = dialog.entity
                entity_type, participant_count = self._get_entity_type(entity)
                dialog_info = DialogInfo(
                    name=dialog.name or "Unnamed",
                    entity_id=entity.id,
                    entity_type=entity_type,
                    participant_count=participant_count
                )
                dialogs.append(dialog_info)
            logger.info(f"Found {len(dialogs)} dialogs")
            return dialogs
        except FloodWaitError as e:
            logger.error(f"Rate limited while fetching dialogs. Wait {e.seconds} seconds.")
            raise
        except Exception as e:
            logger.error(f"Error while fetching dialogs: {e}")
            raise

    async def disconnect(self) -> None:
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect() 