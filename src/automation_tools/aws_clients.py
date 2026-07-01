"""Helpers for creating AWS service clients lazily."""

from __future__ import annotations


def create_aws_client(service_name: str, region: str | None = None):
    """Create a boto3 client with a friendly error if boto3 is missing."""

    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError(
            "AWS tools require boto3. Install this project with `python -m pip install -e .`."
        ) from exc

    if region:
        return boto3.client(service_name, region_name=region)

    return boto3.client(service_name)
