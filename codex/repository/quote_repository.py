from codex.models import Quote
from codex.storage import json_store

ENTITY = "quotes"

class QuoteRepository:
    """Manages persistance and retrieval of Quote records"""

    def _load(self) -> list[Quote]:
        return json_store.load(ENTITY, Quote)
    
    def _save(self, quotes: list[Quote]) -> None:
        json_store.save(ENTITY, quotes)
    
    def add(self, quote: Quote) -> Quote:
        """It takes a fully constructed object, not individual fields,
        it's the CLI's job to construct the object and pass to repo"""
        quotes = self._load()
        quotes.append(quote)
        self._save(quotes)
        return quote

    def get_by_id(self, id: str) -> Quote | None:
        return next((q for q in self._load() if q.id == id), None)
    
    def get_by_book(self, book_id: str) -> list[Quote]:
        """Return all quotes attached to a given book"""
        return [q for q in self._load() if q.book_id == book_id]

    def get_by_author(self, author_id: str) -> list[Quote]:
        """Return all quotes referencing the given author"""
        return [q for q in self._load() if q.author_id == author_id]
    
    def get_by_tag(self, tag: str) -> list[Quote]:
        tag_lower = tag.lower()
        return [q for q in self._load() if tag_lower in [t.lower() for t in q.tags]]
    
    def search(self, query: str) -> list[Quote]:
        """Fulll text search across Quote contents"""
        query_lower = query.lower()
        return [q for q in self._load() if query_lower in q.text.lower()]

    def list_all(self) -> list[Quote]:
        return self._load()

    def update(self, updated_quote: Quote) -> Quote | None:
        quotes = self._load()
        for i, q in enumerate(quotes):
            if q.id == updated_quote.id:
                quotes[i] = updated_quote
                self._save(quotes)
                return updated_quote
        return None

    def delete(self, id: str) -> bool:
        quotes = self._load()
        filtered = [q for q in quotes if q.id != id]
        if len(filtered) == len(quotes):
            return False
        self._save(filtered)
        return True
