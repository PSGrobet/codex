from codex.models import Book
from codex.storage import json_store

ENTITY = "books"

class BookRepository:
    """Manages persistence and retrieval of Book records"""
    def _load(self) -> list[Book]:
        return json_store.load(ENTITY, Book)
    
    def _save(self, books: list[Book]) -> None:
        json_store.save(ENTITY, books)
    
    def add(self, book: Book) -> Book:
        books = self._load()
        books.append(book)
        self._save(books)
        return book

    def get_by_id(self, id: str) -> Book | None:
        return next((b for b in self._load() if b.id == id), None)
    
    def get_by_title(self, title: str) -> list[Book]:
        """Find all books that have the string in their title, even if there are many"""
        title_lower = title.lower()
        return [b for b in self._load() if title_lower in b.title.lower()]
    
    def get_by_author(self, author_id: str) -> list[Book]:
        """Return all book referencint the given author_id"""
        return [b for b in self._load() if b.author_id == author_id]
    
    def get_by_series(self, series: str) -> None:
        series_lower = series.lower()
        return [b for b in self._load() if series_lower in b.series.lower()]

    def list_all(self) -> list[Book]:
        return self._load()
    
    def update(self, updated_book: Book) -> Book | None:
        books = self._load()
        for i, b in enumerate(books):
            if b.id == updated_book.id:
                books[i] = updated_book
                self._save(books)
                return updated_book
        return None

    def delete(self, id: str) -> bool:
        """Deleta a book by id, true if succesful, false if it diddn't find the book"""
        books = self._load()
        filtered = [b for b in books if b.id != id]
        if len(filtered) == len(books):
            return False
        self._save(filtered)
        return True
    
    


