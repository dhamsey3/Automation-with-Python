# Automation with Python

A collection of Python automation scripts designed to simplify repetitive tasks and improve productivity.

---

# File Organizer

The **File Organizer** automatically organizes files into folders based on their file extensions. It is a simple yet practical automation tool that demonstrates Python file handling, directory management, and command-line scripting.

Whether you're cleaning up your Downloads or Documents folder, this script helps keep files organized with minimal effort.

---

## Features

* 📂 Organizes files by file extension.
* 📁 Automatically creates destination folders when needed.
* 📝 Supports common document, image, audio, video, and archive formats.
* ⚠️ Prevents overwriting duplicate files by generating unique filenames.
* 🔍 Includes a **dry-run** mode to preview changes before moving files.
* 💻 Supports custom target directories through command-line arguments.
* ✅ Handles invalid or missing directories gracefully.

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
├── file_organizer.py
└── README.md
```

---

## Requirements

* Python 3.8+
* No third-party libraries required.

Built using Python's standard library:

* `os`
* `shutil`
* `argparse`
* `datetime`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dhamsey3/Automation-with-Python.git

cd Automation-with-Python
```

---

## Usage

Organize the default **Documents** directory:

```bash
python file_organizer.py
```

Organize another directory:

```bash
python file_organizer.py Downloads
```

Preview changes without moving files:

```bash
python file_organizer.py Downloads --dry-run
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
* Unit tests.

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
