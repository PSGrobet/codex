from codex.models import Note
from codex.storage import json_store

ENTITY ="notes"

class NoteRepository:
    """Manages persistence and retrieval of Note records"""

    def _load(self) -> list[Note]:
        return json_store.load(ENTITY, Note)

    def _save(self, notes: list[Note]) -> None:
        json_store.save(ENTITY, notes)
    
    def add(self, note: Note) -> Note:
        """It takes a fully constructed object, not individual fields,
        it's the CLI's job to construct the object and pass to repo"""
        notes = self._load()
        notes.append(note)
        self._save(notes)
        return note
    
    def get_by_id(self, id: str) -> Note | None:
        return next((n for n in self._load() if n.id == id), None)

    def get_by_target(self, target_id: str) -> list[Note]:
        """Return all notes attached to a given entity"""
        return [n for n in self._load() if n.target_id == target_id]

    def get_by_tag(self, tag: str) -> list[Note]:
        """Return all notes that include the given tag."""
        tag_lower = tag.lower()
        return [n for n in self._load() if tag_lower in [t.lower() for t in n.tags]]

    def search(self, query: str) -> list[Note]:
        """Full text search across note contents"""
        query_lower = query.lower()
        return [n for n in self._load() if query_lower in n.text.lower()]
    
    def list_all(self) -> list[Note]:
        return self._load()
    
    def update(self, updated_note: Note) -> Note | None:
        notes = self._load()
        for i, n in enumerate(notes):
            if n.id == updated_note.id:
                notes[i] = updated_note
                self._save(notes)
                return updated_note
        return None

    def delete(self, id: str) -> bool:
        notes = self._load()
        filtered = [n for n in notes if n.id != id]
        if len(filtered) == len(notes):
            return False
        self._save(filtered)
        return True