from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from automation_tools.file_organizer import get_unique_destination, organize_files


class FileOrganizerTests(unittest.TestCase):
    def test_organize_files_moves_supported_files(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "notes.txt").write_text("hello", encoding="utf-8")
            (target / "photo.JPG").write_text("image", encoding="utf-8")
            (target / "script.py").write_text("print('hi')", encoding="utf-8")

            result = organize_files(target)

            self.assertEqual(result.moved, 2)
            self.assertEqual(result.skipped, 1)
            self.assertTrue((target / "Text Files" / "notes.txt").exists())
            self.assertTrue((target / "Images" / "photo.JPG").exists())
            self.assertTrue((target / "script.py").exists())

    def test_organize_files_dry_run_does_not_move_files(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "report.pdf").write_text("pdf", encoding="utf-8")

            result = organize_files(target, dry_run=True)

            self.assertEqual(result.moved, 1)
            self.assertTrue(result.dry_run)
            self.assertTrue((target / "report.pdf").exists())
            self.assertFalse((target / "PDFs").exists())

    def test_get_unique_destination_avoids_overwriting(self) -> None:
        with TemporaryDirectory() as directory:
            destination = Path(directory) / "notes.txt"
            destination.write_text("existing", encoding="utf-8")

            unique_destination = get_unique_destination(destination)

            self.assertNotEqual(unique_destination, destination)
            self.assertTrue(unique_destination.name.startswith("notes_"))
            self.assertEqual(unique_destination.suffix, ".txt")

    def test_organize_files_rejects_missing_directory(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                organize_files(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
