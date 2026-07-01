from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from automation_tools.aws_s3_backup import backup_to_s3, build_s3_key


class FakeS3Client:
    def __init__(self) -> None:
        self.uploads = []

    def upload_file(self, source: str, bucket: str, key: str) -> None:
        self.uploads.append((source, bucket, key))


class S3BackupTests(unittest.TestCase):
    def test_build_s3_key_uses_prefix_and_relative_path(self) -> None:
        with TemporaryDirectory() as directory:
            source = Path(directory)
            reports = source / "reports"
            reports.mkdir()
            file_path = reports / "january.txt"
            file_path.write_text("data", encoding="utf-8")

            key = build_s3_key(file_path, source, "backups/")

            self.assertEqual(key, "backups/reports/january.txt")

    def test_backup_to_s3_uploads_files_recursively(self) -> None:
        with TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "a.txt").write_text("a", encoding="utf-8")
            nested = source / "nested"
            nested.mkdir()
            (nested / "b.txt").write_text("b", encoding="utf-8")
            client = FakeS3Client()

            result = backup_to_s3(source, "my-bucket", prefix="daily", s3_client=client)

            self.assertEqual(result.uploaded, 2)
            self.assertEqual(
                [upload[2] for upload in client.uploads],
                ["daily/a.txt", "daily/nested/b.txt"],
            )

    def test_backup_to_s3_dry_run_does_not_upload(self) -> None:
        with TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "a.txt").write_text("a", encoding="utf-8")
            client = FakeS3Client()

            result = backup_to_s3(source, "my-bucket", dry_run=True, s3_client=client)

            self.assertEqual(result.uploaded, 1)
            self.assertEqual(client.uploads, [])


if __name__ == "__main__":
    unittest.main()
