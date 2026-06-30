import os
import shutil
import argparse
from datetime import datetime

EXTENSION_TO_FOLDER = {
    ".txt": "Text Files",
    ".pdf": "PDFs",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp3": "Music",
    ".mp4": "Videos",
    ".docx": "Word Documents",
    ".xlsx": "Excel Files",
    ".pptx": "PowerPoint Files",
    ".zip": "Archives",
}


def get_unique_filename(destination_path):
    """Avoid overwriting files with the same name."""
    if not os.path.exists(destination_path):
        return destination_path

    folder = os.path.dirname(destination_path)
    filename = os.path.basename(destination_path)
    name, extension = os.path.splitext(filename)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{name}_{timestamp}{extension}"

    return os.path.join(folder, new_filename)


def organize_files(target_directory, dry_run=False):
    if not os.path.exists(target_directory):
        print(f"The directory '{target_directory}' does not exist.")
        return

    moved_count = 0
    skipped_count = 0

    for filename in os.listdir(target_directory):
        source_path = os.path.join(target_directory, filename)

        if not os.path.isfile(source_path):
            continue

        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in EXTENSION_TO_FOLDER:
            print(f"Skipped unsupported file: {filename}")
            skipped_count += 1
            continue

        folder_name = EXTENSION_TO_FOLDER[file_extension]
        destination_folder = os.path.join(target_directory, folder_name)
        destination_path = os.path.join(destination_folder, filename)
        destination_path = get_unique_filename(destination_path)

        if dry_run:
            print(f"[DRY RUN] Would move '{filename}' to '{folder_name}'")
        else:
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(source_path, destination_path)
            print(f"Moved '{filename}' to '{folder_name}'")

        moved_count += 1

    print("\nFile organization complete.")
    print(f"Files moved: {moved_count}")
    print(f"Files skipped: {skipped_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument(
        "directory",
        nargs="?",
        default="Documents",
        help="Directory to organize. Default is 'Documents'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files.",
    )

    args = parser.parse_args()
    organize_files(args.directory, args.dry_run)
