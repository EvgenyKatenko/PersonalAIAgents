from dataclasses import dataclass
from typing import Optional

@dataclass
class DialogInfo:
    """Information about a Telegram dialog."""
    name: str
    entity_id: int
    entity_type: str
    participant_count: Optional[int] = None 