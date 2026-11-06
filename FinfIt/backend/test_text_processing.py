import unittest

from backend.text_processing import (
    tokenize,
    normalize,
    make_snippet,
    STOP_WORDS
)


class TestTextProcessing(unittest.TestCase):

    def test_tokenize_basic(self):
        result = tokenize("Hello World Python")
        self.assertEqual(result, ["hello", "world", "python"])

    def test_tokenize_lowercase(self):
        result = tokenize("SEARCH ENGINE MINING")
        self.assertEqual(result, ["search", "engine", "mining"])

    def test_tokenize_numbers(self):
        result = tokenize("Python 123 C++ 456")
        self.assertEqual(result, ["python", "123", "c", "456"])

    def test_tokenize_special_characters(self):
        result = tokenize("hello@world.com!")
        self.assertEqual(result, ["hello", "world", "com"])

    def test_tokenize_empty_string(self):
        self.assertEqual(tokenize(""), [])

    def test_normalize_remove_stopwords(self):
        result = normalize("the search engine is powerful")
        self.assertEqual(result, ["search", "engine", "powerful"])

    def test_normalize_keep_stopwords(self):
        result = normalize(
            "the search engine",
            remove_stopwords=False
        )
        self.assertEqual(result, ["the", "search", "engine"])

    def test_normalize_empty_string(self):
        self.assertEqual(normalize(""), [])

    def test_stopwords_collection(self):
        self.assertIn("the", STOP_WORDS)
        self.assertIn("and", STOP_WORDS)

    def test_make_snippet_matching_query(self):
        text = "Information retrieval is an important field of computer science."
        result = make_snippet(text, "retrieval")

        self.assertIn("retrieval", result)

    def test_make_snippet_no_match(self):
        text = "Python is a programming language."
        result = make_snippet(text, "database")

        self.assertEqual(result, text)

    def test_make_snippet_empty_text(self):
        result = make_snippet("", "search")
        self.assertEqual(result, "")

    def test_make_snippet_length_limit(self):
        text = "python " * 100
        result = make_snippet(text, "java", length=50)

        self.assertLessEqual(len(result), 51)

    def test_make_snippet_whitespace(self):
        result = make_snippet(
            "Python    is\n\npowerful",
            "python"
        )

        self.assertIn("Python is powerful", result)

    def test_make_snippet_middle_of_long_text(self):
        text = ("A" * 150) + " search " + ("B" * 500)

        result = make_snippet(text, "search", length=100)

        self.assertTrue(result.startswith("…"))
        self.assertTrue(result.endswith("…"))
        self.assertIn("search", result)


if __name__ == "__main__":
    unittest.main()