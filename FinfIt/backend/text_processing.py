import re

# A compact English stop-word list keeps the project self-contained.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but",
    "by", "for", "from", "had", "has", "have", "he", "her", "hers",
    "him", "his", "i", "in", "into", "is", "it", "its", "me", "my",
    "of", "on", "or", "our", "ours", "she", "that", "the", "their",
    "theirs", "them", "they", "this", "those", "to", "was", "we",
    "were", "what", "when", "where", "which", "who", "will", "with",
    "you", "your", "yours"
}

def tokenize(text):
    """Convert text into lowercase word tokens."""
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def normalize(text, remove_stopwords=True):
    """Tokenize text and optionally remove common stop words."""
    tokens = tokenize(text)
    if remove_stopwords:
        tokens = [word for word in tokens if word not in STOP_WORDS]
    return tokens

def make_snippet(text, query, length=260):
    """Return a short preview around the first matching query term."""
    clean = re.sub(r"\s+", " ", text).strip()
    terms = [t for t in tokenize(query) if t]
    lower = clean.lower()
    positions = [lower.find(term) for term in terms if lower.find(term) >= 0]
    if positions:
        start = max(0, min(positions) - 90)
        end = min(len(clean), start + length)
        snippet = clean[start:end]
        if start:
            snippet = "…" + snippet
        if end < len(clean):
            snippet += "…"
        return snippet
    return clean[:length] + ("…" if len(clean) > length else "")
