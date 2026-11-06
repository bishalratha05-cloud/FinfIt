import math
from collections import Counter


class RankingAlgorithms:

    def __init__(self):
        self.k1 = 1.5
        self.b = 0.75

    def calculate_tf(self, term, document):
        words = document.split()

        if not words:
            return 0

        frequency = words.count(term)

        return frequency / len(words)

    def calculate_idf(self, term, documents):
        total_documents = len(documents)

        if total_documents == 0:
            return 0

        document_frequency = sum(
            1 for doc in documents if term in doc.split()
        )

        return math.log(
            1 + (total_documents - document_frequency + 0.5)
            / (document_frequency + 0.5)
        )

    def tf_idf_score(self, query, document, documents):
        score = 0

        query_terms = query.lower().split()
        document = document.lower()

        for term in query_terms:
            tf = self.calculate_tf(term, document)
            idf = self.calculate_idf(term, documents)

            score += tf * idf

        return score

    def bm25_score(self, query, document, documents):
        query_terms = query.lower().split()
        document_words = document.lower().split()

        total_documents = len(documents)

        if total_documents == 0 or not document_words:
            return 0

        average_length = sum(
            len(doc.split()) for doc in documents
        ) / total_documents

        document_length = len(document_words)
        frequencies = Counter(document_words)

        score = 0

        for term in query_terms:
            frequency = frequencies[term]

            if frequency == 0:
                continue

            document_frequency = sum(
                1 for doc in documents
                if term in doc.lower().split()
            )

            idf = math.log(
                1 + (
                    total_documents - document_frequency + 0.5
                ) / (document_frequency + 0.5)
            )

            numerator = frequency * (self.k1 + 1)

            denominator = frequency + self.k1 * (
                1 - self.b
                + self.b * document_length / average_length
            )

            score += idf * numerator / denominator

        return score

    def rank_documents(self, query, documents, method="bm25"):
        results = []

        for index, document in enumerate(documents):
            if method == "tfidf":
                score = self.tf_idf_score(
                    query, document, documents
                )
            else:
                score = self.bm25_score(
                    query, document, documents
                )

            results.append({
                "document_id": index,
                "score": score
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results