from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from automation_tools.log_analyzer import (
    build_report,
    count_by_level,
    filter_entries,
    parse_log_file,
)


class LogAnalyzerTests(unittest.TestCase):
    def test_parse_log_file_extracts_supported_levels(self) -> None:
        with TemporaryDirectory() as directory:
            log_file = Path(directory) / "app.log"
            log_file.write_text(
                "\n".join(
                    [
                        "2026-01-01 INFO Application started",
                        "2026-01-01 WARN Disk space low",
                        "This line has no level",
                        "2026-01-01 ERROR Database unavailable",
                    ]
                ),
                encoding="utf-8",
            )

            entries = parse_log_file(log_file)

            self.assertEqual([entry.level for entry in entries], ["INFO", "WARNING", "ERROR"])
            self.assertEqual(entries[1].line_number, 2)

    def test_filter_entries_by_level_and_keyword(self) -> None:
        with TemporaryDirectory() as directory:
            log_file = Path(directory) / "app.log"
            log_file.write_text(
                "\n".join(
                    [
                        "INFO cache warm",
                        "ERROR database timeout",
                        "ERROR payment timeout",
                    ]
                ),
                encoding="utf-8",
            )

            entries = parse_log_file(log_file)
            filtered = filter_entries(entries, level="ERROR", keyword="database")

            self.assertEqual(len(filtered), 1)
            self.assertIn("database", filtered[0].message)

    def test_count_by_level(self) -> None:
        with TemporaryDirectory() as directory:
            log_file = Path(directory) / "app.log"
            log_file.write_text("DEBUG x\nINFO y\nERROR z\nERROR z2\n", encoding="utf-8")

            counts = count_by_level(parse_log_file(log_file))

            self.assertEqual(counts["DEBUG"], 1)
            self.assertEqual(counts["INFO"], 1)
            self.assertEqual(counts["ERROR"], 2)

    def test_build_report_includes_summary(self) -> None:
        with TemporaryDirectory() as directory:
            log_file = Path(directory) / "app.log"
            log_file.write_text("INFO ready\nWARNING slow\n", encoding="utf-8")

            report = build_report(log_file, parse_log_file(log_file))

            self.assertIn("Log Analysis Report", report)
            self.assertIn("Total Entries: 2", report)
            self.assertIn("WARNING: 1", report)


if __name__ == "__main__":
    unittest.main()
