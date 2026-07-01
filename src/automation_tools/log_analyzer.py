"""Parse, filter, and report on application log files."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re


LOG_LEVELS = ("ERROR", "WARNING", "INFO", "DEBUG")
LEVEL_PATTERN = re.compile(r"\b(ERROR|WARNING|WARN|INFO|DEBUG)\b", re.IGNORECASE)


@dataclass(frozen=True)
class LogEntry:
    line_number: int
    level: str
    message: str


def normalize_level(level: str) -> str:
    normalized = level.upper()
    return "WARNING" if normalized == "WARN" else normalized


def parse_log_file(log_file: str | Path) -> list[LogEntry]:
    path = Path(log_file).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"The log file '{path}' does not exist.")

    if not path.is_file():
        raise IsADirectoryError(f"'{path}' is not a file.")

    entries: list[LogEntry] = []
    with path.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            message = line.rstrip("\n")
            match = LEVEL_PATTERN.search(message)
            if match:
                entries.append(
                    LogEntry(
                        line_number=line_number,
                        level=normalize_level(match.group(1)),
                        message=message,
                    )
                )

    return entries


def filter_entries(
    entries: list[LogEntry],
    level: str | None = None,
    keyword: str | None = None,
) -> list[LogEntry]:
    filtered = entries

    if level:
        normalized_level = normalize_level(level)
        filtered = [entry for entry in filtered if entry.level == normalized_level]

    if keyword:
        search_term = keyword.casefold()
        filtered = [
            entry for entry in filtered if search_term in entry.message.casefold()
        ]

    return filtered


def count_by_level(entries: list[LogEntry]) -> Counter[str]:
    return Counter(entry.level for entry in entries)


def build_report(log_file: str | Path, entries: list[LogEntry]) -> str:
    counts = count_by_level(entries)
    path = Path(log_file).expanduser()
    lines = [
        "Log Analysis Report",
        "=" * 50,
        f"Log File: {path}",
        f"Total Entries: {len(entries):,}",
        f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Level Summary:",
    ]

    for level in LOG_LEVELS:
        lines.append(f"  {level}: {counts.get(level, 0):,}")

    lines.extend(
        [
            "",
            f"Errors Found: {counts.get('ERROR', 0):,}",
            f"Warnings Found: {counts.get('WARNING', 0):,}",
            f"Info Messages: {counts.get('INFO', 0):,}",
            f"Debug Messages: {counts.get('DEBUG', 0):,}",
            "=" * 50,
        ]
    )

    return "\n".join(lines)


def format_entries(entries: list[LogEntry]) -> str:
    if not entries:
        return "No matching log entries found."

    return "\n".join(
        f"{entry.line_number}: [{entry.level}] {entry.message}" for entry in entries
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze log files.")
    parser.add_argument("log_file", help="Path to the log file to analyze.")
    parser.add_argument(
        "--filter-level",
        choices=LOG_LEVELS,
        help="Only show entries with this severity level.",
    )
    parser.add_argument(
        "--filter-keyword",
        help="Only show entries containing this keyword.",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Print counts by log level.",
    )
    parser.add_argument(
        "--report",
        help="Save the analysis report to this file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        entries = parse_log_file(args.log_file)
    except (FileNotFoundError, IsADirectoryError) as exc:
        parser.error(str(exc))

    filtered_entries = filter_entries(
        entries,
        level=args.filter_level,
        keyword=args.filter_keyword,
    )

    if args.count:
        counts = count_by_level(filtered_entries)
        for level in LOG_LEVELS:
            print(f"{level}: {counts.get(level, 0)}")
    elif args.filter_level or args.filter_keyword:
        print(format_entries(filtered_entries))
    else:
        print(build_report(args.log_file, entries))

    if args.report:
        report_path = Path(args.report).expanduser()
        report_path.write_text(build_report(args.log_file, filtered_entries), encoding="utf-8")
        print(f"\nReport saved to {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
