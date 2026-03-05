import typer
from codex.models import Book
from codex.repository import BookRepository, AuthorRepository

app = typer.Typer()
book_repo = BookRepository()
author_repo = AuthorRepository()

@app.command("add")
def add_book(
    title: str = typer.Option(..., prompt=True),
    author_id: str = typer.Option(..., prompt=True),
    year: int = typer.Option(None),
    genre: str = typer.Option(None),
    series: str = typer.Option(None),
    series_order: int = typer.Option(None)
):
    """Add a new book to the archive.
    Requires having author_id first"""
    book = Book(title=title, author_id=author_id, year=year, genre=genre, series=series, series_order=series_order)
    book_repo.add(book)
    typer.echo(f"Added book {book.title} by {author_repo.get_by_id(author_id).name}")


@app.command("list")
def list_books():
    books = book_repo.list_all()
    if not books:
        typer.echo("No books found.")
        raise typer.Exit()
    for b in books:
        typer.echo(f"- {author_repo.get_by_id(b.author_id).name}, {b.title}, {b.year}")
        typer.echo(f"\tid: {b.id}")
        if b.series is not None:
            typer.echo(f"\tSeries: {b.series}, #{b.series_order}")
        if b.genre is not None:
            typer.echo(f"\tGenre(s): {b.genre}")


@app.command("search-title")
def search_title(title: str = typer.Argument(...)):
    """Search books by title"""
    results = book_repo.get_by_title(title)
    if not results:
        typer.echo(f"No books found matching '{title}' in title")
        raise typer.Exit()
    for b in results:
        typer.echo(f"- {author_repo.get_by_id(b.author_id).name}, {b.title}, {b.year}")
        typer.echo(f"\tid: {b.id}")
        if b.series is not None:
            typer.echo(f"\tSeries: {b.series}, #{b.series_order}")
        if b.genre is not None:
            typer.echo(f"\tGenre(s): {b.genre}")


@app.command("search-author")
def search_author(
    id: str = typer.Option(None),
    name: str = typer.Option(None)
):
    """search books by author"""
    if id is None and name is None:
        typer.echo("Need to specify either id or name.")
        raise typer.Exit()
    if id is not None:
        results = book_repo.get_by_author(id)
    else:
        results = [b for b in book_repo.list_all() if name.lower() in author_repo.get_by_id(b.author_id).name.lower()]
    if not results:
        typer.echo(f"No matching books for author: {id}.")
    for b in results:
        typer.echo(f"- {author_repo.get_by_id(b.author_id).name}, {b.title}, {b.year}")
        typer.echo(f"\tid: {b.id}")
        if b.series is not None:
            typer.echo(f"\tSeries: {b.series}, #{b.series_order}")
        if b.genre is not None:
            typer.echo(f"\tGenre(s): {b.genre}")


@app.command("search-genre")
def search_genre(genre: str = typer.Argument(...)):
    """Search books by genre"""
    results = []
    for b in book_repo.list_all():
        if b.genre:
            if genre.lower() in b.genre.lower():
                results.append(b)

    if not results:
        typer.echo(f"No matches found for genre '{genre}'.")
        raise typer.Exit()
    for b in results:
        typer.echo(f"- {author_repo.get_by_id(b.author_id).name}, {b.title}, {b.year}")
        typer.echo(f"\tid: {b.id}")
        if b.series is not None:
            typer.echo(f"\tSeries: {b.series}, #{b.series_order}")
        if b.genre is not None:
            typer.echo(f"\tGenre(s): {b.genre}")


@app.command("search-series")
def search_series(series: str = typer.Argument(...)):
    results = book_repo.get_by_series(series)
    if not results:
        typer.echo(f"No matches found for series '{series}'.")
        raise typer.Exit()
    for b in results:
        typer.echo(f"- {author_repo.get_by_id(b.author_id).name}, {b.title}, {b.year}")
        typer.echo(f"\tid: {b.id}")
        if b.series is not None:
            typer.echo(f"\tSeries: {b.series}, #{b.series_order}")
        if b.genre is not None:
            typer.echo(f"\tGenre(s): {b.genre}")


@app.command("delete")
def delete_book(id: str = typer.Argument(...)):
    """Delete a book by id"""
    deleted = book_repo.delete(id)
    if deleted:
        typer.echo(f"Book {id} deleted")
    else:
        typer.echo(f"No book found with id {id}")


@app.command("update")
def update_book(
    id: str = typer.Argument(...),
    title: str = typer.Option(None),
    author_id: str = typer.Option(None),
    year: int = typer.Option(None),
    genre: str = typer.Option(None),
    series: str = typer.Option(None),
    series_order: str = typer.Option(None)
):
    book = book_repo.get_by_id(id)
    if not book:
        typer.echo(f"No book found with id {id}")
        raise typer.Exit()

    if title is not None:
        book.title = title
    if author_id is not None:
        book.author_id = author_id
    if year is not None:
        book.year = year
    if genre is not None:
        book.genre = genre
    if series is not None:
        book.series = series
    if series_order is not None:
        book.series_order = series_order

    book_repo.update(book)
    typer.echo(f"Updated book: {book.title} (id: {book.id})")