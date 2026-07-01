import os
import tempfile
import unittest
from pathlib import Path

from src.main import read_file_code, save_documentation


class MainUtilityTests(unittest.TestCase):
    def test_read_file_code_reads_valid_file(self) -> None:
        source_code = "print('hello')\n"

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"
            file_path.write_text(source_code, encoding="utf-8")

            result = read_file_code(file_path)

        self.assertEqual(result, source_code)

    def test_read_file_code_rejects_missing_file(self) -> None:
        missing_file = Path("missing_example.py")

        with self.assertRaisesRegex(ValueError, "File does not exist"):
            read_file_code(missing_file)

    def test_read_file_code_rejects_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "empty.py"
            file_path.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Source file is empty"):
                read_file_code(file_path)

    def test_save_documentation_creates_expected_markdown_file(self) -> None:
        markdown = "# Test Documentation"
        source_file = Path("example.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                output_path = save_documentation(markdown, source_file)
            finally:
                os.chdir(original_cwd)

            expected_path = Path(temp_dir) / "output" / "example_documentation.md"

            self.assertEqual(output_path, Path("output") / "example_documentation.md")
            self.assertTrue((Path(temp_dir) / "output").is_dir())
            self.assertTrue(expected_path.exists())
            self.assertEqual(expected_path.read_text(encoding="utf-8"), markdown)
