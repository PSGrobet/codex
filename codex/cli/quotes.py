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
    
    author = author_repo.get_by_id(q.author_id) if q.author_id else None
    author_string = author.name if author else "Unknown author"

    book = book_repo.get_by_id(q.book_id) if q.book_id else None
    book_string = f", {book.title}" if book else ""
    attr_string = f"{author_string}{book_string}{location_string}"
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
def list_quotes():
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
        typer.echo(f"No quotes found by id {author_id}.")
        raise typer.Exit()
    for i, q in enumerate(results, 1):
        print(f"---- [{i}]")
        _format_quote(q)

@app.command("by-book")
def quotes_by_book(book_id: str = typer.Argument(...)):
    """Get all quotes attached to a book"""
    results = quote_repo.get_by_book(book_id)
    if not results:
        typer.echo(f"Couldn't find any quotes for book id {book_id}")
        raise typer.Exit()
    for i, q in enumerate(results, 1):
        print(f"--- [{i}]")
        _format_quote(q)

@app.command("by-tag")
def quotes_by_tag(tag: str = typer.Argument(...)):
    """Get all quotes related to speecified tag."""
    results = quote_repo.get_by_tag(tag)
    if not results:
        typer.echo(f"No quotes found with tag '{tag}'.")
        raise typer.Exit()
    for i, q in enumerate(results, 1):
        print(f"---[{i}]")
        _format_quote(q)

@app.command("search")
def search_quotes(query: str = typer.Argument(...)):
    """Full text searc across quotes content."""
    results = quote_repo.search(query)
    if not results: 
        typer.echo(f"No quotes found matching query '{query}'.")
        raise typer.Exit()
    for i, q in enumerate(results, 1):
        print(f"---[{i}]")
        _format_quote(q)

@app.command("delete")
def delete_quote(id: str = typer.Argument(...)):
    """Delete a note by id."""
    deleted = quote_repo.delete(id)
    if deleted:
        typer.echo(f"Quote {id} deleted.")
    else:
        typer.echo(f"No quote found with id {id}.")

@app.command("update")
def update_quote(
        id: str = typer.Argument(...),
        text: str = typer.Option(None),
        tags: str = typer.Option(None, help="Comma separated list of tags, replaces existing tags")
):
    """Update a quote's text or tag list."""
    quote = quote_repo.get_by_id(id)
    if not quote:
        typer.echo(f"No quotes found with id {id}.")
        raise typer.Exit()

    if text is not None:
        quote.text = text
    if tags is not None:
        quote.tags = [t.strip() for t in tags.split(",")]

    quote_repo.update(quote)
    typer.echo(f"Quote updated (id: {id}).")
