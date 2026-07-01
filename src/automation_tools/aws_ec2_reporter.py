"""Generate a compact report of EC2 instances."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from automation_tools.aws_clients import create_aws_client


@dataclass(frozen=True)
class EC2Instance:
    instance_id: str
    state: str
    instance_type: str
    public_ip: str
    name: str


def get_tag_value(tags: list[dict] | None, key: str, default: str = "") -> str:
    for tag in tags or []:
        if tag.get("Key") == key:
            return tag.get("Value", default)

    return default


def list_ec2_instances(region: str | None = None, ec2_client=None) -> list[EC2Instance]:
    client = ec2_client or create_aws_client("ec2", region=region)
    paginator = client.get_paginator("describe_instances")
    instances: list[EC2Instance] = []

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append(
                    EC2Instance(
                        instance_id=instance.get("InstanceId", ""),
                        state=instance.get("State", {}).get("Name", "unknown"),
                        instance_type=instance.get("InstanceType", ""),
                        public_ip=instance.get("PublicIpAddress", ""),
                        name=get_tag_value(instance.get("Tags"), "Name", ""),
                    )
                )

    return instances


def format_instances(instances: list[EC2Instance]) -> str:
    if not instances:
        return "No EC2 instances found."

    rows = ["Instance ID          State      Type          Public IP        Name"]
    rows.append("-" * 72)

    for instance in instances:
        rows.append(
            f"{instance.instance_id:<20} "
            f"{instance.state:<10} "
            f"{instance.instance_type:<13} "
            f"{instance.public_ip or '-':<16} "
            f"{instance.name or '-'}"
        )

    return "\n".join(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List EC2 instances in a region.")
    parser.add_argument("--region", help="AWS region, for example us-east-1.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        print(format_instances(list_ec2_instances(region=args.region)))
    except RuntimeError as exc:
        parser.error(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
