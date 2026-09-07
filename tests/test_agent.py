"""Focused tests for the collector contract and CLI serialization."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from collectors.services import ServicesCollector
from collectors.smart import SmartCollector
from proxmox_agent import main


class AgentTests(unittest.TestCase):
    """Verify stdout remains valid JSON and service calls stay batched."""

    @patch("collectors.services.run_result", return_value=("active\ninactive\nfailed\n", 3))
    def test_services_payload(self, run_command: object) -> None:
        with patch("sys.stdout") as stdout:
            ServicesCollector().collect()
        self.assertEqual(run_command.call_count, 1)

    @patch("collectors.smart.run_result")
    def test_smart_requests_complete_json(self, run_command: object) -> None:
        run_command.side_effect = [
            ("sda disk\n", 0),
            ('{"smart_status":{"passed":true},"temperature":{"current":32}}', 0),
        ]
        payload = SmartCollector().collect()
        self.assertEqual(payload["devices"]["sda"]["health"], 1)
        self.assertEqual(payload["devices"]["sda"]["temperature"], 32)
        self.assertEqual(payload["data"], [{"{#DEVICE}": "sda"}])
        self.assertEqual(run_command.call_args_list[1].args[0][1:3], ["--all", "--json"])

    def test_smart_excludes_virtual_devices_when_sysfs_is_available(self) -> None:
        with patch("collectors.smart.Path.exists", side_effect=[True, True, False]):
            self.assertEqual(SmartCollector._physical_disks(["sda disk", "zd0 disk"]), ["sda"])

    @patch("collectors.journal.run_result")
    def test_journal_ignores_generic_error_messages(self, run_command: object) -> None:
        run_command.return_value = ('{"MESSAGE":"generic error","PRIORITY":"3","_SYSTEMD_UNIT":"cron.service"}\n', 0)
        from collectors.journal import JournalCollector

        self.assertEqual(JournalCollector().collect()["proxmox_error"], 0)
        self.assertEqual(run_command.call_args.args[0][2:4], ["--since", "10 minutes ago"])

    @patch("proxmox_agent.create")
    def test_main_writes_json(self, create: object) -> None:
        create.return_value.collect.return_value = {"health": 1}
        with patch("sys.stdout") as stdout:
            main(["api"])
            output = "".join(call.args[0] for call in stdout.write.call_args_list)
        self.assertEqual(json.loads(output), {"health": 1})


if __name__ == "__main__":
    unittest.main()