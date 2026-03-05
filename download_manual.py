import os
import urllib.request
from pathlib import Path

repo_url = "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main"
files = [
    "config.json",
    "config_sentence_transformers.json",
    "modules.json",
    "README.md",
    "sentence_bert_config.json",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.txt",
    "pytorch_model.bin",
    "1_Pooling/config.json"
]

local_dir = Path("local_model")
local_dir.mkdir(exist_ok=True)
(local_dir / "1_Pooling").mkdir(exist_ok=True)

for file in files:
    out_path = local_dir / file
    if not out_path.exists():
        url = f"{repo_url}/{file}"
        print(f"Downloading {file}...")
        try:
            urllib.request.urlretrieve(url, out_path)
            print(f"Downloaded {file}!")
        except Exception as e:
            print(f"Failed to download {file}: {e}")

print("All files downloaded.")
