import os
import pickle
from pathlib import Path
import pathspec
from rich.console import Console
from sklearn.feature_extraction.text import TfidfVectorizer

from config import SUPPORTED_EXTENSIONS, CHUNK_SIZE, CHUNK_OVERLAP, DB_DIR

console = Console()

VECTOR_FILE = DB_DIR / "vector_store.pkl"

def get_ignore_spec(directory: Path) -> pathspec.PathSpec:
    gitignore_path = directory / ".gitignore"
    patterns = [
        ".git/", ".venv/", "venv/", "node_modules/", 
        "__pycache__/", "*.pyc", "build/", "dist/",
        "*.min.js", "*.min.css", "local_model/"
    ]
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                patterns.extend(f.readlines())
        except Exception:
            pass
    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, patterns)

def get_files_to_index(directory: Path) -> list[Path]:
    spec = get_ignore_spec(directory)
    files_to_index = []
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not spec.match_file(str((root_path / d).relative_to(directory)) + "/")]
        for file in files:
            full_path = root_path / file
            try:
                rel_path = full_path.relative_to(directory)
                if spec.match_file(str(rel_path)):
                    continue
                if full_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files_to_index.append(full_path)
            except ValueError:
                pass
    return files_to_index

def chunk_text(text: str, max_chars: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text: return []
    chunks, start, text_len = [], 0, len(text)
    while start < text_len:
        end = start + max_chars
        chunks.append(text[start:end])
        start += (max_chars - overlap)
    return chunks

def index_directory(directory: Path):
    directory = Path(directory).resolve()
    console.print(f"[bold blue]Scanning directory: {directory}[/bold blue]")
    files = get_files_to_index(directory)
    console.print(f"Found [bold green]{len(files)}[/bold green] text files.")
    
    if not files:
        console.print("[yellow]No files found.[/yellow]")
        return
        
    all_chunks = []
    metadatas = []
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            chunks = chunk_text(content)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                metadatas.append({"file_path": str(file_path), "chunk_index": i})
        except Exception as e:
            pass
            
    console.print("[dim]Vectorizing codebase using TF-IDF (Zero-download ML)...[/dim]")
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(all_chunks)
    
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with open(VECTOR_FILE, "wb") as f:
        pickle.dump({
            "vectorizer": vectorizer,
            "matrix": tfidf_matrix,
            "metadatas": metadatas,
            "documents": all_chunks
        }, f)
        
    console.print(f"\n✨ [bold green]Indexing complete! Extracted {len(all_chunks)} chunks.[/bold green] ✨")
