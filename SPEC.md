# Codex — Project Spec & Progress Log

## Concept
A CLI-based literary archive engine. Lets you catalog books and authors, attach notes and quotes, tag and cross-reference entries, search content, and export structured data. Built like a small backend service, emphasizing professional structure, OOP, separation of concerns, and clean error handling.

---

## Tech Stack
- Python 3.10+
- `uv` for project management
- `typer` for CLI
- JSON files for persistence (one per entity type, stored in `data/`)
- `ruff` for linting

---

## Project Structure

```
codex/
├── main.py                        # Entry point, wires CLI together
├── pyproject.toml
├── uv.lock
├── README.md
├── SPEC.md
├── data/                          # Auto-created at runtime
│   ├── authors.json
│   ├── books.json
│   ├── notes.json
│   └── quotes.json
└── codex/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py            # Re-exports: Author, Book, Note, Quote
    │   ├── author.py
    │   ├── book.py
    │   ├── note.py
    │   └── quote.py
    ├── storage/
    │   ├── __init__.py
    │   └── json_store.py          # save() and load() functions
    ├── repository/
    │   ├── __init__.py            # Re-exports all four repositories
    │   ├── author_repository.py
    │   ├── book_repository.py
    │   ├── note_repository.py
    │   └── quote_repository.py
    └── cli/
        ├── __init__.py
        ├── authors.py             # DONE
        ├── books.py               # DONE
        ├── notes.py               # DONE
        └── quotes.py              # TODO
```

---

## Architecture

### Layers (bottom to top)
1. **Models** — pure dataclasses, no logic, no dependencies
2. **Storage** — `json_store.py`, handles file I/O and serialization
3. **Repository** — one class per entity, abstracts storage, holds query logic
4. **CLI** — Typer commands, constructs objects, calls repository methods

Each layer only knows about the layer directly below it. Models have no dependencies at all.

### Key patterns
- `dataclasses.asdict()` for serialization, `Model(**dict)` for deserialization
- Repository pattern: CLI never touches storage directly
- `field(default_factory=...)` for mutable defaults and dynamic values (uuid, timestamps)
- `__post_init__` for validation (used in Quote)
- `TypeVar` + `Callable` for generic `load()` function
- Explicit re-exports in `__init__.py` files (ruff `PEP 484` convention)

---

## Models

### `Author`
```python
@dataclass
class Author:
    name: str
    nationality: str | None = None
    birth_year: int | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
```

### `Book`
```python
@dataclass
class Book:
    title: str
    author_id: str              # foreign key → Author.id
    year: int | None = None
    genre: str | None = None
    series: str | None = None
    series_order: int | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
```

### `Note`
```python
@dataclass
class Note:
    text: str
    target_id: str              # foreign key → Author.id or Book.id
    target_type: str            # "book" or "author"
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())
    id: str = field(default_factory=lambda: str(uuid4()))
```

### `Quote`
```python
@dataclass
class Quote:
    text: str
    target_book_id: str | None = None
    author_id: str | None = None
    tags: list[str] = field(default_factory=list)
    page: str | None = None
    loc: str | None = None      # ebook location reference
    created_at: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if not self.target_book_id and not self.author_id:
            raise ValueError("A quote must reference at least a book or an author")
```

---

## Storage — `json_store.py`

```python
DATA_DIR = Path("data")

def save(entity_type: str, records: list) -> None:
    # serializes list of dataclasses to data/{entity_type}.json

def load(entity_type: str, factory: Callable[..., T]) -> list[T]:
    # deserializes JSON back into dataclass instances using factory(**item)
```

`_ensure_file()` creates the data dir and empty JSON file if they don't exist.

---

## Repositories

All repositories follow the same pattern:

| Method | Returns | Notes |
|---|---|---|
| `add(entity)` | entity | appends and saves |
| `get_by_id(id)` | entity \| None | |
| `list_all()` | list | |
| `update(entity)` | entity \| None | match by id, replace in list |
| `delete(id)` | bool | True if something was deleted |

### `AuthorRepository` — additional methods
- `get_by_name(name)` — case-insensitive substring match

### `BookRepository` — additional methods
- `get_by_title(title)` — case-insensitive substring match
- `get_by_author(author_id)` — exact match on foreign key
- `get_by_series(series)` — case-insensitive substring match

### `NoteRepository` — additional methods
- `get_by_target(target_id)` — all notes for a given entity
- `get_by_tag(tag)` — exact tag match (case-insensitive)
- `search(query)` — full text search across note text AND tags (single file load)

### `QuoteRepository` — additional methods
- `get_by_book(book_id)` — match on `target_book_id`
- `get_by_author(author_id)` — match on `author_id`
- `get_by_tag(tag)` — exact tag match (case-insensitive)
- `search(query)` — full text search across quote text

---

## CLI

### Conventions
- `typer.Option(..., prompt=True)` only for required fields on `add` commands
- Optional fields passed as flags: `--year 1944`, never prompted
- `update` commands take an id as positional `Argument`, all fields as optional `Option`
- Tags passed as comma-separated string: `--tags "exile,memory"`, split in the command
- `TargetType` enum (`"book"` | `"author"`) used in notes CLI for type safety
- `_format_*` helper functions used to avoid repeating output formatting
- Target existence validated in `notes add` before saving

### `main.py`
```python
app = typer.Typer()
app.add_typer(authors.app, name="authors")
app.add_typer(books.app, name="books")
app.add_typer(notes.app, name="notes")
# TODO: app.add_typer(quotes.app, name="quotes")
```

### Commands per subapp

**authors:** `add`, `list`, `search`, `update`, `delete`
**books:** `add`, `list`, `search-title`, `search-author`, `search-genre`, `search-series`, `update`, `delete`
**notes:** `add`, `list`, `by-target`, `by-tag`, `search`, `update`, `delete`
**quotes:** `add`, `list`, `by-book`, `by-author`, `by-tag`, `search`, `update`, `delete` ← TODO

---

## What's Left (TODO)

### Immediate
- [ ] `codex/cli/quotes.py` — same pattern as notes, but with `page`/`loc` fields and no `TargetType` enum (quotes reference book or author directly via separate fields)
- [ ] Wire `quotes` into `main.py`

### Nice to have / stretch goals
- [ ] Export command — dump archive to a single structured JSON or Markdown file
- [ ] `cross-ref` command — show everything attached to a book or author (notes + quotes together)
- [ ] Refactor repeated output formatting into a shared `codex/cli/formatters.py`
- [ ] Abstract shared repository logic into a generic `BaseRepository` class
- [ ] Auto-detect or configure timezone (hint: `datetime.now().astimezone().tzinfo` already used)
- [ ] `ruff format` pass over all files

---

## Running the Project

```bash
# Add an author
uv run python main.py authors add --name "Borges" --nationality "Argentine" --birth-year 1899

# Add a book
uv run python main.py books add --title "Ficciones" --author-id <id> --year 1944

# Add a note
uv run python main.py notes add --text "Recurring labyrinth motif" --target-id <id> --target-type book --tags "labyrinth,metaphor"

# Search notes
uv run python main.py notes search "labyrinth"
```
