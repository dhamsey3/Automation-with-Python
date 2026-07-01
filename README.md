# Automation with Python

A small collection of command-line Python automation tools designed to simplify repetitive tasks and improve productivity.

## Projects

- **File Organizer**: organizes files into folders based on their extensions.
- **Log Analyzer**: parses log files, filters entries, counts severity levels, and generates reports.
- **AWS S3 Backup**: uploads local files or folders to S3.
- **AWS EC2 Reporter**: lists EC2 instances with state, type, IP, and Name tag.
- **AWS CloudWatch Logs**: downloads recent CloudWatch log events into a text file.

---

## File Organizer

The **File Organizer** automatically organizes files into folders based on their file extensions. It demonstrates Python file handling, directory management, and command-line scripting.

---

## Features

* Organizes files by file extension.
* Automatically creates destination folders when needed.
* Supports common document, image, audio, video, and archive formats.
* Prevents overwriting duplicate files by generating unique filenames.
* Includes a **dry-run** mode to preview changes before moving files.
* Supports custom target directories through command-line arguments.
* Handles invalid or missing directories gracefully.

---

## Supported File Types

| File Type      | Extensions                      |
| -------------- | ------------------------------- |
| Text           | `.txt`                          |
| PDF            | `.pdf`                          |
| Images         | `.jpg`, `.jpeg`, `.png`, `.gif` |
| Music          | `.mp3`                          |
| Videos         | `.mp4`                          |
| Word Documents | `.docx`                         |
| Excel Files    | `.xlsx`                         |
| PowerPoint     | `.pptx`                         |
| Archives       | `.zip`                          |

More file types can easily be added by extending the `EXTENSION_TO_FOLDER` dictionary.

---

## Project Structure

```text
Automation-with-Python/
│
├── README.md
├── pyproject.toml
├── src/
│   └── automation_tools/
│       ├── __init__.py
│       ├── aws_clients.py
│       ├── aws_cloudwatch_logs.py
│       ├── aws_ec2_reporter.py
│       ├── aws_s3_backup.py
│       ├── file_organizer.py
│       └── log_analyzer.py
├── tests/
│   ├── test_aws_cloudwatch_logs.py
│   ├── test_aws_ec2_reporter.py
│   ├── test_aws_s3_backup.py
│   ├── test_file_organizer.py
│   └── test_log_analyzer.py
├── .gitignore
└── .gitattributes
```

---

## Requirements

* Python 3.8+
* `boto3` for AWS tools.

The local file and log tools use Python's standard library. The AWS tools require configured AWS credentials through the normal AWS credential chain, such as environment variables, shared credentials, SSO, or an IAM role.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dhamsey3/Automation-with-Python.git

cd Automation-with-Python
```

---

## Usage

Run directly from the project:

```bash
PYTHONPATH=src python -m automation_tools.file_organizer Downloads --dry-run
PYTHONPATH=src python -m automation_tools.log_analyzer /path/to/app.log
PYTHONPATH=src python -m automation_tools.aws_s3_backup ./Documents my-bucket --prefix documents --dry-run
```

Or install the local package in editable mode:

```bash
python -m pip install -e .
```

Organize your default **Documents** directory:

```bash
file-organizer
```

Organize another directory:

```bash
file-organizer Downloads
```

Preview changes without moving files:

```bash
file-organizer Downloads --dry-run
```

---

## Log Analyzer

Analyze a log file and print a summary report:

```bash
log-analyzer /path/to/app.log
```

Filter by severity:

```bash
log-analyzer /path/to/app.log --filter-level ERROR
```

Search by keyword:

```bash
log-analyzer /path/to/app.log --filter-keyword database
```

Count entries by level:

```bash
log-analyzer /path/to/app.log --count
```

Save a report:

```bash
log-analyzer /path/to/app.log --report output_report.txt
```

---

## AWS Tools

Back up a folder to S3:

```bash
aws-s3-backup ./Documents my-backup-bucket --prefix documents/
```

Preview an S3 backup without uploading:

```bash
aws-s3-backup ./Documents my-backup-bucket --prefix documents/ --dry-run
```

List EC2 instances:

```bash
aws-ec2-report --region us-east-1
```

Download recent CloudWatch logs:

```bash
aws-cloudwatch-logs /aws/lambda/my-function --hours 24 --output lambda_logs.txt --region us-east-1
```

You can analyze downloaded CloudWatch logs with the log analyzer:

```bash
log-analyzer lambda_logs.txt --filter-level ERROR
```

## Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

---

## Example

### Before

```text
Documents/
│
├── report.pdf
├── notes.txt
├── holiday.jpg
├── music.mp3
└── presentation.pptx
```

### After

```text
Documents/
│
├── PDFs/
│   └── report.pdf
│
├── Text Files/
│   └── notes.txt
│
├── Images/
│   └── holiday.jpg
│
├── Music/
│   └── music.mp3
│
└── PowerPoint Files/
    └── presentation.pptx
```

---

## Future Improvements

Possible enhancements include:

* Recursive folder scanning.
* File organization by creation or modification date.
* Duplicate file detection using file hashes.
* Configuration file (YAML or JSON).
* Logging to a file.
* Interactive menu.
* Graphical User Interface (GUI).
* Scheduled automatic organization.

---

## Learning Outcomes

This project demonstrates:

* Python scripting
* File and directory operations
* Command-line applications
* Error handling
* Code organization
* Automation techniques
* Standard library usage

---

## Contributing

Contributions are welcome!

If you'd like to improve the project, feel free to:

* Open an issue
* Submit a pull request
* Suggest new features

---

## License

This project is available for educational and personal use.
