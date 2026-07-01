from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from automation_tools.aws_cloudwatch_logs import download_cloudwatch_logs


class FakeLogsClient:
    def __init__(self) -> None:
        self.calls = []

    def filter_log_events(self, **kwargs):
        self.calls.append(kwargs)
        if "nextToken" not in kwargs:
            return {
                "events": [
                    {
                        "timestamp": 1700000000000,
                        "logStreamName": "stream-a",
                        "message": "INFO first",
                    }
                ],
                "nextToken": "token-1",
            }

        return {
            "events": [
                {
                    "timestamp": 1700000001000,
                    "logStreamName": "stream-b",
                    "message": "ERROR second",
                }
            ]
        }


class CloudWatchLogsTests(unittest.TestCase):
    def test_download_cloudwatch_logs_writes_paginated_events(self) -> None:
        with TemporaryDirectory() as directory:
            output_file = Path(directory) / "logs.txt"
            client = FakeLogsClient()

            result = download_cloudwatch_logs(
                "/aws/lambda/example",
                output_file,
                hours=1,
                filter_pattern="ERROR",
                logs_client=client,
            )

            contents = output_file.read_text(encoding="utf-8")
            self.assertEqual(result.events, 2)
            self.assertIn("INFO first", contents)
            self.assertIn("ERROR second", contents)
            self.assertEqual(client.calls[0]["filterPattern"], "ERROR")
            self.assertEqual(client.calls[1]["nextToken"], "token-1")

    def test_download_cloudwatch_logs_rejects_invalid_hours(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                download_cloudwatch_logs(
                    "/aws/lambda/example",
                    Path(directory) / "logs.txt",
                    hours=0,
                    logs_client=FakeLogsClient(),
                )


if __name__ == "__main__":
    unittest.main()
