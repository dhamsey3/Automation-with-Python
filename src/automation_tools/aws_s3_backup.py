"""Upload local files to Amazon S3."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from automation_tools.aws_clients import create_aws_client


@dataclass(frozen=True)
class BackupResult:
    uploaded: int = 0
    skipped: int = 0
    dry_run: bool = False


def iter_files(source: Path, recursive: bool = True) -> list[Path]:
    if source.is_file():
        return [source]

    pattern = "**/*" if recursive else "*"
    return sorted(path for path in source.glob(pattern) if path.is_file())


def build_s3_key(file_path: Path, source: Path, prefix: str = "") -> str:
    base_path = source if source.is_dir() else source.parent
    relative_path = file_path.relative_to(base_path).as_posix()
    clean_prefix = prefix.strip("/")

    if clean_prefix:
        return f"{clean_prefix}/{relative_path}"

    return relative_path


def backup_to_s3(
    source_path: str | Path,
    bucket: str,
    prefix: str = "",
    recursive: bool = True,
    dry_run: bool = False,
    s3_client=None,
) -> BackupResult:
    source = Path(source_path).expanduser()

    if not source.exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    files = iter_files(source, recursive=recursive)
    client = s3_client if dry_run else s3_client or create_aws_client("s3")
    uploaded = 0

    for file_path in files:
        key = build_s3_key(file_path, source, prefix)

        if dry_run:
            print(f"[DRY RUN] Would upload '{file_path}' to s3://{bucket}/{key}")
        else:
            client.upload_file(str(file_path), bucket, key)
            print(f"Uploaded '{file_path}' to s3://{bucket}/{key}")

        uploaded += 1

    print("\nS3 backup complete.")
    print(f"Files uploaded: {uploaded}")

    return BackupResult(uploaded=uploaded, skipped=0, dry_run=dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Back up local files to Amazon S3.")
    parser.add_argument("source", help="File or folder to upload.")
    parser.add_argument("bucket", help="Destination S3 bucket.")
    parser.add_argument("--prefix", default="", help="Optional S3 key prefix.")
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only upload files directly inside the source folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview uploads without sending files to S3.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        backup_to_s3(
            args.source,
            args.bucket,
            prefix=args.prefix,
            recursive=not args.no_recursive,
            dry_run=args.dry_run,
        )
    except (FileNotFoundError, RuntimeError) as exc:
        parser.error(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
