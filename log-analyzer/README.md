# Log Analyzer

## Description
The Log Analyzer project provides tools to parse, filter, and generate reports from log files. It helps identify errors, warnings, and patterns in application logs efficiently.

## Features
- Parse log files and extract log entries
- Filter logs by severity level (ERROR, WARNING, INFO, DEBUG)
- Search logs by keyword
- Count log entries by level
- Generate comprehensive log analysis reports
- Save reports to file for documentation
- Command-line interface for various analysis options
- Error handling for file operations

## Benefits
- Quickly identify and troubleshoot errors
- Generate reports for compliance and documentation
- Save time manually reviewing large log files
- Useful for system administration and debugging
- Automated analysis of application logs

## Usage

### Generate basic log report:
```bash
python main.py /path/to/logfile.log
```

### Filter logs by severity level:
```bash
python main.py /path/to/logfile.log --filter-level ERROR
```

### Search logs by keyword:
```bash
python main.py /path/to/logfile.log --filter-keyword "database"
```

### Count entries by level:
```bash
python main.py /path/to/logfile.log --count
```

### Generate and save report to file:
```bash
python main.py /path/to/logfile.log --report output_report.txt
```

### Combine multiple filters:
```bash
python main.py /path/to/logfile.log --filter-level WARNING --report warnings.txt
```

## Supported Log Levels
- `ERROR`: Critical errors that need immediate attention
- `WARNING`: Warning messages indicating potential issues
- `INFO`: Informational messages about application state
- `DEBUG`: Detailed debug information

## Output Example
```
Log Analysis Report
==================================================
Log File: app.log
Total Entries: 1,250
Analysis Time: 2024-01-15 14:30:45

Level Summary:
  ERROR: 45
  WARNING: 120
  INFO: 980
  DEBUG: 105

Errors Found: 45
Warnings Found: 120
Info Messages: 980
Debug Messages: 105
==================================================
```

## Libraries and Modules
- `os` module: for file and directory operations
- `logging` module: for logging configuration
- `datetime` module: for timestamp handling
- `argparse` module: for command-line interface

## Report Contents
- Log file path and analysis time
- Total number of entries
- Distribution by severity level
- Error and warning counts
- Summary statistics

## Future Enhancements
- Real-time log monitoring
- Pattern detection and anomaly alerts
- Visualization of log trends
- Export to JSON/CSV formats
- Integration with monitoring systems
- Log rotation and archival
- Performance metrics extraction
