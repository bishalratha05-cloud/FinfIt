import math
from collections import defaultdict
from pathlib import Path

from backend.document_loader import extract_text
from backend.text_processing import normalize, tokenize, make_snippet
from backend.query_processor import QueryProcessor


class SearchEngine:

    def __init__(self, folders):
        self.folders = [Path(folder) for folder in folders]

        self.documents = {}
        self.tokens = {}
        self.inverted_index = defaultdict(set)
        self.document_count = 0

        self.query_processor = QueryProcessor()

        self.rebuild()

    # --------------------------------
    # DOCUMENT INDEXING
    # --------------------------------

    def rebuild(self):

        self.documents.clear()
        self.tokens.clear()
        self.inverted_index = defaultdict(set)

        for folder in self.folders:

            folder.mkdir(parents=True, exist_ok=True)

            for path in folder.iterdir():

                if path.is_file() and path.suffix.lower() in {
                    ".txt", ".pdf", ".docx"
                }:

                    try:

                        text = extract_text(path)

                        if not text.strip():
                            continue

                        doc_id = str(path.resolve())

                        self.documents[doc_id] = {
                            "id": doc_id,
                            "title": path.name,
                            "text": text,
                            "source": path.parent.name
                        }

                        terms = normalize(text)

                        self.tokens[doc_id] = terms

                        for term in set(terms):
                            self.inverted_index[term].add(doc_id)

                    except Exception as error:

                        print(
                            f"Error processing {path.name}: {error}"
                        )

        self.document_count = len(self.documents)

    # --------------------------------
    # IDF CALCULATION
    # --------------------------------

    def calculate_idf(self, term):

        df = len(self.inverted_index.get(term, ()))

        n = max(self.document_count, 1)

        return math.log(
            1 + (n - df + 0.5) / (df + 0.5)
        )

    # --------------------------------
    # TF-IDF RANKING
    # --------------------------------

    def tfidf_search(self, query_terms):

        scores = defaultdict(float)

        for term in query_terms:

            idf = math.log(
                (1 + self.document_count) /
                (1 + len(self.inverted_index.get(term, ())))
            ) + 1

            for doc_id in self.inverted_index.get(term, ()):

                tf = self.tokens[doc_id].count(term)

                scores[doc_id] += (
                    (1 + math.log(tf)) * idf
                )

        return scores

    # --------------------------------
    # BM25 RANKING
    # --------------------------------

    def bm25_search(self, query_terms, k1=1.5, b=0.75):

        scores = defaultdict(float)

        lengths = {
            doc_id: len(tokens)
            for doc_id, tokens in self.tokens.items()
        }

        avg_length = (
            sum(lengths.values()) /
            max(len(lengths), 1)
        )

        for term in query_terms:

            idf = self.calculate_idf(term)

            for doc_id in self.inverted_index.get(term, ()):

                tf = self.tokens[doc_id].count(term)

                doc_length = lengths[doc_id]

                denominator = (
                    tf + k1 * (
                        1 - b + b * doc_length /
                        max(avg_length, 1)
                    )
                )

                score = (
                    idf * tf * (k1 + 1)
                ) / denominator

                scores[doc_id] += score

        return scores

    # --------------------------------
    # BOOLEAN RETRIEVAL
    # --------------------------------

    def boolean_search(self, query):

        parts = query.upper().split()

        if not parts:
            return set()

        result = set(
            self.inverted_index.get(
                parts[0].lower(), ()
            )
        )

        operators = {"AND", "OR", "NOT"}

        i = 1

        while i < len(parts):

            operator = parts[i]

            if operator not in operators or i + 1 >= len(parts):
                i += 1
                continue

            term = parts[i + 1].lower()

            matching_docs = set(
                self.inverted_index.get(term, ())
            )

            if operator == "AND":
                result &= matching_docs

            elif operator == "OR":
                result |= matching_docs

            elif operator == "NOT":
                result -= matching_docs

            i += 2

        return result

    # --------------------------------
    # PHRASE SEARCH
    # --------------------------------

    def phrase_search(self, query):

        phrase = " ".join(tokenize(query))

        matching_docs = set()

        for doc_id, document in self.documents.items():

            document_text = " ".join(
                tokenize(document["text"])
            )

            if phrase in document_text:
                matching_docs.add(doc_id)

        return matching_docs

    # --------------------------------
    # QUERY PROCESSING
    # --------------------------------

    def process_query(self, query):

        return self.query_processor.process_query(query)

    # --------------------------------
    # MAIN SEARCH FUNCTION
    # --------------------------------

    def search(self, query, method="bm25", mode="ranked"):

        processed = self.process_query(query)

        query_terms = normalize(query)

        raw_terms = processed["tokens"]

        if not raw_terms:
            return []

        # Boolean search

        if mode == "boolean":

            doc_ids = self.boolean_search(query)

            scores = {
                doc_id: 1.0
                for doc_id in doc_ids
            }

        # Phrase search

        elif mode == "phrase":

            doc_ids = self.phrase_search(query)

            scores = {
                doc_id: 1.0
                for doc_id in doc_ids
            }

        # Ranked retrieval

        else:

            if not query_terms:
                return []

            if method == "tfidf":

                scores = self.tfidf_search(query_terms)

            else:

                scores = self.bm25_search(query_terms)

            doc_ids = set(scores.keys())

        # Prepare results

        results = []

        for doc_id in doc_ids:

            document = self.documents[doc_id]

            results.append({

                "title": document["title"],

                "source": document["source"],

                "score": round(
                    scores.get(doc_id, 0), 4
                ),

                "snippet": make_snippet(
                    document["text"], query
                ),

                "document_id": doc_id

            })

        results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return results

    # --------------------------------
    # DOCUMENT LIST
    # --------------------------------

    def list_documents(self):

        documents = []

        for document in self.documents.values():

            documents.append({

                "title": document["title"],

                "source": document["source"]

            })

        return sorted(
            documents,
            key=lambda item: item["title"].lower()
        )

    # --------------------------------
    # COLLECTION STATISTICS
    # --------------------------------

    def get_statistics(self):

        total_terms = sum(
            len(terms)
            for terms in self.tokens.values()
        )

        vocabulary_size = len(self.inverted_index)

        return {

            "total_documents": self.document_count,

            "total_terms": total_terms,

            "vocabulary_size": vocabulary_size,

            "indexed_terms": vocabulary_size

        }