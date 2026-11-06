# FinfIt — Information Retrieval System
## Mini Project Report (Web Search Mining)

### 1. Abstract
FinfIt is a web-based educational information retrieval system. It accepts a query from a user and searches a collection of text documents. The system extracts text from TXT, PDF and DOCX files, processes the text, builds an inverted index, and retrieves relevant documents. It supports TF-IDF and BM25 ranking, simple Boolean retrieval, exact phrase search, document upload, and search history.

### 2. Problem Statement
Users often need to locate useful information inside a collection of documents. Opening every document and reading it manually is inefficient. The project demonstrates how an information retrieval system can index documents and return likely relevant items in response to a query.

### 3. Objectives
1. Build a simple web interface for searching documents.
2. Extract text from common document formats.
3. Process text into normalized terms.
4. Build an inverted index.
5. Implement ranked retrieval using TF-IDF and BM25.
6. Demonstrate Boolean and phrase searching.
7. Store search history in SQLite.

### 4. System Requirements
**Hardware:** A computer capable of running Python and a modern web browser.

**Software:** Windows/macOS/Linux, Python 3.10+, Flask, pypdf, python-docx, SQLite, and a web browser.

### 5. System Architecture
User → Flask web interface → Query processing → Inverted index / ranking engine → Ranked results → User.

Documents follow a separate path: Upload or sample folder → Text extraction → Tokenization and stop-word removal → Inverted index.

### 6. Methodology
**Document processing:** The system reads TXT, PDF or DOCX content. It converts text to lowercase tokens and removes a small set of common English stop words.

**Inverted index:** Each distinct term maps to a set of document identifiers containing that term.

**TF-IDF:** Term frequency rewards terms occurring in a document. Inverse document frequency gives greater weight to terms that appear in fewer documents. The implementation sums weighted term contributions for matching documents.

**BM25:** BM25 uses term frequency, inverse document frequency, and document-length normalization. The parameters used are k1 = 1.5 and b = 0.75.

**Boolean retrieval:** A basic parser supports AND, OR and NOT between terms.

**Phrase retrieval:** The query's normalized word sequence is checked as a contiguous phrase in each document.

### 7. Modules
1. `app.py`: Flask routes, upload handling and page rendering.
2. `document_loader.py`: TXT, PDF and DOCX text extraction.
3. `text_processing.py`: Tokenization, stop-word removal and snippets.
4. `search_engine.py`: Inverted index and retrieval algorithms.
5. `database.py`: SQLite search-history functions.
6. HTML templates: Search, upload, history and about pages.
7. CSS: Responsive visual design.

### 8. Testing
Suggested test cases:
- Search `artificial intelligence` using BM25.
- Search `information retrieval` using TF-IDF.
- Boolean query `artificial AND intelligence`.
- Boolean query `healthcare OR database`.
- Phrase query `information retrieval`.
- Upload a TXT file and search for a term inside it.
- Upload a text-based PDF and a DOCX file.
- Visit search history and clear it.

Record actual results and screenshots after running the project. Do not claim a test passed until it has been performed.

### 9. Limitations
- The system searches only documents stored in its local collection.
- It does not crawl or index the entire internet.
- PDF OCR for scanned images is not included.
- Boolean parsing is intentionally basic.
- The in-memory index is rebuilt when the application starts and after uploads.
- Search ranking is an educational implementation, not a production search service.

### 10. Future Scope
- Add a web crawler with responsible crawling rules.
- Add OCR for scanned documents.
- Add query spelling correction and autocomplete.
- Add field-aware ranking and metadata filters.
- Add evaluation datasets and precision/recall dashboards.
- Store the index persistently for larger collections.
- Add authentication and secure file management before public deployment.

### 11. Conclusion
FinfIt demonstrates the main stages of a document information retrieval pipeline: text extraction, preprocessing, indexing, query processing, ranking, and result presentation. It provides a practical foundation for understanding concepts in Web Search Mining.

### 12. References
- Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, *Introduction to Information Retrieval*, Cambridge University Press, 2008.
- Flask documentation: https://flask.palletsprojects.com/
- Python documentation: https://docs.python.org/3/
- SQLite documentation: https://www.sqlite.org/docs.html
