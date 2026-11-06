# FinfIt — Information Retrieval System

FinfIt is a Flask-based educational document search application for the Web Search Mining course. It indexes a local collection of TXT, PDF and DOCX files and retrieves relevant documents using TF-IDF, BM25, Boolean retrieval and exact-phrase search.

## Features

- Search local documents with BM25 or TF-IDF ranking.
- Boolean queries using `AND`, `OR` and `NOT`.
- Exact phrase searching.
- Upload and index TXT, PDF and DOCX files (15 MB maximum).
- Browse indexed documents and recent search history.
- SQLite-backed search history.
- Responsive dark navy/blue interface.
- Backend unit tests and retrieval evaluation metrics.

> FinfIt searches the documents in its local collection. It is not an internet crawler or a general-purpose public web search engine. Scanned PDFs without selectable text are not OCR-processed.

## Project structure

```text
FinfIt/
├── app.py                      # Flask application and routes
├── requirements.txt            # Python dependencies
├── README.md
├── PROJECT_REPORT.md
├── .gitignore
├── backend/
│   ├── database.py             # SQLite search history
│   ├── document_loader.py      # TXT/PDF/DOCX extraction
│   ├── evaluation.py           # Precision, recall, MAP, MRR, etc.
│   ├── query_processor.py      # Query parsing and normalization
│   ├── ranking.py              # Standalone ranking helpers
│   ├── search_engine.py        # Indexing and retrieval
│   └── test_*.py               # Unit tests
├── sample_documents/           # Example documents indexed on startup
├── templates/                  # Jinja HTML pages
├── static/css/style.css        # Website styling
├── uploads/                    # User-uploaded documents
└── data/                       # Local SQLite database
```

## Requirements

- Python 3.10+
- pip
- VS Code (recommended)
- A modern web browser

## Run locally (Windows PowerShell)

1. Open this folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.
3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Start the app:

   ```powershell
   python app.py
   ```
5. Visit **http://127.0.0.1:5000** in your browser.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Run tests

From the project root:

```bash
python -m unittest discover -s backend -p 'test*.py' -v
```

## GitHub setup

Create a new empty GitHub repository named `FinfIt`, then run these commands from this folder (replace the URL with your repository URL):

```bash
git init
git add .
git commit -m "Create FinfIt information retrieval system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/FinfIt.git
git push -u origin main
```

Do not commit `.venv`, local database files, or uploaded user documents; `.gitignore` excludes them.

## Academic scope

The project demonstrates document extraction, text normalization, inverted indexing, query processing, ranked retrieval and evaluation. It is intended as an educational prototype, not a production search service.

## Author

**Ashish Gain**  
Computer Science and Engineering  
IIIT Bhubaneswar
