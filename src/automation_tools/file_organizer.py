"""Organize files into folders based on their extensions."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


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


@dataclass(frozen=True)
class OrganizationResult:
    """Summary of a file organization run."""

    moved: int = 0
    skipped: int = 0
    dry_run: bool = False


def get_unique_destination(destination_path: Path) -> Path:
    """Return a non-conflicting destination path."""

    if not destination_path.exists():
        return destination_path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = destination_path.with_name(
        f"{destination_path.stem}_{timestamp}{destination_path.suffix}"
    )

    counter = 1
    while candidate.exists():
        candidate = destination_path.with_name(
            f"{destination_path.stem}_{timestamp}_{counter}{destination_path.suffix}"
        )
        counter += 1

    return candidate


def organize_files(
    target_directory: str | Path,
    dry_run: bool = False,
    extension_map: dict[str, str] | None = None,
) -> OrganizationResult:
    """Organize files in ``target_directory`` by extension."""

    target_path = Path(target_directory).expanduser()
    folders_by_extension = extension_map or EXTENSION_TO_FOLDER

    if not target_path.exists():
        raise FileNotFoundError(f"The directory '{target_path}' does not exist.")

    if not target_path.is_dir():
        raise NotADirectoryError(f"'{target_path}' is not a directory.")

    moved_count = 0
    skipped_count = 0

    for source_path in sorted(target_path.iterdir()):
        if not source_path.is_file():
            continue

        folder_name = folders_by_extension.get(source_path.suffix.lower())
        if folder_name is None:
            print(f"Skipped unsupported file: {source_path.name}")
            skipped_count += 1
            continue

        destination_folder = target_path / folder_name
        destination_path = get_unique_destination(destination_folder / source_path.name)

        if dry_run:
            print(f"[DRY RUN] Would move '{source_path.name}' to '{folder_name}'")
        else:
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(source_path), str(destination_path))
            print(f"Moved '{source_path.name}' to '{folder_name}'")

        moved_count += 1

    print("\nFile organization complete.")
    print(f"Files moved: {moved_count}")
    print(f"Files skipped: {skipped_count}")

    return OrganizationResult(moved=moved_count, skipped=skipped_count, dry_run=dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(Path.home() / "Documents"),
        help="Directory to organize. Defaults to your Documents folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        organize_files(args.directory, args.dry_run)
    except (FileNotFoundError, NotADirectoryError) as exc:
        parser.error(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
