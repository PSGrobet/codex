import typer
from enum import Enum
from codex.models import Note
from codex.repository import NoteRepository, BookRepository, AuthorRepository

app = typer.Typer()
note_repo = NoteRepository()
book_repo = BookRepository()
author_repo = AuthorRepository()

class TargetType(str, Enum):
    book = "book"
    author = "author"

def _format_note(n: Note) -> None:
    """helper to print a note consistently accross commands"""
    #typer.echo(f"- {n.text[:60]}{'...' if len(n.text) > 60 else ''}")
    typer.echo(f"- {n.text}\n")
    if n.target_type == "book":
        target = book_repo.get_by_id(n.target_id)
        typer.echo(f"target: [{n.target_type}] {target.title} (id: {n.target_id})")
    elif n.target_type == "author":
        target = author_repo.get_by_id(n.target_id)
        typer.echo(f"target: [{n.target_type}] {target.name} (id: {n.target_id})")
    typer.echo(f"id: {n.id}")
    if n.tags:
        typer.echo(f"tags: {', '.join(n.tags)}")
    typer.echo(f"created: {n.created_at}")
    typer.echo("")

@app.command("add")
def add_note(
        text: str = typer.Option(..., prompt=True),
        target_id: str = typer.Option(..., prompt=True),
        target_type: TargetType = typer.Option(..., prompt=True),
        tags: str = typer.Option(None, help="Comma-separated list of tags, e.g. 'exile,memory'"),
):
    """Add a note to a book or author"""
    # verify the target actually exists
    if target_type == TargetType.book and not book_repo.get_by_id(target_id):
        typer.echo(f"No book found with id {target_id}")
        raise typer.Exit()
    if target_type == TargetType.author and not author_repo.get_by_id(target_id):
        typer.echo(f"No author found with id {target_id}")
        raise typer.Exit()

    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    note = Note(
        text=text,
        target_id=target_id,
        target_type=target_type.value,
        tags=tag_list,
    )
    note_repo.add(note)
    typer.echo(f"Note added (id: {note.id})")

@app.command("list")
def list_notes():
    """List all notes in the archive"""
    notes = note_repo.list_all()
    if not notes:
        typer.echo("No notes found")
        raise typer.Exit()
    for i, n in enumerate(notes, 1):
        print(f"---- [{i}]")
        _format_note(n)


@app.command("by-target")
def notes_by_target(target_id: str = typer.Argument(...)):
    """Get all notes attached to a specific book or author id."""
    results = note_repo.get_by_target(target_id)
    if not results:
        typer.echo(f"No notes found for target {target_id}.")
        raise typer.Exit()
    for i, n in enumerate(results, 1):
        print(f"---- [{i}]")
        _format_note(n)


@app.command("by-tag")
def notes_by_tag(tag: str = typer.Argument(...)):
    """Get all notes with a specific tag."""
    results = note_repo.get_by_tag(tag)
    if not results:
        typer.echo(f"No notes found with tag '{tag}'.")
        raise typer.Exit()
    for i, n in enumerate(results, 1):
        print(f"---- [{i}]")
        _format_note(n)


@app.command("search")
def search_notes(query: str = typer.Argument(...)):
    """Full text search across notes content."""
    results = note_repo.search(query)
    if not results:
        typer.echo(f"No notes found matching query '{query}'.")
        raise typer.Exit()
    for i, n in enumerate(results, 1):
        print(f"---- [{i}]")
        _format_note(n)


@app.command("delete")
def delete_note(id: str = typer.Argument(...)):
    """Delete a note by id."""
    deleted = note_repo.delete(id)
    if deleted:
        typer.echo(f"Note {id} deleted.")
    else:
        typer.echo(f"No note found with id {id}.")


@app.command("update")
def update_note(
        id: str = typer.Argument(...),
        text: str = typer.Option(None),
        tags: str = typer.Option(None, help="Comma separated list of tags, replaces existing tags"),
):
    """Update a note's text or tags."""
    note = note_repo.get_by_id(id)
    if not note:
        typer.echo(f"No note found with id {id}.")
        raise typer.Exit()

    if text is not None:
        note.text = text
    if tags is not None:
        note.tags = [t.strip() for t in tags.split(",")]

    note_repo.update(note)
    typer.echo(f"Note updated (id: {note.id}).")
