import pickle
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from sklearn.metrics.pairwise import cosine_similarity
from config import DB_DIR

console = Console()
VECTOR_FILE = DB_DIR / "vector_store.pkl"

def search_codebase(query: str, n_results: int = 5):
    if not VECTOR_FILE.exists():
        console.print("[yellow]Database is empty. Please run 'index <dir>' first.[/yellow]")
        return
        
    with open(VECTOR_FILE, "rb") as f:
        data = pickle.load(f)
        
    vectorizer = data["vectorizer"]
    matrix = data["matrix"]
    metadatas = data["metadatas"]
    documents = data["documents"]
    
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, matrix).flatten()
    
    # Get top N indices sorted by similarity score
    top_indices = similarities.argsort()[-n_results:][::-1]
    
    if similarities[top_indices[0]] == 0:
        console.print("[yellow]No relevant results found for your query.[/yellow]")
        return
        
    console.print(f"\n[bold green]Top {n_results} Results for:[/bold green] '{query}'\n")
    
    for idx in top_indices:
        score = similarities[idx]
        if score == 0:
            continue
            
        doc = documents[idx]
        file_path = metadatas[idx]["file_path"]
        
        ext = Path(file_path).suffix.lower()
        lang_map = {
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".go": "go", ".rs": "rust", ".md": "markdown",
            ".html": "html", ".css": "css", ".json": "json"
        }
        lang = lang_map.get(ext, "text")
        
        syntax = Syntax(doc, lang, theme="monokai", line_numbers=True, word_wrap=True)
        similarity_pct = score * 100
        
        panel = Panel(
            syntax, 
            title=f"[bold cyan]{file_path}[/bold cyan] [dim text](Relevance: {similarity_pct:.1f}%)[/dim text]",
            title_align="left",
            border_style="cyan"
        )
        console.print(panel)
        console.print()
