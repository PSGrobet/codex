import typer
from codex.cli import authors, books

app = typer.Typer()
app.add_typer(authors.app, name="authors")
app.add_typer(books.app, name="books")

if __name__ == "__main__":
    app()