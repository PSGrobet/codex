from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Author:
    """Represents a literary author in the archive."""
    name: str
    nationality: str = ""
    birth_year: int | None = None

    # Generated automatically - caller never passes this in
    id: str =  field(default_factory=lambda: str(uuid4()))