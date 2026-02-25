from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

local_tz = datetime.now().astimezone().tzinfo

@dataclass
class Quote:
    """A quote referencing a book, page or location, author"""

    text: str
    target_book_id: str
    tags: list[str] = field(default_factory=list)
    page: str | None = None
    loc: str | None = None

    created_at: str = field(
        default_factory=lambda: datetime.now().astimezone().isoformat()
    )
    id: str = field(default_factory=lambda: str(uuid4()))