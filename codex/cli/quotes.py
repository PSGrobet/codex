import typer
from codex.models import Quote
from codex.repository import QuoteRepository, BookRepository, AuthorRepository

app = typer.Typer()
quote_repo = QuoteRepository()
book_repo = BookRepository()
author_repo = AuthorRepository()


def _format_quote(q: Quote) -> None:
    """Helper to print quote consistently across commands"""
    if q.loc:
        location_string = f", (digital) loc: {q.loc}"
    elif q.page:
        location_string = f", p: {q.page}"
    else:
        location_string = ""
    
    book_string = f", {book_repo.get_by_id(q.book_id).title}" if q.book_id else ""
    attr_string = f"{author_repo.get_by_id(q.author_id).name}{book_string}{location_string}"
    typer.echo(f"{q.text}")
    typer.echo(f"\t- {attr_string}\n")
    typer.echo(f"Quote id: {q.id}")
    typer.echo(f"Author id: {q.author_id}")
    typer.echo(f"Book id: {q.book_id}\n" if q.book_id else "")


@app.command("add")
def add_quote(
        text: str = typer.Option(..., prompt=True),
        target_author_id: str = typer.Option(..., prompt=True),
        target_book_id: str = typer.Option(None),
        page: str = typer.Option(None),
        loc: str = typer.Option(None),
        tags: str = typer.Option(None, help="Comma-separated list of tags, e.g. 'wisdom,magick'"),
):
    """Add a quote to the archive"""
    # Verify the target exists
    if target_book_id and not book_repo.get_by_id(target_book_id):
        typer.echo(f"No book found with id {target_book_id}")
        raise typer.Exit()
    if target_author_id and not author_repo.get_by_id(target_author_id):
        typer.echo(f"No author found with id {target_author_id}")
        raise typer.Exit()
    
    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    quote = Quote(text=text, author_id=target_author_id, book_id=target_book_id, tags=tag_list, page=page, loc=loc)

    quote_repo.add(quote)
    typer.echo(f"Added new quote (id: {quote.id})")


@app.command("list")
def list_quotees():
    """List all quotes in the archive"""
    quotes = quote_repo.list_all()
    if not quotes:
        typer.echo("No quotes found")
    for i, q in enumerate(quotes, 1):
        print(f"----[{i}]")
        _format_quote(q)


@app.command("by-author")
def quotes_by_author(author_id: str = typer.Argument(...)):
    """Get all quotes by specified author"""
    results = quote_repo.get_by_author(author_id)
    if not results:
        typer.echo(f"No quotes found by {author_repo.get_by_id(author_id).name}")
        raise typer.Exit()
    for i, q in enumerate(results, 1):
        print(f"---- [{i}]")
        _format_quote(q)
