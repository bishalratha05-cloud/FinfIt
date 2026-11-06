import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from backend.document_loader import extract_text


class TestDocumentLoader(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_extract_txt(self):
        file = self.folder / "test.txt"
        file.write_text("FinfIt Information Retrieval", encoding="utf-8")

        result = extract_text(file)

        self.assertEqual(result, "FinfIt Information Retrieval")

    def test_extract_pdf(self):
        file = self.folder / "test.pdf"
        file.touch()

        mock_reader = SimpleNamespace(
            pages=[
                SimpleNamespace(extract_text=lambda: "PDF content"),
                SimpleNamespace(extract_text=lambda: None)
            ]
        )

        with patch.dict("sys.modules", {
            "pypdf": SimpleNamespace(
                PdfReader=lambda path: mock_reader
            )
        }):
            result = extract_text(file)

        self.assertEqual(result, "PDF content\n")

    def test_extract_docx(self):
        file = self.folder / "test.docx"
        file.touch()

        mock_doc = SimpleNamespace(
            paragraphs=[
                SimpleNamespace(text="First paragraph"),
                SimpleNamespace(text="Second paragraph")
            ]
        )

        with patch.dict("sys.modules", {
            "docx": SimpleNamespace(
                Document=lambda path: mock_doc
            )
        }):
            result = extract_text(file)

        self.assertEqual(
            result,
            "First paragraph\nSecond paragraph"
        )

    def test_unsupported_format(self):
        file = self.folder / "test.xlsx"
        file.touch()

        with self.assertRaises(ValueError):
            extract_text(file)

    def test_empty_txt(self):
        file = self.folder / "empty.txt"
        file.write_text("", encoding="utf-8")

        result = extract_text(file)

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
    