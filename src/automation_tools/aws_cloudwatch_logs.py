"""Download CloudWatch log events to a local text file."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from automation_tools.aws_clients import create_aws_client


@dataclass(frozen=True)
class DownloadResult:
    events: int = 0
    output_file: Path | None = None


def utc_milliseconds(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def download_cloudwatch_logs(
    log_group: str,
    output_file: str | Path,
    hours: int = 24,
    region: str | None = None,
    filter_pattern: str = "",
    logs_client=None,
) -> DownloadResult:
    if hours <= 0:
        raise ValueError("hours must be greater than zero.")

    client = logs_client or create_aws_client("logs", region=region)
    output_path = Path(output_file).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    params = {
        "logGroupName": log_group,
        "startTime": utc_milliseconds(start_time),
        "endTime": utc_milliseconds(end_time),
        "interleaved": True,
    }
    if filter_pattern:
        params["filterPattern"] = filter_pattern

    event_count = 0
    with output_path.open("w", encoding="utf-8") as file:
        while True:
            response = client.filter_log_events(**params)
            for event in response.get("events", []):
                timestamp = datetime.fromtimestamp(
                    event["timestamp"] / 1000,
                    tz=timezone.utc,
                ).isoformat()
                stream = event.get("logStreamName", "-")
                message = event.get("message", "").rstrip("\n")
                file.write(f"{timestamp} {stream} {message}\n")
                event_count += 1

            next_token = response.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    print(f"Downloaded {event_count} log events to {output_path}")
    return DownloadResult(events=event_count, output_file=output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download CloudWatch log events.")
    parser.add_argument("log_group", help="CloudWatch log group name.")
    parser.add_argument(
        "--output",
        default="cloudwatch_logs.txt",
        help="Output text file. Defaults to cloudwatch_logs.txt.",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="How many recent hours of logs to download.",
    )
    parser.add_argument("--region", help="AWS region, for example us-east-1.")
    parser.add_argument("--filter-pattern", default="", help="CloudWatch filter pattern.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        download_cloudwatch_logs(
            args.log_group,
            args.output,
            hours=args.hours,
            region=args.region,
            filter_pattern=args.filter_pattern,
        )
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
