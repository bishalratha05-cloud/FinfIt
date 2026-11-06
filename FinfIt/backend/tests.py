import unittest
import tempfile
from pathlib import Path

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
            "Information retrieval finds relevant documents using search.",
            encoding="utf-8"
        )

        (self.folder / "data_mining.txt").write_text(
            "Data mining discovers useful patterns in large datasets.",
            encoding="utf-8"
        )

        self.engine = SearchEngine([self.folder])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_document_loading(self):

        self.assertEqual(
            self.engine.document_count, 3
        )

    def test_bm25_search(self):

        results = self.engine.search(
            "machine learning",
            method="bm25"
        )

        self.assertGreater(len(results), 0)

        self.assertIn(
            "machine_learning.txt",
            results[0]["title"]
        )

    def test_tfidf_search(self):

        results = self.engine.search(
            "information retrieval",
            method="tfidf"
        )

        self.assertGreater(len(results), 0)

    def test_boolean_search(self):

        results = self.engine.search(
            "machine AND learning",
            mode="boolean"
        )

        self.assertGreater(len(results), 0)

    def test_phrase_search(self):

        results = self.engine.search(
            "machine learning",
            mode="phrase"
        )

        self.assertGreater(len(results), 0)

    def test_document_listing(self):

        documents = self.engine.list_documents()

        self.assertEqual(len(documents), 3)

    def test_statistics(self):

        stats = self.engine.get_statistics()

        self.assertEqual(stats["total_documents"], 3)

        self.assertGreater(
            stats["vocabulary_size"], 0
        )


if __name__ == "__main__":
    unittest.main()