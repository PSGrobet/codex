from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

# Auto-detect timezone from user's system
local_tz = datetime.now().astimezone().tzinfo

@dataclass
class Note:
    """
    A freeform note attached to any entity in the archive

    target_type + target_id together form a reference to the parent entity.
    e.g. target_type="book", target_id="<some-book-uuid>"
    """
    text: str
    target_id: str
    target_type: str # "book" or "author" for now, extensible later
    tags: list[str] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.now().astimezone().isoformat()
    )
    id: str = field(default_factory=lambda: str(uuid4()))