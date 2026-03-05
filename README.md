<div align="center">
  <img src="https://raw.githubusercontent.com/sxmuel-py/sonar/main/assets/banner.png" alt="Sonar Logo" width="100%" />

# 🦇 Sonar

**A blazing fast, zero-dependency local semantic code search engine.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

_Find the conceptual needle in your 10,000-file haystack. Offline. Instantly._

</div>

<br />

## 🚀 Why Sonar?

Tired of using `grep` and only finding exact string matches? Sick of paying for cloud APIs just to search your own code?

**Sonar** is a privacy-first CLI tool for semantically searching through your local codebase. It reads your code, creates a TF-IDF mathematical vector space of your syntax, and retrieves the most conceptually relevant files using _Cosine Similarity_.

### ✨ Features

- 🔒 **100% Offline & Private:** Your proprietary code never leaves your laptop. Zero API calls. Zero cost.
- ⚡ **Blazing Fast Matmatics:** Built with highly optimized Scikit-Learn sparse matrix operations instead of heavy ML models.
- 🧠 **Context-Aware Ingestion:** Automatically respects `.gitignore` rules (via `pathspec`) out of the box to prevent indexing `node_modules` or massive build artifacts.
- 🎨 **Gorgeous CLI UX:** Powered by `Rich` and `Typer`, featuring dynamic, language-aware syntax highlighting for every search result.
- ⌨️ **Interactive REPL:** Search multiple queries rapidly without restarting the script.

<br />

---

## 🛠 Installation

1. Ensure you have **Python 3.10+** installed.
2. Clone this repository and initialize the virtual environment:

```bash
git clone https://github.com/sxmuel-py/sonar.git
cd sonar

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install typer rich pathspec scikit-learn numpy
```

<br />

---

## 💻 Usage

Sonar comes with a convenient `run.sh` wrapper that handles the virtual environment for you.

### 1. Index a Directory

Tell Sonar to read a directory, parse all the code, and build the TF-IDF mathematical matrix.

```bash
./run.sh index /path/to/your/codebase
```

_(Sonar will dynamically chunk large files, extract the semantic context, and save the compressed `vector_store.pkl` database to `~/.sonar/vector_db`.)_

### 2. Search (Single Query)

Find the most relevant snippets of code using natural language.

```bash
./run.sh search "how does the file parser skip ignored directories?" --num 3
```

### 3. Interactive Search Mode (REPL)

Launch the interactive shell to run rapid-fire semantic queries.

```bash
./run.sh search
```

> `🦇 Entering Interactive Sonar Search... (type 'exit' to quit)`

### 4. Clear the Database

Wipe your local vector store clean.

```bash
./run.sh clear
```

<br />

---

## 🧠 How it Works Under the Hood

Unlike typical LLM-based RAG engines that require downloading gigabytes of neural network weights (like HuggingFace embeddings), Sonar utilizes **Applied Mathematics**:

1. **Extraction:** It reads your files, chunking them into 500-character overlapping segments to preserve context.
2. **Vectorization (TF-IDF):** It calculates a _Term Frequency-Inverse Document Frequency_ matrix across the entire codebase.
3. **Retrieval (Cosine Similarity):** When you search, it converts your query into a vector and calculates the $\frac{A \cdot B}{||A|| ||B||}$ geometric angle between your query and every code chunk, returning the closest mathematical matches.

<br />

---

## 🤝 Support the Creator

If this tool saved you hours of `grep`ing through legacy code, consider buying me a coffee! As an independent developer, your support helps me keep building privacy-first, zero-telemetry open-source tools.

<br />

<div align="center">
  
  ### ☕ Buy Me A Coffee (Crypto)
  If you love decentralization as much as I do:
  
  **BTC:** `bc1q... (Add your BTC address here)`  
  **ETH / ERC-20:** `0x... (Add your ETH address here)`  
  **SOL:** `... (Add your Solana address here)`

  <br />

### 🇳🇬 Direct Support (Naira)

For my local supporters:

**Bank:** `(Insert Bank Name)`  
 **Account Number:** `(Insert Account Number)`  
 **Account Name:** `(Insert Your Name)`

</div>

<br />

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
