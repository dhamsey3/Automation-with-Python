"""Log Analyzer Module - Analyze and report on log files."""

from .main import parse_log_file, filter_logs_by_level, filter_logs_by_keyword, count_log_entries, generate_log_report, setup_logging

__all__ = ["parse_log_file", "filter_logs_by_level", "filter_logs_by_keyword", "count_log_entries", "generate_log_report", "setup_logging"]
__version__ = "1.0.0"
