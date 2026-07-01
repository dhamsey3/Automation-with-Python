from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from automation_tools.aws_ec2_reporter import format_instances, list_ec2_instances


class FakePaginator:
    def paginate(self):
        return [
            {
                "Reservations": [
                    {
                        "Instances": [
                            {
                                "InstanceId": "i-123",
                                "State": {"Name": "running"},
                                "InstanceType": "t3.micro",
                                "PublicIpAddress": "203.0.113.10",
                                "Tags": [{"Key": "Name", "Value": "web"}],
                            }
                        ]
                    }
                ]
            }
        ]


class FakeEC2Client:
    def get_paginator(self, operation_name: str):
        self.operation_name = operation_name
        return FakePaginator()


class EC2ReporterTests(unittest.TestCase):
    def test_list_ec2_instances_maps_response(self) -> None:
        client = FakeEC2Client()

        instances = list_ec2_instances(ec2_client=client)

        self.assertEqual(client.operation_name, "describe_instances")
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0].instance_id, "i-123")
        self.assertEqual(instances[0].name, "web")

    def test_format_instances_handles_empty_list(self) -> None:
        self.assertEqual(format_instances([]), "No EC2 instances found.")

    def test_format_instances_includes_instance_data(self) -> None:
        instances = list_ec2_instances(ec2_client=FakeEC2Client())

        output = format_instances(instances)

        self.assertIn("i-123", output)
        self.assertIn("running", output)
        self.assertIn("web", output)


if __name__ == "__main__":
    unittest.main()
