# Sonar 🦇

A privacy-first, ultra-fast CLI tool for semantically searching through your local codebase. It parses your code into meaningful overlapping chunks, creates a TF-IDF mathematical vector space of your code, and retrieves the most relevant files using Cosine Similarity.

## Why this is impressive

1. Zero API calls. Zero cost. Your proprietary code never leaves your laptop.
2. Built with highly optimized Scikit-Learn sparse matrix operations.
3. Automatically respects `.gitignore` rules out of the box to prevent indexing `node_modules` or build artifacts.

## Installation

1. Ensure you have Python 3.10+ installed.
2. The project uses a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install typer rich pathspec scikit-learn numpy
```

## Usage

The CLI comes with a convenient `run.sh` wrapper.

**1. Index a directory:**
The tool traverses your source code and builds the TF-IDF Matrix index.

```bash
./run.sh index .
```

**2. Search the codebase:**
Find the most relevant snippets of code using mathematical similarity.

```bash
./run.sh search "how does vectorization work" --num 3
```

**3. Clear the database:**

```bash
./run.sh clear
```
