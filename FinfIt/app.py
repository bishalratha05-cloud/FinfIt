from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from backend.document_loader import extract_text
from backend.search_engine import SearchEngine
from backend.database import init_db, save_search, get_history, clear_history

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
SAMPLE_DIR = BASE_DIR / "sample_documents"
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-before-deployment"
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024  # 15 MB
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

UPLOAD_DIR.mkdir(exist_ok=True)
SAMPLE_DIR.mkdir(exist_ok=True)
init_db(BASE_DIR / "data" / "finfit.db")
engine = SearchEngine([SAMPLE_DIR, UPLOAD_DIR])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    method = "bm25"
    mode = "ranked"
    searched = False
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        method = request.form.get("method", "bm25")
        mode = request.form.get("mode", "ranked")
        searched = True
        if not query:
            flash("Please enter a search query.", "warning")
        else:
            results = engine.search(query, method=method, mode=mode)
            save_search(BASE_DIR / "data" / "finfit.db", query, method, len(results))
    return render_template("index.html", results=results, query=query,
                           method=method, mode=mode, searched=searched,
                           document_count=engine.document_count)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded = request.files.get("document")
        if not uploaded or not uploaded.filename:
            flash("Choose a file first.", "warning")
            return redirect(url_for("upload"))
        filename = secure_filename(uploaded.filename)
        if not allowed_file(filename):
            flash("Only TXT, PDF and DOCX files are supported.", "danger")
            return redirect(url_for("upload"))
        destination = UPLOAD_DIR / filename
        uploaded.save(destination)
        # Validate that text can be extracted before reporting success.
        try:
            text = extract_text(destination)
            if not text.strip():
                destination.unlink(missing_ok=True)
                raise ValueError("No readable text was found in this document.")
        except Exception as exc:
            destination.unlink(missing_ok=True)
            flash(f"Could not read that document: {exc}", "danger")
            return redirect(url_for("upload"))
        engine.rebuild()
        flash(f"Uploaded and indexed: {filename}", "success")
        return redirect(url_for("upload"))
    return render_template("upload.html", documents=engine.list_documents())

@app.route("/history")
def history():
    rows = get_history(BASE_DIR / "data" / "finfit.db")
    return render_template("history.html", rows=rows)

@app.route("/history/clear", methods=["POST"])
def history_clear():
    clear_history(BASE_DIR / "data" / "finfit.db")
    flash("Search history cleared.", "success")
    return redirect(url_for("history"))

@app.route("/about")
def about():
    return render_template("about.html", document_count=engine.document_count)

@app.errorhandler(413)
def too_large(_error):
    flash("The file is too large. Maximum upload size is 15 MB.", "danger")
    return redirect(url_for("upload"))

if __name__ == "__main__":
    # debug=True is useful locally. Turn it off for public deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)
