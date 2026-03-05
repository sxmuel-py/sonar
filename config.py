import os
from pathlib import Path

# Paths
APP_DIR = Path.home() / ".sonar"
DB_DIR = APP_DIR / "vector_db"

# Create directories if they don't exist
APP_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
EMBEDDING_MODEL = "./local_model"
COLLECTION_NAME = "codebase_chunks"

# Chunking configuration
CHUNK_SIZE = 500  # Number of characters approximately
CHUNK_OVERLAP = 50

# Supported text extensions
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".md", ".txt", 
    ".json", ".html", ".css", ".java", ".c", ".cpp", ".h", ".hpp", 
    ".sh", ".yaml", ".yml", ".toml", ".ini"
}
