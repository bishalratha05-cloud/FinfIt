import re
from collections import Counter

from backend.text_processing import (
    tokenize,
    normalize,
    STOP_WORDS
)


class QueryProcessor:

    def __init__(self):
        self.stop_words = STOP_WORDS

    def clean_query(self, query):

        query = query.strip().lower()

        query = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            query
        )

        query = re.sub(
            r"\s+",
            " ",
            query
        )

        return query

    def tokenize_query(self, query):

        cleaned_query = self.clean_query(query)

        return tokenize(cleaned_query)

    def remove_stopwords(self, query):

        tokens = self.tokenize_query(query)

        return [
            word for word in tokens
            if word not in self.stop_words
        ]

    def process_query(self, query):

        original_tokens = self.tokenize_query(query)

        filtered_tokens = self.remove_stopwords(query)

        return {
            "original_query": query,
            "cleaned_query": self.clean_query(query),
            "tokens": original_tokens,
            "filtered_tokens": filtered_tokens,
            "token_count": len(original_tokens),
            "unique_terms": list(
                dict.fromkeys(filtered_tokens)
            )
        }

    def query_frequency(self, query):

        tokens = self.remove_stopwords(query)

        return dict(Counter(tokens))

    def detect_boolean_operators(self, query):

        operators = re.findall(
            r"\b(AND|OR|NOT)\b",
            query.upper()
        )

        return operators

    def detect_phrase_query(self, query):

        return (
            len(query) >= 2
            and query.startswith('"')
            and query.endswith('"')
        )

    def extract_phrase(self, query):

        if self.detect_phrase_query(query):

            return query[1:-1].strip()

        return None

    def suggest_query(self, query, vocabulary, limit=5):

        query = query.lower().strip()

        suggestions = []

        for word in vocabulary:

            if word.startswith(query) and word != query:

                suggestions.append(word)

        return suggestions[:limit]

    def query_statistics(self, query):

        tokens = self.tokenize_query(query)

        filtered = self.remove_stopwords(query)

        return {
            "total_words": len(tokens),
            "unique_words": len(set(tokens)),
            "filtered_words": len(filtered),
            "stopwords_removed": (
                len(tokens) - len(filtered)
            )
        }