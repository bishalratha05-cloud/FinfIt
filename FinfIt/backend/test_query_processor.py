import unittest
from unittest.mock import patch

from backend.query_processor import QueryProcessor


class TestQueryProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = QueryProcessor()
        self.processor.stop_words = {"the", "is", "a", "and"}

    def test_clean_query(self):
        result = self.processor.clean_query("Hello, WORLD! FinfIt 123")
        self.assertEqual(result, "hello world finfit 123")

    def test_tokenize_query(self):
        with patch("backend.query_processor.tokenize",
                   return_value=["hello", "world"]):
            result = self.processor.tokenize_query("Hello World")
        self.assertEqual(result, ["hello", "world"])

    def test_remove_stopwords(self):
        with patch("backend.query_processor.tokenize",
                   return_value=["the", "search", "is", "working"]):
            result = self.processor.remove_stopwords("the search is working")
        self.assertEqual(result, ["search", "working"])

    def test_process_query(self):
        with patch("backend.query_processor.tokenize",
                   return_value=["the", "search", "engine"]):
            result = self.processor.process_query("the search engine")

        self.assertEqual(result["original_query"], "the search engine")
        self.assertEqual(result["tokens"], ["the", "search", "engine"])
        self.assertEqual(result["filtered_tokens"], ["search", "engine"])
        self.assertEqual(result["token_count"], 3)
        self.assertEqual(result["unique_terms"], ["search", "engine"])

    def test_query_frequency(self):
        with patch("backend.query_processor.tokenize",
                   return_value=["search", "engine", "search"]):
            result = self.processor.query_frequency("search engine search")
        self.assertEqual(result, {"search": 2, "engine": 1})

    def test_detect_boolean_operators(self):
        result = self.processor.detect_boolean_operators(
            "python AND java OR C++ NOT PHP"
        )
        self.assertEqual(result, ["AND", "OR", "NOT"])

    def test_detect_no_boolean_operators(self):
        result = self.processor.detect_boolean_operators("python programming")
        self.assertEqual(result, [])

    def test_detect_phrase_query(self):
        self.assertTrue(
            self.processor.detect_phrase_query('"information retrieval"')
        )
        self.assertFalse(
            self.processor.detect_phrase_query("information retrieval")
        )

    def test_extract_phrase(self):
        result = self.processor.extract_phrase('"information retrieval"')
        self.assertEqual(result, "information retrieval")

    def test_extract_invalid_phrase(self):
        result = self.processor.extract_phrase("information retrieval")
        self.assertIsNone(result)

    def test_suggest_query(self):
        result = self.processor.suggest_query(
            "pro",
            ["programming", "python", "project", "java"],
            limit=2
        )
        self.assertEqual(result, ["programming", "project"])

    def test_suggest_query_no_results(self):
        result = self.processor.suggest_query(
            "xyz", ["python", "java", "programming"]
        )
        self.assertEqual(result, [])

    def test_query_statistics(self):
        with patch("backend.query_processor.tokenize",
                   return_value=["the", "search", "engine", "search"]):
            result = self.processor.query_statistics(
                "the search engine search"
            )

        self.assertEqual(result["total_words"], 4)
        self.assertEqual(result["unique_words"], 3)
        self.assertEqual(result["filtered_words"], 3)
        self.assertEqual(result["stopwords_removed"], 1)


if __name__ == "__main__":
    unittest.main()