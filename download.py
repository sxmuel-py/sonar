import os
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from sentence_transformers import SentenceTransformer

print("Downloading all-MiniLM-L6-v2 headless...")
SentenceTransformer("all-MiniLM-L6-v2")
print("Download complete!")
