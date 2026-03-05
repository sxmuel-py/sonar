import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

from indexer import index_directory
from searcher import search_codebase
from db import get_collection

app = typer.Typer(help="Sonar: A blazing fast, zero-dependency local semantic code search engine.")
console = Console()

@app.command()
def index(directory: str = typer.Argument(..., help="Path to the directory to index")):
    """Scan and index a directory of source code into the local vector DB."""
    path = Path(directory)
    if not path.is_dir():
        console.print(f"[bold red]Error:[/bold red] '{directory}' is not a valid directory.")
        raise typer.Exit(code=1)
        
    index_directory(path)

@app.command()
def search(
    query: str = typer.Argument(None, help="Natural language query to search for. Leave empty for interactive mode."),
    n: int = typer.Option(5, "--num", "-n", help="Number of results to return")
):
    """Semantic search your indexed codebase."""
    if query:
        search_codebase(query, n_results=n)
    else:
        console.print("[bold cyan]🦇 Entering Interactive Sonar Search... (type 'exit' to quit)[/bold cyan]")
        while True:
            try:
                user_query = Prompt.ask("\n[bold green]Query[/bold green]")
                if user_query.strip().lower() in ['exit', 'quit']:
                    console.print("[dim]Exiting Sonar...[/dim]")
                    break
                if user_query.strip():
                    search_codebase(user_query, n_results=n)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Exiting Sonar...[/dim]")
                break

@app.command()
def clear():
    """Clear the local vector database."""
    confirm = typer.confirm("Are you sure you want to delete all indexed data?")
    if confirm:
        collection = get_collection()
        collection.clear()
        console.print("[green]Database cleared![/green]")

if __name__ == "__main__":
    app()
