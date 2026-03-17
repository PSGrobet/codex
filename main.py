import typer
from codex.cli import authors, books, notes, quotes

app = typer.Typer()
app.add_typer(authors.app, name="authors")
app.add_typer(books.app, name="books")
app.add_typer(notes.app, name="notes")
app.add_typer(quotes.app, name="quotes")

if __name__ == "__main__":
    app()
