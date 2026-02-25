from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Book:
    """Represents a book in the archive."""
    title: str
    author_id: str # reference to Author.id, not the Author object itself
    year: int | None = None
    genre: str = ""
    series: str = ""
    series_order: int | None = None

    # Generated automatically - caller never passes this in
    id: str = field(default_factory=lambda: str(uuid4()))