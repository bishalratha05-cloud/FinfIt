import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from backend.search_engine import SearchEngine


class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        (self.folder / "machine_learning.txt").write_text(
            "Machine learning is a branch of artificial intelligence.",
            encoding="utf-8"
        )

        (self.folder / "information_retrieval.txt").write_text(
            "Information retrieval is used in search engines.",
            encoding="utf-8"
        )

        (self.folder / "python_programming.txt").write_text(
            "Python is a popular programming language.",
            encoding="utf-8"
        )

        self.engine = SearchEngine([self.folder])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialization(self):
        self.assertEqual(self.engine.document_count, 3)

    def test_rebuild(self):
        self.engine.rebuild()
        self.assertEqual(self.engine.document_count, 3)

    def test_document_indexing(self):
        self.assertEqual(len(self.engine.documents), 3)

    def test_inverted_index(self):
        self.assertIn("python", self.engine.inverted_index)
        self.assertIn("machine", self.engine.inverted_index)

    def test_calculate_idf(self):
        result = self.engine.calculate_idf("python")
        self.assertGreater(result, 0)

    def test_calculate_idf_unknown_term(self):
        result = self.engine.calculate_idf("unknownword")
        self.assertGreater(result, 0)

    def test_tfidf_search(self):
        result = self.engine.tfidf_search(["python"])
        self.assertGreater(len(result), 0)

    def test_bm25_search(self):
        result = self.engine.bm25_search(["python"])
        self.assertGreater(len(result), 0)

    def test_bm25_custom_parameters(self):
        result = self.engine.bm25_search(
            ["python"], k1=2.0, b=0.5
        )
        self.assertGreater(len(result), 0)

    def test_boolean_search_and(self):
        result = self.engine.boolean_search(
            "information AND retrieval"
        )
        self.assertEqual(len(result), 1)

    def test_boolean_search_or(self):
        result = self.engine.boolean_search(
            "python OR machine"
        )
        self.assertEqual(len(result), 2)

    def test_boolean_search_not(self):
        result = self.engine.boolean_search(
            "python NOT programming"
        )
        self.assertEqual(len(result), 0)

    def test_boolean_empty_query(self):
        result = self.engine.boolean_search("")
        self.assertEqual(result, set())

    def test_boolean_invalid_operator(self):
        result = self.engine.boolean_search(
            "python UNKNOWN machine"
        )
        self.assertEqual(len(result), 1)

    def test_phrase_search(self):
        result = self.engine.phrase_search(
            "information retrieval"
        )
        self.assertEqual(len(result), 1)

    def test_phrase_search_no_match(self):
        result = self.engine.phrase_search(
            "artificial programming retrieval"
        )
        self.assertEqual(len(result), 0)

    def test_process_query(self):
        result = self.engine.process_query("python programming")

        self.assertIn("tokens", result)
        self.assertIn("filtered_tokens", result)

    def test_search_bm25(self):
        result = self.engine.search("python", method="bm25")

        self.assertGreater(len(result), 0)
        self.assertIn("title", result[0])
        self.assertIn("score", result[0])
        self.assertIn("snippet", result[0])

    def test_search_tfidf(self):
        result = self.engine.search("python", method="tfidf")
        self.assertGreater(len(result), 0)

    def test_search_boolean(self):
        result = self.engine.search(
            "python AND programming",
            mode="boolean"
        )
        self.assertEqual(len(result), 1)

    def test_search_phrase(self):
        result = self.engine.search(
            "information retrieval",
            mode="phrase"
        )
        self.assertEqual(len(result), 1)

    def test_search_empty_query(self):
        result = self.engine.search("")
        self.assertEqual(result, [])

    def test_search_only_stopwords(self):
        result = self.engine.search("the and is")
        self.assertEqual(result, [])

    def test_search_unknown_term(self):
        result = self.engine.search("xyzunknown")
        self.assertEqual(result, [])

    def test_list_documents(self):
        result = self.engine.list_documents()

        self.assertEqual(len(result), 3)
        self.assertIn("title", result[0])
        self.assertIn("source", result[0])

    def test_list_documents_sorted(self):
        result = self.engine.list_documents()

        titles = [doc["title"] for doc in result]

        self.assertEqual(titles, sorted(titles, key=str.lower))

    def test_get_statistics(self):
        result = self.engine.get_statistics()

        self.assertEqual(result["total_documents"], 3)
        self.assertGreater(result["total_terms"], 0)
        self.assertGreater(result["vocabulary_size"], 0)

    def test_empty_directory(self):
        empty_folder = self.folder / "empty"
        empty_folder.mkdir()

        engine = SearchEngine([empty_folder])

        self.assertEqual(engine.document_count, 0)
        self.assertEqual(engine.search("python"), [])

    def test_empty_document(self):
        empty_folder = self.folder / "empty_docs"
        empty_folder.mkdir()

        (empty_folder / "empty.txt").write_text(
            "", encoding="utf-8"
        )

        engine = SearchEngine([empty_folder])

        self.assertEqual(engine.document_count, 0)

    def test_unsupported_file(self):
        unsupported_folder = self.folder / "unsupported"
        unsupported_folder.mkdir()

        (unsupported_folder / "data.xlsx").write_text(
            "Some data", encoding="utf-8"
        )

        engine = SearchEngine([unsupported_folder])

        self.assertEqual(engine.document_count, 0)

    def test_rebuild_handles_extraction_error(self):
        error_folder = self.folder / "errors"
        error_folder.mkdir()

        (error_folder / "broken.txt").write_text(
            "Broken document", encoding="utf-8"
        )

        engine = SearchEngine([error_folder])

        (error_folder / "bad.pdf").touch()

        with patch(
            "backend.search_engine.extract_text",
            side_effect=ValueError("Invalid document")
        ):
            engine.rebuild()

        self.assertEqual(engine.document_count, 0)


if __name__ == "__main__":
    unittest.main()