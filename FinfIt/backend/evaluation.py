class EvaluationMetrics:

    # Extract document IDs from search results
    @staticmethod
    def extract_ids(documents):

        extracted = []

        for document in documents:

            if isinstance(document, dict):
                extracted.append(document.get("document_id"))
            else:
                extracted.append(document)

        return [doc for doc in extracted if doc is not None]

    # Precision
    @staticmethod
    def precision(retrieved, relevant):

        retrieved = EvaluationMetrics.extract_ids(retrieved)
        relevant = set(EvaluationMetrics.extract_ids(relevant))

        if not retrieved:
            return 0.0

        relevant_retrieved = len(set(retrieved) & relevant)

        return relevant_retrieved / len(retrieved)

    # Recall
    @staticmethod
    def recall(retrieved, relevant):

        retrieved = EvaluationMetrics.extract_ids(retrieved)
        relevant = set(EvaluationMetrics.extract_ids(relevant))

        if not relevant:
            return 0.0

        relevant_retrieved = len(set(retrieved) & relevant)

        return relevant_retrieved / len(relevant)

    # Precision at K
    @staticmethod
    def precision_at_k(retrieved, relevant, k=10):

        if k <= 0:
            return 0.0

        retrieved = EvaluationMetrics.extract_ids(retrieved)
        relevant = set(EvaluationMetrics.extract_ids(relevant))

        top_k = retrieved[:k]

        relevant_count = sum(
            1 for doc in top_k if doc in relevant
        )

        return relevant_count / k

    # Recall at K
    @staticmethod
    def recall_at_k(retrieved, relevant, k=10):

        retrieved = EvaluationMetrics.extract_ids(retrieved)
        relevant = set(EvaluationMetrics.extract_ids(relevant))

        if not relevant or k <= 0:
            return 0.0

        top_k = retrieved[:k]

        relevant_count = sum(
            1 for doc in top_k if doc in relevant
        )

        return relevant_count / len(relevant)

    # F1 Score
    @staticmethod
    def f1_score(precision, recall):

        if precision + recall == 0:
            return 0.0

        return (
            2 * precision * recall
        ) / (precision + recall)

    # Average Precision
    @staticmethod
    def average_precision(retrieved, relevant):

        retrieved = EvaluationMetrics.extract_ids(retrieved)
        relevant = set(EvaluationMetrics.extract_ids(relevant))

        if not relevant:
            return 0.0

        relevant_count = 0
        precision_sum = 0.0

        for rank, document in enumerate(retrieved, start=1):

            if document in relevant:

                relevant_count += 1

                precision_sum += relevant_count / rank

        return precision_sum / len(relevant)

    # Mean Average Precision
    @staticmethod
    def mean_average_precision(results, relevant_documents):

        if not results:
            return 0.0

        average_precisions = []

        for query, retrieved in results.items():

            relevant = relevant_documents.get(query, set())

            ap = EvaluationMetrics.average_precision(
                retrieved, relevant
            )

            average_precisions.append(ap)

        return sum(average_precisions) / len(average_precisions)

    # Mean Reciprocal Rank
    @staticmethod
    def mean_reciprocal_rank(results, relevant_documents):

        if not results:
            return 0.0

        reciprocal_ranks = []

        for query, retrieved in results.items():

            retrieved = EvaluationMetrics.extract_ids(retrieved)

            relevant = set(
                EvaluationMetrics.extract_ids(
                    relevant_documents.get(query, set())
                )
            )

            reciprocal_rank = 0.0

            for rank, document in enumerate(retrieved, start=1):

                if document in relevant:

                    reciprocal_rank = 1 / rank
                    break

            reciprocal_ranks.append(reciprocal_rank)

        return sum(reciprocal_ranks) / len(reciprocal_ranks)

    # Complete Evaluation Report
    @staticmethod
    def evaluate(retrieved, relevant, k=10):

        p = EvaluationMetrics.precision(retrieved, relevant)
        r = EvaluationMetrics.recall(retrieved, relevant)

        return {
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1_score": round(
                EvaluationMetrics.f1_score(p, r), 4
            ),
            "precision_at_k": round(
                EvaluationMetrics.precision_at_k(
                    retrieved, relevant, k
                ), 4
            ),
            "recall_at_k": round(
                EvaluationMetrics.recall_at_k(
                    retrieved, relevant, k
                ), 4
            ),
            "average_precision": round(
                EvaluationMetrics.average_precision(
                    retrieved, relevant
                ), 4
            )
        }