from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

local_tz = datetime.now().astimezone().tzinfo

@dataclass
class Quote:
    """A quote referencing a book, page or location, author"""

    text: str
    book_id: str | None = None
    author_id: str | None = None
    tags: list[str] = field(default_factory=list)
    page: str | None = None
    loc: str | None = None

    created_at: str = field(
        default_factory=lambda: datetime.now().astimezone().isoformat()
    )
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if not self.book_id and not self.author_id:
            raise ValueError("A quote must reference at least a book or an author")