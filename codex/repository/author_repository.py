from codex.models import Author
from codex.storage import json_store

ENTITY = "authors"

class AuthorRepository:
    """Manages persistence and retrieval of Author records"""

    def _load(self) -> list[Author]:
        return json_store.load(ENTITY, Author)
    
    def _save(self, authors: list[Author]) -> None:
        json_store.save(ENTITY, authors)
    
    def add(self, author: Author) -> Author:
        authors = self._load()
        authors.append(author)
        self._save(authors)
        return author 
        ## Why does this function return the same as given in parameter?
        ## Could it return a bool if successful or something else?

    def get_by_id(self, id: str) -> Author | None:
        return next((a for a in self._load() if a.id == id), None)

    def get_by_name(self, name: str) -> list[Author]:
        name_lower = name.lower()
        return [a for a in self._load() if name_lower in a.name.lower()]
    
    def list_all(self) -> list[Author]:
        return self._load()
    
    def delete(self, id: str) -> bool:
        """Returns True if something was deleted, False if id wasn't found"""
        authors = self._load()
        filtered = [a for a in authors if a.id != id]
        if len(filtered) == len(authors):
            return False
        self._save(filtered)
        return True