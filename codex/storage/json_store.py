import json
from pathlib import Path
from dataclasses import asdict
from typing import TypeVar, Callable

# TypeVar lets us write generic functions that preserve the specific type being passed in - so load() can return list[Author] or list[Book], etc.
T = TypeVar("T")

# Default data directory, relative to wherever the project is run from
DATA_DIR = Path("data")

def _ensure_file(path: Path) -> None:
    """Create the data directory an file if they don't already exist"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]")
    
def save(entity_type: str, records: list) -> None:
    """
    Write a list of dataclass instances to a JSON file.
    entity_type is just e filename stem, e.g. "authors" -> data/authors.json
    """
    path = DATA_DIR / f"{entity_type}.json" # this is just how you join filepaths from with Path object
    _ensure_file(path)
    with open(path, "w") as f:
        json.dump([asdict(r) for r in records], f, indent=2)

def load(entity_type: str, factory: Callable[..., T]) -> list[T]:
    """
    Read a JSON file and reconstruct a list of dataclass instances.
    factory is the dataclass constructor, e.g. Author, Book, etc
    """
    path = DATA_DIR / f"{entity_type}.json"
    _ensure_file(path)
    with open(path) as f:
        raw = json.load(f)
    return [factory(**item) for item in raw]


