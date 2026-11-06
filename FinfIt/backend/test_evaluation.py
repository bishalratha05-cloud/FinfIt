import unittest

from backend.evaluation import EvaluationMetrics


class TestEvaluationMetrics(unittest.TestCase):

    def setUp(self):
        self.retrieved = ["D1", "D2", "D3", "D4"]
        self.relevant = {"D1", "D3", "D5"}

    def test_extract_ids(self):
        documents = [
            {"document_id": "D1"},
            "D2",
            {"document_id": None},
            {"title": "Missing ID"}
        ]
        self.assertEqual(
            EvaluationMetrics.extract_ids(documents),
            ["D1", "D2"]
        )

    def test_precision(self):
        self.assertAlmostEqual(
            EvaluationMetrics.precision(
                self.retrieved, self.relevant
            ), 0.5
        )

    def test_precision_empty_retrieved(self):
        self.assertEqual(
            EvaluationMetrics.precision([], self.relevant), 0.0
        )

    def test_recall(self):
        self.assertAlmostEqual(
            EvaluationMetrics.recall(
                self.retrieved, self.relevant
            ), 2 / 3
        )

    def test_recall_empty_relevant(self):
        self.assertEqual(
            EvaluationMetrics.recall(self.retrieved, set()), 0.0
        )

    def test_f1_score(self):
        self.assertAlmostEqual(
            EvaluationMetrics.f1_score(0.5, 2 / 3), 4 / 7
        )

    def test_f1_score_zero(self):
        self.assertEqual(
            EvaluationMetrics.f1_score(0, 0), 0.0
        )

    def test_precision_at_k(self):
        self.assertAlmostEqual(
            EvaluationMetrics.precision_at_k(
                self.retrieved, self.relevant, 2
            ), 0.5
        )

    def test_precision_at_k_zero(self):
        self.assertEqual(
            EvaluationMetrics.precision_at_k(
                self.retrieved, self.relevant, 0
            ), 0.0
        )

    def test_recall_at_k(self):
        self.assertAlmostEqual(
            EvaluationMetrics.recall_at_k(
                self.retrieved, self.relevant, 2
            ), 1 / 3
        )

    def test_recall_at_k_empty_relevant(self):
        self.assertEqual(
            EvaluationMetrics.recall_at_k(
                self.retrieved, set(), 2
            ), 0.0
        )

    def test_recall_at_k_zero(self):
        self.assertEqual(
            EvaluationMetrics.recall_at_k(
                self.retrieved, self.relevant, 0
            ), 0.0
        )

    def test_average_precision(self):
        self.assertAlmostEqual(
            EvaluationMetrics.average_precision(
                self.retrieved, self.relevant
            ), 5 / 9
        )

    def test_average_precision_empty_relevant(self):
        self.assertEqual(
            EvaluationMetrics.average_precision(
                self.retrieved, set()
            ), 0.0
        )

    def test_mean_average_precision(self):
        results = {
            "query1": ["D1", "D2", "D3"],
            "query2": ["D4", "D5", "D6"]
        }
        relevant_documents = {
            "query1": {"D1", "D3"},
            "query2": {"D5"}
        }

        self.assertAlmostEqual(
            EvaluationMetrics.mean_average_precision(
                results, relevant_documents
            ), 2 / 3
        )

    def test_mean_average_precision_empty(self):
        self.assertEqual(
            EvaluationMetrics.mean_average_precision({}, {}), 0.0
        )

    def test_mean_average_precision_missing_relevant_query(self):
        result = EvaluationMetrics.mean_average_precision(
            {"query1": ["D1"]},
            {}
        )
        self.assertEqual(result, 0.0)

    def test_mean_reciprocal_rank(self):
        results = {
            "query1": ["D1", "D2", "D3"],
            "query2": ["D4", "D5", "D6"]
        }
        relevant_documents = {
            "query1": {"D3"},
            "query2": {"D5"}
        }

        self.assertAlmostEqual(
            EvaluationMetrics.mean_reciprocal_rank(
                results, relevant_documents
            ), 5 / 12
        )

    def test_mean_reciprocal_rank_empty(self):
        self.assertEqual(
            EvaluationMetrics.mean_reciprocal_rank({}, {}), 0.0
        )

    def test_mean_reciprocal_rank_no_match(self):
        result = EvaluationMetrics.mean_reciprocal_rank(
            {"query1": ["D1", "D2"]},
            {"query1": {"D3"}}
        )
        self.assertEqual(result, 0.0)

    def test_complete_evaluation(self):
        result = EvaluationMetrics.evaluate(
            self.retrieved, self.relevant, k=2
        )

        self.assertIn("precision", result)
        self.assertIn("recall", result)
        self.assertIn("f1_score", result)
        self.assertIn("precision_at_k", result)
        self.assertIn("recall_at_k", result)
        self.assertIn("average_precision", result)

    def test_complete_evaluation_empty(self):
        result = EvaluationMetrics.evaluate([], set())

        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["f1_score"], 0.0)


if __name__ == "__main__":
    unittest.main()