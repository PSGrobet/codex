import typer
from codex.models import Author
from codex.repository import AuthorRepository

app = typer.Typer()
repo = AuthorRepository()

@app.command("add")
def add_author(
    name: str = typer.Option(..., prompt=True), ## default value is typer.Option, which prompts user for input if it is not set.
    nationality: str = typer.Option(""),
    birth_year: int = typer.Option(None)
):
    """Add a new author to the archive."""
    author = Author(name=name, nationality=nationality, birth_year= birth_year)
    repo.add(author)
    typer.echo(f"added author: {author.name} (id : {author.id})")

@app.command("list")
def list_authors():
    """List all authors in the archive"""
    authors = repo.list_all()
    if not authors:
        typer.echo("No authors found")
        raise typer.Exit()
    for a in authors:
        typer.echo(f"{a.name} ({a.nationality}, {a.birth_year}) - id: {a.id}")

@app.command("search-name")
def search_name(name: str = typer.Argument(...)):
    """Search authors by name"""
    results = repo.get_by_name(name)
    if not results:
        typer.echo(f"No authors found matching name '{name}'.")
        raise typer.Exit()
    for a in results:
        typer.echo(f"{a.name} ({a.nationality}, {a.birth_year}) - id: {a.id}")

@app.command("search-nationality")
def search_nationality(nationality: str = typer.Argument(...)):
    results = [a for a in repo.list_all() if nationality.lower() in a.nationality.lower()]
    if not results:
        typer.echo(f"No authors found matching nationality '{nationality}'.")
    for a in results:
        typer.echo(f"{a.name} ({a.nationality}, {a.birth_year})")

@app.command("delete")
def delete_author(id: str = typer.Argument(...)):
    """Delete an author by id"""
    deleted = repo.delete(id)
    if deleted:
        typer.echo(f"Author {id} deleted.")
    else:
        typer.echo(f"No author found with id {id}.")

@app.command("update")
def update_author(
    id: str = typer.Argument(...),
    name: str = typer.Option(None),
    nationality: str = typer.Option(None),
    birth_year: int = typer.Option(None),
):
    """Update an existing author's fields. Only provided fields will be updated"""
    author = repo.get_by_id(id)
    if not author:
        typer.echo(f"No author found with id {id}")
        raise typer.Exit()
    
    # Only update fields that were actually provided
    if name is not None:
        author.name = name
    if nationality is not None:
        author.nationality = nationality
    if birth_year is not None:
        author.birth_year = birth_year
    
    repo.update(author)
    typer.echo(f"Updated author: {author.name} (id: {author.id})")
